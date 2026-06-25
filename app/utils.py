"""Reusable helper functions for image validation and manipulation."""

from io import BytesIO

from fastapi import Response
from fastapi import UploadFile
from PIL import Image

from app.config import ALLOWED_CONTENT_TYPES
from app.config import MAX_UPLOAD_SIZE_BYTES


class InvalidImageError(Exception):
    """Raised when the uploaded file is not a valid image."""


def validate_image_upload(file: UploadFile, content: bytes) -> None:
    """Validate uploaded image bytes before processing."""
    if not content:
        raise InvalidImageError("Uploaded file is empty.")

    if len(content) > MAX_UPLOAD_SIZE_BYTES:
        raise InvalidImageError(
            f"File exceeds maximum allowed size of {MAX_UPLOAD_SIZE_BYTES} bytes."
        )

    content_type = file.content_type or ""
    if content_type and content_type not in ALLOWED_CONTENT_TYPES:
        raise InvalidImageError(f"Unsupported content type: {content_type}.")

    try:
        with Image.open(BytesIO(content)) as image:
            image.verify()
    except Exception as exc:
        raise InvalidImageError("Uploaded file is not a valid image.") from exc


def get_content_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    """Return bounding box of non-transparent pixels in an RGBA image."""
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        raise InvalidImageError("Image has no visible content after processing.")

    return bbox


def bytes_to_response(data: bytes, media_type: str) -> Response:
    """Return raw bytes as an HTTP response."""
    return Response(content=data, media_type=media_type)
