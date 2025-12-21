import unittest
from unittest.mock import MagicMock

from core.models import FlashCard
from core.storage import StorageManager
from core.formManager import FormsManager 


class TestFormsManagerEdward(unittest.TestCase):

    def setUp(self):
        # Mock du StorageManager pour ne pas toucher à la vraie DB
        self.mock_storage = MagicMock(spec=StorageManager)

        # Pour create_form : on simule que la DB renvoie un id (ex: 42)
        self.mock_storage.add_form_to_db.return_value = 42

        # Pour delete_form : on n'a pas besoin de valeur de retour
        self.forms_manager = FormsManager(storage=self.mock_storage)
        # On évite de charger depuis la DB dans les tests unitaires
        self.forms_manager.fiches = []
        self.forms_manager._next_id = 1

    def test_create_form_adds_form_in_memory_and_db(self):
        # Arrange
        question = "Quelle est la capitale de la France ?"
        reponse = "Paris"
        tags = ["géographie", "europe"]

        # Act
        fiche = self.forms_manager.create_form(question, reponse, tags)

        # Assert : vérifie le type et le contenu de la fiche
        self.assertIsInstance(fiche, FlashCard)
        self.assertEqual(fiche.id, 42)  # id mis à jour avec celui renvoyé par la DB
        self.assertEqual(fiche.question, question)
        self.assertEqual(fiche.reponses, [reponse])
        self.assertEqual(fiche.tags, tags)

        # Vérifie que la fiche est bien ajoutée en mémoire
        self.assertIn(fiche, self.forms_manager.fiches)

        # Vérifie que la méthode de persistance a été appelée une fois
        self.mock_storage.add_form_to_db.assert_called_once_with(fiche)

    def test_delete_form_removes_form_in_memory_and_db(self):
        # Arrange : on prépare une fiche déjà présente
        fiche = FlashCard(
            id=10,
            question="Question test",
            reponses=["Réponse"],
            tags=[]
        )
        self.forms_manager.fiches = [fiche]

        # Act
        result = self.forms_manager.delete_form(fiche_id=10)

        # Assert : la méthode doit renvoyer True
        self.assertTrue(result)

        # La fiche doit être supprimée de la liste en mémoire
        self.assertNotIn(fiche, self.forms_manager.fiches)

        # La méthode delete_form_from_db du storage doit être appelée avec le bon id
        self.mock_storage.delete_form_from_db.assert_called_once_with(10)


if __name__ == "__main__":
    unittest.main()
