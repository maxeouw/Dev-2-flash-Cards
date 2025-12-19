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
from core.audio_manager import AudioManager
from ui.stats_page import StatsPage
from ui.end_session_page import EndOfSessionPage
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

        # 1. Moteur audio
        self.audio_manager = AudioManager()

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
        self.pages["MainMenu"] = MainMenuPage(self.page_container, self, self.audio_manager)
        self.pages["MainMenu"].grid(row=0, column=0, sticky="nsew")

        # Page de gestion des fiches et des decks. 
        self.pages["FichesView"] = FichesViewPage(self.page_container, self, self.forms_manager, self.audio_manager)
        self.pages["FichesView"].grid(row=0, column=0, sticky="nsew")

        # Page fiches
        self.pages["AddForm"] = AddFormPage(self.page_container, self, self.forms_manager, self.audio_manager)
        self.pages["AddForm"].grid(row=0, column=0, sticky="nsew")

        #Page de lancement de revision
        self.pages["Revision"] = RevisionPage(self.page_container, self, self.forms_manager, self.audio_manager)
        self.pages["Revision"].grid(row=0, column=0, sticky="nsew")

        #Page d'ajout de decks
        self.pages["AddPaquet"] = AddPaquetPage(self.page_container, self, self.forms_manager, self.audio_manager)
        self.pages["AddPaquet"].grid(row=0, column=0, sticky="nsew")

        #Page gestion des fiches
        self.pages["FormList"] = ListeFichesPage(self.page_container,self, self.forms_manager, self.audio_manager)
        self.pages["FormList"].grid(row=0, column=0, sticky="nsew")

        #Page édition des fiches
        self.pages["EditForm"] = EditFormPage(self.page_container, self, self.forms_manager)
        self.pages["EditForm"].grid(row=0, column=0, sticky="nsew")

        #Page de liste de decks
        self.pages["DeckList"] = ManagePaquetsPage(self.page_container, self, self.forms_manager, self.audio_manager)
        self.pages["DeckList"].grid(row=0, column=0, sticky="nsew")

        #Page de révision
        self.pages["RevisionSession"] = RevisionSessionPage(self.page_container, self, self.forms_manager, self.audio_manager)
        self.pages["RevisionSession"].grid(row=0, column=0, sticky="nsew")

        #Page de gestion des decks
        self.pages["deckGestion"] = DeckDetailPage(self.page_container, self, self.forms_manager, self.audio_manager)
        self.pages["deckGestion"].grid(row=0, column=0, sticky="nsew")
        #pages de stqts
        self.pages["Stats"] = StatsPage(self.page_container, self, self.storage_manager, self.forms_manager)
        self.pages["Stats"].grid(row=0, column=0, sticky="nsew")
        # Page de fin de session
        self.pages["EndSession"] = EndOfSessionPage(self.page_container, self, self.forms_manager)
        self.pages["EndSession"].grid(row=0, column=0, sticky="nsew")

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
        # Focus sur le 1er bouton de la page d'accueil (mode d'accesibilité)
        if name == "MainMenu" and hasattr(page, "focus_first_button"):
            page.focus_first_button()
        if name == "Revision" and hasattr(page, "focus_button_if_enabled"):
            page.focus_button_if_enabled()
        page.tkraise()

        # Gest° focus accessibilité
        accessibilite_active = self.audio_manager and self.audio_manager.actif

        if accessibilite_active:
            if hasattr(page, "focus_button_if_enabled"):
                self.after(50, page.focus_button_if_enabled)
            
            elif hasattr(page, "focus_first_button"):
                self.after(50, page.focus_first_button)


# ---------------------------------------------------------
# PAGE D'ACCUEIL
# ---------------------------------------------------------
class MainMenuPage(ttk.Frame):
    def __init__(self, parent, controller, audio_manager=None):
        super().__init__(parent)
        self.controller = controller
        self.audio_manager = audio_manager
        self.boutons_menu = []

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
# --- BOUTON D'ACCESSIBILITÉ ---
        self.mode_actif = False 
        toggle_frame = ttk.Frame(self)
        toggle_frame.pack(pady=20, anchor="n")

        self.mode_var = tk.BooleanVar(value=False)
        self.checkbox = ttk.Checkbutton(
            toggle_frame,
            text="🔊 Mode Accessibilité",
            variable=self.mode_var,
            command=self.toggle_mode
        )
        self.checkbox.pack(side="left", padx=5)
        self.checkbox.bind("<space>", lambda e: self.dire("Case à cocher Mode Accessibilité", stop_action=True))
        self.checkbox.bind("<Right>", lambda e: self.action_droite(lambda: self.checkbox.invoke()))
        self.checkbox.bind("<FocusIn>", lambda e: self.dire("Case à cocher Mode Accessibilité"))
        self.status_label = ttk.Label(toggle_frame, text="(désactivé)", foreground="#666")
        self.status_label.pack(side="left", padx=5)
        
        # --- Conteneur des boutons ---
        menu_frame = ttk.Frame(self)
        menu_frame.pack(pady=10)

        self.add_btn(menu_frame, "Gérer mes fiches et decks",
                     lambda: controller.show_page("FichesView"))
        self.add_btn(menu_frame, "Commencer une révision",
                     lambda: controller.show_page("Revision"))
        self.add_btn(menu_frame, "Tableau de bord",
                    lambda: controller.show_page("Stats"))
        self.add_btn(menu_frame, "Quitter", controller.quit)

        # Activation nav clavier
        self.setup_navigation()

        # --- Citation en bas ---
        quote_label = ttk.Label(
            self,
            text='"Chaque jour est une nouvelle graine de savoir à planter." 🌼',
            font=("Segoe UI", 10, "italic"),
            foreground="#555",
        )
        quote_label.pack(side="bottom", pady=20)

    def toggle_mode(self):
        # Activer/désactiver son, clavier
        self.mode_actif = self.mode_var.get()
        if self.audio_manager:
            self.audio_manager.set_actif(self.mode_actif)

        if self.mode_actif:
            self.status_label.config(text="(activé)", foreground="#28a745")
            if self.audio_manager:
                self.audio_manager.parler("Mode accessibilité activé.")
            self.focus_first_button()
        else:
            if self.audio_manager:
                self.audio_manager.set_actif(True)
                self.audio_manager.parler("Mode accessibilité désactivé.")
                self.audio_manager.set_actif(False)
            self.status_label.config(text="(désactivé)", foreground="#666")

    # Ajout d'un bouton stylisé
    def add_btn(self, parent, text, command):
        btn = ttk.Button(parent, text=text, command=command)
        btn.pack(pady=8, ipadx=10, ipady=5, fill="x", expand=True)

        btn.bind("<FocusIn>", lambda e: self.dire(text))
        btn.bind("<Right>", lambda e: self.action_droite(command))
        btn.bind("<Left>", lambda e: self.action_gauche())
        btn.bind("<space>", lambda e: self.repeter_selection(text))
        self.boutons_menu.append(btn)

    def setup_navigation(self):
        tous_les_elements = [self.checkbox] + self.boutons_menu
        total = len(tous_les_elements)
        for i, btn in enumerate(tous_les_elements):
            prev = tous_les_elements[i - 1]
            next_btn = tous_les_elements[(i + 1) % total]

            btn.bind("<Up>", lambda e, b=prev: self.naviguer_vers(b))
            btn.bind("<Down>", lambda e, b=next_btn: self.naviguer_vers(b))

    # FCT ne font rien si mode désactivé
    
    def repeter_selection(self, text):
        if self.mode_actif:
            self.dire(text)
            return "break"
        
    def naviguer_vers(self, widget_cible):
        if self.mode_actif:
            widget_cible.focus_set()

    def action_droite(self, command):
        if self.mode_actif:
            command()

    def action_gauche(self):
        if self.mode_actif:
            self.controller.quit()

    def dire(self, text):
        if self.audio_manager and self.mode_actif:
            try:
                self.audio_manager.parler(f"Bouton : {text}")
            except: pass

    def focus_first_button(self):
        if self.boutons_menu and self.mode_actif:
            self.boutons_menu[0].focus_set()
