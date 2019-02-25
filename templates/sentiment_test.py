import ast
from configparser import ConfigParser
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

MONGO_HOST = 'mongodb://localhost/housedb'

def gather_tweets(phrase, collection):
    cursor = collection.find({"text": {"$regex" : phrase, "$options": "$i"}})
    entries = list(cursor[:])
    return(entries)


if __name__ == "__main__":
    config = ConfigParser()
    client = MongoClient(MONGO_HOST)
    db = client.housedb
    presort = db.presort
    entries = gather_tweets("Donald Trump", presort)
    print(len(entries))
    #senate = section_to_dict('HOUSE', config)
    #f = open('house_count.csv', 'w+')
    #f.write('Race,Tweets\n')
    #for i in senate:
    #    print(i)
    #    count = gather_tweets(i, presort)
    #    print(count)
    #    f.write(i + ',' + str(count) + '\n')
    #f.close()
