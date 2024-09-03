#client_onboarding.py

"""
Description:
------------
This module handles the onboarding process for new clients, including the addition or update of client and city information in the database.

Features:
---------
- Adds or updates cities in the database.
- Adds or updates client information in the database.
- Logs errors encountered during the process and confirms successful operations.

Main Functions:
---------------
1. onboarding_client(first_name: str, last_name: str, email: str, is_active: bool, selected_cities: list[list[str]]):
   - Onboards a new client by adding/updating their information and associated cities in the database.
"""

import logging
from storage import add_or_update_client, add_or_update_city


def onboard_client(first_name: str, last_name: str, email: str, is_active: bool, city_data: list[list[str]]):
    """
    Handles the onboarding of a new client by ensuring that the client and their associated cities
    are added or updated in the database.

    Args:
        first_name (str): The first name of the client.
        last_name (str): The last name of the client.
        email (str): The email address of the client.
        is_active (bool): Whether the client is active or not.
        city_data (list[list[str]]): A list of lists, each containing [zipcode, insee_code, city_name].
    """
    try:
        for city_info in city_data:
            add_or_update_city(city_info)
        logging.info(f"All cities processed for client {email}.")
        
        add_or_update_client(first_name, last_name, email, is_active, city_data)
        logging.info(f"Client {email} successfully onboarded.")
        
    except Exception as e:
        logging.error(f"Error during onboarding for client {email}: {e}", exc_info=True)