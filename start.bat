@echo off
setlocal
chcp 65001 > nul

echo [INFO] Запускаем QA Helper Pro...

:: Активируем виртуальное окружение
call venv\Scripts\activate.bat

:: Запускаем приложение Streamlit
streamlit run main.py

endlocal