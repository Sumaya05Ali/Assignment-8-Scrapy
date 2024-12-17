# Assignment-8-Scrapy

# Trip Scraper

A web scraping project that extracts hotel data from Trip.com and stores it in a PostgreSQL database using SQLAlchemy. The data includes property title, rating, location, latitude, longitude, room type, price, and images. This project stores the hotel images in a directory and references them in the database.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Environment Setup](#environment-setup)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [License](#license)


## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/Sumaya05Ali/Assignment-8-Scrapy.git
    cd Assignment-8-Scrapy-main
    ```

    Set Up the Virtual Environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Ensure you have **Docker** and **Docker Compose** installed on your machine. You can download Docker from [here](https://www.docker.com/get-started).

4. Build the Docker containers:

    ```bash
    docker-compose build
    ```
5. Once the build process is complete, you can bring up the containers:

    ```bash
    docker-compose up
    ```

## Usage

1. Once the containers are running, Scrapy will begin scraping data. The spider will extract information about hotels in a randomly selected city from **inboundCities** and save it into a PostgreSQL database and a local directory.

2. To check if the spider has run successfully, you can visit your database using the following command:

    ```bash
    docker exec -it hotel_scraper_db bash
    ```

    Then log into PostgreSQL:

    ```bash
    psql -U user -d trip_scraper_db
    ``` 
    
3. After logging in, check the tables and inspect the data:

    ```sql
    \dt
    SELECT * FROM hotels;
    ```
4. The scraped images are saved in a directory called `scraped_data/images/` inside the container.


## Environment Setup

Make sure to configure the environment variables in the **docker-compose.yml** file. The PostgreSQL credentials and database configuration are specified under the `environment` section:

```yaml
environment:
  - POSTGRES_USER=myuser
  - POSTGRES_PASSWORD=mypassword
  - POSTGRES_DB=hotel_db
 ```

Also, in your spider code, update the DATABASE_URL environment variable for PostgreSQL:

```yaml
environment:
  - DATABASE_URL=postgresql+psycopg2://myuser:mypassword@db:5432/hotel_db
 ```

## Project Structure

The project directory structure is as follows:

```graphql
trip-scraper/
├── scraped_data/                # Directory for storing scraped data
│   └── images/                   # Directory for storing hotel images
├── trip_scraper/
│   ├── spiders/                  # Folder containing Scrapy spider code
│   │   └── spider.py             # Main spider file for scraping hotels
│   ├── pipelines.py              # Scrapy pipelines for processing data
│   ├── settings.py               # Scrapy settings file
│   ├── models.py                 # SQLAlchemy models for PostgreSQL
│   └── init_db.py                # Initialize the database
├── docker-compose.yml            # Docker Compose configuration
├── Dockerfile                    # Dockerfile for building the project container
└── README.md                     # This file
 ```

## Dependencies

1. Scrapy - A fast web crawling and web scraping framework.
2. SQLAlchemy - A SQL toolkit and ORM for Python.
3. PostgreSQL - A powerful, open-source relational database.
4. requests - A simple HTTP library for downloading images.
5. psycopg2 - A PostgreSQL adapter for Python.
To install the dependencies, you can use Docker Compose to pull the required images and set up the services.


## License
This project is licensed under the MIT License - see the LICENSE file for details.
