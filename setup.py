#!/usr/bin/env python3
"""
Script de setup automat pentru Security Calculator.
Creeaza venv si instaleaza dependentele.
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Ruleaza o comanda si afiseaza progresul."""
    print(f"[~] {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                                capture_output=True, text=True)
        print(f"[V] {description} - Succes!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[X] {description} - Esuat!")
        print(f"Eroare: {e.stderr}")
        return False

def check_python_version():
    """Verifica versiunea Python."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("[X] Python 3.8+ este necesar!")
        print(f"Versiunea ta: Python {version.major}.{version.minor}")
        return False
    
    print(f"[V] Python {version.major}.{version.minor}.{version.micro} - OK!")
    return True

def setup_environment():
    """Configureaza mediul de dezvoltare."""
    print("SETUP SECURITY CALCULATOR")
    print("=" * 50)
    
    if not check_python_version():
        return False
    
    os_name = platform.system()
    print(f"Sistem de operare: {os_name}")
    
    if os_name == "Windows":
        venv_create = "python -m venv venv"
        venv_activate = "venv\\Scripts\\activate"
        pip_upgrade = "python -m pip install --upgrade pip"
        pip_install = "pip install -r requirements.txt"
        separator = " && "
    else:
        venv_create = "python3 -m venv venv"
        venv_activate = "source venv/bin/activate"
        pip_upgrade = "python -m pip install --upgrade pip"
        pip_install = "pip install -r requirements.txt"
        separator = " && "
    
    print(f"\nDirector curent: {os.getcwd()}")
    
    if not os.path.exists('requirements.txt'):
        print("[!] Fișierul requirements.txt nu exista. Se creeaza automat...")
        create_requirements_file()
    
    if os.path.exists('venv'):
        print("Sterg venv existent...")
        if os_name == "Windows":
            run_command("rmdir /s /q venv", "Stergere venv")
        else:
            run_command("rm -rf venv", "Stergere venv")
    
    if not run_command(venv_create, "Creare virtual environment"):
        return False
    
    full_command = f"{venv_activate}{separator}{pip_upgrade}{separator}{pip_install}"
    
    if not run_command(full_command, "Instalare dependente"):
        return False
    
    print("\nSETUP COMPLET!")
    print("=" * 50)
    print("Pentru a rula calculatorul:\n")
    
    if os_name == "Windows":
        print("1. Activeaza venv:\n   venv\\Scripts\\activate")
    else:
        print("1. Activeaza venv:\n   source venv/bin/activate")
    
    print("2. Ruleaza testul rapid:\n   python quick_test.py")
    print("3. Ruleaza calculatorul:\n   python security_calculator.py")
    print("4. Genereaza raport HTML:\n   python html_report_generator.py")
    print("\nAsigura-te ca fisierul CSV este in acelasi director:")
    print("   package-analysis_agl-demo-platform_raspberrypi4-64.csv")
    
    return True

def create_requirements_file():
    """Creeaza fisierul requirements.txt."""
    requirements_content = """# Dependente pentru Security Calculator
pandas>=2.0.0
numpy>=1.24.0
python-dateutil>=2.8.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.15.0
ipython>=8.0.0
setuptools>=65.0.0
wheel>=0.40.0
"""
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements_content)
    print("[V] Fișierul requirements.txt a fost creat!")

def main():
    """Functia principala."""
    try:
        success = setup_environment()
        if success:
            print("\nGata! Poti incepe sa rulezi calculatorul.")
        else:
            print("\nSetup-ul a esuat. Verifica erorile de mai sus.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nSetup intrerupt de utilizator.")
        sys.exit(1)
    except Exception as e:
        print(f"\nEroare neasteptata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
