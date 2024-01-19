@echo off
setlocal

:: Request admin privileges
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

:: If not running as admin, relaunch with admin rights
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    setlocal & pushd .
    cd /d %~dp0
    del "%temp%\getadmin.vbs"

:: Uninstallation process begins
echo Welcome to the Quick Image Sorter Uninstaller.
echo Are you sure you want to uninstall Quick Image Sorter? (Y/N)
set /p userinput=
if /I not "%userinput%"=="Y" exit /B

:: Removing program files
echo Removing Quick Image Sorter from Program Files...
if exist "C:\Program Files\Quick Image Sorter\" (
    rmdir /S /Q "C:\Program Files\Quick Image Sorter"
    echo Program files removed.
) else (
    echo Program files not found.
)

:: Removing Start Menu shortcut
echo Removing Start Menu shortcut...
if exist "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\ECP Apps\Quick Image Sorter.lnk" (
    del "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\ECP Apps\Quick Image Sorter.lnk"
    echo Start Menu shortcut removed.
) else (
    echo Start Menu shortcut not found.
)

:: Removing Desktop shortcut
echo Removing Desktop shortcut...
if exist "%userprofile%\Desktop\Quick Image Sorter.lnk" (
    del "%userprofile%\Desktop\Quick Image Sorter.lnk"
    echo Desktop shortcut removed.
) else (
    echo Desktop shortcut not found.
)

:: Final message
echo.
echo Quick Image Sorter has been successfully uninstalled. Press any key to close this window...
pause > nul
