# ui/stats_page.py
import tkinter as tk
from tkinter import ttk


class StatsPage(ttk.Frame):
    def __init__(self, parent, controller, storage_manager, forms_manager):
        super().__init__(parent)
        self.controller = controller
        self.storage_manager = storage_manager
        self.forms_manager = forms_manager

        ttk.Label(self, text="Tableau de bord", font=("Segoe UI", 16, "bold")).pack(pady=20)

        # --- Ligne de contrôle (deck + boutons) ---
        control_frame = ttk.Frame(self)
        control_frame.pack(pady=5)

        ttk.Label(control_frame, text="Deck :").pack(side="left", padx=5)

        # Combobox pour choisir le deck
        self.deck_var = tk.StringVar()
        self.deck_combo = ttk.Combobox(
            control_frame,
            textvariable=self.deck_var,
            state="readonly",
            width=25
        )
        self.deck_combo.pack(side="left", padx=5)

        # Mapping nom_deck -> id
        self.deck_name_to_id = {}

        # Bouton Rafraîchir (table)
        ttk.Button(
            control_frame,
            text="Rafraîchir",
            command=self.refresh_stats_all
        ).pack(side="left", padx=5)

        # Bouton Voir graphe
        ttk.Button(
            control_frame,
            text="Voir graphe",
            command=self.show_graph_for_selected_deck
        ).pack(side="left", padx=5)

        # --- Tableau des sessions ---
        columns = ("date", "deck", "total", "failed", "success_pct")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        self.tree.heading("date", text="Date")
        self.tree.heading("deck", text="Deck")
        self.tree.heading("total", text="Cartes")
        self.tree.heading("failed", text="Échecs")
        self.tree.heading("success_pct", text="% .de réussite")

        for col in columns:
            self.tree.column(col, anchor="center", width=90)

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Canvas pour graphe ---
        self.canvas = tk.Canvas(self, width=500, height=200, bg="white")
        self.canvas.pack(pady=10)

        # Bouton retour
        ttk.Button(
            self,
            text="Retour",
            command=lambda: controller.show_page("MainMenu")
        ).pack(pady=10)

        # Charger les decks et les stats au démarrage
        self.load_decks_into_combobox()
        self.refresh_stats_all()

    # ------------------------------------------------------------------
    # Combobox decks
    # ------------------------------------------------------------------
    def load_decks_into_combobox(self):
        """Remplit le combobox avec tous les decks."""
        self.deck_name_to_id.clear()
        decks = self.forms_manager.tous_les_decks()
        names = []
        for deck in decks:
            name = deck.nom
            self.deck_name_to_id[name] = deck.id
            names.append(name)

        self.deck_combo["values"] = names
        if names:
            self.deck_combo.current(0)  # sélectionne le premier deck

    # ------------------------------------------------------------------
    # Tableau des sessions
    # ------------------------------------------------------------------
    def refresh_stats_all(self):
        """Affiche toutes les sessions dans le tableau."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        # None = tous les decks
        stats = self.storage_manager.load_stats_for_deck()

        # Pour afficher le nom du deck, on construit un mapping id->nom
        decks = {d.id: d.nom for d in self.forms_manager.tous_les_decks()}

        for s in stats:
            success_pct = s["success_rate"]
            date_str = s["date_session"].split("T")[0]
            deck_id = s["deck_id"]
            deck_name = decks.get(deck_id, "Inconnu")  

            self.tree.insert(
                "",
                "end",
                values=(
                    date_str,
                    deck_name,
                    s["total_cards"],
                    s["failed_cards"],
                    f"{success_pct:.1f}%",
                ),
            )

    # ------------------------------------------------------------------
    # Graphe par deck
    # ------------------------------------------------------------------
    def show_graph_for_selected_deck(self):
        """Récupère le deck choisi et trace la courbe de réussite de tous ses runs."""
        self.canvas.delete("all")

        deck_name = self.deck_var.get()
        if not deck_name or deck_name not in self.deck_name_to_id:
            return  # rien sélectionné

        deck_id = self.deck_name_to_id[deck_name]
        stats = self.storage_manager.load_stats_for_deck(deck_id)

        if not stats:
            # Rien à tracer
            self.canvas.create_text(
                250, 100,
                text="Aucune session pour ce deck.",
                fill="gray"
            )
            return

        # success_values = pourcentage de réussite de chaque run
        success_values = [s["success_rate"] for s in stats]

        # Option : moyenne cumulative pour visualiser l'amélioration globale
        cumulated = []
        total = 0.0
        for i, val in enumerate(success_values, start=1):
            total += val
            cumulated.append(total / i)

        # Choisir ce que tu veux tracer :
        values_to_plot = cumulated  # courbe d'amélioration moyenne
        # values_to_plot = success_values  # courbe brute run par run

        n = len(values_to_plot)
        max_val = 100.0  # échelle fixe 0–100

        w = int(self.canvas["width"])
        h = int(self.canvas["height"])
        padding = 30

        # Axes
        self.canvas.create_line(padding, h - padding, w - padding, h - padding)  # X
        self.canvas.create_line(padding, padding, padding, h - padding)          # Y

        # Graduation Y : 0, 10, 20, ..., 100
        for pct in range(0, 101, 10):
            y = h - padding - (pct / 100.0) * (h - 2 * padding)
            self.canvas.create_line(padding - 5, y, padding + 5, y)
            self.canvas.create_text(padding - 10, y, text=str(pct), anchor="e")

        # Pas en X
        if n == 1:
            x_step = w - 2 * padding
        else:
            x_step = (w - 2 * padding) / (n - 1)

        points = []
        for i, val in enumerate(values_to_plot):
            x = padding + i * x_step
            y = h - padding - (val / max_val) * (h - 2 * padding)
            points.append((x, y))

        # Ligne
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill="green", width=2)

        # Points + numéros de run en X
        for idx, (x, y) in enumerate(points, start=1):
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="green")
            self.canvas.create_text(x, h - padding + 10, text=str(idx), anchor="n")
