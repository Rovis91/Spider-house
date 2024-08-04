"""
storage.py
----------

This module handles the storage and retrieval of JSON data for all listings.
"""

import logging
import os
import re
from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Environment variables for database connection
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Create the database engine
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
Session = sessionmaker(bind=engine)

# SQLAlchemy setup
Base = declarative_base()

class Annonce(Base):
    __tablename__ = 'annonces'

    id = Column(Integer, primary_key=True)
    publication_date = Column(DateTime, nullable=False)
    status = Column(Enum('active', 'inactive', name='status_enum'), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    url = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location_city = Column(String(100), nullable=True)
    location_zipcode = Column(Integer, nullable=True)
    type = Column(Enum('professional', 'private', name='owner_type_enum'), nullable=False)
    real_estate_type = Column(Enum('Apartment', 'House', 'Other', 'Parking', 'Land', name='real_estate_type_enum'), nullable=False)
    square = Column(Integer, nullable=True)
    rooms = Column(Integer, nullable=True)
    energy_rate = Column(String(1), nullable=True)
    ges = Column(String(1), nullable=True)
    bathrooms = Column(Integer, nullable=True)
    land_surface = Column(Integer, nullable=True)
    parking = Column(Boolean, nullable=True)
    cellar = Column(Boolean, nullable=True)
    swimming_pool = Column(Boolean, nullable=True)
    equipments = Column(String, nullable=True)
    elevator = Column(Boolean, nullable=True)
    fai_included = Column(Boolean, nullable=True)
    floor_number = Column(Integer, nullable=True)
    nb_floors_building = Column(Integer, nullable=True)
    outside_access = Column(String(50), nullable=True)
    building_year = Column(Integer, nullable=True)
    annual_charges = Column(Integer, nullable=True)
    bedrooms = Column(Integer, nullable=True)
    immo_sell_type = Column(String(20), nullable=True)
    old_price = Column(Integer, nullable=True)
    images = relationship("Image", back_populates="annonce")

class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    ad_id = Column(Integer, ForeignKey('annonces.id', ondelete='CASCADE'))
    url = Column(String(255), nullable=False)
    annonce = relationship("Annonce", back_populates="images")

def validate_data(ad: Dict[str, Any]) -> List[str]:
    """
    Validate ad data to ensure it meets expected criteria.

    Args:
        ad (Dict[str, Any]): The ad data to validate.

    Returns:
        List[str]: A list of validation error messages.
    """
    errors = []

    # 1. ID (Required, positive integer)
    if not isinstance(ad.get('id'), int) or ad['id'] <= 0:
        errors.append('Invalid or missing id')

    # 2. Publication Date (Required, timestamp format)
    if not ad.get('publication_date'):
        errors.append('Missing publication_date')
    else:
        try:
            datetime.strptime(ad['publication_date'], '%Y-%m-%d %H:%M:%S')  # Validate timestamp format
        except ValueError:
            errors.append('Invalid publication_date format')

    # 3. Status (Required, must be 'active' or 'inactive')
    if ad.get('status') not in ['active', 'inactive']:
        errors.append('Invalid status')

    # 4. Title (Required, string with a maximum length)
    if not ad.get('title') or len(ad['title']) > 100:
        errors.append('Invalid or missing title')

    # 5. URL (Required, string with a maximum length)
    if not ad.get('url') or len(ad['url']) > 255:
        errors.append('Invalid or missing url')

    # 6. Price (Required, must be an integer)
    if not isinstance(ad.get('price'), int):
        errors.append('Invalid or missing price')

    # 7. Latitude (Optional, float between -90 and 90)
    if ad.get('latitude') is not None and not isinstance(ad['latitude'], (int, float)):
        errors.append('Invalid latitude')
    elif ad.get('latitude') is not None and not (-90 <= ad['latitude'] <= 90):
        errors.append('Latitude out of range')

    # 8. Longitude (Optional, float between -180 and 180)
    if ad.get('longitude') is not None and not isinstance(ad['longitude'], (int, float)):
        errors.append('Invalid longitude')
    elif ad.get('longitude') is not None and not (-180 <= ad['longitude'] <= 180):
        errors.append('Longitude out of range')

    # 9. City (Optional, string with a maximum length)
    if ad.get('location_city') and len(ad['location_city']) > 100:
        errors.append('Invalid location_city')

    # 10. Zip Code (Optional, integer with 5 digits)
    if ad.get('location_zipcode') and (not isinstance(ad['location_zipcode'], int) or not (10000 <= ad['location_zipcode'] <= 99999)):
        errors.append('Invalid location_zipcode')

    # 11. Owner Type (Required, must be 'professional' or 'private')
    if ad.get('type') not in ['professional', 'private']:
        errors.append('Invalid type')

    # 12. Real Estate Type (Required, must be one of the defined types)
    if ad.get('real_estate_type') not in ['Apartment', 'House', 'Other', 'Parking', 'Land']:
        errors.append('Invalid real_estate_type')

    # 13. Square Meters (Optional, must be an integer)
    if ad.get('square') is not None and not isinstance(ad['square'], int):
        errors.append('Invalid square')

    # 14. Rooms (Optional, positive integer)
    if ad.get('rooms') is not None and not isinstance(ad['rooms'], int):
        errors.append('Invalid rooms')

    # 15. Energy Rate (Optional, single letter from A to G)
    if ad.get('energy_rate') and not re.match('^[A-G]$', ad['energy_rate']):
        errors.append('Invalid energy_rate')

    # 16. GES (Optional, single letter from A to G)
    if ad.get('ges') and not re.match('^[A-G]$', ad['ges']):
        errors.append('Invalid ges')

    # 17. Bathrooms (Optional, positive integer)
    if ad.get('bathrooms') is not None and not isinstance(ad['bathrooms'], int):
        errors.append('Invalid bathrooms')

    # 18. Land Surface (Optional, must be an integer)
    if ad.get('land_surface') is not None and not isinstance(ad['land_surface'], int):
        errors.append('Invalid land_surface')

    # 19. Parking (Optional, boolean)
    if ad.get('parking') is not None and not isinstance(ad['parking'], bool):
        errors.append('Invalid parking')

    # 20. Cellar (Optional, boolean)
    if ad.get('cellar') is not None and not isinstance(ad['cellar'], bool):
        errors.append('Invalid cellar')

    # 21. Swimming Pool (Optional, boolean)
    if ad.get('swimming_pool') is not None and not isinstance(ad['swimming_pool'], bool):
        errors.append('Invalid swimming_pool')

    # 22. Equipments (Optional, string with maximum length and limited items)
    if ad.get('equipments') is not None and not isinstance(ad['equipments'], str):
        errors.append('Invalid equipments')
    elif ad.get('equipments') is not None and len(ad['equipments'].split(',')) > 10:
        errors.append('Too many equipment items')

    # 23. Elevator (Optional, boolean)
    if ad.get('elevator') is not None and not isinstance(ad['elevator'], bool):
        errors.append('Invalid elevator')

    # 24. Fees Included (Optional, boolean)
    if ad.get('fai_included') is not None and not isinstance(ad['fai_included'], bool):
        errors.append('Invalid fai_included')

    # 25. Floor Number (Optional, integer)
    if ad.get('floor_number') is not None and not isinstance(ad['floor_number'], int):
        errors.append('Invalid floor_number')

    # 26. Number of Floors in Building (Optional, integer)
    if ad.get('nb_floors_building') is not None and not isinstance(ad['nb_floors_building'], int):
        errors.append('Invalid nb_floors_building')

    # 27. Outside Access (Optional, string with a maximum length)
    if ad.get('outside_access') and len(ad['outside_access']) > 50:
        errors.append('Invalid outside_access')

    # 28. Building Year (Optional, integer)
    if ad.get('building_year') is not None and not isinstance(ad['building_year'], int):
        errors.append('Invalid building_year')

    # 29. Annual Charges (Optional, must be a positive integer)
    if ad.get('annual_charges') is not None and (not isinstance(ad['annual_charges'], int) or ad['annual_charges'] < 0):
        errors.append('Invalid annual_charges')

    # 30. Bedrooms (Optional, integer)
    if ad.get('bedrooms') is not None and not isinstance(ad['bedrooms'], int):
        errors.append('Invalid bedrooms')

    # 31. Real Estate Sell Type (Optional, expected data includes 'new', 'renovated', 'old', etc.)
    if ad.get('immo_sell_type') and len(ad['immo_sell_type']) > 20:
        errors.append('Invalid immo_sell_type')

    # 32. Old Price (Optional, must be an integer)
    if ad.get('old_price') is not None and not isinstance(ad['old_price'], int):
        errors.append('Invalid old_price')

    # 33. Images (Required, must contain at least one valid URL string)
    images = ad.get('images', [])
    if not images or not isinstance(images, list) or not all(isinstance(url, str) for url in images) or len(images) == 0:
        errors.append('Missing or invalid images')

    return errors

def process_ad(ad_data: Dict[str, Any]):
    """
    Process ad data: validate, insert or update in the database.

    Args:
        ad_data (Dict[str, Any]): The ad data to process.
    """
    session = Session()

    # Validate data
    errors = validate_data(ad_data)
    if errors:
        logging.error(f"Validation errors for ad {ad_data.get('id')}: {errors}")
        return

    try:
        # Check if the ad already exists
        existing_ad = session.query(Annonce).filter_by(id=ad_data['id']).first()

        if existing_ad:
            # Update price if necessary
            if existing_ad.price != ad_data['price']:
                existing_ad.price = ad_data['price']
                logging.info(f"Updated price for ad {ad_data['id']}")
        else:
            # Insert new ad using explicit parameter mapping
            new_ad = Annonce(
                id=ad_data['id'],
                publication_date=datetime.strptime(ad_data['publication_date'], '%Y-%m-%d %H:%M:%S'),
                status=ad_data['status'],
                title=ad_data['title'],
                description=ad_data.get('description'),
                url=ad_data['url'],
                price=ad_data['price'],
                latitude=ad_data.get('latitude'),
                longitude=ad_data.get('longitude'),
                location_city=ad_data.get('location_city'),
                location_zipcode=ad_data.get('location_zipcode'),
                type=ad_data['type'],
                real_estate_type=ad_data['real_estate_type'],
                square=ad_data.get('square'),
                rooms=ad_data.get('rooms'),
                energy_rate=ad_data.get('energy_rate'),
                ges=ad_data.get('ges'),
                bathrooms=ad_data.get('bathrooms'),
                land_surface=ad_data.get('land_surface'),
                parking=ad_data.get('parking'),
                cellar=ad_data.get('cellar'),
                swimming_pool=ad_data.get('swimming_pool'),
                equipments=ad_data.get('equipments'),
                elevator=ad_data.get('elevator'),
                fai_included=ad_data.get('fai_included'),
                floor_number=ad_data.get('floor_number'),
                nb_floors_building=ad_data.get('nb_floors_building'),
                outside_access=ad_data.get('outside_access'),
                building_year=ad_data.get('building_year'),
                annual_charges=ad_data.get('annual_charges'),
                bedrooms=ad_data.get('bedrooms'),
                immo_sell_type=ad_data.get('immo_sell_type'),
                old_price=ad_data.get('old_price')
            )
            session.add(new_ad)
            logging.info(f"Inserted new ad {ad_data['id']}")

        session.flush()  # Ensure ad ID is available before adding images

        # Handle images
        for url in ad_data['images']:
            image_exists = session.query(Image).filter_by(ad_id=ad_data['id'], url=url).first()
            if not image_exists:
                new_image = Image(ad_id=ad_data['id'], url=url)
                session.add(new_image)
                logging.info(f"Inserted image for ad {ad_data['id']}")

        session.commit()

    except Exception as e:
        session.rollback()
        logging.error(f"Error processing ad {ad_data['id']}: {e}")
    finally:
        session.close()
