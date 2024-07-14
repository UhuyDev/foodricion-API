import uvicorn
import models
import routes
from fastapi import FastAPI
from database.Engine import engine
from middlewares.ResponseMiddleware import ResponseMiddleware
from tasks.scheduler import start_scheduler, shutdown_scheduler

# Initialize FastAPI application
app = FastAPI()

# Create all database tables
models.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(routes.AuthRouter)
app.include_router(routes.OTPRouter)
app.include_router(routes.UserRouter)
app.include_router(routes.NutritionRouter)
app.include_router(routes.BookmarkRouter)
app.include_router(routes.ChatbotRouter)

# Include Middleware
app.add_middleware(ResponseMiddleware)


# Root endpoint to check if the API is working
@app.head("/", status_code=200)
@app.get("/", status_code=200)
def welcome():
    return "foodricion-api is working"


# Startup event to start the scheduler
@app.on_event("startup")
def startup_event():
    start_scheduler()


# Shutdown event to stop the scheduler
@app.on_event("shutdown")
def shutdown_event():
    shutdown_scheduler()


# Run the application using uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
