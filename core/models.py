from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class FlashCard:
    id: int
    question: str
    tags: List[str] = field(default_factory=list)
    date_creation: datetime = field(default_factory=datetime.now)
    derniere_revision: datetime = field(default_factory=datetime.now)
    intervalle: int = 1
    niveau: int = 0
    media: List[str] = field(default_factory=list)
    reponses: List[str] = field(default_factory=list)  

    @property
    def titre(self) -> str:
        """Alias pour compatibilité : le titre = la question."""
        return self.question
    
    @property
    def reponse(self) -> str:
        """Retourne la première réponse (pour compatibilité avec ancien code)"""
        return self.reponses[0] if self.reponses else ""
    
    @reponse.setter
    def reponse(self, value):
        """Setter pour assigner une réponse (convertit en liste)"""
        if isinstance(value, str):
            self.reponses = [value]
        else:
            self.reponses = value if value else []


@dataclass
class Deck:
    id: int
    nom: str
    fiche_ids: List[int] = field(default_factory=list)

@dataclass
class Stats:
    """Représente une session de révision enregistré en base"""
    deck_id: Optional[int]
    date_session: datetime
    total_cards: int
    failed_cards: int
    success_rate: float  # 0–100

    @property
    def fail_rate(self) -> float:
        """Pourcentage d'échec, calculé à partir du taux de réussi"""
        return 100.0 - self.success_rate