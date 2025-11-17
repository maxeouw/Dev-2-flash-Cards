import tkinter as tk
from tkinter import ttk, simpledialog, messagebox


class FichesView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame")

        # --- TITRE ---
        lbl = ttk.Label(
            self,
            text="Mes listes de fiches",
            font=("Segoe UI", 14, "bold"),
            background="#f8f9fa"
        )
        lbl.pack(pady=18)

        # --- CONTENEUR DES LISTES ---
        self.lists_frame = ttk.Frame(self)
        self.lists_frame.pack(padx=24, pady=7, fill=tk.BOTH, expand=True)

        # --- BOUTON CREER UNE LISTE ---
        creer_liste_btn = ttk.Button(self, text="Créer une nouvelle liste", command=self.creer_liste)
        creer_liste_btn.pack(pady=8)

        # --- BOUTON RETOUR ---
        btn_retour = ttk.Button(
            self,
            text="⬅ Retour",
            command=lambda: controller.show_page("MainMenu")
        )
        btn_retour.pack(pady=12)

        # --- DONNÉES DE TEST ---
        self.lists = ["Électricité", "Histoire", "Maths"]
        
        self.refresh_lists()

    # -----------------------------------------------------------
    # LOGIQUE DE GESTION DES LISTES
    # -----------------------------------------------------------
    def creer_liste(self):
        nom = simpledialog.askstring("Nouvelle liste", "Nom de la nouvelle liste :", parent=self)
        if nom and nom not in self.lists:
            self.lists.append(nom)
            self.refresh_lists()

    def refresh_lists(self):
        for widget in self.lists_frame.winfo_children():
            widget.destroy()

        for idx, nom in enumerate(self.lists):
            row = ttk.Frame(self.lists_frame)
            row.pack(side=tk.TOP, fill=tk.X, pady=2)

            lbl = ttk.Label(row, text=nom, font=("Segoe UI", 12), width=62)
            lbl.pack(side=tk.LEFT, padx=(5, 8))

            # --- Bouton MODIFIER ---
            btn_modif = ttk.Button(
                row, text="Modifier", width=10,
                command=lambda i=idx: self.modifier_liste(i)
            )
            btn_modif.pack(side=tk.LEFT, padx=3)

            # --- Bouton SUPPRIMER ---
            btn_suppr = ttk.Button(
                row, text="Supprimer", width=10,
                command=lambda i=idx: self.supprimer_liste(i)
            )
            btn_suppr.pack(side=tk.LEFT, padx=3)


    def supprimer_liste(self, idx):
        nom = self.lists[idx]
        if messagebox.askokcancel("Suppression", f"Supprimer la liste '{nom}' ?"):
            del self.lists[idx]
            self.refresh_lists()

