"""Facade class to deal with arbitrary database(s)
"""
import json
import os

from src.db.sql_db import SqlDB

CONFIG = os.environ['WTHR_CONFIG']
with open(CONFIG, mode='r') as fr:  # pylint: disable=invalid-name
    cfg = json.load(fr)
    DB_PATH = cfg['db_path']


class Facade():
    def __init__(self):
        self.sql_db = SqlDB(DB_PATH)

    def insert(self, json_dict: dict):
        self.sql_db.insert(json_dict)

    def query(self, ts_from: int, ts_to: int, city: str):
        return self.sql_db.query(ts_from, ts_to, city)
