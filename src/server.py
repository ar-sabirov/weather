from flask import Flask, request, jsonify
from src.db.sqlite_db import SqliteDB

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World"


#TODO read-write collisions in db.query

#TODO try-catch weather unit


@app.route('/weather/<city>', methods=['GET'])
def query_weather(city):
    db = SqliteDB('/home/arthur/test.db')
    result = db.query_city('London')
    unit = request.args.get('unit', 'K')
    return jsonify([x.pretty(unit) for x in result])


if __name__ == "__main__":
    app.run(host='localhost', port='5050', debug=True)
