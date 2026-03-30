# Servo Motor code 
# Migrated from https://wokwi.com/projects/429869337693554689

from machine import Pin, PWM
from time import sleep

class Motor:
    def __init__(self, pin):
        self.servo = PWM(Pin(pin))
        self.servo.freq(50)  # 50Hz is standard for servo motors

    # Function to move the servo to a specific angle
    def move_servo(self, angle):
        min_duty = 1638   # 0 degrees (~0.5ms pulse)
        max_duty = 8192   # 180 degrees (~2.5ms pulse)
        duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
        self.servo.duty_u16(duty)

    # Pill pushing sequence
    def push_pill(self):
        print("Pushing pill...")
        self.move_servo(120)    # Move to push position (90 degrees)
        sleep(2)          # Wait for 1 second
        self.move_servo(0)     # Return to original position
        print("Returned to rest.")