import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from core.formManager import DeckNotFoundError

class DeckDetailPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager, audio_manager=None):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager
        self.audio_manager = audio_manager
        self.deck = None  # deck actuellement affiché
        self.buttons = []

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

        # --- Contenu du deck ---
        ttk.Label(self, text="Contenu du deck :", font=("Segoe UI", 10, "bold")).pack(pady=(10, 0))
        
        self.tree = ttk.Treeview(self, columns=("id", "question"), show="headings", height=8)
        self.tree.heading("id", text="ID"); self.tree.column("id", width=50, anchor="center")
        self.tree.heading("question", text="Question"); self.tree.column("question", width=400)
        self.tree.pack(padx=20, pady=5, fill="both", expand=True)

        # --- Nombre de fiches ---
        self.nb_label = ttk.Label(self, text="Nombre de fiches : 0", font=("Segoe UI", 12))
        self.nb_label.pack(pady=10)


        # --- Boutons d'action ---
        ttk.Button(
            self,
            text="Supprimer le deck",
            command=self.supprimer_deck
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Lier une fiche",
            command=self.ouvrir_fenetre_selection
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Supprimer une fiche",
            command=self.retirer_fiche
        ).pack(pady=10)

        # --- Retour ---
        self.retour_btn = ttk.Button(
            self,
            text="Retour",
            command=lambda: controller.show_page("DeckList")
        )
        self.retour_btn.pack(pady=20)

        if self.audio_manager:
            self.buttons = audio_manager.setup_full_accessibility(self, controller, "DeckList")
        self.after(100, self.focus_button_if_enabled)

    def focus_button_if_enabled(self):
        """Exactement la même logique que dans revision_view.py"""
        if self.buttons:
            # On vérifie si le mode est actif dans le MainMenu
            main_menu = self.controller.pages.get("MainMenu")
            if main_menu and hasattr(main_menu, 'mode_actif') and main_menu.mode_actif:
                self.buttons[0].focus_set()
                if self.audio_manager:
                    self.audio_manager.parler(f"Bouton : {self.buttons[0]['text']}")

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
        self.nom_var.set(deck.nom)                      
        self.nb_label.config(text=f"Nombre de fiches : {len(deck.fiche_ids)}")
        self.update_table()

        if self.audio_manager:
            self.audio_manager.parler(f"Détails du deck {deck.nom}")

    def ouvrir_fenetre_selection(self):
        """Ouvre une popup pour choisir une fiche."""
        if not self.deck:
            return

        # Pop-up
        top = Toplevel(self)
        top.title(f"Ajouter au deck : {self.deck.nom}")
        top.geometry("600x400")

        if self.audio_manager:
            self.audio_manager.parler("Sélectionnez une fiche à ajouter. Flèche gauche pour annuler.")

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

        # Validation / Annulation
        valider = lambda e: self.valider_ajout(tree, top)
        tree.bind("<Double-1>", valider)
        tree.bind("<Return>", valider)
        tree.bind("<space>", valider)
        tree.bind("<Right>", valider)
        tree.bind("<Left>", lambda e: top.destroy())

        if self.audio_manager:
            self.audio_manager.setup_treeview_accessibility(
                tree, 
                speak_callback=lambda e: self.speak_fiche_selection(tree),
                validate_callback=valider,
                back_callback=lambda e: top.destroy()
            )

        # Focus au début
        tree.focus_set()
        if tree.get_children():
            premier = tree.get_children()[0]
            tree.selection_set(premier)
            tree.focus(premier)

    def valider_ajout(self, tree, window):
        """Appelée quand on clique sur une fiche dans la popup."""
        selection = tree.selection()
        if not selection:
            return

        item = selection[0]
        valeurs = tree.item(item, "values")
        fiche_id = int(valeurs[0])

        try:
            self.forms_manager.ajouter_fiche_a_deck(self.deck.id, fiche_id)

            if self.audio_manager:
                self.audio_manager.parler("Fiche ajoutée au deck")

            #messagebox.showinfo("Succès", "Fiche ajoutée au deck !")
            self.nb_label.config(
                text=f"Nombre de fiches : {len(self.deck.fiche_ids)}"
            )
            self.update_table()
            window.destroy()

        except DeckNotFoundError as e:
            messagebox.showerror(
                "Deck introuvable",
                "Le deck sélectionné n'existe plus.\nVeuillez rafraîchir la liste."
            )

        except Exception as e:
            # Sécurité : bug inattendu
            messagebox.showerror(
                "Erreur inattendue",
                f"Une erreur est survenue : {e}"
            )

    def speak_fiche_selection(self, tree):
        if not self.audio_manager or not self.audio_manager.actif:
            return
        
        selection = tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = tree.item(item, "values")
        # values[0] = id, values[1] = question
        question = values[1]
        self.audio_manager.parler(f"Question : {question}")


    def supprimer_deck(self):
        """Supprime le deck courant après confirmation."""
        if not self.deck:
            messagebox.showerror("Erreur", "Aucun deck chargé.")
            return

        reponse = messagebox.askyesno(
            "Confirmation",
            f"Voulez-vous vraiment supprimer le deck '{self.deck.nom}' ?"
        )
        if not reponse:
            return

        try:
            self.forms_manager.delete_deck(self.deck.id)

            messagebox.showinfo("Succès", "Le deck a bien été supprimé.")
            # Retour à la liste des decks
            self.controller.show_page("DeckList")

            # Rafraîchir la liste si une méthode existe
            page = self.controller.pages.get("DeckList")
            if page and hasattr(page, "charger_decks"):
                page.charger_decks()

        except DeckNotFoundError:
            messagebox.showerror(
                "Deck introuvable",
                "Ce deck n'existe plus. Veuillez rafraîchir la liste."
            )
        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Une erreur est survenue lors de la suppression : {e}"
            )

    def retirer_fiche(self):
        sel = self.tree.selection()
        if sel and messagebox.askyesno("Confirmation", "Retirer cette fiche ?"):
            fid = int(self.tree.item(sel[0], "values")[0])
            self.deck.fiche_ids.remove(fid)
            self.forms_manager.storage.unlink_card_from_deck_in_db(self.deck.id, fid) 
            self.update_table()

    def update_table(self):
        """tableau avec les fiches actuelles du deck."""
        for i in self.tree.get_children(): self.tree.delete(i)
        
        if not self.deck: return
        self.nb_label.config(text=f"Nombre de fiches : {len(self.deck.fiche_ids)}")

        for f in self.forms_manager.toutes_les_fiches():
            if f.id in self.deck.fiche_ids:
                self.tree.insert("", "end", values=(f.id, f.question))
