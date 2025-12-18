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
        for widget in page.winfo_children():
            if isinstance(widget, ttk.Button):
                buttons.append(widget)

        for i, btn in enumerate(buttons):
            btn.bind("<Up>", lambda e, b=buttons[i-1]: b.focus_set())
            btn.bind("<Down>", lambda e, b=buttons[(i+1) % len(buttons)]: b.focus_set())
            btn.bind("<FocusIn>", lambda e, text=btn['text']: self.parler(f"Bouton : {text}"))
            
            if back_page and controller:
                btn.bind("<Left>", lambda e: controller.show_page(back_page))
            btn.bind("<Right>", lambda e, b=btn: b.invoke())

        return buttons