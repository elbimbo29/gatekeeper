"""
create_tables.py
----------------
This script creates all tables defined in models.py.
Run this once to generate the users.db file with the users table.
"""

from db_setup import engine, Base
from models import User  # Import models so Base knows about them

# Create all tables in the database
Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")
