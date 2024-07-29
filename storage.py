"""
storage.py
----------

This module handles the storage and retrieval of JSON data for all listings.
"""
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

def store_data_to_sql(ad):
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
        
    except Exception as e:
        print(f"Error inserting ad data: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
