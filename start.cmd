@echo off
cd /d %~dp0
echo %cd%

tasklist /nh|find /i "Appium.exe"
if errorlevel 1 (
    echo could not start while Appium not running
    goto run
) else (
    REM echo Appium is running
)

tasklist /nh|find /i "Nox.exe"
if errorlevel 1 (
    echo could not start while Nox not running
    goto finish
) else (
    REM echo Nox is running
    goto run
)

:run
REM echo venv\scripts\python -m xuexi
venv\scripts\python -m xuexi
echo xuexi successfully!
pause
exit

:finish
echo please start Appium and Nox before
pause