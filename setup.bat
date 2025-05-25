@echo off
echo ========================================
echo    SECURITY CALCULATOR SETUP - WINDOWS
echo ========================================
echo.

:: Verifică Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nu este instalat!
    echo Te rog să instalezi Python 3.8+ de pe python.org
    pause
    exit /b 1
)

:: Afișează versiunea Python
echo ✅ Python detectat:
python --version

:: Creează directorul dacă nu există
if not exist "venv" (
    echo.
    echo 🔄 Creez virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Eroare la crearea venv!
        pause
        exit /b 1
    )
    echo ✅ Virtual environment creat!
)

:: Activează venv și instalează dependențele
echo.
echo 🔄 Activez venv și instalez dependențele...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Eroare la instalarea dependențelor!
    pause
    exit /b 1
)

echo.
echo 🎉 SETUP COMPLET!
echo ========================================
echo.
echo Pentru a rula calculatorul:
echo.
echo 1. Activează venv:
echo    venv\Scripts\activate
echo.
echo 2. Testare rapidă:
echo    python quick_test.py
echo.
echo 3. Calculatorul complet:
echo    python security_calculator.py
echo.
echo 4. Raport HTML:
echo    python html_report_generator.py
echo.
echo ⚠️  IMPORTANT: Copiază fișierul CSV în acest director!
echo    packageanalysis_agldemoplatform_raspberrypi464.csv
echo.
pause