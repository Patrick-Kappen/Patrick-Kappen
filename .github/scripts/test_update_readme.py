"""Offline checks for the GitHub profile layout and its generated sections."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import update_readme as profile


def entry(repo, day, title="A useful change"):
    return {
        "repo": repo,
        "when": f"2026-10-{day:02d}T12:00:00Z",
        "icon": "✨",
        "title": title,
        "url": f"https://github.com/{repo}/pull/1",
    }


class ProfileTests(unittest.TestCase):
    def test_activity_is_recent_compact_and_varied(self):
        pulls = [
            entry("Patrick-Kappen/graft", 2),
            entry("Azure/vault", 5),
            entry("Patrick-Kappen/provider", 3),
            entry("Other/project", 1),
        ]
        with patch.object(profile, "merged_pull_requests", return_value=pulls), patch.object(
            profile, "releases", return_value=[entry("Patrick-Kappen/graft", 6, "v1.0")]
        ):
            lines = profile.shipped()
        self.assertEqual(len(lines), 3)
        self.assertIn("[v1.0]", lines[0])
        self.assertIn("<sub>graft ·", lines[0])
        self.assertIn("<sub>Azure/vault ·", lines[1])
        self.assertIn("<sub>provider ·", lines[2])
        self.assertEqual(sum("<sub>graft ·" in line for line in lines), 1)
        self.assertTrue(all("<br><sub>" in line for line in lines))

    def test_pull_collection_skips_duplicate_repositories(self):
        items = [
            {
                "title": "fix: test change",
                "repository_url": f"{profile.API}/repos/{repo}",
                "number": number,
                "closed_at": f"2026-10-{4 - number:02d}T00:00:00Z",
                "html_url": f"https://github.com/{repo}/pull/{number}",
            }
            for number, repo in enumerate(
                ["Patrick-Kappen/graft", "Patrick-Kappen/graft", "Azure/vault"], 1
            )
        ]
        with patch.object(profile, "api", return_value={"items": items}) as api:
            pulls = profile.merged_pull_requests()
        self.assertEqual(len(pulls), 2)
        self.assertEqual(api.call_count, 1)

    def test_meaningful_nonconventional_prs_are_not_lost(self):
        items = [
            {"title": title, "repository_url": f"{profile.API}/repos/Other/{name}",
             "closed_at": "2026-11-13T00:00:00Z", "html_url": f"https://github.com/Other/{name}/pull/1"}
            for title, name in [("sdk: improve argument handling", "sdk"),
                                ("ci: sync branches", "ci"), ("sync: upstream changes", "sync")]
        ]
        with patch.object(profile, "api", return_value={"items": items}):
            result = profile.merged_pull_requests()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["repo"], "Other/sdk")
        self.assertEqual(result[0]["icon"], "🔧")

    def test_pr_selection_uses_merge_date_not_search_update_order(self):
        items = [
            {"title": title, "repository_url": f"{profile.API}/repos/Other/project",
             "closed_at": date, "html_url": "https://github.com/Other/project/pull/1"}
            for title, date in [("fix: older PR with a new comment", "2026-10-01T00:00:00Z"),
                                ("fix: genuinely newer merge", "2026-11-13T00:00:00Z")]
        ]
        with patch.object(profile, "api", return_value={"items": items}):
            result = profile.merged_pull_requests()
        self.assertEqual(result[0]["title"], "Genuinely newer merge")

    def test_tool_logos_are_local_limited_and_html_escaped(self):
        tools = [
            {"name": 'Tool "A&B"', "group": "cloud", "highlight": i,
             "logo": f"/assets/logos/tool-{i}.svg"}
            for i in range(12)
        ]
        tools.append({"name": "External", "group": "cloud", "highlight": 13,
                      "logo": "https://example.com/tracker.svg"})
        data = {
            "site.yaml": {"certifications": ["AZ-400"], "studying": ["GitHub Actions"]},
            "tool-groups.yaml": [{"id": "cloud", "order": 1, "title": "Cloud"}],
            "tools.yaml": tools,
        }
        with patch.object(profile, "load", side_effect=lambda _, name: data[name]):
            result = profile.render_site(Path("unused"))
        self.assertEqual(result.count('src="public/assets/logos/'), profile.TOOL_LOGO_LIMIT)
        self.assertIn('src="public/assets/logos/tool-0.svg"', result)
        self.assertIn('alt="Tool &quot;A&amp;B&quot;"', result)
        self.assertNotIn("tracker.svg", result)
        self.assertIn("<details>", result)
        self.assertIn(profile.TOOLS_INTRO, result.split("<details>")[0])
        self.assertIn("AZ-400", result)
        self.assertIn("</details>", result)

    def test_writing_only_shows_published_posts_newest_first(self):
        with tempfile.TemporaryDirectory() as directory:
            content = Path(directory)
            (content / "posts").mkdir()
            for slug, kind, status, day in [
                ("older", "post", "published", 1),
                ("newer", "post", "published", 2),
                ("secret-draft", "post", "draft", 3),
                ("work-item", "work", "published", 4),
            ]:
                (content / "posts" / f"{slug}.md").write_text(
                    f"---\ntitle: {slug}\nkind: {kind}\nstatus: {status}\n"
                    f"date: 2026-10-{day:02d}\n---\nBody\n"
                )
            result = profile.writing(content)
        self.assertEqual(len(result), 2)
        self.assertIn("newer", result[0])
        self.assertIn("older", result[1])

    def test_article_summaries_are_live_optional_and_html_escaped(self):
        with tempfile.TemporaryDirectory() as directory:
            content = Path(directory)
            posts = content / "posts"
            posts.mkdir()
            front = "---\ntitle: Visible\nkind: post\nstatus: published\ndate: 2026-10-02\n"
            article = posts / "visible.md"
            article.write_text(front + 'description: "A <tag> & extra details."\n---\nBody')
            (posts / "older.md").write_text(
                "---\ntitle: Older\nkind: post\nstatus: published\ndate: 2026-10-01\n---\nBody")
            (posts / "secret.md").write_text(
                "---\ntitle: Secret\nkind: post\nstatus: draft\ndate: 2026-10-03\n"
                "description: Never publish this\n---\nBody")
            result = profile.writing(content)
            self.assertEqual(len(result), 2)
            self.assertIn("<br>\n  A &lt;tag&gt; &amp; extra details.", result[0])
            self.assertNotIn("<br>", result[1])
            self.assertNotIn("Never publish", "\n".join(result))
            article.write_text(front + "description: Updated summary\n---\nBody")
            self.assertIn("Updated summary", profile.writing(content)[0])

    def test_narrative_survives_generated_sections_and_empty_writing_stays_hidden(self):
        now = {"updated": "2026-10-02", "now": []}
        with patch.object(profile, "writing", return_value=["- A published article"]):
            rendered = profile.render(now, Path("unused"), work=[])
        self.assertIn(profile.WRITING_INTRO, rendered)
        with patch.object(profile, "writing", return_value=[]):
            rendered = profile.render(now, Path("unused"), work=[])
        self.assertNotIn(profile.WRITING_INTRO, rendered)

    def test_empty_sections_and_github_failure_are_safe(self):
        now = {"updated": "2026-10-02", "now": ["Testing restores"]}
        with patch.object(profile, "writing", return_value=[]), patch.object(
            profile, "shipped", side_effect=OSError("offline")
        ), contextlib.redirect_stderr(io.StringIO()):
            result = profile.render(now, Path("unused"))
        self.assertIn("Testing restores", result)
        self.assertNotIn("rabbit hole", result)
        self.assertNotIn("Git log", result)

    def test_recent_work_fallback_survives_heading_changes(self):
        work = ["- A real shipped change"]
        now = {"updated": "2026-11-13", "now": []}
        with patch.object(profile, "writing", return_value=[]):
            rendered = profile.render(now, Path("unused"), work=work)
        self.assertEqual(profile.previous_work(rendered), work)
        self.assertEqual(profile.previous_work("### 🚢 Recently shipped\n\n- Older change\n\n## Next"), ["- Older change"])

    def test_generated_blocks_preserve_surroundings_and_are_idempotent(self):
        original = f"Illustration\n{profile.START}\nOld\n{profile.END}\nHouse rules"
        rendered = profile.replace_block(
            original, profile.START, profile.END, "New", "README.md"
        )
        self.assertTrue(rendered.startswith("Illustration\n"))
        self.assertTrue(rendered.endswith("\nHouse rules"))
        self.assertEqual(rendered, profile.replace_block(
            rendered, profile.START, profile.END, "New", "README.md"
        ))
        with self.assertRaises(SystemExit):
            profile.replace_block("No markers", profile.START, profile.END, "New", "README.md")


if __name__ == "__main__":
    unittest.main()
