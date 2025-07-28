import base64
import os
from io import BytesIO
from typing import Optional
from huggingface_hub import InferenceClient


class ImageGeneratorService:
    """Service for generating recipe images using AI."""

    def __init__(self, api_key: Optional[str] = None, save_images: bool = True):
        self._api_key = api_key or os.environ.get("STABLE_DIFFUSION_API_KEY")
        self._save_images = save_images
        self._has_credits = True
        self._image_dir = "generated_images"

        if self._save_images:
            os.makedirs(self._image_dir, exist_ok=True)

    def generate_recipe_image(self, recipe_name: str) -> Optional[str]:
        if not self._has_credits or not self._api_key:
            return None

        try:
            client = InferenceClient(provider="nebius", api_key=self._api_key)
            prompt = f"A beautiful food image of a {recipe_name}"
            image = client.text_to_image(prompt, model="stabilityai/stable-diffusion-xl-base-1.0")

            if self._save_images:
                self._save_image_to_disk(image, recipe_name)

            return self._convert_to_base64(image)

        except Exception as e:
            print(f"\n[!] Warning: Failed to generate image for '{recipe_name}': {e}\n")
            self._has_credits = False
            return None

    def _save_image_to_disk(self, image, recipe_name: str) -> None:
        image_path = os.path.join(self._image_dir, f"{recipe_name}.jpg")

        try:
            image.save(image_path, format='JPEG', quality=85)
            print(f"Image saved: {image_path}")
        except Exception as e:
            print(f"Warning: Failed to save image for '{recipe_name}': {e}")

    @staticmethod
    def _convert_to_base64(image) -> str:
        buffer = BytesIO()
        image.save(buffer, format='JPEG', quality=85)
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
