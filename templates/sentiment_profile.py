import ast
import sys
from configparser import ConfigParser
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

MONGO_HOST = 'mongodb://localhost/housedb'
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
    db = client.housedb
    presort = db.presort
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
        if (sentiment['compound'] < 0):
            neg_tweets += 1
        ave_score += sentiment['compound']
        count += 1
    print("Average score:", ave_score/count, "Positive Tweets:", pos_tweets,
            "Negative Tweets:", neg_tweets, "Neutral Tweets:", neu_tweets)
