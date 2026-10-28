# PlacementPilot — Environment & Setup Guide

This guide provides instructions for configuring and running the **PlacementPilot** platform on Windows and Linux development workstations.

---

## 1. Prerequisites Verified

The following development environment tools are installed and verified:
- **Operating System:** Windows 11 / Windows 10 (or Linux via WSL)
- **Python:** 3.12+ (installed: Python 3.12.3)
- **Node.js:** v20.12+ (installed: v20.12.2)
- **npm:** 10.8+ (installed: 10.8.1)
- **Git:** 2.40+ (installed: 2.55.0)
- **Docker & Docker Compose:** Installed (Docker Desktop v29.1.3)
- **Package Manager:** Windows Package Manager (winget v1.29.380)

---

## 2. Configuration Setup (`.env`)

1. Copy the example configuration to a local `.env` file in the project root:
   ```powershell
   Copy-Item .env.example .env
   ```
2. Populate the required environment variables:
   - `DATABASE_URL`: `postgresql://postgres:postgres@localhost:5432/placementpilot_db`
   - `SECRET_KEY`: Generate a 32+ character random secret string.
   - `FRONTEND_ORIGIN`: `http://localhost:5173`
   - `BACKEND_URL`: `http://localhost:8000`
   - `AI_PROVIDER`: `mock` (or `gemini` if API key is provided)

---

## 3. PostgreSQL Database Setup

PlacementPilot requires PostgreSQL 16 as its relational database. You can run PostgreSQL via **Docker** (recommended) or a **Local Windows Service**.

### Option A: Using Docker (Recommended)
1. Start Docker Desktop application from the Windows Start Menu or command line:
   ```powershell
   Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
   ```
2. Once Docker Desktop is running, launch the PostgreSQL container:
   ```powershell
   docker compose up -d postgres
   ```
3. Confirm container status:
   ```powershell
   docker ps
   ```

### Option B: Local Windows PostgreSQL Installation
If you prefer running a native Windows PostgreSQL server without Docker:
1. Install PostgreSQL 16 via winget:
   ```powershell
   winget install PostgreSQL.PostgreSQL.16
   ```
2. Ensure the Windows PostgreSQL service is started:
   ```powershell
   Start-Service postgresql-x64-16
   ```
3. Create the target database:
   ```powershell
   createdb -U postgres placementpilot_db
   ```

---

## 4. Database Connectivity Verification

Run the built-in diagnostic script to verify your database connection:
```powershell
.\backend\.venv\Scripts\python.exe scripts\verify_db.py
```
- If successful, you will see `[SUCCESS] PostgreSQL connection verified successfully!`.
- If PostgreSQL is offline, the script will output sanitized diagnostics without exposing passwords.

---

## 5. Running the Application

### 5.1 One-Click Launch
- **Start Backend:** Double-click or run `scripts\run_backend.bat`
- **Start Frontend:** Double-click or run `scripts\run_frontend.bat`
- **Run All Tests:** Double-click or run `scripts\run_tests.bat`

### 5.2 Manual Terminal Commands
#### Backend (FastAPI)
```powershell
cd backend
.\.venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Interactive API Docs (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)
- Health Check: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

#### Frontend (React + Vite)
```powershell
cd frontend
npm run dev
```
- Web Application: [http://localhost:5173](http://localhost:5173)

---

## 6. Running Test Suites

### Backend Unit Tests
```powershell
cd backend
.\.venv\Scripts\pytest.exe -v
```

### Frontend Vitest Suite
```powershell
cd frontend
npm run test
```

### Frontend Production Build Validation
```powershell
cd frontend
npm run build
```
