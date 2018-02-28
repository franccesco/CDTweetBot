import tweepy
import sqlite3
import requests
from os import getenv
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv
# from time import sleep

# load environment keys
load_dotenv(find_dotenv())
consumer_key = getenv('consumer_key')
consumer_secret = getenv('consumer_secret')
access_token = getenv('access_token')
access_secret = getenv('access_secret')


def auth():
    """handling authentication and setting API."""
    twitter_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    twitter_auth.set_access_token(access_token, access_secret)
    api = tweepy.API(twitter_auth)
    return api

# rate-limit handler
# def limit_handled(cursor):
#     while True:
#         try:
#             yield cursor.next()
#         except tweepy.RateLimitError:
#             sleep(15 * 60)


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


def connect_database():
    """Connects/create database if it doesn't exists."""
    posts_db = 'posts.db'
    conn = sqlite3.connect(posts_db)
    return conn


def populate_posts_db():
    """Populates posts.db with posts and links."""
    links = get_links()

    # connecting to posts.db
    conn = connect_database()
    posts_db = conn.cursor()

    # creating table posts with post title and link
    posts_db.execute('CREATE TABLE posts (title TEXT, link TEXT)')

    # populating with posts
    for title, link in links.items():
        posts_db.execute("INSERT INTO posts (title, link) \
                         VALUES ('{}', '{}')".format(title, link))
    conn.commit()
    conn.close()
    return True
