# AURA Image Service

Standalone microservice for image processing in the AURA application. Receives an image via REST API, removes the background, centers the clothing item on a white canvas, and returns a processed WEBP image.

## Tech Stack

- Python 3.12+
- FastAPI
- rembg (background removal)
- Pillow (image manipulation)
- Uvicorn
- Docker

## Project Structure

```
app/
    main.py        # API routes only
    processor.py   # Image processing logic
    config.py      # Configurable constants
    utils.py       # Reusable helper functions
requirements.txt
Dockerfile
docker-compose.yml
```

## Requirements

- Python 3.12 or higher
- Docker (optional, for containerized deployment)

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Docker Setup

```bash
docker compose up --build
```

The service listens on port `8000`.

## Railway Deployment

1. Push this repo to GitHub as `aura-image-service`.
2. In Railway, create a new service from the repo and select **Dockerfile** as the build method.
3. Railway injects `PORT` automatically; the Dockerfile reads it at runtime.
4. Use at least **1 GB RAM** (2 GB recommended) — rembg loads an ~176 MB ONNX model.

## API

### POST /process

Accepts `multipart/form-data` with a single field:

| Field  | Type | Description        |
|--------|------|--------------------|
| image  | file | Image to process   |

**Success response:** `200 OK` with `Content-Type: image/webp` (binary WEBP body).

**Error responses:**

| Status | Condition              | Body        |
|--------|------------------------|-------------|
| 400    | Invalid upload         | JSON error  |
| 500    | Background removal fail| JSON error  |

### Example

```bash
curl -X POST http://localhost:8000/process \
  -F "image=@prenda.jpg" \
  -o output.webp
```

## Processing Pipeline

1. Remove background using rembg
2. Preserve the clothing item
3. Create a square white canvas
4. Center the clothing item
5. Resize to 800x800 px
6. Convert to WEBP (quality ~90)
7. Return the WEBP image in the HTTP response

Images are processed entirely in memory. No files are stored permanently.

## Extensibility

Future processors (dominant color extraction, clothing classification, OCR, etc.) can be added as new classes implementing the `ImageProcessor` protocol in `processor.py` without modifying the API layer.

## License

Internal AURA project.
