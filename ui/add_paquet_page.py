import tkinter as tk
from tkinter import ttk, messagebox
from core.formManager import DeckCreationError



class AddPaquetPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager

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



    def creer_deck(self, event=None):
        nom = self.nom_deck_entry.get() 

        try:
            # On tente de créer le deck
            deck = self.forms_manager.create_deck(nom)
            
            # Si succès (POST effectif dans l'UI)
            self.nom_deck_entry.delete(0, "end")
            messagebox.showinfo("Succès", f"Le deck '{deck.nom}' a bien été créé !")
            
        except DeckCreationError as e:
            # On attrape l'exception pour ne pas faire crasher l'app
            messagebox.showerror("Erreur de création", str(e))

