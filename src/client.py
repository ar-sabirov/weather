import requests
import logging

import asyncio

api_url_base = 'http://api.openweathermap.org/data/2.5/weather?q=London,uk&appid=332aff71953e43412a946ab10190bc7a'

logger = logging.getLogger('asyncio')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('log.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
logger.addHandler(fh)
logger.addHandler(ch)


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
            return response
        logger.debug('Waiting')
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
    loop = asyncio.get_event_loop()
    #loop.run_until_complete(fetch_async(api_url_base))
    loop.run_until_complete(asyncio.wait([run(), run2()]))
    loop.close()