@echo off
:runscript
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo An error occurred. Press any key to return to the menu...
    pause > nul
)

:menu
cls
echo.
echo 1. Run the Python script again
echo 2. Exit
echo.
set /p choice="Enter your choice (1 or 2): "

if "%choice%"=="1" goto runscript
if "%choice%"=="2" exit

echo Invalid choice
pause
goto menu
