#!/usr/bin/env python3
"""Basic ST7789 test - bypasses our Display class"""

import ST7789 as st7789
from PIL import Image, ImageDraw
import time

print("=== Basic ST7789 Test ===")

# Test right eye first (SPI CS0)
print("\n1. Testing RIGHT eye (CS0) - should show solid RED")

display = st7789.ST7789(
    height=240,
    width=240,
    rotation=0,
    port=0,
    cs=0,          # Right eye
    dc=25,         # BCM 25 (Pin 22)
    rst=6,         # BCM 6 (Pin 31)
    backlight=5,   # BCM 5 (Pin 29)
    spi_speed_hz=20 * 1000 * 1000,
)

print("Initializing display...")
display.begin()

print("Creating red image...")
img = Image.new('RGB', (240, 240), color='red')

print("Sending to display...")
display.display(img)

print("Turning on backlight...")
display.set_backlight(True)

print("You should see a RED screen on the right eye for 5 seconds")
time.sleep(5)

print("\n2. Testing solid BLUE")
img = Image.new('RGB', (240, 240), color='blue')
display.display(img)
time.sleep(3)

print("\n3. Testing solid GREEN")
img = Image.new('RGB', (240, 240), color='green')
display.display(img)
time.sleep(3)

print("\n4. Testing pattern with shapes")
img = Image.new('RGB', (240, 240), color='black')
draw = ImageDraw.Draw(img)
draw.rectangle([(20, 20), (220, 220)], outline='white', width=5)
draw.ellipse([(60, 60), (180, 180)], fill='yellow')
display.display(img)
time.sleep(3)

print("\n5. Turning off backlight")
display.set_backlight(False)

print("\nTest complete!")
print("\nDid you see colors on the display? (yes/no)")
