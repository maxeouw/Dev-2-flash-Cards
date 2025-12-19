import tkinter as tk
from tkinter import ttk


class ListeFichesPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager, audio_manager=None):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager
        self.audio_manager = audio_manager

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

        # --- Double-clic pour éditer ---
        self.tree.bind("<Double-1>", self.on_double_click)

        # --- Bouton retour ---
        self.btn_retour = ttk.Button(
            self,
            text="Retour",
            command=lambda: controller.show_page("FichesView")
        )
        self.btn_retour.pack(pady=15)

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

            if self.audio_manager:
                self.audio_manager.setup_treeview_accessibility(
                self.tree,
                self.speak_selection,
                validate_callback=lambda e: self.on_double_click(e),
                back_callback=lambda e: self.btn_retour.invoke()
                )
    # --------------------------------------------------
    def on_double_click(self, event):
        """Gère le double-clic sur une fiche."""
        selection = self.tree.selection()
        
        if not selection:
            return
        
        # Récupère l'ID de la fiche sélectionnée
        item = selection[0]
        values = self.tree.item(item, 'values')
        fiche_id = int(values[0])
        
        # Charge la fiche dans la page d'édition
        edit_page = self.controller.pages["EditForm"]
        edit_page.charger_fiche(fiche_id)
        
        # Affiche la page d'édition
        self.controller.show_page("EditForm")

    def speak_selection(self, event):
        if not self.audio_manager or not self.audio_manager.actif: return
        
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item, "values")
            self.audio_manager.parler(f"Fiche {values[0]} : {values[1]}")
