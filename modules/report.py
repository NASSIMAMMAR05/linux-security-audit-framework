#!/usr/bin/env python3
"""
Module 5: Génération de rapports HTML
"""

import os
from datetime import datetime

def generate_html_report(findings, cve_results, score_result):
    """Generate HTML report"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname = os.popen("hostname").read().strip()
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Linux Security Audit Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }}
        .score-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
        }}
        .score {{
            font-size: 48px;
            font-weight: bold;
        }}
        .finding {{
            border-left: 4px solid;
            margin: 10px 0;
            padding: 10px;
            background: #f9f9f9;
        }}
        .CRITICAL {{ border-color: #dc3545; }}
        .HIGH {{ border-color: #fd7e14; }}
        .MEDIUM {{ border-color: #ffc107; }}
        .LOW {{ border-color: #28a745; }}
        .severity-badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 10px;
        }}
        .severity-CRITICAL {{ background: #dc3545; color: white; }}
        .severity-HIGH {{ background: #fd7e14; color: white; }}
        .severity-MEDIUM {{ background: #ffc107; color: black; }}
        .severity-LOW {{ background: #28a745; color: white; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 10px;
            border: 1px solid #ddd;
            text-align: left;
        }}
        th {{
            background-color: #007bff;
            color: white;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #777;
        }}
        .fix-code {{
            background: #f4f4f4;
            padding: 5px 10px;
            border-radius: 3px;
            font-family: monospace;
            font-size: 12px;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 Linux Security Audit Report</h1>
        <p><strong>Hostname:</strong> {hostname}</p>
        <p><strong>Date:</strong> {timestamp}</p>
        
        <div class="score-box">
            <div class="score">Security Score: {score_result['score']}/100</div>
            <div>Grade: {score_result['grade']}</div>
        </div>
        
        <h2>📊 Audit Summary</h2>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Total Findings</td><td>{len(findings)}</td></tr>
            <tr><td>Vulnerabilities Found</td><td>{len(cve_results) if cve_results else 0}</td></tr>
            <tr><td>Penalty Points</td><td>{score_result['penalty']}</td></tr>
        </table>
        
        <h2>⚠️ Security Findings</h2>
"""
    
    if findings:
        for finding in findings:
            severity = finding.get('severity', 'LOW')
            html_content += f"""
        <div class="finding {severity}">
            <span class="severity-badge severity-{severity}">{severity}</span>
            <strong>{finding.get('title', 'Issue')}</strong>
            <p>{finding.get('description', 'Security issue detected')}</p>
            <div class="fix-code">🔧 Fix: {finding.get('fix', 'No fix provided')}</div>
        </div>
"""
    else:
        html_content += "<p>✅ No security issues found!</p>"
    
    if cve_results:
        html_content += """
        <h2>🐛 CVE Vulnerabilities</h2>
        <table>
            <tr><th>Package</th><th>CVEs Found</th><th>Severity</th></tr>
"""
        for cve in cve_results:
            html_content += f"""
            <tr>
                <td>{cve.get('package', 'Unknown')}</td>
                <td>{cve.get('count', 0)}</td>
                <td>{cve.get('severity', 'MEDIUM')}</td>
            </tr>
"""
        html_content += "</table>"
    
    html_content += f"""
        <h2>📋 Recommendations</h2>
        <ul>
            <li>Enable firewall: <code>sudo ufw enable</code></li>
            <li>Fix crontab permissions: <code>sudo chmod 600 /etc/crontab</code></li>
            <li>Regular system updates: <code>sudo apt update && sudo apt upgrade</code></li>
            <li>Install security tools: <code>sudo apt install rkhunter chkrootkit lynis</code></li>
        </ul>
        
        <div class="footer">
            <p>Generated by Linux Security Audit Framework | PFA Project 2025-2026</p>
            <p>Author: Nassim Ammar | Domain: Pentest & Audit Interne</p>
        </div>
    </div>
</body>
</html>
"""
    
    os.makedirs("reports", exist_ok=True)
    report_path = f"reports/audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(report_path, 'w') as f:
        f.write(html_content)
    
    print(f"\n✅ HTML Report generated: {report_path}")
    return report_path

if __name__ == "__main__":
    test_findings = [{'title': 'Test', 'severity': 'HIGH', 'fix': 'sudo fix', 'description': 'Test'}]
    generate_html_report(test_findings, [], {'score': 50, 'grade': 'D', 'penalty': 50})
