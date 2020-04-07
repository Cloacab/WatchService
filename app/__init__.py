from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from pytz import utc

# Flask app:
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

# Data base:
db = SQLAlchemy(app)
migrate = Migrate(app, db)


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

    scheduler.reschedule_job(job_id='covid_job', trigger='interval', minutes=app.config['REQUEST_INTERVAL'])
    scheduler.reschedule_job(job_id='currencies_job', trigger='interval', minutes=app.config['REQUEST_INTERVAL'])

    scheduler.print_jobs()


from app import models, routes
