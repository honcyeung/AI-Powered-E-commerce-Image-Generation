from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import os

IMAGE_PATH = "./images/"
EDITED_IMAGE_PATH = "./edited_images/"

def standardize_size(image, target_size = (1080, 1080)):

    # Use LANCZOS for the highest quality downsampling
    return image.resize(target_size, Image.Resampling.LANCZOS)

def enhance_image(image, brightness_factor = 1.05, contrast_factor = 1.15):

    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness_factor)

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast_factor)

    return image

def save_optimized_image(image, unique_id, quality = 90):

    try:
        output_image_path = os.path.join(EDITED_IMAGE_PATH, f'{unique_id}_edited.jpg')
        final_image = image.convert("RGB")  # Ensure it's in RGB mode for JPEG
        final_image.save(output_image_path, 'JPEG', quality = quality, optimize = True)
        print(f"Optimized image {unique_id} saved.")

    except Exception as e:
        print(f"Error: {e}")

        return

def run_edit_pipeline(unique_id):

    try:
        input_image_path = os.path.join(IMAGE_PATH, f'{unique_id}.jpg')
        image = Image.open(input_image_path)

        image_resized = standardize_size(image)
        image_enhanced = enhance_image(image_resized)
        save_optimized_image(image_enhanced, unique_id)

        return image_enhanced

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_image_path}")

        return
    except Exception as e:
        print(f"Error: {e}")

        return

