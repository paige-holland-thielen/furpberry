from furpberry.util.pins import Pin
from furpberry.util.logger import get_logger
import RPi.GPIO as GPIO

logger = get_logger(__name__)


class LightSense:
    def __init__(self, measurement_pin: Pin = Pin.PI40):
        self.measurement_pin = measurement_pin.value

        # set up GPIO pin for light sensor as input
        GPIO.setup(self.measurement_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def measure(self) -> bool:
        """Returns True if light is detected"""
        result = GPIO.input(self.measurement_pin) == GPIO.HIGH
        logger.debug(f"Light sensor: {'LIGHT DETECTED' if result else 'no light'}")
        return result

    def wait_for_edge(self, type: GPIO):
        GPIO.wait_for_edge(self.measurement_pin, type)
