import json
from datetime import datetime
from pytz import utc
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

# Constant to set interval of requests
REQUEST_INTERVAL = 10

# Time in seconds while data is valuable
EXPIRATION_INTERVAL = 1800

# Data base:
db = SQLAlchemy(app)


# Scheduler:
@app.before_first_request
def add_scheduler():
    jobstores = {
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    }
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

    scheduler.start()
    scheduler.remove_all_jobs()

    scheduler.add_job(Covid().get_info, 'interval', minutes=REQUEST_INTERVAL, id='covid_job')
    scheduler.add_job(Currencies().get_info, 'interval', minutes=REQUEST_INTERVAL, id='currencies_job')

    scheduler.print_jobs()


@app.route('/get_info/get_currency', methods=['GET'])
def currency():
    request_time = datetime.utcnow()
    currencies = models.Currency_model.query.order_by('date desc').get(1)
    if currencies is None:
        return 'something went wrong, nothing in database'
    if (request_time - currencies.date).seconds > EXPIRATION_INTERVAL:
        response = Currencies().get_info()
    else:
        response = currencies.body
    return response


@app.route('/get_info/get_covid', methods=['GET'])
def covid():
    request_time = datetime.utcnow()
    covids = models.Covid_model.query.order_by('date desc').get(1)
    if covids is None:
        return 'something went wrong, nothing in database'
    if (request_time - covids.date).seconds > EXPIRATION_INTERVAL:
        response = Covid().get_info()
    else:
        response = covids.body
    return response


from app import models
from app.requests import Covid, Currencies
