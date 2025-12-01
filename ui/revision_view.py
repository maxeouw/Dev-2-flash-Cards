import tkinter as tk
from tkinter import ttk, messagebox

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
            text="Reviser les fiches par themes"
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
