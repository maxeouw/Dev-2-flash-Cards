import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class RevisionSessionPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager

        self.fiches = []
        self.current_index = 0
        self.deck_id_filter = None  # ID deck à réviser (None = tous)

        ttk.Label(
            self,
            text="Session de révision",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)

        # Zone pour afficher la question
        self.question_label = ttk.Label(self, text="", font=("Segoe UI", 13), wraplength=500)
        self.question_label.pack(pady=10)

        # Champ de réponse de l'utilisateur
        self.reponse_entry = ttk.Entry(self, width=50)
        self.reponse_entry.pack(pady=10)

        # Réponse correcte
        self.reponse_correcte_label = ttk.Label(self, text="", font=("Segoe UI", 11, "italic"))
        self.reponse_correcte_label.pack(pady=10)

        # Bouton "Valider"
        self.valider_btn = ttk.Button(self, text="Valider", command=self.valider_reponse)
        self.valider_btn.pack(pady=5)

        # Bouton "Suivant"
        self.suivant_btn = ttk.Button(self, text="Suivant", command=self.question_suivante, state="disabled")
        self.suivant_btn.pack(pady=5)

        # Bouton retour
        ttk.Button(
            self,
            text="Retour",
            command=lambda: controller.show_page("Revision")
        ).pack(pady=20)

    # -----------------------------------------------------------------------

    def start_session(self):
        """Lancée automatiquement quand on arrive sur la page."""
        if self.deck_id_filter is not None:
            # Si filtre actif, on charge uniquement ce deck
            self.fiches = self.forms_manager.get_fiches_by_deck_id(self.deck_id_filter)
            self.deck_id_filter = None # IMPORTANT: reset après usage (pour avoir toutes les fiches en mode "tout étudier")
        else:
            # Par défaut tout étudier
            self.fiches = self.forms_manager.toutes_les_fiches()

        if not self.fiches:
            messagebox.showinfo("Révision", "Aucune fiche à réviser.")
            self.controller.show_page("RevisionPage")
            return

        self.current_index = 0
        self.afficher_question()

    # -----------------------------------------------------------------------

    def afficher_question(self):
        fiche = self.fiches[self.current_index]

        self.question_label.config(text=f"Question : {fiche.question}")
        self.reponse_entry.delete(0, tk.END)
        self.reponse_correcte_label.config(text="")
        self.suivant_btn.config(state="disabled")
        self.valider_btn.config(state="normal")

    # -----------------------------------------------------------------------

    def valider_reponse(self):
        fiche = self.fiches[self.current_index]

        user_answer = self.reponse_entry.get()

        # Affiche la réponse correcte
        self.reponse_correcte_label.config(
            text=f"Réponse correcte : {fiche.reponse}"
        )

        # Mise à jour simple de la révision
        fiche.niveau += 1
        fiche.intervalle = max(1, fiche.intervalle + 1)
        fiche.derniere_revision = datetime.now()

        # Désactive validation jusqu'à prochaine question
        self.valider_btn.config(state="disabled")
        self.suivant_btn.config(state="normal")

    # -----------------------------------------------------------------------

    def question_suivante(self):
        self.current_index += 1

        if self.current_index >= len(self.fiches):
            #messagebox.showinfo("Révision", "Révision terminée !")
            self.controller.show_page("Revision")
            return

        self.afficher_question()
