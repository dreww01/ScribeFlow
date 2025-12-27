from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class SubtitleConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    max_words_per_line: int = Field(default=6, ge=1, description="Maximum words per subtitle line")
    subtitle_color: str = Field(default="#FFFFFF", description="Font color in Hex or name")
    font_weight: int = Field(default=400, ge=100, le=900, description="Font weight (100-900)")
    font_size: int = Field(default=48, ge=1, description="Font size")
    shadow_strength: float = Field(default=1.0, ge=0, description="Shadow strength")
    enable_bounce: bool = Field(default=False, description="Enable bounce entry effect")
    lang: str = Field(default="en", description="Audio language code (e.g., 'en', 'th')")
    position: Literal["1", "2", "3", "4"] = Field(default="1", description="1=Bottom, 2=Middle, 3=Top, 4=Offset Bottom")
    use_gpu: bool = Field(default=True, description="Enable GPU acceleration for transcription")
    video_encoding_preset: Literal["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"] = Field(
        default="ultrafast", 
        description="FFmpeg encoding preset. 'ultrafast' is fastest but larger file size. 'medium' is default balance."
    )


    @property
    def alignment(self) -> int:
        alignment_map = {"1": 2, "2": 5, "3": 8, "4": 5}
        return alignment_map.get(self.position, 2)

    @property
    def margin_v(self) -> int:
        return 180 if self.position == "4" else 30
