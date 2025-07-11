import gzip
import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional
from lufa import LufaRecipe


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

    __paprika_file_extension = ".paprikarecipe"

    @classmethod
    def from_lufa_recipe(cls, lufa_recipe: LufaRecipe) -> 'PaprikaRecipe':
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
        )

    def to_dict(self) -> dict:
        return asdict(self)

    def to_paprika_file(self, output_path: Optional[str] = None):
        internal_filename = os.path.basename(output_path)
        json_data = json.dumps(self.to_dict()).encode('utf-8')

        with open(output_path + self.__paprika_file_extension, 'wb') as f_out:
            with gzip.GzipFile(filename=internal_filename, mode='wb', fileobj=f_out) as gz_out:
                gz_out.write(json_data)
