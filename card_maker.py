#!/usr/bin/env python3
import argparse
import cairosvg
import json
import os
import random
import svgwrite

def generate_card(buzzwords, card_id, height, width, free_space=True, cell_width=200, cell_height=150):
    # Calculate the number of buzzwords needed.
    # If free_space is enabled and the grid has a center cell, subtract one.
    if free_space and height % 2 == 1 and width % 2 == 1:
        required_buzzwords = height * width - 1
    else:
        required_buzzwords = height * width

    if len(buzzwords) < required_buzzwords:
        print(f'Error: Not enough buzzwords to generate a card of this size. Needed {required_buzzwords}, got {len(buzzwords)}.')
        print('Please add more buzzwords to the buzzwords.json file, consider adding more categories, or reduce the size of the card.')
        exit(1)

    # Randomly sample the buzzwords needed.
    random_buzzwords = random.sample(buzzwords, required_buzzwords)

    # Create the SVG drawing with validation disabled.
    total_width = width * cell_width
    total_height = height * cell_height
    svg_filename = f'bingo_card_{card_id}.svg'
    png_filename = f'bingo_card_{card_id}.png'
    dwg = svgwrite.Drawing(svg_filename, size=(total_width, total_height), profile='tiny', debug=False)

    # Draw the outer rectangle (optional)
    dwg.add(dwg.rect(insert=(0, 0), size=(total_width, total_height),
                     fill='white', stroke='black'))

    word_index = 0
    for i in range(height):
        for j in range(width):
            x = j * cell_width
            y = i * cell_height
            # Draw the cell rectangle.
            dwg.add(dwg.rect(insert=(x, y), size=(cell_width, cell_height),
                             fill='white', stroke='black'))
            # If free_space is enabled and this is the center cell, label it as "FREE".
            if free_space and i == height // 2 and j == width // 2:
                text_value = "FREE"
            else:
                text_value = random_buzzwords[word_index]
                word_index += 1
            # Add the text to the cell.
            dwg.add(dwg.text(text_value,
                             insert=(x + cell_width / 2, y + cell_height / 2),
                             text_anchor="middle",
                             dominant_baseline="middle",
                             font_family="Arial",
                             font_size="14px",
                             fill="black"))
    dwg.save()

    # Convert the SVG to PNG
    cairosvg.svg2png(url=svg_filename, write_to=png_filename)
    # Remove the SVG file
    os.remove(svg_filename)

if __name__ == "__main__":
    # Initialize argument parser
    parser = argparse.ArgumentParser(description='Generate a bingo card with buzzwords.')
    parser.add_argument('--height', type=int, default=5, help='Height of the bingo card')
    parser.add_argument('--width', type=int, default=5, help='Width of the bingo card')
    parser.add_argument('--free_space', action='store_true', help='Include a free space in the center of the card')
    parser.add_argument('--cell_width', type=int, default=200, help='Width of each cell in the bingo card')
    parser.add_argument('--cell_height', type=int, default=150, help='Height of each cell in the bingo card')
    parser.add_argument('--buzzwords_file', type=str, default='buzzwords.json', help='Path to the buzzwords JSON file')
    parser.add_argument('--categories', type=str, nargs='+', help='Categories to include in the bingo card')
    parser.add_argument('--list_categories', action='store_true', help='List available categories and exit')
    parser.add_argument('--quantity', type=int, default=1, help='Number of bingo cards to generate')
    # Parse arguments
    args = parser.parse_args()
    # Load buzzwords from a JSON file named 'buzzwords.json'
    with open(args.buzzwords_file, 'r') as f:
        buzzwords = json.load(f)
    # List available categories and exit if requested
    available_categories = buzzwords.keys()
    if args.list_categories:
        print('Available categories:')
        for category in available_categories:
            print(f'  - {category}')
            exit(0)
    elif args.categories:
        # Fail if any requested category is not available and show available categories
        for category in args.categories:
            if category not in available_categories:
                print(f'Error: Category "{category}" not found. Available categories are:')
                for category in available_categories:
                    print(f'  - {category}')
                exit(1)
        buzzwords = [buzzword for category in args.categories for buzzword in buzzwords[category]]
       
    else:
        # Use all categories if none are specified
        buzzwords = [buzzword for category in available_categories for buzzword in buzzwords[category]]
    
    # Convert buzzwords to a list
    buzzwords = list(buzzwords)
    
    # Generate a 5x5 bingo card with larger dimensions
    for i in range(args.quantity):
        generate_card(buzzwords, i, args.height, args.width, args.free_space, args.cell_width, args.cell_height)

