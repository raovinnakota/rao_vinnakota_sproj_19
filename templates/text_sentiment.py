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
    return(tweet, sentiment)

if __name__ == '__main__':
    client = MongoClient(MONGO_HOST)
    db = client.miscdb
    presort = db.misc
    cursor = presort.find()
    f = open('sentiment.csv', 'w+')
    #f.write("Text,Compound,Pos,Neg,Neu\n")
    count = 0
    for i in cursor:
        count += 1
        while count < 284608:
            continue
        tweet, sentiment = build_sentiment_profile(i['text'])
        print(count, tweet)
        line = (str(tweet) + ',' + str(sentiment['compound']) +
        ',' + str(sentiment['pos']) + ',' + str(sentiment['neg']) +
        ',' + str(sentiment['neu']) + '\n')
        f.write(line)
    f.close()
