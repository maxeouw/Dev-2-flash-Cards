import tkinter as tk
from tkinter import ttk


class FichesViewPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager

        ttk.Label(
            self,
            text="Gestion des fiches et paquets",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=30)

        ttk.Button(
            self,
            text="➕ Ajouter une fiche",
            command=lambda: controller.show_page("AddForm")
        ).pack(pady=10, ipadx=10, ipady=5)

        ttk.Button(
            self,
            text="Gérer les fiches",
            command=lambda: self.open_forms_list()
        ).pack(pady=10, ipadx=10, ipady=5)
        
        ttk.Button(
            self,
            text="➕ Ajouter un paquet",
            command=lambda: controller.show_page("AddPaquet")
        ).pack(pady=10, ipadx=10, ipady=5)

        ttk.Button(
            self,
            text="Gérer les paquets",
            command=lambda: self.open_paquets_list()
        ).pack(pady=10, ipadx=10, ipady=5)

        ttk.Button(
            self,
            text="Retour",
            command=lambda: controller.show_page("MainMenu")
        ).pack(pady=10, ipadx=10, ipady=5)
    
    def open_forms_list(self):

        page = self.controller.pages["FormList"]
        page.update_list()

        self.controller.show_page("FormList")

    def open_paquets_list(self):
        # Recharger et afficher depuis la DB (pour avoir les nouveaux paquets)
        self.forms_manager.charger_decks_depuis_db()

        page = self.controller.pages["EditDecks"]
        page.update_list()
        self.controller.show_page("EditDecks")
