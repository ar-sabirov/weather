"""
"""
import logging
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.orm_weather_report import WeatherReport

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class SqlDB():

    #TODO Write ahead log or wtf with read-write simultaneously
    #TODO add path
    def __init__(self, path: str):
        self.engine = create_engine(path, echo=True)
        self.Session = sessionmaker(bind=self.engine)  # pylint: disable=invalid-name
        self.Session.configure(bind=self.engine)

    def insert(self, json_dict: dict) -> bool:
        record = WeatherReport.from_json(json_dict)
        logger.debug(f'Inserting {record}')
        session = self.Session()
        session.add_all([record])
        session.commit()

    def query(self, ts_from: int, ts_to: int,
              city: str) -> List[WeatherReport]:
        logger.debug(f'Querying from: {ts_from} to: {ts_to} at: {city}')
        session = self.Session()

        result = session.query(WeatherReport).filter(
            WeatherReport.ts.between(ts_from,
                                     ts_to)).filter(WeatherReport.city == city)
        return result
