This script parses the Direwolf comma-delimited log in real time and generates an image displaying selected information. It allows you to customize the appearance and data selection via command-line arguments.


Example Usage

    Monitor a log file and generate a custom image:

python script.py --log_file /path/to/direwolf.log --output_image /tmp/custom_aprs.png

Customize the banner title:

python script.py --banner_title "Custom APRS Display"

Use specific columns for the display:

python script.py --columns source heard latitude longitude

Set custom colors:

    python script.py --banner_background_color black --banner_text_color white --row_text_color blue

