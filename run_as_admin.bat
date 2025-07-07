@echo off
set VENV_PYTHON=f:\MyProject\euro-truck-sim2\env\Scripts\python.exe
if exist %VENV_PYTHON% (
    powershell -Command "Start-Process '%VENV_PYTHON%' -ArgumentList 'master.py' -Verb RunAs"
) else (
    echo محیط مجازی پیدا نشد. در حال استفاده از پایتون سیستمی...
    powershell -Command "Start-Process python -ArgumentList 'master.py' -Verb RunAs"
)