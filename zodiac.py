from flask import Flask
from flask import render_template, redirect, make_response
import requests
import datetime
import json
import flask
from urllib import parse, request

app = Flask(__name__)

DEFAULT = {'sign': 'aries'}

def get_value_with_fallback(key):
    if flask.request.args.get(key):
        return flask.request.args.get(key)
    if flask.request.cookies.get(key):
        return flask.request.cookies.get(key)
    return DEFAULT[key]

@app.route('/')
def home():
    sign = get_value_with_fallback('sign')
    astro = get_astro(sign)
    date = get_date(sign)
    info = get_info(sign)
    sign = sign.title()
    response = make_response(render_template('home.html', astro=astro, date=date, info=info, sign=sign))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie('sign', sign, expires=expires)
    return response

def get_astro(query):
    query = parse.quote(query)
    url = "https://sameer-kumar-aztro-v1.p.rapidapi.com/"
    headers = {"X-RapidAPI-Key": "a26c4f9336mshfccf72aba459d25p13af07jsn566ee16f2f31",
               "X-RapidAPI-Host": "sameer-kumar-aztro-v1.p.rapidapi.com"}
    querystring = {"sign": query, "day": "today"}
    response = requests.request("POST", url, headers=headers, params=querystring)
    astro = response.json()['description']
    return astro

def get_date(query):
    query = parse.quote(query)
    url = "https://sameer-kumar-aztro-v1.p.rapidapi.com/"
    headers = {"X-RapidAPI-Key": "a26c4f9336mshfccf72aba459d25p13af07jsn566ee16f2f31",
               "X-RapidAPI-Host": "sameer-kumar-aztro-v1.p.rapidapi.com"}
    querystring = {"sign": query, "day": "today"}
    response = requests.request("POST", url, headers=headers, params=querystring)
    date = response.json()['current_date']
    return date

def get_info(query):
    query = parse.quote(query)
    url = "https://sameer-kumar-aztro-v1.p.rapidapi.com/"
    headers = {"X-RapidAPI-Key": "a26c4f9336mshfccf72aba459d25p13af07jsn566ee16f2f31",
               "X-RapidAPI-Host": "sameer-kumar-aztro-v1.p.rapidapi.com"}
    querystring = {"sign": query, "day": "today"}
    response = requests.request("POST", url, headers=headers, params=querystring)
    info = {
        'color': response.json()['color'],
        'compatibility': response.json()['compatibility'],
        'number': response.json()['lucky_number'],
        'time': response.json()['lucky_time'],
        'date_range': response.json()['date_range']
    }
    return info

if __name__ == '__main__':
    app.run(port=5000, debug=True)
