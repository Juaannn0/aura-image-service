"""Configurable constants for the AURA Image Service."""

from typing import Final

OUTPUT_SIZE: Final[tuple[int, int]] = (800, 800)
WEBP_QUALITY: Final[int] = 90
CANVAS_COLOR: Final[tuple[int, int, int]] = (255, 255, 255)
MAX_UPLOAD_SIZE_BYTES: Final[int] = 10 * 1024 * 1024
REMBG_MODEL: Final[str] = "u2netp"

ALLOWED_CONTENT_TYPES: Final[frozenset[str]] = frozenset(
    {
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
        "image/bmp",
        "image/tiff",
    }
)
