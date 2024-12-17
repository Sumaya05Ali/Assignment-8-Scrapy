import scrapy
import json
import os
import re
import requests
from sqlalchemy.orm import sessionmaker
from models import Hotel, City, Image, init_db

class TripHotelsSpider(scrapy.Spider):
    name = 'trip_hotels'
    allowed_domains = ['uk.trip.com']
    start_urls = [
        'https://uk.trip.com/hotels/list?city=733',
        'https://uk.trip.com/hotels/list?city=270226',
        'https://uk.trip.com/hotels/list?city=6570'
    ]

    def __init__(self, *args, **kwargs):
        super(TripHotelsSpider, self).__init__(*args, **kwargs)
        self.save_dir = 'scraped_data'
        os.makedirs(self.save_dir, exist_ok=True)
        self.Session = sessionmaker(bind=init_db())  # Initialize DB session

    def parse(self, response):
        # Extract the city ID from the URL
        city_id = re.search(r'city=(\d+)', response.url).group(1)
        city_image_dir = os.path.join(self.save_dir, f'city_{city_id}/images')
        os.makedirs(city_image_dir, exist_ok=True)  # Ensure directory for city images

        # Extract the script containing the hotel data
        script_contents = response.xpath('//script[contains(text(), "window.IBU_HOTEL")]/text()').get()
        if script_contents:
            try:
                json_match = re.search(r'window\.IBU_HOTEL\s*=\s*({.*?});', script_contents, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                    data = json.loads(json_str)

                    # Extract hotel list data
                    hotel_list = data.get('initData', {}).get('firstPageList', {}).get('hotelList', [])
                    session = self.Session()

                    if hotel_list:
                        for hotel in hotel_list:
                            hotel_info = hotel.get('hotelBasicInfo', {})
                            hotel_name = hotel_info.get('hotelName', 'N/A')

                            # Extract rating
                            comment_info = hotel.get('commentInfo', {})
                            rating = comment_info.get('commentScore', 'No Rating')

                            # Extract latitude and longitude
                            position_info = hotel.get('positionInfo', {})
                            coordinates = position_info.get('mapCoordinate', [])
                            latitude = 'No Latitude Info'
                            longitude = 'No Longitude Info'
                            if coordinates:
                                for coord in coordinates:
                                    if coord.get('coordinateType') == 1:
                                        latitude = coord.get('latitude', 'No Latitude Info')
                                        longitude = coord.get('longitude', 'No Longitude Info')
                                        break

                            # Extract price
                            price = hotel_info.get('price', 'N/A')

                            # Extract room type
                            room_info = hotel.get('roomInfo', {})
                            room_type = room_info.get('physicalRoomName', 'Not Available')

                            # Extract images and download
                            images = hotel_info.get('hotelImgRoundLoad', [])
                            downloaded_images = []
                            for img in images:
                                img_url = img.get('url')
                                if img_url:
                                    image_name = img_url.split('/')[-1]
                                    image_path = os.path.join(city_image_dir, image_name)
                                    with open(image_path, 'wb') as img_file:
                                        img_file.write(requests.get(img_url).content)
                                    downloaded_images.append(image_name)

                            # Save hotel data to the database
                            city = session.query(City).filter_by(city_id=city_id).first()
                            if not city:
                                city = City(city_id=city_id, city_name=position_info.get('cityName', 'Unknown'))
                                session.add(city)
                                session.commit()

                            hotel_db = Hotel(
                                hotel_name=hotel_name,
                                city_id=city.city_id,
                                rating=rating,
                                latitude=latitude,
                                longitude=longitude,
                                price=price,
                                room_type=room_type
                            )
                            session.add(hotel_db)
                            session.commit()

                            # Save images to database
                            for image_name in downloaded_images:
                                image_db = Image(hotel_id=hotel_db.hotel_id, image_path=image_name)
                                session.add(image_db)

                            session.commit()
                    session.close()

            except Exception as e:
                self.logger.error(f'Unexpected error: {e}')
