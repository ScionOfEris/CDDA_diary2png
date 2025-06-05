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
    help="Maximum height of the image in pixels",
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
parser.add_argument(
    "--diary_id",
    type=str,
    metavar="Diary ID String",
    help="String to identify the diary entry's start",
    default="Diary:",
    required=False,
)
parser.add_argument(
    "--max_line_length",
    type=int,
    metavar="Max Line Length",
    help="Maximum line length for text wrapping",
    default=52,
    required=False,
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
    img_width = args.width

    # Calculate height based on the number of lines in the text
    lines = entry_text.splitlines()
    line_height = args.size + 5  # Add some padding for line height
    img_height = args.height if args.height else line_height * len(lines) + 10  # Add padding

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


for i, entry in enumerate(entries, start=1):
    date_line, *rest = re.split(r'\n\s*\n', entry, maxsplit=1)
    diary_id = args.diary_id

    # Find the diary_id tag in the entry
    diary_id_idx = entry.find(diary_id)
    if diary_id_idx == -1:
        # If diary_id not found, fallback to original logic or skip
        continue

    # Everything after diary_id is the diary text
    diary_text = entry[diary_id_idx + len(diary_id):].strip()

    # Everything between date_line and diary_id
    between = entry[len(date_line):diary_id_idx].strip()

    # Compose structured_text: date_line, then diary_text, then between
    structured_text = f"{date_line}\n\n{diary_text}"
    if between:
        structured_text += f"\n\n{between}"

    # Cut any line that is over max_line_length into multiple lines, breaking at whitespace
    max_len = args.max_line_length
    wrapped_lines = []
    for line in structured_text.splitlines():
        while len(line) > max_len:
            # Find the last whitespace before max_len
            break_idx = line.rfind(' ', 0, max_len)
            if break_idx == -1:
                break_idx = max_len  # No whitespace found, hard break
            wrapped_lines.append(line[:break_idx].rstrip())
            line = line[break_idx:].lstrip()
        wrapped_lines.append(line)
    structured_text = "\n".join(wrapped_lines)

    create_image(structured_text, i)

print("PNG files created successfully!")

