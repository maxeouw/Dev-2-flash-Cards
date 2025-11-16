from typing import List, Optional
from datetime import datetime
from models import forms
from time import timedelta


class FormsManager:
    """
    Gère l’ensemble des fiches : création, modification, suppression,
    recherche et sélection pour la révision.
    """

    def __init__(self):
        self.fiches: List[forms] = []
        self._next_id = 1

    # ----------------------------------------------------------
    # CRUD : Create, Read, Update, Delete
    # ----------------------------------------------------------

    def create_form(self, titre: str, contenu: str, tags: Optional[List[str]] = None) -> forms:
        """Crée une nouvelle fiche et l’ajoute à la liste."""
        fiche = forms(
            id=self._next_id,
            titre=titre,
            contenu=contenu,
            tags=tags if tags else [],
        )
        self.fiches.append(fiche)
        self._next_id += 1
        return fiche

    def delete_form(self, fiche_id: int) -> bool:
        """Supprime une fiche par son ID."""
        for fiche in self.fiches:
            if fiche.id == fiche_id:
                self.fiches.remove(fiche)
                return True
        return False

    def modify_form(self, fiche_modifiee: forms) -> bool:
        """Met à jour une fiche existante."""
        for i, fiche in enumerate(self.fiches):
            if fiche.id == fiche_modifiee.id:
                self.fiches[i] = fiche_modifiee
                return True
        return False

    def get_form(self, fiche_id: int) -> Optional[forms]:
        """Retourne une fiche spécifique grâce à son ID."""
        for fiche in self.fiches:
            if fiche.id == fiche_id:
                return fiche
        return None

    # ----------------------------------------------------------
    # Recherche et filtrage
    # ----------------------------------------------------------

    def rechercher(self, mot_clef: str) -> List[forms]:
        """Recherche dans le titre et le contenu."""
        mot_clef = mot_clef.lower()
        return [
            fiche for fiche in self.fiches
            if mot_clef in fiche.titre.lower() or mot_clef in fiche.contenu.lower()
        ]

    def filtrer_par_tag(self, tag: str) -> List[forms]:
        """Retourne les fiches qui contiennent un tag donné."""
        return [fiche for fiche in self.fiches if tag in fiche.tags]

    # ----------------------------------------------------------
    # Révision : fiches à revoir selon la date
    # ----------------------------------------------------------

    def fiches_a_reviser(self) -> List[forms]:
        """
        Retourne les fiches qui doivent être révisées
        (dernière révision + intervalle <= maintenant).
        """
        maintenant = datetime.now()
        a_reviser = []
        for fiche in self.fiches:
            prochaine_revision = fiche.derniere_revision.replace() \
                + timedelta(days=fiche.intervalle)

            if prochaine_revision <= maintenant:
                a_reviser.append(fiche)

        return a_reviser

    # ----------------------------------------------------------
    # Import / Export interne (pour StorageManager)
    # ----------------------------------------------------------

    def charger_fiches(self, fiches: List[forms]):
        """
        Charge une liste de fiches depuis le stockage.
        Réinitialise le système d'ID.
        """
        self.fiches = fiches
        if fiches:
            self._next_id = max(f.id for f in fiches) + 1
        else:
            self._next_id = 1

    def toutes_les_fiches(self) -> List[forms]:
        """Renvoie toutes les fiches existantes."""
        return self.fiches

"""
class SpacesRepetitionEngine:

class StorageManager

class StatsManager

class MotivationEngine
"""