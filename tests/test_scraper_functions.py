import unittest
import requests
import re
from bs4 import BeautifulSoup
from scraper_functions import list_property_urls, extract_blocks, scrape_meta_information


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


class TestExtractBlocks(unittest.TestCase):
    def setUp(self) -> None:
        self.dummy_url = "https://www.wikipedia.org"
        self.property_url =  "https://www.seloger.com/annonces/locations/appartement/paris-5eme-75/saint-victor/158755387.htm?projects=1&types=1&places=[{ci:750105}]&rooms=1&enterprise=0&qsVersion=1.0&bd=ListToDetail"
        self.header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,'referer':'https://www.google.com/'}
        response = requests.get(self.property_url, headers=self.header)
        dummy_response = requests.get(self.dummy_url, headers=self.header)
        self.property_soup = BeautifulSoup(response.text, "html.parser")
        self.dummy_soup = BeautifulSoup(dummy_response.text, "html.parser")

    def test_empty_soup(self):
        with self.assertRaises(IndexError):
            extract_blocks(self.dummy_soup)

    def test_correct_soup(self):
        self.assertEqual(len(extract_blocks(self.property_soup)), 6)

class TestScrapeMetaInformation(unittest.TestCase):
    def setUp(self) -> None:
        self.property_url =  "https://www.seloger.com/annonces/locations/appartement/paris-5eme-75/saint-victor/158755387.htm?projects=1&types=1&places=[{ci:750105}]&rooms=1&enterprise=0&qsVersion=1.0&bd=ListToDetail"
        self.header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,'referer':'https://www.google.com/'}
        response = requests.get(self.property_url, headers=self.header)
        self.property_soup = BeautifulSoup(response.text, "html.parser")
        main_tag = self.property_soup.find_all('div', class_=re.compile("^app__CWrapMain-aroj7e-3"))[0]
        self.summary_block = main_tag.find_all('div', class_=re.compile("^Summarystyled__MainWrapper-tzuaot-1"))[0]

    def test_returns_meta_info(self):
        # TODO: Find a way to get a valid property (studio only)
        meta_info = scrape_meta_information(self.property_soup, self.summary_block)
        expected_result = (
            'Location Studio Paris 5ème - Appartement F1/T1/1 pièce 19,92m² 835€/mois - SeLoger',
            'https://www.seloger.com/annonces/locations/appartement/paris-5eme-75/saint-victor/158755387.htm',
            '19,92m²',
            '1 pièce',
                           )
        self.assertEqual(meta_info, expected_result)
