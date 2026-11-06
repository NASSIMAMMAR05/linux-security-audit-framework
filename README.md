# 🔒 Linux Security Audit Framework

## Framework d'Audit de Sécurité Automatisé pour Infrastructures Linux

---

**Auteur :** Nassim Ammar  
**Domaine :** Pentest & Audit Interne  
**Année universitaire :** 2025 - 2026  
**Établissement :** EMSI

---

## 📋 Table des matières

1. [Présentation](#présentation)
2. [Fonctionnalités](#fonctionnalités)
3. [Architecture](#architecture)
4. [Installation](#installation)
5. [Utilisation](#utilisation)
6. [Commandes CLI](#commandes-cli)
7. [Modules](#modules)
8. [Rapports](#rapports)
9. [Dépannage](#dépannage)

---

## Présentation

### Contexte
Les systèmes Linux sont devenus essentiels dans les environnements critiques (serveurs web, cloud, DevOps). Les audits de sécurité manuels sont longs et sujets à erreurs.

### Solution
Le **Linux Security Audit Framework** est un outil automatisé qui permet d'analyser la sécurité d'un système Linux et de générer des rapports détaillés.

### Problématique résolue
- ❌ Processus long et répétitif
- ❌ Risque d'erreurs humaines
- ❌ Difficulté à maintenir la conformité
- ❌ Manque d'automatisation
- ❌ Évolution constante des vulnérabilités (CVE)

---

## Fonctionnalités

### Core Features

| Fonctionnalité | Description |
|----------------|-------------|
| **50+ vérifications** | Basées sur les CIS Benchmarks |
| **Scan CVE** | Intégration API NVD |
| **Scoring CVSS** | Score 0-100 avec grades A+ à F |
| **Rapports HTML/PDF** | Professionnels avec recommandations |
| **Architecture modulaire** | 5 modules indépendants |

### Interfaces

| Interface | Description |
|-----------|-------------|
| **CLI** | Ligne de commande avec bannière ASCII |
| **Web Dashboard** | Interface Flask sur port 5000 |

### Bonus

| Bonus | Description |
|-------|-------------|
| **Port Scanner** | Détection TCP/UDP, services, risques |
| **Process Monitor** | CPU, mémoire, top processus |
| **Scan distant (--target)** | Audit via SSH |
| **OpenSCAP** | Conformité CIS (bonus) |

---

## Architecture

┌─────────────────────────────────────────────────────────────────────────────┐
│ LINUX SECURITY AUDIT FRAMEWORK │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE UTILISATEUR │
├─────────────────────────────┬───────────────────────────────────────────────┤
│ CLI (main.py) │ WEB DASHBOARD (Flask) │
│ --scan --quick-scan --target│ http://localhost:5000 │
└─────────────────────────────┴───────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ MOTEUR D'AUDIT │
├───────────┬───────────┬───────────┬───────────┬───────────┬────────────────┤
│ Module 1 │ Module 2 │ Module 3 │ Module 4 │ Module 5 │ Bonus │
│ Collecteur│ Audit │ CVE │ Scoring │ Rapport │ │
├───────────┼───────────┼───────────┼───────────┼───────────┼────────────────┤
│ OS │ SSH │ API NVD │ CVSS │ HTML │ Port Scanner │
│ Packages │ Sudoers │ 30 packs │ 0-100 │ PDF │ Process Mon. │
│ Users │ Kernel │ Alertes │ A+ à F │ Fix │ OpenSCAP │
│ Services │ Permissions│ │ │ │ │
│ Ports │ Firewall │ │ │ │ │
└───────────┴───────────┴───────────┴───────────┴───────────┴────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ RAPPORTS │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📊 Score: XX/100 │ 🔍 50+ vérifications │ 🐛 CVEs trouvées │
│ 📄 Rapport HTML │ 📑 Rapport PDF │ 🔧 Recommandations │
└─────────────────────────────────────────────────────────────────────────────┘
