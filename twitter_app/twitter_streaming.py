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

def get_tweets(number):
    program = Main(number)
    program.get_streaming_data()

class StdOutListener(StreamListener):

    def __init__(self, num_tweets_to_grab):
        self.counter = 0
        self.num_tweets_to_grab = num_tweets_to_grab

    def on_data(self, data):
        try:
            json_data = json.loads(data)
            logging.info("===")
            logging.info(json_data)
            logging.info("===")
            tweet = Tweet()
            if json_data["user"]:
                if json_data["user"]["location"]:
                    tweet.location = json_data["user"]["location"].encode("ascii","ignore").decode("utf-8", "ignore")
                    logging.error(tweet.location)
            if json_data["user"]:
                if json_data["user"]["lang"]:
                    tweet.user_lang = json_data["user"]["lang"]
                    logging.error(tweet.user_lang)
            if json_data["coordinates"]:
                tweet.coordinates = json_data["coordinates"]
                logging.error(tweet.coordinates)
            if json_data["created_at"]:
                tweet.created_at = json_data["created_at"]
                logging.error(tweet.created_at)
            if json_data["favorite_count"]:
                tweet.favorite_count = json_data["favorite_count"]
                logging.error(tweet.favorite_count)
            if json_data["lang"]:
                tweet.tweet_lang = json_data["lang"]
                logging.error(tweet.tweet_lang)
            if json_data["retweet_count"]:
                tweet.retweet_count = json_data["retweet_count"]
                logging.error(tweet.retweet_count)
            if json_data["text"]:
                tweet.text = json_data["text"].encode("ascii","ignore").decode("utf-8", "ignore")
                logging.error("=== text: %s"%tweet.text)
            #if  json_data["entities"]:
               #if json_data["entities"]["hashtags"]:
                   #tweet.hashtag = json_data["entities"]["hashtags"][1].encode("utf-8")
            session.add(tweet)
            session.commit()
            self.counter += 1
            logging.info(self.counter)
            logging.info(self.num_tweets_to_grab)
            logging.error("===All Done")
            if self.counter == self.num_tweets_to_grab:
                return False

            return True
        except Exception as e:
            #logging.error("Keyword requested, but didn't exist. Here is the returned data .{}".format(data))
            logging.error(e)

    def on_error(self, status):
        print(status)


class Main():

    def __init__(self, num_tweets_to_grab):
        self.l = StdOutListener(num_tweets_to_grab)
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

    def get_streaming_data(self):
        twitter_stream = Stream(self.auth, self.l)
        try:
            search_results = twitter_stream.filter(track=["trump"])
            # need to pass this as an argument from the command line
            for result in search_results:
                print(result)

        except Exception as e:
            print(e)
