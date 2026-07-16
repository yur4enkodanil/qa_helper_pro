@echo off
setlocal
chcp 65001 > nul

echo =================================================
echo  QA Helper Pro - Uninstallation
echo =================================================
echo.
echo WARNING: This will permanently delete the following:
echo   - The Python virtual environment (venv folder)
echo   - Downloaded system libraries (dlls folder)
echo   - All generated files and notes (generated_files, test_tree, qa_notes_storage)
echo   - The application log file (qa_helper_pro.log)
echo.
echo This action CANNOT be undone.
echo.

set /p "confirm=Are you sure you want to continue? (y/n): "

if /i not "%confirm%"=="y" (
    echo Uninstallation cancelled.
    pause
    exit /b 1
)

echo.
echo Starting uninstallation...

:: Remove directories
if exist "venv" ( rmdir /s /q "venv" && echo [OK] Virtual environment removed. )
if exist "dlls" ( rmdir /s /q "dlls" && echo [OK] Downloaded DLLs removed. )
if exist "generated_files" ( rmdir /s /q "generated_files" && echo [OK] Generated files removed. )
if exist "test_tree" ( rmdir /s /q "test_tree" && echo [OK] Test tree removed. )
if exist "qa_notes_storage" ( rmdir /s /q "qa_notes_storage" && echo [OK] Notes storage removed. )

:: Remove log file
if exist "qa_helper_pro.log" ( del /q "qa_helper_pro.log" && echo [OK] Log file removed. )

:: NEW: Remove python cache folders
echo [INFO] Cleaning up Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    rmdir /s /q "%%d"
)
echo [OK] Python cache removed.

echo.
echo =================================================
echo  Uninstallation Complete
echo =================================================
echo.
echo All local data for QA Helper Pro has been removed.
echo The core application files have NOT been deleted.
echo.
echo NOTE: To remove the browsers downloaded by Playwright,
echo you can run 'playwright uninstall' manually.
echo.
pause