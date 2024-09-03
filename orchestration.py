# orchestration.py

import logging
from celery import group
from tasks import scrape_leboncoin, scrape_pap
from storage import get_cities_by_conditions  # Assuming this function gets cities with URLs

# Set up logging
logging.basicConfig(level=logging.INFO)

def orchestrate_scraping():
    logging.info("Starting the scraping orchestration...")

    # Fetch all cities to scrape (you may add conditions to filter specific cities)
    cities = get_cities_by_conditions(is_active=True)
    
    # List to keep track of all the tasks
    tasks = []

    for city in cities:
        insee_code = city.insee_code
        
        # Create task groups for each website scraper
        leboncoin_task = scrape_leboncoin.s(insee_code)
        pap_task = scrape_pap.s(insee_code)
        
        # Add tasks to the list
        tasks.extend([leboncoin_task, pap_task])

    # Group tasks to run them concurrently
    job = group(tasks)
    result = job.apply_async()
    
    logging.info("All tasks have been queued.")
    
    # Optionally, you can wait for the results if you want synchronous execution
    result.get()

    logging.info("Scraping orchestration completed.")

if __name__ == '__main__':
    orchestrate_scraping()
