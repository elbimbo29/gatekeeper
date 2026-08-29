"""
logger.py
---------
Centralized logging module for Gatekeeper App.
- Records login attempts (success/failure)
- Tracks JWT expiry and invalid token events
- Logs suspicious activity
- Uses rotating log files (daily rotation)
"""

import logging
from logging.handlers import TimedRotatingFileHandler

# --- Logger Configuration ---
logger = logging.getLogger("gatekeeper")
logger.setLevel(logging.INFO)

# TimedRotatingFileHandler:
# - Rotates logs every midnight
# - Keeps 7 backup log files (gatekeeper.log.1 ... gatekeeper.log.7)
file_handler = TimedRotatingFileHandler(
    "gatekeeper.log", when="midnight", interval=1, backupCount=7
)

# Log format: timestamp, log level, message
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Attach handler to logger
logger.addHandler(file_handler)


def log_login_attempt(username: str, success: bool):
    """Log a user login attempt."""
    if success:
        logger.info(f"✅ Login successful for user '{username}'")
    else:
        logger.warning(f"❌ Login failed for user '{username}'")


def log_jwt_event(event: str, username: str = None):
    """Log JWT-related events (expired, invalid, tampered)."""
    if username:
        logger.warning(f"⚠️ JWT {event} for user '{username}'")
    else:
        logger.warning(f"⚠️ JWT {event} detected (no username)")


def log_suspicious_activity(username: str, reason: str):
    """Log suspicious activity for a user."""
    logger.error(f"🚨 Suspicious activity for user '{username}': {reason}")
