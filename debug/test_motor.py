import time

from furpberry.util.logger import configure_logging
from furpberry.util.motor import Motor

configure_logging("DEBUG")

duty_cycle = 1
motor = Motor(dutyCycle=duty_cycle)

# Enable the motor driver (take it out of standby)
motor.set_standby()
motor.set_clockwise()

print("Testing motor, press CTRL+C to move to next phase (loop through duty cycles")
try:
    motor.start()
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("CTRL+C pressed, cleaning up")
finally:
    print("Stopping motor")
    motor.stop()

test_cycles = [10, 25, 50, 100, 50, 25, 10, 1]
idx = 0

print("Testing different duty cycles, press CTRL+C to stop motor and exit")
try:
    motor.start()
    while True:
        idx = idx if idx < len(test_cycles) else 0
        print(f"Setting duty cycle to: {test_cycles[idx]}")
        motor.set_duty_cycle(test_cycles[idx])
        time.sleep(5)
        idx += 1
except KeyboardInterrupt:
    print("CTRL+C pressed, cleaning up")
finally:
    print("Stopping motor")
    motor.stop()
    motor.reset()
