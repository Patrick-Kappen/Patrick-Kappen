"""Shared transparent artwork, SVG section banners and regeneration checks."""

import re
import tempfile
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

import profile_activity as activity
import profile_projects as projects
import profile_visuals as visuals

NS = "{http://www.w3.org/2000/svg}"


def contrast(first, second):
    def luminance(color):
        channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
        channels = [value / 12.92 if value <= .04045 else ((value + .055) / 1.055) ** 2.4 for value in channels]
        return sum(value * weight for value, weight in zip(channels, (.2126, .7152, .0722)))
    a, b = luminance(first), luminance(second)
    return (max(a, b) + .05) / (min(a, b) + .05)


class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags, self.text = [], []

    def handle_starttag(self, tag, attributes):
        self.tags.append((tag, dict(attributes)))

    def handle_data(self, text):
        self.text.append(text)


class VisualTests(unittest.TestCase):
    def test_headings_use_one_picture_for_logo_and_title(self):
        for key, (label, _) in visuals.HEADINGS.items():
            level = 1 if key == "intro" else 2
            markup = Markup()
            markup.feed(visuals.section_heading(key, level))
            self.assertEqual(markup.tags[0], ("p", {"align": "center", "id": key}))
            self.assertEqual("".join(markup.text).strip(), "")
            images = [attributes for tag, attributes in markup.tags if tag == "img"]
            self.assertEqual(len(images), 1)
            self.assertEqual(images[0]["alt"], label)
            self.assertEqual(images[0]["src"], f".github/assets/headings/{key}-light.svg")
            sources = [attributes for tag, attributes in markup.tags if tag == "source"]
            self.assertEqual(len(sources), 2)
            self.assertEqual(sources[0]["srcset"], f".github/assets/headings/{key}-dark.svg")

    def test_committed_readme_references_existing_images_with_correct_heading_alt_text(self):
        root = Path(visuals.__file__).resolve().parents[2]
        markup = Markup()
        markup.feed((root / "README.md").read_text())
        for tag, attributes in markup.tags:
            if tag not in ("img", "source"):
                continue
            source = attributes.get("src") or attributes.get("srcset")
            self.assertTrue((root / source).is_file(), source)
            if tag == "img":
                self.assertIn("alt", attributes)
                if source.startswith(".github/assets/headings/"):
                    key = Path(source).name.removesuffix("-light.svg")
                    self.assertEqual(attributes["alt"], visuals.HEADINGS[key][0])

    def test_section_titles_and_footer_have_no_separator_markup(self):
        root = Path(visuals.__file__).resolve().parents[2]
        readme = (root / "README.md").read_text()
        self.assertNotRegex(readme, r"<h[12]\b")
        self.assertNotRegex(readme, r"(?m)^---\s*$")
        self.assertNotIn("<hr", readme)
        for key in visuals.HEADINGS:
            for level in (1, 2, 3):
                markup = visuals.section_heading(key, level)
                self.assertNotRegex(markup, r"<h[123]\b")

    def test_section_banners_match_the_approved_weight_and_spacing(self):
        self.assertEqual(set(visuals.HEADINGS), set(visuals.HEADING_METRICS))
        for key, (label, _) in visuals.HEADINGS.items():
            for theme in visuals.THEMES:
                root = ET.fromstring(visuals.render_heading_svg(key, theme))
                self.assertEqual(root.get("height"), "144")
                self.assertEqual(root.find(NS + "title").text, label)
                self.assertIsNone(root.find(NS + "rect"))
                text = root.find(NS + "text")
                self.assertEqual(text.text, label)
                self.assertEqual(text.get("font-weight"), "700")
                group = root.find(NS + "g")
                self.assertEqual(group.get("stroke-width"), "3")
                self.assertEqual(group.get("stroke-linecap"), "square")
                self.assertFalse(any(node.get("stroke") == visuals.THEMES[theme]["line"] for node in root.iter()))
                values = re.fullmatch(r"translate\(([-\d.]+) ([-\d.]+)\) scale\(([-\d.]+)\)", group.get("transform"))
                self.assertIsNotNone(values)
                left, _, scale = map(float, values.groups())
                self.assertEqual(scale * 64, 56)
                self.assertEqual(float(text.get("x")) - left - 56, 28)
                right = float(text.get("x")) + float(text.get("textLength"))
                self.assertAlmostEqual(left, float(root.get("width")) - right)
                self.assertGreaterEqual(left - 12, 12)
                self.assertFalse(list(root.iter(NS + "script")))
                self.assertFalse(list(root.iter(NS + "foreignObject")))

    def test_section_banner_text_and_geometry_are_identical_across_themes(self):
        for key in visuals.HEADINGS:
            dark = ET.fromstring(visuals.render_heading_svg(key, "dark"))
            light = ET.fromstring(visuals.render_heading_svg(key, "light"))
            for attribute in ("width", "height", "viewBox"):
                self.assertEqual(dark.get(attribute), light.get(attribute))
            self.assertEqual(dark.find(NS + "text").text, light.find(NS + "text").text)
            self.assertEqual(dark.find(NS + "g").get("transform"), light.find(NS + "g").get("transform"))
            for root, background in ((dark, "#0d1117"), (light, "#ffffff")):
                text = root.find(NS + "text")
                self.assertGreaterEqual(contrast(text.get("fill"), background), 4.5)

    def test_unsupported_heading_level_is_rejected(self):
        with self.assertRaises(ValueError):
            visuals.section_heading("intro", 9)

    def test_pictures_use_both_themes_and_escape_alt_and_link_attributes(self):
        markup = visuals.themed_picture(".github/assets/test", 'A <tag> & "quote"',
                                        href='https://github.com/test/repo?q="x"')
        parser = Markup()
        parser.feed(markup)
        self.assertEqual([tag for tag, _ in parser.tags], ["a", "picture", "source", "source", "img"])
        sources = [attributes for tag, attributes in parser.tags if tag == "source"]
        self.assertEqual(sources[0]["media"], "(prefers-color-scheme: dark)")
        self.assertEqual(sources[1]["srcset"], ".github/assets/test-light.svg")
        self.assertNotIn("<tag>", markup)
        image = parser.tags[-1][1]
        self.assertEqual(image["alt"], 'A <tag> & "quote"')
        self.assertEqual(image["width"], "100%")

    def test_banner_has_no_canvas_or_opaque_device_panels(self):
        visible = []
        for theme in visuals.THEMES:
            svg = visuals.render_banner_svg(theme)
            root = ET.fromstring(svg)
            self.assertFalse(any(rect.get("width") == "1200" for rect in root.iter(NS + "rect")))
            self.assertNotIn("data-fill", svg)
            self.assertNotIn("data-stroke", svg)
            self.assertNotIn("data-stop-color", svg)
            for rect in root.iter(NS + "rect"):
                if rect.get("width") == "54":  # The little orange AI badge, not a background.
                    continue
                self.assertEqual(rect.get("fill"), "none")
            visible.append([node.text for node in root.iter(NS + "text")])
            self.assertFalse(list(root.iter(NS + "script")))
            self.assertFalse(list(root.iter(NS + "foreignObject")))
        self.assertEqual(visible[0], visible[1])

    def test_banner_text_is_readable_in_both_themes(self):
        for theme, background in [("dark", "#0d1117"), ("light", "#ffffff")]:
            palette = visuals.THEMES[theme]
            root = ET.fromstring(visuals.render_banner_svg(theme))
            parents = {child: parent for parent in root.iter() for child in parent}
            for node in root.iter(NS + "text"):
                ancestor, fill = node, node.get("fill")
                while fill is None and ancestor in parents:
                    ancestor = parents[ancestor]
                    fill = ancestor.get("fill")
                colors = [palette["accent"], palette["label"]] if fill.startswith("url(") else [fill]
                surface = palette["label"] if node.text == "AI" else background
                for color in colors:
                    self.assertGreaterEqual(contrast(color, surface), 4.5, (theme, node.text, color))

    def test_icons_are_transparent_safe_and_visible_in_both_themes(self):
        for key in visuals.ICONS:
            root = ET.fromstring(visuals.render_icon_svg(key))
            self.assertEqual(root.get("viewBox"), "0 0 64 64")
            self.assertEqual(root.find(NS + "g").get("stroke-width"), "3")
            for rect in root.iter(NS + "rect"):
                self.assertLessEqual(float(rect.get("width")), 10)
            self.assertFalse(list(root.iter(NS + "script")))
            self.assertFalse(list(root.iter(NS + "foreignObject")))
        for background in ("#0d1117", "#ffffff"):
            self.assertGreaterEqual(contrast(visuals.ICON_COLOR, background), 3)

    def test_visual_refresh_is_idempotent_and_removes_only_legacy_banner(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            assets = root / visuals.ASSETS
            assets.mkdir(parents=True)
            (assets / "control-room.svg").write_text("Old background")
            (assets / "unrelated.svg").write_text("Keep this")
            visuals.update_visuals(root)
            first = {path.relative_to(assets): path.read_text() for path in assets.rglob("*.svg")}
            visuals.update_visuals(root)
            second = {path.relative_to(assets): path.read_text() for path in assets.rglob("*.svg")}
            self.assertEqual(first, second)
            self.assertFalse((assets / "control-room.svg").exists())
            self.assertEqual((assets / "unrelated.svg").read_text(), "Keep this")
            for key in visuals.ICONS:
                ET.parse(assets / "icons" / f"{key}.svg")
            for theme in visuals.THEMES:
                ET.parse(assets / f"control-room-{theme}.svg")
                for key in visuals.HEADINGS:
                    ET.parse(assets / "headings" / f"{key}-{theme}.svg")

    def test_failed_banner_render_preserves_both_previous_variants(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            assets = root / visuals.ASSETS
            assets.mkdir(parents=True)
            for theme in visuals.THEMES:
                (assets / f"control-room-{theme}.svg").write_text("Last good banner")
            with patch.object(visuals, "render_banner_svg", side_effect=["New dark", ValueError("bad light")]):
                with self.assertRaises(ValueError):
                    visuals.update_visuals(root)
            for theme in visuals.THEMES:
                self.assertEqual((assets / f"control-room-{theme}.svg").read_text(), "Last good banner")

    def test_project_cards_share_the_palette_and_are_transparent(self):
        project = {
            "repo": {"full_name": "Owner/project", "description": "Live project description", "fork": True},
            "activity": {"when": "2026-11-13T08:00:00Z", "state": "open", "title": "Current work",
                         "url": "https://github.com/Owner/project/pull/1"},
        }
        visible = []
        self.assertIs(activity.THEMES, visuals.THEMES)
        for theme, background in [("dark", "#0d1117"), ("light", "#ffffff")]:
            root = ET.fromstring(projects.render_project_svg(project, 1, theme))
            self.assertFalse(list(root.iter(NS + "rect")))
            visible.append([node.text for node in root.iter(NS + "text")])
            for node in root.iter(NS + "text"):
                self.assertGreaterEqual(contrast(node.get("fill"), background), 4.5)
        self.assertEqual(visible[0], visible[1])

    def test_failed_project_theme_render_cannot_publish_a_mixed_pair(self):
        project = {"full_name": "Owner/project", "description": "Project", "fork": False}
        entry = {"repo": "Owner/project", "when": "2026-11-13T08:00:00Z", "title": "Change",
                 "url": "https://github.com/Owner/project/pull/1"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            assets = root / projects.ASSETS
            assets.mkdir(parents=True)
            for theme in visuals.THEMES:
                (assets / f"project-1-{theme}.svg").write_text("Last good card")
            with patch.object(projects, "render_project_svg", side_effect=["New dark", ValueError("bad light")]):
                with self.assertRaises(ValueError):
                    projects.update_projects(root, [entry], lambda _: project, "Patrick-Kappen")
            for theme in visuals.THEMES:
                self.assertEqual((assets / f"project-1-{theme}.svg").read_text(), "Last good card")


if __name__ == "__main__":
    unittest.main()
