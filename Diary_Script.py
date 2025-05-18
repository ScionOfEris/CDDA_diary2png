#!/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import textwrap
import re

# Load your text file
with open("Chau_Hutsons_diary.txt", "r", encoding="utf-8") as f:
    content = f.read()

entries = re.split(r"\n\nEntry:", content)  # Split entries
entries = [e.strip() for e in entries if e.strip()]  # Clean empty entries

def extract_diary(entry_text):
    """Extracts the diary section from the entry."""
    parts = entry_text.split("\n\n")
    
    # Find the 'Kills' section index
    kills_index = next((i for i, part in enumerate(parts) if part.strip().startswith("Kills:")), None)

    if kills_index is not None:
        diary_text = "\n\n".join(parts[kills_index + 1:])  # Everything after 'Kills'
        non_diary_text = "\n\n".join(parts[:kills_index + 1])  # Everything before 'Kills'
    else:
        diary_text = "\n\n".join(parts)
        non_diary_text = ""

    return diary_text.strip(), non_diary_text.strip()

def create_image(entry_text, entry_num):
    """Generates an image from entry text."""
    img_width, img_height = 800, 1200
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    
    img = Image.new("RGB", (img_width, img_height), background_color)
    draw = ImageDraw.Draw(img)

    font = ImageFont.load_default()  # You can use a custom font

    wrapped_text = textwrap.fill(entry_text, width=80)  # Wrap text for readability
    draw.text((20, 20), wrapped_text, fill=text_color, font=font)

    img.save(f"Entry_{entry_num}.png")

# Process each entry
for i, entry in enumerate(entries, start=1):
    parts = entry.split("\n\n")
    date_line = parts[0].split(",")[0].strip()
    
    diary_text, non_diary_text = extract_diary(entry)
    
    structured_text = f"{date_line}\n\n{diary_text}\n\n{non_diary_text}"
    create_image(structured_text, i)

print("PNG files created successfully!")

