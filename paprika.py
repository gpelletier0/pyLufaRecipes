from dataclasses import dataclass, field, asdict
from datetime import datetime
from lufa import LufaRecipe
from typing import List, Optional


@dataclass
class PaprikaRecipe:
    uid: str
    hash: str
    name: str
    description: str
    ingredients: str
    directions: str
    notes: str
    nutritional_info: str
    prep_time: str
    cook_time: str
    total_time: str
    difficulty: str
    servings: str
    rating: int
    source: str
    source_url: str
    photo: str
    photo_hash: str
    image_url: str
    categories: List[str]
    photo_data: str
    photos: List[str]
    created: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    photo_large: Optional[str] = None

    @classmethod
    def from_lufa_recipe(cls, lufa_recipe: LufaRecipe) -> 'PaprikaRecipe':
        return cls(
            name=lufa_recipe.name,
            prep_time=lufa_recipe.preparation_time,
            servings=lufa_recipe.servings,
            ingredients=lufa_recipe.ingredients,
            directions=lufa_recipe.instructions,
            notes=lufa_recipe.tip,
            nutritional_info=f"Calories per serving: {lufa_recipe.calories_per_serving}",
            categories=lufa_recipe.categories,
            source=lufa_recipe.source,
        )

    @classmethod
    def to_dict(cls, self) -> dict:
        return asdict(self)
