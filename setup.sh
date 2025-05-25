#!/bin/bash

echo "========================================"
echo "   SECURITY CALCULATOR SETUP - LINUX"
echo "========================================"
echo

# Verifică Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nu este instalat!"
    echo "Pe Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    echo "Pe CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "Pe macOS: brew install python3"
    exit 1
fi

# Afișează versiunea Python
echo "✅ Python detectat:"
python3 --version

# Verifică dacă venv există
if [ -d "venv" ]; then
    echo "🗑️  Șterg venv existent..."
    rm -rf venv
fi

# Creează venv
echo
echo "🔄 Creez virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Eroare la crearea venv!"
    echo "Încearcă: sudo apt install python3-venv"
    exit 1
fi

echo "✅ Virtual environment creat!"

# Activează venv și instalează dependențele
echo
echo "🔄 Activez venv și instalez dependențele..."
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Instalează requirements
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Eroare la instalarea dependențelor!"
    exit 1
fi

echo
echo "🎉 SETUP COMPLET!"
echo "========================================"
echo
echo "Pentru a rula calculatorul:"
echo
echo "1. Activează venv:"
echo "   source venv/bin/activate"
echo
echo "2. Testare rapidă:"
echo "   python quick_test.py"
echo
echo "3. Calculatorul complet:"
echo "   python security_calculator.py"
echo
echo "4. Raport HTML:"
echo "   python html_report_generator.py"
echo
echo "⚠️  IMPORTANT: Copiază fișierul CSV în acest director!"
echo "   packageanalysis_agldemoplatform_raspberrypi464.csv"
echo

# Fă scriptul executabil
chmod +x "$0"