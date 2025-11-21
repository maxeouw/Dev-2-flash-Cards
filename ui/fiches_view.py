import tkinter as tk
from tkinter import ttk, messagebox

class AddFormPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager

        ttk.Label(self, text="Créer une nouvelle fiche", font=("Segoe UI", 16, "bold")).pack(
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

        ttk.Button(btn_frame, text="Créer la fiche", command=self.creer_fiche).pack(
            side="left", padx=10
        )

        ttk.Button(btn_frame, text="Retour", command=lambda: controller.show_page("MainMenu")).pack(
            side="left", padx=10
        )

    # ----------------------------------------------------------
    def creer_fiche(self):
        question = self.question_entry.get().strip()
        reponse = self.reponse_text.get("1.0", "end").strip()
        tags_raw = self.tags_entry.get().strip()

        if not question or not reponse:
            messagebox.showerror("Erreur", "La question et la réponse sont obligatoires.")
            return

        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

        self.forms_manager.create_form(question, reponse, tags)

        messagebox.showinfo("Succès", "La fiche a été créée !")

        self.question_entry.delete(0, "end")
        self.reponse_text.delete("1.0", "end")
        self.tags_entry.delete(0, "end")
