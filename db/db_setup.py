"""
db_setup.py
-----------
This file handles database configuration only.
It defines the engine, Base class, and session factory.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database URL
# "sqlite:///users.db" → SQLite database stored in a file called users.db
DATABASE_URL = "sqlite:///users.db"

# Create the database engine
# echo=True → logs SQL commands to the console (helpful for debugging)
engine = create_engine(DATABASE_URL, echo=True)

# Base class → all models (tables) will inherit from this
Base = declarative_base()

# Session factory → used to interact with the database
SessionLocal = sessionmaker(bind=engine)
