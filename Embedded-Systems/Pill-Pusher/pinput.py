from machine import Pin
from time import ticks_ms, ticks_diff

# Debounce time
DEBOUNCE_DELAY = 200 # 200ms (0.2s)
    
class Input:
    
    def __init__(self, hour, min, confirm, confirmed, display):
        self.btn_hour = Pin(hour, Pin.IN, Pin.PULL_DOWN)
        self.btn_min = Pin(min, Pin.IN, Pin.PULL_DOWN)
        self.btn_ok = Pin(confirm, Pin.IN, Pin.PULL_DOWN)
        self.hours = 0
        self.minutes = 0
        self.confirmed = False
        self.display = display
        
        # init debounce tracker
        self.since_last_db = ticks_ms()
        print ("Set the timer: ")
        
        # init buttons
        self.btn_hour.irq(trigger=Pin.IRQ_RISING, handler=self.debounce)
        self.btn_min.irq(trigger=Pin.IRQ_RISING, handler=self.debounce)
        self.btn_ok.irq(trigger=Pin.IRQ_RISING, handler=self.debounce)
        
        # init callbacks
        self.time_confirmed = confirmed # lambda hr, mn : print("{:02d}:{:02d}".format(hr, mn)) # default

    def debounce(self, pin):
        global since_last_db

        cur_time = ticks_ms()

        if ticks_diff(cur_time, self.since_last_db) <= DEBOUNCE_DELAY:
            return

        self.since_last_db = cur_time

        if (pin == self.btn_hour):
            self.set_hour()
        
        elif (pin == self.btn_min):
            self.set_minute()
        
        elif (pin == self.btn_ok):
            self.confirm_time()


    def set_hour(self):
        self.hours = (self.hours + 1) % 24
        self.display.display_timer_setup(self.hours, self.minutes)
        print("Hours set to:", self.hours)


    # increment minutes
    def set_minute(self):
        if self.minutes < 5:
            self.minutes = (self.minutes + 1) % 60
        else:
            self.minutes = (self.minutes + 5) % 60
        self.display.display_timer_setup(self.hours, self.minutes)
        print("Minutes set to:", self.minutes)

    def confirm_time(self):
        
        if not self.confirmed:
            self.display.display_confirmation(self.hours, self.minutes)
            self.time_confirmed(self.hours, self.minutes)
            
        self.confirmed = not self.confirmed


