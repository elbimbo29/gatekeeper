import os

# Define project structure (no extra "gatekeeper" root)
structure = [
    "app.py",
    "requirements.txt",
    "Dockerfile",
    "README.md",
    "auth/__init__.py",
    "auth/auth_utils.py",
    "auth/jwt_manager.py",
    "db/__init__.py",
    "db/models.py",
    "db/db_setup.py",
    "pages/admin_dashboard.py",
    "pages/user_dashboard.py",
]

# Create directories and files
for file in structure:
    path = os.path.join(".", file)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("")  # create empty file

print("✅ Gatekeeper project structure created successfully in current folder!")
