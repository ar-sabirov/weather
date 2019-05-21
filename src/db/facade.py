"""Facade class to deal with arbitrary database(s)
"""

from src.config import get_config
from src.db.sql_db import SqlDB

CONFIG = get_config()


class Facade():
    def __init__(self):
        self.sql_db = SqlDB(CONFIG['db_path'])

    def insert(self, json_dict: dict):
        self.sql_db.insert(json_dict)

    def query(self, ts_from: int, ts_to: int, city: str):
        return self.sql_db.query(ts_from, ts_to, city)
