import json
from datetime import datetime

from sqlalchemy import text

from app import app
from app.api import get_currencies, get_covid
from app.models import Currency, Covid


@app.route('/get_info/get_currency', methods=['GET'])
def currency():
    request_time = datetime.utcnow()
    currencies = Currency.query.order_by(text('-id')).first()
    if currencies is None:
        return 'something went wrong, nothing in database'
    if (request_time - currencies.date).seconds > app.config['EXPIRATION_INTERVAL']:
        print('Too much time elapsed: {}'.format(request_time - currencies.date))
        response = get_currencies()
    else:
        response = json.loads(currencies.body)
    return response


@app.route('/get_info/get_covid', methods=['GET'])
def covid():
    request_time = datetime.utcnow()
    covids = Covid.query.order_by(text('-id')).first()
    if covids is None:
        return 'something went wrong, nothing in database'
    if (request_time - covids.date).seconds > app.config['EXPIRATION_INTERVAL']:
        print('Too much time elapsed: {}'.format(request_time - covids.date))
        response = get_covid()
    else:
        response = json.loads(covids.body)
    return response
