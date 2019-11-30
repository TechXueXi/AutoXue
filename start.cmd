@echo off
cd /d %~dp0
echo %cd%
echo [Nox] is running?
pause
echo [Appium-Desktop] is running?
pause
REM echo venv\scripts\python -m xuexi
venv\scripts\python -m xuexi
echo xuexi successfully!
pause