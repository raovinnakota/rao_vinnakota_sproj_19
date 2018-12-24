from pymongo import MongoClient

MONGO_HOST = 'mongodb://localhost/miscdb'
client = MongoClient(MONGO_HOST)
db = client.miscdb
misc = db.misc
cursor = misc.find()
democrats = []
republicans = []
for tweet in cursor:
    dict_tweet = dict(tweet)
    if "#democrats" in dict_tweet.text:
        democrats.append(dict_tweet.text)
    elif "#gop" in dict_tweet.text:
        republicans.append(dict_tweet.text)
    print("Democrats" + str(len(democrats)) + "\nRepublicans" + str(len(republicans)))
