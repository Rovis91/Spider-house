-- Création des types énumérés
CREATE TYPE status_enum AS ENUM ('active', 'inactive');
CREATE TYPE owner_type_enum AS ENUM ('professional', 'private');
CREATE TYPE real_estate_type_enum AS ENUM ('Apartment', 'House', 'Other', 'Parking', 'Land');

-- Create the new table with the updated schema
CREATE TABLE IF NOT EXISTS listing (
    id BIGINT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,  -- Optional
    url VARCHAR(255) NOT NULL,
    publication_date TIMESTAMP NOT NULL,
    price DECIMAL(10, 2) NOT NULL, 
    old_price DECIMAL(10, 2),  -- Old price, Optional
    immo_sell_type VARCHAR(20),  -- Sale type (Old, New, etc.), Optional
    status status_enum NOT NULL,
    type owner_type_enum NOT NULL,  -- Owner type (professional or private)
    real_estate_type real_estate_type_enum NOT NULL,  -- Real estate type (required)
    square DECIMAL(10, 2),  -- Surface area (in m²), Optional
    rooms INT,  -- Number of rooms, Optional
    bedrooms INT,  -- Number of bedrooms, Optional
    bathrooms INT,  -- Number of bathrooms, Optional
    energy_rate VARCHAR(1) CHECK (energy_rate ~ '^[A-G]$'),  -- Energy class, Optional, accepts a single uppercase letter between A and G
    ges VARCHAR(1) CHECK (ges ~ '^[A-G]$'),  -- GES, Optional, accepts a single uppercase letter between A and G
    latitude DECIMAL(10, 7),  -- Optional, Format XX.XXXXXXX
    longitude DECIMAL(10, 7),  -- Optional, Format XX.XXXXXXX
    location_city VARCHAR(100),  -- Optional
    location_inseecode VARCHAR(20) NOT NULL,  -- Mandatory INSEE code
    adresse VARCHAR(100),  -- Address, Optional
    land_surface DECIMAL(10, 2),  -- Land area (in m²), Optional
    parking BOOLEAN,  -- Parking availability (Yes/No), Optional
    cellar BOOLEAN,  -- Cellar availability (Yes/No), Optional
    swimming_pool BOOLEAN,  -- Swimming pool availability (Yes/No), Optional
    equipments TEXT,  -- List of equipments (comma-separated), Optional
    elevator BOOLEAN,  -- Elevator availability (Yes/No), Optional
    fai_included BOOLEAN,  -- Fees included (Yes/No), Optional
    floor_number INT,  -- Property floor number, Optional
    nb_floors_building INT,  -- Number of floors in the building, Optional
    outside_access VARCHAR(50),  -- Exterior access (Balcony, Terrace, etc.), Optional
    building_year INT,  -- Year of construction, Optional
    annual_charges DECIMAL(10, 2) CHECK (annual_charges >= 0)  -- Annual co-ownership charges, Optional
);

-- Create an index on location_inseecode for better performance
CREATE INDEX idx_location_inseecode ON listing (location_inseecode);

-- Create an index on publication_date for better performance
CREATE INDEX idx_publication_date ON listing (publication_date);

-- Create the table for images
CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    ad_id BIGINT REFERENCES listing(id) ON DELETE CASCADE,
    url VARCHAR(255) NOT NULL
);

-- Updated clients table with city codes as VARCHAR(5)
CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    selected_cities VARCHAR(5)[] NOT NULL,  -- City codes stored as strings
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index sur l'email pour éviter les doublons et optimiser les recherches
CREATE INDEX idx_email ON clients (email);

-- Index sur is_active pour optimiser les recherches des clients actifs
CREATE INDEX idx_is_active ON clients (is_active);

-- Création des tables des villes et des URLs par site
CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    zipcode VARCHAR(5) NOT NULL,
    insee_code VARCHAR(5) NOT NULL UNIQUE,
    city_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS website_urls (
    id SERIAL PRIMARY KEY,
    insee_code VARCHAR(5) NOT NULL REFERENCES cities(insee_code) ON DELETE CASCADE,
    lbc_url VARCHAR(255), 
    pap_url VARCHAR(255), 
    etp_url VARCHAR(255),
    puv_url VARCHAR(255)

);
