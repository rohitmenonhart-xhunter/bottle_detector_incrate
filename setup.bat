@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Setup complete! You can now run the application with: python bottle_counter.py
pause 