import json

from flask import Flask, send_from_directory
from dateutil.parser import parse
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/positions")
def positions():
    with open('data/positions-hashed.txt', 'r') as f:
        positions = []
        for line in f.readlines():
            if '\n' in line:
                line = line[:-1]
            positions.append([int(x) for x in line.split(',')])
        return json.dumps(positions)

@app.route("/api/image")
def image():
    return send_from_directory("data", "camera-image.jpg")

@app.route("/api/customers/maxcount")
def max_customers():
    max_count = 0
    with open('data/records.txt', 'r') as f:
        records = [line[:-1] if '\n' in line else line for line in f.readlines()]
        for record in records:
            record_arr = record.split('  ')
            record_count = int(record_arr[0])
            print(record_count)
            if record_count > max_count:
                max_count = record_count
    return max_count

@app.route("/api/customers/count")
def current_customers_count():
    with open('data/state.txt', 'r') as f:
        record = f.read()[:-1]
        data_array = record.split('  ')
        return json.dumps({
            'count': data_array[0],
            'datetime': data_array[1]
        })


@app.route("/api/products")
def products():
    with open('data/products.txt', 'r') as f:
        products = [line[:-1] if '\n' in line else line for line in f.readlines()]
        return json.dumps(products)


@app.route("/api/customers/counts")
def customers_counts():
    MINUTES_BLOCK = 1
    starting_hour = None
    starting_minute = None
    ending_hour = None
    ending_minute = None
    record_arrs = []
    with open('data/records.txt', 'r') as f:
        records = [line[:-1] if '\n' in line else line for line in f.readlines()]
        for record in records:
            record_arr = record.split('  ')
            record_time = parse(record_arr[1])
            record_arrs.append([int(record_arr[0]), record_time])
            if starting_hour is None and starting_minute is None:
                starting_hour = record_time.hour
                starting_minute = record_time.minute
            ending_hour = record_time.hour
            ending_minute = record_time.minute

    minutes = (ending_hour - starting_hour) * 60 + ending_minute - starting_minute
    groups = (minutes // MINUTES_BLOCK) + 1
    counts = [[] for _ in range(0, groups)]

    for record_arr in record_arrs:
        record_minutes = (record_arr[1].hour - starting_hour) * 60 + record_arr[1].minute - starting_minute
        index = record_minutes // MINUTES_BLOCK
        counts[index].append(record_arr[0])

    max_counts = []
    for count in counts:
        max_count = 0
        for c in count:
            if c > max_count:
                max_count = c
        max_counts.append(max_count)
    return json.dumps(max_counts)
