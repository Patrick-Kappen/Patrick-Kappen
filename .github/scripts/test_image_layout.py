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
    def assert_canvas(self, source, height):
        root = ET.fromstring(source)
        self.assertEqual(root.get("width"), "100%")
        self.assertEqual(root.get("height"), str(height))
        self.assertNotIn("viewBox", root.attrib)
        for key in ("title", "desc"):
            self.assertIsNotNone(root.find(NS + key))
            self.assertEqual(sum(node.get("id") == key for node in root.iter()), 1)
        return root

    def assert_contained(self, source, height, viewbox):
        root = self.assert_canvas(source, height)
        inner = root.find(NS + "svg")
        self.assertIsNotNone(inner)
        self.assertEqual(inner.get("width"), "100%")
        self.assertEqual(inner.get("height"), "100%")
        self.assertEqual(inner.get("viewBox"), viewbox)
        self.assertEqual(inner.get("preserveAspectRatio"), "xMidYMid meet")
        self.assertNotIn("role", inner.attrib)
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
        for compact, height in ((False, 450), (True, 400)):
            for theme in visuals.THEMES:
                svg = visuals.render_banner_svg(theme, compact)
                root = self.assert_canvas(svg, height)
                text.append([node.text for node in root.iter(NS + "text")])
        self.assertTrue(all(value == text[0] for value in text))

    def test_telemetry_caps_preserve_all_figures_in_every_variant(self):
        today = date(2026, 11, 13)
        days = [(today - timedelta(days=364 - index), 1) for index in range(365)]
        metrics = {period: {key: period for key, _ in activity.METRICS} for _, period in activity.PERIODS}
        text = []
        self.assertEqual(len(activity.ACTIVITY_VARIANTS), 4)
        for (theme, compact), _ in activity.ACTIVITY_VARIANTS.items():
            height = 560 if compact else 760
            root = self.assert_canvas(activity.render_activity_svg(days, metrics, theme, compact), height)
            self.assertTrue(all("viewBox" not in node.attrib for node in root.iter(NS + "svg")))
            counters = [node for node in root.iter(NS + "svg") if node.get("class") == "counter"]
            self.assertEqual([node.get("x") for node in counters],
                             ["0%", "50%", "0%", "50%"] if compact else ["0%", "25%", "50%", "75%"])
            self.assertTrue(all(node.get("width") == ("50%" if compact else "25%") for node in counters))
            self.assertEqual([node.get("y") for node in counters],
                             ["0", "0", "132", "132"] if compact else ["0"] * 4)
            bars = [node for node in root.iter(NS + "rect") if node.get("class") == "month-bar"]
            self.assertEqual(len(bars), len(activity.monthly_totals(days)))
            self.assertTrue(all(node.get("x").endswith("%") and node.get("width").endswith("%") for node in bars))
            text.append([node.text for node in root.iter(NS + "text")])
        self.assertTrue(all(value == text[0] for value in text))

    def test_banner_distributes_scenes_without_enlarging_them_on_wide_screens(self):
        root = self.assert_canvas(visuals.render_banner_svg("dark"), 450)
        columns = root.findall(NS + "svg")
        self.assertEqual([node.get("class") for node in columns],
                         ["banner-copy", "banner-rack", "banner-intern"])
        self.assertEqual([node.get("x") for node in columns], ["0%", "50%", "70%"])
        self.assertEqual([node.get("width") for node in columns], ["50%", "20%", "30%"])
        for width in (1920, 2560, 3840):
            for node in columns:
                _, _, logical_width, logical_height = map(float, node.get("viewBox").split())
                available = width * float(node.get("width").rstrip("%")) / 100
                self.assertEqual(min(available / logical_width, 450 / logical_height), 450 / 440)

    def test_monthly_bars_expand_horizontally_while_height_and_font_sizes_stay_fixed(self):
        days = [(date(2026, 1, 1), 10), (date(2026, 2, 1), 20)]
        metrics = {period: {key: period for key, _ in activity.METRICS} for _, period in activity.PERIODS}
        root = self.assert_canvas(activity.render_activity_svg(days, metrics), 760)
        bars = [node for node in root.iter(NS + "rect") if node.get("class") == "month-bar"]
        self.assertEqual([node.get("x") for node in bars], ["8.000000%", "58.000000%"])
        self.assertEqual([node.get("width") for node in bars], ["34.000000%", "34.000000%"])
        heights = [float(node.get("height")) for node in bars]
        self.assertAlmostEqual(heights[1], 210 * 760 / 710, places=2)
        self.assertGreater(heights[1], 2 * 175 * 420 / 710)
        painted_widths = [width * .94 * .34 for width in (1920, 2560, 3840)]
        self.assertLess(painted_widths[0], painted_widths[1])
        self.assertEqual(painted_widths[2], painted_widths[0] * 2)
        # No SVG ancestor has a viewBox that could scale fonts or bar heights.
        self.assertTrue(all(node.get("viewBox") is None for node in root.iter(NS + "svg")))

    def test_banner_artwork_grows_at_the_actual_github_column_width(self):
        root = ET.fromstring(visuals.render_banner_svg("dark"))
        old_widths = (600, 260, 364)
        for column, old_width in zip(root.findall(NS + "svg"), old_widths):
            available = 838 * float(column.get("width").rstrip("%")) / 100
            _, _, logical_width, logical_height = map(float, column.get("viewBox").split())
            old_scale = min(available / old_width, 240 / 440)
            new_scale = min(available / logical_width, 450 / logical_height)
            self.assertGreater(new_scale, old_scale * 1.35)

    def test_phone_banner_stacks_and_telemetry_uses_readable_two_column_counters(self):
        root = self.assert_canvas(visuals.render_banner_svg("dark", compact=True), 400)
        columns = root.findall(NS + "svg")
        self.assertEqual([node.get("y") for node in columns], ["0%", "55%", "55%"])
        self.assertEqual([node.get("height") for node in columns], ["55%", "45%", "45%"])
        days = [(date(2026, 1, 1), 10), (date(2026, 2, 1), 20)]
        metrics = {period: {key: period for key, _ in activity.METRICS} for _, period in activity.PERIODS}
        root = self.assert_canvas(activity.render_activity_svg(days, metrics, compact=True), 560)
        main = next(node for node in root.iter(NS + "text") if node.text == "30")
        self.assertGreaterEqual(float(main.get("font-size")), 28)
        self.assertLess(float(list(root.iter(NS + "text"))[-1].get("y")), 560)

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
        parser.feed(visuals.themed_picture(".github/assets/project-1", "Project", width="390"))
        self.assertEqual(len(parser.sources), 2)
        self.assertEqual(parser.images[0]["width"], "390")


if __name__ == "__main__":
    unittest.main()
