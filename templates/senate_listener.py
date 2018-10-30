from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from pymongo import MongoClient
from races import choose_collection, create_keywords
import json
import sys



MONGO_HOST= 'mongodb://localhost/miscdb'
#PATH_TO_CONFIG_FILE = '/root/rao_vinnakota_sproj_19/templates/races.ini'
ckey = "pF5W6BaHFteEYdkq38cgZ755g"
csecret = "AwnBHQTmvVr6cMSYKm89vQOXMO3sPyoGvhXMaow3zlg2G74vLq"
atoken = "2646419088-gtzEn525GUUtTlwpegdZGd8dGLWl8m2IGq9jk9y"
asecret = "iQbg8ZfJ8KkI06n0lwkCVVprtkzsIp6h1RMXP5LN3Z6o2"

class StreamListener(StreamListener):
    #This is a class provided by tweepy to access the Twitter Streaming API.

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        #This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            #client = MongoClient(MONGO_HOST)

            # Use twitterdb database. If it doesn't exist, it will be created.
            #db = client.senatedb


            # Decode the JSON from Twitter
            datajson = json.loads(data)
            for keyword in keywords:
                if keyword in datajson['text']:
                    return keyword
                    break
            collection = choose_collection(datajson, out_dict, keywords)
            #grab the 'created_at' data from the Tweet to use for display
            created_at = datajson['created_at']

            #print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at) + " " + datajson['text'])

            #insert the data into the mongoDB into a collection called twitter_search
            #if twitter_search doesn't exist, it will be created.
            #db.collection.insert(datajson)
        except Exception as e:
           print(e)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
#keywords = ["Antonio Delgado", "John Faso", "NY19", "@DelgadoforNY19", "@RepJohnFaso"]
#keywords = ["#midterms", "#vote", "#bluewave", "#redwave", "#democrats", "#elections", "#gop", "#usa"]
out_dict, keywords = create_keywords('SENATE')
print(keywords)
twitterStream = Stream(auth, StreamListener())
twitterStream.filter(track=keywords)
'''

'''
