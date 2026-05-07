import os
import time
from pathlib import Path
from random import randint

from PIL import Image

from furpberry.main import crop_image
from furpberry.util.display import Display

eye_0 = Display(0)
eye_1 = Display(1)

eye_width = 240
eye_height = 240

image_dir = Path(__file__).parent.parent / "src/furpberry/util/resized_images"
images: list[str] = sorted(os.listdir(image_dir))
idx = randint(0, len(images) - 1)

try:
    print("Displaying initial image for 10 seconds, press CTRL+C to move to the next stage (looping through images).")
    initial_img = Image.open(Path(__file__).parent / "test_image.bmp")
    left_crop, right_crop = crop_image(initial_img, eye_width, eye_height)

    eye_0.open_eye(right_crop)
    eye_1.open_eye(left_crop)
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("CTRL+C pressed, cleaning up")

try:
    print("Testing displays by looping through eyeball images every 3s, press CTRL+C to begin looping.")
    while True:
        idx = idx if idx < len(images) else 0
        image_filename = os.path.join(image_dir, images[idx])
        left_crop, right_crop = crop_image(image_filename, eye_width, eye_height)

        eye_0.open_eye(right_crop)
        eye_1.open_eye(left_crop)

        time.sleep(3)
        idx += 1
except KeyboardInterrupt:
    print("CTRL+C pressed, cleaning up")

eye_0.close_eye()
eye_1.close_eye()
