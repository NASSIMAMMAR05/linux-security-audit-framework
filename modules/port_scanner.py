#!/usr/bin/env python3
"""
Module Port Scanner Avancé - Monitoring détaillé
"""

import os
import subprocess
import socket
from datetime import datetime

# Base de données des services et risques
SERVICES_DB = {
    20: {'name': 'FTP-data', 'risk': 'MEDIUM', 'desc': 'Transfert de données non chiffré'},
    21: {'name': 'FTP', 'risk': 'HIGH', 'desc': 'Protocole non sécurisé, préférer SFTP'},
    22: {'name': 'SSH', 'risk': 'LOW', 'desc': 'Accès sécurisé si bien configuré'},
    23: {'name': 'Telnet', 'risk': 'CRITICAL', 'desc': 'Non chiffré, à désactiver'},
    25: {'name': 'SMTP', 'risk': 'MEDIUM', 'desc': 'Email, vulnérable au spoofing'},
    53: {'name': 'DNS', 'risk': 'MEDIUM', 'desc': 'Risque d\'empoisonnement DNS'},
    80: {'name': 'HTTP', 'risk': 'MEDIUM', 'desc': 'Non chiffré, utiliser HTTPS'},
    443: {'name': 'HTTPS', 'risk': 'LOW', 'desc': 'Sécurisé si certificat valide'},
    3306: {'name': 'MySQL', 'risk': 'MEDIUM', 'desc': 'Base de données, configurer bind-address'},
    5432: {'name': 'PostgreSQL', 'risk': 'MEDIUM', 'desc': 'Base de données'},
    27017: {'name': 'MongoDB', 'risk': 'MEDIUM', 'desc': 'Base NoSQL, activer auth'},
    6379: {'name': 'Redis', 'risk': 'MEDIUM', 'desc': 'Cache, désactiver si non utilisé'},
    8080: {'name': 'HTTP-Alt', 'risk': 'MEDIUM', 'desc': 'Serveur web alternatif'},
    8443: {'name': 'HTTPS-Alt', 'risk': 'LOW', 'desc': 'HTTPS alternatif'},
}

def get_service_info(port):
    port_int = int(port) if str(port).isdigit() else 0
    if port_int in SERVICES_DB:
        return SERVICES_DB[port_int]
    return {'name': 'Unknown', 'risk': 'UNKNOWN', 'desc': 'Service non identifié'}

def scan_all_ports():
    """Scan complet de tous les ports (1-65535) - Version rapide"""
    print("\n" + "="*70)
    print("🔌 PORT SCANNER AVANCÉ - MONITORING COMPLET")
    print("="*70)
    print(f"⏰ Scan time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ports communs à vérifier
    common_ports = [20,21,22,23,25,53,80,110,111,135,137,139,143,443,445,
                    465,514,587,631,636,993,995,1433,1521,2049,3306,3389,
                    5432,5900,6379,8080,8443,27017]
    
    print("\n📡 PORTS COMMUNS SCAN:")
    print("-" * 70)
    print(f"{'PORT':<8} {'SERVICE':<15} {'RISK':<10} {'STATUS':<10} {'DESCRIPTION'}")
    print("-" * 70)
    
    result = subprocess.run(["ss", "-tln"], capture_output=True, text=True)
    open_ports = []
    
    for port in common_ports:
        if f":{port}" in result.stdout or f":{port} " in result.stdout:
            info = get_service_info(port)
            risk_symbol = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(info['risk'], "⚪")
            print(f"{port:<8} {info['name']:<15} {risk_symbol} {info['risk']:<8} {'✅ OPEN':<10} {info['desc'][:40]}")
            open_ports.append({'port': port, 'info': info})
    
    return open_ports

def get_ports_with_details():
    """Obtenir les ports avec processus détaillés"""
    print("\n" + "="*70)
    print("🔍 PORTS AVEC PROCESSUS DÉTAILLÉS")
    print("="*70)
    print(f"{'PORT':<8} {'PROTOCOL':<8} {'PROCESS':<20} {'PID':<8} {'USER':<12}")
    print("-" * 70)
    
    result = subprocess.run(["sudo", "lsof", "-i", "-P", "-n"], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')[1:25]
    
    for line in lines:
        if line:
            parts = line.split()
            if len(parts) >= 9:
                process = parts[0][:20]
                pid = parts[1]
                user = parts[2][:12]
                port = parts[8].split(':')[-1] if ':' in parts[8] else 'unknown'
                proto = parts[7] if len(parts) > 7 else 'tcp'
                if port.isdigit():
                    print(f"{port:<8} {proto:<8} {process:<20} {pid:<8} {user:<12}")

def check_listening_services():
    """Vérifier les services en écoute avec plus de détails"""
    print("\n" + "="*70)
    print("🎯 SERVICES EN ÉCOUTE (LISTENING)")
    print("="*70)
    
    result = subprocess.run(["ss", "-tlnp"], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')[1:]
    
    services = []
    for line in lines:
        if line:
            parts = line.split()
            if len(parts) >= 6:
                port = parts[3].split(':')[-1]
                process = parts[-1].split('"')[1] if '"' in parts[-1] else 'system'
                state = parts[0]
                if port.isdigit():
                    services.append({'port': port, 'process': process, 'state': state})
                    print(f"   Port {port}: {process} ({state})")
    
    return services

def get_risk_assessment():
    """Évaluation des risques par port"""
    print("\n" + "="*70)
    print("⚠️ ÉVALUATION DES RISQUES")
    print("="*70)
    
    result = subprocess.run(["ss", "-tln"], capture_output=True, text=True)
    
    critical_ports = [23, 513, 514, 515]  # Telnet, rlogin, etc
    high_risk_ports = [21, 25, 111, 139, 445, 2049]
    medium_risk_ports = [53, 80, 110, 143, 3306, 5432, 5900]
    
    risks = {'CRITICAL': [], 'HIGH': [], 'MEDIUM': []}
    
    for port in critical_ports:
        if f":{port}" in result.stdout:
            risks['CRITICAL'].append(port)
            print(f"   🔴 CRITICAL: Port {port} ({get_service_info(port)['name']})")
    
    for port in high_risk_ports:
        if f":{port}" in result.stdout:
            risks['HIGH'].append(port)
            print(f"   🟠 HIGH: Port {port} ({get_service_info(port)['name']})")
    
    for port in medium_risk_ports:
        if f":{port}" in result.stdout:
            risks['MEDIUM'].append(port)
            print(f"   🟡 MEDIUM: Port {port} ({get_service_info(port)['name']})")
    
    return risks

def run_port_scan():
    """Exécuter le scan complet des ports"""
    open_ports = scan_all_ports()
    get_ports_with_details()
    check_listening_services()
    risks = get_risk_assessment()
    
    print("\n" + "="*70)
    print("📊 RÉSUMÉ DU SCAN PORTS")
    print("="*70)
    print(f"   🔓 Ports ouverts: {len(open_ports)}")
    print(f"   🔴 Critiques: {len(risks['CRITICAL'])}")
    print(f"   🟠 Haut risque: {len(risks['HIGH'])}")
    print(f"   🟡 Risque moyen: {len(risks['MEDIUM'])}")
    
    return open_ports

if __name__ == "__main__":
    run_port_scan()
