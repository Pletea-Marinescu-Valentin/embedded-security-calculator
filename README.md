# 🔐 Etichetă de Securitate pentru Produse Embedded

Calculator de securitate pentru analiza produselor embedded, bazat pe principiile OpenSSF Criticality Score și adaptat pentru ecosistemul AGL Demo Platform.

## 📋 Descriere

Acest proiect implementează o formulă avansată pentru evaluarea securității produselor embedded prin combinarea a 4 metrici principale:

- **CVE Analysis Safety (40%)** - Analiza vulnerabilităților cunoscute
- **Code Coverage (25%)** - Acoperirea testelor de cod
- **Static Code Analysis (20%)** - Analiza statică a codului
- **Dynamic Program Analysis (15%)** - Analiza dinamică în runtime

### 🎯 Obiective

- Evaluarea obiectivă a securității pentru 4,601+ pachete software
- Generarea de scoruri de securitate standardizate (0-100)
- Identificarea pachetelor cu risc maxim
- Furnizarea de recomandări prioritizate pentru remediere

## 🚀 Instalare Rapidă

### Opțiunea 1: Script Automat (Recomandat)

**Windows:**
```bash
# Dublu-click pe setup.bat
# SAU din Command Prompt:
setup.bat
```

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

### Opțiunea 2: Manual

```bash
# 1. Creează virtual environment
python -m venv venv

# 2. Activează venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Instalează dependențele
pip install -r requirements.txt
```

## 📊 Utilizare

### 1. Test Rapid
```bash
python quick_test.py
```
Verifică rapid validitatea datelor și afișează statistici de bază.

### 2. Analiza Completă
```bash
python security_calculator.py
```
Calculează scorurile complete pentru toate pachetele și generează recomandări.

### 3. Raport HTML
```bash
python html_report_generator.py
```
Generează un raport HTML profesional cu grafice și vizualizări.

## 📁 Structura Proiectului

```
embedded-security-calculator/
├── security_calculator.py      # Calculator principal
├── quick_test.py              # Test rapid pentru verificare
├── html_report_generator.py   # Generator rapoarte HTML
├── config.json               # Configurația sistemului
├── requirements.txt          # Dependențe Python
├── setup.py                 # Script setup automat
├── setup.bat               # Setup Windows
├── setup.sh               # Setup Linux/macOS
├── README.md             # Această documentație
├── .gitignore           # Fișiere ignorate de Git
└── packageanalysis_agldemoplatform_raspberrypi464.csv  # Date AGL
```

## 🔧 Configurare

Editează `config.json` pentru a personaliza:

```json
{
    "weights": {
        "cve_analysis_safety": 0.40,
        "code_coverage": 0.25,
        "static_analysis": 0.20,
        "dynamic_analysis": 0.15
    },
    "thresholds": {
        "critical_score": 30,
        "warning_score": 60,
        "excellent_score": 90
    }
}
```

## 📈 Rezultate

### Scoruri Generate
- **Scor Global (0-100)**: Media ponderată pentru întreg sistemul
- **Note Alfabetice**: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
- **Identificare Pachete Critice**: Pachete cu scor < 30

### Outputs
- `security_analysis_YYYYMMDD_HHMMSS.json` - Rezultate complete
- `security_report_YYYYMMDD_HHMMSS.html` - Raport vizual
- `worst_packages_YYYYMMDD_HHMMSS.csv` - Top pachete problematice

## 🏆 Exemple de Rezultate

```
=== REZULTATE ANALIZA SECURITATE AGL DEMO PLATFORM ===
Scor sistem: 67.3/100 (Nota: C)
Total pachete analizate: 4,601
Pachete critice: 287
Pachete vulnerabile (CVE=0): 156
Pachete netestrate (Coverage=0): 89
```

### Top Pachete cu Risc Maxim
1. **agl-vss-helper**: CVE=0, Coverage=79
2. **abseil-cpp**: CVE=5, Coverage=82
3. **agl-shell-grpc-server**: CVE=37, Coverage=5

## 🔬 Metodologie

### Formula de Bază
```
Security_Score = (CVE_Safety × 0.4) + (Code_Coverage × 0.25) + 
                (Static_Analysis × 0.2) + (Dynamic_Analysis × 0.15)
```

### Proprietăți Bonus
- **PDCI** (Package Dependency Criticality Index)
- **TVDF** (Temporal Vulnerability Decay Factor)
- **LRA** (License Risk Assessment)
- **CIC** (Component Interaction Complexity)

## 📋 Cerințe de Sistem

- **Python**: 3.8+
- **Memorie RAM**: 2GB+ (pentru procesarea celor 4,601 pachete)
- **Spațiu disk**: 100MB pentru outputs
- **OS**: Windows 10+, Linux (Ubuntu 18.04+), macOS 10.14+

### Dependențe Python
- `pandas >= 2.0.0` - Procesarea datelor
- `numpy >= 1.24.0` - Calcule numerice
- `matplotlib >= 3.7.0` - Grafice (opțional)
- `seaborn >= 0.12.0` - Vizualizări (opțional)

### Referințe
- [OpenSSF Criticality Score](https://openssf.org/projects/criticality-score/)
- [AGL (Automotive Grade Linux)](https://www.automotivelinux.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## 🤝 Contribuții

Pentru îmbunătățiri sau bug-uri:
1. Fork proiectul
2. Creează un branch pentru feature (`git checkout -b feature/ImbunatatireNoua`)
3. Commit schimbările (`git commit -m 'Adaugă funcționalitate nouă'`)
4. Push la branch (`git push origin feature/ImbunatatireNoua`)
5. Deschide un Pull Request

## 📄 Licență

Acest proiect este dezvoltat în scopuri educaționale ca parte a unei teme universitare.

## 👤 Autor

**Valentin Pletea-Marinescu**
- Grupa: 332AB
- Email: pletea.valentin2003@gmail.com
- Universitatea Politehnica București

---

## 🔍 Quick Start

```bash
# 1. Clonează repository-ul
git clone https://github.com/Pletea-Marinescu-Valentin/embedded-security-calculator.git
cd embedded-security-calculator

# 2. Setup rapid
./setup.sh  # Linux/macOS
setup.bat   # Windows

# 3. Copiază fișierul CSV
# Copiază package-analysis_agl-demo-platform_raspberrypi4-64.csv în directorul proiectului

# 4. Rulează analiza
source venv/bin/activate  # Linux/macOS
python security_calculator.py

# 5. Vezi raportul HTML
python html_report_generator.py
```