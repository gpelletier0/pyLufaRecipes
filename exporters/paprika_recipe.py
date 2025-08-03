import gzip
import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional

from models.lufa_recipe import LufaRecipe
from services.image_generator import ImageGeneratorService


@dataclass
class PaprikaRecipe:
    name: str
    ingredients: str
    directions: str
    uid: Optional[str] = None
    hash: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    nutritional_info: Optional[str] = None
    prep_time: Optional[str] = None
    cook_time: Optional[str] = None
    total_time: Optional[str] = None
    difficulty: Optional[str] = None
    servings: Optional[str] = None
    rating: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    photo: Optional[str] = None
    photo_hash: Optional[str] = None
    image_url: Optional[str] = None
    categories: Optional[List[str]] = None
    photo_data: Optional[str] = None
    photos: Optional[List[str]] = None
    photo_large: Optional[str] = None
    created: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    FILE_EXTENSION = ".paprikarecipe"

    @classmethod
    def from_lufa_recipe(cls, lufa_recipe: LufaRecipe, image_generator: Optional[ImageGeneratorService] = None) -> 'PaprikaRecipe':
        photo_data = None

        if image_generator:
            photo_data = image_generator.generate_recipe_image(lufa_recipe.name)

        return cls(
            name=lufa_recipe.name,
            ingredients=lufa_recipe.ingredients,
            directions=lufa_recipe.instructions,
            notes=lufa_recipe.tip,
            nutritional_info=f"Calories per serving: {lufa_recipe.calories_per_serving}",
            prep_time=lufa_recipe.preparation_time,
            servings=lufa_recipe.servings,
            source=lufa_recipe.source,
            source_url=lufa_recipe.source,
            categories=lufa_recipe.categories,
            photo_data=photo_data
        )

    def save_to_file(self, output_path: str) -> None:
        full_path = f"{output_path}{self.FILE_EXTENSION}"
        internal_filename = os.path.basename(full_path)
        json_data = json.dumps(self.to_dict()).encode('utf-8')

        try:
            with open(full_path, 'wb') as f_out:
                with gzip.GzipFile(filename=internal_filename, mode='wb', fileobj=f_out) as gz_out:
                    gz_out.write(json_data)
        except Exception as e:
            raise IOError(f"Failed to save Paprika recipe to {full_path}: {e}") from e

    def to_dict(self) -> dict:
        return asdict(self)

    def __str__(self) -> str:
        return f"PaprikaRecipe(name='{self.name}')"

    def __repr__(self) -> str:
        return self.__str__()
