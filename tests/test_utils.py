import unittest
from requests.exceptions import MissingSchema
from utils import get_url_soup

class TestGetURLSoup(unittest.TestCase):
    def setUp(self):
        self.url = "https://www.wikipedia.org/"
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,'referer':'https://www.google.com/'}

    def test_invalid_string(self):
        with self.assertRaises(MissingSchema):
            get_url_soup(url='', headers=headers)
            