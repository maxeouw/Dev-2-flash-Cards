import tkinter as tk
from tkinter import ttk


class FichesViewPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager, audio_manager=None):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager
        self.audio_manager = audio_manager

        ttk.Label(
            self,
            text="Gestion des fiches et decks",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=30)

        ttk.Button(
            self,
            text="Ajouter une fiche",
            command=lambda: controller.show_page("AddForm")
        ).pack(pady=10, ipadx=10, ipady=5)

        ttk.Button(
            self,
            text="Gérer les fiches",
            command=lambda: self.open_forms_list()
        ).pack(pady=10, ipadx=10, ipady=5)
        
        ttk.Button(
            self,
            text="Ajouter un deck",
            command=lambda: controller.show_page("AddPaquet")
        ).pack(pady=10, ipadx=10, ipady=5)

        ttk.Button(
            self,
            text="Gérer les decks",
            command=lambda: self.open_paquets_list()
        ).pack(pady=10, ipadx=10, ipady=5)

        ttk.Button(
            self,
            text="Retour",
            command=lambda: controller.show_page("MainMenu")
        ).pack(pady=10, ipadx=10, ipady=5)

        if self.audio_manager:
            self.buttons = self.audio_manager.setup_full_accessibility(self, controller, "MainMenu")
            
            self.after(100, self.focus_button_if_enabled)
    
    def focus_button_if_enabled(self):
        if self.buttons:
            main_menu = self.controller.pages.get("MainMenu")
            if main_menu and hasattr(main_menu, 'mode_actif') and main_menu.mode_actif:
                self.buttons[0].focus_set()
                if self.audio_manager:
                    self.audio_manager.parler(f"Bouton : {self.buttons[0]['text']}")
    
    def open_forms_list(self):

        page = self.controller.pages["FormList"]
        page.update_list()

        self.controller.show_page("FormList")

    def open_paquets_list(self):
        # Recharger et afficher depuis la DB (pour avoir les nouveaux decks)
        self.forms_manager.charger_decks_depuis_db()

        page = self.controller.pages["DeckList"]
        page.update_list()
        self.controller.show_page("DeckList")
