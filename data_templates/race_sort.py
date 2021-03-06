import datetime
import ast
from configparser import ConfigParser
from pymongo import MongoClient

FILE_NAME = 'races.ini'
MONGO_HOST = 'mongodb://localhost/housedb'

def section_to_dict(section, parser):
    #change path to your ini file if running locally
    parser.read(FILE_NAME)
    out_dict = {}
    for key in parser[section]:
        temp = ast.literal_eval(parser[section][key])
        out_dict[temp[-1]] = temp[:-1]
    return(out_dict)

def gather_tweets(race, collection):
    total = 0
    for i in race:
        count = collection.find({"text": {"$regex" : i , "$options": "$i"}}).count()
        print(count)
        total += count
    return(total)

if __name__ == "__main__":
    config = ConfigParser()
    client = MongoClient(MONGO_HOST)
    db = client.housedb
    presort = db.presort
    senate = section_to_dict('HOUSE', config)
    f = open('house_count.csv', 'w+')
    f.write('Race,Tweets\n')
    for i in senate:
        print(i)
        count = gather_tweets(i, presort)
        print(count)
        f.write(i + ',' + str(count) + '\n')
    f.close()
