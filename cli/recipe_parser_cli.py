import argparse
import datetime
import json
import os
import sys
from typing import List, Optional
from datetime import datetime

from models.lufa_recipe import LufaRecipe
from exporters.paprika_recipe import PaprikaRecipe
from parsers.pdf_parser import LufaPdfParser
from services.image_generator import ImageGeneratorService


class RecipeParserCLI:
    DEBUG_DEFAULT_PDF = ""
    DEBUG_MODE = False

    def __init__(self):
        self.parser = LufaPdfParser()
        self.image_generator = None

    @staticmethod
    def setup_argument_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Extract recipes from Lufa meal plan PDF files",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s meal_plan.pdf
  %(prog)s meal_plan.pdf --format json
  %(prog)s meal_plan.pdf --format paprika --output-dir ./my_recipes
  %(prog)s meal_plan.pdf --no-images
            """
        )

        parser.add_argument(
            "pdf_path",
            nargs="?" if RecipeParserCLI.DEBUG_MODE else None,
            default=RecipeParserCLI.DEBUG_DEFAULT_PDF if RecipeParserCLI.DEBUG_MODE else None,
            help=(f"Path to the PDF file to process (default: {RecipeParserCLI.DEBUG_DEFAULT_PDF})" if RecipeParserCLI.DEBUG_MODE else "")
        )

        parser.add_argument(
            "--format", "-f",
            choices=["json", "paprika"],
            default="paprika",
            help="Output format (default: paprika)"
        )

        parser.add_argument(
            "--output-dir", "-o",
            default="./recipes",
            help="Output directory for generated files (default: ./recipes)"
        )

        parser.add_argument(
            "--no-images",
            action="store_true",
            help="Skip image generation for recipes"
        )

        parser.add_argument(
            "--verbose", "-v",
            action="store_true",
            default=RecipeParserCLI.DEBUG_MODE,
            help="Enable verbose output" + (" (default in debug mode)" if RecipeParserCLI.DEBUG_MODE else "")
        )

        parser.add_argument("--version", action="version", version="Lufa Recipe Parser 1.0.0")

        return parser

    def initialize_image_generator(self, enable_images: bool) -> None:
        if enable_images:
            api_key = os.environ.get("STABLE_DIFFUSION_API_KEY")
            if api_key:
                self.image_generator = ImageGeneratorService(api_key=api_key)
                print("[✓] Image generation enabled")
            else:
                print("[!] Warning: STABLE_DIFFUSION_API_KEY not found. Images will not be generated.")
        else:
            print("[✓] Image generation disabled")

    def extract_recipes(self, pdf_path: str, verbose: bool = False) -> List[LufaRecipe]:
        try:
            if verbose:
                print(f"Processing PDF: {pdf_path}")

                if self.DEBUG_MODE:
                    print(f"[-] Debug mode enabled - using default file: {pdf_path}")

            recipes = self.parser.extract_recipes(pdf_path)

            if not recipes:
                print("[X] No recipes were found in the document.")
                sys.exit(1)

            if verbose:
                print(f"[✓] Successfully extracted {len(recipes)} recipes")
                for i, recipe in enumerate(recipes, 1):
                    print(f"  {i}. {recipe.name} ({recipe.meal_type})")

            return recipes

        except FileNotFoundError:
            print(f"[X] Error: The file '{pdf_path}' was not found.")
            sys.exit(1)
        except ValueError as e:
            print(f"[X] Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"[X] An unexpected error occurred: {e}")
            if verbose:
                import traceback
                traceback.print_exc()

            sys.exit(1)

    @staticmethod
    def export_to_json(recipes: List[LufaRecipe], output_dir: str) -> None:
        try:
            os.makedirs(output_dir, exist_ok=True)

            filename = f"meal_plan_recipes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            output_path = os.path.join(output_dir, filename)
            recipes_data = [recipe.__dict__ for recipe in recipes]

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(recipes_data, f, indent=2, ensure_ascii=False)

            print(f"[✓] Exported {len(recipes)} recipes to JSON: {output_path}")

        except Exception as e:
            print(f"Failed to export to JSON: {e}")
            sys.exit(1)

    def export_to_paprika(self, recipes: List[LufaRecipe], output_dir: str, verbose: bool = False) -> None:
        try:
            os.makedirs(output_dir, exist_ok=True)

            exported_count = 0
            for recipe in recipes:
                if verbose:
                    print(f"Processing: {recipe.name}")

                paprika_recipe = PaprikaRecipe.from_lufa_recipe(recipe, self.image_generator)
                output_path = os.path.join(output_dir, recipe.name)
                paprika_recipe.save_to_file(output_path)
                exported_count += 1

                if verbose:
                    print(f"\t[✓] Saved: {recipe.name}.paprikarecipe")

            print(f"[✓] Exported {exported_count} recipes to Paprika format in: {output_dir}")

        except Exception as e:
            print(f"[X] Failed to export to Paprika format: {e}")
            sys.exit(1)

    def run(self, test_args: Optional[List[str]] = None) -> None:
        arg_parser = self.setup_argument_parser()

        if test_args is not None:
            args = arg_parser.parse_args(test_args)
        else:
            args = arg_parser.parse_args()

        if self.DEBUG_MODE and args.verbose:
            print("-" * 50)
            print(f"[-] Debug mode active")
            print(f"[-] PDF path: {args.pdf_path}")
            print(f"[-] Format: {args.format}")
            print(f"[-] Output dir: {args.output_dir}")
            print(f"[-] No images: {args.no_images}")
            print("-" * 50)

        if not os.path.isfile(args.pdf_path):
            print(f"[X] Error: PDF file '{args.pdf_path}' does not exist.")
            if self.DEBUG_MODE:
                print(f"[-] Debug tip: Update DEBUG_DEFAULT_PDF to point to an existing file")
            sys.exit(1)

        self.initialize_image_generator(not args.no_images and args.format == "paprika")

        recipes = self.extract_recipes(args.pdf_path, args.verbose)

        if args.format == "json":
            self.export_to_json(recipes, args.output_dir)
        else:
            self.export_to_paprika(recipes, args.output_dir, args.verbose)

        print("Recipe extraction completed successfully!")
