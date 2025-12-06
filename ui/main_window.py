import tkinter as tk
from tkinter import ttk, messagebox
from ui.fiches_view import FichesViewPage
from ui.revision_view import RevisionPage
from core.formManager import FormsManager
from ui.add_form_page import AddFormPage
from ui.add_paquet_page import AddPaquetPage
from ui.forms_list import ListeFichesPage
from core.storage import StorageManager
from ui.edit_format_page import EditFormPage
from ui.paquets_list import ManagePaquetsPage
from ui.revision_session_page import RevisionSessionPage
from ui.edit_decks_page import DeckDetailPage


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Configuration de base ---
        self.title("Jean-Révise Mémorator 🌱")
        self.geometry("700x500")
        self.minsize(600, 400)
        self.configure(bg="#f8f9fa")

        # --- Style global ---
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11), padding=10)
        style.configure("TLabel", background="#f8f9fa", font=("Segoe UI", 12))
        style.configure("TFrame", background="#f8f9fa")

        # --- CONTENEUR CENTRAL DES PAGES ---
        self.page_container = ttk.Frame(self)
        self.page_container.pack(fill="both", expand=True)

        # Gestionnaires de stockage et de fiches
        self.storage_manager = StorageManager()
        self.forms_manager = FormsManager(self.storage_manager)

        # Initialisation des pages
        self.pages = {}
        self.create_pages()

        # Affichage de la page d'accueil
        self.show_page("MainMenu")

    # ---------------------------------------------------------
    # Création des pages
    # ---------------------------------------------------------
    def create_pages(self):

        # Page principale
        self.pages["MainMenu"] = MainMenuPage(self.page_container, self)
        self.pages["MainMenu"].grid(row=0, column=0, sticky="nsew")

        # Page de gestion des fiches et des paquets. 
        self.pages["FichesView"] = FichesViewPage(self.page_container, self, self.forms_manager)
        self.pages["FichesView"].grid(row=0, column=0, sticky="nsew")

        # Page fiches
        self.pages["AddForm"] = AddFormPage(self.page_container, self, self.forms_manager)
        self.pages["AddForm"].grid(row=0, column=0, sticky="nsew")

        #Page de lancement de revision
        self.pages["Revision"] = RevisionPage(self.page_container, self, self.forms_manager)
        self.pages["Revision"].grid(row=0, column=0, sticky="nsew")

        #Page d'ajout de paquets
        self.pages["AddPaquet"] = AddPaquetPage(self.page_container, self, self.forms_manager)
        self.pages["AddPaquet"].grid(row=0, column=0, sticky="nsew")

        #Page gestion des fiches
        self.pages["FormList"] = ListeFichesPage(self.page_container,self, self.forms_manager)
        self.pages["FormList"].grid(row=0, column=0, sticky="nsew")

        #Page édition des fiches
        self.pages["EditForm"] = EditFormPage(self.page_container, self, self.forms_manager)
        self.pages["EditForm"].grid(row=0, column=0, sticky="nsew")

        #Page de liste de decks
        self.pages["DeckList"] = ManagePaquetsPage(self.page_container, self, self.forms_manager)
        self.pages["DeckList"].grid(row=0, column=0, sticky="nsew")

        #Page de révision
        self.pages["RevisionSession"] = RevisionSessionPage(self.page_container, self, self.forms_manager)
        self.pages["RevisionSession"].grid(row=0, column=0, sticky="nsew")

        #Page de gestion des decks
        self.pages["deckGestion"] = DeckDetailPage(self.page_container, self, self.forms_manager)
        self.pages["deckGestion"].grid(row=0, column=0, sticky="nsew")

    # ---------------------------------------------------------
    # Affichage d'une page
    # ---------------------------------------------------------
    def show_page(self, name: str):
        page = self.pages[name]
        # Actualise le contenu si la page a une méthode update_list (En gros si il y aune liste dans la page)
        if hasattr(page, "update_list"):
            page.update_list()
        if name == "RevisionSession":
            page.start_session()
        page.tkraise()


# ---------------------------------------------------------
# PAGE D'ACCUEIL
# ---------------------------------------------------------
class MainMenuPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # --- CONTENEUR CENTRAL (pour centrer tous les éléments) ---
        center_frame = ttk.Frame(self)
        center_frame.place(relx=0.6, rely=0.5, anchor="center")
        """
        # --- Titre principal ---
        title_label = ttk.Label(
            center_frame,
            text="Bienvenue dans ton jardin de connaissances 🌿",
            font=("Segoe UI", 16, "bold"),
            foreground="#2f4f4f",
        )
        title_label.pack(pady=(40, 10))
        
        # --- Sous-titre ---
        subtitle_label = ttk.Label(
            center_frame,
            text="Choisis une activité pour entretenir ta mémoire :",
            font=("Segoe UI", 12),
            foreground="#3c3c3c",
        )
        subtitle_label.pack(pady=(0, 25))
        """
        # --- Conteneur des boutons ---
        menu_frame = ttk.Frame(self)
        menu_frame.pack(pady=10)

        self.add_btn(menu_frame, "📘 Gérer mes fiches et paquets",
                     lambda: controller.show_page("FichesView"))
        self.add_btn(menu_frame, "🧠 Commencer une révision",
                     lambda: controller.show_page("Revision"))
        self.add_btn(menu_frame, "📊 Tableau de bord",
                     lambda: messagebox.showinfo("Dashboard", "À implémenter"))
        self.add_btn(menu_frame, "🚪 Quitter", controller.quit)

        # --- Citation en bas ---
        quote_label = ttk.Label(
            self,
            text='"Chaque jour est une nouvelle graine de savoir à planter." 🌼',
            font=("Segoe UI", 10, "italic"),
            foreground="#555",
        )
        quote_label.pack(side="bottom", pady=20)

    # Ajout d'un bouton stylisé
    def add_btn(self, parent, text, command):
        ttk.Button(parent, text=text, command=command).pack(
            pady=8, ipadx=10, ipady=5, fill="x", expand=True
        )
