"""ORM for weather report data with sqlalchemy
"""
import logging
from datetime import datetime

from sqlalchemy import Column, Integer, Sequence, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

from src.config import get_config
from src.utils.utils import convert_kelvin

CONFIG = get_config()

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
        # pylint: disable=invalid-name
        dt = datetime.fromtimestamp(self.timestamp)
        date = dt.strftime("%a %d %b %Y %H:%M")
        target_temp = convert_kelvin(self.temp, scale)
        return f"{self.city}, {date}, {self.weather}, {target_temp}"

    def __repr__(self):
        return (f"""WeatherReport(id={self.id}, city={self.city},"""
                f"""weather={self.weather}, temp={self.temp},"""
                f"""ts={self.timestamp})""")


ENGINE = create_engine(CONFIG['db_path'], echo=True)
Base.metadata.create_all(ENGINE)
