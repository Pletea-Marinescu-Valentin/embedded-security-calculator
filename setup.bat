@echo off
echo ========================================
echo    SECURITY CALCULATOR SETUP - WINDOWS
echo ========================================
echo.

:: Verifica Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python nu este instalat!
    echo Te rog sa instalezi Python 3.8+ de pe python.org
    pause
    exit /b 1
)

:: Afiseaza versiunea Python
echo [V] Python detectat:
python --version

:: Creeaza directorul daca nu exista
if not exist "venv" (
    echo.
    echo [~] Creez virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [X] Eroare la crearea venv!
        pause
        exit /b 1
    )
    echo [V] Virtual environment creat!
)

:: Activeaza venv si instaleaza dependentele
echo.
echo [~] Activez venv si instalez dependentele...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo [X] Eroare la instalarea dependentelor!
    pause
    exit /b 1
)

echo.
echo [*] SETUP COMPLET!
echo ========================================
echo.
echo Pentru a rula calculatorul:
echo.
echo 1. Activeaza venv:
echo    venv\Scripts\activate
echo.
echo 2. Testare rapida:
echo    python quick_test.py
echo.
echo 3. Calculatorul complet:
echo    python security_calculator.py
echo.
echo 4. Raport HTML:
echo    python html_report_generator.py
echo.
echo [!] IMPORTANT: Copiaza fisierul CSV in acest director!
echo    package-analysis_agl-demo-platform_raspberrypi4-64.csv
echo.
pause
