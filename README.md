# Lufa.com Generated Recipe PDF Parser

This project is designed to extract recipe details from lufa.com generated meal plan PDF files. It parses the text to identify individual recipes and their components, then saves the structured data into a JSON file.

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
- Saves the extracted recipes in a clean, easy-to-read JSON format.
- Automatically names the output file based on an identifier from the PDF's filename.

## Requirements

- Python 3.6+
- PyMuPDF

## Installation

**Clone the repository**

**Install the required dependencies:**
    ```
    pip install PyMuPDF
    ```

## Usage

To run the script, execute the main script from your terminal and provide the path to the meal plan PDF file.
