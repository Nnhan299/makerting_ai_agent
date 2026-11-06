@echo off
chcp 65001 > nul
title Khoi Dong He Thong AuraAI Marketing Agent

echo ======================================================================
echo   AuraAI Marketing Intelligence Enterprise - Khoi Dong He Thong
echo ======================================================================
echo.

set "PYTHON_EXE=C:\Users\Acer\AppData\Local\Programs\Python\Python311\python.exe"
set "PATH=C:\Program Files\nodejs;%PATH%"

:: 1. Khoi dong FastAPI Backend Server (Port 8000)
echo [1/3] Dang khoi dong Backend API Server (Port 8000)...
start "AuraAI Backend API Server" /min cmd /c ""%PYTHON_EXE%" -m uvicorn api_server:app --host 0.0.0.0 --port 8000"

:: 2. Doi Backend khoi dong trong 2 giay
timeout /t 2 /nobreak > nul

:: 3. Tu dong mo trinh duyet
echo [2/3] Dang mo trinh duyet http://localhost:3000...
start http://localhost:3000

:: 4. Khoi dong Vite Frontend (Port 3000)
echo [3/3] Dang chay React Vite Frontend Studio (Port 3000)...
echo.
cd /d "%~dp0frontend"
call npm.cmd run dev

pause
