from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class Form:
    id: int
    question: str
    reponse: str
    tags: List[str] = field(default_factory=list)
    date_creation: datetime = field(default_factory=datetime.now)
    derniere_revision: datetime = field(default_factory=datetime.now)
    intervalle: int = 1
    niveau: int = 0
    media: List[str] = field(default_factory=list)

    @property
    def titre(self) -> str:
        """Alias pour compatibilité : le titre = la question."""
        return self.question



@dataclass
class deck:
    pass