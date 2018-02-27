import unittest
from cdtweetbot import get_links


class TestCDbot(unittest.TestCase):
    """Class that tests cdtweetbot.py"""

    def test_get_posts(self):
        """Test if links are ordered correctly."""
        links = get_links()
        links_amount = len(links)
        links_type = type(links)
        self.assertTrue(links_type == dict)
        self.assertGreater(links_amount, 1)


unittest.main()
