"""
leboncoin.py

Description:
------------
This module is designed to scrape and process real estate listings from Leboncoin. 
It retrieves HTML content, extracts JSON data from the page, transforms ad listings 
into structured data, and processes each ad for validation and storage in the database.

Features:
---------
- Retrieves HTML content from a specified Leboncoin URL.
- Extracts JSON data from specific script tags in the HTML.
- Parses and transforms JSON data into structured real estate listings.
- Validates and processes listings for storage in a database.
- Supports conversion of various property attributes to standard data types.

Main Functions:
---------------
1. html_to_json(html_content: str) -> Optional[Dict[str, Any]]:
   - Converts HTML content to JSON by extracting data from a specific script tag.

2. extract_ads(json_data: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
   - Extracts the list of ads from the JSON data.

3. extract_properties(ads_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
   - Extracts and transforms properties from the ads list into structured data.

4. main(target_url: str):
   - Main function demonstrating the process of retrieving and processing real estate listings from Leboncoin.
"""

import logging
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from html_retriever import retrieve_html
from storage import process_ad, get_leboncoin_urls_by_conditions

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
    
    # Check if there is results 
    if soup.find('div', {'data-test-id': 'noResult'}):
        return 'noResult'
    
    # Extract JSON data from the script tag
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
    transformed_ads = []

    for ad in ads_list:
        transformed_ad = {
            'id': ad.get('list_id'),
            'title': ad.get('subject', ''),
            'description': ad.get('body', ''),
            'url': ad.get('url'),
            'publication_date': datetime.fromisoformat(ad['first_publication_date']),
            'price': ad['price'][0],
            'old_price': None,  # Default to None unless found
            'immo_sell_type': None,  # Will be populated if found in attributes
            'status': ad.get('status'),
            'type': ad['owner']['type'],
            'real_estate_type': None,  # Will be populated if found in attributes
            'square': None,  # Will be populated if found in attributes
            'rooms': None,  # Will be populated if found in attributes
            'bedrooms': None,  # Will be populated if found in attributes
            'bathrooms': None,  # Default to None unless specified
            'energy_rate': None,  # Will be populated if found in attributes
            'ges': None,  # Will be populated if found in attributes
            'latitude': ad['location'].get('lat'),
            'longitude': ad['location'].get('lng'),
            'location_city': ad['location'].get('city_label'),
            'location_inseecode': ad['location'].get('department_id'),
            'adresse': None,  # Default to None unless specified
            'land_surface': None,  # Will be populated if found in attributes
            'parking': None,  # Default to None unless specified
            'cellar': None,  # Default to None unless specified
            'swimming_pool': None,  # Default to None unless specified
            'equipments': None,  # Will be concatenated from specific attributes
            'elevator': None,  # Will be populated if found in attributes
            'fai_included': None,  # Will be populated if found in attributes
            'floor_number': None,  # Default to None unless specified
            'nb_floors_building': None,  # Will be populated if found in attributes
            'outside_access': None,  # Will be populated if found in attributes
            'building_year': None,  # Will be populated if found in attributes
            'annual_charges': None  # Will be populated if found in attributes
        }

        # Extracting specific attributes
        for attribute in ad['attributes']:
            key = attribute.get('key')
            value = attribute.get('value')

            if key == 'real_estate_type':
                transformed_ad['real_estate_type'] = attribute['value_label']
            elif key == 'square':
                transformed_ad['square'] = float(value)
            elif key == 'rooms':
                transformed_ad['rooms'] = int(value)
            elif key == 'bedrooms':
                transformed_ad['bedrooms'] = int(value)
            elif key == 'energy_rate':
                transformed_ad['energy_rate'] = attribute['value_label']
            elif key == 'ges':
                transformed_ad['ges'] = attribute['value_label']
            elif key == 'land_plot_surface':
                transformed_ad['land_surface'] = float(value)
            elif key == 'elevator':
                transformed_ad['elevator'] = (value == '1')
            elif key == 'fai_included':
                transformed_ad['fai_included'] = (value == '1')
            elif key == 'nb_floors_building':
                transformed_ad['nb_floors_building'] = int(value)
            elif key == 'outside_access':
                transformed_ad['outside_access'] = attribute['value_label']
            elif key == 'building_year':
                transformed_ad['building_year'] = int(value)
            elif key == 'annual_charges':
                transformed_ad['annual_charges'] = float(value)
            elif key == 'old_price':
                transformed_ad['old_price'] = float(value)

        # Extract images
        transformed_ad['images'] = [
            {'url': image_url} for image_url in ad['images']['urls']
        ]

        transformed_ads.append(transformed_ad)

    return transformed_ads

def scrape_all_city_listings(insee_code: str) -> int:
    """
    Scrape all listings for a given city from Leboncoin.

    Args:
        insee_code (str): The INSEE code of the city to scrape.

    Returns:
        int: Total number of ads processed.
    """
    # Retrieve the URL for the city using the INSEE code
    base_url_data = get_leboncoin_urls_by_conditions(insee_code=insee_code)
    if not base_url_data:
        logging.error(f"No URL found for INSEE code: {insee_code}")
        return 0

    base_url = base_url_data[0].url
    total_ads_processed = 0

    page = 1
    while True:
        # Construct the paginated URL
        paginated_url = f"{base_url}&page={page}"
        
        # Retrieve the HTML content
        html_content = retrieve_html(paginated_url)
        
        if html_content == 'noResult':
            logging.info(f"No results on page {page} for URL: {base_url}")
            break  # Exit loop if no results

        # Convert HTML to JSON
        json_data = html_to_json(html_content)
        if not json_data:
            logging.warning(f"Failed to extract JSON from page {page} for URL: {base_url}")
            break  # Exit loop if JSON conversion fails

        # Extract ads from the JSON data
        ads_list = extract_ads(json_data)
        if not ads_list:
            logging.info(f"No ads found on page {page} for URL: {base_url}")
            break  # Exit loop if no ads are found

        # Transform and process ads
        sql_ready_data = extract_properties(ads_list)
        for ad in sql_ready_data:
            process_ad(ad)
            total_ads_processed += 1
        
        logging.info(f"Processed {len(sql_ready_data)} ads from page {page} for URL: {base_url}")

        # Move to the next page
        page += 1
    
    logging.info(f"Total ads processed: {total_ads_processed}")
    return total_ads_processed
