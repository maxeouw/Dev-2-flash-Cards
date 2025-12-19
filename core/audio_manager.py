import threading
import pyttsx3
from tkinter import ttk

class AudioManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.current_msg_id = 0
        self._actif = False
        self._rate = 175     # Vitesse de la parole

    @property
    def rate(self) -> int:
        """Getter : récupère la vitesse de parole."""
        return self._rate

    @rate.setter
    def rate(self, vitesse: int) -> None:
        """Setter : change la vitesse avec validation (50-300)."""
        if not 50 <= vitesse <= 300:
            raise ValueError("La vitesse doit être entre 50 et 300")
        self._rate = vitesse

    @property
    def actif(self) -> bool:
        """Getter : récupère l'état du mode accessibilité."""
        return self._actif

    @actif.setter
    def actif(self, etat: bool) -> None:
        """Setter : change l'état du mode accessibilité avec validation."""
        if not isinstance(etat, bool):
            raise ValueError("L'état doit être un booléen (True/False)")
        self._actif = etat

    def set_actif(self, etat: bool):
        self.actif = etat   # setter appelé

    def parler(self, texte):
        if not self.actif:  # getter appelé
            return
        self.current_msg_id += 1
        this_msg_id = self.current_msg_id 
        
        thread = threading.Thread(target=self._speak_one_shot, args=(texte, this_msg_id))
        thread.start()

    def _speak_one_shot(self, texte, msg_id):
        with self.lock:
            # dernier msg demandé ?
            if msg_id != self.current_msg_id:
              # interrompu par un autre message
                return

            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', self.rate) # getter
                
                engine.say(texte)
                engine.runAndWait()
            except Exception as e:
                print(f"[Erreur Audio] : {e}")

    def setup_full_accessibility(self, page, controller=None, back_page=None):
        buttons = []
        def find_buttons(widget):
            if isinstance(widget, ttk.Button):
                buttons.append(widget)
            for child in widget.winfo_children():
                find_buttons(child)
    
        find_buttons(page)

        for i, btn in enumerate(buttons):
            btn.bind("<Up>", lambda e, b=buttons[i-1]: b.focus_set())
            btn.bind("<Down>", lambda e, b=buttons[(i+1) % len(buttons)]: b.focus_set())
            btn.bind("<FocusIn>", lambda e, text=btn['text']: self.parler(f"Bouton : {text}"))
            
            btn.bind("<Return>", lambda e, b=btn: b.invoke())
            btn.bind("<space>", lambda e, b=btn: b.invoke())
            btn.bind("<Right>", lambda e, b=btn: b.invoke())
         
            if back_page and controller and "Retour" in btn['text']:
                btn.bind("<Left>", lambda e: controller.show_page(back_page))
        return buttons

    def setup_treeview_accessibility(self, treeview, speak_callback, validate_callback=None, back_callback=None):
        if not self.actif:
            return

        def navigate_up(event):
            selection = treeview.selection()
            if not selection:
                return

            current = selection[0]
            children = treeview.get_children()
            try:
                idx = children.index(current)
                if idx > 0:
                    new_idx = idx - 1
                    treeview.selection_set(children[new_idx])
                    treeview.see(children[new_idx])
                    speak_callback(event)
            except ValueError:
                pass

        def navigate_down(event):
            selection = treeview.selection()
            if not selection:
                return

            current = selection[0]
            children = treeview.get_children()
            try:
                idx = children.index(current)
                if idx < len(children) - 1:
                    new_idx = idx + 1
                    treeview.selection_set(children[new_idx])
                    treeview.see(children[new_idx])
                    speak_callback(event)
            except ValueError:
                pass

        treeview.bind("<Up>", navigate_up)
        treeview.bind("<Down>", navigate_down)
        if validate_callback:
            treeview.bind("<Right>", validate_callback)
        if back_callback:
            treeview.bind("<Left>", back_callback)
        
        # Focus sur le premier item
        if treeview.get_children():
            first_item = treeview.get_children()[0]
            treeview.selection_set(first_item)
            treeview.focus_set()
            speak_callback(None)

    def setup_form_buttons(self, buttons, controller=None, back_page=None):
    
        if not self.actif:
            return
        
        for i, btn in enumerate(buttons):
            btn.bind("<Tab>", lambda e, b=buttons[(i+1) % len(buttons)]: b.focus_set())
            btn.bind("<shift-Tab>", lambda e, b=buttons[(i-1) % len(buttons)]: b.focus_set())
            btn.bind("<Return>", lambda e, b=btn: b.invoke())
            btn.bind("<space>", lambda e, b=btn: b.invoke())
            btn.bind("<FocusIn>", lambda e, text=btn['text']: self.parler(f"Bouton : {text}"))
        
        if back_page and controller and buttons:
            buttons[0].bind("<Escape>", lambda e: controller.show_page(back_page))