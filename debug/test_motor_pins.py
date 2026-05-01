#!/usr/bin/env python3
"""Diagnose TB6612 motor driver connection issues"""

import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

print("=== TB6612 Motor Driver Pin Test ===\n")

# Motor control pins (from motor.py)
PWM_PIN = 4   # Physical Pin 7
IN1_PIN = 18  # Physical Pin 12
IN2_PIN = 17  # Physical Pin 11
STBY_PIN = 27 # Physical Pin 13

print("Pin Configuration:")
print(f"  PWM (PWMA):  BCM {PWM_PIN}  (Physical Pin 7)")
print(f"  IN1 (AIN1):  BCM {IN1_PIN}  (Physical Pin 12)")
print(f"  IN2 (AIN2):  BCM {IN2_PIN}  (Physical Pin 11)")
print(f"  STBY:        BCM {STBY_PIN} (Physical Pin 13)")
print()

# Setup pins
GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.setup(IN1_PIN, GPIO.OUT)
GPIO.setup(IN2_PIN, GPIO.OUT)
GPIO.setup(STBY_PIN, GPIO.OUT)

print("Test 1: Pin Toggle Test")
print("-" * 60)
print("Testing if each pin can output HIGH/LOW signals\n")

test_pins = [
    (STBY_PIN, 13, "STBY"),
    (IN1_PIN, 12, "IN1/AIN1"),
    (IN2_PIN, 11, "IN2/AIN2"),
    (PWM_PIN, 7, "PWM/PWMA"),
]

for bcm, physical, name in test_pins:
    print(f"Testing {name} (Physical Pin {physical})...")
    for i in range(3):
        GPIO.output(bcm, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(bcm, GPIO.LOW)
        time.sleep(0.2)
    print(f"  ✓ Pin {physical} toggled 3 times")

print("\nTest 2: Try multiple directions and duty cycles")
print("-" * 60)
print("Testing for mechanical limitations in housing\n")

# Enable driver
GPIO.output(STBY_PIN, GPIO.HIGH)
print("✓ STBY set HIGH (driver enabled)\n")

# Create PWM object
pwm = GPIO.PWM(PWM_PIN, 100)  # 100 Hz

# Test configurations
test_configs = [
    ("Clockwise", GPIO.HIGH, GPIO.LOW, [25, 50, 75, 100]),
    ("Counter-clockwise", GPIO.LOW, GPIO.HIGH, [25, 50, 75, 100]),
]

motor_worked = False

for direction_name, in1_state, in2_state, duty_cycles in test_configs:
    print(f"\n{direction_name} Direction Test:")
    print("-" * 40)
    GPIO.output(IN1_PIN, in1_state)
    GPIO.output(IN2_PIN, in2_state)
    print(f"Set direction: IN1={in1_state}, IN2={in2_state}")

    for dc in duty_cycles:
        print(f"\n  Testing {dc}% duty cycle...")
        pwm.start(dc)
        print(f"  Motor running at {dc}% - listen/feel for movement")
        time.sleep(3)
        pwm.stop()

        response = input(f"  Did motor move/hum/anything at {dc}%? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            motor_worked = True
            print(f"  ✓ Motor responded at {direction_name} {dc}%!")
        else:
            print(f"  ✗ No response at {direction_name} {dc}%")

        time.sleep(1)  # Pause between tests

print("\n" + "="*60)
print("Test 3: Rapid direction changes (if motor worked)")
print("="*60)

if motor_worked:
    print("\nTesting quick direction reversals (may help if stuck)...\n")

    for i in range(5):
        print(f"Pulse {i+1}/5 - Clockwise")
        GPIO.output(IN1_PIN, GPIO.HIGH)
        GPIO.output(IN2_PIN, GPIO.LOW)
        pwm.start(75)
        time.sleep(0.5)
        pwm.stop()

        time.sleep(0.2)

        print(f"Pulse {i+1}/5 - Counter-clockwise")
        GPIO.output(IN1_PIN, GPIO.LOW)
        GPIO.output(IN2_PIN, GPIO.HIGH)
        pwm.start(75)
        time.sleep(0.5)
        pwm.stop()

        time.sleep(0.2)

    print("\n✓ Direction pulse test complete")
else:
    print("\nSkipping pulse test - no response detected")

# Cleanup
GPIO.output(STBY_PIN, GPIO.LOW)
GPIO.output(IN1_PIN, GPIO.LOW)
GPIO.output(IN2_PIN, GPIO.LOW)
print("\n✓ Motor stopped and disabled")

print("\n" + "="*60)
print("WIRING CHECKLIST")
print("="*60)
print("\nTB6612 Pin → Connection")
print("-" * 60)
print("POWER:")
print("  VCC  → 3.3V or 5V (logic power for TB6612 chip)")
print("  VM   → Motor voltage (4.5V-13.5V, typically 6V battery)")
print("  GND  → Ground (MUST be shared with Pi GND)")
print()
print("CONTROL (from Raspberry Pi):")
print("  PWMA → Physical Pin 7  (BCM 4)")
print("  AIN1 → Physical Pin 12 (BCM 18)")
print("  AIN2 → Physical Pin 11 (BCM 17)")
print("  STBY → Physical Pin 13 (BCM 27)")
print()
print("MOTOR OUTPUT:")
print("  AO1  → Motor wire 1 (polarity doesn't matter)")
print("  AO2  → Motor wire 2")
print()

print("="*60)
print("TROUBLESHOOTING")
print("="*60)
print()

response = input("Did the motor do ANYTHING? (yes/no): ").strip().lower()

if response in ['yes', 'y']:
    print("\n✓ Motor responded! Check:")
    print("  - If it hummed but didn't spin: VM voltage too low")
    print("  - If it spun weakly: Increase PWM duty cycle")
    print("  - If it spun: Everything is working!")
else:
    print("\n✗ Motor did nothing. Most likely issues:")
    print()
    print("1. VM (motor power) not connected")
    print("   - TB6612 needs BOTH VCC (logic) AND VM (motor power)")
    print("   - VM should be 6V from battery, not from Pi")
    print("   - Check: Does VM pin have voltage?")
    print()
    print("2. Ground not shared")
    print("   - Pi GND MUST connect to TB6612 GND")
    print("   - Battery GND MUST connect to TB6612 GND")
    print("   - All grounds must be connected together")
    print()
    print("3. Motor not connected to AO1/AO2")
    print("   - Motor wires should go to AO1 and AO2 on TB6612")
    print()
    print("4. TB6612 damaged or not powered")
    print("   - Check VCC has 3.3V or 5V")
    print("   - Check VM has battery voltage (6V)")
    print()
    print("5. Wrong motor")
    print("   - Does motor work when connected directly to battery?")
    print()

print("\nNEXT STEPS:")
print("  1. Use multimeter to check TB6612 VCC and VM voltages")
print("  2. Verify ground connections between Pi, TB6612, and battery")
print("  3. Test motor directly with battery (bypass TB6612)")
print()

GPIO.cleanup()
print("✓ GPIO cleaned up")