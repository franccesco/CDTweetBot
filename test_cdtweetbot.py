import unittest
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


unittest.main()
