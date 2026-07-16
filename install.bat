@echo off
setlocal enabledelayedexpansion
chcp 65001 > nul

echo =================================================
echo  QA Helper Pro - Installation and Setup (Robust Mode)
echo =================================================
echo This script will now install all components step-by-step to prevent silent failures.
echo.

:: NEW: Force-stop any lingering Streamlit processes that might lock the venv folder
echo [STEP 0] Terminating any running QA Helper Pro instances...
taskkill /F /IM streamlit.exe /T > nul 2>&1
echo [OK]
echo.

:: 1. Проверка наличия Python в системе
echo [STEP 1] Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FATAL ERROR] Python is not found in your system's PATH.
    echo.
    echo Please install Python 3.10+ from python.org and ensure you check "Add Python to PATH" during installation.
    echo.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python found:
python --version
echo.

:: 2. Создание виртуального окружения
echo [STEP 2] Creating a clean virtual environment...
if exist "venv" (
    echo [INFO] Existing 'venv' folder found. Deleting it to ensure a clean install...
    rmdir /s /q "venv"
)
echo [INFO] Creating new 'venv' folder...
python -m venv venv
if %errorlevel% neq 0 (
    echo [FATAL ERROR] Failed to create the virtual environment.
    pause
    exit /b 1
)
echo [OK] Virtual environment created successfully.
echo.

:: 3. Установка библиотек
echo [STEP 3] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [FATAL ERROR] Failed to activate the virtual environment.
    pause
    exit /b 1
)
echo [OK] Virtual environment activated.
echo.

echo [STEP 4] Installing libraries one by one...
echo [STEP 4.1] Upgrading pip (using recommended method)...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo [FATAL ERROR] Failed to upgrade pip. The script will now stop.
    pause
    exit /b 1
)

set "PACKAGES_TO_INSTALL=streamlit pandas faker opencv-python Pillow requests numpy beautifulsoup4 playwright axe-core-python qrcode[pil] pyzbar lxml polib plotly easyocr streamlit-drawable-canvas"

for %%p in (%PACKAGES_TO_INSTALL%) do (
    echo [INSTALLING] %%p
    pip install "%%p"
    if !errorlevel! neq 0 (
        echo [FATAL ERROR] Failed to install package: %%p
        echo Please check the error message above. It might be a network issue or a package-specific problem.
        echo The script will now stop.
        pause
        exit /b 1
    )
    echo [OK] %%p installed.
    echo.
)

echo [OK] All Python libraries installed successfully.
echo.

:: 4.5. Верификация критических пакетов
echo [STEP 4.5] Verifying critical packages...
python -c "import cv2; import pyzbar.pyzbar; import easyocr"
if %errorlevel% neq 0 (
    echo [FATAL ERROR] One or more critical libraries (e.g., opencv, pyzbar, easyocr) failed to import after installation.
    echo This likely means the installation was incomplete, possibly due to a network error during a large download (like PyTorch for easyocr).
    echo Please try running install.bat again. The script will now stop.
    pause
    exit /b 1
)
echo [OK] Critical packages verified successfully.
echo.

:: 6. Установка браузеров
echo [STEP 5] Installing browsers for Playwright...
playwright install
if %errorlevel% neq 0 (
    echo [WARNING] Failed to automatically install browsers. The 'Frontend Analyzer' module may not work.
)
echo [OK] Browser installation complete.
echo.

echo.
echo =================================================
echo  Installation Complete!
echo =================================================
echo You can now run the program using 'start.bat'.
echo.
pause