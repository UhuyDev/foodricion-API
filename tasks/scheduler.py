from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timezone
from database.Engine import Sessionlocal
import models

def datetime_to_timestamp(dt):
    return int(dt.timestamp())

def delete_expired_otps():
    with Sessionlocal() as db:
        db.query(models.OTP).filter(models.OTP.expires_at <= datetime_to_timestamp(datetime.now(timezone.utc))).delete()
        db.commit()

def delete_expired_refresh_tokens():
    with Sessionlocal() as db:
        db.query(models.Token).filter(
            models.Token.expires_at <= datetime_to_timestamp(datetime.now(timezone.utc))).delete()
        db.commit()

scheduler = BackgroundScheduler()
scheduler.add_job(delete_expired_otps, IntervalTrigger(minutes=1))
scheduler.add_job(delete_expired_refresh_tokens, IntervalTrigger(minutes=1))

def start_scheduler():
    scheduler.start()

def shutdown_scheduler():
    scheduler.shutdown()