import tkinter as tk
from tkinter import ttk


class FichesViewPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager

        ttk.Label(
            self,
            text="Gestion des fiches",
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
            command=self.display_forms
        ).pack(pady=10, ipadx=10, ipady=5)
        
        ttk.Button(
            self,
            text="➕ Ajouter un paquet",
            command=lambda: controller.show_page("AddPaquet")
        ).pack(pady=10, ipadx=10, ipady=5)

        ttk.Button(
            self,
            text="Gérer les paquets"
        ).pack(pady=10, ipadx=10, ipady=5)

        ttk.Button(
            self,
            text="Retour",
            command=lambda: controller.show_page("MainMenu")
        ).pack(pady=10, ipadx=10, ipady=5)
    
    def display_forms(self):
        fiches = self.forms_manager.toutes_les_fiches()

        if not fiches:
            print("\n Aucune fiche n'a encore été créée.\n")
            return

        print("\n Fiches de la session :")
        print("----------------------------------------")

        for fiche in fiches:
            print(f"ID : {fiche.id}")
            print(f"Question : {fiche.question}")
            print(f"Réponse : {fiche.reponse}")
            print(f"Tags : {fiche.tags}")
            print("----------------------------------------")
