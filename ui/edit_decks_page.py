import tkinter as tk
from tkinter import ttk

class DeckDetailPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager
        self.deck = None  # deck actuellement affiché

        self.title_label = ttk.Label(
            self, text="Détails du paquet", font=("Segoe UI", 16, "bold")
        )
        self.title_label.pack(pady=20)

        # --- Champ pour modifier le nom du deck ---
        self.nom_frame = ttk.Frame(self)
        self.nom_frame.pack(pady=10)

        ttk.Label(self.nom_frame, text="Nom :", font=("Segoe UI", 12)).pack(side="left", padx=5)

        self.nom_var = tk.StringVar()
        self.nom_entry = ttk.Entry(self.nom_frame, textvariable=self.nom_var, width=40)
        self.nom_entry.pack(side="left", padx=5)

        # --- Nombre de fiches ---
        self.nb_label = ttk.Label(self, text="Nombre de fiches : 0", font=("Segoe UI", 12))
        self.nb_label.pack(pady=10)

        # --- Boutons purement UI (non fonctionnels pour l'instant) ---
        ttk.Button(self, text="Supprimer le paquet").pack(pady=10)
        ttk.Button(self, text="Lier une fiche").pack(pady=10)

        # --- Retour ---
        ttk.Button(
            self,
            text="Retour",
            command=lambda: controller.show_page("DeckList")
        ).pack(pady=20)

    # ------------------------------------------------------
    def charger_deck(self, deck_id: int):
        """Charge les infos dans l'UI (affichage uniquement)."""
        deck = next((d for d in self.forms_manager.decks if d.id == deck_id), None)

        if deck is None:
            self.title_label.config(text="Erreur : deck introuvable")
            self.nom_var.set("")
            self.nb_label.config(text="")
            return

        self.deck = deck

        self.title_label.config(text=f"Paquet #{deck.id}")
        self.nom_var.set(deck.nom)                      # ← Remplace le label par un Entry éditable
        self.nb_label.config(text=f"Nombre de fiches : {len(deck.fiche_ids)}")
