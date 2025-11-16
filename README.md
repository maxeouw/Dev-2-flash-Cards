# Arborescence du projet:

```bash
jean_memorator/
│
├── main.py                  # Point d’entrée de l’application
│
├── core/                    # Logique métier
│   ├── models.py            # Classes Fiche, Tag, Utilisateur, etc.
│   ├── spaced_repetition.py # Système de révision espacée
│   └── storage.py           # Sauvegarde/chargement local (JSON, SQLite)
│
├── ui/                      # Interface graphique
│   ├── main_window.py       # Fenêtre principale (menu, navigation)
│   ├── fiches_view.py       # Vue de gestion des fiches
│   ├── revision_view.py     # Vue de révision
│   └── dashboard_view.py    # Tableau de bord / statistiques
│
├── assets/                  # Images, sons, icônes, etc.
│
└── data/                    # Données locales (fichiers JSON / DB)
    └── fiches.json

```
