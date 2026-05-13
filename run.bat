@echo off
:: run.bat — One-click launcher for Weather Analytics Dashboard (Windows)
:: SAVE THIS FILE AS: run.bat
:: Double-click this file OR run it from terminal: .\run.bat

echo.
echo =========================================
echo   Weather Analytics Dashboard
echo =========================================
echo.

:: Check if virtual environment exists
IF NOT EXIST "venv\Scripts\activate.bat" (
    echo [STEP 1] Creating virtual environment...
    python -m venv venv
    echo Done.
) ELSE (
    echo [OK] Virtual environment found.
)

:: Activate venv
echo [STEP 2] Activating virtual environment...
call venv\Scripts\activate.bat

:: Install/upgrade dependencies
echo [STEP 3] Installing dependencies...
pip install -q -r requirements.txt

:: Generate dataset if missing
IF NOT EXIST "data\weather.csv" (
    echo [STEP 4] Generating dataset...
    python data\generate_data.py
) ELSE (
    echo [OK] Dataset already exists.
)

:: Run the app
echo.
echo [STEP 5] Starting dashboard at http://127.0.0.1:8050
echo          Press CTRL+C to stop.
echo.
python app.py

pause
