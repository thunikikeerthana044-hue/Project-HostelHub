@echo off
title HostelHub Launcher
echo ==========================================================
echo   🏠 HOSTEL HUB — Launching Project...
echo ==========================================================
echo.
echo [1/3] Verifying python dependencies...
python -c "import django, razorpay, PIL" 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [!] Missing dependencies! Installing Django, Razorpay, and Pillow...
    pip install django razorpay pillow
) else (
    echo [*] Python packages are OK.
)
echo.
echo [2/3] Running database migrations...
python manage.py migrate
echo.
echo [3/3] Starting Django web server...
echo.
echo ==========================================================
echo   🔑 PRE-CONFIGURED LOGIN CREDENTIALS
echo ==========================================================
echo   🎓 Seeker / Student:   Username: seeker   Password: password123
echo   🏢 Owner / Host:       Username: owner    Password: password123
echo ==========================================================
echo.
echo [i] Launching browser to http://127.0.0.1:8000/ ...
start http://127.0.0.1:8000/
echo.
python manage.py runserver
pause
