from furpberry.util.logger import configure_logging
import os
import time
from pathlib import Path
from random import randint

from PIL import Image

from furpberry.main import crop_image
from furpberry.util.display import Display

configure_logging("DEBUG")

# Use rotation=0 for testing (doesn't matter for square images)
eye_0 = Display(0, rotation=270, invert=False)
eye_1 = Display(1, rotation=90, invert=False)

eye_width = 240
eye_height = 240

image_dir = Path(__file__).parent.parent / "src/furpberry/util/img"
images: list[str] = sorted(os.listdir(image_dir))
idx = randint(0, len(images) - 1)

try:
    print("Displaying initial image, press CTRL+C to move to the next stage (looping through images).")
    initial_img = str(Path(__file__).parent / "test_image.bmp")
    left_crop, right_crop = crop_image(initial_img, eye_width, eye_height)

    eye_0.open_eye(right_crop)
    eye_1.open_eye(left_crop)
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("CTRL+C pressed, cleaning up")

try:
    print("Testing displays by looping through eyeball images every 3s, press CTRL+C to stop looping.")
    while True:
        idx = idx if idx < len(images) else 0
        image_filename = os.path.join(image_dir, images[idx])
        left_crop, right_crop = crop_image(image_filename, eye_width, eye_height)

        eye_0.open_eye(right_crop)
        eye_1.open_eye(left_crop)

        time.sleep(1)
        idx += 1
except KeyboardInterrupt:
    print("CTRL+C pressed, cleaning up")
finally:
    eye_0.close_eye()
    eye_1.close_eye()
