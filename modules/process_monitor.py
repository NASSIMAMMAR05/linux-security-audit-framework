#!/usr/bin/env python3
"""
Module Process Monitor Avancé - Monitoring complet des processus
"""

import os
import subprocess
import psutil
from datetime import datetime

def get_all_processes_detailed():
    """Obtenir tous les processus avec détails"""
    print("\n" + "="*70)
    print("📊 PROCESS MONITORING AVANCÉ")
    print("="*70)
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n🔄 TOP 20 PROCESSUS PAR CPU:")
    print("-" * 70)
    print(f"{'PID':<8} {'NAME':<25} {'CPU%':<8} {'MEM%':<8} {'STATUS':<10}")
    print("-" * 70)
    
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            pinfo = proc.info
            if pinfo['cpu_percent'] and pinfo['cpu_percent'] > 0:
                processes.append(pinfo)
        except:
            pass
    
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    
    for proc in processes[:20]:
        pid = proc['pid']
        name = (proc['name'] or 'unknown')[:25]
        cpu = proc['cpu_percent'] or 0
        mem = proc['memory_percent'] or 0
        
        if cpu > 50:
            status = "⚠️ HIGH CPU"
        elif cpu > 25:
            status = "🟡 MEDIUM"
        else:
            status = "🟢 NORMAL"
        
        print(f"{pid:<8} {name:<25} {cpu:<8.1f} {mem:<8.1f} {status:<10}")
    
    return processes[:20]

def get_memory_details():
    """Détails mémoire détaillés"""
    print("\n" + "="*70)
    print("💾 MÉMOIRE DÉTAILLÉE")
    print("="*70)
    
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    print(f"   RAM Totale:     {memory.total / (1024**3):.2f} GB")
    print(f"   RAM Utilisée:   {memory.used / (1024**3):.2f} GB ({memory.percent}%)")
    print(f"   RAM Libre:      {memory.free / (1024**3):.2f} GB")
    print(f"   RAM Cache:      {memory.cached / (1024**3):.2f} GB" if hasattr(memory, 'cached') else "")
    print(f"   Swap Totale:    {swap.total / (1024**3):.2f} GB")
    print(f"   Swap Utilisée:  {swap.used / (1024**3):.2f} GB ({swap.percent}%)")
    
    # Alerte mémoire
    if memory.percent > 90:
        print("   🔴 CRITICAL: Mémoire très haute!")
    elif memory.percent > 75:
        print("   🟡 WARNING: Mémoire élevée")
    else:
        print("   🟢 OK: Mémoire normale")

def get_cpu_details():
    """Détails CPU détaillés"""
    print("\n" + "="*70)
    print("🖥️ CPU DÉTAILLÉ")
    print("="*70)
    
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    
    print(f"   CPU Usage:      {cpu_percent}%")
    print(f"   CPU Cores:      {cpu_count}")
    print(f"   CPU Frequency:  {cpu_freq.current:.0f} MHz" if cpu_freq else "")
    
    # Par core
    print("\n   CPU par cœur:")
    for i, perc in enumerate(psutil.cpu_percent(percpu=True)):
        bar = "█" * int(perc / 5) + "░" * (20 - int(perc / 5))
        print(f"   Cœur {i}: {bar} {perc}%")
    
    if cpu_percent > 90:
        print("\n   🔴 CRITICAL: CPU très haute!")
    elif cpu_percent > 75:
        print("\n   🟡 WARNING: CPU élevée")
    else:
        print("\n   🟢 OK: CPU normale")

def get_disk_details():
    """Détails disque détaillés"""
    print("\n" + "="*70)
    print("💿 DISQUE DÉTAILLÉ")
    print("="*70)
    
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            bar = "█" * int(usage.percent / 5) + "░" * (20 - int(usage.percent / 5))
            print(f"\n   {partition.mountpoint}:")
            print(f"      Usage: {bar} {usage.percent}%")
            print(f"      Total: {usage.total / (1024**3):.2f} GB")
            print(f"      Utilisé: {usage.used / (1024**3):.2f} GB")
            print(f"      Libre: {usage.free / (1024**3):.2f} GB")
            
            if usage.percent > 90:
                print(f"      🔴 CRITICAL: Disque presque plein!")
            elif usage.percent > 75:
                print(f"      🟡 WARNING: Disque élevé")
        except:
            pass

def get_system_health():
    """Score de santé système"""
    print("\n" + "="*70)
    print("💚 SYSTÈME HEALTH SCORE")
    print("="*70)
    
    score = 100
    alerts = []
    
    # CPU
    cpu = psutil.cpu_percent()
    if cpu > 90:
        score -= 30
        alerts.append("CPU très haute")
    elif cpu > 75:
        score -= 15
        alerts.append("CPU élevée")
    
    # Mémoire
    mem = psutil.virtual_memory().percent
    if mem > 90:
        score -= 30
        alerts.append("Mémoire très haute")
    elif mem > 75:
        score -= 15
        alerts.append("Mémoire élevée")
    
    # Disque
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint).percent
            if usage > 90:
                score -= 20
                alerts.append(f"Disque {partition.mountpoint} plein")
                break
            elif usage > 75:
                score -= 10
        except:
            pass
    
    score = max(0, score)
    
    if score >= 90:
        grade = "A+ (Excellent)"
        emoji = "🟢"
    elif score >= 80:
        grade = "A (Good)"
        emoji = "🟢"
    elif score >= 70:
        grade = "B (Average)"
        emoji = "🟡"
    elif score >= 60:
        grade = "C (Needs Attention)"
        emoji = "🟡"
    else:
        grade = "D (Critical)"
        emoji = "🔴"
    
    print(f"   {emoji} Health Score: {score}/100")
    print(f"   Grade: {grade}")
    
    if alerts:
        print(f"\n   ⚠️ Alertes:")
        for alert in alerts:
            print(f"      - {alert}")
    
    return {'score': score, 'grade': grade, 'alerts': alerts}

def run_process_monitor():
    """Exécuter le monitoring complet"""
    get_all_processes_detailed()
    get_memory_details()
    get_cpu_details()
    get_disk_details()
    get_system_health()
    
    print("\n" + "="*70)
    print("✅ Monitoring terminé!")
    print("="*70)

if __name__ == "__main__":
    run_process_monitor()
