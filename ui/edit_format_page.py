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
            reponses_texte = '\n'.join(fiche.reponses)
            self.reponse_text.insert("1.0", reponses_texte)

    # ----------------------------------------------------------
    def modifier_fiche(self):
        """Modifie la fiche dans la base de données."""
        question = self.question_entry.get().strip()
        reponses_text = self.reponse_text.get("1.0", "end").strip()  

        if not question or not reponses_text:
            messagebox.showerror("Erreur", "La question et au moins une réponse sont obligatoires.")
            return

        reponses = [r.strip() for r in reponses_text.split('\n') if r.strip()]
    
        if not reponses:
            messagebox.showerror("Erreur", "Veuillez entrer au moins une réponse.")
            return

        fiche = self.forms_manager.get_form(self.fiche_id)
        fiche.question = question
        fiche.reponses = reponses  
    
        self.forms_manager.modify_form(fiche)

        page = self.controller.pages["FormList"]
        page.update_list()
        self.controller.show_page("FormList")

    # ----------------------------------------------------------
    def supprimer_fiche(self):
        """Supprime la fiche de la base de données."""
        #if messagebox.askyesno("Êtes-vous sûr de bien vouloir supprimer cette fiche ?"):
        self.forms_manager.delete_form(self.fiche_id)
            
            #messagebox.showinfo("La fiche a bien été suprimée")
            
        # Retour à la liste
        page = self.controller.pages["FormList"]
        page.update_list()
        self.controller.show_page("FormList")
