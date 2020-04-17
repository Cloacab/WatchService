from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc

from app import app
from create_db import bootstrap

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


@app.before_first_request
def add_scheduler():
    scheduler.start()

    try:
        scheduler.reschedule_job(job_id='covid_job', trigger='interval', minutes=app.config['REQUEST_INTERVAL'])
        scheduler.reschedule_job(job_id='currencies_job', trigger='interval', minutes=app.config['REQUEST_INTERVAL'])
    except Exception as e:
        bootstrap(scheduler)

    scheduler.print_jobs()
