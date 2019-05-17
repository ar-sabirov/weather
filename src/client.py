import asyncio
import logging

import requests

from src.db.sqlite_db import SqliteDB
from src.process import WeatherRecord

#TODO move to global config
api_url_base = 'http://api.openweathermap.org/data/2.5/weather?q=London,uk&appid=332aff71953e43412a946ab10190bc7a'
database = '/home/arthur/test.db'

logger = logging.getLogger('asyncio')


def fetch(url: str):
    response = requests.get(url)
    if response.ok:
        logger.debug("Fetched %s", response.json())
        return response
    else:
        logger.debug('Fetch failed')
        return None


async def fetch_retry(url: str, interval: int = 5):
    pending = True
    while pending:
        response = fetch(url)
        if response:
            pending = False
            wr = WeatherRecord.from_json(response.json())
            SqliteDB(database).put(wr)
        logger.debug('Waiting 200 response')
        await asyncio.sleep(interval)


async def run():
    while True:
        await fetch_retry(api_url_base, interval=3)
        await asyncio.sleep(10)


async def run2():
    while True:
        logger.debug('Running along')
        await asyncio.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(filename='client.log', level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([run(), run2()]))
    loop.close()
