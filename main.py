import json
import re
import sys
import fitz
from dataclasses import asdict
from datetime import datetime
from typing import List
from lufa import LufaRecipe

_MEAL_PLAN_SEPARATOR = re.compile(r'Meal Plan for the Week\s+')
_RECIPE_TITLE_PATTERN = re.compile(r"\*\*\s\d")


def extract_order_identifier_filename(pdf_path: str) -> str:
    match = re.search(r'\d+', pdf_path)
    order_identifier = match.group(0) if match else datetime.now().strftime("%Y%m%d")

    return order_identifier


def extract_recipes_from_pdf(file_path: str) -> List[LufaRecipe]:
    """Extracts recipe data from a given PDF file."""
    text = _extract_text_from_pdf(file_path)
    recipe_sections = _split_into_recipe_sections(text)

    return [LufaRecipe.from_string(section) for section in recipe_sections]


def _extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    return "\n".join(page.get_text() for page in doc)


def _split_into_recipe_sections(text: str) -> List[str]:
    recipe_contents = []
    for section in _MEAL_PLAN_SEPARATOR.split(text):
        if not section.strip():
            continue

        lines = section.splitlines()
        for i, line in enumerate(lines):
            if _RECIPE_TITLE_PATTERN.search(line):
                recipe_contents.append("\n".join(lines[i:]))
                break
    return recipe_contents


def dump_all_recipes_to_json(all_recipes: list[LufaRecipe], output_filename: str):
    recipes_dict = [asdict(recipe) for recipe in all_recipes]

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(recipes_dict, f, indent=2, ensure_ascii=False)

    print(f"✅ Extracted {len(all_recipes)} recipes to '{output_filename}'")


def main():
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = "Meal-Plan-Order-23135319.pdf"

    order_identifier = extract_order_identifier_filename(pdf_path)
    output_filename = f"meal_plan_recipes-{order_identifier}.json"

    try:
        all_recipes = extract_recipes_from_pdf(pdf_path)
        if not all_recipes:
            print("No recipes were found in the document.")
            return

        dump_all_recipes_to_json(all_recipes, output_filename)

    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()