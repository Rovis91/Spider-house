"""
config.py
---------

This module contains specific configurations for scraping leboncoin.fr,
including proxy settings and HTTP headers.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

PROXY = {
    'http': os.getenv('PROXY_HTTP'),
    'https': os.getenv('PROXY_HTTPS')
}

# Initialization of configurations.
