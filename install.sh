#!/bin/bash
# Script d'installation automatique - Linux Security Audit Framework
# Auteur: Nassim Ammar

echo "🔒 Linux Security Audit Framework - Installation"
echo "================================================"

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "📦 Installation de Python..."
    sudo apt update && sudo apt install python3 python3-pip python3-venv -y
fi

# Créer le projet
cd ~
mkdir -p linux-audit-framework
cd linux-audit-framework

# Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer dépendances
pip install flask requests reportlab psutil

# Créer les dossiers
mkdir -p modules templates reports logs

# Télécharger les fichiers depuis GitHub (ou copier depuis source)
echo "📥 Téléchargement des fichiers..."
# Remplacer par ton repo GitHub
git clone https://github.com/tonusername/linux-audit-framework.git temp
cp -r temp/* .
rm -rf temp

chmod +x main.py web_dashboard.py

echo ""
echo "✅ Installation terminée!"
echo ""
echo "Pour lancer l'outil:"
echo "  cd ~/linux-audit-framework"
echo "  source venv/bin/activate"
echo "  python3 main.py --quick-scan"
echo "  python3 web_dashboard.py"
