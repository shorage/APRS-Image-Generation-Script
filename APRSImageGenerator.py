import os
import time
import argparse
from PIL import Image, ImageDraw, ImageFont

def create_aprs_image(data, output_image_path, image_width, image_height, font_path, row_colors, row_text_color, banner_background_color, banner_text_color):
    banner_text = "APRS BPQ"
    
    # Create image
    image = Image.new("RGB", (image_width, image_height), color=banner_background_color)
    draw = ImageDraw.Draw(image)
    
    # Banner
    font_title = ImageFont.truetype(font_path, 28)
    banner_height = image_height // 6
    draw.rectangle([0, 0, image_width, banner_height], fill=banner_background_color)
    banner_text_width, banner_text_height = draw.textbbox((0, 0), banner_text, font=font_title)[2:4]
    draw.text(
        ((image_width - banner_text_width) / 2, (banner_height - banner_text_height) / 2),
        banner_text,
        fill=banner_text_color,
        font=font_title,
    )
    
    # Rows
    font_row = ImageFont.truetype(font_path, 18)
    row_height = (image_height - banner_height) // len(data)
    for idx, (key, value) in enumerate(data.items()):
        row_y = banner_height + idx * row_height
        draw.rectangle([0, row_y, image_width, row_y + row_height], fill=row_colors[idx % len(row_colors)])
        text = f"{key}: {value}"
        text_width, text_height = draw.textbbox((0, 0), text, font=font_row)[2:4]
        draw.text(
            ((image_width - text_width) / 2, row_y + (row_height - text_height) / 2),
            text,
            fill=row_text_color,
            font=font_row,
        )
    
    image.save(output_image_path)

def parse_log_line(line):
    columns = [
        "chan", "utime", "isotime", "source", "heard", "level", "error", "dti",
        "name", "symbol", "latitude", "longitude", "speed", "course", "altitude",
        "frequency", "offset", "tone", "system", "status", "telemetry", "comment"
    ]
    values = line.strip().split(",")
    parsed_data = dict(zip(columns, values))
    
    # Truncate latitude and longitude to 5 decimal places
    try:
        parsed_data["latitude"] = f"{float(parsed_data.get('latitude', '')):.5f}" if parsed_data.get("latitude") else ""
        parsed_data["longitude"] = f"{float(parsed_data.get('longitude', '')):.5f}" if parsed_data.get("longitude") else ""
    except ValueError:
        parsed_data["latitude"] = parsed_data["longitude"] = ""
    return parsed_data

def process_log_file(log_file_path, callback):
    with open(log_file_path, "r", encoding="utf-8", errors="ignore") as file:
        # Seek to the end of the file
        file.seek(0, os.SEEK_END)
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)
                continue
            parsed_data = parse_log_line(line)
            callback(parsed_data)

def handle_parsed_data(parsed_data, output_image_path, image_width, image_height, font_path, row_colors, row_text_color, banner_background_color, banner_text_color):
    # Filter out rows with no data
    filtered_data = {
        key: value for key, value in parsed_data.items()
        if key in ["source", "heard", "latitude", "longitude", "speed", "altitude"] and value
    }
    if filtered_data:
        create_aprs_image(filtered_data, output_image_path, image_width, image_height, font_path, row_colors, row_text_color, banner_background_color, banner_text_color)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-time APRS log monitor with image generation.")
    parser.add_argument("--log_file", default="/path/to/direwolf/direwolf.log", help="Path to the log file.")
    parser.add_argument("--output_image", default="/path/to/aprswatch.png", help="Path to save the output image.")
    parser.add_argument("--image_width", type=int, default=320, help="Width of the output image.")
    parser.add_argument("--image_height", type=int, default=240, help="Height of the output image.")
    parser.add_argument("--font_path", default="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", help="Path to the font file.")
    parser.add_argument("--banner_background_color", default="navy", help="Background color of the banner.")
    parser.add_argument("--banner_text_color", default="yellow", help="Text color of the banner.")
    parser.add_argument("--row_text_color", default="white", help="Text color for each row.")
    parser.add_argument("--row_colors", nargs="+", default=["red", "green", "blue", "purple", "orange"], help="Colors for each row.")
    args = parser.parse_args()

    def callback(parsed_data):
        handle_parsed_data(
            parsed_data,
            args.output_image,
            args.image_width,
            args.image_height,
            args.font_path,
            args.row_colors,
            args.row_text_color,
            args.banner_background_color,
            args.banner_text_color,
        )

    process_log_file(args.log_file, callback)
