import base64
import os
import requests


class RecipeImageGenerator:
    __prompt = f"A small image for the following recipe description for a paprika recipe manager (https://www.paprikaapp.com/):"

    def __init__(self):
        self.__stable_diffusion_api_key = os.environ.get("STABLE_DIFFUSION_API_KEY")

    def generate_with_stable_diffusion(self, recipe_name: str) -> str | None:
        api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        headers = {"Authorization": f"Bearer {self.__stable_diffusion_api_key}"}

        payload = {
            "inputs": f"A beautiful small image of a {recipe_name}",
            "options": {"wait_for_model": True}
        }

        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code == 200:
            image_bytes = response.content

            image_dir = "generated_images"
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            safe_filename = "".join(c for c in recipe_name if c.isalnum() or c in (' ', '_')).rstrip().replace(' ', '_')
            image_path = os.path.join(image_dir, f"{safe_filename}.jpg")

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            print(f"Image saved to {image_path}")

            return base64.b64encode(image_bytes).decode("utf-8")
        else:
            print(f"Error generating image: {response.text}")
            return None
