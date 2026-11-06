# Guide d'Installation - Linux Security Audit Framework

## Prérequis

| Composant | Minimum |
|-----------|---------|
| RAM | 2 GB |
| CPU | 1 cœur |
| Disque | 500 MB |
| OS | Ubuntu 22.04+ |

## Installation rapide

```bash
# 1. Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# 2. Installer Python
sudo apt install python3 python3-pip python3-venv -y

# 3. Créer le projet
mkdir -p ~/linux-audit-framework
cd ~/linux-audit-framework

# 4. Environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 5. Dépendances
pip install flask requests reportlab psutil

# 6. Tester
python3 main.py --quick-scan
