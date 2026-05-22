@echo off
echo ========================================
echo    StaySphere Hotel Management System
echo ========================================
echo.
echo Setting up your StaySphere application...
echo.

echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)
echo Python found successfully!

echo.
echo [2/5] Installing required packages...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)
echo Packages installed successfully!

echo.
echo [3/5] Setting up database...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Database migration failed
    pause
    exit /b 1
)
echo Database setup completed!

echo.
echo [4/5] Creating sample data...
python manage.py create_dummy_data
echo Sample data created successfully!

echo.
echo [5/5] Starting development server...
echo.
echo ========================================
echo    StaySphere is ready!
echo ========================================
echo.
echo Application URL: http://127.0.0.1:8000
echo Admin Panel: http://127.0.0.1:8000/admin/
echo.
echo Default Admin Login:
echo   Username: admin
echo   Password: (set during superuser creation)
echo.
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver
