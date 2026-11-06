#!/usr/bin/env python3
"""
Linux Security Audit Framework - PFA 2025-2026
Author: Nassim Ammar
"""

import argparse
import sys
import os
import subprocess
from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    banner = f"""
{Colors.BLUE}{'='*70}
   ██╗     ██╗███╗   ██╗██╗   ██╗██╗  ██╗
   ██║     ██║████╗  ██║██║   ██║╚██╗██╔╝
   ██║     ██║██╔██╗ ██║██║   ██║ ╚███╔╝ 
   ██║     ██║██║╚██╗██║██║   ██║ ██╔██╗ 
   ███████╗██║██║ ╚████║╚██████╔╝██╔╝ ██╗
   ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝
{Colors.ENDC}
{Colors.BOLD}🔒 LINUX SECURITY AUDIT FRAMEWORK - PFA 2025-2026{Colors.ENDC}
{Colors.YELLOW}Author: Nassim Ammar | Domain: Pentest & Audit Interne{Colors.ENDC}
{Colors.BLUE}{'='*70}{Colors.ENDC}
    """
    print(banner)

def run_remote_scan(target):
    """Run audit on remote server via SSH"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}📡 Remote Scan on: {target}{Colors.ENDC}\n")
    
    result = subprocess.run(f"ssh -o ConnectTimeout=10 {target} 'echo OK'", 
                           shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"{Colors.RED}❌ Cannot connect to {target}{Colors.ENDC}")
        return
    
    print(f"{Colors.GREEN}✅ SSH connection successful{Colors.ENDC}")
    
    os.system(f"ssh {target} 'mkdir -p ~/linux-audit-framework'")
    os.system(f"rsync -avz --exclude venv --exclude reports --exclude logs --exclude __pycache__ ./ {target}:~/linux-audit-framework/ 2>/dev/null")
    os.system(f"ssh {target} 'cd ~/linux-audit-framework && python3 -m pip install flask requests reportlab psutil --user 2>/dev/null'")
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}🔍 Running audit on remote server...{Colors.ENDC}\n")
    os.system(f"ssh -t {target} 'cd ~/linux-audit-framework && python3 main.py --scan --report both'")
    
    print(f"\n{Colors.BOLD}📥 Downloading report from remote server...{Colors.ENDC}")
    os.system(f"scp {target}:~/linux-audit-framework/reports/*.html reports/ 2>/dev/null")
    
    print(f"\n{Colors.GREEN}✅ Remote scan completed! Report saved in reports/{Colors.ENDC}")

def quick_scan():
    print(f"\n{Colors.BOLD}{Colors.YELLOW}⚡ QUICK SECURITY SCAN{Colors.ENDC}")
    print(f"{Colors.BOLD}{'-'*50}{Colors.ENDC}\n")
    
    print("[CHECK] SSH Root Login")
    if os.path.exists("/etc/ssh/sshd_config"):
        result = os.popen("grep PermitRootLogin /etc/ssh/sshd_config | grep -v '^#'").read()
        if "yes" in result:
            print("❌ HIGH: Root login ENABLED")
        else:
            print("✅ OK: Root login disabled")
    else:
        print("⚠️ SSH not installed")
    
    print("\n[CHECK] Open Ports")
    os.system("ss -tuln | grep -E ':(22|80|443|3306)' || echo 'No common ports'")
    
    print("\n[CHECK] Users without password")
    os.system("awk -F: '($2 == \"\") {print $1}' /etc/shadow 2>/dev/null || echo 'All users have passwords'")
    
    print("\n[CHECK] Running Services")
    os.system("systemctl list-units --type=service --state=running | head -8")
    
    print("\n[CHECK] Firewall Status")
    os.system("ufw status 2>/dev/null || echo 'UFW not installed'")
    
    print(f"\n{Colors.GREEN}✅ Quick scan complete{Colors.ENDC}")

def full_scan():
    print(f"\n{Colors.BOLD}{Colors.GREEN}📊 Starting Full Security Audit...{Colors.ENDC}\n")
    
    try:
        from modules import collector, audit, cve_scanner, scoring, report
        from modules import advanced_security, port_scanner, process_monitor
    except ImportError as e:
        print(f"⚠️ Module import error: {e}")
        quick_scan()
        return
    
    # Module 1: Collector
    print(f"{Colors.BOLD}📋 MODULE 1: Information Collection{Colors.ENDC}")
    collector.run_collector()
    
    # Module 2: Audit
    print(f"\n{Colors.BOLD}🔍 MODULE 2: Audit Engine{Colors.ENDC}")
    audit.run_all()
    advanced_security.run_all_advanced()
    
    # Bonus: Port Scanner
    print(f"\n{Colors.BOLD}🔌 BONUS: Port Scanner{Colors.ENDC}")
    port_scanner.run_port_scan()
    
    # Bonus: Process Monitor
    print(f"\n{Colors.BOLD}📊 BONUS: Process Monitor{Colors.ENDC}")
    process_monitor.run_process_monitor()
    
    # Module 3: CVE Scanner
    print(f"\n{Colors.BOLD}🐛 MODULE 3: CVE Analysis{Colors.ENDC}")
    cve_results = cve_scanner.check_cve_vulnerabilities()
    
    # Module 4: Scoring - Use real findings from audit
    print(f"\n{Colors.BOLD}📊 MODULE 4: Security Scoring{Colors.ENDC}")
    
    # Collect real findings from the audit (simplified)
    findings = []
    
    # Check crontab permissions
    if os.path.exists("/etc/crontab"):
        perms = os.popen("stat -c %a /etc/crontab").read().strip()
        if perms != "600":
            findings.append({'title': 'Crontab Permissions', 'severity': 'HIGH', 'fix': 'sudo chmod 600 /etc/crontab'})
    
    # Check firewall
    ufw_status = os.popen("ufw status | grep -i active").read()
    if not ufw_status:
        findings.append({'title': 'Firewall Disabled', 'severity': 'MEDIUM', 'fix': 'sudo ufw enable'})
    
    # Check X11Forwarding
    if os.path.exists("/etc/ssh/sshd_config"):
        x11 = os.popen("grep -i 'X11Forwarding yes' /etc/ssh/sshd_config | grep -v '^#'").read()
        if x11:
            findings.append({'title': 'X11Forwarding Enabled', 'severity': 'MEDIUM', 'fix': 'Set X11Forwarding no'})
    
    # Calculate score with CVEs
    from modules.scoring import calculate_severity_score
    score_result = calculate_severity_score(findings, cve_results)
    
    # Module 5: Report
    if hasattr(args, 'report') and args.report:
        print(f"\n{Colors.BOLD}📄 MODULE 5: Report Generation{Colors.ENDC}")
        if args.report in ['html', 'both']:
            report.generate_html_report(findings, cve_results, score_result)
    
    # Display results
    print(f"\n{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}📈 SECURITY SCORE SUMMARY{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"\nScore: {score_result['score']}/100")
    print(f"Grade: {score_result['grade']}")
    print(f"Penalty: {score_result['penalty']} points")
    print(f"\n{Colors.GREEN}✅ Audit Complete!{Colors.ENDC}")

def main():
    parser = argparse.ArgumentParser(description="Linux Security Audit Framework")
    parser.add_argument("--scan", action="store_true", help="Run full security audit")
    parser.add_argument("--quick-scan", action="store_true", help="Run quick security check")
    parser.add_argument("--cve", action="store_true", help="Check CVE vulnerabilities only")
    parser.add_argument("--report", choices=['html', 'pdf', 'both'], help="Generate report format")
    parser.add_argument("--target", type=str, help="Target host for remote scan")
    
    global args
    args = parser.parse_args()
    
    print_banner()
    
    if args.target and args.scan:
        run_remote_scan(args.target)
        return
    elif args.target:
        print(f"{Colors.YELLOW}⚠️ --target requires --scan{Colors.ENDC}")
        return
    
    if args.quick_scan:
        quick_scan()
    elif args.scan:
        full_scan()
    elif args.cve:
        print("🐛 CVE Scan - Use --scan for full CVE detection")
    else:
        print(f"""
{Colors.GREEN}Available Commands:{Colors.ENDC}
  python3 main.py --quick-scan              Quick security check
  python3 main.py --scan                    Full security audit
  python3 main.py --scan --report html      Full audit with HTML report
  python3 main.py --target user@IP --scan   Remote scan
        """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ Audit interrupted{Colors.ENDC}")
        sys.exit(0)
