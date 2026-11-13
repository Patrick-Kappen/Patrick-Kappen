"""Shared palettes and self-contained transparent profile/section banners."""

import html
from math import ceil
from pathlib import Path
import xml.etree.ElementTree as ET

ASSETS = ".github/assets"
BANNER_SOURCE = Path(__file__).resolve().parents[1] / "art/control-room.svg"
THEMES = {
    "dark": {
        "text": "#f0f6fc", "muted": "#9198a1", "line": "#3d444d",
        "accent": "#f58220", "label": "#ffa45b", "on_accent": "#0d1117",
        "bars": ("#d96b22", "#f58220", "#ffa45b", "#f58220"),
    },
    "light": {
        "text": "#1f2328", "muted": "#59636e", "line": "#d1d9e0",
        "accent": "#bc4c00", "label": "#a74600", "on_accent": "#ffffff",
        "bars": ("#9a4000", "#bc4c00", "#a74600", "#bc4c00"),
    },
}
# The small standalone accordion icon is visible on both GitHub themes.
ICON_COLOR = "#cf6b21"
# Original PK/circuit artwork, on a common 64px grid with 3px square-ended strokes.
ICONS = {
    "profile": '<path d="m32 4 22 13v30L32 60 10 47V17zM4 23h6m-6 18h6m44-18h6m-6 18h6M18 42V22h6a7 7 0 0 1 0 14h-6m19-14v20m0-10 10-10M37 32l10 10"/><path d="M22 10v6m20-6v6M22 48v6m20-6v6" opacity=".5"/>',
    "projects": '<path d="m32 7 24 13-24 13L8 20zM8 32l24 13 24-13M8 44l24 13 24-13M32 33v24M3 20h5m48 0h5"/>',
    "git-log": '<rect x="10" y="6" width="10" height="10"/><rect x="10" y="48" width="10" height="10"/><rect x="44" y="6" width="10" height="10"/><path d="M15 16v32m0-17h22l12-12v-3M4 25h6m-6 12h6m44-6h6M37 31v19h12"/><circle cx="52" cy="50" r="3" fill="currentColor"/>',
    "shipped": '<path d="m8 22 24-13 24 13v28L32 61 8 50zm0 0 24 13 24-13M32 35v26M20 15l24 13M48 3v16m-6-6 6 6 6-6"/>',
    "now": '<circle cx="32" cy="32" r="24"/><circle cx="32" cy="32" r="12"/><path d="M32 32 50 14M32 3v7m29 22h-7M32 61v-7M3 32h7"/><circle cx="32" cy="32" r="3" fill="currentColor"/>',
    "writing": '<path d="m10 48 3-12L42 7l14 14-29 29-12 3zm25-34 14 14M13 36l14 14M8 59h48M4 48h5m47-10h5"/>',
    "tools": '<path d="m40 8-8 10 3 11 11 3 10-8a19 19 0 0 1-24 22L16 61 5 50l16-16A19 19 0 0 1 40 8z"/>',
    "certifications": '<circle cx="32" cy="24" r="17"/><path d="m22 38-5 22 15-8 15 8-5-22M23 24l7 7 14-17"/>',
    "rules": '<path d="m32 5 23 10v16c0 14-23 28-23 28S9 45 9 31V15zm-12 26 8 8 17-20"/>',
}
HEADINGS = {
    "intro": ("Hey, I'm Patrick", "profile"),
    "projects": ("Builds & side quests", "projects"),
    "git-log": ("The Git log", "git-log"),
    "shipped": ("Recently shipped", "shipped"),
    "now": ("On the radar", "now"),
    "writing": ("Notes from the rabbit hole", "writing"),
    "tools": ("Things I reach for", "tools"),
    "toolbox": ("Toolbox", "tools"),
    "certifications": ("Certifications", "certifications"),
}
# Measured from Noto Sans Bold at 30px: (text width, optical baseline).
# SVG textLength fixes horizontal layout even when a viewer uses a fallback font.
# Keep these metrics in sync with the static labels; CI needs no fonts or Pillow.
HEADING_METRICS = {
    "intro": (236.0, 80.0), "projects": (297.0, 80.0), "git-log": (160.0, 80.0),
    "shipped": (252.0, 80.0), "now": (189.0, 83.5), "writing": (396.0, 83.5),
    "tools": (261.0, 80.0), "toolbox": (117.0, 83.5), "certifications": (201.0, 83.5),
}
HEADING_HEIGHT, HEADING_ICON_SIZE, HEADING_GAP = 144, 56, 28


def heading_width(key):
    # Leave room for the end ticks on long titles, rather than squeezing the logo.
    text_width, _ = HEADING_METRICS[key]
    return max(500, ceil((HEADING_ICON_SIZE + HEADING_GAP + text_width + 80) / 20) * 20)


def section_heading(key, level=2):
    """Image section titles without GitHub's automatic H1/H2 underlines."""
    if level not in (1, 2, 3):
        raise ValueError("Unsupported heading level")
    label, _ = HEADINGS[key]
    width = heading_width(key)
    if level == 3:
        width = round(width * .84)
    picture = themed_picture(f"{ASSETS}/headings/{key}", label, width=str(width))
    return f'<p align="center" id="{key}">\n{picture}\n</p>'


def themed_picture(stem, alt, width="100%", href=None):
    source = html.escape(stem, quote=True)
    picture = "\n".join([
        '<picture>',
        f'  <source media="(prefers-color-scheme: dark)" srcset="{source}-dark.svg">',
        f'  <source media="(prefers-color-scheme: light)" srcset="{source}-light.svg">',
        f'  <img src="{source}-light.svg" width="{html.escape(width, quote=True)}" '
        f'alt="{html.escape(alt, quote=True)}">',
        '</picture>',
    ])
    if href:
        return f'<a href="{html.escape(href, quote=True)}">\n{picture}\n</a>'
    return picture


def render_banner_svg(theme):
    """The editable source is transparent; semantic color roles select the palette."""
    palette = THEMES[theme]
    root = ET.fromstring(BANNER_SOURCE.read_text())
    for node in root.iter():
        for attribute in ("fill", "stroke", "stop-color"):
            role = node.attrib.pop(f"data-{attribute}", None)
            if role:
                node.set(attribute, palette[role])
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    rendered = ET.tostring(root, encoding="unicode")
    return "\n".join(line.rstrip() for line in rendered.splitlines()) + "\n"


def icon_group(key, color, transform=""):
    return (
        f'<g fill="none" stroke="{color}" color="{color}" stroke-width="3" '
        f'stroke-linecap="square" stroke-linejoin="miter" transform="{transform}">'
        f'{ICONS[key]}</g>'
    )


def render_icon_svg(key):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64" '
        'aria-hidden="true">' + icon_group(key, ICON_COLOR) + '</svg>\n'
    )


def render_heading_svg(key, theme):
    label, icon = HEADINGS[key]
    text_width, baseline = HEADING_METRICS[key]
    palette = THEMES[theme]
    width = heading_width(key)
    combined = HEADING_ICON_SIZE + HEADING_GAP + text_width
    start, center = (width - combined) / 2, HEADING_HEIGHT / 2
    text_x = start + HEADING_ICON_SIZE + HEADING_GAP
    transform = f"translate({start:.1f} {center - HEADING_ICON_SIZE / 2:.1f}) scale({HEADING_ICON_SIZE / 64})"
    return "\n".join([
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{HEADING_HEIGHT}" viewBox="0 0 {width} {HEADING_HEIGHT}" '
        'role="img" aria-labelledby="title desc">',
        f'<title id="title">{html.escape(label)}</title>',
        '<desc id="desc">Original PK/circuit chapter banner with the logo and title aligned together.</desc>',
        f'<path d="M{start - 12:.1f} {center - 4}v8M{start + combined + 12:.1f} {center - 4}v8" '
        f'stroke="{palette["accent"]}" stroke-width="1.75" opacity=".6"/>',
        icon_group(icon, palette["accent"], transform),
        f'<text x="{text_x:.1f}" y="{baseline:.1f}" fill="{palette["text"]}" '
        f'font-family="Noto Sans, Arial, sans-serif" font-size="30" font-weight="700" '
        f'textLength="{text_width:.1f}" lengthAdjust="spacingAndGlyphs">{html.escape(label)}</text>',
        '</svg>',
    ]) + "\n"


def update_visuals(root):
    """Regenerate all static art without API/font access; leave brand logos alone."""
    rendered = {f"control-room-{theme}.svg": render_banner_svg(theme) for theme in THEMES}
    rendered.update({f"icons/{key}.svg": render_icon_svg(key) for key in ICONS})
    rendered.update({f"headings/{key}-{theme}.svg": render_heading_svg(key, theme)
                     for key in HEADINGS for theme in THEMES})
    for name, svg in rendered.items():
        path = root / ASSETS / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(svg)
    for folder in ("icons", "headings"):
        for path in (root / ASSETS / folder).glob("*.svg"):
            if f"{folder}/{path.name}" not in rendered:
                path.unlink()
    (root / ASSETS / "control-room.svg").unlink(missing_ok=True)
