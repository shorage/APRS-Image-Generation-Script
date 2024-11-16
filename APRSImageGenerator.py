import argparse
import os
import time
from PIL import Image, ImageDraw, ImageFont

# Constants for default behavior
DEFAULT_LOG_FILE = "/home/fcosta/digipi/direwolf.log"
DEFAULT_OUTPUT_IMAGE = "/tmp/direwatch.png"
DEFAULT_IMAGE_WIDTH = 320
DEFAULT_IMAGE_HEIGHT = 240
DEFAULT_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DEFAULT_BANNER_TITLE = "APRS BPQ"
DEFAULT_COLUMNS = ["source", "heard", "latitude", "longitude", "speed"]
DEFAULT_BANNER_BACKGROUND_COLOR = "navy"
DEFAULT_BANNER_TEXT_COLOR = "yellow"
DEFAULT_ROW_TEXT_COLOR = "white"
DEFAULT_ROW_COLORS = ["red", "green", "blue", "purple", "orange"]

def create_aprs_image(data, output_path, image_width, image_height, font_path, banner_title,
                      banner_background_color, banner_text_color, row_text_color, row_colors):
    """
    Create an image with APRS data.
    """
    # Create a blank image
    image = Image.new("RGB", (image_width, image_height), banner_background_color)
    draw = ImageDraw.Draw(image)

    # Load fonts
    font_title = ImageFont.truetype(font_path, size=int(image_height * 0.1))
    font_row = ImageFont.truetype(font_path, size=int(image_height * 0.07))

    # Draw the banner
    banner_height = int(image_height * 0.15)
    draw.rectangle([0, 0, image_width, banner_height], fill=banner_background_color)
    text_width, text_height = draw.textbbox((0, 0), banner_title, font=font_title)[2:]
    draw.text(
        ((image_width - text_width) / 2, (banner_height - text_height) / 2),
        banner_title,
        fill=banner_text_color,
        font=font_title,
    )

    # Draw rows of data
    row_height = (image_height - banner_height) // len(data)
    for i, (key, value) in enumerate(data.items()):
        row_y = banner_height + i * row_height
        row_color = row_colors[i % len(row_colors)]
        draw.rectangle([0, row_y, image_width, row_y + row_height], fill=row_color)

        # Text for the row
        text = f"{key}: {value}"
        text_width, text_height = draw.textbbox((0, 0), text, font=font_row)[2:]
        draw.text(
            ((image_width - text_width) / 2, row_y + (row_height - text_height) / 2),
            text,
            fill=row_text_color,
            font=font_row,
        )

    # Save the image
    image.save(output_path)

def parse_log_line(line):
    """
    Parse a single line from the Direwolf log.
    """
    columns = [
        "chan", "utime", "isotime", "source", "heard", "level", "error", "dti",
        "name", "symbol", "latitude", "longitude", "speed", "course", "altitude",
        "frequency", "offset", "tone", "system", "status", "telemetry", "comment"
    ]
    values = line.strip().split(",")
    return {columns[i]: values[i] if i < len(values) else "" for i in range(len(columns))}

def process_log_file(log_file, callback, columns):
    """
    Monitor the log file and process lines in real time.
    """
    with open(log_file, "r") as file:
        # Start from the end of the file
        file.seek(0, os.SEEK_END)

        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)
                continue

            # Parse the log line and filter by selected columns
            parsed_data = parse_log_line(line)
            filtered_data = {key: parsed_data[key] for key in columns if parsed_data.get(key)}
            
            # Skip if no selected columns contain data
            if not any(filtered_data.values()):
                continue

            callback(filtered_data)

if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description="Generate APRS image from Direwolf log data.")
    parser.add_argument("--log_file", default=DEFAULT_LOG_FILE, help="Path to the log file.")
    parser.add_argument("--output_image", default=DEFAULT_OUTPUT_IMAGE, help="Path to save the image.")
    parser.add_argument("--image_width", type=int, default=DEFAULT_IMAGE_WIDTH, help="Width of the image.")
    parser.add_argument("--image_height", type=int, default=DEFAULT_IMAGE_HEIGHT, help="Height of the image.")
    parser.add_argument("--font_path", default=DEFAULT_FONT_PATH, help="Path to the font file.")
    parser.add_argument("--banner_title", default=DEFAULT_BANNER_TITLE, help="Text to display in the banner.")
    parser.add_argument("--columns", nargs="+", default=DEFAULT_COLUMNS, help="Columns to display in the image.")
    parser.add_argument("--banner_background_color", default=DEFAULT_BANNER_BACKGROUND_COLOR, help="Background color of the banner.")
    parser.add_argument("--banner_text_color", default=DEFAULT_BANNER_TEXT_COLOR, help="Text color of the banner.")
    parser.add_argument("--row_text_color", default=DEFAULT_ROW_TEXT_COLOR, help="Text color for rows.")
    parser.add_argument(
        "--row_colors",
        nargs="+",
        default=DEFAULT_ROW_COLORS,
        help="Background colors for rows.",
    )

    args = parser.parse_args()

    # Generate the image for new log lines
    def handle_parsed_data(data):
        create_aprs_image(
            data,
            output_path=args.output_image,
            image_width=args.image_width,
            image_height=args.image_height,
            font_path=args.font_path,
            banner_title=args.banner_title,
            banner_background_color=args.banner_background_color,
            banner_text_color=args.banner_text_color,
            row_text_color=args.row_text_color,
            row_colors=args.row_colors,
        )

    process_log_file(args.log_file, handle_parsed_data, args.columns)
