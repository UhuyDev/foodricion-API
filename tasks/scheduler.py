# Import the necessary modules for scheduling tasks and database operations
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timezone
from database.Engine import Sessionlocal
import models


# Function to convert datetime to timestamp
def datetime_to_timestamp(dt):
    return int(dt.timestamp())


# Function to delete expired OTPs from the database
def delete_expired_otps():
    with Sessionlocal() as db:
        db.query(models.OTP).filter(models.OTP.expires_at <= datetime_to_timestamp(datetime.now(timezone.utc))).delete()
        db.commit()


# Function to delete expired refresh tokens from the database
def delete_expired_refresh_tokens():
    with Sessionlocal() as db:
        db.query(models.Token).filter(
            models.Token.expires_at <= datetime_to_timestamp(datetime.now(timezone.utc))).delete()
        db.commit()


# Initialize the background scheduler
scheduler = BackgroundScheduler()

# Add jobs to the scheduler to run the delete functions every minute
scheduler.add_job(delete_expired_otps, IntervalTrigger(minutes=1))
scheduler.add_job(delete_expired_refresh_tokens, IntervalTrigger(minutes=1))


# Function to start the scheduler
def start_scheduler():
    scheduler.start()


# Function to shut down the scheduler
def shutdown_scheduler():
    scheduler.shutdown()
