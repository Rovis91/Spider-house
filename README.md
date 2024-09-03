
# Real Estate Scraper

## Overview

This project is designed to scrape real estate listings from multiple websites, including Leboncoin and others. The scraped data is processed and stored in a PostgreSQL database. The system uses Celery for task management, enabling scalable and parallel scraping across multiple websites and cities.

## Features

- **Scalable Scraping:** Uses Celery with Redis to manage and distribute scraping tasks across multiple workers.
- **Modular Scraper Design:** Each website scraper inherits from a common base class, making it easy to add support for new websites.
- **Robust Error Handling:** Implements retry logic, error logging, and pagination handling.
- **Proxy Support:** Retrieves HTML content through proxies to avoid blocking by websites.
- **Database Integration:** Stores scraped listings in a PostgreSQL database, ensuring data integrity and consistency.

## Requirements

Ensure you have the following dependencies installed:

```plaintext
beautifulsoup4==4.12.2
requests==2.31.0
sqlalchemy==2.0.20
psycopg2==2.9.6
celery==5.2.7
redis==4.5.4
python-dotenv==1.0.0
```

You can install all dependencies using:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Scraper

1. **Start Redis**: Ensure Redis is running on your system.

2. **Start Celery Worker**: Run the Celery worker with the following command:

   ```bash
   celery -A celery worker --loglevel=info
   ```

3. **Run the Orchestration Script**: Kick off the scraping tasks by running:

   ```bash
   python orchestration.py
   ```

This script will enqueue tasks for scraping various websites and cities. The Celery workers will pick up these tasks and process them concurrently.

### Adding New Websites

To add support for a new website:

1. Create a new scraper class that inherits from `BaseScraper` in `scraper_base.py`.
2. Implement the `extract_ads`, `transform_ad`, and `html_to_json` methods according to the website's structure.
3. Define a new Celery task in `tasks.py` for the new scraper.
4. Add the task to the orchestration script.

## Monitoring

You can monitor your Celery tasks using Flower:

```bash
celery -A celery flower
```

This will give you a web-based dashboard to track task progress, status, and more.

## License

This project is licensed under the MIT License.
