"""
models.py
---------
This file defines the database tables (models).
We currently have: User, Log, and SupportTicket.
"""

from sqlalchemy import Column, Integer, String, DateTime, func
from db.db_setup import Base  # Import Base from db_setup.py


# 📝 Support Tickets
class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user = Column(String, nullable=False)  # who submitted
    description = Column(String, nullable=False)  # issue/request text
    status = Column(String, default="open")  # open, in-progress, closed
    admin_response = Column(String, nullable=True)  # response from admin


# 📜 Audit Logs
class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    event = Column(String, nullable=False)  # what happened
    actor = Column(String, nullable=False)  # who performed the action
    target = Column(String, nullable=True)  # which user was affected


# 👤 Users
class User(Base):
    __tablename__ = "users"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique ID
    username = Column(String, unique=True, nullable=False)  # must be unique
    password_hash = Column(String, nullable=False)  # hashed password
    role = Column(String, default="user")  # user/admin/logs
