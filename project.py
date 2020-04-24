import csv
import json
import os
import random
import sqlite3
import string

import requests
from faker import Faker
from flask import Flask, send_from_directory, request

fake = Faker()

app = Flask('app')


@app.route('/gen-password')
def gen_password():
    default_length = 12
    default_digit = 0
    length = int(request.args.get('length', default_length))
    digit = int(request.args.get('digit', default_digit))
    if length < 8 or length > 24:
        return 'error'
    elif digit == 1:
        return ''.join([
            random.choice(string.hexdigits)
            for _ in range(length)
        ])
    else:
        return ''.join([
            random.choice(string.ascii_lowercase)
            for _ in range(length)
        ])


@app.route('/get-customers')
def get_customers():
    query = 'select FirstName, LastName from customers where City = "Oslo" or City = "Paris"'
    records = execute_query(query)
    result = '<br>'.join([
        str(record)
        for record in records
    ])
    return result


def execute_query(query):
    db_path = os.path.join(os.getcwd(), 'chinook.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    records = cur.fetchall()
    return records


@app.route('/get-first-name')
def get_custom():
    query = 'select distinct FirstName from customers'
    records = execute_query(query)
    result = '<br>'.join([
        str(record)
        for record in records
    ])
    return result


@app.route('/get-city-and-state')
def get_city_and_state():
    default_city = ''
    default_state = ''
    state = request.args.get('State', default_state)
    city = request.args.get('City', default_city)
    query = f'select FirstName, LastName, State, City from customers where State = "{state}" or City = "{city}"'
    records = execute_query(query)
    result = '<br>'.join([
        str(record)
        for record in records
    ])
    return result


@app.route('/get-astronauts')
def get_astronauts():
    response = requests.get('http://api.open-notify.org/astros.json')
    if response.status_code == 200:
        resp = json.loads(response.text)
        return f"Astronauts number: {resp.get('number', '<N/A>')}"
    else:
        return f'Error {response.status_code}'


@app.route('/')
def hello():
    return "Hello"


@app.route('/req')
def send():
    return send_from_directory('./', 'requirements.txt')


@app.route('/gen')
def series():
    return '<br>'.join([
        str(fake.email() + ' - ' + fake.name())
        for _ in range(100)
    ])


@app.route('/average')
def students():
    with open('hw2.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        total = total2 = count = 0

        for row in csv_reader:
            total += float(row[' \"Height(Inches)\"'])
            total2 += float(row[' \"Weight(Pounds)\"'])
            count += 1

        if count:
            aver1 = total / count
            aver2 = total2 / count
            ### 1дюйм = 2,54см   и  1фунт = 0,453592кг

            #########  переводим в см и кг, как и указано в задании
            average1 = aver1 * 2.54
            average2 = aver2 * 0.453592
            foo1 = average1, average2
            return 'Средний рост и вес (в см и кг соответственно) составляют - ' + str(foo1)


@app.route('/turnover')
def get_turnover():
    query = 'select sum(UnitPrice) * sum(Quantity) from invoice_items'
    records = execute_query(query)
    result = '<br>'.join(['Оборот компании - ' +
        str(record)
        for record in records
    ])
    return result


app.run(debug=True)
