import json

from flask import Flask
from dateutil.parser import parse
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# @app.route("/api/customers")
# def customers():
#     with open('customers.txt', 'r') as f:
#         customer_records = [line[:-1] if '\n' in line else line for line in f.readlines()]
#         customer_arrays = [customer_record.split('  ') for customer_record in customer_records]
#         return json.dumps(
#             [{'profile': customer_array[0], 'item_count': customer_array[1], 'updated_at': customer_array[2]}
#              for customer_array in customer_arrays])

@app.route("/api/positions")
def positions():
    with open('positions.txt', 'r') as f:
        positions = [line[:-1] if '\n' in line else line for line in f.readlines()]
        return json.dumps(positions)

@app.route("/api/customers/maxcount")
def max_customers():
    max_count = 0
    with open('records.txt', 'r') as f:
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
    with open('state.txt', 'r') as f:
        record = f.read()[:-1]
        data_array = record.split('  ')
        return json.dumps({
            'count': data_array[0],
            'datetime': data_array[1]
        })


@app.route("/api/products")
def products():
    with open('products.txt', 'r') as f:
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
    with open('records.txt', 'r') as f:
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
