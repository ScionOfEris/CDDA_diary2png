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
    default=18,
    required=False,
)
parser.add_argument(
    "--height",
    metavar="Height",
    type=int,
    help="Maximum height of the image in pixels (this will cut of text if it exceeds this height)",
    required=False,
)
parser.add_argument(
    "--width",
    metavar="Width",
    type=int,
    help="Width of the image in pixels",
    default="1000",
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
    "--format_style",
    type=str,
    metavar="Format Style",
    help="Format style for the text (options: 'default', 'wrap_long_side', 'trunc_long_side')",
    default="default",
    choices=["default", "wrap_long_side", "trunc_long_side"],
    required=False, 
)
parser.add_argument(
    "--max_line_length",
    type=int,
    metavar="Max Line Length",
    help="Maximum line length for text wrapping (per side)",
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

# Function to wrap lines to max_line_length
def wrap_text(text, max_len):
    wrapped_lines = []
    for line in text.splitlines():
        while len(line) > max_len:
            break_idx = line.rfind(' ', 0, max_len)
            if break_idx == -1:
                break_idx = max_len  # No whitespace found, hard break
            wrapped_lines.append(line[:break_idx].rstrip())
            line = line[break_idx:].lstrip()
        wrapped_lines.append(line)
    return "\n".join(wrapped_lines)

def create_image(date_line, data_text, diary_text, entry_tag):
    """Generates an image with two columns: data (left), diary (right), and date_line on top."""
    img_width = args.width
    padding = 20
    col_gap = 20
    col_width = (img_width - 3 * padding) // 2

    font = ImageFont.load_default(size=args.size)
    line_height = args.size + 5

    # Split and count lines for each column
    data_lines = data_text.splitlines()
    diary_lines = diary_text.splitlines()
    num_lines = max(len(data_lines), len(diary_lines))

    # Calculate image height
    img_height = (num_lines + 3) * line_height + padding * 2  # +3 for date_line and spacing

    background_color = args.background
    text_color = args.text_color
    img = Image.new("RGB", (img_width, img_height), background_color)
    draw = ImageDraw.Draw(img)

    # Draw date_line at the top, centered
    date_y = padding
    date_x = img_width // 2 - draw.textlength(date_line, font=font) // 2
    draw.text((date_x, date_y), date_line, fill=text_color, font=font)

    # Draw data (left column)
    y = date_y + line_height * 2
    for line in data_lines:
        draw.text((padding, y), line, fill=text_color, font=font)
        y += line_height

    # Draw diary (right column)
    y = date_y + line_height * 2
    for line in diary_lines:
        draw.text((padding + col_width + col_gap, y), line, fill=text_color, font=font)
        y += line_height

    img.save(f"Entry_{entry_tag}.png")

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

    # Compose diary_structured_text: date_line, then diary_text
    #diary_structured_text = f"{date_line}\n\n{diary_text}"

    # Compose data_structured_text: date_line, then between
    #data_structured_text = f"{date_line}"
    #if between:
    #    data_structured_text += f"\n\n{between}"

    diary_structured_text = wrap_text(diary_text, args.max_line_length)
    data_structured_text = wrap_text(between, args.max_line_length)

    # for data, delete emtpy lines if the following line contains no colon
    # Remove superfluous blank lines from data_structured_text
    data_lines = data_structured_text.splitlines()
    cleaned_data_lines = []
    for idx, line in enumerate(data_lines):
        if line.strip() == "":
            # Check if next line exists and is a section header (ends with ':')
            if idx + 1 < len(data_lines) and data_lines[idx + 1].strip().endswith(":"):
                cleaned_data_lines.append(line)
            # Else, skip this blank line
        else:
            cleaned_data_lines.append(line)
    data_structured_text = "\n".join(cleaned_data_lines)

    # Apply format_style logic
    if args.format_style == "wrap_long_side":
        data_lines = data_structured_text.splitlines()
        diary_lines = diary_structured_text.splitlines()
        len_data = len(data_lines)
        len_diary = len(diary_lines)
        diff = abs(len_data - len_diary)
        if diff > 10:
            # Add 4 lines of padding and a continuation note to the short side
            pad_lines = [""] * 4 + ["(continued from other side)"]
            diff = diff - 5 # to account for the 4 padding lines and the continuation note
            if len_data < len_diary:
                data_lines += pad_lines
                # Move last X lines from diary to data
                x = diff // 2
                moved = diary_lines[-x:] if x > 0 else []
                data_lines += moved
                diary_lines = diary_lines[:-x] if x > 0 else diary_lines
            else:
                diary_lines += pad_lines
                # Move last X lines from data to diary
                x = diff // 2
                moved = data_lines[-x:] if x > 0 else []
                diary_lines += moved
                data_lines = data_lines[:-x] if x > 0 else data_lines
            # Re-join for image creation
            data_structured_text = "\n".join(data_lines)
            diary_structured_text = "\n".join(diary_lines)

    elif args.format_style == "trunc_long_side":
        data_lines = data_structured_text.splitlines()
        diary_lines = diary_structured_text.splitlines()
        len_data = len(data_lines)
        len_diary = len(diary_lines)
        diff = abs(len_data - len_diary)
        if len_data > len_diary:
            data_lines = data_lines[:len_diary]
            data_lines += ["(truncated)"]
        elif len_diary > len_data:
            diary_lines = diary_lines[:len_data]
            diary_lines += ["(truncated)"]
        data_structured_text = "\n".join(data_lines)
        diary_structured_text = "\n".join(diary_lines)

    #create_image(diary_structured_text, f"{i}_diary")
    #create_image(data_structured_text, f"{i}_stats")
    create_image(date_line, data_structured_text, diary_structured_text, f"{i}_combined")

print("PNG files created successfully!")

