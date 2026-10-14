@echo off
setlocal
cd /d "%~dp0"
if not exist "%~dp0env\Scripts\activate.bat" (
  echo Please run setupdev.bat first.
  exit /b 1
)
start "Vocabulary Trainer API" cmd /k "cd /d ""%~dp0"" && call ""%~dp0env\Scripts\activate.bat"" && python main.py"
start "Vocabulary Trainer Frontend" cmd /k "cd /d ""%~dp0frontend"" && npm start"
echo Backend: http://127.0.0.1:8000/docs
echo Frontend: http://127.0.0.1:5173
