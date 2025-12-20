# ui/end_session_page.py
import tkinter as tk
from tkinter import ttk

class EndOfSessionPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager, audio_manager=None):
        super().__init__(parent)
        self.controller = controller
        self.forms_manager = forms_manager
        self.audio_manager = audio_manager
        self.buttons = []

        self.deck_id = None
        self.success_rate = 0
        self.total = 0
        self.fails = 0

        ttk.Label(
            self,
            text="Résultat de ta session",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)

        self.message_label = ttk.Label(self, text="", font=("Segoe UI", 12), wraplength=500)
        self.message_label.pack(pady=10)

        # Bouton pour voir le graphe de ce deck
        self.graph_button = ttk.Button(
            self,
            text="Voir ton graphe 📈",
            command=self.go_to_graph
        )
        self.graph_button.pack(pady=5)

        # Bouton pour revenir à la révision
        ttk.Button(
            self,
            text="Retour à la révision",
            command=lambda: controller.show_page("Revision")
        ).pack(pady=10)

        # --- Accessibilité ---
        if self.audio_manager:
            # On configure la navigation et on stocke les boutons
            self.buttons = self.audio_manager.setup_full_accessibility(self, controller, "Revision")

    def configure_result(self, deck_id, success_rate, total, fails):
        """Appelée par RevisionSessionPage à la fin de la session."""
        self.deck_id = deck_id
        self.success_rate = success_rate
        self.total = total
        self.fails = fails

        if success_rate >= 80:
            titre = "Bravo ! 🎉"
            texte = (
                f"{titre}\n\nTu as réussi {success_rate:.0f}% des cartes "
                f"({total - fails}/{total}). Continue comme ça !"
            )
        elif success_rate >= 50:
            titre = "Bien joué 👍"
            texte = (
                f"{titre}\n\nTu as réussi {success_rate:.0f}% des cartes "
                f"({total - fails}/{total}). Il y a encore un peu de travail."
            )
        else:
            titre = "Courage 💪"
            texte = (
                f"{titre}\n\nTu as réussi seulement {success_rate:.0f}% des cartes "
                f"({total - fails}/{total}). Revois surtout les cartes ratées."
            )

        self.message_label.config(text=texte)

        # Si deck_id est None (révision de tous les decks), le graphe n'a pas de deck précis
        if deck_id is None:
            self.graph_button.config(state="disabled")
        else:
            self.graph_button.config(state="normal")

    def go_to_graph(self):
        """Ouvre la page Stats avec ce deck déjà sélectionné et son graphe."""
        if self.deck_id is None:
            return
        stats_page = self.controller.pages["Stats"]
        # Recharge la combobox decks
        stats_page.load_decks_into_combobox()

        # Trouver le nom du deck à partir de l'id
        decks = self.forms_manager.tous_les_decks()
        deck_name = None
        for d in decks:
            if d.id == self.deck_id:
                deck_name = d.nom
                break

        if deck_name is None:
            return

        # Sélection dans la combobox
        stats_page.deck_var.set(deck_name)
        # Lancer le graphe pour ce deck
        stats_page.show_graph_for_selected_deck()

        self.controller.show_page("Stats")

    def focus_button_if_enabled(self):
        if self.audio_manager and self.audio_manager.actif:
            texte_resultat = self.message_label.cget("text")
            self.audio_manager.parler(texte_resultat)
            if self.buttons:
                self.buttons[-1].focus_set()
