import json
import os
import unittest

os.environ['TEST'] = "1"
# pylint: disable=wrong-import-position
from src.config import get_config
from src.db.facade import Facade
from src.db.orm_weather_report import WeatherReport
from src.server import app

CONFIG = get_config()


class ServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        this_filepath = os.path.dirname(__file__)
        weather_file = os.path.join(this_filepath, 'weather.txt')
        with open(weather_file, 'r') as fr:  # pylint: disable=invalid-name
            cls.sample_response = json.load(fr)

        cls.db = Facade()
        cls.db.insert(cls.sample_response)

    def setUp(self):
        self.test_client = app.test_client()

    def test_server_200(self):
        res = self.test_client.get('/weather/London')
        self.assertEqual(res.status_code, 200)

    def test_server_400(self):
        with self.assertRaises(ValueError):
            self.test_client.get('/weather/London?unit=broken',
                                 'Passing bad temperature unit')
        with self.assertRaises(ValueError):
            self.test_client.get('/weather/London?unit=C&stop=13-37-37',
                                 'Parsing broken date')

    def test_db(self):
        sample_record = WeatherReport.from_json(self.sample_response)
        sample_record.id = 1
        res = self.db.query(0, 2147483648, 'London')
        result_record = res[0]
        self.assertEqual(len(list(res)), 1, 'Must be exactly 1 record in db')
        self.assertEqual(sample_record.pretty(), result_record.pretty())

    @classmethod
    def tearDownClass(cls):
        os.remove(CONFIG['db_path'].split('///')[1])


if __name__ == "__main__":
    unittest.main()
