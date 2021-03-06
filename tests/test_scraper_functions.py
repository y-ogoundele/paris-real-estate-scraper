import unittest
import requests
import re
from bs4 import BeautifulSoup
from scraper_functions import list_property_urls, extract_blocks, scrape_meta_information, scrape_rent_information, \
    scrape_geo_information, scrape_amenities, scrape_energy_diagnostics, scrape_property_page


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
        self.property_url = "https://www.seloger.com/annonces/locations/appartement/paris-20eme-75/pere-lachaise-reunion/164290613.htm"
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            'referer': 'https://www.google.com/'}
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
        self.property_url = "https://www.seloger.com/annonces/locations/appartement/paris-20eme-75/pere-lachaise-reunion/164290613.htm"
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            'referer': 'https://www.google.com/'}
        response = requests.get(self.property_url, headers=self.header)
        self.property_soup = BeautifulSoup(response.text, "html.parser")
        main_tag = self.property_soup.find_all('div', class_=re.compile("^app__CWrapMain-aroj7e-3"))[0]
        self.summary_block = main_tag.find_all('div', class_=re.compile("^Summarystyled__TagsWrapper-tzuaot-19"))[0]

    def test_returns_meta_info(self):
        # TODO: Find a way to get a valid property (studio only)
        meta_info = scrape_meta_information(self.property_soup, self.summary_block)
        expected_result = (
            'Location Appartement 2 pièces Paris 20ème - Appartement F2/T2/2 pièces 34m² 1290€/mois - SeLoger',
            'https://www.seloger.com/annonces/locations/appartement/paris-20eme-75/pere-lachaise-reunion/164290613.htm',
            ['2 pièces', '1 chambre', '34m²']
        )
        self.assertEqual(meta_info, expected_result)


class TestScrapeRentInformation(unittest.TestCase):
    def setUp(self) -> None:
        self.property_url = "https://www.seloger.com/annonces/locations/appartement/paris-20eme-75/pere-lachaise-reunion/164290613.htm"
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            'referer': 'https://www.google.com/'}
        response = requests.get(self.property_url, headers=self.header)
        self.property_soup = BeautifulSoup(response.text, "html.parser")
        main_tag = self.property_soup.find_all('div', class_=re.compile("^app__CWrapMain-aroj7e-3"))[0]
        self.price_block = main_tag.find('section', attrs={'data-test': 'price-block'})

    def test_returns_rent_info(self):
        rent_info = scrape_rent_information(self.price_block)
        self.assertEqual(len(rent_info), 3)


class TestScrapeGeoInformation(unittest.TestCase):
    def setUp(self) -> None:
        self.property_url = "https://www.seloger.com/annonces/locations/appartement/paris-20eme-75/pere-lachaise-reunion/164290613.htm"
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            'referer': 'https://www.google.com/'}
        response = requests.get(self.property_url, headers=self.header)
        self.property_soup = BeautifulSoup(response.text, "html.parser")
        main_tag = self.property_soup.find_all('div', class_=re.compile("^app__CWrapMain-aroj7e-3"))[0]
        self.quartier_block = main_tag.find('p', class_=re.compile("^Map__AddressLine-sc-6i077b-2"))

    def test_returns_geo_info(self):
        geo_info = scrape_geo_information(self.quartier_block)
        self.assertEqual(len(geo_info), 2)


class TestScrapeAmenities(unittest.TestCase):
    def setUp(self) -> None:
        self.property_url = "https://www.seloger.com/annonces/locations/appartement/paris-20eme-75/pere-lachaise-reunion/164290613.htm"
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            'referer': 'https://www.google.com/'}
        response = requests.get(self.property_url, headers=self.header)
        self.property_soup = BeautifulSoup(response.text, "html.parser")
        main_tag = self.property_soup.find_all('div', class_=re.compile("^app__CWrapMain-aroj7e-3"))[0]
        self.description_block = (
            main_tag.find_all('div', class_=re.compile('^TitledDescription__TitledDescriptionContent-sc-1r4hqf5-1')))

    def test_returns_amenities_info(self):
        amenities = scrape_amenities(self.description_block)
        self.assertEqual(len(amenities), 3)

class TestScrapeEnergyDiagnostics(unittest.TestCase):
    def setUp(self) -> None:
        self.property_url = "https://www.seloger.com/annonces/locations/appartement/paris-20eme-75/pere-lachaise-reunion/164290613.htm"
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            'referer': 'https://www.google.com/'}
        response = requests.get(self.property_url, headers=self.header)
        self.property_soup = BeautifulSoup(response.text, "html.parser")
        main_tag = self.property_soup.find_all('div', class_=re.compile("^app__CWrapMain-aroj7e-3"))[0]
        self.diagnostics_block = main_tag.find_all('div', id='diagnostics')[0]

    def test_returns_diagnostics_info(self):
        energy_diagnostics = scrape_energy_diagnostics(self.diagnostics_block)
        self.assertEqual(len(energy_diagnostics), 2)

class TestScrapeProperty(unittest.TestCase):
    def setUp(self) -> None:
        self.property_url = "https://www.seloger.com/annonces/locations/appartement/paris-20eme-75/pere-lachaise-reunion/164290613.htm"
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            'referer': 'https://www.google.com/'}
        response = requests.get(self.property_url, headers=self.header)
        self.property_soup = BeautifulSoup(response.text, "html.parser")

    def test_returns_data(self):
        scrape_property_page(self.property_soup)