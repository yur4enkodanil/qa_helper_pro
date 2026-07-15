@echo off
setlocal
chcp 65001 > nul

echo =================================================
echo  QA Helper Pro - Обновление библиотек
echo =================================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Виртуальное окружение не найдено. Пожалуйста, сначала запустите install.bat.
    pause
    exit /b 1
)

:: Активация виртуального окружения
call venv\Scripts\activate.bat

echo [INFO] Обновление библиотек из requirements.txt...
pip install --upgrade -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Не удалось обновить библиотеки.
    pause
    exit /b 1
)

echo.
echo [INFO] Установка браузеров для Frontend Анализатора (может занять несколько минут)...
playwright install
if %errorlevel% neq 0 (
    echo [WARNING] Не удалось автоматически установить браузеры. Модуль Frontend Анализатор может не работать.
)

echo.
echo Обновление завершено!
pause