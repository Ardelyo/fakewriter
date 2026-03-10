@echo off
setlocal

:: Check for Administrative privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Running as Administrator.
) else (
    echo [ERROR] This script must be run as Administrator!
    echo Prease right-click on this file and select 'Run as Administrator'.
    pause
    exit /b 1
)

:: Navigate to script directory
cd /d "%~dp0"

echo [1/3] Checking dependencies...
pip install -r requirements.txt --quiet

echo [2/3] Generating assets...
python create_icon.py

echo [3/3] Launching FakeWriter...
python main.py

if %errorLevel% neq 0 (
    echo [ERROR] Application crashed. See details above.
    pause
)

endlocal
