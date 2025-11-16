from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class Fiche:
    id: int
    titre: str
    contenu: str
    tags: List[str] = field(default_factory=list)
    date_creation: datetime = field(default_factory=datetime.now)
    derniere_revision: datetime = field(default_factory=datetime.now)
    intervalle: int = 1
    niveau: int = 0
    media: List[str] = field(default_factory=list)
