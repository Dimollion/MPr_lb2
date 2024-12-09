from flask import Flask, request, abort
from datetime import datetime, timedelta
import xml.etree.ElementTree
import requests
import json


app = Flask(__name__)


@app.route("/", methods = ['GET'])
def hello_world():
    return '<html><body>Hello World!<body/></html>'


@app.route("/currency/static", methods = ['GET'])
def static_rate():
    if 'today' in request.args:
        return 'Today the euro exchange rate is 40.00 UAH'
    if 'yesterday' in request.args:
        return 'Yesterday the dollar exchange rate was 8 UAH.'
    return 'Select the desired day'


@app.route("/currency/dynamic", methods = ['GET'])
def dynamic_rate():
    selec_date = 'YYYYMMDD'
    if 'today' in request.args:
        selec_date = datetime.now().strftime('%Y%m%d')
    if 'yesterday' in request.args:
        selec_date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    if 'today' not in request.args and 'yesterday' not in request.args:
        return 'Select the desired day'

    r = requests.get(f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={selec_date}&end={selec_date}&valcode=eur&?json')
    r_js = json.loads(r.text)

    for i in r_js:
        return 'Euro exchange rate for the selected day: ' + str(i['rate']) + ' UAH.'


@app.route("/currency/give", methods = ['GET'])
def my_get_header():
    selec_date = datetime.now().strftime('%Y%m%d')
    if request.headers.get('Content-Type') == 'application/json':
        r = requests.get(f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={selec_date}&end={selec_date}&valcode=eur&?json')
        r_js = json.loads(r.text)
        return r_js
    if request.headers.get('Content-Type') == 'application/xml':
        r = requests.get(f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={selec_date}&end={selec_date}&valcode=eur&?xml')
        r_js = r.text
        return r_js
    return 'Bad Content-Type'


@app.route("/currency", methods = ['POST']) # Тільки json!!!
def post_handler():
    if 'Content-Type' not in request.headers:
        abort(400)
    if request.headers['Content-Type'] != 'application/json':
        abort(400)
    if saver(request.json):
        return "written", 201
    return "ok", 200

def saver(post_data):
    file = open("my_file.txt", 'a')
    file.write(json.dumps(post_data, indent=4) + '\n')
    file.close()
    return True


if __name__ == '__main__':
    app.run(port=8000)