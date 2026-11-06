# Guide d'Utilisation - Linux Security Audit Framework

## Commandes CLI

| Commande | Description |
|----------|-------------|
| `python3 main.py --help` | Afficher l'aide |
| `python3 main.py --quick-scan` | Scan rapide (5-10 sec) |
| `sudo python3 main.py --scan` | Audit complet (30-60 sec) |
| `sudo python3 main.py --scan --report html` | Audit + rapport HTML |
| `sudo python3 main.py --scan --report pdf` | Audit + rapport PDF |
| `sudo python3 main.py --scan --report both` | Audit + HTML + PDF |
| `python3 main.py --target user@IP --scan` | Scan distant |

## Interface Web

```bash
# Lancer le serveur
python3 web_dashboard.py

# Ouvrir le navigateur
firefox http://localhost:5000
