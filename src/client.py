"""Client app to fetch weather reports
"""
import asyncio
import json
import logging
import os

import requests
from requests.models import PreparedRequest

from src.db.facade import Facade

CONFIG = os.environ['WTHR_CONFIG']
with open(CONFIG, mode='r') as fr:  # pylint: disable=invalid-name
    CONFIG = json.load(fr)  # pylint: disable=invalid-name

logger = logging.getLogger('asyncio')  # pylint: disable=invalid-name


def fetch(url: str) -> requests.models.Response:
    """Synchronous data fetch using requests module.
    (for mock tests)

    Parameters
    ----------
    url : str
        Resource url

    Returns
    -------
    requests.models.Response
        Resulting response (can be None)
    """
    response = requests.get(url)
    if response.ok:
        logger.debug("Fetched %s", response.json())
        return response
    else:
        logger.debug('Fetch failed')
        return None


async def fetch_retry(url: str, interval: int = 5):
    """Asynchronous data fetch. If response is None,
    retries after <interval> seconds until successful
    fetch

    Parameters
    ----------
    url : str
        Resourse url
    interval : int, optional
        Retry after, by default 5
    """
    pending = True
    while pending:
        response = fetch(url)
        if response:
            pending = False
            json_dict = response.json()
            Facade().insert(json_dict)
            return
        logger.debug('Waiting 200 response')
        await asyncio.sleep(interval)


async def run(url: str):  # pylint: disable=missing-docstring
    while True:
        await fetch_retry(url, interval=3)
        await asyncio.sleep(5)


if __name__ == "__main__":
    # pylint: disable=invalid-name
    logging.basicConfig(filename='client.log', level=logging.DEBUG)

    req = PreparedRequest()
    req.prepare_url(CONFIG['api_url_base'], CONFIG['query_args'])

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([run(req.url)]))
    loop.close()
