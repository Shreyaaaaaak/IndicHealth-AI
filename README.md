# AarogyaMitra Backend (FastAPI)

AI-Powered Multilingual Rural Healthcare Assistant - Modular Backend Service.

## Tech Stack
* **Framework**: FastAPI (Python 3.10+)
* **Database**: MySQL / SQLite fallback (SQLAlchemy ORM)
* **Authentication**: JWT Bearer Tokens (`pyjwt` + `passlib[bcrypt]`)
* **AI Integration**: Google Gemini API
* **Documentation**: OpenAPI / Swagger UI (`/docs`)

---

## 🚀 Quick Start Guide

### 1. Setup Virtual Environment & Install Dependencies
```bash
# Navigate to backend folder
cd aarogyamitra-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Key settings in `.env`:
* `DATABASE_URL`: Set to MySQL `mysql+pymysql://user:pass@localhost:3306/db_name` or leave default SQLite `sqlite:///./aarogyamitra.db`.
* `GEMINI_API_KEY`: Add your Google Gemini API key for live AI answers.

### 3. Run Development Server
```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Interactive API Documentation
Open your browser and navigate to:
* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📡 API Endpoints Overview

### Authentication
* `POST /register` - Register a new user
* `POST /login` - Authenticate user & receive JWT token
* `GET /me` - Get current user profile (Protected)

### Health Profile
* `POST /profile` - Create health profile (Protected)
* `GET /profile` - Get current user's profile (Protected)
* `PUT /profile` - Update health profile (Protected)

### AI Assistant Chat
* `POST /chat` - Send medical query to Gemini AI (Protected)
* `GET /chat/history` - Retrieve conversation history (Protected)

### Symptom Assessment
* `POST /symptom-check` - Rule-based symptom check & doctor recommendation

### Medicine Information
* `GET /medicine/{medicine_name}` - Search medicine usage, dosage, side effects
* `GET /medicine` - List all 25 pre-seeded medicines
