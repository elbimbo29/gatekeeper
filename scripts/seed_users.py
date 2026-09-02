import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.db_setup import SessionLocal
from db.models import User
from auth.auth_utils import hash_password


def seed_users():
    db = SessionLocal()
    users = [
        ("admin_test", "Admin123!", "admin"),
        ("logs_test", "Logs123!", "logs"),
        ("user_test", "User123!", "user"),
        ("dup_test", "Dup123!", "user"),
        ("remember_test", "Remember123!", "user"),
    ]

    for username, password, role in users:
        if not db.query(User).filter_by(username=username).first():
            new_user = User(
                username=username, password_hash=hash_password(password), role=role
            )
            db.add(new_user)

    db.commit()
    db.close()
    print("✅ Test users seeded successfully!")


if __name__ == "__main__":
    seed_users()
