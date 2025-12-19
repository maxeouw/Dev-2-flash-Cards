import tkinter as tk
from tkinter import ttk, messagebox


class AddFormPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager, audio_manager=None):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager
        self.audio_manager = audio_manager

        ttk.Label(self, text="Créer une nouvelle fiche", font=("Segoe UI", 16, "bold")).pack(
            pady=20
        )

        # --- Champ Question ---
        ttk.Label(self, text="Question :").pack(anchor="w", padx=20)
        self.question_entry = ttk.Entry(self, width=60)
        self.question_entry.pack(padx=20, pady=5)

        if self.audio_manager:
            self.question_entry.bind("<FocusIn>", lambda e: self.audio_manager.parler("Champ Question"))

        # --- Champ Réponses (une par ligne) ---
        ttk.Label(self, text="Réponses (une par ligne) :").pack(anchor="w", padx=20)
        ttk.Label(self, text="Vous pouvez ajouter plusieurs réponses acceptées", 
                 font=("Segoe UI", 9, "italic")).pack(anchor="w", padx=20)
        self.reponse_text = tk.Text(self, width=60, height=8)
        self.reponse_text.pack(padx=20, pady=5)

        if self.audio_manager:
            self.reponse_text.bind("<FocusIn>", lambda e: self.audio_manager.parler("Champ Réponses, une par ligne"))

        # --- Boutons ---
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=20)

        self.btn_creer = ttk.Button(
            btn_frame, 
            text="Créer la fiche", 
            command=self.creer_fiche
        )
        self.btn_creer.pack(side="left", padx=10)

        self.btn_retour = ttk.Button(
            btn_frame, 
            text="Retour", 
            command=lambda: controller.show_page("FichesView")
        )
        self.btn_retour.pack(side="left", padx=10)



# Accessibilité
        if self.audio_manager:
            self.audio_manager.setup_full_accessibility(self, controller, "FichesView")

        def handle_tab_in_text(event):
            self.btn_creer.focus_set()
            return "break"

        self.reponse_text.bind("<Tab>", handle_tab_in_text)

        # Focus initial
        self.after(100, lambda: self.question_entry.focus_set())
        
    def focus_button_if_enabled(self):
                if self.audio_manager and self.audio_manager.actif:
                    self.question_entry.focus_set()
                    self.audio_manager.parler("Nouvelle fiche. Entrez la question.")

    # ----------------------------------------------------------
    def creer_fiche(self):
        """Crée une nouvelle fiche avec question et réponses multiples."""
        question = self.question_entry.get().strip()
        reponses_text = self.reponse_text.get("1.0", "end").strip()

        if not question or not reponses_text:
            messagebox.showerror("Erreur", "La question et au moins une réponse sont obligatoires.")
            return

        # Convertir le texte en liste de réponses (une par ligne)
        reponses = [r.strip() for r in reponses_text.split('\n') if r.strip()]

        if not reponses:
            messagebox.showerror("Erreur", "Veuillez entrer au moins une réponse.")
            return

        # Créer la fiche avec la liste de réponses
        fiche = self.forms_manager.create_form(question, reponses)

        print(f"\nNouvelle fiche créée :")
        print(f"ID : {fiche.id}")
        print(f"Question : {fiche.question}")
        print(f"Réponses : {fiche.reponses}\n")
        msg = "Fiche créée avec succès !"
        if self.audio_manager: self.audio_manager.parler(msg)

        # Vider les champs
        self.question_entry.delete(0, "end")
        self.reponse_text.delete("1.0", "end")
        
        messagebox.showinfo("Succès", "Fiche créée avec succès!")
