#!/usr/bin/env python3
"""
Script de setup automat pentru Security Calculator.
Creează venv și instalează dependențele.
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Rulează o comandă și afișează progresul."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} - Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Verifică versiunea Python."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ este necesar!")
        print(f"Versiunea ta: Python {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK!")
    return True

def setup_environment():
    """Configurează mediul de dezvoltare."""
    print("🚀 SETUP SECURITY CALCULATOR")
    print("=" * 50)
    
    # Verifică Python
    if not check_python_version():
        return False
    
    # Detectează OS
    os_name = platform.system()
    print(f"🖥️  Sistem de operare: {os_name}")
    
    # Comenzi pentru venv
    if os_name == "Windows":
        venv_create = "python -m venv venv"
        venv_activate = "venv\\Scripts\\activate"
        pip_upgrade = "python -m pip install --upgrade pip"
        pip_install = "pip install -r requirements.txt"
        separator = " && "
    else:  # Linux/macOS
        venv_create = "python3 -m venv venv"
        venv_activate = "source venv/bin/activate"
        pip_upgrade = "python -m pip install --upgrade pip"
        pip_install = "pip install -r requirements.txt"
        separator = " && "
    
    print(f"\n📁 Director curent: {os.getcwd()}")
    
    # Verifică dacă requirements.txt există
    if not os.path.exists('requirements.txt'):
        print("❌ Fișierul requirements.txt nu există!")
        print("Creez fișierul requirements.txt...")
        create_requirements_file()
    
    # Șterge venv existent dacă există
    if os.path.exists('venv'):
        print("🗑️  Șterg venv existent...")
        if os_name == "Windows":
            run_command("rmdir /s /q venv", "Ștergere venv")
        else:
            run_command("rm -rf venv", "Ștergere venv")
    
    # Creează venv nou
    if not run_command(venv_create, "Creare virtual environment"):
        return False
    
    # Comando completă pentru instalare
    full_command = f"{venv_activate}{separator}{pip_upgrade}{separator}{pip_install}"
    
    if not run_command(full_command, "Upgrade pip și instalare dependențe"):
        return False
    
    print("\n🎉 SETUP COMPLET!")
    print("=" * 50)
    print("Pentru a rula calculatorul:")
    print()
    
    if os_name == "Windows":
        print("1. Activează venv:")
        print("   venv\\Scripts\\activate")
        print()
        print("2. Rulează testul rapid:")
        print("   python quick_test.py")
        print()
        print("3. Rulează calculatorul complet:")
        print("   python security_calculator.py")
        print()
        print("4. Generează raport HTML:")
        print("   python html_report_generator.py")
    else:
        print("1. Activează venv:")
        print("   source venv/bin/activate")
        print()
        print("2. Rulează testul rapid:")
        print("   python quick_test.py")
        print()
        print("3. Rulează calculatorul complet:")
        print("   python security_calculator.py")
        print()
        print("4. Generează raport HTML:")
        print("   python html_report_generator.py")
    
    print()
    print("📁 Asigură-te că ai fișierul CSV în același director:")
    print("   package-analysis_agl-demo-platform_raspberrypi4-64.csv")
    
    return True

def create_requirements_file():
    """Creează fișierul requirements.txt dacă nu există."""
    requirements_content = """# Dependențe pentru Security Calculator - AGL Demo Platform Analysis
# Core data processing
pandas>=2.0.0
numpy>=1.24.0

# Logging și configurare
python-dateutil>=2.8.0

# Optional: Pentru analize mai avansate (dacă vrei să extinzi)
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.15.0

# Pentru debugging și development
ipython>=8.0.0

# Asigurare compatibilitate
setuptools>=65.0.0
wheel>=0.40.0
"""
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements_content)
    
    print("✅ Fișierul requirements.txt a fost creat!")

def main():
    """Funcția principală."""
    try:
        success = setup_environment()
        if success:
            print("\n🚀 Gata! Poți începe să rulezi calculatorul!")
        else:
            print("\n❌ Setup-ul a întâmpinat erori. Verifică mesajele de mai sus.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup întrerupt de utilizator.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Eroare neașteptată: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()