"""
city_processor.py

Description:
------------
This module processes postal codes to retrieve associated city names and INSEE codes, 
and manages the generation and verification of Leboncoin URLs for these cities. 
It interacts with the database to update city and URL information and validates 
the accessibility of the URLs.

Features:
---------
- Fetches city names and INSEE codes using a public API based on postal codes.
- Generates Leboncoin URLs for real estate listings based on city names and postal codes.
- Verifies the accessibility and validity of the generated URLs by analyzing their HTML structure.
- Updates the database with city and URL information, handling errors and logging outcomes.

Main Functions:
---------------
1. process_postal_code(postal_code: str) -> List[Tuple[str, str, str]]:
   - Retrieves city names and INSEE codes based on the given postal code and updates the database.

2. generate_leboncoin_url(city_name: str, postal_code: str) -> str:
   - Generates a Leboncoin URL for a given city name and postal code.

3. verify_url_accessibility(url: str) -> bool:
   - Checks if the generated URL is accessible and has the expected HTML structure.

4. process_zipcode(zipcode: int):
   - Processes a postal code to generate, verify, and store URLs for associated cities.
"""


import logging
import requests
from typing import List, Tuple
from unidecode import unidecode
from bs4 import BeautifulSoup
from storage import add_or_update_city, add_or_update_leboncoin_url
from html_retriever import retrieve_html

def process_postal_code(postal_code: str) -> List[Tuple[str, str, str]]:
    """
    Process a postal code to retrieve the city names, INSEE codes, and update the database.

    Args:
        postal_code (str): The postal code to search for.

    Returns:
        List[Tuple[str, str, str]]: A list of tuples containing city names, INSEE codes, and the postal code.
    """
    url = f"https://api-adresse.data.gouv.fr/search/?q={postal_code}&type=municipality&autocomplete=0"
    response = requests.get(url)
    city_data = []  # To store tuples of (city_name, insee_code, postal_code)

    if response.status_code == 200:
        data = response.json()

        # Extract the city names and INSEE codes from the results
        for feature in data['features']:
            city_name = feature['properties']['city']
            insee_code = feature['properties']['citycode']

            # Add or update the city in the database
            add_or_update_city(zipcode=postal_code, insee_code=insee_code, city_name=city_name)

            # Store the city name, INSEE code, and postal code as a tuple
            city_data.append((city_name, insee_code, postal_code))

            logging.info(f"Processed city {city_name} with postal code {postal_code}.")
    else:
        logging.error(f"Error fetching city data for postal code {postal_code}: {response.status_code}")

    return city_data

def generate_leboncoin_url(city_name: str, postal_code: str) -> str:
    """
    Generate a Leboncoin URL for a given city name and postal code.

    Args:
        city_name (str): The name of the city.
        postal_code (str): The postal code of the city.

    Returns:
        str: The generated URL for the city on Leboncoin.
    """
    # Strip leading and trailing spaces from city_name and postal_code
    city_name = city_name.strip()
    postal_code = postal_code.strip()

    # Remove accents from city_name
    city_name = unidecode(city_name)

    # Replace spaces in the city name with hyphens
    city_name = city_name.replace(" ", "-")

    # Generate the URL in the specified format
    url = f"https://www.leboncoin.fr/cl/ventes_immobilieres/cp_{city_name}_{postal_code}"
    return url

def verify_url_accessibility(url: str) -> bool:
    """
    Verify if the generated URL is accessible by checking its HTML structure.

    Args:
        url (str): The URL to verify.

    Returns:
        bool: True if the URL is accessible and valid, False otherwise.
    """
    try:
        html_content = retrieve_html(url)
        if not html_content:
            logging.error(f"Error retrieving HTML content for URL {url}")
            return False

        soup = BeautifulSoup(html_content, 'html.parser')

        # Check for specific HTML elements to confirm page structure
        script_tag = soup.select_one('script#__NEXT_DATA__')
        search_tag = soup.select_one('div[data-test-id="sticky-filters-panel"]')
        ad_tag = soup.select_one('div[class="mb-lg"]')

        if script_tag and search_tag and ad_tag:
            return True
        else:
            logging.error(f"URL {url} is not accessible or does not have the expected HTML structure.")
            return False
    except Exception as e:
        logging.error(f"Error verifying URL {url}: {e}")
        return False

def process_zipcode(zipcode: int):
    """
    Process a zipcode, generating and verifying URLs for associated cities.

    Args:
        zipcode (int): The postal code to process.
    """
    city_data = process_postal_code(str(zipcode))  # This returns a list of (city_name, insee_code, postal_code) tuples

    if city_data:
        print("Cities found:")
        for city_name, insee_code, postal_code in city_data:
            print(f"- {city_name}")
            # Generate and verify the Leboncoin URL for each city
            leboncoin_url = generate_leboncoin_url(city_name, postal_code)
            print(f"  Generated URL: {leboncoin_url}")
            if verify_url_accessibility(leboncoin_url):
                print("  URL is accessible.")
                # Insert in database with URL
                add_or_update_leboncoin_url(insee_code, leboncoin_url)
                print("  URL added to the database.")
            else:
                print("  URL is not accessible or invalid.")
    else:
        print("No cities found or an error occurred.")
