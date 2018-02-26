import tweepy
from os import getenv
from time import sleep
from dotenv import load_dotenv, find_dotenv

# load environment keys
load_dotenv(find_dotenv())
consumer_key = getenv('consumer_key')
consumer_secret = getenv('consumer_secret')
access_token = getenv('access_token')
access_secret = getenv('access_secret')

# handling authentication setting API
twitter_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
twitter_auth.set_access_token(access_token, access_secret)
api = tweepy.API(twitter_auth)


# rate-limit handler
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            sleep(15 * 60)
