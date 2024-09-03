
# scraper_base.py

"""
Description:
------------
This module provides a base class for web scrapers, abstracting common functionality 
such as HTML retrieval, pagination, and ad processing. It allows for easy extension 
to support scraping from multiple websites with different structures but similar goals.

Features:
---------
- Abstract base class for scrapers that includes common functionality.
- Handles HTML retrieval with proxy support.
- Supports pagination logic to scrape multiple pages until a known listing is found.
- Transforms ad data into a standardized format for easy storage.
- Easily extendable to support additional websites by inheriting and overriding methods.

Main Components:
----------------
1. BaseScraper (class):
   - Abstract base class providing common functionality for scrapers.

2. Derived Classes:
   - Example derived class for Leboncoin, showcasing how to implement website-specific scraping logic.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging
import json
from bs4 import BeautifulSoup
from html_retriever import retrieve_html
from storage import process_ad

class BaseScraper(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_html_content(self, url: str) -> Optional[str]:
        return retrieve_html(url)

    @abstractmethod
    def extract_ads(self, json_data: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """Extract ad listings from the JSON data. Must be implemented by derived classes."""
        pass

    @abstractmethod
    def transform_ad(self, ad_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform raw ad data into a standardized format. Must be implemented by derived classes."""
        pass

    def scrape_listings(self, insee_code: str) -> int:
        """
        Scrape all listings for a given city from the website, handling pagination.

        Args:
            insee_code (str): The INSEE code of the city to scrape.

        Returns:
            int: Total number of ads processed.
        """
        page = 1
        total_ads_processed = 0
        known_listings = self.get_known_listings()

        while True:
            paginated_url = f"{self.base_url}&page={page}"
            html_content = self.get_html_content(paginated_url)
            if not html_content or html_content == 'noResult':
                break
            
            json_data = self.html_to_json(html_content)
            if not json_data:
                break

            ads_list = self.extract_ads(json_data)
            if not ads_list:
                break

            for ad in ads_list:
                transformed_ad = self.transform_ad(ad)
                if self.is_known_listing(transformed_ad, known_listings):
                    return total_ads_processed

                process_ad(transformed_ad)
                total_ads_processed += 1
            
            page += 1
        
        return total_ads_processed

    def get_known_listings(self) -> List[str]:
        """Retrieve a list of known listings from the database to avoid duplicates."""
        # Implement the logic to get known listings
        return []

    def is_known_listing(self, ad_data: Dict[str, Any], known_listings: List[str]) -> bool:
        """Check if the ad is already known."""
        return ad_data['url'] in known_listings

    @abstractmethod
    def html_to_json(self, html_content: str) -> Optional[Dict[str, Any]]:
        """Convert HTML content to JSON. Must be implemented by derived classes."""
        pass

class LeboncoinScraper(BaseScraper):
    def extract_ads(self, json_data: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        try:
            return json_data['props']['pageProps']['searchData']['ads']
        except KeyError as e:
            logging.error(f"Error extracting ads: {e}")
            return None

    def transform_ad(self, ad_data: Dict[str, Any]) -> Dict[str, Any]:
        # Same transformation logic as before
        transformed_ad = {
            'id': ad_data.get('list_id'),
            'title': ad_data.get('subject', ''),
            # Additional fields here
        }
        # Extract specific attributes and process them
        for attribute in ad_data['attributes']:
            key = attribute.get('key')
            value = attribute.get('value')
            if key == 'real_estate_type':
                transformed_ad['real_estate_type'] = attribute['value_label']
            # Additional attribute processing

        transformed_ad['images'] = [{'url': image_url} for image_url in ad_data['images']['urls']]
        return transformed_ad

    def html_to_json(self, html_content: str) -> Optional[Dict[str, Any]]:
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tag = soup.select_one('script#__NEXT_DATA__')
        if script_tag:
            try:
                return json.loads(script_tag.string)
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON: {e}")
                return None
        logging.error('No script tag with id "__NEXT_DATA__" found.')
        return None

