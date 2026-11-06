#!/usr/bin/env python3
"""
Module 1: Collecte d'informations
- Version OS
- Packages installés
- Utilisateurs
- Services
- Ports
"""

import os
import subprocess
import platform

def collect_os_info():
    print("\n[Module 1 - Collecte d'informations]")
    print("=" * 50)
    print("1.1 Version OS:")
    
    os_info = platform.uname()
    print(f"   Système: {os_info.system}")
    print(f"   Nom d'hôte: {os_info.node}")
    print(f"   Version: {os_info.release}")
    print(f"   Architecture: {os_info.machine}")
    
    if os.path.exists("/etc/os-release"):
        result = subprocess.run(["cat", "/etc/os-release"], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if "PRETTY_NAME" in line:
                print(f"   Distribution: {line.split('=')[1].strip('\"')}")

def collect_packages():
    print("\n1.2 Packages installés:")
    if os.path.exists("/usr/bin/dpkg"):
        result = subprocess.run(["dpkg-query", "-W", "-f=${Package}\n"], capture_output=True, text=True)
        packages = result.stdout.strip().split('\n')
        print(f"   Nombre total de packages: {len(packages)}")
        print(f"   Exemple: {', '.join(packages[:5])}")

def collect_users():
    print("\n1.3 Utilisateurs:")
    with open("/etc/passwd", "r") as f:
        users = f.readlines()
    regular_users = []
    for user in users:
        username = user.split(':')[0]
        uid = int(user.split(':')[2])
        if uid >= 1000 and uid < 65534:
            regular_users.append(username)
    print(f"   Utilisateurs réguliers: {len(regular_users)}")
    print(f"   Liste: {', '.join(regular_users[:5])}")

def collect_services():
    print("\n1.4 Services actifs:")
    result = subprocess.run(["systemctl", "list-units", "--type=service", "--state=running", "--no-pager"], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    services = []
    for line in lines[1:]:
        if line and not line.startswith('UNIT'):
            parts = line.split()
            if parts:
                services.append(parts[0])
    print(f"   Nombre de services actifs: {len(services)}")
    print(f"   Principaux: {', '.join(services[:10])}")

def collect_ports():
    print("\n1.5 Ports ouverts:")
    result = subprocess.run(["ss", "-tuln"], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')[1:]
    ports = []
    for line in lines:
        if line:
            parts = line.split()
            if len(parts) >= 5:
                port = parts[4].split(':')[-1]
                if port.isdigit():
                    ports.append(port)
    unique_ports = sorted(set(ports))
    print(f"   Ports ouverts: {', '.join(unique_ports[:15])}")

def run_collector():
    collect_os_info()
    collect_packages()
    collect_users()
    collect_services()
    collect_ports()
    return True

if __name__ == "__main__":
    run_collector()
