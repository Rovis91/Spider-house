"""
scraper.py
----------

This module contains functions for retrieving real estate listings
from a given URL on the site leboncoin.fr. It uses Playwright to
automate navigation and bypass anti-bot protections.
"""

from playwright.sync_api import sync_playwright
import leboncoin.parsing as parsing
import leboncoin.config as config
import json

# Initialization and necessary imports.
