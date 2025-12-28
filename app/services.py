import os
import subprocess
import time
import logging
from datetime import timedelta
from faster_whisper import WhisperModel
from app.config import FONTS_DIR, DEFAULT_FONT_NAME
from app.schemas import SubtitleConfig
from typing import List, Iterable

from typing import List, Iterable, Dict

logger = logging.getLogger("uvicorn")

# Common color names to RGB hex mapping
COLOR_MAP: Dict[str, str] = {
    "white": "FFFFFF",
    "black": "000000",
    "red": "FF0000",
    "green": "00FF00",
    "blue": "0000FF",
    "yellow": "FFFF00",
    "cyan": "00FFFF",
    "magenta": "FF00FF",
    "silver": "C0C0C0",
    "gray": "808080",
    "maroon": "800000",
    "olive": "808000",
    "purple": "800080",
    "teal": "008080",
    "navy": "000080",
    "orange": "FFA500",
    "gold": "FFD700",
    "pink": "FFC0CB",
    "brown": "A52A2A",
}

def color_to_ass(color_str: str) -> str:
    """
    Converts a color string (hex or name) to ASS format (&H00BBGGRR).
    Defaults to white if invalid.
    """
    color_str = color_str.strip().lower()
    
    # Check if it's a known color name
    if color_str in COLOR_MAP:
        hex_val = COLOR_MAP[color_str]
    elif color_str.startswith("#"):
        hex_val = color_str.lstrip("#")
        # Handle short hex #FFF
        if len(hex_val) == 3:
            hex_val = "".join([c*2 for c in hex_val])
    else:
        # If it's not a name or hex, might be a bare hex string
        hex_val = color_str

    # Ensure we have exactly 6 characters of hex
    if len(hex_val) != 6 or not all(c.lower() in "0123456789abcdef" for c in hex_val):
        logger.warning(f"Invalid color format: {color_str}. Defaulting to white.")
        return "&H00FFFFFF"

    # ASS format is &H00BBGGRR (BGR, not RGB)
    r = hex_val[0:2]
    g = hex_val[2:4]
    b = hex_val[4:6]
    return f"&H00{b}{g}{r}".upper()

class ModelManager:
    _instance = None
    _device = "cpu"


    @classmethod
    def load_model(cls, use_gpu: bool = True):
        device = "cuda" if use_gpu else "cpu"
        compute_type = "float16" if use_gpu else "int8"
        
        if cls._instance is None or cls._device != device:
            try:
                logger.info(f"Loading Whisper Model on {device}...")
                cls._instance = WhisperModel("small", device=device, compute_type=compute_type)
                cls._device = device
                logger.info("Model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load model on {device}: {e}")
                if device == "cuda":
                    logger.info("Falling back to CPU...")
                    cls._instance = WhisperModel("small", device="cpu", compute_type="int8")
                    cls._device = "cpu"
                else:
                    raise e
        return cls._instance

def format_time(seconds: float) -> str:
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    centis = int((seconds - total_seconds) * 100)
    return f"{hours}:{minutes:02}:{secs:02}.{centis:02}"

def extract_audio(video_path: str, audio_path: str) -> None:
    logger.info(f"Extracting audio from {video_path} to {audio_path}")
    command = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        audio_path
    ]
    # Capture stderr to debug ffmpeg issues
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode()
        logger.error(f"FFmpeg failed: {error_msg}")
        raise RuntimeError(f"FFmpeg failed with error: {error_msg}")


def generate_subtitles(audio_path: str, lang: str, use_gpu: bool) -> List:
    try:
        model = ModelManager.load_model(use_gpu)
        segments, _ = model.transcribe(audio_path, language=lang)
        # Convert generator to list to ensure processing finishes
        return list(segments)
    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}")
        raise

def create_ass_file(segments, ass_path: str, settings: SubtitleConfig) -> None:
    ass_color = color_to_ass(settings.subtitle_color)
    
    with open(ass_path, "w", encoding="utf-8") as f:
        # Header
        f.write("[Script Info]\nScriptType: v4.00+\nPlayResX:1280\nPlayResY:720\nWrapStyle:0\nScaledBorderAndShadow:yes\n\n")
        # Styles
        f.write("[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n")
        f.write(f"Style: Default,{DEFAULT_FONT_NAME},{settings.font_size},{ass_color},{settings.font_weight},0,0,0,100,100,0,0,1,2,{settings.shadow_strength},{settings.alignment},10,10,{settings.margin_v},1\n\n")
        # Events
        f.write("[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n")
        
        for segment in segments:
            words = segment.text.strip().split()
            if not words:
                continue
            
            duration = segment.end - segment.start
            if duration <= 0:
                continue

            avg_word_duration = duration / len(words)
            
            for i in range(0, len(words), settings.max_words_per_line):
                chunk = words[i:i + settings.max_words_per_line]
                chunk_start = segment.start + i * avg_word_duration
                chunk_end = chunk_start + len(chunk) * avg_word_duration
                text = " ".join(chunk)
                
                if settings.enable_bounce:
                    effect = r"{\fscx30\fscy30\t(0,75,\fscx115\fscy115)\t(75,150,\fscx100\fscy100)}"
                    text = f"{effect}{text}"
                
                f.write(f"Dialogue: 0,{format_time(chunk_start)},{format_time(chunk_end)},Default,,0,0,0,,{text}\n")

def burn_subtitles(video_path: str, ass_path: str, output_path: str, preset: str = "ultrafast") -> None:
    # Convert paths to forward slashes for ffmpeg compatibility (Windows issue)
    ass_path_ffmpeg = ass_path.replace("\\", "/").replace(":", "\\:")
    fonts_dir_ffmpeg = FONTS_DIR.replace("\\", "/").replace(":", "\\:")
    
    logger.info(f"Burning subtitles: {ass_path} -> {output_path} (Preset: {preset})")
    
    # Note: escaping the colon for Windows absolute paths in filter arguments
    # Simplest safe way is usually relative paths or complex escaping. 
    # Let's try basic forward slash replacement which works in many cases, 
    # but the Drive letter colon (C:) is tricky in filters.
    
    # robust path handling for windows ffmpeg filters
    def escape_path(path):
        # Escape colons and backslashes
        return path.replace("\\", "/").replace(":", "\\:")

    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", f"ass='{escape_path(ass_path)}':fontsdir='{escape_path(fonts_dir_ffmpeg)}'",
        "-c:v", "libx264", "-preset", preset,
        "-c:a", "copy",
        output_path
    ]
    
    # Debug print
    logger.debug(f"FFmpeg command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg Error: {e.stderr.decode()}")
        raise RuntimeError(f"FFmpeg failed to burn subtitles")
