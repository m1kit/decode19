#!/usr/bin/env python3
"""Starter entry point for the grid-code decoder assignment."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image
from formats import (
    aztec, aztec_rune, code128, code39, data_matrix,
    databar_expanded_stacked, dx_film_edge, ean13, hccb,
    japanese_braille, maxicode, micro_pdf417, micro_qr, morse, pdf417,
    pzn, qr, rmqr, telepen,
)


Pixel = tuple[int, int, int]
PixelGrid = list[list[Pixel]]


DECODERS = {
    module.__name__.rsplit(".", 1)[-1]: module.decode
    for module in (
        japanese_braille, morse, code39, pzn, ean13, telepen,
        dx_film_edge, hccb, aztec_rune, code128,
        data_matrix, qr, micro_qr, rmqr, aztec, pdf417,
        micro_pdf417, databar_expanded_stacked, maxicode,
    )
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
