#!/usr/bin/env python3
"""Starter entry point for the grid-code decoder assignment."""

from __future__ import annotations

import sys
from importlib import import_module
from pathlib import Path

from PIL import Image


Pixel = tuple[int, int, int]
PixelGrid = list[list[Pixel]]


FORMAT_NAMES = (
    "00_braille", "01_morse", "02_code39", "03_pzn", "04_ean13",
    "05_telepen", "06_dx_film_edge", "07_hccb", "08_aztec_rune",
    "09_code128", "10_data_matrix", "11_qr", "12_micro_qr", "13_rmqr",
    "14_aztec", "15_pdf417", "16_micro_pdf417",
    "17_databar_expanded_stacked", "18_maxicode",
)

DECODERS = {
    name: import_module(f"formats.{name}").decode for name in FORMAT_NAMES
}

SUPPORTED_TYPES = set(DECODERS)


def decode(code_type: str, pixels: PixelGrid) -> str:
    """Dispatch a 2-D RGB pixel array to the selected starter module."""
    return DECODERS[code_type](pixels)


def load_pixels(image_path: Path) -> PixelGrid:
    image = Image.open(image_path).convert("RGB")
    return [[image.getpixel((x, y)) for x in range(image.width)]
            for y in range(image.height)]


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"usage: {argv[0]} CODE_TYPE IMAGE_PATH", file=sys.stderr)
        return 2
    code_type = argv[1]
    if code_type not in SUPPORTED_TYPES:
        print(f"unsupported code type: {code_type}", file=sys.stderr)
        return 2
    try:
        answer = decode(code_type, load_pixels(Path(argv[2])))
    except Exception as exc:
        print(exc, file=sys.stderr)
        return 1
    print(answer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
