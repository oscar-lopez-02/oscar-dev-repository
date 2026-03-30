from machine import Pin
from utime import sleep
import _thread

class Blinker:
    
    def __init__(self, led, freq):
        self.led = Pin(led, Pin.OUT)
        self.freq = freq
        self.blinking = False
        self.led.off()
        
    def start(self):
        self.blinking = True
        _thread.start_new_thread(self._blinker, ())
    
    def stop(self):
        self.blinking = False
        self.led.off()

    def _blinker(self):
        while self.blinking:
            self.led.toggle()
            sleep(self.freq)
        return

