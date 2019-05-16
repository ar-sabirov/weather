import os
import json
import unittest
from unittest.mock import Mock, patch
from nose.tools import assert_is_not_none
from src.process import WeatherRecord
from src.client import fetch


class WeatherClientTest(unittest.TestCase):
    def setUp(self):
        this_filepath = os.path.dirname(__file__)
        weather_file = os.path.join(this_filepath, 'weather.txt')
        with open(weather_file, 'r') as fr:
            self.sample_response = json.load(fr)

    def test_request_ok(self):
        with patch('src.client.requests.get') as mock_get:
            mock_get.return_value.ok = True
            response = fetch('')
        assert_is_not_none(response)

    @patch('src.client.requests.get')
    def test_fetch_mock(self, mock_get):
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = self.sample_response

        response = fetch('')
        self.assertEqual(response.json(), self.sample_response)
        record = WeatherRecord(response.json())
        self.assertEqual(record.pretty('C'),
                         'London, Wed 14 Dec 2016 13:50, haze, 11C')


if __name__ == "__main__":
    unittest.main()