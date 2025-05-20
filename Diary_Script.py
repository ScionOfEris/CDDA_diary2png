#!/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import textwrap
import re
import sys

# Load your text file
with open("Chau_Hutsons_diary.txt", "r", encoding="utf-8") as f:
    content = f.read()

# first dos2unix the file
content = content.replace("\r\n", "\n")  # Normalize line endings

entries = re.split(r"\n\nEntry:", content)  # Split entries
entries = [e.strip() for e in entries if e.strip()]  # Clean empty entries


def create_image(entry_text, entry_num):
    """Generates an image from entry text."""
    img_width, img_height = 800, 1200
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    
    img = Image.new("RGB", (img_width, img_height), background_color)
    draw = ImageDraw.Draw(img)

    font = ImageFont.load_default()  # You can use a custom font
    #fontsize = 20
    #font = ImageFont.truetype("arial.ttf", fontsize)  # Load a TTF font

    #wrapped_text = textwrap.fill(entry_text, width=80)  # Wrap text for readability
    wrapped_text = entry_text
    draw.text((20, 20), wrapped_text, fill=text_color, font=font)

    img.save(f"Entry_{entry_num}.png")

# Process each entry
for i, entry in enumerate(entries, start=1):

    parts = entry.split("\n\n")
    parts = re.split(r'\n\s*\n', entry)  # Split by double newlines
    date_line_parts = parts[0].split(',',4)
    if len(date_line_parts) > 4:
        date_line = ','.join(date_line_parts[:4]) + ',\n' + date_line_parts[4]
    else:
        date_line = ','.join(date_line_parts)
    
    header = ''
    diary = ''

    # go through each part until you find one that does not start with text followed by a colon
    # and a newline
    for part in parts[1:]:
        if re.match(r"^[A-Z a-z]+:", part):
            header += part + "\n\n"
        else:
            diary += part + "\n\n"

    structured_text = f"{date_line}\n\n{diary}\n\n{header}"
    #print(structured_text)

    create_image(structured_text, i)

print("PNG files created successfully!")

