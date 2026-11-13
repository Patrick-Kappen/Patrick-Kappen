"""Shared palettes and self-contained transparent profile/section banners."""

import html
from math import ceil
from pathlib import Path
import xml.etree.ElementTree as ET

ASSETS = ".github/assets"
# Desktop / compact intrinsic heights; desktop content lays out across the available width.
CONTAINED_IMAGES = {
    f"{ASSETS}/control-room": (450, 400),
    f"{ASSETS}/git-activity": (760, 560),
}
COMPACT_BREAKPOINT = 600
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
# Standalone icons remain visible on both GitHub themes.
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
    "approach": ("How I build things", "rules"),
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
    "intro": (236.0, 80.0), "approach": (272.0, 80.0),
    "projects": (297.0, 80.0), "git-log": (160.0, 80.0),
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
    sources = []
    if stem in CONTAINED_IMAGES:
        sources = [
            f'  <source media="(prefers-color-scheme: {theme}) and (max-width: {COMPACT_BREAKPOINT}px)" '
            f'srcset="{source}-compact-{theme}.svg">' for theme in THEMES
        ]
    picture = "\n".join([
        '<picture>', *sources,
        f'  <source media="(prefers-color-scheme: dark)" srcset="{source}-dark.svg">',
        f'  <source media="(prefers-color-scheme: light)" srcset="{source}-light.svg">',
        f'  <img src="{source}-light.svg" width="{html.escape(width, quote=True)}" '
        f'alt="{html.escape(alt, quote=True)}">',
        '</picture>',
    ])
    if href:
        return f'<a href="{html.escape(href, quote=True)}">\n{picture}\n</a>'
    return picture


def image_height(stem, compact=False):
    return CONTAINED_IMAGES[stem][int(compact)]


def contain_svg(source, height):
    """Fluid viewport, fixed intrinsic height, no cover/crop or proportional upscaling.

    The outer SVG deliberately has a percentage width and NO viewBox, so it has
    no intrinsic aspect ratio that could make <img height=auto> grow vertically.
    Only the nested SVG has a viewBox; `meet` keeps all artwork visible.
    """
    if type(height) is not int or height <= 0:
        raise ValueError("Expected a positive canvas height")
    namespace = "{http://www.w3.org/2000/svg}"
    inner = ET.fromstring(source)
    if not inner.get("viewBox"):
        raise ValueError("Contained artwork requires an original viewBox")
    outer = ET.Element(namespace + "svg", {
        "width": "100%", "height": str(height), "role": "img",
        "aria-labelledby": inner.get("aria-labelledby", "title desc"),
    })
    for node in list(inner):
        if node.tag in (namespace + "title", namespace + "desc"):
            inner.remove(node)
            outer.append(node)
    inner.attrib.pop("role", None)
    inner.attrib.pop("aria-labelledby", None)
    inner.set("width", "100%")
    inner.set("height", "100%")
    inner.set("preserveAspectRatio", "xMidYMid meet")
    outer.append(inner)
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    rendered = ET.tostring(outer, encoding="unicode")
    return "\n".join(line.rstrip() for line in rendered.splitlines()) + "\n"


def render_banner_svg(theme, compact=False):
    """The editable source is transparent; semantic color roles select the palette."""
    palette = THEMES[theme]
    root = ET.fromstring(BANNER_SOURCE.read_text())
    for node in root.iter():
        for attribute in ("fill", "stroke", "stop-color"):
            role = node.attrib.pop(f"data-{attribute}", None)
            if role:
                node.set(attribute, palette[role])
    regions = {node.attrib.pop("data-region"): node for node in root if "data-region" in node.attrib}
    height = image_height(f"{ASSETS}/control-room", compact)
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    # Tighter scene bounds let the artwork itself grow at GitHub column widths,
    # instead of increasing only the empty canvas around a width-limited drawing.
    columns = {
        "copy": ("0%", "0%", "50%", "100%", "24 0 440 440", "xMinYMid meet"),
        "rack": ("50%", "0%", "20%", "100%", "640 0 192 440", "xMidYMid meet"),
        "intern": ("70%", "0%", "30%", "100%", "836 0 332 440", "xMaxYMid meet"),
    }
    if compact:
        # Stack the copy above the illustrations; do not shrink a desktop banner.
        columns = {
            "copy": ("0%", "0%", "100%", "55%", "24 0 440 440", "xMidYMid meet"),
            "rack": ("0%", "55%", "45%", "45%", "640 0 192 440", "xMidYMid meet"),
            "intern": ("45%", "55%", "55%", "45%", "836 0 332 440", "xMidYMid meet"),
        }
    if regions.keys() != columns.keys():
        raise ValueError("The banner must define copy, rack and intern regions")
    root.set("width", "100%")
    root.set("height", str(height))
    root.attrib.pop("viewBox")
    for key, (x, y, width, scene_height, viewbox, alignment) in columns.items():
        viewport = ET.SubElement(root, "{http://www.w3.org/2000/svg}svg", {
            "class": f"banner-{key}", "x": x, "y": y, "width": width, "height": scene_height,
            "viewBox": viewbox, "preserveAspectRatio": alignment,
            # The rack sparkles sit outside its tighter device bounds.
            "overflow": "visible" if key == "rack" else "hidden",
        })
        root.remove(regions[key])
        viewport.append(regions[key])
    return "\n".join(line.rstrip() for line in ET.tostring(root, encoding="unicode").splitlines()) + "\n"


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
    rendered = {f"control-room{'-compact' if compact else ''}-{theme}.svg": render_banner_svg(theme, compact)
                for compact in (False, True) for theme in THEMES}
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
