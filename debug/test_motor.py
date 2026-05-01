import time

from furpberry.util.motor import Motor

motor = Motor()

# Enable the motor driver (take it out of standby)
motor.set_standby()
motor.set_clockwise()
motor.set_duty_cycle(50)
# Start the motor
motor.start()
time.sleep(10)
motor.stop()