#!/usr/bin/env python3
"""
Module OpenSCAP - Conformité CIS Benchmarks
"""

import subprocess
import os

def check_openscap_installed():
    result = subprocess.run(["which", "oscap"], capture_output=True, text=True)
    return result.returncode == 0

def run_openscap_scan():
    print("\n" + "="*60)
    print("🔓 OPENSCAP COMPLIANCE SCAN (CIS Benchmarks)")
    print("="*60)
    
    if not check_openscap_installed():
        print("❌ OpenSCAP not installed")
        print("   Install with: sudo apt install openscap-scanner -y")
        return None
    
    print("✅ OpenSCAP is installed")
    print("📋 OpenSCAP can check compliance with CIS Benchmarks")
    print("   To run a full compliance scan:")
    print("   sudo oscap xccdf eval --profile cis /usr/share/xml/scap/ssg/content/ssg-ubuntu2204-ds.xml")
    
    return {'status': 'available', 'tool': 'OpenSCAP'}

def run_openscap_audit():
    return run_openscap_scan()

if __name__ == "__main__":
    run_openscap_audit()
