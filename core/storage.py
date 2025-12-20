# POUR SUPPRIMER TABLE SI PROBLEME ENLEVER COMMENTAIRE LIGNE 23-29

import sqlite3
from datetime import datetime
from typing import List
from core.models import Form, Stats


class StorageManager:
    """Gère la persistance des fiches en base de données SQLite."""
    
    DB_FILE = "storage.db"

    def __init__(self):
        self.db_path = self.DB_FILE
        self._init_db()

    def _init_db(self):
        """Créer les tables si elles n'existent pas."""
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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stats_revision (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    deck_id INTEGER,              -- NULL = all decks / "review all"
                    date_session TEXT NOT NULL,   -- ISO format
                    total_cards INTEGER NOT NULL,
                    failed_cards INTEGER NOT NULL,
                    success_rate REAL NOT NULL,   -- between 0 and 100
                    FOREIGN KEY(deck_id) REFERENCES categorie(id)
                )
            """)
            db.commit()

    def add_form_to_db(self, form: Form) -> int:
        """Insère une fiche dans la DB et retourne son ID."""
        tags_str = ",".join(form.tags) if form.tags else ""
        reponses_str = "|".join(form.reponses) if form.reponses else ""
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO carte
                (question, reponse, tags, date_creation, derniere_revision, intervalle, niveau, media)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                form.question,
                reponses_str,
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
        reponses_str = "|".join(form.reponses) if form.reponses else ""
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""
                UPDATE carte
                SET question = ?, reponse = ?, tags = ?, 
                    derniere_revision = ?, intervalle = ?, niveau = ?
                WHERE id = ?
            """, (
                form.question,
                reponses_str,
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
            reponses_list = row[2].split("|") if row[2] else [""]

            forms.append(Form(
                id=row[0],
                question=row[1],
                reponses=reponses_list,
                tags=row[3].split(",") if row[3] else [],
                date_creation=datetime.fromisoformat(row[4]),
                derniere_revision=datetime.fromisoformat(row[5]),
                intervalle=row[6],
                niveau=row[7],
                media=[]
            ))
        return forms

    # ----------------------------------------------------------
    # Decks
    # ----------------------------------------------------------

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
        

    # --- supprime un deck de la db ---    
    def delete_deck_from_db(self, deck_id: int) -> bool:
        """Supprime un deck et ses liens carte↔deck dans la DB."""
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()

            # Supprimer les liens entre ce deck et les cartes
            cursor.execute(
                "DELETE FROM lier_fiche_deck WHERE deck_id = ?",
                (deck_id,)
            )

            # Supprimer le deck lui-même
            cursor.execute(
                "DELETE FROM categorie WHERE id = ?",
                (deck_id,)
            )

            db.commit()
            return cursor.rowcount > 0

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
            with sqlite3.connect(self.db_path) as db2:
                cursor2 = db2.cursor()
                cursor2.execute("SELECT card_id FROM lier_fiche_deck WHERE deck_id = ?", (current_deck_id,))
                fiche_rows = cursor2.fetchall()
            
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
    def add_stats_session(self, deck_id, total_cards, failed_cards) -> int:
        if total_cards <= 0:
            return 0
        success_rate = (total_cards - failed_cards) / total_cards * 100.0
        date_session = datetime.now().isoformat()

        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute(
                """
                INSERT INTO stats_revision
                    (deck_id, date_session, total_cards, failed_cards, success_rate)
                VALUES (?, ?, ?, ?, ?)
                """,
                (deck_id, date_session, total_cards, failed_cards, success_rate),
            )
            db.commit()
            return cursor.lastrowid

    def load_stats_for_deck(self, deck_id=None) -> List[Stats]:
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            if deck_id is None:
                cursor.execute(
                    """
                    SELECT deck_id, date_session, total_cards, failed_cards, success_rate
                    FROM stats_revision
                    ORDER BY date_session ASC
                    """
                )
            else:
                cursor.execute(
                    """
                    SELECT deck_id, date_session, total_cards, failed_cards, success_rate
                    FROM stats_revision
                    WHERE deck_id = ?
                    ORDER BY date_session ASC
                    """,
                (deck_id,),
                )
            rows = cursor.fetchall()

        stats: List[Stats] = []
        for deck_id_val, date_session, total, failed, success in rows:
            stats.append(
                Stats(
                    deck_id=deck_id_val,
                    date_session=datetime.fromisoformat(date_session),
                    total_cards=total,
                    failed_cards=failed,
                    success_rate=success,
                )
            )
        return stats
    def get_last_stats_for_deck(self, deck_id: int) -> Stats:
        """Retourne la dernière session pour un deck, ou StatsNotFoundError"""
        stats = self.load_stats_for_deck(deck_id)
        if not stats:
            raise StatsNotFoundError(f"Aucune statistique pour le deck {deck_id}")
        return stats[-1]


class StatsNotFoundError(Exception):
    """Exception si il n'y a pas des stats pour un deck"""
    pass
