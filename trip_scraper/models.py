from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

# Hotel model
class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    rating = Column(String)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    price = Column(Float)
    room_type = Column(String)

    city_id = Column(Integer, ForeignKey('cities.id'))
    city = relationship('City', back_populates='hotels')
    images = relationship('Image', back_populates='hotel')

# City model
class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    hotels = relationship('Hotel', back_populates='city')

# Image model
class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    file_path = Column(String)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    hotel = relationship('Hotel', back_populates='images')

def init_db():
    # Initialize the database connection
    DATABASE_URL = "postgresql://user:password@db:5432/trip_scraper_db"
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    return Session()
