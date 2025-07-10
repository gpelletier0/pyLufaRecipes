from dataclasses import dataclass


@dataclass
class Recipe:
    name: str
    meal_type: str
    preparation_time: str
    servings: str
    calories_per_serving: str
    cost_per_serving: str
    ingredients: str
    instructions: str
    tip: str

    @classmethod
    def from_text_section(cls, section: str) -> 'Recipe':
        try:
            header, rest = section.split("Ingredients\nQuantity", 1)
            header_lines = header.strip().split("\n")
            ingredients_lines, rest = rest.split("Cooking Instructions:", 1)
            instructions_lines, tip_part = rest.split("Tip!:", 1)
        except ValueError as e:
            raise ValueError(f"Invalid recipe section format: {e}\nSection: {section[:200]}...") from e

        def _get_value(line: str) -> str:
            parts = line.split(":", 1)
            return parts[1].strip() if len(parts) > 1 else ""

        return cls(
            name=header_lines[0].split("** ")[0],
            meal_type=header_lines[1].strip(),
            preparation_time=_get_value(header_lines[2]),
            servings=_get_value(header_lines[3]),
            calories_per_serving=_get_value(header_lines[4]),
            cost_per_serving=_get_value(header_lines[5]),
            ingredients=cls._parse_ingredients(ingredients_lines),
            instructions=instructions_lines.strip(),
            tip=f"Tip!: {tip_part.strip()}"
        )

    @staticmethod
    def _parse_ingredients(ingredients_block: str) -> str:
        """Parses the ingredients block into a formatted string."""
        lines = [line for line in ingredients_block.strip().splitlines() if line.strip()]
        ingredients = []

        for i in range(0, len(lines), 2):
            if i + 1 < len(lines):
                ingredient_name = lines[i]
                quantity = lines[i + 1]
                ingredients.append(f"{quantity} {ingredient_name}")

        return "\n".join(ingredients)
