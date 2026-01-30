@echo off
REM CPR Pose Detection Model - Windows Setup Script
REM Professional deployment script for hackathon evaluation

echo ==========================================
echo CPR Pose Detection Model Setup
echo ==========================================

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% == 0 (
    echo Node.js found
    for /f "tokens=*" %%i in ('node --version') do echo Version: %%i
    
    echo Starting model server...
    echo Model will be available at: http://localhost:8000
    echo Press Ctrl+C to stop the server
    echo.
    
    npx serve . -p 8000
    goto :end
)

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% == 0 (
    echo Python found
    for /f "tokens=*" %%i in ('python --version') do echo Version: %%i
    
    echo Starting Python server...
    echo Model will be available at: http://localhost:8000
    echo Press Ctrl+C to stop the server
    echo.
    
    python -m http.server 8000
    goto :end
)

echo No suitable server found.
echo Please install Node.js or Python to run the model.
echo.
echo Installation options:
echo - Node.js: https://nodejs.org/
echo - Python: https://python.org/
echo.
echo Alternative: Open index.html directly in browser
echo (Note: Camera may not work without proper server)

:end
pause