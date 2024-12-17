FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Scrapy project
COPY . .

CMD ["scrapy", "crawl", "trip_hotels"]
