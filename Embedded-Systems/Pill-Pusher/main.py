from pdisplay import Display
from pbuzzer import PillBuzzer
from pinput import Input
from pmotor import Motor
from pled import Blinker
from prfid import RFID
from time import sleep, ticks_ms, ticks_diff

# --- CONSTANTS ---
SCAN_TIMEOUT = 5000 
BLUE_TAG = 3775564842

# Component Setup
display = Display(18, 19)
display.show_loading_sequence() # Plays branding animation first

buzzer = PillBuzzer(16)
blinker = Blinker(15, 0.2)
motor = Motor(20)

pill_served = False
reset_window = False # Flag to restart scan window after error

def scanned(card_id):
    """Callback for RFID tag detection."""
    global pill_served, reset_window
    if pill_served: return
    
    if card_id == BLUE_TAG:
        display.display_card_accepted()
        blinker.stop()
        buzzer.stop() 
        pill_served = True
    else:
        display.display_invalid_card(card_id)
        # Restart the 5s Scan Window
        reset_window = True 

def input_confirmed(hr, mn):
    """Callback for button confirmation."""
    global delay_sec, countdown 
    display.display_confirmation(hr, mn)
    if hr == 0 and mn == 0:
        delay_sec = 2 # Demo mode interval
    else:
        delay_sec = mn * 60 + hr * 3600
    countdown = delay_sec
    
def timer_elapsed():
    """Alarm loop. Alternates between music and active scan window."""
    global pill_served, reset_window
    blinker.start()
    
    while not pill_served:
        # Phase 1: Alarm song (Pico is busy here)
        display.display_pill_reminder() # "GET CARD READY"
        buzzer.play_tune() 
        
        # Phase 2: Active Scan Window (Sun animation)
        start_time = ticks_ms()
        while ticks_diff(ticks_ms(), start_time) < SCAN_TIMEOUT:
            if pill_served: break
            
            # Restart window if invalid tag was detected
            if reset_window:
                start_time = ticks_ms()
                reset_window = False
            
            elapsed = ticks_diff(ticks_ms(), start_time)
            remaining = SCAN_TIMEOUT - elapsed
            
            # Update 'Sun' animation
            display.display_scan_window(remaining, SCAN_TIMEOUT)
            
            rfid.update()
            sleep(0.01)
        
        # Reset visual state if timeout occurred before scan
        if not pill_served:
            display.display_pill_reminder()
                
    # Phase 3: Servo animation and mechanical push
    for i in range(11):
        display.display_serving(i)
        sleep(0.05)
    motor.push_pill() 
    pill_served = False

# Initialize input listeners
input = Input(13, 12, 11, input_confirmed, display)
rfid = RFID(0, 2, 4, 3, 1, 0, scanned)

# Initial screen shown after the 4s loading sequence
display.display_timer_setup(0, 0)

while True:
    if input.confirmed: # Check if Confirm button was pressed
        if countdown > 0:
            display.display_countdown(countdown, delay_sec) 
            countdown -= 1
            sleep(1)
            if countdown == 0:
                timer_elapsed()
                countdown = delay_sec
            continue
    sleep(0.1)