@echo off
setlocal enabledelayedexpansion

set "LOG_FILE=%~dp0qa_helper_pro.log"

:: Настройка интерфейса
title QA Helper Pro - Запуск
color 0B
echo ====================================================== >> "%LOG_FILE%"
echo           QA HELPER PRO - STARTUP SYSTEM >> "%LOG_FILE%"
echo ====================================================== >> "%LOG_FILE%"

set "ROOT_DIR=%~dp0"
set "VENV_DIR=%ROOT_DIR%venv"
set "GUIDE_FILE=УСТАНОВКА_QA_HELPER.txt"

:: 1. ПРОВЕРКА: УСТАНОВЛЕН ЛИ PYTHON В СИСТЕМЕ?
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python not found in your system. >> "%LOG_FILE%"
    echo ------------------------------------------------------ >> "%LOG_FILE%"
    echo PLEASE INSTALL PYTHON MANUALLY USING THE GUIDE: >> "%LOG_FILE%"
    echo --^> %GUIDE_FILE% >> "%LOG_FILE%"
    echo ------------------------------------------------------ >> "%LOG_FILE%"
    goto tail
)

:: 2. СОЗДАНИЕ VENV (если еще нет)
if not exist "%VENV_DIR%" (
    echo [1/3] Creating virtual environment... >> "%LOG_FILE%"
    python -m venv "%VENV_DIR%"
    if %errorlevel% neq 0 (
        color 0C
        echo [ERROR] Failed to create venv. >> "%LOG_FILE%"
        echo Please try to create it manually as described in: >> "%LOG_FILE%"
        echo --^> %GUIDE_FILE% >> "%LOG_FILE%"
        goto tail
    )
)

:: 3. УСТАНОВКА БИБЛИОТЕК
echo [2/3] Checking and installing libraries... >> "%LOG_FILE%"
:: Используем requirements.txt для большей гибкости
"%VENV_DIR%\Scripts\python.exe" -m pip install -r "%ROOT_DIR%requirements.txt" >> "%LOG_FILE%" 2>&1
if %errorlevel% neq 0 (
    color 0E
    echo [WARNING] Failed to install libraries automatically. >> "%LOG_FILE%"
    echo This might be due to no internet connection or network restrictions. >> "%LOG_FILE%"
    echo. >> "%LOG_FILE%"
    echo If the application fails to start, please install them manually: >> "%LOG_FILE%"
    echo --^> %GUIDE_FILE% >> "%LOG_FILE%"
    echo. >> "%LOG_FILE%"
    timeout /t 5
)

:: 4. ЗАПУСК
echo [3/3] Starting application... >> "%LOG_FILE%"
echo ------------------------------------------------------ >> "%LOG_FILE%"
start "" "%VENV_DIR%\Scripts\streamlit.exe" run "%ROOT_DIR%main.py" --server.port 8501

if %errorlevel% neq 0 (
    color 0C
    echo [ОШИБКА] Не удалось запустить Streamlit.
    echo Проверьте выполнение всех шагов в файле:
    echo --^> %GUIDE_FILE%
    goto tail
)

exit /b 0

:tail
echo.
echo ======================================================
echo Нажми любую клавишу для выхода...
pause >nul
exit /b 1