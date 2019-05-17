import logging
import sqlite3
from sqlite3 import Error
from typing import List

from src.db.base import BaseDataLayer
from src.process import WeatherRecord

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


#TODO универсальный класс для БД (фасад), который решает какую БД использовать
class Sqlite3_connection():
    def __init__(self, path):
        self.path = path
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        logger.debug('Connected to sqlite db')
        return self.conn

    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()


def create_table(conn: sqlite3.Connection,
                 create_table_statement: str) -> None:
    """create a table from the create_table_statement statement

    Parameters
    ----------
    conn : sqlite3.Connection
        Connection object
    create_table_statement : str
        a CREATE TABLE statement
    """
    try:
        cur = conn.cursor()
        cur.execute(create_table_statement)
        logger.debug('Create table if not exist')
    except Error as e:
        logger.exception(e)


class SqliteDB(BaseDataLayer):
    _create_weather_table = """
    CREATE TABLE IF NOT EXISTS reports (
    id integer PRIMARY KEY,
    city text NOT NULL,
    weather text NOT NULL,
    temp integer NOT NULL,
    ts integer NOT NULL
    );
    """

    _insert_statement = """
    INSERT INTO reports(city,weather,temp,ts)
    VALUES(?,?,?,?)
    """

    _select_range_statement = """
    SELECT
    *
    FROM reports
    WHERE (ts BETWEEN ? AND ?) AND (city = ?)
    """

    #TODO Write ahead log or wtf with read-write simultaneously
    def __init__(self, path: str):
        self.path = path
        with Sqlite3_connection(path) as conn:
            create_table(conn, SqliteDB._create_weather_table)

    def put(self, record: WeatherRecord) -> bool:
        values = record.city, record.weather, record.temp, record.ts
        logger.debug(values)
        with Sqlite3_connection(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(SqliteDB._insert_statement, values)
        logger.debug('Written record db')

    def query(self, ts_from: int, ts_to: int,
              city: str) -> List[WeatherRecord]:
        with Sqlite3_connection(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(SqliteDB._select_range_statement,
                           (ts_from, ts_to, city))
            result = [
                WeatherRecord(city=x[1], weather=x[2], temp=x[3], ts=x[4])
                for x in cursor.fetchall()
            ]
            return result
