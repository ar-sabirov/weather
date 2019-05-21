import json
import os
import unittest
from unittest.mock import patch

os.environ['TEST'] = "1"

# pylint: disable=wrong-import-position
from src.client import fetch
from src.db.orm_weather_report import WeatherReport


class ClientTest(unittest.TestCase):
    def setUp(self):
        this_filepath = os.path.dirname(__file__)
        weather_file = os.path.join(this_filepath, 'weather.txt')
        with open(weather_file, 'r') as fr:  # pylint: disable=invalid-name
            self.sample_response = json.load(fr)

    @patch('src.client.requests.get')
    def test_fetch_mock(self, mock_requests_get):
        mock_requests_get.return_value.ok = True
        mock_requests_get.return_value.json.return_value = self.sample_response

        response = fetch('')
        self.assertEqual(response.json(), self.sample_response)
        record = WeatherReport.from_json(response.json())
        self.assertEqual(record.pretty('C'),
                         'London, Wed 14 Dec 2016 13:50, haze, 11C')


if __name__ == "__main__":
    unittest.main()
