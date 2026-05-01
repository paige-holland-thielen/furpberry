#!/usr/bin/env python3
"""Test light sensor wiring and configuration"""

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PIN = 21  # Pin.PI40 = GPIO 21

print("Testing light sensor on GPIO 21 (Pin 40)")
print("\n=== Test 1: Pull-DOWN (for photoresistor to 3.3V) ===")
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
time.sleep(0.1)

for i in range(5):
    state = GPIO.input(PIN)
    print(f"Reading {i+1}: {state} ({'HIGH' if state else 'LOW'})")
    time.sleep(0.5)

print("\n=== Test 2: Pull-UP (for photoresistor to GND) ===")
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
time.sleep(0.1)

for i in range(5):
    state = GPIO.input(PIN)
    print(f"Reading {i+1}: {state} ({'HIGH' if state else 'LOW'})")
    time.sleep(0.5)

print("\nNow cover the sensor completely and watch for changes...")
print("Press Ctrl+C to exit\n")

try:
    last_state = None
    while True:
        state = GPIO.input(PIN)
        if state != last_state:
            print(f"State changed: {state} ({'HIGH' if state else 'LOW'})")
            last_state = state
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nDone!")
    GPIO.cleanup()