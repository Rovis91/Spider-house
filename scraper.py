"""
proxy_scraper.py

Description:
------------
This module handles the retrieval of HTML content from websites using a proxy. 
It configures a proxy connection using environment variables and supports retry 
mechanisms to handle common HTTP errors, such as 502 Bad Gateway.

Features:
---------
- Loads environment variables for proxy configuration, including username, password, and host details.
- Creates a proxy opener with user-defined settings for secure web requests.
- Retrieves HTML content from target URLs using the configured proxy.
- Implements retry logic for handling specific HTTP errors to ensure robust web scraping.

Main Functions:
---------------
1. get_proxy_opener(username=USERNAME, password=PASSWORD, user_agent=USER_AGENT, country=COUNTRY, host=HOST, port=PORT) -> urllib.request.OpenerDirector:
   - Creates and returns a proxy opener using specified parameters, ensuring proper setup for web requests.

2. retrieve_html(target_url: str) -> Optional[str]:
   - Retrieves HTML content from the specified URL using the configured proxy opener and handles HTTP errors with retries.
"""


import os
import random
import logging
import urllib.request
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
USERNAME = os.getenv('BD_USERNAME')
PASSWORD = os.getenv('PASSWORD')
USER_AGENT = os.getenv('USER_AGENT')
COUNTRY = os.getenv('COUNTRY', 'fr')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_proxy_opener(username=USERNAME, password=PASSWORD, user_agent=USER_AGENT, country=COUNTRY, host=HOST, port=PORT) -> urllib.request.OpenerDirector:
    """
    Create a proxy opener with the specified parameters.

    Args:
        username (str): The proxy username.
        password (str): The proxy password.
        user_agent (str): The User-Agent string for HTTP headers.
        country (str): The country code for the proxy.
        host (str): The proxy host.
        port (str): The proxy port.

    Returns:
        urllib.request.OpenerDirector: The configured proxy opener.

    Raises:
        ValueError: If any required proxy parameters are missing.
        Exception: For other errors during proxy setup.
    """
    try:
        if not all([username, password, user_agent, host, port]):
            raise ValueError("All proxy parameters must be provided and non-empty.")

        # Generate a random session ID for the proxy
        session_id = random.randint(0, 1000000)
        super_proxy_url = f'http://{username}-country-{country}-session-{session_id}:{password}@{host}:{port}'
        
        logging.info(f'Proxy URL: {super_proxy_url}')
        
        proxy_handler = urllib.request.ProxyHandler({
            'http': super_proxy_url,
            'https': super_proxy_url,
        })
        
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [
            ('User-Agent', user_agent),
            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        ]
        
        return opener
    except Exception as e:
        logging.error(f'Error creating proxy opener: {e}')
        raise

def retrieve_html(target_url: str) -> Optional[str]:
    """
    Retrieve HTML content from a given URL using a proxy opener.

    Args:
        target_url (str): The URL of the target website.

    Returns:
        Optional[str]: The HTML content of the page, or None if an error occurs.
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            opener = get_proxy_opener()
            logging.info('Performing request to %s', target_url)
            response = opener.open(target_url)
            html_content = response.read().decode('utf-8')  # Decode the content to string
            logging.info('HTML content retrieved successfully')
            return html_content
        except urllib.error.HTTPError as e:
            if e.code == 502:
                logging.warning(f"HTTP 502 error encountered. Retrying ({attempt + 1}/{max_retries})...")
                continue  # Retry for 502 Bad Gateway
            elif e.code == 404:
                logging.error(f"Error 404: Not Found for URL {target_url}")
                return None
            else:
                logging.error(f"HTTP error {e.code} for URL {target_url}: {e.reason}")
                return None
        except Exception as e:
            logging.error(f"Error retrieving URL {target_url}: {e}")
            return None
    logging.error(f"Failed to retrieve URL {target_url} after {max_retries} attempts.")
    return None
