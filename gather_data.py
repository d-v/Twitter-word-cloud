import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import json

class ChiListener(StreamListener):
    def __init__(self, data_dir):
        self.outfile = "%s/stream.json" % (data_dir)
    
    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
                f.write(data)
                print(data)
                return True
        except BaseException as e:
            print("Error: %s" % str(e))
            time.sleep(5)
        return True

consumer_key =  'wgorbbXUouRhjQelJgXUf7N36'
consumer_secret =  '8jnO5OSzzS4ek2ZOc82GNQYixrANacoyg3uBoIM1fA0nEJpL7P'
access_token = '746156478940209153-5toY0P7jWlVoM6dja6SjT6l5BLr331U'
access_secret = 'msHILdWjmSec6kcS1MMZyIPqmA536pteaZj530DJK1731'
query = ['security', 'privacy']
dir = "./data"
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
    
twitter_stream = Stream(auth, ChiListener(dir))
twitter_stream.filter(track=query)
