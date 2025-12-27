# Deploying ScribeFlow 🚀

This guide explains how to host ScribeFlow on various platforms, with a focus on Google Cloud Platform (GCP).

## 1. Containerization (Recommended)

ScribeFlow is packaged as a Docker container. This is the preferred way to deploy to production.

### Build and Push Image

1.  **Tag your image**:
    ```bash
    docker tag scribeflow us-central1-docker.pkg.dev/YOUR_PROJECT_ID/repo/scribeflow
    ```
2.  **Push to Registry**:
    ```bash
    docker push us-central1-docker.pkg.dev/YOUR_PROJECT_ID/repo/scribeflow
    ```

## 2. Google Cloud Run Deployment

Cloud Run is the easiest way to host ScribeFlow. It scales to zero when not in use, making it cost-effective for portfolio projects.

### Recommended Configuration

*   **Port**: `8080`
*   **Memory**: `4Gi` (Minimum recommended for Whisper "small")
*   **CPU**: `2`
*   **Timeout**: Increase to `3000` seconds (50 minutes) for large videos.

### Deployment Command

```bash
gcloud run deploy scribeflow \
    --image us-central1-docker.pkg.dev/YOUR_PROJECT_ID/repo/scribeflow \
    --platform managed \
    --region us-central1 \
    --port 8080 \
    --memory 4Gi \
    --cpu 2 \
    --timeout 3000 \
    --allow-unauthenticated
```

## 3. Important Considerations

1.  **Ephemeral Filesystem**: Cloud Run files are temporary. For production, consider uploading finished videos to Google Cloud Storage (GCS).
2.  **Concurrency**: Set `--concurrency 1` to ensure each container instance processes only one video at a time, preventing memory exhaustion.
3.  **Model Loading**: ScribeFlow pre-bakes the Whisper model into the image, so you don't need to worry about runtime download errors or HF rate limits.

## 4. Other Platforms

*   **AWS ECS / Fargate**: Use the same Docker image and similar RAM/CPU allocations.
*   **DigitalOcean App Platform**: Select the "Docker" runtime and ensure 4GB+ RAM tier.
