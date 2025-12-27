# Use Python 3.10 slim image
FROM python:3.10-slim

# Install FFmpeg and system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for cache efficiency
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Pre-download the Whisper model to bake it into the image
RUN python3 -c "from faster_whisper import WhisperModel; WhisperModel('small', device='cpu', compute_type='int8')"

# Create necessary directories
RUN mkdir -p videos audio outputs subtitles fonts temp

# Expose the API port
EXPOSE 8080

# Run the application
CMD ["python", "run.py"]
