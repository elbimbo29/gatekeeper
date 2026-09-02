from db.db_setup import SessionLocal
from db.models import User
from auth.auth_utils import hash_password


def reset_password(username: str, new_password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if not user:
        print(f"❌ User {username} not found.")
        return
    user.password_hash = hash_password(new_password)
    db.commit()
    db.close()
    print(f"✅ Password for {username} has been reset.")


if __name__ == "__main__":
    # Example usage
    reset_password("bimbo", "newsecurepassword123")
