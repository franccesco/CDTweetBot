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

    def test_purge_posts_database(self):
        """Test if purge switch in database works correctly."""
        conn_successful = tb.create_table(purge='y')
        self.assertTrue(conn_successful)

    def test_duplication_posts_db(self):
        """Test if duplicate entries are handled correctly."""
        self.assertTrue(tb.create_table(purge='y'))
        self.assertTrue(tb.populate_posts_db())

    def test_populate_posts_db(self):
        """Test populate posts."""
        self.assertTrue(tb.populate_posts_db())


unittest.main()
