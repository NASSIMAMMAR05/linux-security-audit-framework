#!/usr/bin/env python3
"""
Module 2: Moteur d'audit - CIS Benchmarks
"""

import os
import subprocess

def check_ssh_root():
    print("\n[CHECK] SSH Root Login")
    if os.path.exists("/etc/ssh/sshd_config"):
        result = os.popen("grep PermitRootLogin /etc/ssh/sshd_config | grep -v '^#'").read()
        if "yes" in result:
            print("❌ HIGH: Root login ENABLED")
        else:
            print("✅ OK: Root login disabled")
    else:
        print("⚠️ SSH not installed")

def check_open_ports():
    print("\n[CHECK] Open Ports")
    os.system("ss -tuln | grep -E ':(21|22|23|80|443|3306)' || echo 'No common ports'")

def check_users_without_password():
    print("\n[CHECK] Users without password")
    result = os.popen("awk -F: '($2 == \"\") {print $1}' /etc/shadow 2>/dev/null").read()
    if result:
        print(f"❌ Users with no password: {result.strip()}")
    else:
        print("✅ OK")

def check_sudoers_config():
    print("\n[CHECK] Sudoers Configuration")
    os.system("grep -E '^[^#].*NOPASSWD' /etc/sudoers /etc/sudoers.d/* 2>/dev/null || echo '✅ No NOPASSWD entries'")

def check_inactive_users():
    print("\n[CHECK] Inactive Users")
    os.system("lastlog | grep 'Never' | head -5 2>/dev/null || echo 'Command not available'")

def check_failed_logins():
    print("\n[CHECK] Failed Login Attempts")
    if os.path.exists("/var/log/auth.log"):
        os.system("grep 'Failed password' /var/log/auth.log | tail -3 2>/dev/null")

def check_running_services():
    print("\n[CHECK] Running Services")
    os.system("systemctl list-units --type=service --state=running | head -10")

def check_kernel_parameters():
    print("\n[CHECK] Kernel Parameters")
    checks = [("net.ipv4.tcp_syncookies", "SYN Flood"), ("net.ipv4.ip_forward", "IP Forward")]
    for param, desc in checks:
        result = subprocess.run(f"sysctl -n {param}", shell=True, capture_output=True, text=True)
        print(f"  {desc}: {result.stdout.strip()}")

def check_file_permissions():
    print("\n[CHECK] File Permissions")
    files = [("/etc/passwd", "644"), ("/etc/shadow", "640"), ("/etc/crontab", "600")]
    for path, expected in files:
        if os.path.exists(path):
            perms = os.popen(f"stat -c %a {path}").read().strip()
            status = "✅" if perms == expected else "❌"
            print(f"  {status} {path}: {perms} (expected {expected})")

def check_password_policies():
    print("\n[CHECK] Password Policies")
    os.system("grep -E 'PASS_MAX_DAYS|PASS_MIN_DAYS' /etc/login.defs | grep -v '^#' | head -5")

def check_firewall_status():
    print("\n[CHECK] Firewall Status")
    os.system("ufw status 2>/dev/null || echo 'UFW not installed'")
    os.system("iptables -L -n 2>/dev/null | head -5")

def check_apparmor():
    print("\n[CHECK] AppArmor")
    os.system("aa-status 2>/dev/null | head -5 || echo 'AppArmor not installed'")

def run_all():
    print("\n" + "="*60)
    print("🔒 SECURITY AUDIT")
    print("="*60)
    check_ssh_root()
    check_sudoers_config()
    check_kernel_parameters()
    check_file_permissions()
    check_users_without_password()
    check_inactive_users()
    check_failed_logins()
    check_password_policies()
    check_open_ports()
    check_running_services()
    check_firewall_status()
    check_apparmor()
    print("\n✅ Audit Complete!")

if __name__ == "__main__":
    run_all()
