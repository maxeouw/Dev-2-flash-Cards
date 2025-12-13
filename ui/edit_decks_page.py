import tkinter as tk
from tkinter import ttk, messagebox, Toplevel

class DeckDetailPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager
        self.deck = None  # deck actuellement affiché

        self.title_label = ttk.Label(
            self, text="Détails du deck", font=("Segoe UI", 16, "bold")
        )
        self.title_label.pack(pady=20)

        # --- Champ pour modifier le nom du deck ---
        self.nom_frame = ttk.Frame(self)
        self.nom_frame.pack(pady=10)

        ttk.Label(self.nom_frame, text="Nom :", font=("Segoe UI", 12)).pack(side="left", padx=5)

        self.nom_var = tk.StringVar()
        self.nom_entry = ttk.Entry(self.nom_frame, textvariable=self.nom_var, width=40)
        self.nom_entry.pack(side="left", padx=5)

        # --- Nombre de fiches ---
        self.nb_label = ttk.Label(self, text="Nombre de fiches : 0", font=("Segoe UI", 12))
        self.nb_label.pack(pady=10)

        # --- Boutons purement UI (non fonctionnels pour l'instant) ---
        ttk.Button(self, text="Supprimer le deck").pack(pady=10)
        ttk.Button(self, text="Lier une fiche",command=self.ouvrir_fenetre_selection).pack(pady=10)

        # --- Retour ---
        ttk.Button(
            self,
            text="Retour",
            command=lambda: controller.show_page("DeckList")
        ).pack(pady=20)

    # ------------------------------------------------------
    def charger_deck(self, deck_id: int):
        """Charge les infos dans l'UI (affichage uniquement)."""
        deck = next((d for d in self.forms_manager.decks if d.id == deck_id), None)

        if deck is None:
            self.title_label.config(text="Erreur : deck introuvable")
            self.nom_var.set("")
            self.nb_label.config(text="")
            return

        self.deck = deck

        self.title_label.config(text=f"deck #{deck.id}")
        self.nom_var.set(deck.nom)                      # ← Remplace le label par un Entry éditable
        self.nb_label.config(text=f"Nombre de fiches : {len(deck.fiche_ids)}")


    def ouvrir_fenetre_selection(self):
        """Ouvre une popup pour choisir une fiche."""
        if not self.deck:
            return

        # Pop-up
        top = Toplevel(self)
        top.title(f"Ajouter au deck : {self.deck.nom}")
        top.geometry("600x400")

        ttk.Label(top, text="Double-cliquez sur une fiche pour l'ajouter").pack(pady=10)

        columns = ("id", "question")
        tree = ttk.Treeview(top, columns=columns, show="headings")
        tree.heading("id", text="ID")
        tree.heading("question", text="Question")
        tree.column("id", width=50)
        tree.column("question", width=450)
        tree.pack(fill="both", expand=True, padx=10, pady=5)

        toutes = self.forms_manager.toutes_les_fiches()
        for f in toutes:
            if f.id not in self.deck.fiche_ids:
                tree.insert("", "end", values=(f.id, f.question))

        # Double clic
        tree.bind("<Double-1>", lambda e: self.valider_ajout(tree, top))

    def valider_ajout(self, tree, window):
        """Appelée quand on clique sur une fiche dans la popup."""
        selection = tree.selection()
        if not selection:
            return

        item = selection[0]
        valeurs = tree.item(item, "values")
        fiche_id = int(valeurs[0])

        succes = self.forms_manager.ajouter_fiche_a_deck(self.deck.id, fiche_id)

        if succes:
            messagebox.showinfo("Succès", "Fiche ajoutée au deck !")
            self.nb_label.config(text=f"Nombre de fiches : {len(self.deck.fiche_ids)}")
            window.destroy()
        else:
            messagebox.showerror("Erreur", "Impossible d'ajouter la fiche.")