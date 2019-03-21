import sys
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

MONGO_HOST = 'mongodb://localhost/'
FILE_NAME = 'sentiment.csv'

def strip_tweet(text):
    text = text.replace('\n', '')
    text = text.replace(',',' ')
    return(text)

def build_sentiment_profile(text):
    analyzer = SentimentIntensityAnalyzer()
    tweet = strip_tweet(text)
    sentiment = analyzer.polarity_scores(tweet)
    return(sentiment)

if __name__ == '__main__':
    client = MongoClient(MONGO_HOST)
    db = client.miscdb
    presort = db.presort
    cursor = presort.find()
    for i in cursor:
        print(build_sentiment_profile(text))
    
