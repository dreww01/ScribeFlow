import os
import shutil
import json
import logging
import uvicorn
from contextlib import asynccontextmanager
from typing import Annotated, Literal
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from app.services import ModelManager, extract_audio, generate_subtitles, create_ass_file, burn_subtitles
from app.schemas import SubtitleConfig
from app.config import TEMP_DIR, AUDIO_DIR, ASS_DIR, OUTPUT_DIR


# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Startup: ScribeFlow API is starting...")
    yield
    # Shutdown logic
    logger.info("Shutdown: Cleaning up...")

app = FastAPI(title="ScribeFlow API", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Welcome to ScribeFlow API. Go to /docs for the interface."}

def get_subtitle_config(
    max_words_per_line: int = Form(6, ge=1, description="Maximum words per subtitle line"),
    subtitle_color: str = Form("#FFFFFF", description="Font color in Hex or name"),
    font_weight: int = Form(400, ge=100, le=900, description="Font weight (100-900)"),
    font_size: int = Form(48, ge=1, description="Font size"),
    shadow_strength: float = Form(1.0, ge=0, description="Shadow strength"),
    enable_bounce: bool = Form(False, description="Enable bounce entry effect"),
    lang: str = Form("en", description="Audio language code (e.g., 'en', 'th')"),
    position: Literal["1", "2", "3", "4"] = Form("1", description="1=Bottom, 2=Middle, 3=Top, 4=Offset Bottom"),
    use_gpu: bool = Form(True, description="Enable GPU acceleration for transcription"),
    video_encoding_preset: Literal["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"] = Form(
        "ultrafast", 
        description="FFmpeg encoding preset. 'ultrafast' is fastest but larger file size."
    )
) -> SubtitleConfig:
    return SubtitleConfig(
        max_words_per_line=max_words_per_line,
        subtitle_color=subtitle_color,
        font_weight=font_weight,
        font_size=font_size,
        shadow_strength=shadow_strength,
        enable_bounce=enable_bounce,
        lang=lang,
        position=position,
        use_gpu=use_gpu,
        video_encoding_preset=video_encoding_preset
    )

@app.post("/generate")
async def generate_video(
    video: Annotated[UploadFile, File(description="Video file to process")],
    settings: Annotated[SubtitleConfig, Depends(get_subtitle_config)]
):
    try:
        
        # unique ID for this request
        timestamp = str(int(os.times().elapsed * 100)) # using simplified timestamp
        base_name = f"req_{timestamp}"
        
        # Save uploaded video
        video_ext = os.path.splitext(video.filename)[1]
        input_video_path = os.path.join(TEMP_DIR, f"{base_name}{video_ext}")
        
        with open(input_video_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
            
        # Paths
        audio_path = os.path.join(AUDIO_DIR, f"{base_name}.wav")
        ass_path = os.path.join(ASS_DIR, f"{base_name}.ass")
        output_video_path = os.path.join(OUTPUT_DIR, f"subbed_{base_name}.mp4")
        
        # 1. Extract Audio
        extract_audio(input_video_path, audio_path)
        
        # 2. Transcribe
        segments = generate_subtitles(audio_path, settings.lang, settings.use_gpu)
        
        # 3. Create ASS
        create_ass_file(segments, ass_path, settings)
        
        # 4. Burn Subtitles
        burn_subtitles(input_video_path, ass_path, output_video_path, settings.video_encoding_preset)
        
        # 5. Cleanup (Optional, removing temp video/audio)
        if os.path.exists(input_video_path):
            os.remove(input_video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)
            
        return FileResponse(output_video_path, media_type="video/mp4", filename=f"subbed_{video.filename}")

    except Exception as e:
        logger.error(f"Processing error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
