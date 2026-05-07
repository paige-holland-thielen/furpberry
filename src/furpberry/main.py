import time
from random import randint
from typing import Any

import click
from importlib_resources import files
from PIL import Image
import os
import furpberry.util.img
from furpberry.util.logger import configure_logging, get_logger
from furpberry.util.google_home import GoogleHome
from furpberry.util.light_sensor import LightSense
from furpberry.util.motor import Motor
from furpberry.util.display import Display

logger = get_logger(__name__)


class Furby:
    def __init__(
        self,
        x_offset: int = 0,
        y_offset: int = 0,
        height: int = 240,
        width: int = 240,
        l_rotation: int = 180,
        r_rotation: int = 0,
        invert: bool = False,
    ) -> None:
        self.eye_height = height
        self.eye_width = width
        self.left_eye: Display = Display(1, x_offset, y_offset, height, width, l_rotation, invert)
        self.right_eye: Display = Display(0, x_offset, y_offset, height, width, r_rotation, invert)
        self.light_sensor = LightSense()
        self.motor = Motor()
        self.google_home = GoogleHome("furby")

        self.image_dir = files(furpberry.util).joinpath('resized_images')
        self.images: list[str] = sorted(os.listdir(self.image_dir))
        self.starting_image_index: int = -1

    def open_eyes(self, starting_image_index: int) -> None:
        # crop image into two images
        # display left half on left eye
        # display right_eye half on right_eye eye
        self.starting_image_index = starting_image_index if starting_image_index < len(self.images) else 0
        image_filename = self.images[self.starting_image_index]
        logger.debug(f"Opening eyes with image: {image_filename}")

        image_path = os.path.join(self.image_dir, image_filename)
        left_crop, right_crop = crop_image(image_path, self.eye_width, self.eye_height)

        self.left_eye.open_eye(left_crop)
        self.right_eye.open_eye(right_crop)

    def close_eyes(self) -> None:
        self.left_eye.close_eye()
        self.right_eye.close_eye()

    def roll_eyes(self):
        self.open_eyes(self.starting_image_index)
        self.starting_image_index += 1
        time.sleep(1)

    def wake_up_and_dance(self):
        # move motor and
        # cycle through eyeball images
        logger.info("Furby waking up!")
        starting_eyes_index = randint(0, len(self.images) - 1)
        self.motor.start()
        self.open_eyes(starting_eyes_index)
        while self.light_sensor.measure() or self.google_home.read_status():
            self.roll_eyes()
        logger.info("Furby going to sleep")
        self.close_eyes()
        self.motor.stop()


def crop_image(image_path: str, height: int, width: int) -> tuple[Any, Any]:
    image_original = Image.open(image_path)
    image_resized = image_original.resize((width * 2, height))

    left_crop = image_resized.crop((0, 0, width, height))
    right_crop = image_resized.crop((0 + width, 0, width * 2, height))
    return left_crop, right_crop


@click.command()
@click.option("--log_level", default="INFO", help="Log level", type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]))
def run_furby(log_level: str) -> None:
    # Configure logging
    configure_logging(log_level)
    logger.info(f"Starting Furby with log level: {log_level}")

    furby = Furby()
    try:
        while True:
            if furby.light_sensor.measure() or furby.google_home.read_status():
                furby.wake_up_and_dance()
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down Furby")
        furby.close_eyes()


if __name__ == "__main__":
    run_furby("DEBUG")
