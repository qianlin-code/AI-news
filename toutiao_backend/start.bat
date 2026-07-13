@echo off
title News App - Start All
set "REDIS=E:\Redis"

echo ================================
echo   [1/3] Starting Redis...
echo ================================
"%REDIS%\redis-cli.exe" ping >nul 2>&1
if not errorlevel 1 (
    echo        Redis already running
) else (
    start "Redis" /min "%REDIS%\redis-server.exe"
    timeout /t 3 /nobreak >nul
    "%REDIS%\redis-cli.exe" ping >nul 2>&1
    if not errorlevel 1 (
        echo        Redis started OK
    ) else (
        echo        [WARN] Redis may have failed - check E:\Redis
    )
)

echo.
echo ================================
echo   [2/3] Starting Backend :8000
echo ================================
cd /d "%~dp0"
start "Backend-FastAPI" cmd /k "call ..\.venv\Scripts\activate.bat && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

echo.
echo ================================
echo   [3/3] Starting Frontend :5173
echo ================================
start "Frontend-Vite" cmd /k "cd /d %~dp0..\xwzx-news && npm run dev"

echo.
echo ================================
echo   All started!
echo   Backend : http://127.0.0.1:8000/docs
echo   Frontend: http://127.0.0.1:5173
echo ================================
echo.
echo You can close this window now.
pause
