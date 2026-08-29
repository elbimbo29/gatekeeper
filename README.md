# Gatekeeper 🔐

## 📖 Overview
Gatekeeper is a security‑focused authentication and authorization system built with **Python** and **Streamlit**.  
It demonstrates modern role‑based access control, secure credential handling, and deployment pipelines using **Docker** and **GitHub Actions**.

---

## ✨ Features
- Role‑based dashboards for admins, users, and evaluators  
- JWT authentication with expiry enforcement  
- Password hashing using bcrypt  
- Logs dashboard to view, filter, search, and export activity  
- Database integration with SQLite  
- CI/CD pipeline using Docker, GHCR, and Render  

---

## 🛠 Tech Stack
- **Python** – core programming language  
- **Streamlit** – interactive UI framework  
- **SQLAlchemy + SQLite** – database ORM and lightweight DB  
- **PyJWT** – JSON Web Token authentication  
- **bcrypt** – password hashing for secure storage  
- **Docker** – containerization for deployment  
- **GitHub Actions** – CI/CD automation  
- **GHCR (GitHub Container Registry)** – container registry for storing images  
- **Render** – cloud hosting platform  
- **GitHub** – version control and collaboration  

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/elbimbo29/gatekeeper.git
cd gatekeeper

### 2. Create a virtual environment
```bash
python -m venv .venv

### Activate the environment
- **Windows**
```bash
.venv\Scripts\activate

### 3. Install dependencies
```bash
pip install -r requirements.txt

### 4. Run locally
```bash
streamlit run app.py
