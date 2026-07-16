@echo off
setlocal
chcp 65001 > nul

echo =================================================
echo  QA Helper Pro - Обновление библиотек
echo =================================================
echo.

:: NEW: Force-stop any lingering Streamlit processes that might lock the venv folder
echo [INFO] Terminating any running QA Helper Pro instances...
taskkill /F /IM streamlit.exe /T > nul 2>&1
echo [OK]

if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Виртуальное окружение не найдено. Пожалуйста, сначала запустите install.bat.
    pause
    exit /b 1
)

:: Активация виртуального окружения
call venv\Scripts\activate.bat

echo [INFO] Обновление библиотек из requirements.txt...

echo [INFO] Updating all libraries directly to bypass file issues...
pip install --upgrade streamlit pandas faker opencv-python Pillow requests numpy beautifulsoup4 playwright axe-core-python "qrcode[pil]" pyzbar lxml polib plotly easyocr streamlit-drawable-canvas
if %errorlevel% neq 0 (
    echo [ERROR] Не удалось обновить библиотеки.
    pause
    exit /b 1
)

echo.
echo [INFO] Verifying critical packages...
python -c "import cv2; import pyzbar.pyzbar; import easyocr"
if %errorlevel% neq 0 (
    echo [ERROR] One or more critical libraries (e.g., opencv, pyzbar, easyocr) failed to import after update.
    echo This might indicate a broken installation. Please try running install.bat to perform a clean installation.
    echo The script will now stop.
    pause
    exit /b 1
)
echo [OK] Critical packages verified successfully.

echo.
echo [INFO] Установка браузеров для Frontend Анализатора (может занять несколько минут)...
playwright install
if %errorlevel% neq 0 (
    echo [WARNING] Не удалось автоматически установить браузеры. Модуль Frontend Анализатор может не работать.
)

echo.
echo Обновление завершено!
pause