import time
from apscheduler.schedulers.background import BackgroundScheduler
from central_control.collect_data import collect


def job():
    scheduler = BackgroundScheduler()
    scheduler.add_job(collect, 'cron', minute='*/5')
    scheduler.start()

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


