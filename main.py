import json
import os
import re
import fitz
import argparse
from dataclasses import asdict
from datetime import datetime
from typing import List
from image_generation import RecipeImageGenerator
from lufa import LufaRecipe
from paprika import PaprikaRecipe

_MEAL_PLAN_SEPARATOR = re.compile(r'Meal Plan for the Week\s+')
_RECIPE_TITLE_PATTERN = re.compile(r"\*\*\s\d")


def extract_order_identifier_filename(pdf_path: str) -> str:
    match = re.search(r'\d+', pdf_path)
    order_identifier = match.group(0) if match else datetime.now().strftime("%Y%m%d")

    return order_identifier


def extract_recipes_from_pdf(file_path: str) -> List[LufaRecipe]:
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


def dump_all_recipes_to_paprika_file(all_recipes):
    output_dir = "recipes"
    generator = RecipeImageGenerator()

    os.makedirs(output_dir, exist_ok=True)

    for lufa_recipe in all_recipes:
        paprika_recipe = PaprikaRecipe.from_lufa_recipe(lufa_recipe, generator)

        safe_name = paprika_recipe.name.replace('/', '_').replace('\\', '_').replace(':', '_')
        output_path = os.path.join(output_dir, safe_name)

        paprika_recipe.to_paprika_file(output_path)

    print(f"✅ Extracted {len(all_recipes)} recipes to Paprika format files in 'recipes' directory")


def main():
    parser = argparse.ArgumentParser(description="Process Lufa meal plan PDF and extract recipes")
    parser.add_argument("pdf_path", nargs="?", default="Meal-Plan-Order-23135319.pdf", help="Path to the PDF file")
    parser.add_argument("--format", "-f", choices=["json", "paprika"], default="paprika", help="Output format (default: paprika)")
    args = parser.parse_args()
    pdf_path = args.pdf_path

    try:
        all_recipes = extract_recipes_from_pdf(pdf_path)
        if not all_recipes:
            print("No recipes were found in the document.")
            return

        if args.format == "json":
            order_identifier = extract_order_identifier_filename(pdf_path)
            output_filename = f"meal_plan_recipes-{order_identifier}.json"
            dump_all_recipes_to_json(all_recipes, output_filename)
        else:
            dump_all_recipes_to_paprika_file(all_recipes)

    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
