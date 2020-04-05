from datetime import datetime

from app import app
from app import models, requests


@app.route('/get_info/get_currency', methods=['GET'])
def currency():
    request_time = datetime.utcnow()
    currencies = models.Currency_model.query.order_by('date desc').get(1)
    if currencies is None:
        return 'something went wrong, nothing in database'
    if (request_time - currencies.date).seconds > app.config['EXPIRATION_INTERVAL']:
        response = requests.Currencies().get_info()
    else:
        response = currencies.body
    return response


@app.route('/get_info/get_covid', methods=['GET'])
def covid():
    request_time = datetime.utcnow()
    covids = models.Covid_model.query.order_by('date desc').get(1)
    if covids is None:
        return 'something went wrong, nothing in database'
    if (request_time - covids.date).seconds > app.config['EXPIRATION_INTERVAL']:
        response = requests.Covid().get_info()
    else:
        response = covids.body
    return response
