-- Création des types énumérés
CREATE TYPE status_enum AS ENUM ('active', 'inactive');
CREATE TYPE owner_type_enum AS ENUM ('professional', 'private');
CREATE TYPE real_estate_type_enum AS ENUM ('Apartment', 'House', 'Other', 'Parking', 'Land');

-- Création de la table des annonces
CREATE TABLE annonces (
    id BIGINT PRIMARY KEY,
    publication_date TIMESTAMP NOT NULL,
    status status_enum NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,  -- Optionnel
    url VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL, 
    latitude DECIMAL(10, 7),  -- Optionnel, Format XX.XXXXXXX
    longitude DECIMAL(10, 7),  -- Optionnel, Format XX.XXXXXXX
    location_city VARCHAR(100),  -- Optionnel
    location_zipcode INTEGER CHECK (location_zipcode >= 10000 AND location_zipcode <= 99999),  -- Optionnel, entier à 5 chiffres
    type owner_type_enum NOT NULL,  -- Type de propriétaire (professional ou private)
    real_estate_type real_estate_type_enum NOT NULL,  -- Type de bien immobilier (requis)
    square DECIMAL(10, 2),  -- Superficie (en m²), Optionnel
    rooms INT,  -- Nombre de pièces, Optionnel
    energy_rate VARCHAR(1) CHECK (energy_rate ~ '^[A-G]$'),  -- Classe énergétique, Optionnel, accepte une seule lettre majuscule entre A et G
    ges VARCHAR(1) CHECK (ges ~ '^[A-G]$'),  -- GES, Optionnel, accepte une seule lettre majuscule entre A et G
    bathrooms INT,  -- Nombre de salles de bain, Optionnel
    land_surface DECIMAL(10, 2),  -- Superficie du terrain (en m²), Optionnel
    parking BOOLEAN,  -- Présence d'un parking (Oui/Non), Optionnel
    cellar BOOLEAN,  -- Présence d'une cave (Oui/Non), Optionnel
    swimming_pool BOOLEAN,  -- Présence d'une piscine (Oui/Non), Optionnel
    equipments TEXT,  -- Liste des équipements (séparés par des virgules), Optionnel
    elevator BOOLEAN,  -- Ascenseur (Oui/Non), Optionnel
    fai_included BOOLEAN,  -- Frais inclus (Oui/Non), Optionnel
    floor_number INT,  -- Étage du bien, Optionnel
    nb_floors_building INT,  -- Nombre d'étages dans le bâtiment, Optionnel
    outside_access VARCHAR(50),  -- Extérieurs (Balcon, Terrasse, etc.), Optionnel
    building_year INT,  -- Année de construction, Optionnel
    annual_charges DECIMAL(10, 2) CHECK (annual_charges >= 0),  -- Charges annuelles de copropriété, Optionnel
    bedrooms INT,  -- Nombre de chambres, Optionnel
    immo_sell_type VARCHAR(20),  -- Type de vente (Ancien, Neuf, etc.), Optionnel
    old_price DECIMAL(10, 2)  -- Ancien prix, Optionnel
);

-- Création de la table des images
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    ad_id BIGINT REFERENCES annonces(id) ON DELETE CASCADE,
    url VARCHAR(255) NOT NULL
);

-- Création des index séparément
CREATE INDEX idx_publication_date ON annonces(publication_date);
CREATE INDEX idx_location_city ON annonces(location_city);

-- Création des tables des villes et des URLs par site
CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    zipcode VARCHAR(5) NOT NULL,
    insee_code VARCHAR(5) NOT NULL UNIQUE,
    city_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS leboncoin_urls (
    id SERIAL PRIMARY KEY,
    insee_code VARCHAR(5) NOT NULL REFERENCES cities(insee_code) ON DELETE CASCADE,
    url VARCHAR(255) NOT NULL
);
