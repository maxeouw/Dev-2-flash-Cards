# ui/stats_page.py

import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as mticker


class StatsPage(ttk.Frame):
    def __init__(self, parent, controller, storage_manager, forms_manager):
        super().__init__(parent)

        self.controller = controller
        self.storage_manager = storage_manager
        self.forms_manager = forms_manager
        center_frame = ttk.Frame(self)
        center_frame.pack(expand=True)

        ttk.Label(center_frame, text="Tableau de bord",
                  font=("Segoe UI", 16, "bold")).pack(pady=20)

        # deck + buttns
        control_frame = ttk.Frame(center_frame)
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
        self.deck_combo.bind("<<ComboboxSelected>>",
                             lambda e: self.refresh_stats_all())

        # Mapping name -> id
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
        self.tree = ttk.Treeview(center_frame, columns=columns,
                                 show="headings", height=10)
        self.tree.heading("date", text="Date")
        self.tree.heading("deck", text="Deck")
        self.tree.heading("total", text="Cartes")
        self.tree.heading("failed", text="Échecs")
        self.tree.heading("success_pct", text="% de réussite")

        for col in columns:
            self.tree.column(col, anchor="center", width=90)

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # espace entre les graphs
        self.graph_frame = ttk.Frame(center_frame)
        self.graph_frame.pack(pady=20)

        # 2 graphiques
        self.figure = Figure(figsize=(15, 3), dpi=100)
        self.ax_avg = self.figure.add_subplot(121)   # moyenne 
        self.ax_raw = self.figure.add_subplot(122, sharex=self.ax_avg)  # brut

        self.canvas_mpl = FigureCanvasTkAgg(self.figure,
                                            master=self.graph_frame)
        self.canvas_mpl.get_tk_widget().pack()

        # Boutton retour
        ttk.Button(
            center_frame,
            text="Retour",
            command=lambda: controller.show_page("MainMenu")
        ).pack(pady=10)

        self.load_decks_into_combobox()
        self.refresh_stats_all()

    # bouton combobox
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
            self.deck_combo.current(0)  

    # bouton refresh pour mettre a jour le tableau et le graph
    def refresh_stats_all(self):
        # Vider le tableau
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Récupérer le deck sélectionné dans le combobox
        deck_name = self.deck_var.get()

        if deck_name and deck_name in self.deck_name_to_id:
            # Filtrer sur deck name
            deck_id = self.deck_name_to_id[deck_name]
            stats = self.storage_manager.load_stats_for_deck(deck_id)
        else:
            # Si rien de valide n'est sélectionné, on n'affiche rien
            stats = []

        # afficher nom du deck name dans le form
        decks = {d.id: d.nom for d in self.forms_manager.tous_les_decks()}

        for s in stats:
            success_pct = s.success_rate
            date_str = s.date_session.date().isoformat()
            deck_id = s.deck_id
            deck_name = decks.get(deck_id, "Inconnu")
            self.tree.insert(
                "",
                "end",
                values=(
                    date_str,
                    deck_name,
                    s.total_cards,
                    s.failed_cards,
                    f"{success_pct:.1f}%",
                ),
            )

    # graph pour deck id
    def show_graph_for_selected_deck(self):
        deck_name = self.deck_var.get()
        if not deck_name or deck_name not in self.deck_name_to_id:
            return

        deck_id = self.deck_name_to_id[deck_name]
        stats = self.storage_manager.load_stats_for_deck(deck_id)
        if not stats:
            # Effacer l'ancien contenu et afficher un message
            self.ax_avg.clear()
            self.ax_raw.clear()
            self.ax_avg.text(
                0.5,
                0.5,
                "Aucune session pour ce deck.",
                ha="center",
                va="center",
                transform=self.ax_avg.transAxes,
            )
            self.ax_avg.set_axis_off()
            self.ax_raw.set_axis_off()
            self.canvas_mpl.draw()
            return
        #on pour les axes
        self.ax_avg.set_axis_on()
        self.ax_raw.set_axis_on()
        success_values = [s.success_rate for s in stats]
        # Moyenne amélioration
        cumulated = []
        total = 0.0
        for i, val in enumerate(success_values, start=1):
            total += val
            cumulated.append(total / i)

        x_values = list(range(1, len(success_values) + 1))
        n = len(x_values)
        x_min = 0.5
        x_max = n + 0.5

        # Graphe 1
        self.ax_avg.clear()
        self.ax_avg.bar(x_values, cumulated, color="green", width=0.5)
        self.ax_avg.set_title("Graphique de l'Amélioration")
        self.ax_avg.set_xlabel("Nombre de révisions (sessions)")
        self.ax_avg.set_ylabel("Moyenne de réussite (%)")
        self.ax_avg.set_xlim(x_min, x_max)
        self.ax_avg.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        self.ax_avg.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        self.ax_avg.set_ylim(0, 110)
        self.ax_avg.grid(True, linestyle="--", alpha=0.3)

        # Graphe 2
        self.ax_raw.clear()
        self.ax_raw.plot(x_values, success_values, marker="o", color="blue")
        self.ax_raw.set_title("Pourcentage de réussite par session")
        self.ax_raw.set_xlabel("Nombre de révisions (sessions)")
        self.ax_raw.set_ylabel("Réussite (%)")
        self.ax_raw.set_xlim(x_min, x_max)
        self.ax_raw.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        self.ax_raw.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        self.ax_raw.set_ylim(0, 110)
        self.ax_raw.grid(True, linestyle="--", alpha=0.3)

        # Plus d’espace entre les deux graphes
        self.figure.tight_layout(h_pad=5)

        self.canvas_mpl.draw()
