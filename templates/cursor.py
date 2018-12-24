from pymongo import MongoClient

MONGO_HOST = 'mongodb://localhost/miscdb'
CLIENT = MongoClient(MONGO_HOST)
db = client.miscdb
misc = db.misc
cursor = misc.find()
democrats = []
republicans = []
for tweet in cursor:
    if "#democrats" in tweet.text:
        democrats.append(tweet.text)
    else if "#gop" in tweet.text:
        republicans.append(tweet.text)
    print("Democrats" + str(len(democrats)) + "\nRepublicans" + str(len(republicans)))
