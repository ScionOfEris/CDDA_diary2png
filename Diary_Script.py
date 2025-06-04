#!/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import argparse
import textwrap
import re
import sys

parser = argparse.ArgumentParser(description="Protect VMs with Recoverpoint")


parser.add_argument(
    "--background",
    metavar="Background Color",
    type=str,
    help="Background color of the image",
    default="black",
    required=False,
)
parser.add_argument(
    "--text_color",
    metavar="Text Color",
    type=str,
    help="Color of the text in the image",
    default="green",
    required=False,
)
parser.add_argument(
    "--size",
    metavar="Font Size",
    type=int,
    help="Font size of the text in the image",
    default=30,
    required=False,
)
parser.add_argument(
    "--height",
    metavar="Height",
    type=int,
    help="Height of the image in pixels",
    default="4800",
    required=False,
)
parser.add_argument(
    "--width",
    metavar="Width",
    type=int,
    help="Width of the image in pixels",
    default="800",
    required=False,
)

parser.add_argument(
    "diary",
    type=str,
    metavar="Diary File",
    help="Diary file to convert to PNG images",
)

args = parser.parse_args()

# Load your text file
with open(args.diary, "r", encoding="utf-8") as f:
    content = f.read()

# first dos2unix the file
content = content.replace("\r\n", "\n")  # Normalize line endings

entries = re.split(r"\n\nEntry:", content)  # Split entries
entries = [e.strip() for e in entries if e.strip()]  # Clean empty entries


def create_image(entry_text, entry_num):
    """Generates an image from entry text."""
    img_width, img_height = args.width, args.height
    background_color = args.background
    text_color = args.text_color
    img = Image.new("RGB", (img_width, img_height), background_color)
    draw = ImageDraw.Draw(img)

    font = ImageFont.load_default(size=args.size)  # You can use a custom font
    #fontsize = 20
    #font = ImageFont.truetype("arial.ttf", fontsize)  # Load a TTF font

    #wrapped_text = textwrap.fill(entry_text, width=52)  # Wrap text for readability
    wrapped_text = entry_text
    draw.text((20, 20), wrapped_text, fill=text_color, font=font, )

    img.save(f"Entry_{entry_num}.png")

SECTION_HEADERS = {
    "Stats:", "Skills:", "Proficiencies:", "Mutations:", "New missions:",
    "Active missions:", "New completed missions:", "Kills:", "NPC Killed:",
    "New Bionics:", "Gained Mutation:", "Lost Mutation:"
}

for i, entry in enumerate(entries, start=1):
    parts = re.split(r'\n\s*\n', entry)
    if not parts:
        continue

    date_line = parts[0]
    diary_blocks = []
    sections = []
    in_diary = False

    # Start after the entry line
    idx = 1
    # Skip all leading section headers
    while idx < len(parts):
        part_stripped = parts[idx].strip()
        if any(part_stripped.startswith(h) for h in SECTION_HEADERS):
            idx += 1
        else:
            break

    # Collect diary blocks until a section header is found
    while idx < len(parts):
        part_stripped = parts[idx].strip()
        if any(part_stripped.startswith(h) for h in SECTION_HEADERS):
            break
        diary_blocks.append(parts[idx])
        idx += 1

    # The rest are sections
    sections = parts[idx:]

    diary = "\n\n".join(diary_blocks).strip()
    #structured_text = f"{date_line}\n\n{diary}\n\n" + "\n\n".join(sections)
    structured_text = f"{date_line}\n\n{diary}"
    create_image(structured_text, i)

print("PNG files created successfully!")

