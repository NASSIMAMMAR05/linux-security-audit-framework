#!/usr/bin/env python3
"""
Module 3: Analyse des vulnérabilités CVE via API NVD
"""

import subprocess
import requests
import os

def get_installed_packages():
    """Get list of installed packages"""
    packages = []
    if os.path.exists("/usr/bin/dpkg"):
        result = subprocess.run(["dpkg-query", "-W", "-f=${Package}\n"], 
                               capture_output=True, text=True)
        packages = result.stdout.strip().split('\n')
    return packages[:30]

def check_cve_vulnerabilities():
    """Check packages against NVD API"""
    print("\n" + "="*60)
    print("🔍 CVE VULNERABILITY SCAN")
    print("="*60)
    
    packages = get_installed_packages()
    if not packages:
        print("⚠️ Could not retrieve package list")
        return []
    
    print(f"Checking {len(packages)} installed packages...\n")
    vulnerabilities = []
    
    for package in packages[:10]:
        if package and len(package) > 2:
            try:
                url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={package}&resultsPerPage=1"
                response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    vuln_count = data.get('totalResults', 0)
                    
                    if vuln_count > 0:
                        print(f"❌ {package}: {vuln_count} known vulnerabilities")
                        vulnerabilities.append({
                            'package': package,
                            'count': vuln_count,
                            'severity': 'HIGH' if vuln_count > 5 else 'MEDIUM'
                        })
                    else:
                        print(f"✅ {package}: No known CVEs")
                else:
                    print(f"⚠️ Could not check {package}")
            except Exception as e:
                print(f"⚠️ Error checking {package}")
    
    if not vulnerabilities:
        print("\n✅ No vulnerabilities found")
    else:
        print(f"\n⚠️ Found {len(vulnerabilities)} packages with vulnerabilities")
    
    return vulnerabilities

if __name__ == "__main__":
    check_cve_vulnerabilities()
