# Assignment-8-Scrapy

# Trip Scraper

A web scraping project that extracts hotel data from Trip.com and stores it in a PostgreSQL database using SQLAlchemy. The data includes property title, rating, location, latitude, longitude, room type, price, and images. This project stores the hotel images in a directory and references them in the database.

## Features
- Scrapes hotel information from multiple cities on Trip.com.
- Stores scraped data in a PostgreSQL database.
- Automatically creates tables and stores image paths in the database.
- Images are downloaded and stored locally.
- Supports scraping multiple cities, including:
  - City 733 (Dhaka)
  - City 270226
  - City 6570

## Requirements

- Docker
- PostgreSQL
- Python 3.12+
- Scrapy
- SQLAlchemy
- Requests

## Setup Instructions

### 1. Clone the repository

Clone the project repository to your local machine:

```bash
git clone https://github.com/Sumaya05Ali/Assignment-8-Scrapy.git
cd Assignment-8-Scrapy-main
```
2. Install dependencies
a) Install Python dependencies:
First, set up a virtual environment and install the required dependencies.

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
b) Install Docker (if not already installed):
Ensure Docker is installed and running on your machine. Follow the installation guide for your operating system.

c) Set up Docker Compose:
Create a docker-compose.yml file in the root directory of the project (if not already provided). It should define services for PostgreSQL and the Scrapy spider.

yaml
Copy code
version: "3.8"

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: trip_scraper_db
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data

  scraper:
    build: .
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/trip_scraper_db
    command: scrapy crawl trip_hotels

volumes:
  db_data:
3. Configure Database
Ensure PostgreSQL is running through Docker. Use docker-compose to start both the PostgreSQL and Scrapy services.

bash
Copy code
docker-compose up --build
4. Run Scrapy Spider
After starting the services, run the Scrapy spider to scrape hotel data:

bash
Copy code
docker-compose up
This will start the spider and store the scraped hotel information in the PostgreSQL database, along with downloading images to a directory named scraped_data.

5. Database Tables
The following tables will be created automatically:

cities: Stores city data (city ID and city name).
hotels: Stores hotel information (name, rating, location, latitude, longitude, price, room type, and city ID).
images: Stores images related to hotels (image path and hotel ID).
6. View Data in Database
To view the data in the PostgreSQL database, use the following command:


docker exec -it trip_scraper-db-1 psql -U postgres -d trip_scraper_db
Once inside the PostgreSQL CLI, you can query the tables to view the scraped data:


SELECT * FROM hotels;
SELECT * FROM cities;
SELECT * FROM images;
7. Code Coverage
Ensure you have at least 60% code coverage for your project. You can use pytest and coverage to measure the code coverage.

bash

pip install pytest coverage
pytest --cov=trip_scraper
This will show the code coverage of your project.

Project Structure
The project structure should look like this:


trip_scraper/
│
├── trip_scraper/                  # Main project directory
│   ├── spiders/                    # Contains the Scrapy spiders
│   │   └── trip_hotels.py          # The main Scrapy spider for scraping hotels
│   ├── models.py                   # SQLAlchemy models for the database
│   ├── requirements.txt            # Python dependencies
│   ├── docker-compose.yml          # Docker Compose configuration
│   └── README.md                   # Project documentation (this file)
│
├── scraped_data/                   # Folder where images and JSON data are stored
│   ├── city_733/                   # Directory for Dhaka (City 733)
│   │   ├── hotels_city_733.json    # Scraped hotel data for Dhaka
│   │   └── images/                 # Folder for city images
│   ├── city_270226/                # Directory for City 270226
│   │   ├── hotels_city_270226.json # Scraped hotel data for City 270226
│   │   └── images/                 # Folder for city images
│   └── city_6570/                  # Directory for City 6570
│       ├── hotels_city_6570.json   # Scraped hotel data for City 6570
│       └── images/                 # Folder for city images
│
└── docker-compose.yml              # Docker Compose file
Troubleshooting
If you encounter any issues, check the following:

Ensure the DATABASE_URL is correct in the docker-compose.yml file.
Check the PostgreSQL logs using docker logs trip_scraper-db-1 if the database isn't starting.
If the spider is failing, check the Scrapy logs for specific error messages.
License
This project is licensed under the MIT License - see the LICENSE file for details.



### Key Notes:
1. Replace `https://github.com/yourusername/trip_scraper.git` with your actual GitHub repository link.
2. Make sure you have included all necessary dependencies in the `requirements.txt` file.
3. The `docker-compose.yml` is configured to run both PostgreSQL and Scrapy, ensure that your Scrapy spider is working properly.
4. The `pytest` setup and code coverage is a suggestion to achieve the 60% coverage requirement.

Let me know if you need further assistance!






