import scrapy
import json
import os
import re

class TripHotelsSpider(scrapy.Spider):
    name = 'trip_hotels'
    allowed_domains = ['uk.trip.com']
    start_urls = ['https://uk.trip.com/hotels/?locale=en-GB&curr=GBP']

    def __init__(self, *args, **kwargs):
        super(TripHotelsSpider, self).__init__(*args, **kwargs)
        self.save_dir = 'scraped_data'
        os.makedirs(self.save_dir, exist_ok=True)

    def parse(self, response):
        # Use a more robust method to extract the JSON data
        script_contents = response.xpath('//script[contains(text(), "window.IBU_HOTEL")]/text()').get()

        if script_contents:
            try:
                # Use regex to extract the JSON-like content more precisely
                json_match = re.search(r'window\.IBU_HOTEL\s*=\s*({.*?});', script_contents, re.DOTALL)

                if json_match:
                    json_str = json_match.group(1)

                    # Parse the JSON string
                    data = json.loads(json_str)

                    # Extract inbound cities
                    inbound_cities = data.get('initData', {}).get('htlsData', {}).get('inboundCities', [])

                    if inbound_cities:
                        # Generate URLs for each city based on the 'id'
                        city_urls = []
                        for city in inbound_cities:
                            city_id = city.get('id')
                            city_url = f'https://uk.trip.com/hotels/list?city={city_id}'
                            city_urls.append({
                                'city': city.get('name'),
                                'url': city_url
                            })

                        # Save the city URLs to a new JSON file
                        urls_file_path = os.path.join(self.save_dir, 'city_urls.json')
                        with open(urls_file_path, 'w', encoding='utf-8') as urls_file:
                            json.dump(city_urls, urls_file, indent=4, ensure_ascii=False)

                        self.logger.info(f'Successfully saved {len(city_urls)} city URLs to {urls_file_path}')

                    # Save the inbound cities data to a JSON file (original data)
                    json_file_path = os.path.join(self.save_dir, 'inbound_cities.json')
                    with open(json_file_path, 'w', encoding='utf-8') as json_file:
                        json.dump(inbound_cities, json_file, indent=4, ensure_ascii=False)

                    self.logger.info(f'Successfully saved {len(inbound_cities)} inbound cities to {json_file_path}')
                    
                else:
                    self.logger.error('Could not extract JSON data from the script tag')

            except json.JSONDecodeError as e:
                self.logger.error(f'JSON Decode Error: {e}')
            except Exception as e:
                self.logger.error(f'Unexpected error: {e}')
        else:
            self.logger.error('No script tag containing IBU_HOTEL data was found')

