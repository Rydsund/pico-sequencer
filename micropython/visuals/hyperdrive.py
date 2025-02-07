import time, math, random
from machine import Pin, I2C
import ssd1306

# Setup I2C and OLED (128×32)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

width, height = 128, 32
center_x, center_y = width // 2, height // 2
num_stars = 50
scale = 20  # scale factor for star displacement

# Each star: [angle, distance]
stars = []
for _ in range(num_stars):
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(0, 1)
    stars.append([angle, distance])

while True:
    oled.fill(0)
    for star in stars:
        angle, dist = star
        prev_dist = dist
        # Accelerate star (tweak these factors to change the effect)
        dist = dist * 1.15 + 0.3
        star[1] = dist

        # Compute previous and current positions
        x_prev = center_x + math.cos(angle) * prev_dist * scale
        y_prev = center_y + math.sin(angle) * prev_dist * scale
        x = center_x + math.cos(angle) * dist * scale
        y = center_y + math.sin(angle) * dist * scale

        # Draw a line from the previous to the new position
        oled.line(int(x_prev), int(y_prev), int(x), int(y), 1)

        # If the star moves off-screen, reinitialize it
        if x < 0 or x >= width or y < 0 or y >= height:
            star[0] = random.uniform(0, 2 * math.pi)
            star[1] = 0

    oled.show()
    time.sleep(0.05)
