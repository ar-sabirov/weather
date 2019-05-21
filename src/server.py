"""Flask server to expose API for collected
weather data
"""
import logging

from flask import Flask, g, jsonify, request

from src.config import get_config
from src.db.facade import Facade
from src.utils.utils import CONVERSION, parse_date, date_to_timestamp

app = Flask(__name__)  # pylint: disable=invalid-name
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
CONFIG = get_config()


def get_db():
    if 'db' not in g:
        g.db = Facade()
    return g.db


class InvalidUsage(Exception):
    """Class for custom exception handling
    """
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        error_dict = dict(self.payload or ())
        error_dict['message'] = self.message
        return error_dict


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):  # pylint: disable=missing-docstring
    return jsonify(error.to_dict()), error.status_code


@app.route('/weather/<city>', methods=['GET'])
def query_weather(city: str):
    db = get_db()  # pylint: disable=invalid-name
    start = request.args.get('start', default='1-1-0001')
    stop = request.args.get('stop', default='31-12-9999')
    unit = request.args.get('unit', 'K')

    if unit not in CONVERSION.keys():
        raise InvalidUsage('Unknown temperature unit', status_code=400)

    try:
        date_start = parse_date(start)
        date_stop = parse_date(stop)
    except ValueError:
        raise InvalidUsage('Unable to parse date', status_code=400)
    if date_start > date_stop:
        raise InvalidUsage(
            f'Start {date_start} is later than stop {date_stop}',
            status_code=400)

    ts_start = date_to_timestamp(date_start, zero_seconds=True)
    ts_stop = date_to_timestamp(date_stop, zero_seconds=False)
    q_res = db.query(ts_start, ts_stop, city)

    result = [x.pretty(unit) for x in q_res]

    return jsonify(result)


if __name__ == "__main__":
    logging.basicConfig(filename=CONFIG['server_log'], level=logging.DEBUG)
    app.run(host=CONFIG['host'], port=CONFIG['port'], debug=True)
