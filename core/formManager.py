from typing import List, Optional
from datetime import datetime
from core.models import Form, Deck
from typing import List, Optional
from datetime import datetime, timedelta
from core.storage import StorageManager


class FormsManager:
    """
    Gère les fiches : création, modification, suppression,
    recherche et sélection pour la révision.
    """

    def __init__(self, storage: StorageManager):
        self.fiches: List[Form] = []
        self.decks: List[Deck] = []
        self._next_id = 1
        self._next_deck_id = 1
        self.storage = storage
        self.charger_fiches_depuis_db()
        self.charger_decks_depuis_db()

    # ----------------------------------------------------------
    # CRUD
    # ----------------------------------------------------------

    def create_form(
        self,
        question: str,
        reponse: str,
        tags: Optional[List[str]] = None
    ) -> Form:
        """Créer une fiche Question/Réponse."""
        fiche = Form(
            id=self._next_id,
            question=question,
            reponse=reponse,
            tags=tags if tags else [],
        )

        db_id = self.storage.add_form_to_db(fiche)
        fiche.id = db_id

        self.fiches.append(fiche)
        self._next_id += 1
        return fiche

    def delete_form(self, fiche_id: int) -> bool:
        """Supprime une fiche de la liste ET de la DB."""
        for fiche in self.fiches:
            if fiche.id == fiche_id:
                self.fiches.remove(fiche)
                # Supprime aussi de la DB
                self.storage.delete_form_from_db(fiche_id)
                return True
        return False

    def modify_form(self, fiche_modifiee: Form) -> bool:
        """Modifie une fiche en mémoire ET dans la DB."""
        for i, fiche in enumerate(self.fiches):
            if fiche.id == fiche_modifiee.id:
                self.fiches[i] = fiche_modifiee
                # Met à jour aussi la DB
                self.storage.update_form_in_db(fiche_modifiee)
                return True
        return False


    def get_form(self, fiche_id: int) -> Optional[Form]:
        for fiche in self.fiches:
            if fiche.id == fiche_id:
                return fiche
        return None

    def create_deck(self, nom: str) -> Deck:
        """Créer un nouveau deck (sans DB pour l'instant)."""
        deck = Deck(
            id=self._next_deck_id,
            nom=nom
        )
        db_id = self.storage.add_deck_to_db(deck)
        deck.id = db_id
        self.decks.append(deck)
        self._next_deck_id += 1
        return deck
    # ----------------------------------------------------------
    # Recherche
    # ----------------------------------------------------------

    def rechercher(self, mot_clef: str) -> List[Form]:
        mot_clef = mot_clef.lower()
        return [
            f for f in self.fiches
            if mot_clef in f.question.lower() or mot_clef in f.reponse.lower()
        ]

    # ----------------------------------------------------------
    # Révision
    # ----------------------------------------------------------

    def fiches_a_reviser(self) -> List[Form]:
        maintenant = datetime.now()
        return [
            fiche for fiche in self.fiches
            if fiche.derniere_revision + timedelta(days=fiche.intervalle) <= maintenant
        ]

    # ----------------------------------------------------------
    # Import / export
    # ----------------------------------------------------------

    def charger_fiches(self, fiches: List[Form]):
        self.fiches = fiches
        self._next_id = max((f.id for f in fiches), default=0) + 1

    def charger_decks(self, decks: List[Deck]):
        self.decks = decks
        self._next_deck_id = max((d.id for d in decks), default=0) + 1

    def toutes_les_fiches(self) -> List[Form]:
        return self.fiches
    
    def tous_les_decks(self) -> List[Deck]:
        return self.decks
    

    # ----------------------------------------------------------
    # Chargement depuis la DB (Decks et Fiches)
    # ----------------------------------------------------------
    def charger_fiches_depuis_db(self):
        self.fiches = self.storage.load_all_forms()
        self._next_id = max((f.id for f in self.fiches), default=0) + 1
    def charger_decks_depuis_db(self):
        self.decks = self.storage.load_all_decks()
        self._next_deck_id = max((d.id for d in self.decks), default=0) + 1

    # ----------------------------------------------------------
    # Ajout des fiches aux decks
    # ----------------------------------------------------------
    def ajouter_fiche_a_deck(self, deck_id: int, fiche_id: int) -> bool:
        for deck in self.decks:
            if deck.id == deck_id:
                if fiche_id not in deck.fiche_ids:
                    # Ajout en RAM
                    deck.fiche_ids.append(fiche_id)

                    # Ajout en DB
                    if hasattr(self.storage, 'link_card_to_deck_in_db'):
                        self.storage.link_card_to_deck_in_db(deck_id, fiche_id)
                    else:
                        print("ERREUR : Méthode link_card_to_deck_in_db manquante dans Storage")
                return True
        return False
    
    def get_fiches_by_deck_id(self, deck_id: int) -> List[Form]:
        """Récupère les Fiche associées à un deck donné."""
        deck = next((d for d in self.decks if d.id == deck_id), None)
        if not deck:
            return []
        # Vérifier si l'ID de la fiche est présent dans deck.fiche_ids
        fiches_du_deck = [f for f in self.fiches if f.id in deck.fiche_ids]
        
        return fiches_du_deck
"""
class SpacesRepetitionEngine:

class StorageManager

class StatsManager

class MotivationEngine
"""