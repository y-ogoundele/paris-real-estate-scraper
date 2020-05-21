from bs4 import BeautifulSoup, element
import re


# get meta information: title, URL, nb de pieces, nb de m2 OK
# get pricing information: rent price, taxes and fees, caution
# get price evolution if possible
# get geo data: neighborhood, city,
# get text description: l'avis du pro, description
# get energy diagnostic

def list_property_urls(searchresults_soup: BeautifulSoup):
    """From a search results page, list all URLs of shown properties"""
    property_urls = []
    main_tag = searchresults_soup.find_all('div', class_='Page__WrapMain-st6q56-1 bgOcDb')[0]
    results = main_tag.find_all('div', class_="classified__ContentWrapper-sc-1wmlctl-1 iFOIpl")
    for result in results:
        property_urls.append(result.find_all('a', class_='CoveringLink-a3s3kt-0 dXJclF')[0].get('href'))
    return property_urls


def extract_blocks(property_soup: BeautifulSoup):
    """Extrack all blocks found on web page"""
    main_tag = property_soup.find_all('div', class_=re.compile("^app__CWrapMain-aroj7e-3"))[0]
    summary_block = main_tag.find_all('div', class_=re.compile("^Summarystyled__MainWrapper-tzuaot-1"))[0]
    quartier_block = main_tag.find('p', class_=re.compile("^Map__AddressLine-sc-6i077b-2"))
    price_block = main_tag.find('section', attrs={'data-test': 'price-block', 'id': "a-propos-de-ce-prix"})
    description_block = \
    (main_tag.find_all('div', class_=re.compile('^TitledDescription__TitledDescriptionContent-sc-1r4hqf5-1')))[0]
    diagnostics_block = main_tag.find_all('div', id='diagnostics')[0]
    return main_tag, summary_block, quartier_block, price_block, description_block, diagnostics_block


def scrape_meta_information(property_soup: BeautifulSoup, summary_block: element.Tag):
    """Extract title, URL, number of sqm and number of rooms from a given property page"""

    title = property_soup.title.string
    url = property_soup.find('meta', attrs={'property': 'og:url'}).get('content')
    dimensions_block = (
        summary_block
            .find_all('div', class_=re.compile("^Summarystyled__TagsWrapper-tzuaot-18"))[0]
            .find_all('div', class_=re.compile("^TagsWithIcon__TagContainer-j1x9om-1"))
    )
    rooms = dimensions_block[0]
    nr_rooms = rooms.find_all('div')[-1].string
    size = dimensions_block[1]
    nr_sqm = size.find_all('div')[-1].string
    return title, url, nr_sqm, nr_rooms


if __name__ == "__main__":
    import requests

    sr_url = "https://www.seloger.com/list.htm?ci=750105,750111,940067,940080&idq=133102,133103,133104,133105,133106,133107,133108,133109,133110,133111,133112,133113,133114,133115,133764&idtt=1&idtypebien=1&nb_pieces=1&photo=15&si_meuble=1&surfacemin=20&tri=d_dt_crea"
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        'referer': 'https://www.google.com/'}
    response = requests.get(sr_url, headers=header)
    soup = BeautifulSoup(response.text, "html.parser")
    print(list_property_urls(soup)[0])
    print('\n')
    print(len(list_property_urls(soup)))
