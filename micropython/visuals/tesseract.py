import time, math
from machine import Pin, I2C
import ssd1306

# Set up I2C and OLED (assumes 128x32 resolution)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

# Generate 16 vertices for a tesseract (4D hypercube)
vertices = []
for x in [-1, 1]:
    for y in [-1, 1]:
        for z in [-1, 1]:
            for w in [-1, 1]:
                vertices.append([x, y, z, w])

# Determine edges: two vertices are connected if they differ in exactly one coordinate.
edges = []
n = len(vertices)
for i in range(n):
    for j in range(i+1, n):
        diff = 0
        for k in range(4):
            if vertices[i][k] != vertices[j][k]:
                diff += 1
        if diff == 1:
            edges.append((i, j))

def rotate4d(point, angle):
    """Rotate a 4D point in the x-w and y-z planes."""
    x, y, z, w = point
    ca = math.cos(angle)
    sa = math.sin(angle)
    # Rotate in x-w plane
    x_new = x * ca - w * sa
    w_new = x * sa + w * ca
    # Rotate in y-z plane
    y_new = y * ca - z * sa
    z_new = y * sa + z * ca
    return [x_new, y_new, z_new, w_new]

def project_point(point, d4=3, d3=3):
    """
    Project a 4D point to 2D using two-stage perspective projection.
    First, project from 4D to 3D, then from 3D to 2D.
    """
    x, y, z, w = point
    # 4D -> 3D perspective projection
    factor4 = d4 / (d4 - w)
    x3 = x * factor4
    y3 = y * factor4
    z3 = z * factor4
    # 3D -> 2D perspective projection
    factor3 = d3 / (d3 - z3)
    x2 = x3 * factor3
    y2 = y3 * factor3
    return x2, y2

angle = 0
scale = 10  # scale factor to enlarge the projection for our small screen

while True:
    projected = []
    # Rotate and project every vertex
    for v in vertices:
        r = rotate4d(v, angle)
        x2, y2 = project_point(r)
        # Center the result on the OLED display (128x32)
        x_screen = int(128/2 + x2 * scale)
        y_screen = int(32/2 + y2 * scale)
        projected.append((x_screen, y_screen))
    
    # Clear and draw all edges
    oled.fill(0)
    for e in edges:
        p1 = projected[e[0]]
        p2 = projected[e[1]]
        oled.line(p1[0], p1[1], p2[0], p2[1], 1)
    oled.show()
    
    time.sleep(0.05)
    angle += 0.1
