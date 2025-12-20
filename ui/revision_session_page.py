import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random
<<<<<<< HEAD


=======
>>>>>>> refs/remotes/origin/main
class RevisionSessionPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager, audio_manager=None):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager
        self.fiches = []
        self.current_index = 0
        self.deck_id_filter = None  # ID deck à réviser (None = tous)
        self.audio_manager = audio_manager
        self.widgets_nav = []


        #ici cest pour les stats
        self.session_total_cards = 0
        self.session_failed_cards = 0
        self.current_deck_id = None
        
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
        self.reponse_entry.bind("<Return>", lambda event: self.question_suivante() if str(self.suivant_btn['state']) == 'normal' else self.valider_reponse())
        self.reponse_entry.bind("<Return>", lambda event: self.question_suivante() if str(self.suivant_btn['state']) == 'normal' else self.valider_reponse())

        # Champ VRAI / FAUX
        self.feedback_label = ttk.Label(self, text="", font=("Segoe UI", 12, "bold"))
        self.feedback_label.pack(pady=5)

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

        # Raccourcis clavier
        self.valider_btn.bind("<Up>", lambda e: self.audio_manager.parler("Bouton valider") if self.audio_manager else None)
        self.suivant_btn.bind("<Up>", lambda e: self.audio_manager.parler("Bouton suivant") if self.audio_manager else None)

    # -----------------------------------------------------------------------

    def start_session(self):
        """Lancée automatiquement quand on arrive sur la page."""
        if self.deck_id_filter is not None:
             # Si filtre actif, on charge uniquement ce deck
            self.fiches = self.forms_manager.get_fiches_by_deck_id(self.deck_id_filter)
            random.shuffle(self.fiches)
            self.current_deck_id = self.deck_id_filter   # NEW
            self.deck_id_filter = None  # reset
        else:
            # Par défaut tout étudier
            self.fiches = self.forms_manager.toutes_les_fiches()
            random.shuffle(self.fiches)
            self.current_deck_id = None  # signifie "tous les decks"

        if not self.fiches:
            messagebox.showinfo("Révision", "Aucune fiche à réviser.")
            self.controller.show_page("RevisionPage")
            return
        random.shuffle(self.fiches)
        # NEW: init session counters
        self.session_total_cards = len(self.fiches)
        self.session_failed_cards = 0

        self.current_index = 0
        self.afficher_question()


    # -----------------------------------------------------------------------

    def afficher_question(self):
        fiche = self.fiches[self.current_index]

        self.question_label.config(text=f"Question : {fiche.question}")
        if self.audio_manager:
            self.audio_manager.parler(f"Question {self.current_index + 1} : {fiche.question}")

        self.reponse_entry.delete(0, tk.END)
        self.reponse_correcte_label.config(text="")
        self.suivant_btn.config(state="disabled")
        self.valider_btn.config(state="normal")
        self.feedback_label.config(text="")
        self.reponse_entry.focus_set()
        if self.audio_manager:
            self.after(2500, lambda: self.audio_manager.parler("Zone de saisie active"))
    # -----------------------------------------------------------------------

    def valider_reponse(self):
        fiche = self.fiches[self.current_index]
        user_answer = self.reponse_entry.get()

        # Normaliser la réponse de l'utilisateur
        reponse_clean = user_answer.strip().lower()

        # Vérifier si elle correspond à une des réponses enregistrées
        self.resultat_reussite = False
        for reponse_attendue in fiche.reponses:  
            if reponse_clean == reponse_attendue.strip().lower():
                self.resultat_reussite = True
                break
            reponses_text = " ou ".join(fiche.reponses)

        if self.resultat_reussite:
            self.audio_manager.parler("Réponse validée")
            self.feedback_label.config(text="✅ VRAI", foreground="green")
            self.reponse_correcte_label.config(text="Bravo !")
        else:
            self.audio_manager.parler(f"Réponse incorrecte. {reponses_text}")
            self.feedback_label.config(text="❌ FAUX", foreground="red")
            #ici pour stats +1 par faux
            self.session_failed_cards += 1
            # Afficher TOUTES les réponses possibles
            reponses_text = " ou ".join(fiche.reponses)
            self.reponse_correcte_label.config(text=f"Réponse incorrecte : {reponses_text}")
            
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
            # Fin de session : enregistrer les stats
            self._sauvegarder_stats_session()

            # Calcul des infos de la session
            total = self.session_total_cards
            fails = self.session_failed_cards
            success_rate = 0
            if total > 0:
                success_rate = (total - fails) / total * 100.0

            # Configurer la page de fin de session
            end_page = self.controller.pages["EndSession"]
            end_page.configure_result(self.current_deck_id, success_rate, total, fails)

            # Audio si actif
            if self.audio_manager and self.audio_manager.actif:
                self.audio_manager.parler("Révision terminée.")
                self.audio_manager.parler(
                    f"Tu as réussi {int(success_rate)} pour cent des cartes."
                )

            # Aller sur la page de fin
            self.controller.show_page("EndSession")
            return

        # Sinon, on affiche la question suivante
        self.afficher_question()
    def _sauvegarder_stats_session(self):
        """
        Appelée uniquement quand la session est allée jusqu'au bout.
        """
        try:
            total = self.session_total_cards
            fails = self.session_failed_cards
            deck_id = self.current_deck_id

            # StorageManager is in main_window: MainWindow.storage_manager
            # FormsManager already has a reference to it as self.storage
            storage = self.forms_manager.storage
            storage.add_stats_session(deck_id, total, fails)
        except Exception as e:
            print("Erreur lors de la sauvegarde des stats :", e)

