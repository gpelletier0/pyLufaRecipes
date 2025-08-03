# Lufa.com Generated Recipe PDF Parser

This project is designed to extract recipe details from lufa.com generated meal plan PDF files. It parses the text to identify individual recipes and their components, then saves the structured data in either JSON format or Paprika Recipe Manager format.

## Features

- Extracts multiple recipes from a single PDF document.
- Parses various recipe attributes including:
    - Name
    - Meal Type
    - Preparation Time
    - Servings
    - Calories & Cost per Serving
    - Ingredients
    - Cooking Instructions
    - Tips
- Support for multiple output formats:
    - JSON format for easy data exchange
    - Paprika Recipe Manager format (.paprikarecipe) for direct import
- Generates recipe images using AI for visual representation in Paprika
- Automatically names the output file based on an identifier from the PDF's filename.

## Requirements

- Python 3.13+
- PyMuPDF (for PDF parsing)
- huggingface-hub (for recipe image generation)

## Installation

**Clone the repository**

**Install the required dependencies:**
```
pip install -r requirements.txt
```

**Set up environment variables for image generation (optional):**

If you want to use the image generation feature, you'll need to set up an API key:
```
export STABLE_DIFFUSION_API_KEY=your_api_key_here
```

## Usage

To run the script, execute the main script from your terminal and provide the path to the meal plan PDF file:

```
python pylufarecipes.py path/to/your/meal_plan.pdf
```


### Command Line Options

- `pdf_path`: Path to the PDF file to process (required positional argument)

- `--format`, `-f`: Specify the output format
  - Choices: `json`, `paprika`
  - Default: `paprika`
  ```
  python pylufarecipes.py meal_plan.pdf --format json
  ```

- `--output-dir`, `-o`: Output directory for generated files
  - Default: `./recipes`
  ```
  python pylufarecipes.py meal_plan.pdf --output-dir ./my_recipes
  ```

- `--no-images`: Skip image generation for recipes
  - Only affects Paprika format output
  ```
  python pylufarecipes.py meal_plan.pdf --no-images
  ```

- `--verbose`, `-v`: Enable verbose output
  - Shows detailed processing information
  ```
  python pylufarecipes.py meal_plan.pdf --verbose
  ```

- `--version`: Show program version and exit
  ```
  python pylufarecipes.py --version
  ```
  
### Output

- **JSON format**: Creates a single JSON file with all extracted recipes
- **Paprika format**: Creates individual .paprikarecipe files in the 'recipes' directory

Generated recipe images (when using Paprika format) are embedded directly in the .paprikarecipe files.

## Project Structure

- `pylufarecipes.py`: Main entry point for the application
- `cli/`: Command-line interface components
  - `recipe_parser_cli.py`: CLI argument parsing and handling
- `models/`: Data models for recipe representation
  - `lufa_recipe.py`: Contains the `LufaRecipe` class for parsing Lufa recipe data
- `parsers/`: PDF parsing functionality
  - `pdf_parser.py`: PDF text extraction and parsing logic
- `services/`: Business logic and services
  - `image_generator.py`: Handles AI-based recipe image generation
- `exporters/`: Output format handlers
  - `paprika_recipe.py`: Contains the `PaprikaRecipe` class for creating Paprika-compatible recipe files
- `requirements.txt`: Lists all required Python dependencies
