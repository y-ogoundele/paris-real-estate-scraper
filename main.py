import pandas as pd

from config import __args__
from scraper_functions import list_property_urls, scrape_property_page
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep


def scrape_searchresult_url(searchresult_page_root: str, browser):
    values = []
    for i in range(1, 101):
        print(i)
        searchresult_url = searchresult_page_root + str(i)
        # Requesting search results page
        browser.get(searchresult_url)
        sr_html_source = browser.page_source
        searchresults_soup = BeautifulSoup(sr_html_source, 'html.parser')
        try:
            print(searchresults_soup.find('div', {'class': 'sc-bxivhb kOwDzU'}).text[:66])
            print("\nbot detection!")
            sleep(120)
            sr_html_source = browser.page_source
            searchresults_soup = BeautifulSoup(sr_html_source, 'html.parser')
        except:
            print("No bot detection")
        property_url_list = list_property_urls(searchresults_soup)
        # Loop over all properties
        for property_url in property_url_list:
            browser.get(property_url)
            property_html_source = browser.page_source
            property_soup = BeautifulSoup(property_html_source, 'html.parser')
            try:
                row = scrape_property_page(property_soup)
                values.append(row)
            except IndexError:
                pass
            except AttributeError:
                pass
    output = pd.DataFrame(columns=['title', 'url', 'meta', 'current_price', 'deposit', 'price_change',
                                   'city', 'neighborhood', 'amenities_general', 'amenities_inside',
                                   'amenities_other', 'energy_letter', 'energy_consumption'], data=values)
    return output


if __name__ == "__main__":
    sr_page_root = 'https://www.seloger.com/list.htm?projects=2&types=1&natures=1%2C2&places=%5B%7Bcp%3A75%7D%7C%7Bcp%3A93%7D%7C%7Bcp%3A91%7D%7C%7Bcp%3A94%7D%7C%7Bcp%3A92%7D%5D&rooms=1%2C2%2C3&enterprise=0&qsVersion=1.0&LISTING-LISTpg='
    # create webdriver
    opts = Options()
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36")
    browser = webdriver.Chrome('../../../chromedriver', chrome_options=opts)
    browser.set_page_load_timeout(30)
    browser.get('https://www.seloger.com')
    seloger = 'https://www.seloger.com/annonces/locations/appartement/paris-20eme-75/pere-lachaise-reunion/164290613.htm'
    browser.get(seloger)
    sleep(5)
    # run main function
    output_df = scrape_searchresult_url(
        sr_page_root
        , browser)
    # store results in table
    output_df.to_csv(__args__['path_to_output_file'])
