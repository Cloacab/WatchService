import json
from datetime import datetime
from app import app, db
from app import models, requests
from sqlalchemy import func


@app.route('/get_info/get_currency', methods=['GET'])
def currency():
    request_time = datetime.utcnow()
    q = db.session.query(models.Currency_model)
    currencies = q.get(db.session.query(func.max(models.Currency_model.id)).scalar())
    if currencies is None:
        return 'something went wrong, nothing in database'
    if (request_time - currencies.date).seconds > app.config['EXPIRATION_INTERVAL']:
        print('Too much time elapsed: {}'.format(request_time - currencies.date))
        response = requests.Currencies().get_info()
    else:
        response = json.loads(currencies.body)
    return response


@app.route('/get_info/get_covid', methods=['GET'])
def covid():
    request_time = datetime.utcnow()
    q = db.session.query(models.Covid_model)
    covids = q.get(db.session.query(func.max(models.Covid_model.id)).scalar())
    if covids is None:
        return 'something went wrong, nothing in database'
    if (request_time - covids.date).seconds > app.config['EXPIRATION_INTERVAL']:
        print('Too much time elapsed: {}'.format(request_time - covids.date))
        response = requests.Covid().get_info()
    else:
        response = json.loads(covids.body)
    return response
