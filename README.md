# Real Estate Listings Scraping Project on Leboncoin.fr

## Context and Objectives

This project aims to develop a scraping module to retrieve real estate listings from the site leboncoin.fr. The goal is to check daily if new listings have been posted in specific cities and to maintain a history of listings for future comparisons. Eventually, this module could be extended to scrape other sites.

### Main Features

1. **Listings Scraping:**
   - Retrieve real estate listings from a given URL.
   - Extract key information: Title, Publication Date, Price, Link.

2. **Listings Comparison:**
   - Compare new listings with the history to detect new listings or price changes.

3. **Data Storage:**
   - Store listings in JSON format, one file per city (based on postal code).

4. **Proxies and Captchas Management:**
   - Integrate the Web Unlocker service from brightdata.fr to manage proxies and captchas.

### Frequency and Execution

- The script will run daily to check for new listings.
- Initially, tests will be conducted locally on Windows, with a planned migration to a Linux VM for execution.

### Project Structure

1. **Scraping Modules:**
   - **scraper.py:** Contains functions to retrieve listings from a given URL.
   - **parsing.py:** Contains functions to extract relevant data from HTML pages.

2. **Data Management Modules:**
   - **storage.py:** Manages the storage and retrieval of JSON data.
   - **comparison.py:** Manages the comparison between new listings and the history.

3. **Configuration and Utility Modules:**
   - **config.py:** Contains global configurations, including proxy settings.
   - **utils.py:** Contains utility functions for various tasks (e.g., date handling).

4. **Notification Modules (to be implemented later):**
   - **notification.py:** Will send notifications in case of new listings or price changes.

### Technical Details

1. **Scraping:**
   - Use BeautifulSoup and Selectolax libraries for HTML parsing.
   - Use Playwright to automate navigation and bypass anti-bot protections.
   - Configure HTTP headers to simulate human navigation.

2. **Data Storage:**
   - Store listings in JSON format, one file per city. Example structure:

     ```json
     {
         "listings": [
             {
                 "title": "Appartement T3",
                 "publication_date": "2024-07-26",
                 "price": "250000",
                 "link": "https://www.leboncoin.fr/ventes_immobilieres/1234567890"
             }
         ]
     }
     ```

3. **Proxies Management:**
   - Integrate the Web Unlocker service from brightdata.fr to manage proxies and captchas.
   - Configure proxies directly in HTTP requests.

4. **Listings Comparison:**
   - Compare based on the title and link of the listing to identify new listings.
   - Update the listings JSON file, adding new listings or updating prices.

### Directory and File Structure

'''
project_root/
│
├── leboncoin/
│   ├── **init**.py
│   ├── scraper.py
│   ├── parsing.py
│   ├── config.py
│   └── utils.py
│
├── storage.py
├── comparison.py
└── notification.py
'''

## Conclusion

By structuring the project in this way, we separate elements specific to leboncoin.fr from general elements, allowing for better modularity and ease of extension to other sites in the future. The code is organized to be clear, maintainable, and scalable.
