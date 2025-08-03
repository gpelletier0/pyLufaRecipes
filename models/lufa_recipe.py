from dataclasses import dataclass, field
from typing import List


@dataclass
class LufaRecipe:
    name: str
    meal_type: str
    preparation_time: str
    servings: str
    calories_per_serving: str
    cost_per_serving: str
    ingredients: str
    instructions: str
    tip: str
    categories: List[str] = field(default_factory=lambda: ["Lufa"])
    source: str = "Lufa.com"

    @classmethod
    def from_string(cls, recipe_text: str) -> 'LufaRecipe':
        try:
            header, rest = recipe_text.split("Ingredients\nQuantity", 1)
            header_lines = header.strip().split("\n")
            ingredients_section, rest = rest.split("Cooking Instructions:", 1)
            instructions_section, tip_section = rest.split("Tip!:", 1)
        except ValueError as e:
            raise ValueError(f"Invalid recipe format: {e}\n" f"Recipe preview: {recipe_text[:200]}...") from e

        return cls(
            name=header_lines[0],
            meal_type=header_lines[1].strip(),
            preparation_time=cls._extract_field_value(header_lines[2]),
            servings=cls._extract_field_value(header_lines[3]),
            calories_per_serving=cls._extract_field_value(header_lines[4]),
            cost_per_serving=cls._extract_field_value(header_lines[5]),
            ingredients=cls._parse_ingredients(ingredients_section),
            instructions=instructions_section.strip(),
            tip=f"Tip!: {tip_section.strip()}"
        )

    @staticmethod
    def _extract_field_value(line: str) -> str:
        parts = line.split(":", 1)
        return parts[1].strip() if len(parts) > 1 else ""

    @staticmethod
    def _parse_ingredients(ingredients_block: str) -> str:
        lines = [line.strip() for line in ingredients_block.strip().splitlines() if line.strip()]
        ingredients = []

        for i in range(0, len(lines), 2):
            if i + 1 < len(lines):
                ingredient_name = lines[i]
                quantity = lines[i + 1]
                ingredients.append(f"{quantity} {ingredient_name}")

        return "\n".join(ingredients)

    def __str__(self) -> str:
        return f"LufaRecipe(name='{self.name}', meal_type='{self.meal_type}')"

    def __repr__(self) -> str:
        return self.__str__()
