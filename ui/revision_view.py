import tkinter as tk
from tkinter import ttk


class RevisionView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame")

        # --- TITRE ---
        title = ttk.Label(
            self,
            text="🧠 Entraînez-vous par thèmes",
            font=("Segoe UI", 16, "bold"),
            foreground="#2f4f4f"
        )
        title.pack(pady=20)

        # --- SOUS-TITRE ---
        subtitle = ttk.Label(
            self,
            text="Choisissez un thème pour commencer une révision :",
            font=("Segoe UI", 12),
            foreground="#3c3c3c"
        )
        subtitle.pack(pady=(0, 25))

        # --- CONTENEUR BOUTONS ---
        theme_frame = ttk.Frame(self)
        theme_frame.pack(pady=10)

        self.add_theme_btn(theme_frame, "🔌 Électronique")
        self.add_theme_btn(theme_frame, "💻 Programmation")
        self.add_theme_btn(theme_frame, "⚡ Électricité")

        # --- BOUTON RETOUR ---
        btn_back = ttk.Button(
            self,
            text="⬅ Retour",
            command=lambda: controller.show_page("MainMenu")
        )
        btn_back.pack(pady=20)

    # ------------------------------------------------------------
    # Ajout d'un bouton de thème
    # ------------------------------------------------------------
    def add_theme_btn(self, parent, text):
        ttk.Button(
            parent,
            text=text,
            command=lambda t=text: print(f"Thème sélectionné : {t}")
        ).pack(
            pady=8,
            ipadx=10,
            ipady=5,
            fill="x",
            expand=True
        )
