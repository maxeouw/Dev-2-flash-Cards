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
                cursor.execute("DROP TABLE IF EXISTS lier_fiche_deck")
            except:
                pass
                """

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categorie(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL
                )
            """)

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

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lier_fiche_deck(
                    deck_id INTEGER,
                    card_id INTEGER,
                    PRIMARY KEY (deck_id, card_id),
                    FOREIGN KEY(deck_id) REFERENCES categorie(id),
                    FOREIGN KEY(card_id) REFERENCES carte(id)
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

    def update_form_in_db(self, form: Form) -> bool:
        """Met à jour une fiche dans la DB."""
        tags_str = ",".join(form.tags) if form.tags else ""
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""
                UPDATE carte
                SET question = ?, reponse = ?, tags = ?, 
                    derniere_revision = ?, intervalle = ?, niveau = ?
                WHERE id = ?
            """, (
                form.question,
                form.reponse,
                tags_str,
                form.derniere_revision.isoformat(),
                form.intervalle,
                form.niveau,
                form.id
            ))
            db.commit()
            return cursor.rowcount > 0

    def delete_form_from_db(self, fiche_id: int) -> bool:
        """Supprime une fiche de la DB."""
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM carte WHERE id = ?", (fiche_id,))
            db.commit()
            return cursor.rowcount > 0

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

# Decks

    def add_deck_to_db(self, deck) -> int:
        """Insère un deck dans la DB et retourne son ID."""
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO categorie (nom)
                VALUES (?)
            """, (deck.nom,))
            db.commit()
            return cursor.lastrowid

    def load_all_decks(self):
        """Charge tous les decks depuis la DB."""
        from core.models import Deck
        decks = []
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM categorie")
            rows = cursor.fetchall()

        for row in rows:
            current_deck_id = row[0]
            deck_name = row[1]
                # Récupère ID deck et fiches liées
            cursor.execute("SELECT card_id FROM lier_fiche_deck WHERE deck_id = ?", (current_deck_id,))
            fiche_rows = cursor.fetchall()
            ids_fiches = [f[0] for f in fiche_rows]

            decks.append(Deck(
                id=current_deck_id,
                nom=deck_name,
                fiche_ids=ids_fiches
            ))
        return decks
    
    def link_card_to_deck_in_db(self, deck_id: int, card_id: int):
        """Lie une fiche à un deck dans la DB."""
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO lier_fiche_deck (deck_id, card_id)
                VALUES (?, ?)
            """, (deck_id, card_id))
            db.commit()