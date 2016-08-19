from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas as pd
from .config import *
import logging
from .database import session, Tweet, User

# Set the log output file, and the log level
logging.basicConfig(filename="twitter_stream.log", level=logging.DEBUG)

class StdOutListener(StreamListener):

    def __init__(self, num_tweets_to_grab):
        self.counter = 0
        self.num_tweets_to_grab = num_tweets_to_grab

    def on_data(self, data):
        try:
            json_data = json.loads(data)
            tweet = Tweet()
            tweet.location = json_data["user"]["location"]
            tweet.user_lang = json_data["user"]["lang"]
            tweet.coordinates = json_data["tweets"][
                "coordinates"]["coordinates"]
            tweet.created_at = json_data["tweets"]["created_at"]
            tweet.favorite_count = json_data["tweets"]["favorite_count"]
            tweet.tweet_lang = json_data["tweets"]["lang"]
            tweet.retweet_count = json_data["tweets"]["retweet_count"]
            tweet.text = json_data["tweets"]["text"]
            tweet.hashtag = json_data["entities"]["hashtags"][1]
            session.add(tweet)
            session.commit()
            self.counter += 1
            if self.counter == self.num_tweets_to_grab:
                return False

            return True
        except:
            logging.error("Keyword '{}' requested, but didn't exist.".format(data))

    def on_error(self, status):
        print(status)


class Main():

    def __init__(self, num_tweets_to_grab):
        self.l = StdOutListener(num_tweets_to_grab=20)
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.counter = 0
        self.num_tweets_to_grab = num_tweets_to_grab

    def get_streaming_data(self):
        twitter_stream = Stream(self.auth, self.l)
        try:
            search_results = twitter_stream.filter(track="trump")
            for result in search_results:
                print(result)

        except Exception as e:
            print(e)

if __name__ == "__main__":
        num_tweets_to_grab = 20
        program = Main(num_tweets_to_grab)
        program.get_streaming_data()
