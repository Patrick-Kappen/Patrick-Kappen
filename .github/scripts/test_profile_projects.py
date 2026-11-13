"""Offline checks for live project selection, card layout and safe refreshes."""

import contextlib
import io
import tempfile
import unittest
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from unittest.mock import patch

import profile_projects as cards
import update_readme as profile


def entry(repo, day=10, title="A useful change"):
    return {"repo": repo, "when": f"2026-11-{day:02d}T12:00:00Z", "icon": "🔧",
            "title": title, "url": f"https://github.com/{repo}/pull/1"}


def repository(name, **kwargs):
    return {"full_name": name, "description": "The current repository description.",
            "fork": False, "private": False, "archived": False, **kwargs}


class ProjectTests(unittest.TestCase):
    def test_selection_is_recent_and_deduplicates_fork_upstream(self):
        entries = [entry("Upstream/project", 9), entry("Patrick-Kappen/project", 11),
                   entry("Other/second", 10), entry("Other/third", 8)]
        repos = {
            "Upstream/project": repository("Upstream/project"),
            "Patrick-Kappen/project": repository("Patrick-Kappen/project", fork=True,
                                                source={"full_name": "Upstream/project"}),
            "Other/second": repository("Other/second"),
            "Other/third": repository("Other/third"),
        }
        result = cards.select_projects(entries, lambda path: repos[path[6:]], profile.USER)
        self.assertEqual([item["repo"]["full_name"] for item in result],
                         ["Patrick-Kappen/project", "Other/second", "Other/third"])
        self.assertEqual(result[0]["activity"]["when"], entries[1]["when"])

    def test_private_archived_disabled_and_profile_are_not_selected(self):
        repos = {
            "Other/private": repository("Other/private", private=True),
            "Other/archived": repository("Other/archived", archived=True),
            "Other/disabled": repository("Other/disabled", disabled=True),
            "Patrick-Kappen/Patrick-Kappen": repository("Patrick-Kappen/Patrick-Kappen"),
            "Other/active": repository("Other/active"),
        }
        result = cards.select_projects([entry(name) for name in repos],
                                       lambda path: repos[path[6:]], profile.USER)
        self.assertEqual([item["repo"]["full_name"] for item in result], ["Other/active"])

    def test_repository_metadata_is_fetched_once_for_pr_and_release(self):
        entries = [entry("Other/project", 11), entry("Other/project", 10)]
        with patch.object(profile, "api", return_value=repository("Other/project")) as api:
            self.assertEqual(len(cards.select_projects(entries, api, profile.USER)), 1)
        self.assertEqual(api.call_count, 1)

    def test_card_is_rectangular_borderless_and_xml_escaped(self):
        project = {"repo": repository("Other/project", description='Tools & <ideas> "today"'),
                   "activity": entry("Other/project", title="Fix <unsafe> & awkward text")}
        svg = cards.render_project_svg(project, 1)
        root = ET.fromstring(svg)
        ns = {"svg": "http://www.w3.org/2000/svg"}
        background = root.find("svg:rect", ns)
        self.assertNotIn("rx", background.attrib)
        self.assertNotIn("stroke", background.attrib)
        self.assertIn("Tools & <ideas>", root.find("svg:desc", ns).text)
        self.assertIn("MERGED PR", svg)
        self.assertIn("10 Nov 2026", svg)
        self.assertNotIn("<unsafe>", svg)

    def test_open_work_is_current_but_never_claimed_as_shipped(self):
        activity = {**entry("Other/project", title="Work in progress"), "state": "open"}
        project = {"repo": repository("Other/project"), "activity": activity}
        svg = cards.render_project_svg(project, 1)
        self.assertIn("OPEN PR", svg)
        self.assertNotIn("MERGED PR", svg)
        self.assertEqual(profile.shipped([activity]), [])

    def test_refresh_updates_content_and_removes_obsolete_generated_cards(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            assets = root / cards.ASSETS
            assets.mkdir(parents=True)
            (assets / "project-graft.svg").write_text("Old hardcoded card")
            (assets / "control-room.svg").write_text("Keep banner")
            entries = [entry("Other/current")]
            metadata = repository("Other/current", description="Actual live description")
            body, projects = cards.update_projects(root, entries, lambda _: metadata, profile.USER, date(2026, 11, 13))
            self.assertEqual(len(projects), 1)
            self.assertIn("https://github.com/Other/current", body)
            self.assertIn("Automatically refreshed 2026-11-13", body)
            self.assertIn("Actual live description", (assets / "project-1.svg").read_text())
            self.assertFalse((assets / "project-graft.svg").exists())
            self.assertEqual((assets / "control-room.svg").read_text(), "Keep banner")
            metadata["description"] = "Updated next day"
            cards.update_projects(root, entries, lambda _: metadata, profile.USER, date(2026, 11, 14))
            self.assertIn("Updated next day", (assets / "project-1.svg").read_text())

    def test_api_failure_does_not_modify_previous_cards(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / cards.ASSETS / "project-1.svg"
            path.parent.mkdir(parents=True)
            path.write_text("Last good card")
            with patch.object(profile, "api", side_effect=[repository("Other/one"), OSError("offline")]):
                with self.assertRaises(OSError):
                    cards.update_projects(root, [entry("Other/one", 11), entry("Other/two", 10)], profile.api, profile.USER)
            self.assertEqual(path.read_text(), "Last good card")

    def test_no_activity_hides_section_instead_of_inventing_a_project(self):
        with tempfile.TemporaryDirectory() as directory:
            body, projects = cards.update_projects(Path(directory), [], lambda _: None, profile.USER)
        self.assertEqual(body, "")
        self.assertEqual(projects, [])

    def test_wrapping_limits_long_titles_without_losing_xml_safety(self):
        lines = cards.wrapped("very-long-repository-name-" * 10, 23, 2)
        self.assertEqual(len(lines), 2)
        self.assertTrue(all(len(line) <= 23 for line in lines))
        self.assertTrue(lines[-1].endswith("…"))

    def test_main_refreshes_cards_and_only_ships_merged_work(self):
        source = Path(__file__).resolve().parents[2]
        merged = entry("Other/project", 10, "Finished change")
        opened = {**entry("Other/project", 11, "Next unfinished change"), "state": "open"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text((source / "README.md").read_text())
            with patch.object(profile, "__file__", str(root / ".github/scripts/update_readme.py")), \
                 patch.object(profile, "load", return_value={"now": {"updated": "2026-11-13", "now": []}}), \
                 patch.object(profile, "update_activity", return_value=True), \
                 patch.object(profile, "merged_pull_requests", return_value=[merged]), \
                 patch.object(profile, "open_pull_requests", return_value=[opened]), \
                 patch.object(profile, "releases", return_value=[]), \
                 patch.object(profile, "api", return_value=repository("Other/project")) as api, \
                 patch.object(profile, "writing", return_value=[]), \
                 patch.object(profile, "render_site", return_value="Tools"):
                profile.main()
                before = (root / "README.md").read_text()
                profile.main()
                self.assertEqual((root / "README.md").read_text(), before)
            self.assertEqual(api.call_count, 2)  # Once per run, shared by both sections.
            svg = (root / cards.ASSETS / "project-1.svg").read_text()
            self.assertIn("Next unfinished change", svg)
            self.assertIn("OPEN PR", svg)
            self.assertIn("Finished change", before)
            self.assertNotIn("Next unfinished change", before.split("### 🚢 Recently shipped")[1])

    def test_main_keeps_project_block_and_cards_on_github_failure(self):
        source = Path(__file__).resolve().parents[2]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text((source / "README.md").read_text())
            before = (root / "README.md").read_text()
            with patch.object(profile, "__file__", str(root / ".github/scripts/update_readme.py")), \
                 patch.object(profile, "load", return_value={"now": {"updated": "2026-11-13", "now": []}}), \
                 patch.object(profile, "update_activity", return_value=True), \
                 patch.object(profile, "merged_pull_requests", side_effect=OSError("offline")), \
                 patch.object(profile, "writing", return_value=[]), \
                 patch.object(profile, "render_site", return_value="Tools"), \
                 contextlib.redirect_stderr(io.StringIO()):
                profile.main()
            after = (root / "README.md").read_text()
            project_block = lambda text: text.split(cards.PROJECT_START)[1].split(cards.PROJECT_END)[0]
            self.assertEqual(project_block(after), project_block(before))
            self.assertIn('width="100%"', after)


if __name__ == "__main__":
    unittest.main()
