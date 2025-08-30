@echo off
REM Stock Trading Simulator - Windows Run Script

echo 🚀 Starting Stock Trading Simulator...

REM Check if setup has been run
if not exist "backend\venv" (
    echo ❌ Virtual environment not found. Please run setup first:
    echo python setup.py
    pause
    exit /b 1
)

REM Start backend server
echo 🔧 Starting backend server...
cd backend
call venv\Scripts\activate
start /B python src\app.py
cd ..

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend server
echo 🌐 Starting frontend server...
cd frontend
start /B python -m http.server 8000
cd ..

echo ✅ Servers started successfully!
echo.
echo 📊 Backend API: http://localhost:5000
echo 🌐 Frontend: http://localhost:8000
echo.
echo 🎯 Open your browser and go to: http://localhost:8000
echo.
echo Press any key to stop all servers...
pause >nul

REM Kill Python processes (this will stop both servers)
taskkill /f /im python.exe >nul 2>&1
echo 🛑 Servers stopped.
pause