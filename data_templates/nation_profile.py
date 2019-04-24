import ast
import sys
from configparser import ConfigParser
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

MONGO_HOST = 'mongodb://localhost/'
FILE_NAME = 'races.ini'

keywords = ['Donald Trump', 'illegal immigration', 'border wall', 'health care', 'ACA', 'Obamacare']

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

def build_sentiment_profile(politician, collection):
    analyzer = SentimentIntensityAnalyzer()
    entries = gather_tweets(politician, collection)
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
    return (ave_score, count)

if __name__ == "__main__":
    client = MongoClient(MONGO_HOST)
    config = ConfigParser()
    house = client.housedb.presort
    senate = client.senatedb.presort
    misc = client.miscdb.misc
    f = open('misc_sentiment.csv')
    f.write("Search Term, Sen_compound, house_compound, misc_compound, sen_count, house_count, misc_count\n")
    for i in keywords:
        sen_sent, sen_count = build_sentiment_profile(keyword, senate)
        house_sent, house_count = build_sentiment_profile(keyword, house)
        misc_sent, misc_count = build_sentiment_profile(keyword, misc)
        line = str(i) + ',' + str(sen_sent) + ',' + str(house_sent) + ',' + str(misc_sent) + ',' + str(sen_count) + ',' + str(house_count) + ',' + str(misc_count) + '\n'
        f.write(line)
    f.close()
