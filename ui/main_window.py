import tkinter as tk
from tkinter import ttk, messagebox
from ui.fiches_view import FichesView

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Configuration de base ---
        self.title("Jean-Révise Mémorator 🌱")
        self.geometry("850x600")
        self.minsize(700, 500)
        self.configure(bg="#f8f9fa")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11), padding=10)
        style.configure("TLabel", background="#f8f9fa", font=("Segoe UI", 12))

        # --- En-tête (titre général) ---
        self.title_label = ttk.Label(
            self,
            text="Jean-Révise Mémorator 🌱",
            font=("Segoe UI", 20, "bold"),
            background="#f8f9fa",
            foreground="#2f4f4f",
        )
        self.title_label.pack(pady=(28, 6))

        # --- Menu boutons horizontal ---
        self.menu_frame = ttk.Frame(self)
        self.menu_frame.pack(pady=(0,6))

        self._add_menu_button("📘 Gérer mes fiches", self.show_fiches)
        self._add_menu_button("🧠 Commencer une révision", self.show_revision)
        self._add_menu_button("📊 Tableau de bord", self.show_dashboard)
        self._add_menu_button("🏠 Accueil", self.show_home)
        self._add_menu_button("🚪 Quitter", self.quit_app)

        # --- Zone centrale où s'affichent les vues dynamiques ---
        self.central_frame = ttk.Frame(self, style="Central.TFrame")
        self.central_frame.pack(padx=16, pady=(12,10), fill=tk.BOTH, expand=True)

        # --- Citation inspirante en bas ---
        self.quote_label = ttk.Label(
            self,
            text='"Chaque jour est une nouvelle graine de savoir à planter." 🌼',
            font=("Segoe UI", 10, "italic"),
            foreground="#555",
            background="#f8f9fa",
        )
        self.quote_label.pack(side="bottom", pady=14)

        self.show_home()  # Affiche la page d'accueil par défaut

    def _add_menu_button(self, text, command):
        btn = ttk.Button(self.menu_frame, text=text, command=command)
        btn.pack(side="left", padx=6, ipadx=8, ipady=3)

    def clear_central_frame(self):
        for widget in self.central_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_central_frame()
        lbl = ttk.Label(
            self.central_frame,
            text="Bienvenue dans ton jardin de connaissances 🌿\n\nChoisis une activité pour entretenir ta mémoire !",
            font=("Segoe UI", 18, "bold"),
            background="#f8f9fa",
            foreground="#2f4f4f"
        )
        lbl.pack(expand=True, pady=45)

    def show_fiches(self):
        self.clear_central_frame()
        FichesView(self.central_frame).pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    def show_revision(self):
        self.clear_central_frame()
        lbl = ttk.Label(self.central_frame, text="Module de révision prochainement disponible.", font=("Segoe UI", 15), background="#f8f9fa")
        lbl.pack(expand=True)

    def show_dashboard(self):
        self.clear_central_frame()
        lbl = ttk.Label(self.central_frame, text="Tableau de bord/statistiques prochainement disponible.", font=("Segoe UI", 15), background="#f8f9fa")
        lbl.pack(expand=True)

    def quit_app(self):
        if messagebox.askokcancel("Quitter", "Souhaites-tu vraiment quitter l’application ?"):
            self.destroy()
