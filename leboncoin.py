"""
leboncoin.py
----------

Description:
------------
This module contains functions for retrieving real estate listings
from a given URL on the site leboncoin.fr. It uses Playwright to
automate navigation and bypass anti-bot protections.

Functions:
----------
- html_to_json: Converts HTML content to JSON.
- extract_ads: Extracts ad listings from JSON data.
- extract_properties: Transforms raw ad data into structured format.
- main: Demonstrates retrieving and processing real estate listings.

"""

import logging
import json
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from scraper import retrieve_html
from storage import process_ad

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def html_to_json(html_content: str) -> Optional[Dict[str, Any]]:
    """
    Convert HTML content to JSON by extracting the data from a specific script tag.

    Args:
        html_content (str): The HTML content of the page.

    Returns:
        Optional[Dict[str, Any]]: The JSON data extracted from the HTML content, or None if an error occurs.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tag = soup.select_one('script#__NEXT_DATA__')

    if script_tag:
        json_content = script_tag.string
        try:
            json_data = json.loads(json_content)
            logging.info('JSON content extracted successfully')
            return json_data
        except json.JSONDecodeError as e:
            logging.error('Error decoding JSON: %s', e)
            return None
    else:
        logging.error('No script tag with id "__NEXT_DATA__" found.')
        return None

def extract_ads(json_data: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    """
    Extract the list of ads from the JSON data.

    Args:
        json_data (Dict[str, Any]): The JSON data containing ad listings.

    Returns:
        Optional[List[Dict[str, Any]]]: A list of ads, or None if an error occurs.
    """
    try:
        ads_list = json_data['props']['pageProps']['searchData']['ads']
        logging.info('Ads list extracted successfully')
        return ads_list
    except KeyError as e:
        logging.error('Error extracting ads: %s', e)
        return None

def extract_properties(ads_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extract and transform properties from the ads list.

    Args:
        ads_list (List[Dict[str, Any]]): The list of ads.

    Returns:
        List[Dict[str, Any]]: The list of transformed ads.
    """
    def to_int(value: Any) -> Optional[int]:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def to_float(value: Any) -> Optional[float]:
        try:
            return float(str(value).replace(' ', '').replace(',', '.'))
        except (TypeError, ValueError):
            return None

    def to_bool(value: Any) -> bool:
        if isinstance(value, str):
            return value.lower() == 'true'
        return bool(value)

    def map_real_estate_type(value: str) -> str:
        mapping = {
            'Appartement': 'Apartment',
            'Maison': 'House',
            'Autre': 'Other',
            'Parking': 'Parking',
            'Terrain': 'Land'
        }
        return mapping.get(value, 'Other')  # Default to 'Other' if not found

    def map_owner_type(value: str) -> str:
        mapping = {
            'pro': 'professional',
            'particulier': 'private'
        }
        return mapping.get(value, 'private')  # Default to 'private' if not found

    def validate_energy_rate(value: Optional[str]) -> Optional[str]:
        return value.upper() if value and value.upper() in 'ABCDEFG' else None

    transformed_data = []
    for ad in ads_list:
        attributes = {attr['key']: attr['value_label'] for attr in ad.get('attributes', [])}

        # Handle price extraction, assuming it might be a list or a string
        price = ad.get('price')
        if isinstance(price, list):
            price = price[0] if price else None
        price = to_int(price)

        old_price = attributes.get('old_price')
        old_price = to_int(old_price)

        transformed_ad = {
            'id': ad.get('list_id'),
            'publication_date': ad.get('first_publication_date'),
            'status': ad.get('status'),
            'title': ad.get('subject'),
            'description': ad.get('body'),
            'url': ad.get('url'),
            'price': price,
            'latitude': ad.get('location', {}).get('lat'),
            'longitude': ad.get('location', {}).get('lng'),
            'location_city': ad.get('location', {}).get('city'),
            'location_zipcode': to_int(ad.get('location', {}).get('zipcode')),
            'type': map_owner_type(ad.get('owner', {}).get('type')),
            'real_estate_type': map_real_estate_type(attributes.get('real_estate_type', 'Other')),
            'square': to_int(attributes.get('square')),
            'rooms': to_int(attributes.get('rooms')),
            'energy_rate': validate_energy_rate(attributes.get('energy_rate')) if 'energy_rate' in attributes else None,
            'ges': validate_energy_rate(attributes.get('ges')) if 'ges' in attributes else None,
            'bathrooms': to_int(attributes.get('bathrooms')),
            'land_surface': to_int(attributes.get('land_plot_surface')),
            'parking': to_bool(attributes.get('parking')),
            'cellar': to_bool(attributes.get('cellar')),
            'swimming_pool': to_bool(attributes.get('swimming_pool')),
            'equipments': attributes.get('equipments', ''),
            'elevator': to_bool(attributes.get('elevator')),
            'fai_included': to_bool(attributes.get('fai_included')),
            'floor_number': to_int(attributes.get('floor_number')),
            'nb_floors_building': to_int(attributes.get('nb_floors_building')),
            'outside_access': attributes.get('outside_access', ''),
            'building_year': to_int(attributes.get('building_year')),
            'annual_charges': to_int(attributes.get('annual_charges')),
            'bedrooms': to_int(attributes.get('bedrooms')),
            'immo_sell_type': attributes.get('immo_sell_type'),
            'old_price': old_price,
            'images': ad.get('images', {}).get('urls_large', [])
        }
        transformed_data.append(transformed_ad)
    return transformed_data

def main(target_url: str):
    """
    Main function to demonstrate retrieving and processing real estate listings from Leboncoin.

    Args:
        target_url (str): The URL of the target website to scrape.
    """
    # Retrieve HTML content from the target URL and save it to 'output.html'
    html_content = retrieve_html(target_url)
    if html_content:
        with open('output.html', 'w', encoding='utf-8') as file:
            file.write(html_content)

    # Read the HTML content from 'output.html'
    with open('output.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Extract JSON content from the HTML and save it to 'list.json'
    json_data = html_to_json(html_content)
    if json_data:
        with open("list.json", 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)

    # Read the JSON content from 'list.json'
    with open('list.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # Extract ads list from the JSON data and save it to 'list_ads.json'
    ads_list = extract_ads(json_data)
    if ads_list:
        with open("list_ads.json", 'w', encoding='utf-8') as file:
            json.dump(ads_list, file, ensure_ascii=False, indent=4)

    with open('list_ads.json', 'r', encoding='utf-8') as file:
        ads_list = json.load(file)

    # Extract properties to transform raw data into structured data
    sql_ready_data = extract_properties(ads_list)

    # Process each ad, including validation and storage
    for ad in sql_ready_data:
        process_ad(ad)

    logging.info("All ads processed.")

if __name__ == "__main__":
    # Replace with the target URL you want to scrape
    target_url = 'https://www.leboncoin.fr/v/Morsang-sur-Orge_91390/ventes_immobilieres'
    main(target_url)
