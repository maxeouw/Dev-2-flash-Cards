import tkinter as tk
from tkinter import ttk


class ManagePaquetsPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager, audio_manager=None):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager
        self.audio_manager = audio_manager

        ttk.Label(
            self,
            text="Liste des decks",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)

        # --- TABLEAU DES DECKS ---
        columns = ("id", "nom", "nb_fiches")

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("nom", text="Nom du deck")
        self.tree.heading("nb_fiches", text="Nombre de fiches")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("nom", width=300)
        self.tree.column("nb_fiches", width=150, anchor="center")

        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        # --- Double-clic futur (ex: gérer contenu du deck) ---
        self.tree.bind("<Double-1>", self.on_double_click)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=15)
        
        # --- Ajouter un deck ---
        ttk.Button(
            btn_frame,
            text="Ajouter un deck",
            command=lambda: controller.show_page("AddPaquet")
        ).pack(side="left", padx=10, ipadx=10, ipady=5)

        # --- Bouton Retour ---
        self.btn_retour = ttk.Button(
            self,
            text="Retour",
            command=lambda: controller.show_page("FichesView"))
        self.btn_retour.pack(pady=15)

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

   # Accessibilité
        if self.audio_manager:
            self.audio_manager.setup_treeview_accessibility(
            self.tree,
            self.speak_selection,
            validate_callback=lambda e: self.on_double_click(e),
            back_callback=lambda e: self.btn_retour.invoke()
        )
    
    def on_double_click(self, event):
        """Ouvre la page de détails du deck sélectionné."""
        selection = self.tree.selection()
        if not selection:
            return

        item = selection[0]
        values = self.tree.item(item, "values")
        deck_id = int(values[0])

        # Récupération de la page dans le controller
        deck_page = self.controller.pages["deckGestion"]

        # Charger les infos du deck dans la page
        deck_page.charger_deck(deck_id)

        # Afficher la page
        self.controller.show_page("deckGestion")

    def speak_selection(self, event):
        if not self.audio_manager or not self.audio_manager.actif:
            return
        
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item, "values")
            # values[1] c'est le nom, values[2] c'est le nombre de fiches
            nom = values[1]
            nb = values[2]
            self.audio_manager.parler(f"Deck : {nom}, {nb} fiches")