import ast
import sys
from configparser import ConfigParser
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

MONGO_HOST = 'mongodb://localhost/miscdb'
POLITICIAN = sys.argv[1]

def gather_tweets(phrase, collection):
    cursor = collection.find({"text": {"$regex" : phrase, "$options": "$i"}})
    entries = [entry for entry in cursor]
    return(entries)

def strip_tweet(text):
    text = text.replace('\n', '')
    return(text)

if __name__ == "__main__":
    config = ConfigParser()
    client = MongoClient(MONGO_HOST)
    analyzer = SentimentIntensityAnalyzer()
    db = client.miscdb
    presort = db.misc
    entries = gather_tweets(POLITICIAN, presort)
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
        if (sentiments['compound'] < 0):
            neg_tweets += 1
        ave_score += sentiment['conmpound']
        count += 1
    return(ave_score/count, pos_tweets, neg_tweets, neu_tweets)
