#!/usr/bin/env python3
"""
Script pentru calcularea scorului de securitate pentru produse embedded.
Bazat pe principiile OpenSSF Criticality Score, adaptat pentru embedded security.
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
import logging
import os

class EmbeddedSecurityCalculator:
    def __init__(self, config_file='config.json'):
        """Initializeaza calculatorul cu configuratia specificata."""
        self.load_config(config_file)
        self.setup_logging()
        
    def load_config(self, config_file):
        """Incarca configuratia din fisierul JSON."""
        try:
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"Fisierul {config_file} nu a fost gasit. Folosesc configuratia implicita.")
            # Configuratie implicita
            self.config = {
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
    
    def setup_logging(self):
        """Configureaza logging-ul pentru auditabilitate."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('security_calculation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def calculate_package_score(self, package_data):
        """Calculeaza scorul de securitate pentru un pachet individual."""
        weights = self.config["weights"]
        
        score = (
            package_data['CVE Analysis Safety'] * weights['cve_analysis_safety'] +
            package_data['Code Coverage'] * weights['code_coverage'] +
            package_data['Static Code Analysis Status'] * weights['static_analysis'] +
            package_data['Dynamic Program Analysis Status'] * weights['dynamic_analysis']
        )
        
        return min(100, max(0, score))
    
    def calculate_system_score(self, csv_file):
        """Calculeaza scorul de securitate pentru intregul sistem."""
        self.logger.info(f"Incepe calculul pentru {csv_file}")
        
        try:
            df = pd.read_csv(csv_file)
            self.logger.info(f"Incarcat {len(df)} pachete pentru analiza")
        except Exception as e:
            self.logger.error(f"Eroare la incarcarea fisierului: {e}")
            return None
        
        # Calcularea scorului pentru fiecare pachet
        df['Package_Score'] = df.apply(
            lambda row: self.calculate_package_score(row.to_dict()), 
            axis=1
        )
        
        # Calcularea scorului global al sistemului
        system_score = df['Package_Score'].mean()
        
        # Identificarea pachetelor critice
        critical_packages = df[df['Package_Score'] < self.config["thresholds"]["critical_score"]]
        vulnerable_packages = df[df['CVE Analysis Safety'] == 0]
        untested_packages = df[df['Code Coverage'] == 0]
        
        results = {
            'system_score': round(system_score, 1),
            'total_packages': len(df),
            'critical_packages': len(critical_packages),
            'vulnerable_packages': len(vulnerable_packages),
            'untested_packages': len(untested_packages),
            'worst_packages': critical_packages.nsmallest(10, 'Package_Score'),
            'statistics': self.calculate_statistics(df),
            'recommendations': self.generate_recommendations(df),
            'grade': self.calculate_grade(system_score)
        }
        
        self.logger.info(f"Calculul finalizat: Scor sistem = {results['system_score']}")
        return results
    
    def calculate_statistics(self, df):
        """Calculeaza statistici descriptive."""
        return {
            'cve_stats': {
                'mean': round(df['CVE Analysis Safety'].mean(), 1),
                'std': round(df['CVE Analysis Safety'].std(), 1),
                'min': df['CVE Analysis Safety'].min(),
                'max': df['CVE Analysis Safety'].max()
            },
            'coverage_stats': {
                'mean': round(df['Code Coverage'].mean(), 1),
                'std': round(df['Code Coverage'].std(), 1),
                'min': df['Code Coverage'].min(),
                'max': df['Code Coverage'].max()
            },
            'static_analysis_stats': {
                'mean': round(df['Static Code Analysis Status'].mean(), 1),
                'std': round(df['Static Code Analysis Status'].std(), 1)
            },
            'dynamic_analysis_stats': {
                'mean': round(df['Dynamic Program Analysis Status'].mean(), 1),
                'std': round(df['Dynamic Program Analysis Status'].std(), 1)
            }
        }
    
    def calculate_grade(self, score):
        """Calculeaza nota alfabetica bazata pe scor."""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def generate_recommendations(self, df):
        """Genereaza recomandari bazate pe analiza datelor."""
        recommendations = []
        
        vulnerable_count = len(df[df['CVE Analysis Safety'] == 0])
        if vulnerable_count > 0:
            recommendations.append({
                'priority': 'CRITICA',
                'action': f'Remediati imediat {vulnerable_count} pachete cu CVE Score = 0',
                'impact': 'Risc maxim de securitate'
            })
        
        low_coverage = len(df[df['Code Coverage'] < 50])
        if low_coverage > 0:
            recommendations.append({
                'priority': 'RIDICATA',
                'action': f'Imbunatatiti testarea pentru {low_coverage} pachete cu coverage < 50%',
                'impact': 'Reducerea riscului de vulnerabilitati nedetectate'
            })
        
        low_static = len(df[df['Static Code Analysis Status'] < 40])
        if low_static > 0:
            recommendations.append({
                'priority': 'MEDIE',
                'action': f'Imbunatatiti analiza statica pentru {low_static} pachete',
                'impact': 'Detectarea preventiva a problemelor de cod'
            })
        
        return recommendations
    
    def export_results(self, results, format='json'):
        """Exporta rezultatele in formatul specificat."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format.lower() == 'json':
            filename = f"security_analysis_{timestamp}.json"
            results_copy = results.copy()
            
            # Converteste DataFrame-urile in dictionare pentru serializare JSON
            if 'worst_packages' in results_copy:
                results_copy['worst_packages'] = results_copy['worst_packages'].to_dict('records')
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results_copy, f, indent=2, default=str, ensure_ascii=False)
            
            print(f"Rezultatele au fost exportate in {filename}")
            return filename
        
        elif format.lower() == 'csv':
            if 'worst_packages' in results:
                filename = f"worst_packages_{timestamp}.csv"
                results['worst_packages'].to_csv(filename, index=False, encoding='utf-8')
                print(f"Pachetele cu risc maxim exportate in {filename}")
                return filename

def main():
    """Functia principala pentru rularea calculatorului."""
    print("=== Calculator Securitate Embedded ===")
    print()
    
    # Initializare calculator
    calculator = EmbeddedSecurityCalculator()
    
    # Nume fisier CSV real
    csv_file = 'package-analysis_agl-demo-platform_raspberrypi4-64.csv'
    
    # Verifica daca fisierul CSV exista
    if not os.path.exists(csv_file):
        print(f"EROARE: Fisierul {csv_file} nu a fost gasit!")
        print("Te rog sa copiezi fisierul CSV in acelasi director cu scriptul.")
        return
    
    print(f"Gasit fisierul: {csv_file}")
    print("Incep analiza datelor reale AGL Demo Platform...")
    
    # Calculeaza scorul
    results = calculator.calculate_system_score(csv_file)
    
    if results:
        print("\n" + "="*50)
        print("REZULTATE ANALIZA SECURITATE AGL DEMO PLATFORM")
        print("="*50)
        print(f"Scor sistem: {results['system_score']}/100 (Nota: {results['grade']})")
        print(f"Total pachete analizate: {results['total_packages']:,}")
        print(f"Pachete critice (scor < 30): {results['critical_packages']}")
        print(f"Pachete vulnerabile (CVE=0): {results['vulnerable_packages']}")
        print(f"Pachete netestrate (Coverage=0): {results['untested_packages']}")
        
        print(f"\n=== STATISTICI DETALIATE ===")
        print("CVE Analysis Safety:")
        stats = results['statistics']['cve_stats']
        print(f"  Media: {stats['mean']}, Min: {stats['min']}, Max: {stats['max']}, Std: {stats['std']}")
        
        print("Code Coverage:")
        stats = results['statistics']['coverage_stats']
        print(f"  Media: {stats['mean']}, Min: {stats['min']}, Max: {stats['max']}, Std: {stats['std']}")
        
        print("Static Code Analysis:")
        stats = results['statistics']['static_analysis_stats']
        print(f"  Media: {stats['mean']}, Std: {stats['std']}")
        
        print("Dynamic Program Analysis:")
        stats = results['statistics']['dynamic_analysis_stats']
        print(f"  Media: {stats['mean']}, Std: {stats['std']}")
        
        print(f"\n=== RECOMANDARI PRIORITIZATE ===")
        for i, rec in enumerate(results['recommendations'], 1):
            print(f"{i}. [{rec['priority']}] {rec['action']}")
            print(f"   Impact: {rec['impact']}")
        
        print(f"\n=== TOP 5 CELE MAI RISCANTE PACHETE ===")
        if not results['worst_packages'].empty:
            for idx, (_, row) in enumerate(results['worst_packages'].head().iterrows(), 1):
                print(f"{idx}. {row['Package Name']}")
                print(f"   Scor: {row['Package_Score']:.1f}, CVE: {row['CVE Analysis Safety']}, Coverage: {row['Code Coverage']}")
        
        # Exporta rezultatele
        print(f"\n=== EXPORT REZULTATE ===")
        json_file = calculator.export_results(results, 'json')
        csv_file_export = calculator.export_results(results, 'csv')
        
        print(f"\nAnaliza completa! Fisiere generate:")
        print(f"- Raport complet JSON: {json_file}")
        if csv_file_export:
            print(f"- Pachete riscante CSV: {csv_file_export}")
        
        print(f"\nConcluzie: Sistemul AGL Demo Platform are un scor de {results['system_score']}/100")
        print(f"Aceasta corespunde unei note {results['grade']} - {'Excelent' if results['grade'] == 'A' else 'Bun' if results['grade'] == 'B' else 'Satisfacator' if results['grade'] == 'C' else 'Marginal' if results['grade'] == 'D' else 'Nesatisfacator'}")
    else:
        print("Eroare la calcularea scorurilor!")

if __name__ == "__main__":
    main()