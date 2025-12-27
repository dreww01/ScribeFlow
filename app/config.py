import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_DIR = os.path.join(BASE_DIR, "videos")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
ASS_DIR = os.path.join(BASE_DIR, "subtitles")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

# Ensure directories exist
for folder in [VIDEO_DIR, AUDIO_DIR, OUTPUT_DIR, ASS_DIR, FONTS_DIR, TEMP_DIR]:
    os.makedirs(folder, exist_ok=True)


# Default Settings
DEFAULT_FONT_NAME = "Playfair Display"
