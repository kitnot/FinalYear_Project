@echo off
setlocal EnableExtensions
cd /d "%~dp0"

title Smart Attendance - First Time Setup
color 0A

echo.
echo ============================================================
echo              SMART ATTENDANCE SYSTEM
echo                  FIRST TIME SETUP
echo ============================================================
echo.
echo Project folder:
echo %CD%
echo.

REM ============================================================
REM 1. CHECK APP.PY
REM ============================================================

if not exist "app.py" (
    echo [ERROR] app.py was not found.
    echo.
    echo Put setup.bat inside the SmartAttendance folder.
    echo.
    pause
    exit /b 1
)

echo [OK] Project folder detected.
echo.


REM ============================================================
REM 2. FIND PYTHON
REM ============================================================

echo [1/8] Checking Python...

where python >nul 2>&1

if %errorlevel%==0 (
    set "PYTHON_CMD=python"
    goto :python_found
)

where py >nul 2>&1

if %errorlevel%==0 (
    set "PYTHON_CMD=py"
    goto :python_found
)

echo.
echo [ERROR] Python was not found.
echo.
echo Install Python 3.11 or Python 3.12 64-bit.
echo Make sure "Add Python to PATH" is enabled.
echo.
pause
exit /b 1


:python_found

echo [OK] Python found.

%PYTHON_CMD% --version

echo.


REM ============================================================
REM 3. CREATE VIRTUAL ENVIRONMENT
REM ============================================================

echo [2/8] Checking virtual environment...

if exist ".venv\Scripts\python.exe" (
    echo [OK] Virtual environment already exists.
) else (
    echo Creating virtual environment...

    %PYTHON_CMD% -m venv .venv

    if errorlevel 1 (
        echo.
        echo [ERROR] Could not create virtual environment.
        echo.
        pause
        exit /b 1
    )

    echo [OK] Virtual environment created.
)

echo.


REM ============================================================
REM USE VENV PYTHON DIRECTLY
REM ============================================================

set "VENV_PYTHON=%CD%\.venv\Scripts\python.exe"

if not exist "%VENV_PYTHON%" (
    echo [ERROR] Virtual environment Python was not found.
    pause
    exit /b 1
)


REM ============================================================
REM 4. UPGRADE PIP
REM ============================================================

echo [3/8] Updating pip...

"%VENV_PYTHON%" -m pip install --upgrade pip

if errorlevel 1 (
    echo.
    echo [WARNING] pip upgrade failed.
    echo Setup will continue.
)

echo.


REM ============================================================
REM 5. INSTALL REQUIREMENTS
REM ============================================================

echo [4/8] Installing project requirements...

if not exist "requirements.txt" (
    echo.
    echo [ERROR] requirements.txt was not found.
    echo.
    pause
    exit /b 1
)

"%VENV_PYTHON%" -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ============================================================
    echo [ERROR] PACKAGE INSTALLATION FAILED
    echo ============================================================
    echo.
    echo Check the error above.
    echo.
    echo The application will NOT be started because one or more
    echo required packages could not be installed.
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Requirements installed successfully.
echo.


REM ============================================================
REM 6. CHECK IMPORTANT PYTHON MODULES
REM ============================================================

echo [5/8] Testing important Python modules...

"%VENV_PYTHON%" -c "import flask; import flask_sqlalchemy; import flask_login; import cv2; import numpy; print('[OK] Flask'); print('[OK] SQLAlchemy'); print('[OK] Flask-Login'); print('[OK] OpenCV', cv2.__version__); print('[OK] NumPy', numpy.__version__)"

if errorlevel 1 (
    echo.
    echo [ERROR] One or more important Python modules are missing.
    echo.
    pause
    exit /b 1
)

echo.


REM ============================================================
REM 7. CHECK FACE RECOGNITION MODELS
REM ============================================================

echo [6/8] Checking AI face recognition models...

set "YUNET=models\yunet\face_detection_yunet_2023mar.onnx"
set "SFACE=models\sface\face_recognition_sface_2021dec.onnx"

set "MODEL_ERROR=0"

if exist "%YUNET%" (
    echo [OK] YuNet face detector found.
) else (
    echo [MISSING] %YUNET%
    set "MODEL_ERROR=1"
)

if exist "%SFACE%" (
    echo [OK] SFace recognition model found.
) else (
    echo [MISSING] %SFACE%
    set "MODEL_ERROR=1"
)

if "%MODEL_ERROR%"=="1" (
    echo.
    echo ============================================================
    echo [ERROR] FACE RECOGNITION MODEL FILES ARE MISSING
    echo ============================================================
    echo.
    echo Required:
    echo.
    echo models\yunet\face_detection_yunet_2023mar.onnx
    echo models\sface\face_recognition_sface_2021dec.onnx
    echo.
    echo Copy these model files into the correct folders and
    echo run setup.bat again.
    echo.
    pause
    exit /b 1
)

echo.


REM ============================================================
REM 8. CREATE REQUIRED FOLDERS
REM ============================================================

echo [7/8] Creating application folders...

if not exist "instance" mkdir "instance"

if not exist "backups" mkdir "backups"

if not exist "face_data" mkdir "face_data"

echo [OK] Application folders ready.
echo.


REM ============================================================
REM DATABASE / ADMIN
REM ============================================================

echo [8/8] Checking database...

if exist "instance\smart_attendance.db" (
    echo [OK] Existing database found.
    echo Existing students and attendance will be preserved.
    goto :start_application
)

echo.
echo No existing Smart Attendance database was found.
echo.
echo A fresh database will be created when the application starts.
echo.

if exist "create_admin.py" (

    echo ------------------------------------------------------------
    echo ADMIN ACCOUNT SETUP
    echo ------------------------------------------------------------
    echo.
    echo You may now create the first administrator account.
    echo.

    "%VENV_PYTHON%" create_admin.py

    if errorlevel 1 (
        echo.
        echo [WARNING] create_admin.py did not complete successfully.
        echo.
        echo You can run it manually later with:
        echo.
        echo .venv\Scripts\python.exe create_admin.py
        echo.
        pause
    )

) else (

    echo [WARNING] create_admin.py was not found.
    echo The application will continue without running admin setup.

)


REM ============================================================
REM START APPLICATION
REM ============================================================

:start_application

echo.
echo ============================================================
echo                    SETUP COMPLETE
echo ============================================================
echo.
echo Smart Attendance is ready.
echo.
echo Local address:
echo.
echo              http://127.0.0.1:5000
echo.
echo ============================================================
echo.
echo Starting application...
echo.
echo DO NOT CLOSE THIS WINDOW WHILE USING SMART ATTENDANCE.
echo.
echo Press CTRL+C to stop the server.
echo.

timeout /t 2 /nobreak >nul

start "" "http://127.0.0.1:5000"

"%VENV_PYTHON%" app.py


REM ============================================================
REM APPLICATION STOPPED
REM ============================================================

echo.
echo ============================================================
echo Smart Attendance has stopped.
echo ============================================================
echo.

pause

endlocal