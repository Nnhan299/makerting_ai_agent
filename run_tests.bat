@echo off
chcp 65001 > nul
title AuraAI Marketing Agent - Chay Kiem Thu He Thong

echo ======================================================================
echo   AuraAI Marketing Intelligence Enterprise - Chay Bo Kiem Thu He Thong
echo ======================================================================
echo.

set "PYTHON_EXE=C:\Users\Acer\AppData\Local\Programs\Python\Python311\python.exe"
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

echo Dang kich hoat trinh kiem thu tu dong...
echo.
"%PYTHON_EXE%" run_tests.py

echo.
pause
