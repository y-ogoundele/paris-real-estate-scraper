from bs4 import BeautifulSoup, element
import re


def list_property_urls(searchresults_soup: BeautifulSoup):
    """From a search results page, list all URLs of shown properties"""
    property_urls = []
    main_tag = searchresults_soup.find_all('div', class_='Page__WrapMain-st6q56-1 bgOcDb')[0]
    results = main_tag.find_all('div', class_="classified__ContentWrapper-sc-1wmlctl-1 iFOIpl")
    for result in results:
        property_urls.append(result.find_all('a', class_='CoveringLink-a3s3kt-0 dXJclF')[0].get('href'))
    return property_urls


def scrape_property_page(property_soup: BeautifulSoup):
    main_tag, summary_block, quartier_block, price_block, description_block, diagnostics_block = extract_blocks(
        property_soup)
    title, url, nr_sqm, nr_rooms = scrape_meta_information(property_soup, summary_block)
    current_price, deposit, price_change_text = scrape_rent_information(price_block)
    city, neighborhood = scrape_geo_information(quartier_block)
    total_desc = scrape_description(description_block)
    general_list, inside_list, other_list = scrape_amenities(description_block)
    letter, cons = scrape_energy_diagnostics(diagnostics_block)
    return [title, url, nr_sqm, nr_rooms, current_price, deposit, price_change_text, city, neighborhood, total_desc,
            general_list, inside_list, other_list, letter, cons]


def extract_blocks(property_soup: BeautifulSoup):
    """Extrack all blocks found on web page"""
    main_tag = property_soup.find_all('div', class_=re.compile("^app__CWrapMain-aroj7e-3"))[0]
    summary_block = main_tag.find_all('div', class_=re.compile("^Summarystyled__MainWrapper-tzuaot-1"))[0]
    quartier_block = main_tag.find('p', class_=re.compile("^Map__AddressLine-sc-6i077b-2"))
    price_block = main_tag.find('section', attrs={'data-test': 'price-block', 'id': "a-propos-de-ce-prix"})
    description_block = \
        (main_tag.find_all('div', class_=re.compile('^TitledDescription__TitledDescriptionContent-sc-1r4hqf5-1')))
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


def scrape_rent_information(price_block: element.Tag):
    current_price = price_block.find_all('div',
                                         class_=re.compile('^Pricestyled__Price-uc7t2j-0'))[0].find('div').string
    try:
        deposit_block = price_block.find_all('div', class_=re.compile('^rentHelper__Garantie-sc-1x3dozo-0'))[0]
        deposit = deposit_block.strong.contents[0]
    except IndexError:
        deposit = 'N/A'
    try:
        price_fluctuations_block = \
            price_block.find_all('div', class_=re.compile('^PriceHistorystyled__Container-sc-18jhpbr-0'))[0]
        price_change_text = ''.join(price_fluctuations_block.find_all('div', class_=re.compile(
            '^PriceHistorystyled__FirstEvolutionFull-sc-18jhpbr-2'))[0].contents[:3])
        price_change_amount = (
            price_fluctuations_block
                .find_all('span',
                          class_=re.compile('^PriceHistorystyled__BoldDisplayAmount-sc-18jhpbr-4'))
        )[0].contents[0]
        price_change_text += price_change_amount
    except IndexError:
        price_change_text = 'N/A'
    return current_price, deposit, price_change_text


def scrape_geo_information(quartier_block: element.Tag):
    city = ''.join(quartier_block.strong.contents[2:])
    neighborhood = quartier_block.contents[-3]
    return city, neighborhood


def scrape_description(description_block: element.Tag):
    avis_du_pro = description_block[0]
    total_desc = ''
    for s in avis_du_pro.find_all('p'):
        total_desc += s.string
    return total_desc


def scrape_amenities(description_block: element.ResultSet):
    try:
        if len(description_block) == 5 and 'Diagnostics' in description_block[-1].find('div').get('class')[0]:
            general = description_block[-4].find_all('ul', class_=re.compile('^GeneralList__List-sc-9gtpjm-0'))[0].find_all(
                'li')
            inside = description_block[-3].find_all('ul', class_=re.compile('^GeneralList__List-sc-9gtpjm-0'))[0].find_all('li')
            other = description_block[-2].find_all('ul', class_=re.compile('^GeneralList__List-sc-9gtpjm-0'))[0].find_all('li')
            general_list = [s.string for s in general]
            inside_list = [s.string for s in inside]
            other_list = [s.string for s in other]
        elif len(description_block) == 4 and 'Diagnostics' in description_block[-1].find('div').get('class')[0]:
            general = description_block[-4].find_all('ul', class_=re.compile('^GeneralList__List-sc-9gtpjm-0'))[0].find_all(
                'li')
            inside = description_block[-3].find_all('ul', class_=re.compile('^GeneralList__List-sc-9gtpjm-0'))[0].find_all('li')
            other = description_block[-2].find_all('ul', class_=re.compile('^GeneralList__List-sc-9gtpjm-0'))[0].find_all('li')
            general_list = [s.string for s in general]
            inside_list = [s.string for s in inside]
            other_list = [s.string for s in other]
        else:
            general_list = []
            inside_list = []
            other_list = []
    except IndexError: # No other field
        general = description_block[-3].find_all('ul', class_=re.compile('^GeneralList__List-sc-9gtpjm-0'))[0].find_all(
            'li')
        inside = description_block[-2].find_all('ul', class_=re.compile('^GeneralList__List-sc-9gtpjm-0'))[0].find_all('li')
        general_list = [s.string for s in general]
        inside_list = [s.string for s in inside]
        other_list = []
    return general_list, inside_list, other_list


def scrape_energy_diagnostics(diagnostics_block: element.Tag):
    try:
        [energy_diagnostic, ges_diagnostics] = diagnostics_block.find_all('div',
                                                                          class_=re.compile(
                                                                              '^Diagnostics__DiagnosticsContainer-al64ti-2'))
        letter = energy_diagnostic.find_all('div', class_=lambda x: x and 'FocusedTile' in x)[0].p.string
        cons = energy_diagnostic.find('span', class_=re.compile('^Preview__PreviewTooltipValue-sc-1pa12ii-4')).string
        cons += energy_diagnostic.find('span', class_=re.compile('^Preview__PreviewTooltipCaption-sc-1pa12ii-5')).string
    except IndexError:
        letter = 'N/A'
        cons = 'N/A'
    except AttributeError:
        letter = 'N/A'
        cons = 'N/A'
    return letter, cons


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
