from buzzer import Buzzer

class PillBuzzer:
    
    f_note = 1.85 # Full Node
    h_note = 0.94 # Half Note
    q_note = 0.46 # Quarter Note
    e_note = 0.23   # Eigth Note
    
    # Small Pause with slightly shorter notes prior
    sp = 0.02
    spq = 0.44
    spe = 0.21
    
    # This is a basic song that could be used for the buzzer
    alarm_and_jeopardy_song = [
        ("C3", h_note), ("P", q_note), ("C3", h_note), ("P", q_note), ("C3", h_note),  ("P", q_note), ("C3", h_note),("P", q_note), ("C3", h_note),("P", q_note), ("C3", h_note),("P", q_note), ("C3", h_note),("P", q_note), ("C3", h_note),("P", q_note), ("C3", h_note),
        ("P", f_note),    
        ("G5", q_note), ("C6", q_note), ("G5", q_note), ("C5", spe), ("P", sp), ("C5", e_note),
        ("G5", q_note), ("C6", q_note), ("G5", q_note), ("P", q_note),
        ("G5", q_note), ("C6", q_note), ("G5", q_note), ("C6", q_note),
        ("E6", q_note), ("P", e_note), ("D6", e_note), ("C6", e_note), ("B6", e_note), ("A6", e_note), ("GS5", e_note),
        ("G5", q_note), ("C6", q_note), ("G5", q_note), ("C5", spe), ("P", sp), ("C5", e_note),
        ("G5", q_note), ("C6", q_note), ("G5", q_note), ("P", q_note),
        ("C6", q_note), ("P", e_note), ("A6", e_note), ("G5", q_note), ("F5", q_note),
        ("E5", q_note), ("D5", q_note), ("C5", q_note), ("P", q_note),
    ]
    
    def __init__(self, buzzer):
        self.buzzer = Buzzer(buzzer)
        
    def play_tune(self):
        self.buzzer.play_song(self.alarm_and_jeopardy_song)
        
    def stop(self):
        # This tells the underlying Buzzer to go silent
        self.buzzer.bequiet()
        
