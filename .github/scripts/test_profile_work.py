"""Recent public work must be varied, factual, current, safe and scheduled regularly."""

import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

import profile_work as work
import update_readme as profile


def entry(repo, number, state="merged"):
    return {"repo": repo, "title": f"Change {number}", "when": f"2026-11-{number:02d}T12:00:00Z",
            "state": state, "url": f"https://github.com/{repo}/pull/{number}"}


class WorkLogTests(unittest.TestCase):
    def test_eight_entries_with_at_most_two_per_repository(self):
        entries = [entry("Owner/busy", number) for number in range(1, 10)]
        entries += [entry(f"Owner/other-{number}", number) for number in range(1, 10)]
        selected = work.recent_entries(entries)
        self.assertEqual(len(selected), 8)
        self.assertLessEqual(sum(item["repo"] == "Owner/busy" for item in selected), 2)
        self.assertEqual([item["when"] for item in selected],
                         sorted((item["when"] for item in selected), reverse=True))

    def test_duplicates_and_open_work_never_appear_as_completed(self):
        merged = entry("Owner/project", 5)
        self.assertEqual(work.recent_entries([merged, merged, entry("Owner/project", 6, "open")]), [merged])

    def test_no_summary_is_invented_when_body_is_missing(self):
        item = entry("Owner/project", 5)
        result = work.render_work_log([item])[0]
        self.assertIn("MERGED PR #5", result)
        self.assertIn("05 Nov 2026", result)
        self.assertEqual(result.count("<br>"), 1)
        self.assertEqual(work.summary_from_body(None), "")
        self.assertEqual(work.summary_from_body(""), "")

    def test_release_is_not_labelled_as_a_merged_pr(self):
        item = {**entry("Owner/project", 5), "url": "https://github.com/Owner/project/releases/tag/v2"}
        result = work.render_work_log([item])[0]
        self.assertIn("<strong>RELEASE</strong>", result)
        self.assertNotIn("MERGED PR", result)

    def test_description_is_quoted_not_rewritten_and_unsafe_markup_is_escaped(self):
        summary = "The <input> object now retains tool_result arguments & their original order."
        item = {**entry("Owner/project", 5), "title": "Fix <unsafe> & awkward input", "summary": summary}
        result = work.render_work_log([item])[0]
        self.assertIn("Fix &lt;unsafe&gt; &amp; awkward input", result)
        self.assertIn("The &lt;input&gt; object now retains tool_result arguments &amp; their original order.", result)
        self.assertNotIn("<unsafe>", result)

    def test_summary_prefers_explicit_section_and_preserves_code_identifiers(self):
        body = ("Tracking: https://github.com/Owner/project/issues/123\n\n"
                "## Summary\n\nThe `tool_result` event now exposes `<input>` through **both** SDK readers.\n\n"
                "## Verification\n\nUnrelated verification details must not become the summary.")
        self.assertEqual(work.summary_from_body(body),
                         "The tool_result event now exposes <input> through both SDK readers.")

    def test_fences_checklists_comments_and_images_are_not_profile_content(self):
        body = ("<!-- private template instruction -->\n\n```sh\necho secret-example\n```\n\n"
                "- [ ] Checklist content is not a useful description.\n\n"
                "A real explanation of the change, with [documentation](https://example.com). "
                "![tracking image](https://example.com/pixel)\n")
        self.assertEqual(work.summary_from_body(body),
                         "A real explanation of the change, with documentation.")

    def test_long_excerpts_are_bounded_without_making_up_a_conclusion(self):
        result = work.summary_from_body("A factual explanation of this change. " * 30)
        self.assertLessEqual(len(result), 280)
        self.assertTrue(result.endswith("…"))

    def test_syncs_and_cherry_picked_duplicate_titles_do_not_crowd_out_real_work(self):
        items = [{"title": title, "repository_url": f"{profile.API}/repos/Owner/project",
                  "html_url": f"https://github.com/Owner/project/pull/{number}",
                  "closed_at": f"2026-11-{number:02d}T12:00:00Z"}
                 for number, title in [(5, "main: Take fork main with fixes"),
                                       (4, "feat: Upstream sync and release checks"),
                                       (3, "fix: A real improvement"),
                                       (2, "fix: A real improvement"),
                                       (1, "feat: A different improvement")]]
        with patch.object(profile, "api", return_value={"items": items}):
            result = profile.merged_pull_requests()
        self.assertEqual([item["title"] for item in result],
                         ["A real improvement", "A different improvement"])

    def test_problem_and_outcome_excerpt_uses_the_outcome_not_just_the_problem(self):
        body = ("## Problem and outcome\n\nThe previous behaviour lost the prepared tool input.\n\n"
                "The SDK now preserves the prepared tool_input in both extension handlers.")
        self.assertEqual(work.summary_from_body(body),
                         "The SDK now preserves the prepared tool_input in both extension handlers.")

    def test_collecting_more_than_one_page_still_deduplicates_urls(self):
        first = [{"title": "fix: a real change", "repository_url": f"{profile.API}/repos/Owner/project",
                  "html_url": "https://github.com/Owner/project/pull/1",
                  "closed_at": "2026-11-10T12:00:00Z"}] * 100
        second = [{"title": "feat: another real change", "repository_url": f"{profile.API}/repos/Other/project",
                   "html_url": "https://github.com/Other/project/pull/2",
                   "closed_at": "2026-11-11T12:00:00Z",
                   "body": "A current description taken directly from the actual pull request."}]
        with patch.object(profile, "api", side_effect=[{"items": first}, {"items": second}]) as api:
            items = profile.merged_pull_requests()
        self.assertEqual(api.call_count, 2)
        self.assertEqual(len(items), 2)
        self.assertIn("current description", items[0]["summary"])
        self.assertIn("page=2", api.call_args.args[0])

    def test_workflow_runs_each_half_hour_and_only_commits_real_changes(self):
        path = Path(__file__).resolve().parents[1] / "workflows/readme.yml"
        workflow = yaml.load(path.read_text(), Loader=yaml.BaseLoader)
        self.assertEqual(workflow["on"]["schedule"], [{"cron": "17,47 * * * *"}])
        self.assertIn("workflow_dispatch", workflow["on"])
        self.assertEqual(workflow["jobs"]["update"]["runs-on"], "ubuntu-latest")
        commit = workflow["jobs"]["update"]["steps"][-1]["run"]
        self.assertIn("git diff --cached --quiet && exit 0", commit)


if __name__ == "__main__":
    unittest.main()
