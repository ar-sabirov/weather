import sqlite3
from sqlite3 import Error
from typing import List, Tuple

from src.db.base import BaseDataLayer
from src.process import WeatherRecord


class sqlite3_connection():
    def __init__(self, path):
        self.path = path
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        print('CONNECTED!')
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
        c = conn.cursor()
        c.execute(create_table_statement)
        print('CREATED TABLE')
    except Error as e:
        print(e)


class SqliteDB(BaseDataLayer):
    _weather_table = """
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

    _select_statement = """
    SELECT
    *
    FROM reports
    WHERE ts BETWEEN ? AND ?
    """

    def __init__(self, path: str):
        self.path = path
        with sqlite3_connection(path) as conn:
            create_table(conn, SqliteDB._weather_table)

    def put(self, record: WeatherRecord) -> bool:
        values = record.city, record.weather, record.temp, record.ts
        print(values)
        with sqlite3_connection(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(SqliteDB._insert_statement, values)
        print('Written in db')

    def query(self, interval: Tuple[int, int]) -> List[WeatherRecord]:
        with sqlite3_connection(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(SqliteDB._select_statement, interval)
            result = [
                WeatherRecord(city=x[1], weather=x[2], temp=x[3], ts=x[4])
                for x in cursor.fetchall()
            ]
            return result


sample = {
    'coord': {
        'lon': -0.13,
        'lat': 51.51
    },
    'weather': [{
        'id': 721,
        'main': 'Haze',
        'description': 'haze',
        'icon': '50d'
    }],
    'base': 'stations',
    'main': {
        'temp': 284.07,
        'pressure': 1020,
        'humidity': 87,
        'temp_min': 283.15,
        'temp_max': 285.15
    },
    'visibility': 10000,
    'wind': {
        'speed': 3.6,
        'deg': 100
    },
    'clouds': {
        'all': 0
    },
    'dt': 1481712600,
    'sys': {
        'type': 1,
        'id': 5091,
        'message': 0.0081,
        'country': 'GB',
        'sunrise': 1481702376,
        'sunset': 1481730692
    },
    'id': 2643743,
    'name': 'London',
    'cod': 200
}

if __name__ == "__main__":
    db = SqliteDB('/home/arthur/test.db')
    sample_record = WeatherRecord.from_json(sample)
    db.put(sample_record)
    res = db.query((1481712300, 1481712700))
    print([x.pretty('C') for x in res])
