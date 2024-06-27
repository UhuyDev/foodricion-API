import uvicorn
import models
import routes
from fastapi import FastAPI
from database.Engine import engine
from middlewares.ResponseMiddleware import ResponseMiddleware

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
app.add_middleware(ResponseMiddleware)

# Root endpoint to check if the API is working
@app.get("/", status_code=200)
def welcome():
    return "foodricion-api is working"

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)