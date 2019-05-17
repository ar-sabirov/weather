import time
import datetime
from flask import Flask, request, jsonify, current_app, g
from src.db.sqlite_db import SqliteDB

app = Flask(__name__)
app.config['DATABASE'] = '/home/arthur/test.db'


def get_db():
    if 'db' not in g:
        g.db = SqliteDB(current_app.config['DATABASE'])
    return g.db


def toDate(dateString):
    return datetime.datetime.strptime(dateString, "%d-%m-%Y").date()


def datesToInterval(date1: datetime.date, date2: datetime.date):
    d1 = datetime.datetime.combine(date1, datetime.time.min)
    d2 = datetime.datetime.combine(date2, datetime.time.max)
    ts1 = int(time.mktime(d1.timetuple()))
    ts2 = int(time.mktime(d2.timetuple()))
    return ts1, ts2


@app.route('/weather/<city>', methods=['GET'])
def query_weather(city):
    db = get_db()
    start = request.args.get('start', default='1-1-0001')
    stop = request.args.get('stop', default='31-12-9999')
    try:
        date_start = toDate(start)
        date_stop = toDate(stop)
    except ValueError as e:
        return str(e)
    if date_start > date_stop:
        return f'Start {date_start} is later than stop {date_stop}'
    ts_start, ts_stop = datesToInterval(date_start, date_stop)
    q_res = db.query(ts_start, ts_stop, city)
    unit = request.args.get('unit', 'K')
    try:
        result = [x.pretty(unit) for x in q_res]
    except KeyError:
        return f'Unknown unit {unit}'
    return jsonify(result)


if __name__ == "__main__":
    app.run(host='localhost', port='5050', debug=True)
