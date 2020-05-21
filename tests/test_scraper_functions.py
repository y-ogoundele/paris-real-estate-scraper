import unittest
import requests
from bs4 import BeautifulSoup
from scraper_functions import list_property_urls


class TestListPropertyURLs(unittest.TestCase):
    def setUp(self) -> None:
        self.sr_url = "https://www.seloger.com/list.htm?ci=750105,750111,940067,940080&idq=133102,133103,133104,133105,133106,133107,133108,133109,133110,133111,133112,133113,133114,133115,133764&idtt=1&idtypebien=1&nb_pieces=1&photo=15&si_meuble=1&surfacemin=20&tri=d_dt_crea"
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            'referer': 'https://www.google.com/'}
        response = requests.get(self.sr_url, headers=self.header)
        self.searchresult_soup = BeautifulSoup(response.text, "html.parser")

    def test_returns_properties(self):
        property_urls = list_property_urls(self.searchresult_soup)
        for i in range(0, len(property_urls)):
            with self.subTest(i=i):
                self.assertEqual(property_urls[i][24:55], 'annonces/locations/appartement/')


