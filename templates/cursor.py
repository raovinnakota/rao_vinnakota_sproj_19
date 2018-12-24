from pymongo import MongoClient

MONGO_HOST = 'mongodb://localhost/miscdb'
client = MongoClient(MONGO_HOST)
db = cliet.miscdb
misc = db.misc
cursor = misc.find()
democrats = []
republicans = []
for tweet in cursor:
    dict_tweet = dict(tweet)
    if "#democrats" in test_tweet.text:
        democrats.append(test_tweet.text)
    elif "#gop" in test_tweet.text:
        republicans.append(test_tweet.text)
    print("Democrats" + str(len(democrats)) + "\nRepublicans" + str(len(republicans)))
