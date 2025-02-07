import time, math
from machine import Pin, I2C
import ssd1306

# Setup I2C and OLED (128×32)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

width, height = 128, 32
phase = 0

while True:
    oled.fill(0)
    for x in range(width):
        # Combine two sine waves for a more complex pattern
        y = int((math.sin((x + phase) * 0.1) + math.sin((x + phase) * 0.05)) * 4 + height // 2)
        oled.pixel(x, y, 1)
    oled.show()
    phase += 1
    time.sleep(0.03)
