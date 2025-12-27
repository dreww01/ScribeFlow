# ScribeFlow 🎬✨

**Automatic Video Subtitle Generator powered by Whisper AI**

ScribeFlow is a production-ready Python application that automatically generates and burns subtitles into videos using state-of-the-art speech recognition. Built with FastAPI, it offers both a REST API and can be deployed as a scalable microservice.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Deploy to Cloud Run](https://github.com/dreww01/ScribeFlow/actions/workflows/deploy.yml/badge.svg)](https://github.com/dreww01/ScribeFlow/actions/workflows/deploy.yml)

---

## ✨ Features

- 🎯 **Automatic Speech Recognition** - Powered by [OpenAI Whisper](https://github.com/openai/whisper) via [faster-whisper](https://github.com/SYSTRAN/faster-whisper) for accurate transcription
- 🎨 **Customizable Subtitles** - Full control over font, color, size, position, shadows, and animated effects
- 🔥 **Subtitle Burning** - Hardcode subtitles directly into videos using FFmpeg
- 🌍 **Multi-language Support** - English, Thai, Japanese, Chinese, and more
- ⚡ **GPU Acceleration** - Optional CUDA support for faster processing
- 🚀 **REST API** - Production-ready FastAPI server with interactive documentation
- 🐳 **Docker Ready** - Containerized for easy deployment
- ☁️ **Cloud Deployment** - Automated CI/CD pipeline with GitHub Actions to Google Cloud Run
- 🔧 **Highly Configurable** - Extensive customization options via API parameters
- 📦 **Batch Processing** - Process multiple videos efficiently

---

## 📋 Table of Contents

- [Requirements](#-requirements)
- [Quick Start](#-quick-start)
- [Installation](#-installation)B47E-8198
- [Usage](#-usage)
  - [API Server](#api-server)
  - [API Endpoints](#api-endpoints)
  - [Configuration Options](#configuration-options)
- [Docker Deployment](#-docker-deployment)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Advanced Usage](#-advanced-usage)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Credits](#-credits)

---

## 🔧 Requirements

### System Requirements
- **Python**: 3.10 or higher
- **FFmpeg**: Must be installed and available in system PATH
- **RAM**: Minimum 4GB (8GB+ recommended for large videos)
- **GPU** (Optional): NVIDIA GPU with CUDA for faster processing

### Python Dependencies
All dependencies are managed via `pyproject.toml` and `requirements.txt`:
- `faster-whisper>=1.1.1` - Optimized Whisper implementation
- `fastapi` - Web framework
- `uvicorn[standard]` - ASGI server
- `ffmpeg-python>=0.2.0` - FFmpeg wrapper
- `pysrt` - Subtitle parsing
- `python-multipart` - File upload support
- `httpx` - HTTP client
- `numpy>=1.23.0` - Numerical operations

---

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/dreww01/ScribeFlow.git
cd ScribeFlow

# Build and run with Docker
docker build -t scribeflow .
docker run -p 8080:8080 scribeflow

# Access the API at http://localhost:8080/docs
```

### Local Installation

```bash
# Clone the repository
git clone https://github.com/dreww01/ScribeFlow.git
cd ScribeFlow

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python run.py
```

Visit [http://localhost:8080/docs](http://localhost:8080/docs) for interactive API documentation.

---

## 📦 Installation

### Option 1: Using pip (Standard)

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Using uv (Fast Alternative)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer:

```bash
# Install uv (if not already installed)
pip install uv

# Create virtual environment and install dependencies
uv venv
uv pip install -r requirements.txt
```

### Option 3: Using pyproject.toml

```bash
pip install -e .
```

### Installing FFmpeg

#### Windows
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract and add to system PATH
3. Verify: `ffmpeg -version`

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

---

## 💻 Usage

### API Server

#### Start the Server

```bash
# Method 1: Using run.py
python run.py

# Method 2: Using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

# Method 3: Production mode (no reload)
uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers 4
```

The server will start on `http://localhost:8080`

### API Endpoints

#### `POST /generate` - Generate Subtitles

Upload a video and generate subtitles with custom configuration.

**Request:**
```bash
curl -X POST "http://localhost:8080/generate" \
  -F "video=@your_video.mp4" \
  -F 'config_json={"language":"en","subtitle_color":"yellow","font_size":24,"max_words_per_line":5,"use_gpu":false}'
```

**Python Example:**
```python
import requests
import json

url = "http://localhost:8080/generate"

config = {
    "language": "en",
    "subtitle_color": "yellow",
    "font_size": 24,
    "font_weight": "bold",
    "max_words_per_line": 5,
    "use_gpu": False,
    "bounce_effect": True
}

files = {"video": open("video.mp4", "rb")}
data = {"config_json": json.dumps(config)}

response = requests.post(url, files=files, data=data)

with open("output_with_subtitles.mp4", "wb") as f:
    f.write(response.content)
```

**Response:**
- Success: Returns the processed video file (video/mp4)
- Error: Returns JSON with error details

### Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `language` | string | `"en"` | Language code: `en`, `th`, `ja`, `zh` |
| `subtitle_color` | string | `"yellow"` | Color name or hex code |
| `font_size` | integer | `24` | Font size in points |
| `font_name` | string | `"Playfair Display"` | Font family name |
| `font_weight` | string | `"bold"` | Font weight: `normal`, `bold` |
| `max_words_per_line` | integer | `5` | Maximum words per subtitle line |
| `use_gpu` | boolean | `false` | Enable GPU acceleration (requires CUDA) |
| `bounce_effect` | boolean | `false` | Enable animated bounce effect |
| `shadow_depth` | integer | `2` | Shadow depth for text |
| `subtitle_position` | string | `"bottom"` | Position: `top`, `middle`, `bottom` |

### Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: [http://localhost:8080/docs](http://localhost:8080/docs)
- **ReDoc**: [http://localhost:8080/redoc](http://localhost:8080/redoc)

---

## 🐳 Docker Deployment

### Build and Run Locally

> [!NOTE]
> The Whisper "small" model is pre-baked into the Docker image, ensuring fast startup and no runtime dependencies on Hugging Face.

```bash
# Build the image
docker build -t scribeflow:latest .

# Run the container
docker run -d \
  --name scribeflow \
  -p 8080:8080 \
  -v $(pwd)/outputs:/app/outputs \
  scribeflow:latest
```

For more advanced Docker usage, see [docs/docker.md](docs/docker.md).

### Docker Compose (Coming Soon)

```yaml
version: '3.8'
services:
  scribeflow:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./outputs:/app/outputs
    environment:
      - WORKERS=4
```

### Cloud Deployment

#### Google Cloud Run (Recommended)

ScribeFlow includes automated CI/CD deployment to Google Cloud Run using GitHub Actions.

**Features:**
- ✅ Automatic deployment on push to `main` branch
- ✅ Zero-downtime deployments
- ✅ Stays within GCP free tier for portfolio projects
- ✅ Professional CI/CD pipeline

**Setup Guide:** See [docs/gcp-setup.md](docs/gcp-setup.md) for complete step-by-step instructions.

**Quick Start:**
1. Follow the [GCP Setup Guide](docs/gcp-setup.md)
2. Configure GitHub Secrets (`GCP_PROJECT_ID`, `GCP_SA_KEY`)
3. Push to `main` branch - automatic deployment!

**Manual Deployment:**
- Go to **Actions** tab in GitHub
- Select **Manual Deploy to Cloud Run**
- Click **Run workflow**

---

#### Other Cloud Platforms

For deployment to other platforms, see:
- AWS ECS
- Azure Container Instances
- DigitalOcean App Platform

---

## 📁 Project Structure

```
ScribeFlow/
├── app/                    # FastAPI application
│   ├── __init__.py
│   ├── main.py            # API routes and entry point
│   ├── services.py        # Core business logic
│   ├── schemas.py         # Pydantic models
│   └── config.py          # Configuration settings
├── tests/                 # Test suite
│   ├── conftest.py        # Pytest fixtures
│   └── test_main.py       # API tests
├── audio/                 # Extracted audio files (temporary)
├── fonts/                 # Custom font files
├── outputs/               # Final processed videos
├── subtitles/             # Generated .ass subtitle files
├── temp/                  # Temporary file uploads
├── videos/                # Input videos (for manual testing)
├── .dockerignore          # Docker build exclusions
├── .gitignore             # Git exclusions
├── architecture.md        # Detailed architecture documentation
├── docs/                  # Project documentation
│   ├── deployment.md      # Deployment guides
│   ├── gcp-setup.md       # GCP specific setup
│   └── docker.md          # Docker guide
├── Dockerfile             # Container configuration
├── LICENSE                # MIT License
├── pyproject.toml         # Python project metadata
├── README.md              # This file
├── requirements.txt       # Python dependencies
└── run.py                 # Server entry point
```

---

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/dreww01/ScribeFlow.git
cd ScribeFlow

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black ruff mypy
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_main.py -v
```

### Code Quality

```bash
# Format code
black app/ tests/

# Lint code
ruff check app/ tests/

# Type checking
mypy app/
```

### Project Architecture

For detailed architecture documentation, see [architecture.md](architecture.md).

Key components:
- **ModelManager**: Singleton for managing Whisper model lifecycle
- **Audio Extraction**: FFmpeg-based audio extraction
- **Subtitle Generation**: Whisper transcription with timestamp alignment
- **ASS File Creation**: Advanced SubStation Alpha subtitle formatting
- **Subtitle Burning**: FFmpeg-based subtitle rendering

---

## 🎓 Advanced Usage

### Custom Font Installation

1. Add `.ttf` or `.otf` font files to the `fonts/` directory
2. Reference the font name in your configuration:

```json
{
  "font_name": "YourCustomFont",
  "font_size": 28
}
```

### Batch Processing

```python
import os
import requests
import json

video_dir = "path/to/videos"
output_dir = "path/to/outputs"

config = {"language": "en", "use_gpu": True}

for video_file in os.listdir(video_dir):
    if video_file.endswith(".mp4"):
        with open(os.path.join(video_dir, video_file), "rb") as f:
            response = requests.post(
                "http://localhost:5000/generate",
                files={"video": f},
                data={"config_json": json.dumps(config)}
            )
        
        output_path = os.path.join(output_dir, f"subtitled_{video_file}")
        with open(output_path, "wb") as out:
            out.write(response.content)
```

### GPU Acceleration

To enable GPU acceleration:

1. Install CUDA toolkit (11.x or 12.x)
2. Install GPU-enabled dependencies:
   ```bash
   pip install faster-whisper[gpu]
   ```
3. Set `use_gpu: true` in your configuration

### Cross-Platform Path Handling

ScribeFlow automatically handles path formatting for FFmpeg across Windows, macOS, and Linux. No manual path conversion needed.

---

## 🔍 Troubleshooting

### Common Issues

**1. FFmpeg not found**
```
Error: ffmpeg not found in PATH
```
**Solution**: Install FFmpeg and add to system PATH. Verify with `ffmpeg -version`

**2. Out of memory**
```
Error: CUDA out of memory
```
**Solution**: Reduce video resolution or disable GPU (`use_gpu: false`)

**3. Import errors**
```
ModuleNotFoundError: No module named 'app'
```
**Solution**: Run from project root directory or install package: `pip install -e .`

**4. Port already in use**
```
Error: Address already in use
```
**Solution**: Change port in `run.py` or kill process using port 5000

### Performance Tips

- Use GPU acceleration for faster processing
- Process videos in batches during off-peak hours
- Use smaller Whisper models (`tiny`, `base`) for faster but less accurate results
- Increase server workers for concurrent requests: `--workers 4`

### Getting Help

- 📖 Check [architecture.md](architecture.md) for technical details
- 🐛 Report bugs via [GitHub Issues](https://github.com/dreww01/ScribeFlow/issues)
- 💬 Ask questions in [Discussions](https://github.com/dreww01/ScribeFlow/discussions)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs
1. Check existing issues first
2. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)

### Suggesting Features
1. Open an issue with the `enhancement` label
2. Describe the feature and use case
3. Provide examples if possible

### Code Contributions
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `pytest`
6. Format code: `black app/ tests/`
7. Commit changes: `git commit -m 'Add amazing feature'`
8. Push to branch: `git push origin feature/amazing-feature`
9. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add docstrings to functions and classes
- Write unit tests for new features
- Update documentation as needed
- Keep commits atomic and well-described

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**TL;DR**: You can use, modify, and distribute this software freely, even for commercial purposes, as long as you include the original license.

---

## 🙏 Credits

ScribeFlow is built on the shoulders of giants:

- **[OpenAI Whisper](https://github.com/openai/whisper)** - State-of-the-art speech recognition
- **[faster-whisper](https://github.com/SYSTRAN/faster-whisper)** - Optimized Whisper implementation
- **[FFmpeg](https://ffmpeg.org/)** - Multimedia processing framework
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern web framework
- **[CTranslate2](https://github.com/OpenNMT/CTranslate2)** - Fast inference engine

### Contributors

- **[Dreww01](https://github.com/dreww01)** - Creator and maintainer

Want to see your name here? [Contribute to the project!](#-contributing)

---

## 🌟 Star History

If you find ScribeFlow useful, please consider giving it a star ⭐ on GitHub!

---

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/dreww01/ScribeFlow/issues)
- 💡 **Feature Requests**: [GitHub Issues](https://github.com/dreww01/ScribeFlow/issues)
- 📖 **Documentation**: [Architecture Guide](architecture.md) | [Deployment Guide](docs/deployment.md) | [Docker Guide](docs/docker.md)
- 💬 **Community**: [GitHub Discussions](https://github.com/dreww01/ScribeFlow/discussions)

---

<div align="center">

**Made with ❤️ by the ScribeFlow Team**

[Website](https://github.com/dreww01/ScribeFlow) • [Documentation](architecture.md) • [Report Bug](https://github.com/dreww01/ScribeFlow/issues) • [Request Feature](https://github.com/dreww01/ScribeFlow/issues)

</div>
