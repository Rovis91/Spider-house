# storage.py

"""
Description:
------------
This module manages the storage and retrieval of JSON data for real estate listings,
using SQLAlchemy to interact with a PostgreSQL database. It provides functionalities
to validate data, and perform CRUD operations on real estate listings, cities,
Leboncoin URLs, and associated images.

Features:
---------
- Loads environment variables for database configuration.
- Defines data models with SQLAlchemy for cities, Leboncoin URLs, listings, and associated images.
- Validates data for listings, cities, URLs, and images to ensure compliance with required criteria.
- Inserts and updates data in the database with comprehensive error handling and logging.
- Supports dynamic retrieval of records based on specified conditions.
- Logs operations, warnings, and errors to facilitate debugging and monitoring.

Main Functions:
---------------
1. validate_data(ad: Dict[str, Any], model: Type[Base]) -> List[str]:
   - Validates data against the specified SQLAlchemy model to ensure it meets the expected criteria.

2. validate_image_data(image_data: Dict[str, Any]) -> List[str]:
   - Validates image data to ensure it meets the expected criteria.

3. validate_city_data(city_data: Dict[str, Any]) -> List[str]:
   - Validates city data to ensure it meets the expected criteria.

4. validate_url_data(url_data: Dict[str, Any]) -> List[str]:
   - Validates URL data to ensure it meets the expected criteria.

5. process_ad(ad_data: Dict[str, Any]):
   - Validates, inserts, or updates a listing in the database.
   - Manages the addition and updating of images associated with listings.

6. add_or_update_city(zipcode: str, insee_code: str, city_name: str):
   - Adds a new city or updates an existing city's information in the database.

7. add_or_update_leboncoin_url(insee_code: str, url: str):
   - Adds or updates a Leboncoin URL for a specific city in the database.

8. get_listings_by_conditions(**conditions) -> List[Listing]:
   - Retrieves listings based on specified conditions.

9. get_cities_by_conditions(**conditions) -> List[City]:
   - Retrieves cities based on specified conditions.

10. get_leboncoin_urls_by_conditions(**conditions) -> List[LeboncoinURL]:
    - Retrieves Leboncoin URLs based on specified conditions.

11. get_images_by_conditions(**conditions) -> List[Image]:
    - Retrieves images based on specified conditions.
"""

import logging
import os
import re
from typing import Type, Dict, Any, List
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, Boolean, DateTime, Enum,
    DECIMAL, Text, CheckConstraint, ForeignKey, BigInteger, ARRAY,and_
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set default log level to INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.StreamHandler(),  # Output logs to the console
        logging.FileHandler("app.log", mode='a')  # Log to a file
    ]
)

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

class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    zipcode = Column(String(5), nullable=False)
    insee_code = Column(String(5), nullable=False, unique=True)  
    city_name = Column(String(100), nullable=False)

    leboncoin_urls = relationship("LeboncoinURL", back_populates="city", cascade="all, delete-orphan")

class WebsiteURLs(Base):
    __tablename__ = 'website_urls'

    id = Column(Integer, primary_key=True)
    insee_code = Column(String(5), ForeignKey('cities.insee_code', ondelete='CASCADE'), nullable=False)
    lbc_url = Column(String(255), nullable=True)  # Leboncoin URL
    pap_url = Column(String(255), nullable=True)  # PAP URL
    etp_url = Column(String(255), nullable=True)  # EntreParticuliers URL
    puv_url = Column(String(255), nullable=True)  # ParuVendu URL

    # Relationship back to the City table (assuming this relationship is set up in the City class)
    city = relationship("City", back_populates="website_urls")

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    is_active = Column(Boolean, default=True, nullable=False)
    selected_cities = Column(ARRAY(String(5)), nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Listing(Base):
    __tablename__ = 'listings'

    id = Column(BigInteger, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(255), nullable=False)
    publication_date = Column(DateTime, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    old_price = Column(DECIMAL(10, 2), nullable=True)
    immo_sell_type = Column(String(20), nullable=True)
    status = Column(Enum('active', 'inactive', name='status_enum'), nullable=False)
    type = Column(Enum('professional', 'private', name='owner_type_enum'), nullable=False)
    real_estate_type = Column(Enum('Apartment', 'House', 'Other', 'Parking', 'Land', name='real_estate_type_enum'), nullable=False)
    square = Column(DECIMAL(10, 2), nullable=True)
    rooms = Column(Integer, nullable=True)
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    energy_rate = Column(String(1), nullable=True)
    ges = Column(String(1), nullable=True)
    latitude = Column(DECIMAL(10, 7), nullable=True)
    longitude = Column(DECIMAL(10, 7), nullable=True)
    location_city = Column(String(100), nullable=True)
    location_inseecode = Column(String(5), nullable=False)
    adresse = Column(String(100), nullable=True)
    land_surface = Column(DECIMAL(10, 2), nullable=True)
    parking = Column(Boolean, nullable=True)
    cellar = Column(Boolean, nullable=True)
    swimming_pool = Column(Boolean, nullable=True)
    equipments = Column(Text, nullable=True)
    elevator = Column(Boolean, nullable=True)
    fai_included = Column(Boolean, nullable=True)
    floor_number = Column(Integer, nullable=True)
    nb_floors_building = Column(Integer, nullable=True)
    outside_access = Column(String(50), nullable=True)
    building_year = Column(Integer, nullable=True)
    annual_charges = Column(DECIMAL(10, 2), nullable=True)

    images = relationship("Image", back_populates="listing", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("energy_rate ~ '^[A-G]$'", name='check_energy_rate'),
        CheckConstraint("ges ~ '^[A-G]$'", name='check_ges'),
        CheckConstraint("annual_charges >= 0", name='check_annual_charges_positive'),
    )

class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    ad_id = Column(BigInteger, ForeignKey('listings.id', ondelete='CASCADE'), nullable=False)
    url = Column(String(255), nullable=False)
    listing = relationship("Listing", back_populates="images")

def validate_data(ad: Dict[str, Any], model: Type[declarative_base]) -> List[str]:
    """
    Validate ad data based on the model's columns and constraints.

    Args:
        ad (Dict[str, Any]): The ad data to validate.
        model (Type[declarative_base]): The SQLAlchemy model class.

    Returns:
        List[str]: A list of validation error messages.
    """
    errors = []

    for column in model.__table__.columns:
        column_name = column.name
        value = ad.get(column_name)

        # Check for required fields
        if not column.nullable and value is None:
            errors.append(f'Missing required field: {column_name}')
            continue

        # Check data types and constraints
        if value is not None:
            # Check if the column type is Integer and validate the type of the value
            if isinstance(column.type, Integer) and not isinstance(value, int):
                errors.append(f'Invalid type for {column_name}, expected integer')
            
            # Check if the column type is DECIMAL and validate the type of the value
            elif isinstance(column.type, DECIMAL) and not isinstance(value, (int, float)):
                errors.append(f'Invalid type for {column_name}, expected decimal/float')
            
            # Check if the column type is Float and validate the type of the value
            elif isinstance(column.type, Float) and not isinstance(value, (int, float)):
                errors.append(f'Invalid type for {column_name}, expected float')
            
            # Check if the column type is String and validate the type and length of the value
            elif isinstance(column.type, String):
                if not isinstance(value, str):
                    errors.append(f'Invalid type for {column_name}, expected string')
                elif column.type.length and len(value) > column.type.length:
                    errors.append(f'{column_name} exceeds maximum length of {column.type.length}')
            
            # Check if the column type is Text and validate the type of the value
            elif isinstance(column.type, Text) and not isinstance(value, str):
                errors.append(f'Invalid type for {column_name}, expected string')
            
            # Check if the column type is Enum and validate the value
            elif isinstance(column.type, Enum) and value not in column.type.enums:
                errors.append(f'Invalid value for {column_name}, expected one of {column.type.enums}')

        # Specific validation for energy_rate
        if column_name == 'energy_rate' and value is not None and not re.match('^[A-G]$', value):
            errors.append(f'Invalid energy_rate, expected a single letter from A to G')

        # Specific validation for ges
        if column_name == 'ges' and value is not None and not re.match('^[A-G]$', value):
            errors.append(f'Invalid ges, expected a single letter from A to G')

        # Specific validation for annual_charges
        if column_name == 'annual_charges' and value is not None and value < 0:
            errors.append(f'Invalid annual_charges, must be non-negative')

    # Log validation results
    if errors:
        logging.error(f"Validation errors found: {errors}")
    else:
        logging.info("Validation successful with no errors.")

    return errors

def validate_image_data(image_data: Dict[str, Any]) -> List[str]:
    """
    Validate image data to ensure it meets expected criteria.

    Args:
        image_data (Dict[str, Any]): The image data to validate.

    Returns:
        List[str]: A list of validation error messages.
    """
    errors = []

    # Validate ad_id: Ensure it's a positive integer
    ad_id = image_data.get('ad_id')
    if not isinstance(ad_id, (int, BigInteger)) or ad_id <= 0:
        errors.append('Invalid or missing ad_id')

    # Validate URL: Ensure it's a non-empty string and within length constraints
    url = image_data.get('url')
    if not url or not isinstance(url, str):
        errors.append('Invalid or missing URL')
    elif len(url) > 255:
        errors.append('URL exceeds maximum length of 255 characters')

    # Log validation results
    if errors:
        logging.error(f"Image data validation errors: {errors}")
    else:
        logging.info("Image data validation successful with no errors.")

    return errors

def validate_city_data(city_data: Dict[str, Any]) -> List[str]:
    """
    Validate city data to ensure it meets expected criteria.

    Args:
        city_data (Dict[str, Any]): The city data to validate.

    Returns:
        List[str]: A list of validation error messages.
    """
    errors = []

    # Validate zipcode: Must be a 5-character string
    if not isinstance(city_data.get('zipcode'), str) or len(city_data['zipcode']) != 5:
        errors.append('Invalid or missing zipcode')

    # Validate INSEE code: Must be a 5-character string
    if not isinstance(city_data.get('insee_code'), str) or len(city_data['insee_code']) != 5:
        errors.append('Invalid or missing INSEE code')

    # Validate city name: Must be a non-empty string
    if not isinstance(city_data.get('city_name'), str) or not city_data['city_name']:
        errors.append('Invalid or missing city name')

    # Log validation results
    if errors:
        logging.error(f"City data validation errors: {errors}")
    else:
        logging.info("City data validation successful with no errors.")

    return errors

def validate_url_data(url_data: Dict[str, Any]) -> List[str]:
    """
    Validate URL data to ensure it meets expected criteria.

    Args:
        url_data (Dict[str, Any]): The URL data to validate.

    Returns:
        List[str]: A list of validation error messages.
    """
    errors = []

    # Validate INSEE code: Must be a 5-character string
    if not isinstance(url_data.get('insee_code'), str) or len(url_data['insee_code']) != 5:
        errors.append('Invalid or missing INSEE code')

    # Validate URL: Must be a non-empty string
    if not isinstance(url_data.get('url'), str) or not url_data['url']:
        errors.append('Invalid or missing URL')

    # Log validation results
    if errors:
        logging.error(f"URL data validation errors: {errors}")
    else:
        logging.info("URL data validation successful with no errors.")

    return errors

def process_ad(ad_data: Dict[str, Any]):
    """
    Process ad data: validate, insert or update in the database.

    Args:
        ad_data (Dict[str, Any]): The ad data to process.
    """
    session = Session()

    # Step 1: Handle Zipcode and City Lookup
    if 'zipcode' in ad_data and ('location_city' in ad_data or 'city' in ad_data):
        city_name = ad_data.get('location_city') or ad_data.get('city')
        city_record = session.query(City).filter_by(zipcode=ad_data['zipcode'], city_name=city_name).first()

        if city_record:
            logging.info(f"Found city {city_record.city_name} with zipcode {ad_data['zipcode']}")
            ad_data['location_inseecode'] = city_record.insee_code
        else:
            logging.warning(f"City {city_name} with zipcode {ad_data['zipcode']} not found in database.")

        del ad_data['zipcode']

    # Step 2: Ensure optional fields are set to None if unknown
    listing_fields = {col.name for col in Listing.__table__.columns}
    ad_data = {key: (None if key in listing_fields and ad_data[key] in ['', None] and Listing.__table__.columns[key].nullable else value)
               for key, value in ad_data.items()}

    # Step 3: Identify and log unused input data
    unused_data = set(ad_data.keys()) - listing_fields
    if unused_data:
        logging.info(f"Unused input data fields not found in class: {unused_data}")

    # Remove unused fields from ad_data
    ad_data = {k: v for k, v in ad_data.items() if k in listing_fields}

    # Validate ad data
    ad_errors = validate_data(ad_data, Listing)
    if ad_errors:
        logging.error(f"Validation errors for ad {ad_data.get('id')}: {ad_errors}")
        return

    try:
        # Attempt to find an existing ad with matching ID, URL, or title
        existing_ad = session.query(Listing).filter(
            (Listing.id == ad_data['id']) | 
            (Listing.url == ad_data['url']) | 
            (Listing.title == ad_data['title'])
        ).first()

        if existing_ad:
            # Check if at least two out of three identifiers match
            match_count = sum([
                existing_ad.id == ad_data['id'],
                existing_ad.url == ad_data['url'],
                existing_ad.title == ad_data['title']
            ])
            if match_count >= 2:
                # Update fields that have changed
                for key, value in ad_data.items():
                    if key not in ['price', 'images'] and getattr(existing_ad, key) != value:
                        setattr(existing_ad, key, value)
                        logging.info(f"Updated {key} for ad {ad_data['id']}")

                # Handle price update separately
                if existing_ad.price != ad_data['price']:
                    existing_ad.old_price = existing_ad.price
                    existing_ad.price = ad_data['price']
                    logging.info(f"Updated price for ad {ad_data['id']}")
        else:
            # Insert new ad record
            new_ad = Listing(**{k: v for k, v in ad_data.items() if k != 'images'})
            session.add(new_ad)
            logging.info(f"Inserted new ad {ad_data['id']}")

            # Flush to obtain ID for image associations
            session.flush()

            # Process and validate images
            for url in ad_data.get('images', []):
                image_data = {'ad_id': new_ad.id, 'url': url}
                image_errors = validate_image_data(image_data)
                if image_errors:
                    logging.error(f"Validation errors for image of ad {ad_data['id']}: {image_errors}")
                    continue

                # Insert new image record
                new_image = Image(ad_id=new_ad.id, url=url)
                session.add(new_image)
                logging.info(f"Inserted image for ad {ad_data['id']}")

        # Commit all changes to the database
        session.commit()

    except Exception as e:
        session.rollback()
        logging.error(f"Error processing ad {ad_data.get('id')}: {e}", exc_info=True)
    finally:
        # Close the session to release the connection
        session.close()

def add_or_update_city(zipcode: str, insee_code: str, city_name: str):
    """
    Add a new city or update an existing city's information.

    Args:
        zipcode (str): The postal code of the city.
        insee_code (str): The INSEE code of the city.
        city_name (str): The name of the city.
    """
    city_data = {'zipcode': zipcode, 'insee_code': insee_code, 'city_name': city_name}
    
    # Validate city data
    errors = validate_city_data(city_data)
    if errors:
        logging.error(f"Validation errors for city {city_name}: {errors}")
        return

    session = Session()
    try:
        # Attempt to find an existing city by INSEE code
        city = session.query(City).filter_by(insee_code=insee_code).first()
        if city:
            # Update existing city information
            city.zipcode = zipcode
            city.city_name = city_name
            logging.info(f"Updated city {city_name} with INSEE code {insee_code}")
        else:
            # Add a new city
            new_city = City(zipcode=zipcode, insee_code=insee_code, city_name=city_name)
            session.add(new_city)
            logging.info(f"Inserted new city {city_name} with INSEE code {insee_code}")

        # Commit the transaction to save changes
        session.commit()

    except IntegrityError:
        # Handle unique constraint violations, such as duplicate INSEE codes
        session.rollback()
        logging.warning(f"City with INSEE code {insee_code} already exists.")
    except Exception as e:
        # Log any other exceptions that occur
        session.rollback()
        logging.error(f"Error adding/updating city {city_name}: {e}", exc_info=True)
    finally:
        # Ensure the session is closed after processing
        session.close()

def add_or_update_website_url(insee_code: str, lbc_url: str = None, pap_url: str = None, etp_url: str = None, puv_url: str = None):
    """
    Add or update URLs for different websites for a specific city identified by its INSEE code.

    Args:
        insee_code (str): The INSEE code of the city.
        lbc_url (str): The URL of the city on Leboncoin.
        pap_url (str): The URL of the city on PAP.
        etp_url (str): The URL of the city on EntreParticuliers.
        puv_url (str): The URL of the city on ParuVendu.
    """
    session = Session()
    try:
        # Attempt to find an existing entry by INSEE code
        city_urls = session.query(WebsiteURLs).filter_by(insee_code=insee_code).first()
        if city_urls:
            # Update existing URLs if provided
            if lbc_url is not None:
                city_urls.lbc_url = lbc_url
                logging.info(f"Updated Leboncoin URL for city with INSEE code {insee_code}")
            if pap_url is not None:
                city_urls.pap_url = pap_url
                logging.info(f"Updated PAP URL for city with INSEE code {insee_code}")
            if etp_url is not None:
                city_urls.etp_url = etp_url
                logging.info(f"Updated EntreParticuliers URL for city with INSEE code {insee_code}")
            if puv_url is not None:
                city_urls.puv_url = puv_url
                logging.info(f"Updated ParuVendu URL for city with INSEE code {insee_code}")
        else:
            # Add a new entry with the provided URLs
            new_city_urls = WebsiteURLs(
                insee_code=insee_code,
                lbc_url=lbc_url,
                pap_url=pap_url,
                etp_url=etp_url,
                puv_url=puv_url
            )
            session.add(new_city_urls)
            logging.info(f"Inserted new URLs for city with INSEE code {insee_code}")

        # Commit the transaction to save changes
        session.commit()

    except IntegrityError:
        # Handle unique constraint violations, such as duplicate INSEE codes
        session.rollback()
        logging.warning(f"Website URLs for city with INSEE code {insee_code} already exist.")
    except Exception as e:
        # Log any other exceptions that occur
        session.rollback()
        logging.error(f"Error adding/updating website URLs for city with INSEE code {insee_code}: {e}", exc_info=True)
    finally:
        # Ensure the session is closed after processing
        session.close()

def add_or_update_client(first_name: str, last_name: str, email: str, is_active: bool, selected_cities: list[str]):
    """
    Add or update a client in the database.
    **Cities need to be added beforehand.**

    Args:
        first_name (str): The first name of the client.
        last_name (str): The last name of the client.
        email (str): The email address of the client.
        is_active (bool): Whether the client is active or not.
        selected_cities (List[str]): A list of INSEE codes of the cities the client is interested in.
    """
    session = Session()
    # Validate if cities exist in the database
    for city_insee_code in selected_cities:
        if not get_cities_by_conditions(insee_code=city_insee_code):
            logging.error(f"City data not found for INSEE code {city_insee_code}")
            return
            
    # Add or update client in database
    try:
        # Attempt to find an existing client by email
        client = session.query(Client).filter_by(email=email).first()
        if client:
            # Update existing client if provided
            if first_name is not None:
                client.first_name = first_name
                logging.info(f"Updated first name for client {email}")
            if last_name is not None:
                client.last_name = last_name
                logging.info(f"Updated last name for client {email}")
            if email is not None:
                client.email = email
                logging.info(f"Updated email for client {email}")
            if is_active is not None:
                client.is_active = is_active
                logging.info(f"Updated is_active for client {email}")
            if selected_cities is not None:
                client.selected_cities = selected_cities
                logging.info(f"Updated selected cities for client {email}")
        else:
            # Add a new client
            new_client = Client(first_name=first_name, last_name=last_name, email=email, selected_cities=selected_cities)
            session.add(new_client)
            logging.info(f"Inserted new client {email}")
        
        # Commit the transaction to save changes
        session.commit()
    except IntegrityError:
        # Handle unique constraint violations, such as duplicate email addresses
        session.rollback()
        logging.warning(f"Client with email {email} already exists.")
    except Exception as e:
        # Log any other exceptions that occur
        session.rollback()
        logging.error(f"Error adding/updating client {email}: {e}", exc_info=True)
    finally:
        # Ensure the session is closed after processing
        session.close()

def get_listings_by_conditions(**conditions) -> List[Listing]:
    """
    Retrieve listings based on various conditions.

    Args:
        **conditions: Arbitrary keyword arguments representing column names and their desired values.

    Returns:
        List[Listing]: A list of listings matching the specified conditions.
    """
    session = Session()
    try:
        query = session.query(Listing)

        # Build filters based on provided conditions
        filters = []
        for field, value in conditions.items():
            column = getattr(Listing, field, None)
            if column is not None:
                filters.append(column == value)
            else:
                logging.warning(f"Invalid field name {field} in conditions. It does not exist in Listing.")

        # Apply filters to the query
        if filters:
            query = query.filter(and_(*filters))
            logging.info(f"Retrieving listings with conditions: {conditions}")
        else:
            logging.info("No valid conditions provided. Retrieving all listings.")

        # Execute query and retrieve results
        listings = query.all()
        logging.info(f"Retrieved {len(listings)} listings.")

        return listings
    except Exception as e:
        logging.error(f"Error retrieving listings: {e}", exc_info=True)
        return []
    finally:
        # Ensure the session is closed after processing
        session.close()

def get_cities_by_conditions(**conditions) -> List[City]:
    """
    Retrieve cities based on various conditions.

    Args:
        **conditions: Arbitrary keyword arguments representing column names and their desired values.

    Returns:
        List[City]: A list of cities matching the specified conditions.
    """
    session = Session()
    try:
        query = session.query(City)

        # Build filters based on provided conditions
        filters = []
        for field, value in conditions.items():
            column = getattr(City, field, None)
            if column is not None:
                filters.append(column == value)
            else:
                logging.warning(f"Invalid field name {field} in conditions. It does not exist in City.")

        # Apply filters to the query
        if filters:
            query = query.filter(and_(*filters))
            logging.info(f"Retrieving cities with conditions: {conditions}")
        else:
            logging.info("No valid conditions provided. Retrieving all cities.")

        # Execute query and retrieve results
        cities = query.all()
        logging.info(f"Retrieved {len(cities)} cities.")

        return cities
    except Exception as e:
        logging.error(f"Error retrieving cities: {e}", exc_info=True)
        return []
    finally:
        # Ensure the session is closed after processing
        session.close()

def get_client_by_conditions(**conditions) -> Client:
    """ 
    Retrieve the client based on various conditions.

    Args:
        **conditions: Arbitrary keyword arguments representing column names and their desired values.

    Returns:
        Client: A client matching the specified conditions.
    """
    session = Session()
    try:
        query = session.query(Client)

        # Build filters based on provided conditions
        filters = []
        for field, value in conditions.items():
            column = getattr(Client, field, None)
            if column is not None:
                filters.append(column == value)
            else:
                logging.warning(f"Invalid field name {field} in conditions. It does not exist in Client.")

        # Apply filters to the query
        if filters:
            query = query.filter(and_(*filters))
            logging.info(f"Retrieving clients with conditions: {conditions}")
        else:
            logging.info("No valid conditions provided. Retrieving all clients.")
            
        # Execute query and retrieve results
        clients = query.all()
        logging.info(f"Retrieved {len(clients)} clients.")
        
        return clients        
    except Exception as e:
        logging.error(f"Error retrieving clients: {e}", exc_info=True)
        return []        
    finally:
        # Ensure the session is closed after processing
        session.close()   

def get_website_urls_by_insee_codes(insee_codes: List[str]) -> List[WebsiteURLs]:
    """
    Retrieve website URLs based on a list of INSEE codes.

    Args:
        insee_codes (List[str]): A list of INSEE codes to filter the results.

    Returns:
        List[WebsiteURLs]: A list of WebsiteURLs matching the specified INSEE codes.
    """
    session = Session()
    try:
        # Query the database for entries matching the provided INSEE codes
        urls = session.query(WebsiteURLs).filter(WebsiteURLs.insee_code.in_(insee_codes)).all()
        logging.info(f"Retrieved {len(urls)} Website URLs for INSEE codes: {insee_codes}")

        return urls
    except Exception as e:
        logging.error(f"Error retrieving Website URLs for INSEE codes {insee_codes}: {e}", exc_info=True)
        return []
    finally:
        # Ensure the session is closed after processing
        session.close()

def get_images_by_conditions(**conditions) -> List[Image]:
    """
    Retrieve images based on various conditions.

    Args:
        **conditions: Arbitrary keyword arguments representing column names and their desired values.

    Returns:
        List[Image]: A list of images matching the specified conditions.
    """
    session = Session()
    try:
        query = session.query(Image)

        # Build filters based on provided conditions
        filters = []
        for field, value in conditions.items():
            column = getattr(Image, field, None)
            if column is not None:
                filters.append(column == value)
            else:
                logging.warning(f"Invalid field name {field} in conditions. It does not exist in Image.")

        # Apply filters to the query
        if filters:
            query = query.filter(and_(*filters))
            logging.info(f"Retrieving images with conditions: {conditions}")
        else:
            logging.info("No valid conditions provided. Retrieving all images.")

        # Execute query and retrieve results
        images = query.all()
        logging.info(f"Retrieved {len(images)} images.")

        return images
    except Exception as e:
        logging.error(f"Error retrieving images: {e}", exc_info=True)
        return []
    finally:
        # Ensure the session is closed after processing
        session.close()