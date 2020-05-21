import unittest
from requests.exceptions import MissingSchema, ConnectionError
from utils import get_url_soup


class TestGetURLSoup(unittest.TestCase):
    def setUp(self):
        self.url = "https://www.wikipedia.org/"
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            'referer': 'https://www.google.com/'}
        self.invalid_url = 'https://www.wikipediap.org/'

    def test_empty_string(self):
        with self.assertRaises(MissingSchema):
            get_url_soup(url='', headers=self.headers)

    def test_invalid_string(self):
        with self.assertRaises(ConnectionError):
            get_url_soup(url=self.invalid_url, headers=self.headers)

    def test_correct_url(self):
        response_title_string = get_url_soup(url=self.url, headers=self.headers).title.string
        self.assertEqual(response_title_string, 'Wikipedia')


class TestAllPossibleUserAgents(unittest.TestCase):
    def setUp(self):
        self.desktop_agents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

        self.url = "https://www.wikipedia.org/"

    def test_all_agents(self):
        for i in range(0, len(self.desktop_agents)):
            with self.subTest(i=i):
                headers = {'user-agent': self.desktop_agents[i], 'referer': 'https://www.google.com/'}
                response_title_string = get_url_soup(url=self.url, headers=headers).title.string
                self.assertEqual(response_title_string, 'Wikipedia')
