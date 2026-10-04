"""Render a 1200x630 share image as PNG.

Usage: og-image.py OUTPUT.png "Title" ["Eyebrow"]
Needs rsvg-convert on PATH, for example via `nix shell nixpkgs#librsvg`.
"""

import base64
import html
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHOTO = ROOT / "public/assets/patrick.jpg"


def layout(title: str) -> tuple[list[str], int]:
    for width, size in ((26, 64), (30, 56), (34, 50)):
        wrapped = textwrap.wrap(title, width=width)
        if len(wrapped) <= 3:
            return wrapped, size
    wrapped = wrapped[:3]
    wrapped[-1] = wrapped[-1].rstrip(" ,.:;") + "…"
    return wrapped, size


def svg(title: str, eyebrow: str) -> str:
    photo = base64.b64encode(PHOTO.read_bytes()).decode()
    rows, size = layout(title)
    start = 315 - (len(rows) - 1) * size * 0.6
    text = "".join(
        f'<text x="80" y="{start + i * size * 1.2:.0f}" font-size="{size}" font-weight="800" fill="#eeeff2">{html.escape(row)}</text>'
        for i, row in enumerate(rows)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <radialGradient id="glow" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(0 0) scale(900 600)">
      <stop stop-color="#419f99" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#419f99" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="avatar"><circle cx="124" cy="532" r="44"/></clipPath>
  </defs>
  <rect width="1200" height="630" fill="#101114"/>
  <rect width="1200" height="630" fill="url(#glow)"/>
  <rect x="80" y="96" width="56" height="4" rx="2" fill="#419f99"/>
  <g font-family="Noto Sans, sans-serif">
    <text x="80" y="150" font-size="24" font-weight="700" letter-spacing="3" fill="#419f99">{html.escape(eyebrow.upper())}</text>
    {text}
    <image x="80" y="488" width="88" height="88" clip-path="url(#avatar)" preserveAspectRatio="xMidYMid slice" xlink:href="data:image/jpeg;base64,{photo}"/>
    <circle cx="124" cy="532" r="44" fill="none" stroke="#292c32" stroke-width="2"/>
    <text x="192" y="526" font-size="28" font-weight="700" fill="#eeeff2">Patrick Kappen</text>
    <text x="192" y="562" font-size="22" fill="#a1a6af">patrick.kappen.io</text>
  </g>
</svg>"""


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    output, title = Path(sys.argv[1]), sys.argv[2]
    eyebrow = sys.argv[3] if len(sys.argv) > 3 else "Senior DevOps, AI and security engineer"
    subprocess.run(["rsvg-convert", "-w", "1200", "-h", "630", "-o", str(output)], input=svg(title, eyebrow).encode(), check=True)


if __name__ == "__main__":
    main()
