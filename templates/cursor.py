from pymongo import MongoClient

MONGO_HOST = 'mongodb://localhost/miscdb'
client = MongoClient(MONGO_HOST)
f = open('misc.txt', 'w+')
db = client.miscdb
misc = db.misc
cursor = misc.find()
democrats = []
republicans = []
i = 0
for tweet in cursor:
    i += 1
    dict_tweet = dict(tweet)
    text = dict_tweet['text'].replace('\n', '')
    print(text)
    f.write(text + '\n')
f.close()
