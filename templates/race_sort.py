import datetime
import ast
from configparser import ConfigParser
from pymongo import MongoClient

FILE_NAME = 'races.ini'
MONGO_HOST = 'mongodb://localhost/senatedb'

def section_to_dict(section, parser):
    #change path to your ini file if running locally
    parser.read(FILE_NAME)
    out_dict = {}
    for key in parser[section]:
        temp = ast.literal_eval(parser[section][key])
        out_dict[temp[-1]] = temp
    return(out_dict)

def gather_tweets(race, collection):
    total = 0
    for i in race:
        cursor = collection.find({"text": {"$regex" : i , "$options": "$i"}})
        total += cursor.count()
    return(total)

if __name__ == "__main__":
    config = ConfigParser()
    client = MongoClient(MONGO_HOST)
    db = client.senatedb
    presort = db.presort
    senate = section_to_dict('SENATE', config)
    f = open('race_count.txt', 'w+')
    f.write('Race,Tweets\n')
    for i in senate:
        print(i)
        f.write(i + ',' + str(gather_tweets(i, presort)) + '\n')
