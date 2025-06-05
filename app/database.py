import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
load_dotenv()
import os

# Update with your actual database credentials
DATABASE_URL = os.getenv("DATABASE_URL")

# Create a synchronous SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

# Base class for models
Base = declarative_base()

# Function to get the session
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# Test database connection
def test_connection():
    try:
        with engine.connect() as connection:
            print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    test_connection()


