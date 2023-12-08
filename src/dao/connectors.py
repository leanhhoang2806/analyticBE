from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to the database using SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Create a database session
SessionLocal = sessionmaker(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()