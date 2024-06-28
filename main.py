import uvicorn
import models
import routes
from fastapi import FastAPI
from database.Engine import engine, Sessionlocal
from middlewares.ResponseMiddleware import ResponseMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timezone

# Initialize FastAPI application
app = FastAPI()

# Create all database tables
models.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(routes.AuthRouter)
app.include_router(routes.BookmarkRouter)
app.include_router(routes.ChatbotRouter)
app.include_router(routes.NutritionRouter)
app.include_router(routes.UserRouter)
app.include_router(routes.OTPRouter)

# Include Middleware
app.add_middleware(ResponseMiddleware)


# Function For Automatically Delete Expired OTP On Database
def delete_expired_otps():
    with Sessionlocal() as db:
        db.query(models.OTP).filter(models.OTP.expiry_at <= datetime.now(timezone.utc)).delete()
        db.commit()


scheduler = BackgroundScheduler()
scheduler.add_job(delete_expired_otps, IntervalTrigger(minutes=1))


@app.on_event("startup")
def start_scheduler():
    scheduler.start()


@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()


# Root endpoint to check if the API is working
@app.get("/", status_code=200)
def welcome():
    return "foodricion-api is working"


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
