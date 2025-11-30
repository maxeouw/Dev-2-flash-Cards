import tkinter as tk
from tkinter import ttk


class ManagePaquetsPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager

        ttk.Label(
            self,
            text="Liste des paquets",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)

        # --- TABLEAU DES PAQUETS ---
        columns = ("id", "nom", "nb_fiches")

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("nom", text="Nom du paquet")
        self.tree.heading("nb_fiches", text="Nombre de fiches")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("nom", width=300)
        self.tree.column("nb_fiches", width=150, anchor="center")

        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        # --- Double-clic futur (ex: gérer contenu du deck) ---
        # self.tree.bind("<Double-1>", self.on_double_click)

        ttk.Button(
            self,
            text="Retour",
            command=lambda: controller.show_page("FichesView")
        ).pack(pady=15)

    # --------------------------------------------------
    def update_list(self):
        """Recharge les decks dans le tableau."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        decks = self.forms_manager.tous_les_decks()

        for deck in decks:
            self.tree.insert(
                "",
                "end",
                values=(deck.id, deck.nom, len(deck.fiche_ids))
            )
