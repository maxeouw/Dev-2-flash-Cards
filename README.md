# Arborescence du projet:

```bash
jean_memorator/
│
├── main.py                          # Point d'entrée de l'application
│
├── core/                            # Logique métier
│   ├── __pycache__/
│   ├── audio_manager.py             # Gestion audio/accessibilité
│   ├── formManager.py               # Gestion des fiches et decks
│   ├── models.py                    # Classes Fiche, Deck, Utilisateur, etc.
│   ├── spaced_repetition.py         # Système de révision espacée
│   └── storage.py                   # Sauvegarde/chargement (JSON, SQLite)
│
├── ui/                              # Interface graphique (Tkinter)
│   ├── __pycache__/
│   ├── main_window.py               # Fenêtre principale (menu, navigation)
│   ├── fiches_view.py               # Vue de gestion des fiches
│   ├── add_form_page.py             # Ajout de nouvelle fiche
│   ├── edit_format_page.py          # Édition d'une fiche
│   ├── forms_list.py                # Liste des fiches
│   ├── paquets_list.py              # Liste des decks
│   ├── add_paquet_page.py           # Ajout nouveau deck
│   ├── edit_decks_page.py           # Édition d'un deck
│   ├── revision_view.py             # Vue de sélection révision
│   ├── revision_session_page.py     # Session de révision active
│   ├── end_session_page.py          # Résultats fin de session
│   └── stats_page.py                # Tableau de bord / statistiques
│
├── Tests/                           # Tests unitaires
│   ├── __pycache__/
│   ├── unittest_bastien.py
│   ├── unittest_denis.py
│   ├── unittest_edward.py
│   └── unittest_liam.py
│
├── .gitignore                       # Fichiers à ignorer dans Git
├── README.md                        # Documentation du projet
├── storage.db                       # Base de données SQLite

```
