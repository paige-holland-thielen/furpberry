from furpberry.util.pins import Pin
from furpberry.util.logger import get_logger
import RPi.GPIO as GPIO

logger = get_logger(__name__)


class Motor:
    """
    Pinouts for pi zero W motor control with TB6612.
    Motor is the motor for a 2012 Furby.
    Motor power supply is furby battery pack.
    The motor is Motor A, wired per
    https://howchoo.com/pi/controlling-dc-motors-using-your-raspberry-pi
    """

    def __init__(
        self,
        pwm: Pin = Pin.PI8,
        in1: Pin = Pin.PI12,
        in2: Pin = Pin.PI11,
        standby: Pin = Pin.PI13,
        dutyCycle: float = 25.0,
    ):
        self.pwm = pwm.value  # pin value
        self.in1 = in1.value
        self.in2 = in2.value
        self.standby = standby.value
        self.dutyCycle = dutyCycle
        self.frequency = 100

        # set up GPIO pins as outputs, initialize pwm to low, direction to clockwise
        GPIO.setup(self.pwm, GPIO.OUT, initial=GPIO.LOW)  # Connected to PWMA
        GPIO.setup(self.in2, GPIO.OUT, initial=GPIO.LOW)  # Connected to AIN2
        GPIO.setup(self.in1, GPIO.OUT, initial=GPIO.HIGH)  # Connected to AIN1
        GPIO.setup(self.standby, GPIO.OUT, initial=GPIO.HIGH)  # Connected to STBY - HIGH to enable driver

        # set up PWM
        self.motorPWM = GPIO.PWM(self.pwm, self.frequency)  # channel (pin), frequency (Hz)

    def set_duty_cycle(self, dc: float):
        logger.debug(f"Motor: duty cycle changed to {dc}%")
        self.dutyCycle = dc
        self.motorPWM.ChangeDutyCycle(dc)

    def start(self):
        logger.debug(f"Motor: START (duty cycle: {self.dutyCycle}%)")
        self.motorPWM.start(self.dutyCycle)

    def stop(self):
        logger.debug("Motor: STOP")
        self.motorPWM.stop()

    def set_clockwise(self):
        # Set the motor direction to clockwise
        GPIO.output(self.in1, GPIO.HIGH)  # Set AIN1
        GPIO.output(self.in2, GPIO.LOW)  # Set AIN2

    def set_counter_clockwise(self):
        # Set the motor direction to counterclockwise
        GPIO.output(self.in1, GPIO.LOW)  # Set AIN1
        GPIO.output(self.in2, GPIO.HIGH)  # Set AIN2

    def set_standby(self):
        # Disable STBY (standby)
        GPIO.output(self.standby, GPIO.HIGH)

    def reset(self):
        # Reset all the GPIO pins by setting them to LOW
        GPIO.output(self.in1, GPIO.LOW)  # Set AIN1
        GPIO.output(self.in2, GPIO.LOW)  # Set AIN2
        GPIO.output(self.pwm, GPIO.LOW)  # Set PWMA
        GPIO.output(self.standby, GPIO.LOW)  # Set STBY
