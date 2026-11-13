"""Intrinsic-height SVGs must stay fluid without zooming or cropping artwork."""

import unittest
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from html.parser import HTMLParser

import profile_activity as activity
import profile_visuals as visuals

NS = "{http://www.w3.org/2000/svg}"


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources, self.images = [], []

    def handle_starttag(self, tag, attributes):
        if tag == "source":
            self.sources.append(dict(attributes))
        if tag == "img":
            self.images.append(dict(attributes))


class ImageLayoutTests(unittest.TestCase):
    def assert_contained(self, source, height, viewbox):
        root = ET.fromstring(source)
        self.assertEqual(root.get("width"), "100%")
        self.assertEqual(root.get("height"), str(height))
        self.assertNotIn("viewBox", root.attrib)  # No intrinsic ratio that grows the outer height.
        inner = root.find(NS + "svg")
        self.assertIsNotNone(inner)
        self.assertEqual(inner.get("width"), "100%")
        self.assertEqual(inner.get("height"), "100%")
        self.assertEqual(inner.get("viewBox"), viewbox)
        self.assertEqual(inner.get("preserveAspectRatio"), "xMidYMid meet")
        self.assertNotIn("role", inner.attrib)
        for key in ("title", "desc"):
            self.assertIsNotNone(root.find(NS + key))
            self.assertEqual(sum(node.get("id") == key for node in root.iter()), 1)
        return root

    def test_wrapper_preserves_artwork_and_accessibility(self):
        source = (f'<svg xmlns="{NS[1:-1]}" width="100" height="50" viewBox="0 0 100 50" '
                  'role="img" aria-labelledby="title desc"><title id="title">Title</title>'
                  '<desc id="desc">Description</desc><text x="20" y="30">Unchanged</text></svg>')
        root = self.assert_contained(visuals.contain_svg(source, 40), 40, "0 0 100 50")
        text = root.find(NS + "svg").find(NS + "text")
        self.assertEqual((text.get("x"), text.get("y"), text.text), ("20", "30", "Unchanged"))

    def test_wrapper_rejects_invalid_height_and_missing_original_viewbox(self):
        source = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50"/>'
        for height in (0, -1, True, 1.5, "240"):
            with self.subTest(height=height), self.assertRaises(ValueError):
                visuals.contain_svg(source, height)
        with self.assertRaises(ValueError):
            visuals.contain_svg('<svg xmlns="http://www.w3.org/2000/svg"/>', 240)

    def test_banner_desktop_and_compact_caps_keep_the_same_content(self):
        text = []
        for compact, height in ((False, 240), (True, 160)):
            for theme in visuals.THEMES:
                root = self.assert_contained(visuals.render_banner_svg(theme, compact), height, "0 0 1200 440")
                text.append([node.text for node in root.iter(NS + "text")])
        self.assertTrue(all(value == text[0] for value in text))

    def test_telemetry_caps_preserve_all_figures_in_every_variant(self):
        today = date(2026, 11, 13)
        days = [(today - timedelta(days=364 - index), 1) for index in range(365)]
        metrics = {period: {key: period for key, _ in activity.METRICS} for _, period in activity.PERIODS}
        text = []
        self.assertEqual(len(activity.ACTIVITY_VARIANTS), 4)
        for (theme, compact), _ in activity.ACTIVITY_VARIANTS.items():
            height = 220 if compact else 420
            root = self.assert_contained(activity.render_activity_svg(days, metrics, theme, compact),
                                         height, "0 0 1200 710")
            text.append([node.text for node in root.iter(NS + "text")])
        self.assertTrue(all(value == text[0] for value in text))

    def test_compact_sources_precede_desktop_and_control_their_own_height(self):
        for stem in visuals.CONTAINED_IMAGES:
            parser = Images()
            parser.feed(visuals.themed_picture(stem, "Description"))
            self.assertEqual(len(parser.sources), 4)
            for index, theme in enumerate(visuals.THEMES):
                compact = parser.sources[index]
                self.assertIn("max-width: 600px", compact["media"])
                self.assertIn(f"prefers-color-scheme: {theme}", compact["media"])
                self.assertEqual(compact["srcset"], f"{stem}-compact-{theme}.svg")
            self.assertEqual(parser.images[0]["width"], "100%")
            # A fixed HTML height would override the selected compact SVG's smaller height.
            self.assertNotIn("height", parser.images[0])
            self.assertNotIn("style", parser.images[0])

    def test_other_images_keep_their_existing_numeric_size_limits(self):
        for key in visuals.HEADINGS:
            parser = Images()
            parser.feed(visuals.section_heading(key))
            self.assertEqual(len(parser.sources), 2)
            self.assertLessEqual(int(parser.images[0]["width"]), 560)
        parser = Images()
        parser.feed(visuals.themed_picture(".github/assets/project-1", "Project", width="270"))
        self.assertEqual(len(parser.sources), 2)
        self.assertEqual(parser.images[0]["width"], "270")


if __name__ == "__main__":
    unittest.main()
