"""Module for configuration handling
"""
import json
import os


def get_config() -> dict:
    """Loads and returns config if WTHR_CONFIG is present in os.environ
    or returns default config otherwise

    Returns
    -------
    dict
        App configuration file
    """

    default_config = {
        "db_path": "sqlite:///prod.db",
        "api_url_base": "http://api.openweathermap.org/data/2.5/weather",
        "query_args": {
            "appid": "332aff71953e43412a946ab10190bc7a",
            "q": "London,uk"
        },
        "fetch_interval_s": 5,
        "retry_interval_s": 3,
        "host": "localhost",
        "port": "5050",
        "server_log": "server.log",
        "client_log": "client.log"
    }

    test_config = {
        "db_path": "sqlite:////home/arthur/test.db",
        "api_url_base": "http://api.openweathermap.org/data/2.5/weather",
        "query_args": {
            "appid": "332aff71953e43412a946ab10190bc7a",
            "q": "London,uk"
        },
        "fetch_interval_s": 5,
        "retry_interval_s": 3,
        "host": "localhost",
        "port": "5055",
        "server_log": "test_server.log",
        "client_log": "test_client.log"
    }
    if os.environ.get('TEST'):
        return test_config
    if os.environ.get('CONFIG_PATH'):
        with open(os.environ['CONFIG_PATH'], mode='r') as fr:  # pylint: disable=invalid-name
            return json.load(fr)
    else:
        return default_config
