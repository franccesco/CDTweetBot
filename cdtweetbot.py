import time
import tweepy
import requests
from os import getenv
from time import sleep
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv

# load environment keys
load_dotenv(find_dotenv())
consumer_key = getenv('consumer_key')
consumer_secret = getenv('consumer_secret')
access_token = getenv('access_token')
access_secret = getenv('access_secret')

# handling authentication and setting API
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


def get_links():
    """Get post links from codingdose."""

    # collect and parse page with bs4
    base_url = 'https://codingdose.info'
    page = requests.get(base_url)
    page_contents = BeautifulSoup(page.text, 'html.parser')

    # find class post-list and then filter only href lines
    post_list = page_contents.find(class_='post-list')
    posts_items = post_list.find_all('a')

    ordered_posts = {}

    for post in posts_items:
        # appending post title and link to ordered_posts
        post_title = post.contents[0]
        post_link = base_url + post.get('href')
        ordered_posts[post_title] = post_link

    return ordered_posts
