"""FastAPI application exposing the AURA Image Service REST API."""

from fastapi import FastAPI
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi.responses import Response

from app.processor import ProcessingError
from app.processor import process_image
from app.utils import InvalidImageError
from app.utils import bytes_to_response
from app.utils import validate_image_upload

app = FastAPI(title="AURA Image Service")


@app.post("/process")
async def process(image: UploadFile = File(...)) -> Response:
    print("REQUEST RECEIVED")
    print(image.filename)

    content = await image.read()

    print(len(content))
    """Receive an image, process it, and return the result as WEBP."""
    content = await image.read()

    try:
        validate_image_upload(image, content)
    except InvalidImageError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        webp_bytes = process_image(content)
    except ProcessingError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return bytes_to_response(webp_bytes, media_type="image/webp")
