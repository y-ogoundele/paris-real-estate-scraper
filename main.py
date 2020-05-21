import pandas as pd
import time
import random

from config import __args__
from utils import get_url_soup, create_random_user_agent
from scraper_functions import list_property_urls, scrape_property_page


def scrape_searchresult_url(searchresult_url: str):
    values = []
    # Requesting search results page
    headers = create_random_user_agent()
    searchresults_soup = get_url_soup(searchresult_url, headers)
    time.sleep(random.random() * 30)
    property_url_list = list_property_urls(searchresults_soup)

    # Loop over all properties
    for property_url in property_url_list:
        headers = create_random_user_agent()
        property_soup = get_url_soup(property_url, headers)
        time.sleep(random.random() * 30)
        row = scrape_property_page(property_soup)
        values.append(row)
    output = pd.DataFrame(columns=['title', 'url', 'nr_sqm', 'nr_rooms', 'current_price', 'deposit', 'price_change',
                                   'city', 'neighborhood', 'description', 'amenities_general', 'amenities_inside',
                                   'amenities_other', 'energy_letter', 'energy_consumption'], data=values)
    return (output)


if __name__ == "__main__":
    # run main function
    output_df = scrape_searchresult_url(
        'https://www.seloger.com/list.html?projects=1&types=1&places=[{cp:75}|{ci:940080}|{ci:940067}]&rooms=1&furnished=1&enterprise=0&qsVersion=1.0')
    # store results in table
    output_df.to_csv(__args__['path_to_output_file'])
