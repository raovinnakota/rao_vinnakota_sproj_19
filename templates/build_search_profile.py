import ast
import sys
from configparser import ConfigParser
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

MONGO_HOST = 'mongodb://localhost/'
FILE_NAME = 'races.ini'
keywords = ["#midterms", "#vote", "#bluewave", "#redwave", "#democrats", "#elections", "#gop", "#usa"]
#POLITICIAN = sys.argv[1]
DB = sys.argv[1]

def section_to_dict(section, parser):
    #change path to your ini file if running locally
    parser.read(FILE_NAME)
    out_dict = {}
    for key in parser[section]:
        temp = ast.literal_eval(parser[section][key])
        out_dict[temp[-1]] = temp[:-1]
    return(out_dict)

def gather_tweets(phrase, collection):
    cursor = collection.find({"text": {"$regex" : phrase, "$options": "$i"}})
    entries = [entry for entry in cursor]
    return(entries)

def strip_tweet(text):
    text = text.replace('\n', '')
    return(text)

def build_sentiment_profile(politician, db_choice):
    client = MongoClient(MONGO_HOST)
    analyzer = SentimentIntensityAnalyzer()
    if db_choice == 'house':
        db = client.housedb
        presort = db.presort
    if db_choice == 'senate':
        db = client.senatedb
        presort = db.presort
    if db_choice == 'misc':
        db = client.miscdb
        presort = db.misc
    entries = gather_tweets(politician, presort)
    ave_score = 0
    pos_tweets = 0
    neg_tweets = 0
    neu_tweets = 0
    count = 0
    for i in entries:
        tweet = strip_tweet(i['text'])
        sentiment = analyzer.polarity_scores(tweet)
        if (sentiment['compound'] == 0):
            neu_tweets += 1
        if (sentiment['compound'] > 0):
            pos_tweets += 1
        if (sentiment['compound'] < 0):
            neg_tweets += 1
        ave_score += sentiment['compound']
        count += 1
    return (ave_score, pos_tweets, neg_tweets, neu_tweets, count)

if __name__ == "__main__":
    config = ConfigParser()
    if DB == 'senate':
        senate = section_to_dict('SENATE', config)
        f = open('senate_profile.csv', 'w+')
        f.write('Search Term,Race,Count,Pos Tweets,Neg Tweets,Neu Tweets,Average Compound\n')
        for i in senate:
            print(i)
            for term in senate[i]:
                ave_score, pos_tweets, neg_tweets, neu_tweets, count = build_sentiment_profile(term, 'senate')
                if (count > 0):
                    line = str(term) + ',' + str(i) + ',' + str(count) + ',' + str(pos_tweets) + ',' + str(neg_tweets) + ',' + str(neu_tweets) + ',' + str(ave_score/count) + '\n'
                else:
                    line = str(term) + ',' + str(i) + ",0,0,0,0,0\n"
                f.write(line)
    if DB == 'house':
        senate = section_to_dict('HOUSE', config)
        f = open('house_profile.csv', 'w+')
        f.write('Search Term,Race,Count,Pos Tweets,Neg Tweets,Neu Tweets,Average Compound\n')
        for i in senate:
            print(i)
            for term in senate[i]:
                ave_score, pos_tweets, neg_tweets, neu_tweets, count = build_sentiment_profile(term, 'house')
                if (count > 0):
                    line = str(term) + ',' + str(i) + ',' + str(count) + ',' + str(pos_tweets) + ',' + str(neg_tweets) + ',' + str(neu_tweets) + ',' + str(ave_score/count) + '\n'
                else:
                    line = str(term) + ',' + str(i) + ",0,0,0,0,0\n"
                f.write(line)
    if DB == 'misc':
        f = open('misc_profile.csv', 'w+')
        f.write('Search Term,Count,Pos Tweets,Neg Tweets,Neu Tweets,Average Compound\n')
        for i in keywords:
            print(i)
            ave_score, pos_tweets, neg_tweets, neu_tweets, count = build_sentiment_profile(i, 'senate')
            line = str(i) + ',' + str(count) + ',' + str(pos_tweets) + ',' + str(neg_tweets) + ',' + str(neu_tweets) + ',' + str(ave_score/count) + '\n'
            f.write(line)
        f.close()
    f.close()
