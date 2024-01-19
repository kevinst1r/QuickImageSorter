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

:: Your script continues here
:: Check for Python installation and install if not present
python -V >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Installing Python...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; iwr -Uri 'https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe' -OutFile 'python_installer.exe'; Start-Process -FilePath 'python_installer.exe' -Args '/quiet InstallAllUsers=1 PrependPath=1' -Wait; Remove-Item -Path 'python_installer.exe'}"
    echo Python installed.
) ELSE (
    echo Python is already installed.
)

:: Install PyQt5
echo Installing PyQt5...
python -m pip install PyQt5
echo PyQt5 installation complete.

:: Ask for permission to add files to Program Files
echo Do you want to add files to the Program Files directory? (Y/N)
set /p userinput=
if /I "%userinput%"=="Y" (
    echo Copying files to Program Files...
    xcopy /E /I "%~dp0\*" "C:\Program Files\Quick Image Sorter\"
    echo Files copied.
) else (
    echo Skipping file copy to Program Files.
)

:: Create and Copy Desktop Shortcut
echo Do you want to create a 'Quick Image Sorter' desktop shortcut? (Y/N)
set /p userinput=
if /I "%userinput%"=="Y" (
    echo Creating desktop shortcut...
    powershell "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%userprofile%\Desktop\Quick Image Sorter.lnk'); $Shortcut.TargetPath = 'C:\Program Files\Quick Image Sorter\run.bat'; $Shortcut.WorkingDirectory = 'C:\Program Files\Quick Image Sorter'; $Shortcut.Save()"
    echo Shortcut created on desktop.
)

:: Create and Copy Startup Shortcut
echo Do you want to create a 'Quick Image Sorter' startup shortcut? (Y/N)
set /p userinput=
if /I "%userinput%"=="Y" (
    echo Creating startup shortcut...
    powershell "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\ECP Apps\Quick Image Sorter.lnk'); $Shortcut.TargetPath = 'C:\Program Files\Quick Image Sorter\run.bat'; $Shortcut.WorkingDirectory = 'C:\Program Files\Quick Image Sorter'; $Shortcut.Save()"
    echo Shortcut created in startup folder.
)



:: Final message to the user
echo.
echo You are now ready to run 'Quick Image Sorter'. Press any key to close this window...
pause > nul