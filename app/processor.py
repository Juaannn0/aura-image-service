"""Image processing logic for the AURA Image Service."""

from io import BytesIO
from typing import Protocol

from PIL import Image
from rembg import new_session
from rembg import remove

from app.config import CANVAS_COLOR
from app.config import OUTPUT_SIZE
from app.config import REMBG_MODEL
from app.config import WEBP_QUALITY
from app.utils import get_content_bbox


class ProcessingError(Exception):
    """Raised when image processing fails."""


class ImageProcessor(Protocol):
    """Protocol for future image processors."""

    def process(self, image_bytes: bytes) -> bytes:
        """Process raw image bytes and return processed output bytes."""
        ...


class ClothingImageProcessor:
    """Remove background, center clothing on white canvas, export as WEBP."""

    def __init__(self) -> None:
        self._session = new_session(REMBG_MODEL)

    def process(self, image_bytes: bytes) -> bytes:
        try:
            removed_bytes = remove(image_bytes, session=self._session)
        except Exception as exc:
            raise ProcessingError("Background removal failed.") from exc

        try:
            with Image.open(BytesIO(removed_bytes)) as image:
                rgba_image = image.convert("RGBA")
                bbox = get_content_bbox(rgba_image)
                cropped = rgba_image.crop(bbox)

                square_size = max(cropped.width, cropped.height)
                canvas = Image.new("RGB", (square_size, square_size), CANVAS_COLOR)

                offset_x = (square_size - cropped.width) // 2
                offset_y = (square_size - cropped.height) // 2
                canvas.paste(cropped, (offset_x, offset_y), cropped)

                final_image = canvas.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)

                output = BytesIO()
                final_image.save(
                    output,
                    format="WEBP",
                    quality=WEBP_QUALITY,
                    method=6,
                )
                return output.getvalue()
        except ProcessingError:
            raise
        except Exception as exc:
            raise ProcessingError("Image post-processing failed.") from exc


_default_processor: ClothingImageProcessor | None = None


def process_image(image_bytes: bytes) -> bytes:
    """Process an image through the default clothing pipeline."""
    global _default_processor
    if _default_processor is None:
        _default_processor = ClothingImageProcessor()
    return _default_processor.process(image_bytes)
