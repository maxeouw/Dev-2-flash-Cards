# POUR SUPPRIMER TABLE SI PROBLEME ENLEVER COMMENTAIRE LIGNE 23-29

import sqlite3
from datetime import datetime
from typing import List
from core.models import Form


class StorageManager:
    """Gère la persistance des fiches en base de données SQLite."""
    
    DB_FILE = "storage.db"

    def __init__(self):
        self.db_path = self.DB_FILE
        self._init_db()

    def _init_db(self):
        """Créer la table 'carte' si elle n'existe pas."""
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()

            # A ENLEVER EN PRODUCTION
            # SUPPRIME LES ANCIENNES TABLES
            """
            try:
                cursor.execute("DROP TABLE IF EXISTS carte")
                cursor.execute("DROP TABLE IF EXISTS categorie")
            except:
                pass
                """



            cursor.execute("""
                CREATE TABLE IF NOT EXISTS carte(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    reponse TEXT NOT NULL,
                    tags TEXT,
                    date_creation TEXT NOT NULL,
                    derniere_revision TEXT NOT NULL,
                    intervalle INTEGER NOT NULL,
                    niveau INTEGER NOT NULL,
                    media TEXT
                )
            """)
            db.commit()

    def add_form_to_db(self, form: Form) -> int:
        """Insère une fiche dans la DB et retourne son ID."""
        tags_str = ",".join(form.tags) if form.tags else ""
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO carte
                (question, reponse, tags, date_creation, derniere_revision, intervalle, niveau, media)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                form.question,
                form.reponse,
                tags_str,
                form.date_creation.isoformat(),
                form.derniere_revision.isoformat(),
                form.intervalle,
                form.niveau,
                ""
            ))
            db.commit()
            return cursor.lastrowid

    def load_all_forms(self) -> List[Form]:
        """Charge toutes les fiches depuis la DB."""
        forms: List[Form] = []
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM carte")
            rows = cursor.fetchall()

        for row in rows:
            forms.append(Form(
                id=row[0],
                question=row[1],
                reponse=row[2],
                tags=row[3].split(",") if row[3] else [],
                date_creation=datetime.fromisoformat(row[4]),
                derniere_revision=datetime.fromisoformat(row[5]),
                intervalle=row[6],
                niveau=row[7],
                media=[]
            ))
        return forms
