import base64
import os
from io import BytesIO
from huggingface_hub import InferenceClient


class RecipeImageGenerator:
    __has_credits_left = True

    def __init__(self):
        self.__stable_diffusion_api_key = os.environ.get("STABLE_DIFFUSION_API_KEY")

    def generate_with_stable_diffusion(self, recipe_name: str) -> str | None:
        if not self.__has_credits_left:
            return None

        client = InferenceClient(
            provider="nebius",
            api_key=self.__stable_diffusion_api_key
        )

        try:
            image = client.text_to_image(
                f"A beautiful small image of a {recipe_name}",
                model="stabilityai/stable-diffusion-xl-base-1.0",
            )

            # self.save_image_to_disk(image, recipe_name)

            return self.pil_to_base64(image)

        except Exception:
            self.__has_credits_left = False
            return None

    @staticmethod
    def save_image_to_disk(image, recipe_name):
        image_dir = "generated_images"
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        safe_filename = "".join(c for c in recipe_name if c.isalnum() or c in (' ', '_')).rstrip().replace(' ', '_')
        image_path = os.path.join(image_dir, f"{safe_filename}.jpg")
        image.save(image_path, format='JPEG')

        print(f"Image saved to {image_path}")

    @staticmethod
    def pil_to_base64(image):
        buffer = BytesIO()
        image.save(buffer, format='JPEG')

        return base64.b64encode(buffer.getvalue()).decode('utf-8')
