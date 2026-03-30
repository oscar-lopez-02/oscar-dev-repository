from machine import Pin, I2C
from utime import sleep_ms
import ssd1306
import framebuf
import math

class Display:
    def __init__(self, sda, scl):
        """Initializes I2C pins and the SSD1306 OLED display driver."""
        _sda, _scl = Pin(sda), Pin(scl)
        i2c = I2C(1, sda=_sda, scl=_scl, freq=400000)
        self.display = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3C)

    def display_scan_window(self, remaining_ms, total_ms):
        """Creates the 'Solid Sun' radial wipe animation to indicate scan time left."""
        self.display.fill(0)
        ratio = 1.0 - (remaining_ms / total_ms)
        
        # Base layers: Text and Pill drawn first
        self.display.text("MEDICATION TIME!", 0, 0, 1)
        self.draw_pill_image(40, 20, 48, 24, 1)
        self.display.text("SCAN NOW!", 28, 54, 1)

        # Solid Radial Fill: Draws 250 lines from center to edges for a solid look
        cx, cy, r = 64, 32, 85 
        steps = int(ratio * 250) 
        for i in range(steps):
            # Calculate angle moving clockwise starting from 12 o'clock
            angle = (i / 250 * 2 * math.pi) - (math.pi / 2)
            x = int(cx + r * math.cos(angle))
            y = int(cy + r * math.sin(angle))
            self.display.line(cx, cy, x, y, 1)

        # Contrast Inversion: Flips pixels to black as the white 'Sun' covers them
        if ratio > 0.1: self.display.text("MEDICATION TIME!", 0, 0, 0)
        if ratio > 0.4: self.draw_pill_image(40, 20, 48, 24, 0)
        if ratio > 0.8: self.display.text("SCAN NOW!", 28, 54, 0)
        self.display.show()

    def display_pill_reminder(self):
        """Static reminder shown during the buzzer melody phase."""
        self.display.fill(0)
        self.display.text("MEDICATION TIME!", 0, 0, 1)
        self.draw_pill_image(40, 20, 48, 24, 1)
        self.display.text("GET CARD READY", 8, 54, 1)
        self.display.show()

    def draw_pill_image(self, x, y, width, height, color=1):
        """Helper to render the pill frame-buffer graphic."""
        buffer = bytearray(width * height // 8)
        frame = framebuf.FrameBuffer(buffer, width, height, framebuf.MONO_HLSB)
        frame.hline(2, 0, width - 4, color)
        frame.hline(2, height - 1, width - 4, color)
        frame.vline(0, 2, height - 4, color)
        frame.vline(width - 1, 2, height - 4, color)
        frame.vline(width // 2, 0, height, color)
        self.display.blit(frame, x, y)

    def show_loading_sequence(self):
        """Plays the 4-second startup sequence with the 'spu-robotomy' credit."""
        for i in range(0, 101, 2):
            self.display.fill(0)
            self.display.text("PILL PUSHER", 20, 10, 1)
            self.display.text("by spu-robotomy", 4, 25, 1)
            self.display.rect(14, 45, 100, 10, 1)
            fill_w = int(i * 0.96)
            self.display.fill_rect(16, 47, fill_w, 6, 1)
            self.display.text("Loading... {}%".format(i), 20, 56, 1)
            self.display.show()
            sleep_ms(80)

    def display_timer_setup(self, hours, minutes):
        """Main setup menu. If 00:00 is reached, prompts for Demo Mode."""
        self.display.fill(0)
        self.display.text("SET THE TIMER", 12, 0, 1)
        self.display.hline(0, 12, 128, 1)
        self.display.text("Hours: {:02d}".format(hours), 0, 24, 1)
        self.display.text("Mins:  {:02d}".format(minutes), 0, 36, 1)
        if hours == 0 and minutes == 0:
            self.display.fill_rect(0, 50, 128, 14, 1)
            self.display.text("ENTER TO DEMO", 12, 54, 0)
        self.display.show()

    def display_confirmation(self, hours, minutes):
        """Confirmation message before dosage countdown begins."""
        self.display.fill(0)
        self.display.rect(0, 0, 128, 64, 1)
        if hours == 0 and minutes == 0:
            self.display.text("DEMO SELECTED!", 12, 28, 1)
        else:
            self.display.text("CONFIRMED!", 24, 10, 1)
            self.display.text("INTERVAL:", 28, 30, 1)
            self.display.text("{:02d}:{:02d}:00".format(hours, minutes), 32, 45, 1)
        self.display.show()
        sleep_ms(2000)

    def display_countdown(self, remaining_time, total_time=1):
        """Active timer screen with product branding and a progress bar."""
        hours, minutes, seconds = remaining_time // 3600, (remaining_time % 3600) // 60, remaining_time % 60
        time_str = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        self.display.fill(0)
        self.display.text("PILL PUSHER", 20, 2, 1)
        self.display.hline(0, 12, 128, 1)
        self.display.text("NEXT DOSE IN:", 12, 22, 1)
        self.display.text(time_str, 32, 38, 1)
        self.display.rect(14, 54, 100, 6, 1)
        progress = int((1 - (remaining_time / max(1, total_time))) * 96)
        self.display.fill_rect(16, 56, progress, 2, 1)
        self.display.show()

    def display_invalid_card(self, card_id):
        """Error screen for unauthorized RFID tags."""
        self.display.fill(0)
        self.display.text("ACCESS DENIED!", 8, 5, 1)
        self.display.rect(0, 20, 128, 30, 1)
        self.display.text("ID:", 5, 25, 1)
        self.display.text(str(card_id)[:15], 5, 38, 1) 
        self.display.text("UNAUTHORIZED", 16, 54, 1)
        self.display.show()
        sleep_ms(2000)

    def display_card_accepted(self):
        """Success feedback screen for Blue Tag verification."""
        self.display.fill(0)
        self.display.text("ID VERIFIED", 20, 5, 1)
        self.display.rect(49, 22, 30, 20, 1)
        self.display.line(55, 32, 60, 37, 1)
        self.display.line(60, 37, 73, 27, 1)
        self.display.text("DISPENSING...", 16, 52, 1)
        self.display.show()
        sleep_ms(1500)

    def display_serving(self, frame):
        """Mechanical arm animation during pill delivery."""
        self.display.fill(0)
        self.display.text("SERVING PILL", 16, 5, 1)
        cx, cy, length = 64, 40, 18
        angle = (frame * 18) * (math.pi / 180) 
        x_end = int(cx + length * math.cos(angle))
        y_end = int(cy + length * math.sin(angle))
        self.display.rect(44, 25, 40, 30, 1)
        self.display.line(cx, cy, x_end, y_end, 1)
        self.display.show()