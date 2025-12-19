import tkinter as tk
from tkinter import ttk, messagebox


class AddPaquetPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager, audio_manager=None):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager
        self.audio_manager = audio_manager
        ttk.Label(
            self,
            text="Créer un nouveau deck",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=30)

        # --- Champ Nom du deck ---
        ttk.Label(self, text="Nom du deck :").pack(anchor="w", padx=20)
        self.nom_deck_entry = ttk.Entry(self, width=50)
        self.nom_deck_entry.pack(padx=20, pady=10)
        self.nom_deck_entry.bind("<Return>", self.creer_deck)

        if self.audio_manager:
            self.nom_deck_entry.bind("<FocusIn>", lambda e: self.audio_manager.parler("Champ Nom du deck"))

        # --- Boutons d’action ---
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=25)

        ttk.Button(
            btn_frame,
            text="Créer le deck",
            command=self.creer_deck
        ).pack(side="left", padx=10, ipadx=10, ipady=5)

        ttk.Button(
            btn_frame,
            text="Retour",
            command=lambda: controller.show_page("FichesView")
        ).pack(side="left", padx=10, ipadx=10, ipady=5)

        if self.audio_manager:
            self.audio_manager.setup_full_accessibility(self, controller, "FichesView")
            self.buttons = self.audio_manager.setup_full_accessibility(self, controller, "FichesView")
        if self.buttons:
                self.nom_deck_entry.bind("<Down>", lambda e: self.buttons[0].focus_set())
                self.buttons[0].bind("<Up>", lambda e: self.nom_deck_entry.focus_set())

    def focus_button_if_enabled(self):
        if self.audio_manager and self.audio_manager.actif:
            self.nom_deck_entry.focus_set()
            self.audio_manager.parler("Nouveau deck. Entrez le nom.")

    def creer_deck(self, event=None):
        nom = self.nom_deck_entry.get().strip()

        if not nom:
            messagebox.showerror("Erreur", "Le nom du deck est obligatoire.")
            if self.audio_manager: self.audio_manager.parler("Erreur, nom vide")
            return

        deck = self.forms_manager.create_deck(nom)
        if self.audio_manager: self.audio_manager.parler(f"Deck {nom} créé")
        self.controller.show_page("MainMenu")
        self.nom_deck_entry.delete(0, "end")
