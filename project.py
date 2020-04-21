
import csv
from faker import Faker
from flask import Flask, send_from_directory

fake = Faker()

app = Flask('app')


@app.route('/')
def hello():
    return "Hello"


@app.route('/req')
def send():
    return send_from_directory('./', 'requirements.txt')


@app.route('/gen')
def series():
    return ''.join(['\n' +
                    str(fake.email() + ' - ' + fake.name())
                    for _ in range(100)
                    ]).replace('\n', '<br>')


@app.route('/average')
def students():
    with open('hw2.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        total = count = total2 = count2 = 0

        for row in csv_reader:
            total += float(row[1])
            count += 1
            total2 += float(row[2])
            count2 += 1

        if count and count2:
            aver1 = total / count
            aver2 = total2 / count2  ### 1дюйм = 2,54см   и  1фунт = 0,453592кг

            #########  переводим в см и кг, как и указано в задании
            average1 = aver1 * 2.54
            average2 = aver2 * 0.453592
            foo1 = average1, average2
            return 'Средний рост и вес (в см и кг соответственно) составляют - ' + str(foo1)


app.run()
