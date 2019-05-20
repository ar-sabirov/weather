import os
import unittest
import json
from unittest.mock import patch

from src.db.orm_weather_report import WeatherReport
from src.client import fetch


class WeatherClientTest(unittest.TestCase):
    default_config = {
        "db_path": "sqlite:////home/arthur/test.db",
        "api_url_base": "http://api.openweathermap.org/data/2.5/weather",
        "query_args": {
            "appid": "332aff71953e43412a946ab10190bc7a",
            "q": "London,uk"
        }
    }

    def setUp(self):
        this_filepath = os.path.dirname(__file__)
        weather_file = os.path.join(this_filepath, 'weather.txt')
        with open(weather_file, 'r') as fr:
            self.sample_response = json.load(fr)

    # TODO Mock get config for test db
    @patch('src.config.get_config')
    @patch('src.client.requests.get')
    def test_fetch_mock(self, mock_requests_get, mock_get_config):
        mock_get_config.return_value = WeatherClientTest.default_config
        mock_requests_get.return_value.ok = True
        mock_requests_get.return_value.json.return_value = self.sample_response

        response = fetch('')
        self.assertEqual(response.json(), self.sample_response)
        record = WeatherReport.from_json(response.json())
        self.assertEqual(record.pretty('C'),
                         'London, Wed 14 Dec 2016 13:50, haze, 11C')


if __name__ == "__main__":
    unittest.main()
