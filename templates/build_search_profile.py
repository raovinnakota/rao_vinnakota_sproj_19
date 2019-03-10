import ast
import sys
from configparser import ConfigParser
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

MONGO_HOST = 'mongodb://localhost/'
#POLITICIAN = sys.argv[1]
#DB = sys.argv[2]

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
    senate = section_to_dict(SENATE)
    test_list = senate[0]
    f = open('senate_profile.csv')
    f.write('Search Term,Pos Tweets,Neg Tweets,Neu Tweets,Average Compound\n')
    for i in senate:
        for term in senate[i]:
            ave_score, pos_tweets, neg_tweets, neu_tweets, count = build_sentiment_profile(term, senate)
