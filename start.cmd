@echo off
cd /d %~dp0
echo %cd%

tasklist /nh|find /i "Appium.exe"
if errorlevel 1 (
    echo could not start while Appium not running
    goto breakout
) else (
    REM echo Appium is running
)

tasklist /nh|find /i "Nox.exe"
if errorlevel 1 (
    echo could not start while Nox not running
    goto breakout
) else (
    REM echo Nox is running
    goto run
)


:run
REM echo venv\scripts\python -m xuexi
venv\scripts\python -m xuexi
pause
exit

:breakout
echo please start Appium and Nox
pause
exit