import tkinter as tk
from tkinter import ttk, messagebox, Toplevel

class RevisionPage(ttk.Frame):
    def __init__(self, parent, controller, forms_manager):
        super().__init__(parent)

        self.controller = controller
        self.forms_manager = forms_manager

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
            messagebox.showinfo("Info", "Aucun paquet n'a été créé.")
            return

        # fenêtre popup
        top = Toplevel(self)
        top.title("Choisir un thème")
        top.geometry("400x300")
        ttk.Label(top, text="Double-cliquez sur un paquet pour le réviser :").pack(pady=10)

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

        tree.bind("<Double-1>", lambda e: self.lancer_revision_deck(tree, top))

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