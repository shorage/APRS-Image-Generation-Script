Instructions for Using the APRS Image Generation Script

This script processes a real-time APRS log file and generates an image displaying selected APRS data. The script is highly configurable, allowing users to pass various parameters through the command line.
How to Run the Script

    Ensure Prerequisites:
        Python 3 is installed.
        The Pillow library is installed (pip install pillow).

    Run the Script:

python script.py [arguments]

Example Usage:

    python script.py --log_file /path/to/logfile.log --output_image /tmp/direwatch.png --image_width 320 --image_height 240 --font_path /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf --banner_background_color navy --banner_text_color yellow --row_text_color white --row_colors red green blue purple orange

Script Arguments
Log File Options
Argument	Default Value	Description
--log_file	/home/fcosta/digipi/direwolf.log	Path to the APRS log file. The script monitors this file in real time for new entries.
Output Image Options
Argument	Default Value	Description
--output_image	/tmp/direwatch.png	Path to save the generated PNG image.
--image_width	320	Width of the generated image in pixels.
--image_height	240	Height of the generated image in pixels.
Font Options
Argument	Default Value	Description
--font_path	/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf	Path to the font file used for text rendering. Must be a TrueType font (.ttf).
Banner Options
Argument	Default Value	Description
--banner_background_color	navy	Background color of the banner (e.g., red, #000080).
--banner_text_color	yellow	Text color of the banner (e.g., white, #FFFF00).
Row Options
Argument	Default Value	Description
--row_text_color	white	Text color for the rows (e.g., white, #FFFFFF).
--row_colors	["red", "green", "blue", "purple", "orange"]	Background colors for rows. Cycles through these colors for each row.
Columns in the Log File

The log file contains the following columns (data fields). Each column represents specific information extracted during an APRS transmission:
Column Name	Description
chan	Channel number.
utime	Unix timestamp of the transmission.
isotime	ISO 8601 formatted timestamp of the transmission.
source	Source callsign of the transmission.
heard	Destination or relay callsign heard by the source.
level	Signal level (e.g., 14(3/2) for raw level, SNR).
error	Error rate of the signal (e.g., 0 for no errors).
dti	Data type identifier for the transmission.
name	Name of the station or device.
symbol	APRS symbol (e.g., /# for a station).
latitude	Latitude coordinate of the source station. Truncated to 5 decimal places in the image.
longitude	Longitude coordinate of the source station. Truncated to 5 decimal places in the image.
speed	Speed of the source station (in km/h or mph).
course	Direction of movement (in degrees).
altitude	Altitude of the source station (in meters or feet).
frequency	Operating frequency of the station.
offset	Frequency offset (e.g., repeater shift).
tone	Tone frequency for signaling (e.g., CTCSS/DCS).
system	Type of device/system used (e.g., Kenwood TM-D700).
status	Current status of the source station (e.g., In Service).
telemetry	Additional telemetry data sent by the station.
comment	User-defined comments or additional metadata.
How Data is Processed

    Parsing the Log:
        The script monitors the specified log file in real-time and reads new lines as they are added.
        Each line is parsed into a dictionary based on the columns listed above.
        Invalid or missing data for key columns (e.g., latitude and longitude) is handled gracefully.

    Data Filtering:
        Only rows with valid, non-empty data are included in the image generation process.
        Latitude and longitude values are truncated to 5 decimal places.

    Image Generation:
        A banner at the top displays the title (APRS BPQ by default).
        Below the banner, up to 5 rows of data are displayed with configurable background and text colors.
        Rows cycle through the specified row_colors list for their background.

Customizing Rows Displayed

The script is designed to display specific columns in the image. By default, it includes:

    source
    heard
    latitude
    longitude
    speed

You can modify the script to include other columns or dynamically pass the desired columns through command-line arguments.
Common Issues and Debugging

    Font Issues:
        Ensure the --font_path points to a valid .ttf font file. If missing, install fonts (e.g., sudo apt install fonts-dejavu).

    Colors Not Displaying:
        Verify color names or hexadecimal values are valid (e.g., red, #FF0000).

    Log Parsing Errors:
        If the script fails to parse the log file, ensure the file format matches the expected CSV-like format (comma-delimited).

Contact

If you encounter issues or need further assistance, feel free to ask for help!
