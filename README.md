# 🔒 Linux Security Audit Framework

## Framework d'Audit de Sécurité Automatisé pour Infrastructures Linux

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![PFA](https://img.shields.io/badge/PFA-2025--2026-orange)

---

## 📋 Description

Framework automatisé d'audit de sécurité pour infrastructures Linux. Effectue **50+ vérifications de sécurité**, détecte les vulnérabilités **CVE** via l'API NVD, calcule un **score CVSS** et génère des **rapports HTML/PDF** professionnels.

**Réalisé par :** Nassim Ammar  
**Encadrant :** M. Hicham Toumi  
**Établissement :** EMSI - Filière 4CIRM, Cybersécurité  
**Année universitaire :** 2025-2026

---

## ✨ Fonctionnalités

### 🔍 Audit de sécurité
- ✅ **50+ vérifications** basées sur les CIS Benchmarks
- ✅ Vérification SSH (Root Login, X11Forwarding, MaxAuthTries)
- ✅ Vérification des permissions fichiers critiques
- ✅ Vérification du pare-feu (UFW)
- ✅ Vérification des utilisateurs
- ✅ Vérification des paramètres noyau (sysctl)
- ✅ Vérification d'AppArmor

### 🐛 Détection des vulnérabilités
- ✅ Scan CVE via l'API NVD (NIST)
- ✅ Comparaison des packages avec la base de vulnérabilités
- ✅ Classification par sévérité (CVSS)

### 📊 Scoring de sécurité
- ✅ Score global sur 100
- ✅ Grade de A+ à F
- ✅ Pénalités par niveau (CRITICAL, HIGH, MEDIUM, LOW)

### 📄 Rapports
- ✅ Rapport HTML avec design professionnel
- ✅ Rapport PDF imprimable
- ✅ Recommandations avec commandes copier-coller

### 🌐 Interface web
- ✅ Dashboard Flask sur http://localhost:5000
- ✅ Boutons : FULL SCAN, QUICK SCAN, CVE SCAN, DOWNLOAD REPORT, FIX ISSUES
- ✅ Barre de progression en temps réel

### 🔐 Scan distant
- ✅ Audit d'une machine distante via SSH (--target)

---

## 🛠️ Technologies utilisées

| Technologie | Utilisation |
|-------------|-------------|
| **Python 3.12** | Langage principal |
| **Bash** | Commandes système |
| **Flask** | Dashboard web |
| **Jinja2** | Templates HTML |
| **Requests** | API NVD |
| **ReportLab** | Génération PDF |
| **Psutil** | Monitoring processus |
| **VMware** | Virtualisation |
| **Git** | Versioning |

---

## 📊 Standards & Référentiels

- 🛡️ **CIS Benchmarks** (Center for Internet Security)
- 📉 **CVSS** (Common Vulnerability Scoring System)
- 🗄️ **NVD API** (National Vulnerability Database - NIST)
- 🏛️ **NIST Cybersecurity Framework**

---

## 🚀 Installation

### Prérequis
- Ubuntu 24.04 / Debian 12 / Kali Linux
- Python 3.10+
- 500 MB d'espace disque

### Installation rapide

```bash
# 1. Cloner le projet
git clone https://github.com/NASSIMAMMAR05/linux-security-audit-framework.git
cd linux-security-audit-framework

# 2. Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip install flask requests reportlab psutil

# 4. Rendre exécutable
chmod +x main.py web_dashboard.py
chmod +x modules/*.py

# 5. Tester
python3 main.py --quick-scan
