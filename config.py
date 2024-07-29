"""
config.py
---------

This module contains specific configurations for scraping leboncoin.fr,
including proxy settings and HTTP headers.
"""

import os
import random
import logging
from dotenv import load_dotenv
import urllib.request

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

def get_proxy_opener(username=USERNAME, password=PASSWORD, user_agent=USER_AGENT, country=COUNTRY, host=HOST, port=PORT):
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
    """
    try:
        # Ensure session_id is an integer
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
