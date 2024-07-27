"""
scraper.py
----------

Ce module contient les fonctions nécessaires pour récupérer les annonces immobilières 
depuis un lien donné sur le site leboncoin.fr. Il utilise Playwright pour automatiser 
la navigation et contourner les protections anti-bot.
"""

from playwright.sync_api import sync_playwright
import leboncoin.parsing as parsing
import leboncoin.config as config
import json

# Initialisation et importations des bibliothèques nécessaires.
