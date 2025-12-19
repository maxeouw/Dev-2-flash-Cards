import unittest
from unittest.mock import MagicMock
from core.models import Form, Deck
from core.storage import StorageManager
from core.formManager import FormsManager, DeckCreationError

class TestFormsManagerLiam(unittest.TestCase):

    def setUp(self):
        # Mock du StorageManager (simulation de la DB)
        self.mock_storage = MagicMock(spec=StorageManager)
        
        # Configuration des retours simulés
        self.mock_storage.add_form_to_db.return_value = 101  # ID fictif pour une fiche
        self.mock_storage.add_deck_to_db.return_value = 5    # ID fictif pour un deck
        self.mock_storage.update_form_in_db.return_value = True

        # Initialisation du FormsManager avec le mock
        self.forms_manager = FormsManager(storage=self.mock_storage)
        
        # On vide les listes pour partir d'un état propre
        self.forms_manager.fiches = []
        self.forms_manager.decks = []
        self.forms_manager._next_id = 1
        self.forms_manager._next_deck_id = 1

    # --- TEST 1 : Création d'une fiche avec réponses MULTIPLES ---
    def test_create_form_with_multiple_answers(self):
        """Test si une fiche peut gérer plusieurs réponses (liste)."""
        # Arrange
        question = "Capitale de la Belgique ?"
        reponses = ["Bruxelles", "Brussel", "Brussels"]  # Liste de réponses
        
        # Act
        fiche = self.forms_manager.create_form(question, reponses)

        # Assert
        self.assertIsInstance(fiche, Form)
        self.assertEqual(fiche.reponses, reponses)  # Vérifie que la liste est bien stockée
        self.assertEqual(len(fiche.reponses), 3)    # Il doit y avoir 3 variantes
        
        # Vérifie que la propriété de compatibilité .reponse renvoie la première
        self.assertEqual(fiche.reponse, "Bruxelles")

    # --- TEST 2 : Création d'un Deck ---
    def test_create_deck_valid(self):
        """Test la création d'un deck valide."""
        # Arrange
        nom_deck = "Histoire Géo"

        # Act
        deck = self.forms_manager.create_deck(nom_deck)

        # Assert
        self.assertIsInstance(deck, Deck)
        self.assertEqual(deck.nom, "Histoire Géo")
        self.assertEqual(deck.id, 5)  # ID simulé par le mock
        self.assertIn(deck, self.forms_manager.decks)
        
        # Vérifie l'appel à la DB
        self.mock_storage.add_deck_to_db.assert_called_once()

    def test_create_deck_invalid_empty_name(self):
        """Test si la création d'un deck vide lève bien une exception."""
        # Act & Assert
        with self.assertRaises(DeckCreationError):
            self.forms_manager.create_deck("")  # Nom vide
            
        with self.assertRaises(DeckCreationError):
            self.forms_manager.create_deck("   ")  # Espaces seuls

    # --- TEST 3 : Modification d'une fiche ---
    def test_modify_form_updates_memory_and_db(self):
        """Test la modification d'une fiche existante."""
        # Arrange : Création d'une fiche initiale
        fiche_originale = Form(id=1, question="Q1", reponses=["R1"])
        self.forms_manager.fiches = [fiche_originale]

        # On prépare la version modifiée (même ID, nouveau contenu)
        fiche_modifiee = Form(id=1, question="Q1 Modifiée", reponses=["R1", "R2"])

        # Act
        resultat = self.forms_manager.modify_form(fiche_modifiee)

        # Assert
        self.assertTrue(resultat)
        
        # Vérifie que l'objet en mémoire a bien été mis à jour
        fiche_en_memoire = self.forms_manager.get_form(1)
        self.assertEqual(fiche_en_memoire.question, "Q1 Modifiée")
        self.assertEqual(len(fiche_en_memoire.reponses), 2)
        
        # Vérifie que l'appel à la DB a été fait
        self.mock_storage.update_form_in_db.assert_called_once_with(fiche_modifiee)

if __name__ == "__main__":
    unittest.main()
