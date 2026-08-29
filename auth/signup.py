"""
signup.py
---------
Handles user signup:
- Takes username and password
- Hashes password
- Stores user in database
"""

from db.db_setup import SessionLocal
from db.models import User
from auth.auth_utils import hash_password


def signup(username: str, password: str, role: str = "user"):
    db = SessionLocal()
    try:
        # Hash the password
        hashed_pw = hash_password(password)

        # Create new user
        new_user = User(username=username, password_hash=hashed_pw, role=role)

        # Add to DB
        db.add(new_user)
        db.commit()
        print(f"✅ User '{username}' created successfully!")
    except Exception as e:
        print("❌ Error creating user:", e)
        db.rollback()
    finally:
        db.close()


# Example usage
if __name__ == "__main__":
    signup("testuser", "mypassword123", "user")
