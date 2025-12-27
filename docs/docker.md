# Docker Guide for ScribeFlow 🐳

ScribeFlow is designed to be fully containerized, making it easy to deploy on any platform that supports Docker.

## Why use Docker?

1.  **Consistency**: Ensures the application runs exactly the same way in development, staging, and production.
2.  **Dependencies**: Packages FFmpeg and all Python libraries without cluttering your host system.
3.  **Performance**: Our Docker image includes a **pre-baked Whisper model**, meaning:
    *   No runtime downloads from Hugging Face.
    *   Faster startup times (processing starts instantly).
    *   Reliability (works even if Hugging Face is down).

## Quick Start

```bash
# Build the image
docker build -t scribeflow .

# Run the container (Mapping port 8080 and outputs volume)
docker run -d \
  --name scribeflow \
  -p 8080:8080 \
  -v $(pwd)/outputs:/app/outputs \
  scribeflow
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | The port the server listens on | `8080` |
| `HF_TOKEN` | (Optional) Hugging Face token for private models | None |

## GPU Support

To run with GPU acceleration, you must have the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) installed.

```bash
docker run --gpus all -p 8080:8080 scribeflow
```

## Best Practices

*   **Memory**: Allocate at least **4GB of RAM** to the container. Whisper models are memory-intensive.
*   **Volumes**: Always mount a volume to `/app/outputs` to persist your processed videos.
*   **Logging**: Use `docker logs -f scribeflow` to monitor transcription progress.
