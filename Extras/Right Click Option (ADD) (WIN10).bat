@echo off
SETLOCAL

:: Find the path to the Python executable
FOR /F "delims=" %%i IN ('where python') DO SET "pythonPath=%%i"

:: Get the directory where the batch file is located
SET "scriptDir=%~dp0"

:: Remove the trailing backslash
SET "progPath=%scriptDir:~0,-1%\..\main.py"

:: Add to registry
REG ADD "HKCR\Directory\Background\shell\OpenWithYourProgram" /t REG_SZ /d "Open with Quick Image Sorter" /f
REG ADD "HKCR\Directory\Background\shell\OpenWithYourProgram\command" /t REG_SZ /d "\"%pythonPath%\" \"%progPath%\" \"%%V\"" /f

ENDLOCAL
