@echo off
chcp 65001 > nul
echo ========================================================
echo   Dang khoi dong Marketing AI Campaign Manager...
echo ========================================================
"C:\Users\Acer\AppData\Local\Programs\Python\Python311\python.exe" run.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Co loi xay ra khi khoi chay ung dung!
    pause
)

