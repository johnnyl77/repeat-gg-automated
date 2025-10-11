@echo off
REM Set to 1 to pause and review results, 0 to auto-close
set PAUSE_ON_FINISH=1

cd /d "%~dp0"
if "%PAUSE_ON_FINISH%"=="1" (
    start /min "" cmd /c "python repeat-gg-automated.py & pause"
) else (
    start /min "" cmd /c "python repeat-gg-automated.py"
)

    