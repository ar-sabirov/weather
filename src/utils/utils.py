"""Utility module for dealing with weather unit
conversions
"""
import datetime
import time

CONVERSION = {
    'K': lambda x: x,
    'C': lambda x: x - 273.15,
    'F': lambda x: x * 9 / 5 - 459.67
}


def convert_kelvin(temp: float, target: str) -> str:
    """Convert Kelvin temperature to other scale

    Parameters
    ----------
    temp : float
        Kelvin temperature
    target : str, optional
        Target scale name ("C" - Celsius, "F" - Fahrenheit)

    Returns
    -------
    str
        Converted temperature with scale suffix (C/F)
    """
    t_conv = CONVERSION[target](temp)
    return str(round(t_conv)) + target


def parse_date(date_string: str) -> datetime.date:
    """Parse date string ('%d-%m-%Y' -> '02-03-2020')
    convert to datetime.date

    Parameters
    ----------
    date_string : str
        Date string '%d-%m-%Y' (e.g '02-03-2020')

    Returns
    -------
    datetime.date
        datetime.date object
    """
    return datetime.datetime.strptime(date_string, "%d-%m-%Y").date()


def date_to_timestamp(date: datetime.date, zero_seconds: bool) -> int:
    """Convert datetime.date date to integer timestamp
    either at 00:00:00 or 23:59:59 hours

    Parameters
    ----------
    date : datetime.date
        [description]
    zero_seconds : bool
        If true, returns timestamp at 00:00:00 of date,
        else: 23:59:59

    Returns
    -------
    int
        Integer timestamp
    """
    combiner = datetime.time.min if zero_seconds else datetime.time.max
    date_combined = datetime.datetime.combine(date, combiner)
    timestamp = int(time.mktime(date_combined.timetuple()))
    return timestamp
