import tkinter as tk
from tkinter import ttk, messagebox

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Configuration de base ---
        self.title("Jean-Révise Mémorator 🌱")
        self.geometry("700x500")
        self.minsize(600, 400)
        self.configure(bg="#f8f9fa")  # fond clair et doux

        # --- Style général ---
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11), padding=10)
        style.configure("TLabel", background="#f8f9fa", font=("Segoe UI", 12))

        # --- Titre principal ---
        self.title_label = ttk.Label(
            self,
            text="Bienvenue dans ton jardin de connaissances 🌿",
            font=("Segoe UI", 16, "bold"),
            foreground="#2f4f4f",
        )
        self.title_label.pack(pady=(40, 10))

        # --- Sous-titre ---
        self.subtitle_label = ttk.Label(
            self,
            text="Choisis une activité pour entretenir ta mémoire :",
            font=("Segoe UI", 12),
            foreground="#3c3c3c",
        )
        self.subtitle_label.pack(pady=(0, 30))

        # --- Conteneur central ---
        self.menu_frame = ttk.Frame(self)
        self.menu_frame.pack(pady=10)

        # --- Boutons du menu principal ---
        self._add_menu_button("📘 Gérer mes fiches", self.open_fiches)
        self._add_menu_button("🧠 Commencer une révision", self.open_revision)
        self._add_menu_button("📊 Tableau de bord", self.open_dashboard)
        self._add_menu_button("🚪 Quitter", self.quit_app)

        # --- Citation inspirante ---
        self.quote_label = ttk.Label(
            self,
            text='"Chaque jour est une nouvelle graine de savoir à planter." 🌼',
            font=("Segoe UI", 10, "italic"),
            foreground="#555",
        )
        self.quote_label.pack(side="bottom", pady=20)

    def _add_menu_button(self, text, command):
        btn = ttk.Button(self.menu_frame, text=text, command=command)
        btn.pack(pady=8, ipadx=10, ipady=5, fill="x", expand=True)

    def open_fiches(self):
        messagebox.showinfo("Fiches", "Ouverture de la gestion des fiches 📘 (à implémenter)")

    def open_revision(self):
        messagebox.showinfo("Révision", "Démarrage de la révision 🧠 (à implémenter)")

    def open_dashboard(self):
        messagebox.showinfo("Tableau de bord", "Affichage des statistiques 📊 (à implémenter)")

    def quit_app(self):
        if messagebox.askokcancel("Quitter", "Souhaites-tu vraiment quitter l’application ?"):
            self.destroy()
