"""
storage.py
----------

This module handles the storage and retrieval of JSON data for all listings.
"""
import psycopg2
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def store_data_to_sql(ad):
    """
    Store ad data to the SQL database.
    
    Args:
        ad (dict): The ad data to store.
    """
    try:
        # Establish a database connection
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Insert the ad data into the database
        cursor.execute("""
            INSERT INTO annonces (
                id, publication_date, status, title, description, url, price, latitude, 
                longitude, location_city, location_zipcode, type, real_estate_type, square, 
                rooms, energy_rate, ges, bathrooms, land_surface, parking, cellar, 
                swimming_pool, equipments, elevator, fai_included, floor_number, 
                nb_floors_building, outside_access, building_year, annual_charges, 
                bedrooms, immo_sell_type, old_price
            ) VALUES (
                %(id)s, %(publication_date)s, %(status)s, %(title)s, %(description)s, %(url)s, %(price)s, %(latitude)s, 
                %(longitude)s, %(location_city)s, %(location_zipcode)s, %(type)s, %(real_estate_type)s, %(square)s, 
                %(rooms)s, %(energy_rate)s, %(ges)s, %(bathrooms)s, %(land_surface)s, %(parking)s, %(cellar)s, 
                %(swimming_pool)s, %(equipments)s, %(elevator)s, %(fai_included)s, %(floor_number)s, 
                %(nb_floors_building)s, %(outside_access)s, %(building_year)s, %(annual_charges)s, 
                %(bedrooms)s, %(immo_sell_type)s, %(old_price)s
            )
            ON CONFLICT (id) DO NOTHING
        """, ad)

        # Commit the transaction
        conn.commit()
        logging.info(f"Ad {ad['id']} inserted successfully")
        
    except psycopg2.Error as e:
        logging.error(f"Error inserting ad data: {e}")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def store_images_to_sql(ad_id: int, image_urls: list[str]):
    """
    Store image URLs to the SQL database for a given ad.

    Args:
        ad_id (int): The ID of the ad to associate images with.
        image_urls (List[str]): A list of image URLs to store.
    """
    if not image_urls:
        logging.info(f"No images to store for ad {ad_id}")
        return

    try:
        # Establish a database connection
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Insert the image URLs into the images table
        for url in image_urls:
            cursor.execute("""
                INSERT INTO images (ad_id, url) 
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (ad_id, url))

        # Commit the transaction
        conn.commit()
        logging.info(f"Images for ad {ad_id} inserted successfully")
        
    except psycopg2.Error as e:
        logging.error(f"Error inserting image data for ad {ad_id}: {e}")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
