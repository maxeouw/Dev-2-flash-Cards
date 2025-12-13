import threading
import pyttsx3

class AudioManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.current_msg_id = 0
        self.actif = False

    def set_actif(self, etat: bool):
        self.actif = etat

    def parler(self, texte):
        if not self.actif:
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
                engine.setProperty('rate', 150)
                
                engine.say(texte)
                engine.runAndWait()
            except Exception as e:
                print(f"[Erreur Audio] : {e}")