"""Client app to fetch weather reports
"""
import argparse
import asyncio
import logging

import requests
from requests.models import PreparedRequest

from src.config import get_config
from src.db.facade import Facade

logger = logging.getLogger('asyncio')  # pylint: disable=invalid-name
CONFIG = get_config()


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
        logger.exception(f'Fetch failed with {response.json()}')
        return None


async def fetch_retry(url: str, interval=5):
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
        logger.debug('Fetch, waiting 200 response')
        await asyncio.sleep(interval)


async def run(url: str, fetch_interval, retry_interval):  # pylint: disable=missing-docstring
    """Fetch every CONFIG['fetch_interval_s'] seconds
    """
    while True:
        await fetch_retry(url, retry_interval)
        await asyncio.sleep(fetch_interval)


def main():
    parser = argparse.ArgumentParser(description='APS dataset')

    parser.add_argument('-q',
                        '--query',
                        help='City to query weather',
                        type=str,
                        default='London,uk')
    args = parser.parse_args()
    if args.query:
        CONFIG['query_args']['q'] = args.query
    logging.basicConfig(filename=CONFIG['client_log'], level=logging.DEBUG)

    req = PreparedRequest()
    req.prepare_url(CONFIG['api_url_base'], CONFIG['query_args'])
    logger.info(f'Request URL: {req.url}')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.wait([
            run(req.url, CONFIG['fetch_interval_s'],
                CONFIG['retry_interval_s'])
        ]))
    loop.close()


if __name__ == "__main__":
    main()
