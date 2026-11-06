#!/usr/bin/env python3
"""
Module 2 (Avancé): Vérifications supplémentaires
"""

import os
import subprocess

def check_cis_benchmarks():
    print("\n[CHECK] CIS Benchmark Checks")
    print("-" * 40)
    print("1.1 Separate partitions:")
    os.system("mount | grep -E '/var|/tmp|/home' || echo 'Missing partitions'")
    print("\n1.2 Core dumps:")
    os.system("grep -E 'hard core' /etc/security/limits.conf 2>/dev/null || echo 'Not configured'")

def check_database_security():
    print("\n[CHECK] Database Security")
    print("-" * 40)
    if os.path.exists("/etc/mysql/my.cnf"):
        os.system("grep -E 'bind-address' /etc/mysql/my.cnf 2>/dev/null | grep -v '^#'")

def check_webserver_security():
    print("\n[CHECK] Web Server Security")
    print("-" * 40)
    if os.path.exists("/etc/apache2"):
        os.system("grep -E 'ServerTokens|ServerSignature' /etc/apache2/conf-enabled/security.conf 2>/dev/null")
    if os.path.exists("/etc/nginx"):
        os.system("grep -E 'server_tokens' /etc/nginx/nginx.conf 2>/dev/null")

def check_network_security():
    print("\n[CHECK] Network Security")
    print("-" * 40)
    os.system("sysctl net.ipv4.ip_forward")
    os.system("sysctl net.ipv6.conf.all.disable_ipv6")

def check_malware_scanners():
    print("\n[CHECK] Security Tools")
    print("-" * 40)
    tools = ['clamav', 'rkhunter', 'chkrootkit', 'lynis']
    for tool in tools:
        result = subprocess.run(f"which {tool}", shell=True, capture_output=True)
        if result.returncode == 0:
            print(f"  ✅ {tool} installed")
        else:
            print(f"  ❌ {tool} not installed")

def check_audit_logging():
    print("\n[CHECK] Audit & Logging")
    print("-" * 40)
    os.system("systemctl is-active auditd 2>/dev/null || echo 'auditd not running'")
    os.system("ls /etc/logrotate.d/ | wc -l | xargs echo 'Logrotate configs:'")

def check_package_updates():
    print("\n[CHECK] Package Updates")
    print("-" * 40)
    os.system("apt list --upgradable 2>/dev/null | grep security | wc -l | xargs echo 'Security updates:'")

def check_ssh_advanced():
    print("\n[CHECK] Advanced SSH")
    print("-" * 40)
    if os.path.exists("/etc/ssh/sshd_config"):
        os.system("grep -E 'X11Forwarding|MaxAuthTries' /etc/ssh/sshd_config 2>/dev/null | grep -v '^#'")

def check_system_hardening():
    print("\n[CHECK] System Hardening")
    print("-" * 40)
    os.system("sysctl kernel.randomize_va_space")
    os.system("aa-status 2>/dev/null | grep enforce | head -1")

def check_containers():
    print("\n[CHECK] Container Security")
    print("-" * 40)
    if os.path.exists("/usr/bin/docker"):
        os.system("docker ps -a 2>/dev/null | wc -l | xargs echo 'Docker containers:'")

def check_failed_services():
    print("\n[CHECK] Failed Services")
    print("-" * 40)
    os.system("systemctl --failed | head -5")

def check_disk_encryption():
    print("\n[CHECK] Disk Encryption")
    print("-" * 40)
    os.system("lsblk | grep crypt || echo 'No encrypted partitions'")

def check_last_reboot():
    print("\n[CHECK] Last Reboot")
    print("-" * 40)
    os.system("last reboot | head -3")

def check_memory_usage():
    print("\n[CHECK] Memory Usage")
    print("-" * 40)
    os.system("free -h")

def check_disk_usage():
    print("\n[CHECK] Disk Usage")
    print("-" * 40)
    os.system("df -h | grep -E '^/dev/'")

def run_all_advanced():
    print("\n" + "="*60)
    print("🔧 ADVANCED SECURITY CHECKS")
    print("="*60)
    check_cis_benchmarks()
    check_database_security()
    check_webserver_security()
    check_network_security()
    check_malware_scanners()
    check_audit_logging()
    check_package_updates()
    check_ssh_advanced()
    check_system_hardening()
    check_containers()
    check_failed_services()
    check_disk_encryption()
    check_last_reboot()
    check_memory_usage()
    check_disk_usage()

if __name__ == "__main__":
    run_all_advanced()
