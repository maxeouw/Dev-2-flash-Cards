import tkinter as tk
from tkinter import ttk


class ListeFichesPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager, audio_manager=None):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager
        self.audio_manager = audio_manager
        self.buttons = []

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


        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=15)
        
        # --- Bouton retour ---
        self.btn_retour = ttk.Button(
            self,
            text="Retour",
            command=lambda: controller.show_page("FichesView")
        )
        self.btn_retour.pack(pady=15)

        # --- Bouton Ajouter deck ---

        ttk.Button(
            btn_frame,
            text="Ajouter une fiche",
            command=lambda: controller.show_page("AddForm")
        ).pack(side="left", padx=10, ipadx=10, ipady=5)

        # --- ACCESSIBILITÉ ---
        if self.audio_manager:
            self.buttons = self.audio_manager.setup_full_accessibility(self, controller, "FichesView")
            
            if self.buttons:
                self.buttons[0].bind("<Up>", lambda e: self.focus_tree())

    def focus_tree(self):
        """Redonne le focus au tableau"""
        self.tree.focus_set()
        if self.audio_manager and self.audio_manager.actif:
            sel = self.tree.selection()
            msg = f"Tableau des fiches. {self.tree.item(sel[0], 'values')[1]}" if sel else "Tableau des fiches"

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
                premier_btn = self.buttons[0] if self.buttons else None
                self.audio_manager.setup_treeview_accessibility(
                self.tree,
                self.speak_selection,
                validate_callback=lambda e: self.on_double_click(e),
                back_callback=lambda e: self.btn_retour.invoke(),
                next_widget=premier_btn
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
