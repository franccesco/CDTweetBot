"""Command Line Argument Parser."""

import argparse
from time import sleep
from cdtweetbot import delete_all_tweets, create_table, get_posts, tweet_post
from cdtweetbot import populate_posts_db

# CLI arguments with argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--show-posts',
                    help='Show posts in database', action='store_true')
parser.add_argument('-p', '--purge-db',
                    help='Purge the database', action='store_true', default=False)
parser.add_argument('-t', '--tweet-posts',
                    action='store_true', help='Tweet posts.')
exclusive = parser.add_mutually_exclusive_group()
exclusive.add_argument('-d', '--delete-all',
                       help='Delete all tweets', action='store_true')
args = parser.parse_args()

if args.delete_all:
    answer = input('Are you sure you want to delete ALL your tweets? [Y/n]: ')
    answer = answer.lower()
    if answer == 'y' or answer == '':
        print('Deleting all tweets...')
        delete_all_tweets()

if args.purge_db:
    answer = input("You're about to purge the database, proceed? [Y/n]: ")
    answer = answer.lower()
    if answer == 'y' or answer == '':
        create_table(purge=True)
        print('Database purged.')

if args.show_posts:
    posts = get_posts()
    post_no = 0
    for title, link in posts.items():
        print('{}. {}: {}'.format(post_no, title, link))
        post_no += 1

while args.tweet_posts:
    populate_posts_db(tweet=True)
    print('Sleeping for 1hr.')
    try:
        sleep(60 * 60)
    except KeyboardInterrupt:
        q = input('[C]ontinue | [E]xit: ').lower()
        if q == 'c':
            next
        else:
            exit(0)
