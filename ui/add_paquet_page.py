import tkinter as tk
from tkinter import ttk, messagebox


class AddPaquetPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager

        ttk.Label(
            self,
            text="Créer un nouveau paquet",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=30)

        # --- Champ Nom du paquet ---
        ttk.Label(self, text="Nom du paquet :").pack(anchor="w", padx=20)
        self.nom_paquet_entry = ttk.Entry(self, width=50)
        self.nom_paquet_entry.pack(padx=20, pady=10)
        self.nom_paquet_entry.bind("<Return>", self.creer_paquet)

        # --- Boutons d’action ---
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=25)

        ttk.Button(
            btn_frame,
            text="Créer le paquet",
            command=self.creer_paquet
        ).pack(side="left", padx=10, ipadx=10, ipady=5)

        ttk.Button(
            btn_frame,
            text="Retour",
            command=lambda: controller.show_page("FichesView")
        ).pack(side="left", padx=10, ipadx=10, ipady=5)

    def creer_paquet(self, event=None):
        nom = self.nom_paquet_entry.get().strip()

        if not nom:
            messagebox.showerror("Erreur", "Le nom du paquet est obligatoire.")
            return

        deck = self.forms_manager.create_deck(nom)
        
        self.nom_paquet_entry.delete(0, "end")
