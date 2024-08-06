
# Spider House

## Overview

**Spider House** is a web scraping tool designed to extract real estate listings from platforms like Leboncoin. It automates the process of notifying users, particularly real estate agencies, about new listings that match their criteria.

## Features

- **Automated Scraping**: Extracts real estate listings with automated navigation to handle anti-bot protections.
- **Dynamic URL Management**: Generates and verifies URLs for cities based on postal codes.
- **Database Integration**: Stores listings, images, and city information in a PostgreSQL database.
- **Data Validation**: Ensures all data is validated before database insertion.

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Set up environment variables for database and proxy configurations.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Rovis91/Spider-house.git
   cd Spider-house
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**: Create a `.env` file with the following variables:

   ```plaintext
   BD_USERNAME=
   PASSWORD=
   USER_AGENT=
   COUNTRY=
   HOST=
   PORT=
   DB_NAME=
   DB_USER=
   DB_PASSWORD=
   DB_HOST=
   DB_PORT=
   ```

### Usage

As the project is under development, specific scripts and usage instructions will be provided in future updates.

## Contributing

Contributions are welcome! Please open issues or pull requests to propose changes or report problems.

## License

This project is licensed under [MIT License](LICENSE).

## Contact

For any questions, please contact me via [GitHub](https://github.com/Rovis91).

## Roadmap

- Integrate additional real estate websites.
- Develop email alert systems.
- Enhance scraping performance.
- Implement CI/CD pipeline for deployment.

---

### Note

This project is in active development. Tests and comprehensive documentation will be added in future updates.
