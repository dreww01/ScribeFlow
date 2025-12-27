import os
import shutil
import json
import logging
import uvicorn
from contextlib import asynccontextmanager
from typing import Annotated
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
    # Startup: Load Model
    logger.info("Startup: Pre-loading Whisper model...")
    # Pre-load on GPU by default if available
    try:
        ModelManager.load_model(use_gpu=True)
    except Exception as e:
        logger.warning(f"Startup model load failed: {e}")
    yield
    # Shutdown logic (if any)
    logger.info("Shutdown: Cleaning up...")

app = FastAPI(title="ScribeFlow API", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Welcome to ScribeFlow API. Go to /docs for the interface."}

@app.post("/generate")
async def generate_video(
    video: Annotated[UploadFile, File(description="Video file to process")],
    config_json: Annotated[str, Form(description="JSON string of SubtitleConfig")] = '{}'
):
    try:
        # Parse Config
        config_data = json.loads(config_json)
        settings = SubtitleConfig(**config_data)
        
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
