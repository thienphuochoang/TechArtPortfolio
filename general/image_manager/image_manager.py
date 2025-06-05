import os
import requests
from PIL import Image
from io import BytesIO

class ImageManager:
    @staticmethod
    def save_image_from_url(output_dir: str, image_name: str, image_url: str):
        os.makedirs(output_dir, exist_ok=True)
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content)).convert("RGB")
            image.save(os.path.join(output_dir, image_name))
            print(f"Saved: {image_name}")
        except Exception as e:
            print(f"Failed to save {image_name}: {e}")

    @staticmethod
    def scale_down_image(image: Image.Image, max_size: int) -> Image.Image:
        """
        Resize the image while keeping aspect ratio, so the longest side is max_size.
        """
        image.thumbnail((max_size, max_size), Image.ANTIALIAS)
        return image

    @staticmethod
    def convert_to_grayscale(image: Image.Image) -> Image.Image:
        return image.convert("L")

    @staticmethod
    def convert_to_rgba(image: Image.Image) -> Image.Image:
        return image.convert("RGBA")