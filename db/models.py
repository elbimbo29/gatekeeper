"""
models.py
---------
This file defines the database tables (models).
Currently, we only have the User table.
"""

from sqlalchemy import Column, Integer, String
from .db_setup import Base  # Import Base from db_setup.py


# Define the User table
class User(Base):
    __tablename__ = "users"  # Table name in the database

    # Columns (fields) in the table
    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each user
    username = Column(String, unique=True, nullable=False)  # Username must be unique
    password_hash = Column(String, nullable=False)  # Hashed password (bcrypt)
    role = Column(String, default="user")  # Role: "user" or "admin"
