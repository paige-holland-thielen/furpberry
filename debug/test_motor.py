import time

from furpberry.util.motor import Motor

motor = Motor()

# Enable the motor driver (take it out of standby)
motor.set_standby()
motor.set_clockwise()
motor.set_duty_cycle(25)

print("Testing motor, press CTRL+C to stop motor and exit")
try:
    while True:
        motor.start()
        time.sleep(1)
except KeyboardInterrupt:
    print("CTRL+C pressed, cleaning up")
motor.stop()
