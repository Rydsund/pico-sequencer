import time, math
from machine import Pin, I2C
import ssd1306

# Setup I2C and OLED (128×32)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

width, height = 128, 32
center_x, center_y = width // 2, height // 2
angle_offset = 0

while True:
    oled.fill(0)
    # Draw lines at 30° intervals
    for i in range(0, 360, 30):
        a = math.radians(i + angle_offset)
        # Adjust multipliers to suit the screen's aspect ratio
        x = center_x + int(math.cos(a) * 60)
        y = center_y + int(math.sin(a) * 15)
        oled.line(center_x, center_y, x, y, 1)
    oled.show()
    angle_offset += 5
    time.sleep(0.1)
