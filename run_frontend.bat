@echo off
chcp 65001 > nul
set "PATH=C:\Program Files\nodejs;%PATH%"
echo ========================================================
echo   Dang khoi dong AuraAI React Frontend (Port 3000)...
echo ========================================================
cd /d "%~dp0frontend"
call npm.cmd run dev
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Khong the khoi chay Vite dev server!
    pause
)


