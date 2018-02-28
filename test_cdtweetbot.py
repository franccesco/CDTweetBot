import unittest
from os import path
import cdtweetbot as tb


class TestCDbot(unittest.TestCase):
    """Class that tests cdtweetbot.py"""

    def test_get_posts(self):
        """Test if links are ordered correctly."""
        links = tb.get_links()
        links_amount = len(links)
        links_type = type(links)
        self.assertTrue(links_type == dict)
        self.assertGreater(links_amount, 1)

    def test_twitter_auth(self):
        """Test if accessed correctly and an API was returned."""
        self.assertTrue(tb.auth())

    def test_create_db(self):
        """Test database 'posts.db' creation."""

        # create/connection
        conn_successful = tb.connect_database()

        # check if file is found
        file_exists = path.isfile('posts.db')
        file_not_found = 'File posts.db does not exists.'
        self.assertTrue(file_exists, msg=file_not_found)

        # check if connection is successful
        self.assertTrue(conn_successful)

    def test_populate_posts_db(self):
        self.assertTrue(tb.populate_posts_db())


unittest.main()
