"""ORM for weather report data with sqlalchemy
"""
import json
import logging
import os
from datetime import datetime

from sqlalchemy import Column, Integer, Sequence, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

from utils.conversions import convert_kelvin

CONFIG = os.environ['WTHR_CONFIG']
with open(CONFIG, mode='r') as fr:  # pylint: disable=invalid-name
    DB_PATH = json.load(fr)['db_path']

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

Base = declarative_base()  # pylint: disable=invalid-name


class WeatherReport(Base):
    """Declarative ORM description
    """
    __tablename__ = 'reports'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    temp = Column(Integer, nullable=False)
    timestamp = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    weather = Column(String, nullable=False)

    def __init__(self, temp: int, timestamp: int, city: str, weather: str):
        self.temp = temp
        self.timestamp = timestamp
        self.city = city
        self.weather = weather

    @classmethod
    def from_json(cls, json_data: dict) -> 'WeatherRecord':
        """Create an instance of WeatherRecord with
        json data

        Returns
        -------
        src.db.orm_weather_report.WeatherReport
            New instance
        """
        city = json_data['name']
        weather = json_data['weather'][0]['description']
        temp = json_data['main']['temp']
        ts = json_data['dt']  # pylint: disable=invalid-name
        return WeatherReport(city=city,
                             weather=weather,
                             temp=temp,
                             timestamp=ts)

    def pretty(self, scale: str = 'K') -> str:
        """Converts weather record to target scale and formats it to
        'London, Wed 14 Dec 2016 10:37, cloudy, 9C'

        Parameters
        ----------
        scale : str
            Scale used to calculate and print temperature

        Returns
        -------
        str
            Pretty formatted string
        """
        dt = datetime.fromtimestamp(self.timestamp)  # pylint: disable=invalid-name
        date = dt.strftime("%a %d %b %Y %H:%M")
        target_temp = convert_kelvin(self.temp, scale)
        return f"{self.city}, {date}, {self.weather}, {target_temp}"

    def __repr__(self):
        return (f"""WeatherReport(id={self.id}, city={self.city},"""
                f"""weather={self.weather}, temp={self.temp},"""
                f"""ts={self.timestamp})""")


ENGINE = create_engine(DB_PATH, echo=True)
Base.metadata.create_all(ENGINE)
