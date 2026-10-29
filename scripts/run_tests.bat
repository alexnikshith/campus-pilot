@echo off
echo ==========================================
echo Running Backend Pytest Suite...
echo ==========================================
cd /d "%~dp0..\backend"
call .venv\Scripts\pytest.exe -v
if %errorlevel% neq 0 (
    echo [ERROR] Backend tests failed!
    exit /b %errorlevel%
)

echo.
echo ==========================================
echo Running Frontend Vitest Suite...
echo ==========================================
cd /d "%~dp0..\frontend"
call npm run test
if %errorlevel% neq 0 (
    echo [ERROR] Frontend tests failed!
    exit /b %errorlevel%
)

echo.
echo ==========================================
echo ALL TESTS PASSED SUCCESSFULLY!
echo ==========================================
