import tkinter as tk
from tkinter import ttk


class ListeFichesPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager

        ttk.Label(
            self,
            text="Liste des fiches",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)

        # --- TABLEAU DES FICHES ---
        columns = ("id", "question", "reponse")

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("question", text="Question")
        self.tree.heading("reponse", text="Réponse")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("question", width=300)
        self.tree.column("reponse", width=300)

        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        # --- Bouton retour ---
        ttk.Button(
            self,
            text="Retour",
            command=lambda: controller.show_page("FichesView")
        ).pack(pady=15)

    # --------------------------------------------------
    def update_list(self):
        """Recharge les fiches dans le tableau."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        fiches = self.forms_manager.toutes_les_fiches()

        for fiche in fiches:
            self.tree.insert(
                "",
                "end",
                values=(fiche.id, fiche.question, fiche.reponse)
            )
