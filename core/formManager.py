from typing import List, Optional
from datetime import datetime
from core.models import Form


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
        self._next_id = 1
        self.storage = storage
        self.charger_fiches_depuis_db()

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

    def toutes_les_fiches(self) -> List[Form]:
        return self.fiches
    
    # ----------------------------------------------------------
    # Chargement depuis la DB
    # ----------------------------------------------------------
    def charger_fiches_depuis_db(self):
        self.fiches = self.storage.load_all_forms()
        self._next_id = max((f.id for f in self.fiches), default=0) + 1


"""
class SpacesRepetitionEngine:

class StorageManager

class StatsManager

class MotivationEngine
"""