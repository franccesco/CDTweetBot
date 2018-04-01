#!/usr/bin/env python3
#
# Author: Franccesco Orozco
# Version: to_be_filled
#
# CodingDose Tweet Bot is a twitter bot that utilizes Tweepy, requests,
# sqlite3 and BeautifulSoup to automatically extract links from my blog
# codingdose.info and shares them to twitter. It does this by extracting
# all posts links from codingdose.info, stripping the html tags and saving
# the post title + the post link to a database in SQLite3, after it has stored
# all the posts in the database, proceed to share each one of them to twitter
# with relevant hashtags such as 'programming', 'development' and 'coding'.

import tweepy
import sqlite3
import requests
from time import sleep
from bs4 import BeautifulSoup
from os import getenv, path, remove
from dotenv import load_dotenv, find_dotenv

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


def limit_handler(cursor):  # pragma: no cover
    """rate-limit handler will sleep for 15 minutes when limit is reached."""
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            sleep(15 * 60)


def delete_all_tweets(verbose=False):  # pragma: no cover
    """Deletes all tweets made by user."""
    api = auth()
    for status in limit_handler(tweepy.Cursor(api.user_timeline).items()):
        api.destroy_status(status.id)
        if verbose:
            print('Destroid tweet id: {}'.format(status.id))
    return True

# TODO: tweet posts from database.
# def tweet_posts(verbose=False):
#     """Share posts not found in database to twitter."""
#     pass


def get_num_pages():
    """Get number of pages in index."""
    base_url = 'https://codingdose.info/archives/'
    page = requests.get(base_url)
    page_contents = BeautifulSoup(page.text, 'html.parser')

    # get number of pages from class 'page-number'
    class_pages = page_contents.find(class_='page-number')
    total_pages = class_pages.get_text()

    # return the last page number from 'Page 1 of <x>'
    return int(total_pages[-1])


def get_archive_posts():
    """Get post links from codingdose archive."""
    total_pages = get_num_pages()

    # dictionary holding all titles and links
    ordered_posts = {}

    # scraping all pages, page 1 is index, there's no '/page/1/'
    for page in range(1, total_pages + 1):
        if page == 1:
            base_url = 'https://codingdose.info/archives/'
        elif page > 1:
            base_url = 'https://codingdose.info/archives/page/{}/'.format(page)
            # collect and parse page with bs4
            page = requests.get(base_url)
            page_contents = BeautifulSoup(page.text, 'html.parser')

            # find class post-list and then filter only href lines
            post_list = page_contents.find(class_='post-list')
            posts_items = post_list.find_all('a')

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


def create_table(purge=False, verbose=False):
    """Create 'posts' table in database."""
    conn = connect_database()
    posts_db = conn.cursor()

    # if purge switch is activated, then remove posts.db
    if path.isfile('posts.db') and purge is True:
        remove('posts.db')

    # try to create a table, if already exists then leave it be.
    try:
        posts_db.execute('''
                CREATE TABLE `posts` (
                `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                `title` integer NOT NULL UNIQUE,
                `link`  integer NOT NULL UNIQUE,
                UNIQUE(`title`,`link`));
            ''')
    except Exception as e:
        if verbose is True:
            print('Table post already exists.')

    return True


def populate_posts_db(verbose=False):
    """Populates posts.db with posts and links from /archive/."""
    database_connection = connect_database()
    database_cursor = database_connection.cursor()
    archive_links = get_archive_posts()
    for title, link in archive_links.items():
        try:
            database_cursor.execute('''
                INSERT INTO posts (title, link) VALUES ('{}', '{}')
                '''.format(title, link))
        except Exception as e:
            if verbose is True:
                print('Omitted: {} - {} '.format(title, link))
                print(e)
            pass
    database_connection.commit()
    database_connection.close()
    return True


def get_posts(verbose=False):
    """Returns a dictionary with database values"""

    # If database doesn't exist, create it
    if not path.isfile('posts.db'):
        create_table()
        populate_posts_db()

    # connect to database
    conn = connect_database()
    posts_db = conn.cursor()

    # query DB for posts and appends
    #  the elements to a dictionary:
    #   post[0] = title
    #   post[1] = link
    posts = {}
    for post in posts_db.execute('SELECT title, link FROM posts'):
        posts[post[0]] = post[1]
    return posts
