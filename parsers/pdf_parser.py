import re
from typing import List, Optional
import fitz

from models.lufa_recipe import LufaRecipe


class LufaPdfParser:
    MEAL_PLAN_SEPARATOR = re.compile(r'Meal Plan for the Week\s+')
    RECIPE_TITLE_PATTERN = re.compile(r"Lunch|Dinner")

    def __init__(self):
        pass

    def extract_recipes(self, pdf_path: str) -> List[LufaRecipe]:
        try:
            text = self._extract_text_from_pdf(pdf_path)
            recipe_sections = self._split_into_recipe_sections(text)

            if not recipe_sections:
                raise ValueError("No recipe sections found in PDF")

            recipes = []
            for section in recipe_sections:
                try:
                    recipe = LufaRecipe.from_string(section)
                    recipes.append(recipe)
                except ValueError as e:
                    print(f"Warning: Failed to parse recipe section: {e}")
                    continue

            return recipes

        except FileNotFoundError:
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        except Exception as e:
            raise ValueError(f"Failed to parse PDF {pdf_path}: {e}") from e

    @staticmethod
    def _extract_text_from_pdf(file_path: str) -> str:
        with fitz.open(file_path) as doc:
            return "\n".join(page.get_text() for page in doc)

    def _split_into_recipe_sections(self, text: str) -> List[str]:
        recipe_sections = []

        for section in self.MEAL_PLAN_SEPARATOR.split(text):
            if not section.strip():
                continue

            cleaned_recipe = self._extract_recipe_content(section)
            if cleaned_recipe:
                recipe_sections.append(cleaned_recipe)

        return recipe_sections

    def _extract_recipe_content(self, section_text: str) -> Optional[str]:
        lines = section_text.splitlines()

        for i, line in enumerate(lines):
            if self.RECIPE_TITLE_PATTERN.search(line):
                recipe_lines = lines[i - 1:]
                return "\n".join(recipe_lines)

        return None
