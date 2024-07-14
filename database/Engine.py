import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Load environment variables from .env file
load_dotenv()

# Retrieve the database URL from environment variables
URL_DATABASE = os.environ.get("DATABASE_URL")

# Create an SQLAlchemy engine with the specified database URL
engine = create_engine(URL_DATABASE, pool_size=10, max_overflow=30)

# Create a sessionmaker bound to the engine
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base class for declarative models
Base = declarative_base()


# Function to get a database session
def get_db():
    db = Sessionlocal()
    try:
        # Yield the database session to the caller
        yield db
    finally:
        # Ensure the session is closed after use
        db.close()
