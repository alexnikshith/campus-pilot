# PlacementPilot — Testing & Quality Assurance Guide

Testing is a first-class requirement across all development phases of PlacementPilot. This guide outlines how unit, integration, and end-to-end tests are structured and executed.

---

## 1. Test Architecture

### 1.1 Backend (`backend/tests/`)
- **Framework:** Pytest 8.x with `pytest-asyncio` and `pytest-cov`.
- **HTTP Testing:** FastAPI `TestClient` (Starlette) and HTTPX.
- **Fixtures:** Defined in `backend/tests/conftest.py`.
- **Isolation:** Tests use isolated mock sessions or dedicated test databases; no production student data is ever used.

### 1.2 Frontend (`frontend/src/test/`)
- **Runner:** Vitest 2.x configured in `frontend/vite.config.ts`.
- **DOM Simulation:** JSDOM environment with `@testing-library/react` and `@testing-library/jest-dom`.
- **Coverage:** Component mounting, user interactions, form validation, and error states.

---

## 2. Test Execution Commands

### 2.1 Backend Tests
Run all backend tests with verbose output:
```powershell
cd backend
.\.venv\Scripts\pytest.exe -v
```

Generate test coverage report:
```powershell
cd backend
.\.venv\Scripts\pytest.exe --cov=app --cov-report=term-missing
```

### 2.2 Frontend Tests
Run Vitest unit tests:
```powershell
cd frontend
npm run test
```

Run Vitest in watch mode during development:
```powershell
cd frontend
npm run test:watch
```

### 2.3 One-Click Unified Test Runner
Execute both test suites sequentially with immediate failure exit:
```powershell
.\scripts\run_tests.bat
```

---

## 3. Verified Phase 1 Test Results

| Test Suite | File | Status | Duration |
|---|---|---|---|
| Backend | `tests/test_health.py::test_root_endpoint` | PASSED | 0.05s |
| Backend | `tests/test_health.py::test_health_endpoint_success` | PASSED | 0.04s |
| Backend | `tests/test_health.py::test_health_endpoint_degraded` | PASSED | 0.04s |
| Frontend | `src/test/App.test.tsx::renders the application brand and hero header` | PASSED | 0.04s |
| Frontend | `src/test/App.test.tsx::renders Phase 1 verification modules` | PASSED | 0.04s |
| Frontend Build | TypeScript check & Vite production bundling (`tsc -b && vite build`) | PASSED | 11.19s |
