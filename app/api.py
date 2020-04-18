import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import jsonify

from app import app, db
from app.models import Covid, Currency

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-GB,en;q=0.5',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'
}


def get_currencies():
    with app.app_context():
        api_key = 'fe2fbe9c5446ea780042'
        # fe2fbe9c5446ea780042
        # 238c003007bb6d0ad0d8
        base_url = "https://free.currconv.com"
        currencies = ['USD_RUB', 'EUR_RUB', 'GBP_RUB', 'SEK_RUB', 'BTC_RUB', 'EUR_USD']

        response = {}

        params = {
            'q': '',
            'compact': 'ultra',
            'apiKey': api_key
        }

        for curr in currencies:
            params['q'] = curr
            r = requests.get('{}/api/v7/convert'.format(base_url), params=params, headers=headers)
            response[curr] = r.json()[curr]

        currencies = Currency(datetime.utcnow(), json.dumps(response), r.status_code)

        db.session.add(currencies)
        db.session.commit()
        return response


def get_covid():
    url = "https://yandex.ru/web-maps/covid19?ll=82.834231%2C42.110996&z=3"
    with app.app_context():

        r = requests.get(url, headers=headers)

        if r.status_code != 200:
            response = r.text
        else:
            soup = BeautifulSoup(r.text, 'html.parser')

            keys = [name.string for name in (soup.select(".covid-panel-view__item > .covid-panel-view__item-name"))]
            values = [''.join(tag.get_text().split('+')[0].split()) for tag in
                      soup.select(".covid-panel-view__item > .covid-panel-view__item-cases")]
            values = [int(val) for val in values]

            response = dict(zip(keys, values))

        covid = Covid(datetime.utcnow(), json.dumps(response), r.status_code)

        db.session.add(covid)
        db.session.commit()

        return jsonify(response)



