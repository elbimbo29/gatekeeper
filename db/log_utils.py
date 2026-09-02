from db.db_setup import SessionLocal
from db.models import Log
from datetime import datetime


def record_log(event: str, actor: str, target: str = None):
    """
    Record a log entry in the database.

    Args:
        event (str): Description of the event (e.g., "Created user").
        actor (str): Username of the actor performing the action.
        target (str, optional): Target of the action (e.g., affected user).

    Returns:
        None
    """
    with SessionLocal() as db:  # ✅ context manager
        log_entry = Log(
            event=event, actor=actor, target=target, timestamp=datetime.utcnow()
        )
        db.add(log_entry)
        db.commit()  # ✅ commit only when writing
