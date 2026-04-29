@echo off
setlocal enabledelayedexpansion

:: Настройка интерфейса
title QA Helper Pro - Запуск
color 0B
echo ======================================================
echo           QA HELPER PRO - СИСТЕМА ЗАПУСКА
echo ======================================================

set "ROOT_DIR=%~dp0"
set "VENV_DIR=%ROOT_DIR%venv"
set "GUIDE_FILE=УСТАНОВКА_QA_HELPER.txt"

:: 1. ПРОВЕРКА: УСТАНОВЛЕН ЛИ PYTHON В СИСТЕМЕ?
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ОШИБКА] Python не найден в вашей системе.
    echo ------------------------------------------------------
    echo ПРИМЕНИТЕ РУЧНУЮ УСТАНОВКУ ПО ГАЙДУ:
    echo --^> %GUIDE_FILE%
    echo ------------------------------------------------------
    goto tail
)

:: 2. СОЗДАНИЕ VENV (если еще нет)
if not exist "%VENV_DIR%" (
    echo [1/3] Создание виртуального окружения...
    python -m venv "%VENV_DIR%"
    if %errorlevel% neq 0 (
        color 0C
        echo [ОШИБКА] Не удалось создать venv.
        echo Попробуйте создать его вручную, как написано в:
        echo --^> %GUIDE_FILE%
        goto tail
    )
)

:: 3. УСТАНОВКА БИБЛИОТЕК
echo [2/3] Проверка и установка библиотек...
"%VENV_DIR%\Scripts\python.exe" -m pip install streamlit pandas faker opencv-python Pillow
if %errorlevel% neq 0 (
    color 0E
    echo [ПРЕДУПРЕЖДЕНИЕ] Не удалось автоматически поставить библиотеки.
    echo Возможно, у вас нет интернета или доступ заблокирован.
    echo.
    echo Если программа не запустится, установите их сами по гайду:
    echo --^> %GUIDE_FILE%
    echo.
    timeout /t 5
)

:: 4. ЗАПУСК
echo [3/3] Запуск приложения...
echo ------------------------------------------------------
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