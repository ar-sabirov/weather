import unittest
import datetime
from src.utils.utils import date_to_timestamp, parse_date, convert_kelvin


class UtilsTest(unittest.TestCase):
    def test_date_to_interval(self):
        sample_ts = date_to_timestamp(datetime.date(2007, 7, 7),
                                      zero_seconds=True)
        self.assertEqual(sample_ts, 1183752000)
        sample_ts = date_to_timestamp(datetime.date(2007, 7, 7),
                                      zero_seconds=False)
        self.assertEqual(sample_ts, 1183838399)

    def test_parse_date(self):
        self.assertEqual(parse_date('20-12-2020'), datetime.date(2020, 12, 20))
        with self.assertRaises(ValueError):
            parse_date('1337-37-37')

    def test_convert_kelvin(self):
        self.assertEqual(convert_kelvin(290, 'C'),
                         '17C',
                         msg='Invalid conversion to Celsius scale')
        self.assertEqual(convert_kelvin(290, 'F'),
                         '62F',
                         msg='Invalid conversion to Fahrenheit scale')
        with self.assertRaises(KeyError):
            convert_kelvin(290, 'broken')


if __name__ == "__main__":
    unittest.main()