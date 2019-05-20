"""Flask server to expose API for collected
weather data
"""
import datetime
import logging
import time

from flask import Flask, g, jsonify, request

from src.db.facade import Facade

app = Flask(__name__)  # pylint: disable=invalid-name
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def get_db():
    if 'db' not in g:
        g.db = Facade()
    return g.db


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


def date_to_interval(date: datetime.date, zero_seconds: bool) -> int:
    """Convert datetime.date date to integer timestamp
    either at 00:00:00 or 24:59:59 hours

    Parameters
    ----------
    date : datetime.date
        [description]
    zero_seconds : bool
        If true, returns timestamp at 00:00:00 of date,
        else: 24:59:59

    Returns
    -------
    int
        Integer timestamp
    """
    combiner = datetime.time.min if zero_seconds else datetime.time.max
    date_combined = datetime.datetime.combine(date, combiner)
    timestamp = int(time.mktime(date_combined.timetuple()))
    return timestamp


#TODO test sql injections
#TODO test inputs for 500 error


@app.route('/weather/<city>', methods=['GET'])
def query_weather(city: str):
    db = get_db()  # pylint: disable=invalid-name
    start = request.args.get('start', default='1-1-0001')
    stop = request.args.get('stop', default='31-12-9999')

    try:
        date_start = parse_date(start)
        date_stop = parse_date(stop)
    except ValueError as e:  # pylint: disable=invalid-name
        #TODO return code 400 bad request + why
        #TODO do not throw internal error for client
        return str(e)
    if date_start > date_stop:
        #TODO return code 400 bad request + why
        return f'Start {date_start} is later than stop {date_stop}'

    ts_start = date_to_interval(date_start, zero_seconds=True)
    ts_stop = date_to_interval(date_stop, zero_seconds=False)
    q_res = db.query(ts_start, ts_stop, city)
    unit = request.args.get('unit', 'K')

    try:
        result = [x.pretty(unit) for x in q_res]
    except KeyError:
        return f'Unknown unit {unit}'

    return jsonify(result)


if __name__ == "__main__":
    logging.basicConfig(filename='server.log', level=logging.DEBUG)
    app.run(host='localhost', port='5050', debug=True)
