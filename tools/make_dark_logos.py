"""Generate dark-theme logo variants by lightening the gray wordmark.

Keeps the saturated blue/green mark intact and recolors low-saturation (gray)
pixels to a light tone so the wordmark is legible on dark backgrounds.
Run: python tools/make_dark_logos.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

GRAPHICS = Path(__file__).resolve().parent.parent / "Graphics"
LIGHT_TONE = (213, 219, 228)  # #D5DBE4
SAT_THRESHOLD = 55            # pixels below this chroma are treated as "gray"

SOURCES = {
    "S2 Labs Horizontal.png": "S2 Labs Horizontal Dark.png",
    "S2 Labs Stacked.png": "S2 Labs Stacked Dark.png",
    "S2L-Logo.png": "S2L-Logo Dark.png",
}


def lighten_grays(src: Path, dst: Path) -> None:
    img = Image.open(src).convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            lo, hi = min(r, g, b), max(r, g, b)
            chroma = hi - lo
            if lo > 225 and chroma < 20:        # near-white background -> transparent
                px[x, y] = (r, g, b, 0)
            elif chroma < SAT_THRESHOLD:         # gray wordmark -> light tone
                px[x, y] = (*LIGHT_TONE, a)
            # else: keep the saturated blue/green mark
    img.save(dst)
    print(f"wrote {dst.name}")


def main() -> None:
    for src_name, dst_name in SOURCES.items():
        src = GRAPHICS / src_name
        if src.exists():
            lighten_grays(src, GRAPHICS / dst_name)


if __name__ == "__main__":
    main()
