import tkinter as tk
from tkinter import ttk, messagebox, Toplevel

class RevisionPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager, audio_manager=None):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager
        self.audio_manager = audio_manager
        self.widget_nav = []
        self.buttons = []

        ttk.Label(self, text="Révision", font=("Segoe UI", 16, "bold")).pack(pady=20)

        ttk.Button(
            self,
            text="Réviser toutes les fiches",
            command=lambda: controller.show_page("RevisionSession")
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Reviser les fiches par themes", command=self.choisir_deck
            ).pack(pady=10)

        ttk.Button(
            self,
            text="Retour",
            command=lambda: controller.show_page("MainMenu")
        ).pack(pady=10)

# Accessibilité complète
        if audio_manager:
            self.buttons = audio_manager.setup_full_accessibility(self, controller, "MainMenu")
            self.after(100, self.focus_button_if_enabled)

    def focus_button_if_enabled(self):
        if self.buttons:
            main_menu = self.controller.pages.get("MainMenu")
            if main_menu and hasattr(main_menu, 'mode_actif') and main_menu.mode_actif:
                self.buttons[0].focus_set()
                if self.audio_manager:
                    self.audio_manager.parler(f"Bouton : {self.buttons[0]['text']}")

    def start_revision_console(self):
        fiches = self.forms_manager.toutes_les_fiches()

        if not fiches:
            print("\n Aucune fiche à réviser pour le moment.\n")
            messagebox.showinfo("Révision", "Aucune fiche à réviser.")
            return

        print("\n Début de la session de révision :")
        print("----------------------------------------")

        for fiche in fiches:
            print(f"\n QUESTION (fiche #{fiche.id}) :")
            print(fiche.question)
            print("----------------------------------------")

            reponse_user = input("Votre réponse : ")

            print("\n Réponse correcte :")
            print(fiche.reponse)
            print("----------------------------------------")

            #fiche.derniere_revision = datetime.now()
            fiche.intervalle = max(1, fiche.intervalle + 1)
            fiche.niveau += 1

        print("\n🎉 Révision terminée !\n")
        messagebox.showinfo("Révision", "La session de révision est terminée !")

    def choisir_deck(self):
        """Popup pour choisir le deck à réviser."""
        self.forms_manager.charger_decks_depuis_db()
        decks = self.forms_manager.tous_les_decks()

        if not decks:
            messagebox.showinfo("Info", "Aucun deck n'a été créé.")
            return

        # fenêtre popup
        top = Toplevel(self)
        top.title("Choisir un thème")
        top.geometry("400x300")
# msg audio à l'ouverture
        if self.audio_manager:
            self.audio_manager.parler("Choisissez un thème dans la liste")

        ttk.Label(top, text="Double-cliquez (ou Entrée) sur un deck :").pack(pady=10)

        # Liste des decks
        columns = ("id", "nom", "nb")
        tree = ttk.Treeview(top, columns=columns, show="headings")
        tree.heading("id", text="#")
        tree.heading("nom", text="Nom")
        tree.heading("nb", text="Fiches")
        
        tree.column("id", width=40)
        tree.column("nom", width=200)
        tree.column("nb", width=60)
        
        tree.pack(fill="both", expand=True, padx=10, pady=5)

        for deck in decks:
            tree.insert("", "end", values=(deck.id, deck.nom, len(deck.fiche_ids)))

# --- MODIFICATIONS ACCESSIBILITÉ ---
        
        tree.bind("<<TreeviewSelect>>", lambda e: self.speak_deck_selection(tree))        

        valider = lambda e: self.lancer_revision_deck(tree, top)
        tree.bind("<Double-1>", valider)
        tree.bind("<Return>", valider)

        tree.focus_set()
        if tree.get_children():
            first_item = tree.get_children()[0]
            tree.selection_set(first_item)
            tree.focus(first_item)

    def lancer_revision_deck(self, tree, window):
        """Config session avec le deck choisi"""
        selection = tree.selection()
        if not selection:
            return

        item = selection[0]
        values = tree.item(item, "values")
        deck_id = int(values[0])
        
        window.destroy()

        session_page = self.controller.pages["RevisionSession"]
        session_page.deck_id_filter = deck_id

        self.controller.show_page("RevisionSession")

    def speak_deck_selection(self, tree):
        """Lit le nom du deck sélectionné."""
        if not self.audio_manager:
            return

        selection = tree.selection()
        if not selection:
            return

        item = selection[0]
        values = tree.item(item, "values")
        nom_deck = values[1]
        nb_fiches = values[2]

        self.audio_manager.parler(f"{nom_deck}, {nb_fiches} fiches")