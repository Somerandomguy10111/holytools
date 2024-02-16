from apscheduler.schedulers.background import BackgroundScheduler

def schedule(callback : callable, interval_in_sec : int):
    scheduler = BackgroundScheduler()
    scheduler.add_job(callback, 'interval', seconds=interval_in_sec)
    scheduler.start()