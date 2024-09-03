# tasks.py

from celery import Celery
from scraper_base import LeboncoinScraper, PAPScraper  # Assuming these are the scrapers you've implemented

app = Celery('real_estate_scraper')

@app.task
def scrape_leboncoin(insee_code: str):
    scraper = LeboncoinScraper(base_url='https://www.leboncoin.fr/ventes_immobilieres/')
    return scraper.scrape_listings(insee_code)

@app.task
def scrape_pap(insee_code: str):
    scraper = PAPScraper(base_url='https://www.pap.fr/annonces/immobilier')
    return scraper.scrape_listings(insee_code)

# Add more tasks for other websites as needed
