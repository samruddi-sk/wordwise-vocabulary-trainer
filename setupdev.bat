@echo off
setlocal
cd /d "%~dp0"
echo [1/4] Creating Python environment...
if not exist env python -m venv env
call env\Scriptsctivate.bat
if errorlevel 1 goto :error
echo [2/4] Installing backend dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 goto :error
echo [3/4] Applying database migrations...
alembic upgrade head
if errorlevel 1 goto :error
echo [4/4] Installing frontend dependencies...
cd frontend
call npm install
if errorlevel 1 goto :error
cd ..
echo Setup complete. Run runapplication.bat to start the app.
exit /b 0
:error
echo Setup failed. Check the error above.
exit /b 1
