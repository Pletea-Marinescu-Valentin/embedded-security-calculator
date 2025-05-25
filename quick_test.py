#!/usr/bin/env python3
"""
Script de test rapid pentru verificarea datelor AGL Demo Platform.
"""

import pandas as pd
import numpy as np
import os

def quick_analysis():
    """Analiza rapida a datelor pentru verificare."""
    csv_file = 'package-analysis_agl-demo-platform_raspberrypi4-64.csv'
    
    print("=== TEST RAPID ANALIZA AGL DEMO PLATFORM ===")
    print()
    
    # Verifica fisierul
    if not os.path.exists(csv_file):
        print(f"EROARE: Fisierul {csv_file} nu a fost gasit!")
        print("Te rog sa copiezi fisierul CSV in acelasi director.")
        return
    
    try:
        # Incarca datele
        print(f"Incarcam datele din {csv_file}...")
        df = pd.read_csv(csv_file)
        
        print(f"✓ Fisier incarcat cu succes!")
        print(f"✓ Dimensiuni: {df.shape[0]:,} pachete, {df.shape[1]} coloane")
        
        # Verifica coloanele
        print(f"\n=== STRUCTURA DATELOR ===")
        print("Coloane disponibile:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        # Statistici rapide
        print(f"\n=== STATISTICI RAPIDE ===")
        
        metrics = ['CVE Analysis Safety', 'Code Coverage', 
                    'Static Code Analysis Status', 'Dynamic Program Analysis Status']
        
        for metric in metrics:
            if metric in df.columns:
                values = df[metric]
                print(f"\n{metric}:")
                print(f"  Min: {values.min()}, Max: {values.max()}")
                print(f"  Media: {values.mean():.1f}, Mediana: {values.median():.1f}")
                print(f"  Valori = 0: {(values == 0).sum()}")
                print(f"  Valori > 80: {(values > 80).sum()}")
        
        # Calculare scor simplu
        print(f"\n=== CALCUL SCOR SIMPLU ===")
        
        # Formula simplificata
        df['Simple_Score'] = (
            df['CVE Analysis Safety'] * 0.4 +
            df['Code Coverage'] * 0.25 +
            df['Static Code Analysis Status'] * 0.2 +
            df['Dynamic Program Analysis Status'] * 0.15
        )
        
        scor_sistem = df['Simple_Score'].mean()
        
        print(f"Scor sistem calculat: {scor_sistem:.1f}/100")
        
        if scor_sistem >= 90:
            nota = 'A'
        elif scor_sistem >= 80:
            nota = 'B'
        elif scor_sistem >= 70:
            nota = 'C'
        elif scor_sistem >= 60:
            nota = 'D'
        else:
            nota = 'F'
        
        print(f"Nota: {nota}")
        
        # Pachete problematice
        critice = df[df['Simple_Score'] < 30]
        vulnerabile = df[df['CVE Analysis Safety'] == 0]
        netestrate = df[df['Code Coverage'] == 0]
        
        print(f"\n=== PACHETE PROBLEMATICE ===")
        print(f"Pachete critice (scor < 30): {len(critice)}")
        print(f"Pachete vulnerabile (CVE = 0): {len(vulnerabile)}")
        print(f"Pachete netestrate (Coverage = 0): {len(netestrate)}")
        
        # Top 5 cele mai rau
        print(f"\n=== TOP 5 PACHETE CU RISC MAXIM ===")
        worst = df.nsmallest(5, 'Simple_Score')
        for i, (_, row) in enumerate(worst.iterrows(), 1):
            print(f"{i}. {row['Package Name']}")
            print(f"   Scor: {row['Simple_Score']:.1f}")
            print(f"   CVE: {row['CVE Analysis Safety']}, Coverage: {row['Code Coverage']}")
            print(f"   Static: {row['Static Code Analysis Status']}, Dynamic: {row['Dynamic Program Analysis Status']}")
        
        # Top 5 cele mai bune
        print(f"\n=== TOP 5 PACHETE CU SCOR MAXIM ===")
        best = df.nlargest(5, 'Simple_Score')
        for i, (_, row) in enumerate(best.iterrows(), 1):
            print(f"{i}. {row['Package Name']}")
            print(f"   Scor: {row['Simple_Score']:.1f}")
        
        print(f"\n✓ Analiza rapida finalizata cu succes!")
        print(f"Poti rula acum 'python security_calculator.py' pentru analiza completa.")
        
    except Exception as e:
        print(f"EROARE la procesarea fisierului: {e}")
        print("Verifica ca fisierul CSV este valid si are structura corecta.")

if __name__ == "__main__":
    quick_analysis()