@echo off
setlocal
chcp 65001 > nul

echo =================================================
echo  QA Helper Pro - Installation and Setup
echo =================================================
echo.

:: 1. Проверка наличия Python в системе
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python не найден в системных переменных (PATH).
    echo.
    echo Пожалуйста, установите Python 3.10+ с официального сайта и обязательно
    echo поставьте галочку "Add Python to PATH" во время установки.
    echo.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Python обнаружен.
python --version
echo.

:: 2. Создание виртуального окружения, если его нет
if not exist "venv" (
    echo [INFO] Создание виртуального окружения (папка venv)...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Не удалось создать виртуальное окружение.
        pause
        exit /b 1
    )
    echo [INFO] Виртуальное окружение успешно создано.
) else (
    echo [INFO] Виртуальное окружение уже существует.
)
echo.

:: 3. Установка библиотек
echo [INFO] Активация окружения и установка библиотек из requirements.txt...
call venv\Scripts\activate.bat && pip install --upgrade pip && pip install -r requirements.txt && echo. && echo [INFO] Установка браузера для Frontend Анализатора (может занять несколько минут)... && playwright install chromium

if %errorlevel% neq 0 (
    echo [ERROR] Не удалось установить библиотеки. Проверьте подключение к интернету.
    pause
    exit /b 1
)

echo.
echo =================================================
echo  Установка завершена!
echo =================================================
echo Теперь вы можете запускать программу с помощью файла 'start.bat'.
echo.
pause