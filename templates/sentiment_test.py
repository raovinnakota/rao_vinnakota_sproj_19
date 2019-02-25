import ast
import sys
from configparser import ConfigParser
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

MONGO_HOST = 'mongodb://localhost/housedb'

def gather_tweets(phrase, collection):
    cursor = collection.find({"text": {"$regex" : phrase, "$options": "$i"}})
    entries = [entry for entry in cursor]
    return(entries)

def strip_tweet(text):
    text.replace('\n', '')

if __name__ == "__main__":
    config = ConfigParser()
    client = MongoClient(MONGO_HOST)
    analyzer = SentimentIntensityAnalyzer()
    db = client.housedb
    presort = db.presort
    entries = gather_tweets("Donald Trump", presort)
    #f = open('trump_sentiment.csv', 'w+')
    #f.write('Tweet, Pos, Neu, Com,\n')
    for i in entries:
        tweet = strip_tweet(i['text'])
        sentiment = analyzer.polarity_scores(sentence)
        print(tweet, sentiment)

    #senate = section_to_dict('HOUSE', config)
    #f = open('house_count.csv', 'w+')
    #f.write('Race,Tweets\n')
    #for i in senate:
    #    print(i)
    #    count = gather_tweets(i, presort)
    #    print(count)
    #    f.write(i + ',' + str(count) + '\n')
    #f.close()
