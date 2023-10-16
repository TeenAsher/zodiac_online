from flask import Flask
from flask import render_template, make_response
import datetime
import json
import flask
import os
import requests
from urllib import parse

app = Flask(__name__)

DEFAULT = {'sunsign': 'aries'}
DATE = datetime.date.today()
TODAY = DATE.strftime('%B %d, %Y')
API_KEY = os.environ.get("API_KEY")

def get_value_with_fallback(key):
    if flask.request.args.get(key):
        return flask.request.args.get(key)
    return DEFAULT[key]

@app.route('/')
def home():
    sunsign = get_value_with_fallback('sunsign')
    astro = get_astro(sunsign)
    info = get_info(sunsign)
    sunsign = sunsign.title()
    response = make_response(render_template('home.html', sunsign=sunsign, astro=astro, info=info, date=TODAY))
    return response

def get_astro(query):
    query = parse.quote(query)
    url = "https://horoscope-astrology.p.rapidapi.com/horoscope"
    querystring = {"day":"today","sunsign": query}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "horoscope-astrology.p.rapidapi.com"
        }
    response = requests.get(url, headers=headers, params=querystring)
    astro = response["horoscope"]
    return astro

def get_info(query):
    query = parse.quote(query)
    url = "https://horoscope-astrology.p.rapidapi.com/sign"
    querystring = {"s": query}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "horoscope-astrology.p.rapidapi.com"
        }
    response = requests.get(url, headers=headers, params=querystring)
    info = {
        'date_range': response["date_range"],
        'about': response["about"],
        'compatibility': response["compatibility"],
        'weaknesses': response["weaknesses"],
        'strengths': response["strengths"],
        'symbol': response["symbol"],
        'element': response["element"],
        'ruling_planet': response["ruling_planet"],
    }
    return info

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'),500

if __name__ == '__main__':
    app.run(debug=False)
