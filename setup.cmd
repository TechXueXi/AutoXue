@echo off
cd /d %~dp0
echo %cd%
echo python3.7+ installed?
pause
echo install venv...
python -m venv venv
echo venv installed OK.
echo install packages...
REM venv\scripts\python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
venv\scripts\python -m pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
venv\scripts\python -m pip install Appium-Python-Client -i https://pypi.tuna.tsinghua.edu.cn/simple
echo packages installed OK.
pause