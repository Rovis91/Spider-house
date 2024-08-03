"""
utils.py
--------

This module contains utility functions for validating ad data.
"""
import re
from typing import List, Dict, Any

def validate_data(ad: Dict[str, Any]) -> List[str]:
    """
    Validate ad data to ensure it meets expected criteria.

    Args:
        ad (Dict[str, Any]): The ad data to validate.

    Returns:
        List[str]: A list of validation error messages.
    """
    errors = []

    # Verify the presence and type of mandatory fields
    if not isinstance(ad.get('id'), int):
        errors.append('Invalid or missing id')
    if not ad.get('publication_date'):
        errors.append('Missing publication_date')
    if ad.get('status') not in ['active', 'inactive']:
        errors.append('Invalid status')
    if not ad.get('title') or len(ad['title']) > 100:
        errors.append('Invalid or missing title')
    if not ad.get('url') or len(ad['url']) > 255:
        errors.append('Invalid or missing url')
    if not isinstance(ad.get('price'), (int, float)):
        errors.append('Invalid or missing price')
    if ad.get('latitude') and not isinstance(ad['latitude'], (int, float)):
        errors.append('Invalid latitude')
    if ad.get('longitude') and not isinstance(ad['longitude'], (int, float)):
        errors.append('Invalid longitude')
    if ad.get('location_city') and len(ad['location_city']) > 100:
        errors.append('Invalid location_city')
    if ad.get('location_zipcode') and (not isinstance(ad['location_zipcode'], int) or not (10000 <= ad['location_zipcode'] <= 99999)):
        errors.append('Invalid location_zipcode')
    if ad.get('type') not in ['professional', 'private']:
        errors.append('Invalid type')
    if ad.get('real_estate_type') not in ['Apartment', 'House', 'Other', 'Parking', 'Land']:
        errors.append('Invalid real_estate_type')
    if ad.get('square') and not isinstance(ad['square'], (int, float)):
        errors.append('Invalid square')
    if ad.get('rooms') and not isinstance(ad['rooms'], int):
        errors.append('Invalid rooms')
    if ad.get('energy_rate') and not re.match('^[A-G]$', ad['energy_rate']):
        errors.append('Invalid energy_rate')
    if ad.get('ges') and not re.match('^[A-G]$', ad['ges']):
        errors.append('Invalid ges')
    if ad.get('bathrooms') and not isinstance(ad['bathrooms'], int):
        errors.append('Invalid bathrooms')
    if ad.get('land_surface') and not isinstance(ad['land_surface'], (int, float)):
        errors.append('Invalid land_surface')
    if ad.get('parking') and not isinstance(ad['parking'], bool):
        errors.append('Invalid parking')
    if ad.get('cellar') and not isinstance(ad['cellar'], bool):
        errors.append('Invalid cellar')
    if ad.get('swimming_pool') and not isinstance(ad['swimming_pool'], bool):
        errors.append('Invalid swimming_pool')
    if ad.get('equipments') and not isinstance(ad['equipments'], str):
        errors.append('Invalid equipments')
    if ad.get('elevator') and not isinstance(ad['elevator'], bool):
        errors.append('Invalid elevator')
    if ad.get('fai_included') and not isinstance(ad['fai_included'], bool):
        errors.append('Invalid fai_included')
    if ad.get('floor_number') and not isinstance(ad['floor_number'], int):
        errors.append('Invalid floor_number')
    if ad.get('nb_floors_building') and not isinstance(ad['nb_floors_building'], int):
        errors.append('Invalid nb_floors_building')
    if ad.get('outside_access') and len(ad['outside_access']) > 50:
        errors.append('Invalid outside_access')
    if ad.get('building_year') and not isinstance(ad['building_year'], int):
        errors.append('Invalid building_year')
    if ad.get('annual_charges') and (not isinstance(ad['annual_charges'], (int, float)) or ad['annual_charges'] < 0):
        errors.append('Invalid annual_charges')
    if ad.get('bedrooms') and not isinstance(ad['bedrooms'], int):
        errors.append('Invalid bedrooms')
    if ad.get('immo_sell_type') and len(ad['immo_sell_type']) > 20:
        errors.append('Invalid immo_sell_type')
    if ad.get('old_price') and not isinstance(ad['old_price'], (int, float)):
        errors.append('Invalid old_price')

    # Verify that there is at least one image URL
    images = ad.get('images', [])
    if not images or not isinstance(images, list) or not all(isinstance(url, str) for url in images) or len(images) == 0:
        errors.append('Missing or invalid images')

    return errors
