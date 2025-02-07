from machine import Pin, I2C
import ssd1306
import time

# Set up I2C and OLED (128x32)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

def draw_sequencer(current_step, track_length):
    oled.fill(0)  # Clear display
    step_width = 128 // track_length
    y = 10
    box_height = 12
    for i in range(track_length):
        x = i * step_width + 1  # margin for spacing
        w = step_width - 2
        if i == current_step:
            oled.fill_rect(x, y, w, box_height, 1)  # active step (filled)
        else:
            oled.rect(x, y, w, box_height, 1)         # inactive step (outline)
    oled.show()

track_length = 16  # Change this value between 1 and 16

while True:
    for current_step in range(track_length):
        draw_sequencer(current_step, track_length)
        time.sleep(0.3)  # Adjust timing to control playback speed

