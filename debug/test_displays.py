#!/usr/bin/env python3
"""Test display functionality - shows test patterns on both eyes"""

import time
from PIL import Image, ImageDraw, ImageFont
from furpberry.util.display import Display

print("=== Display Test ===")
print("Initializing displays...")

# Initialize both eyes
left_eye = Display(spi_id=1, rotation=180)
right_eye = Display(spi_id=0, rotation=0)

def create_test_image(text, color):
    """Create a simple test image with text"""
    img = Image.new('RGB', (240, 240), color=color)
    draw = ImageDraw.Draw(img)

    # Draw text in center
    try:
        # Try to use a large font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        # Fall back to default font
        font = ImageFont.load_default()

    # Get text size and center it
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (240 - text_width) // 2
    y = (240 - text_height) // 2

    draw.text((x, y), text, fill='white', font=font)
    return img

try:
    print("\n1. Testing LEFT eye - RED")
    red_img = create_test_image("LEFT", 'red')
    left_eye.open_eye(red_img)
    time.sleep(2)

    print("2. Testing RIGHT eye - BLUE")
    blue_img = create_test_image("RIGHT", 'blue')
    right_eye.open_eye(blue_img)
    time.sleep(2)

    print("3. Both eyes - GREEN")
    green_img = create_test_image("BOTH", 'green')
    left_eye.open_eye(green_img)
    right_eye.open_eye(green_img)
    time.sleep(2)

    print("4. Closing both eyes")
    left_eye.close_eye()
    right_eye.close_eye()
    time.sleep(1)

    print("5. Flashing eyes 3 times")
    white_img = create_test_image("BLINK", 'white')
    for i in range(3):
        print(f"   Flash {i+1}/3")
        left_eye.open_eye(white_img)
        right_eye.open_eye(white_img)
        time.sleep(0.3)
        left_eye.close_eye()
        right_eye.close_eye()
        time.sleep(0.3)

    print("\n6. Testing if you have image files...")
    try:
        from importlib_resources import files
        import furpberry.util.img
        import os

        image_dir = files(furpberry.util).joinpath('resized_images')
        if os.path.exists(image_dir):
            images = sorted(os.listdir(image_dir))
            if images:
                print(f"   Found {len(images)} images, showing first one: {images[0]}")
                test_img = Image.open(os.path.join(image_dir, images[0]))
                test_img_resized = test_img.resize((480, 240))

                left_crop = test_img_resized.crop((0, 0, 240, 240))
                right_crop = test_img_resized.crop((240, 0, 480, 240))

                left_eye.open_eye(left_crop)
                right_eye.open_eye(right_crop)
                time.sleep(3)
            else:
                print("   No image files found in resized_images")
        else:
            print("   resized_images directory not found")
    except Exception as e:
        print(f"   Could not load image files: {e}")

    print("\n7. Closing eyes")
    left_eye.close_eye()
    right_eye.close_eye()

    print("\nTest complete!")

except KeyboardInterrupt:
    print("\nTest interrupted")
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
finally:
    print("Cleaning up - closing eyes")
    left_eye.close_eye()
    right_eye.close_eye()