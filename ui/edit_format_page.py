import tkinter as tk
from tkinter import ttk, messagebox

class EditFormPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager
        self.fiche_id = None  # ID de la fiche en cours d'édition

        ttk.Label(self, text="Modifier une fiche", font=("Segoe UI", 16, "bold")).pack(
            pady=20
        )

        # --- Champ Question ---
        ttk.Label(self, text="Question :").pack(anchor="w", padx=20)
        self.question_entry = ttk.Entry(self, width=60)
        self.question_entry.pack(padx=20, pady=5)

        # --- Champ Réponse ---
        ttk.Label(self, text="Réponse :").pack(anchor="w", padx=20)
        self.reponse_text = tk.Text(self, width=60, height=8)
        self.reponse_text.pack(padx=20, pady=5)

        # --- Boutons ---
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Modifier la fiche", command=self.modifier_fiche).pack(
            side="left", padx=10
        )
        
        ttk.Button(btn_frame, text="Supprimer la fiche", command=self.supprimer_fiche).pack(
            side="left", padx=10
        )
        
        ttk.Button(btn_frame, text="Retour", command=lambda: controller.show_page("FormList")).pack(
            side="left", padx=10
        )

    # ----------------------------------------------------------
    def charger_fiche(self, fiche_id):
        """Charge la fiche à éditer."""
        self.fiche_id = fiche_id
        fiche = self.forms_manager.get_form(fiche_id)
        
        if fiche:
            self.question_entry.delete(0, "end")
            self.question_entry.insert(0, fiche.question)
            
            self.reponse_text.delete("1.0", "end")
            self.reponse_text.insert("1.0", fiche.reponse)

    # ----------------------------------------------------------
    def modifier_fiche(self):
        """Modifie la fiche dans la base de données."""
        question = self.question_entry.get().strip()
        reponse = self.reponse_text.get("1.0", "end").strip()

        if not question or not reponse:
            messagebox.showerror("Erreur", "La question et la réponse sont obligatoires.")
            return

        # Récupère la fiche originale
        fiche = self.forms_manager.get_form(self.fiche_id)
        
        # Modifie les attributs
        fiche.question = question
        fiche.reponse = reponse
        
        # Sauvegarde la modification
        self.forms_manager.modify_form(fiche)

        messagebox.showinfo("Succès", "La fiche a été modifiée !")
        
        # Retour à la liste
        page = self.controller.pages["FormList"]
        page.update_list()
        self.controller.show_page("FormList")

    # ----------------------------------------------------------
    def supprimer_fiche(self):
        """Supprime la fiche de la base de données."""
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cette fiche ?"):
            self.forms_manager.delete_form(self.fiche_id)
            
            messagebox.showinfo("Succès", "La fiche a été supprimée !")
            
            # Retour à la liste
            page = self.controller.pages["FormList"]
            page.update_list()
            self.controller.show_page("FormList")
