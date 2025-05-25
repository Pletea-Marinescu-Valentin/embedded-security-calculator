#!/usr/bin/env python3
"""
Generator de rapoarte HTML pentru analiza de securitate.
"""

import pandas as pd
import json
from datetime import datetime
import os

class HTMLReportGenerator:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def generate_html_report(self, results, csv_file):
        """Genereaza un raport HTML complet."""
        
        html_content = f"""
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raport Securitate AGL Demo Platform</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #333;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .score-card {{
            background: #f8f9fa;
            border: 2px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
        }}
        .score-big {{
            font-size: 3em;
            font-weight: bold;
            color: #333;
        }}
        .grade {{
            font-size: 2em;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 50px;
            display: inline-block;
            margin: 10px 0;
        }}
        .grade-A {{ background: #d4edda; color: #155724; }}
        .grade-B {{ background: #d1ecf1; color: #0c5460; }}
        .grade-C {{ background: #fff3cd; color: #856404; }}
        .grade-D {{ background: #f8d7da; color: #721c24; }}
        .grade-F {{ background: #f5c6cb; color: #721c24; }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: #ffffff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }}
        .recommendations {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }}
        .critical {{ border-left: 5px solid #dc3545; }}
        .high {{ border-left: 5px solid #fd7e14; }}
        .medium {{ border-left: 5px solid #ffc107; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        .metric-bar {{
            background: #e9ecef;
            height: 20px;
            border-radius: 10px;
            margin: 5px 0;
            overflow: hidden;
        }}
        .metric-fill {{
            height: 100%;
            background: linear-gradient(90deg, #dc3545 0%, #ffc107 50%, #28a745 100%);
            transition: width 0.3s ease;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Raport Analiza Securitate</h1>
            <h2>AGL Demo Platform - Raspberry Pi 4</h2>
            <p>Generat la: {self.timestamp}</p>
        </div>
        
        <div class="score-card">
            <h2>Scor General Securitate</h2>
            <div class="score-big">{results['system_score']}/100</div>
            <div class="grade grade-{results['grade']}">{results['grade']}</div>
            <p>Scor ponderat cu criticalitate: {results['weighted_score']}/100</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{results['total_packages']:,}</div>
                <div>Total Pachete</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{results['critical_packages']}</div>
                <div>Pachete Critice</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{results['vulnerable_packages']}</div>
                <div>Pachete Vulnerabile</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{results['untested_packages']}</div>
                <div>Pachete Netestrate</div>
            </div>
        </div>
        
        <h2>Statistici Detaliate</h2>
        <table>
            <tr>
                <th>Metrica</th>
                <th>Media</th>
                <th>Minimum</th>
                <th>Maximum</th>
                <th>Deviatia Standard</th>
                <th>Distributie</th>
            </tr>
"""
        
        # Adauga statistici pentru fiecare metrica
        metrics_info = [
            ('CVE Analysis Safety', results['statistics']['cve_stats']),
            ('Code Coverage', results['statistics']['coverage_stats']),
            ('Static Analysis', results['statistics']['static_analysis_stats']),
            ('Dynamic Analysis', results['statistics']['dynamic_analysis_stats'])
        ]
        
        for metric_name, stats in metrics_info:
            mean_val = stats['mean']
            bar_width = mean_val  # Folosim media pentru latimea barei
            
            html_content += f"""
            <tr>
                <td><strong>{metric_name}</strong></td>
                <td>{stats['mean']}</td>
                <td>{stats.get('min', 'N/A')}</td>
                <td>{stats.get('max', 'N/A')}</td>
                <td>{stats['std']}</td>
                <td>
                    <div class="metric-bar">
                        <div class="metric-fill" style="width: {bar_width}%"></div>
                    </div>
                </td>
            </tr>
            """
        
        html_content += """
        </table>
        
        <h2>Recomandări Prioritizate</h2>
        """
        
        # Adauga recomandari
        priority_classes = {
            'CRITICA': 'critical',
            'RIDICATA': 'high', 
            'MEDIE': 'medium'
        }
        
        for i, rec in enumerate(results['recommendations'], 1):
            priority_class = priority_classes.get(rec['priority'], 'medium')
            html_content += f"""
        <div class="recommendations {priority_class}">
            <h3>{i}. Prioritate {rec['priority']}</h3>
            <p><strong>Acțiune:</strong> {rec['action']}</p>
            <p><strong>Impact:</strong> {rec['impact']}</p>
        </div>
            """
        
        # Adauga tabel cu pachetele problematice
        if not results['worst_packages'].empty:
            html_content += """
        <h2>Top 10 Pachete cu Risc Maxim</h2>
        <table>
            <tr>
                <th>Pachet</th>
                <th>Versiune</th>
                <th>Scor Total</th>
                <th>CVE Safety</th>
                <th>Code Coverage</th>
                <th>Static Analysis</th>
                <th>Dynamic Analysis</th>
            </tr>
            """
            
            for _, row in results['worst_packages'].head(10).iterrows():
                html_content += f"""
            <tr>
                <td><strong>{row['Package Name']}</strong></td>
                <td>{row['Package Version']}</td>
                <td>{row['Package_Score']:.1f}</td>
                <td>{row['CVE Analysis Safety']}</td>
                <td>{row['Code Coverage']}</td>
                <td>{row['Static Code Analysis Status']}</td>
                <td>{row['Dynamic Program Analysis Status']}</td>
            </tr>
                """
            
            html_content += "</table>"
        
        # Footer
        html_content += f"""
        <div class="footer">
            <p>Raport generat de Security Calculator v1.0</p>
            <p>Bazat pe analiza {results['total_packages']:,} pachete din {csv_file}</p>
            <p>Formula adaptată din OpenSSF Criticality Score pentru embedded security</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Salveaza fisierul HTML
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"security_report_{timestamp}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Raport HTML generat: {filename}")
        return filename

def main():
    """Genereaza raport HTML din rezultatele JSON existente."""
    
    # Cauta cel mai recent fisier JSON
    json_files = [f for f in os.listdir('.') if f.startswith('security_analysis_') and f.endswith('.json')]
    
    if not json_files:
        print("Nu am gasit fisiere JSON cu rezultate!")
        print("Ruleaza mai intai 'python security_calculator.py'")
        return
    
    # Ia cel mai recent fisier
    latest_json = sorted(json_files)[-1]
    print(f"Folosesc fisierul: {latest_json}")
    
    try:
        with open(latest_json, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        # Converteste worst_packages inapoi in DataFrame pentru procesare
        if 'worst_packages' in results and results['worst_packages']:
            results['worst_packages'] = pd.DataFrame(results['worst_packages'])
        else:
            results['worst_packages'] = pd.DataFrame()
        
        # Genereaza raportul HTML
        generator = HTMLReportGenerator()
        html_file = generator.generate_html_report(results, 'package-analysis_agl-demo-platform_raspberrypi4-64.csv')
        
        print(f"✓ Raport HTML generat cu succes!")
        print(f"✓ Deschide fisierul '{html_file}' in browser pentru vizualizare.")
        
    except Exception as e:
        print(f"Eroare la generarea raportului HTML: {e}")

if __name__ == "__main__":
    main()