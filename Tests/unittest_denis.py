import os
import sqlite3
import unittest
from datetime import datetime

from core.storage import StorageManager, StatsNotFoundError
from core.models import Stats


class TestStatsStorage(unittest.TestCase):
    def setUp(self):
        # Utiliser une DB de test séparée
        self.test_db = "test_storage.db"

        # Créer un StorageManager puis forcer le chemin avant ré-init
        self.storage = StorageManager()
        self.storage.db_path = self.test_db
        self.storage._init_db()

        # Nettoyage de la table stats_revision
        import sqlite3
        with sqlite3.connect(self.test_db) as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM stats_revision")
            db.commit()

    def tearDown(self):
    # On ne supprime pas le fichier pour éviter les problèmes de handle sur Windows.
    # Le setUp nettoie déjà la table stats_revision avant chaque test.
        pass

    def test_add_stats_session_success_rate(self):
        """Vérifie que success_rate est bien calculé pour 6 cartes dont 4 échecs."""
        deck_id = 1
        total = 6
        fails = 4

        self.storage.add_stats_session(deck_id, total, fails)
        stats_list = self.storage.load_stats_for_deck(deck_id)

        self.assertEqual(len(stats_list), 1)
        stats = stats_list[0]
        self.assertAlmostEqual(stats.success_rate, (total - fails) / total * 100.0, places=2)

    def test_get_last_stats_for_deck_exception(self):
        """Vérifie que StatsNotFoundError est levée s'il n'y a pas de stats pour un deck."""
        deck_id = 999
        with self.assertRaises(StatsNotFoundError):
            self.storage.get_last_stats_for_deck(deck_id)


if __name__ == "__main__":
    unittest.main()
