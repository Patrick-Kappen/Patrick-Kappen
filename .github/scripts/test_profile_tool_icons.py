"""Original themed tool artwork and authored radar focus, without website-logo edits."""

import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

import profile_tool_icons as icons
import update_readme as profile

NS = "{http://www.w3.org/2000/svg}"


class ToolIconTests(unittest.TestCase):
    def test_all_twenty_five_have_safe_transparent_light_and_dark_artwork(self):
        self.assertEqual(len(icons.TOOL_ICONS), 25)
        for key, (name, _) in icons.TOOL_ICONS.items():
            captions = []
            for theme in icons.THEMES:
                svg = icons.render_tool_svg(key, theme)
                root = ET.fromstring(svg)
                self.assertEqual(root.get("viewBox"), "0 0 140 104")
                self.assertEqual(root.find(NS + "title").text, name)
                self.assertIn("not an official brand logo", root.find(NS + "desc").text)
                group = root.find(NS + "g")
                self.assertEqual(group.get("fill"), "none")
                self.assertEqual(group.get("stroke-width"), "3")
                self.assertEqual(group.get("stroke-linecap"), "square")
                self.assertEqual(group.get("stroke"), icons.THEMES[theme]["accent"])
                self.assertIsNone(root.find(NS + "rect"))
                self.assertFalse(list(root.iter(NS + "script")))
                self.assertFalse(list(root.iter(NS + "foreignObject")))
                self.assertFalse(list(root.iter(NS + "image")))
                self.assertNotIn("href=", svg)
                captions.append(root.find(NS + "text").text)
            self.assertEqual(captions, [name, name])

    def test_priority_missing_icons_and_original_raster_litellm_are_covered(self):
        for key in ("entra-id", "home-manager", "sops", "llama-cpp", "codex", "pi", "pig", "litellm"):
            self.assertIn(key, icons.TOOL_ICONS)

    def test_rendering_is_idempotent_cleans_only_owned_folder_and_preserves_website_logos(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            website = root / "public/assets/logos/azure.svg"
            website.parent.mkdir(parents=True)
            website.write_text("Original blue brand logo")
            folder = root / icons.TOOL_STEM
            folder.mkdir(parents=True)
            (folder / "obsolete.svg").write_text("Old generated icon")
            (folder / "README.md").write_text("Keep documentation")
            icons.update_tool_icons(root)
            first = {path.name: path.read_text() for path in folder.glob("*.svg")}
            icons.update_tool_icons(root)
            self.assertEqual(first, {path.name: path.read_text() for path in folder.glob("*.svg")})
            self.assertEqual(len(first), 50)
            self.assertEqual(website.read_text(), "Original blue brand logo")
            self.assertEqual((folder / "README.md").read_text(), "Keep documentation")

    def test_failed_render_cannot_publish_a_partly_updated_theme_set(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / icons.TOOL_STEM
            folder.mkdir(parents=True)
            for theme in icons.THEMES:
                (folder / f"azure-{theme}.svg").write_text("Last good artwork")
            with patch.object(icons, "render_tool_svg", side_effect=["New dark", ValueError("bad light")]):
                with self.assertRaises(ValueError):
                    icons.update_tool_icons(root)
            self.assertTrue(all(path.read_text() == "Last good artwork" for path in folder.glob("*.svg")))

    def test_profile_shows_every_highlight_and_profile_extra_with_no_ten_icon_limit(self):
        keys = list(icons.TOOL_ICONS)
        tools = [{"id": key, "name": icons.TOOL_ICONS[key][0], "group": "cloud",
                  **({"highlight": index + 1} if index < 18 else {})}
                 for index, key in enumerate(keys)]
        data = {
            "site.yaml": {"certifications": [], "studying": [], "profileToolExtras": keys[18:] + [keys[0]]},
            "tool-groups.yaml": [{"id": "cloud", "order": 1, "title": "Cloud"}],
            "tools.yaml": tools,
        }
        with patch.object(profile, "load", side_effect=lambda _, name: data[name]):
            result = profile.render_site(Path("unused"))
        self.assertEqual(result.count('width="140"'), 25)
        self.assertNotIn('src="public/assets/logos/', result)
        for key in keys:
            for theme in icons.THEMES:
                self.assertIn(f'{icons.TOOL_STEM}/{key}-{theme}.svg', result)

    def test_unknown_profile_extra_fails_instead_of_silently_publishing_a_broken_icon(self):
        data = {"site.yaml": {"profileToolExtras": ["missing"]}, "tool-groups.yaml": [], "tools.yaml": []}
        with patch.object(profile, "load", side_effect=lambda _, name: data[name]):
            with self.assertRaisesRegex(ValueError, "Unknown profile tool"):
                profile.render_site(Path("unused"))

    def test_radar_uses_authored_categories_and_legacy_strings_still_work(self):
        for name in ("Learning", "Building", "Writing", "Exploring"):
            result = profile.focus_entry(f"{name}: A real authored priority & useful context.")
            self.assertIn(f"**{name}**", result)
            self.assertIn('width="24" height="24"', result)
            self.assertIn('alt=""', result)
            self.assertIn("&amp;", result)
        self.assertEqual(profile.focus_entry("A plain authored priority"), "- A plain authored priority")
        self.assertEqual(profile.focus_entry("Other: No invented category"), "- Other: No invented category")


if __name__ == "__main__":
    unittest.main()
