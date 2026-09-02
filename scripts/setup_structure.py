import os

# Define your project structure
structure = {"gatekeeper": ["auth", "db", "components", "pages", "scripts"]}


def create_structure(base_path="."):
    for root, folders in structure.items():
        root_path = os.path.join(base_path, root)
        os.makedirs(root_path, exist_ok=True)

        for folder in folders:
            folder_path = os.path.join(root_path, folder)
            os.makedirs(folder_path, exist_ok=True)

            # Create __init__.py inside each folder
            init_file = os.path.join(folder_path, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, "w") as f:
                    f.write("# Package initializer\n")

    print("✅ Project structure created with __init__.py files.")


if __name__ == "__main__":
    create_structure()
