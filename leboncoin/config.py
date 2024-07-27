"""
config.py
---------

Ce module contient les configurations spécifiques pour scraper leboncoin.fr,
y compris les paramètres des proxies et les headers HTTP.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # Charger les variables d'environnement depuis le fichier .env

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

PROXY = {
    'http': os.getenv('PROXY_HTTP'),
    'https': os.getenv('PROXY_HTTPS')
}

# Initialisation des configurations.
