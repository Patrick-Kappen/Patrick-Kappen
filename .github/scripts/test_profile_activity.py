"""Offline checks for activity semantics, transparent themes and safe refreshes."""

import contextlib
import io
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import profile_activity as activity
import update_readme as profile

NS = "{http://www.w3.org/2000/svg}"


def calendar_payload(today, count=lambda index: index + 1):
    start = today - timedelta(days=364)
    days = [
        {"date": (start + timedelta(days=index)).isoformat(), "contributionCount": count(index)}
        for index in range(365)
    ]
    return {"data": {"user": {"contributionsCollection": {
        "contributionCalendar": {"weeks": [{"contributionDays": days}]}
    }}}}


def raw_days(payload):
    return payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"][0]["contributionDays"]


def activity_payload(today, zero=False):
    calendar = calendar_payload(today, (lambda _: 0) if zero else (lambda index: index + 1))
    user, data = {}, {}
    for alias, period in activity.PERIODS:
        user[alias] = {
            "totalCommitContributions": 0 if zero else period * 5,
            "totalPullRequestContributions": 0 if zero else period * 2,
            "totalPullRequestReviewContributions": 0 if zero else period,
        }
        data[f"{alias}Merged"] = {"issueCount": 0 if zero else period // 3}
    user["year"].update(calendar["data"]["user"]["contributionsCollection"])
    data["user"] = user
    return {"data": data}


def luminance(color):
    channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    channels = [value / 12.92 if value <= .04045 else ((value + .055) / 1.055) ** 2.4 for value in channels]
    return sum(value * weight for value, weight in zip(channels, (.2126, .7152, .0722)))


class ActivityTests(unittest.TestCase):
    def setUp(self):
        self.today = date(2026, 11, 13)
        self.calendar = calendar_payload(self.today)
        self.payload = activity_payload(self.today)
        self.days, self.metrics = activity.parse_activity(self.payload, self.today)

    def test_calendar_totals_are_inclusive_rolling_windows(self):
        totals = activity.activity_totals(self.days)
        self.assertEqual(totals[7], sum(range(359, 366)))
        self.assertEqual(totals[30], sum(range(336, 366)))
        self.assertEqual(totals[365], sum(range(1, 366)))

    def test_leap_day_and_year_boundary(self):
        today = date(2024, 3, 1)
        days = activity.calendar_days(calendar_payload(today), today)
        self.assertEqual(len(days), 365)
        self.assertIn(date(2024, 2, 29), dict(days))
        self.assertEqual(days[-1][0], today)
        self.assertEqual(days[0][0], today - timedelta(days=364))

    def test_outside_dates_are_not_counted(self):
        raw_days(self.calendar).extend([
            {"date": (self.today + timedelta(days=1)).isoformat(), "contributionCount": 9999},
            {"date": (self.today - timedelta(days=365)).isoformat(), "contributionCount": 9999},
        ])
        self.assertEqual(activity.calendar_days(self.calendar, self.today), self.days)

    def test_incomplete_calendar_is_not_silently_zero_filled(self):
        raw_days(self.calendar).pop()
        with self.assertRaisesRegex(ValueError, "complete"):
            activity.calendar_days(self.calendar, self.today)

    def test_duplicate_days_and_invalid_counts_are_rejected(self):
        for count in (-1, True, "3", None):
            with self.subTest(count=count):
                payload = calendar_payload(self.today)
                raw_days(payload)[0]["contributionCount"] = count
                with self.assertRaises(ValueError):
                    activity.calendar_days(payload, self.today)
        raw_days(self.calendar).append(raw_days(self.calendar)[0])
        with self.assertRaises(ValueError):
            activity.calendar_days(self.calendar, self.today)

    def test_graphql_errors_and_missing_users_are_rejected(self):
        for payload in ({"errors": [{"message": "rate limited"}]}, {"data": {"user": None}},
                        {"data": None}, None, []):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                activity.parse_activity(payload, self.today)

    def test_monthly_bars_partition_the_year_not_the_four_counters(self):
        months = activity.monthly_totals(self.days)
        self.assertEqual(len(months), 13)
        self.assertEqual(months[0][0], date(2025, 11, 1))
        self.assertEqual(months[-1][0], date(2026, 11, 1))
        self.assertEqual(sum(count for _, count in months), sum(count for _, count in self.days))
        self.assertNotEqual(sum(count for _, count in self.days), sum(self.metrics[365].values()))

    def test_four_metrics_use_their_own_api_counts(self):
        self.assertEqual(self.metrics[7], {"commits": 35, "opened": 14, "merged": 2, "reviews": 7})
        self.assertEqual(self.metrics[30], {"commits": 150, "opened": 60, "merged": 10, "reviews": 30})
        self.assertEqual(self.metrics[365], {"commits": 1825, "opened": 730, "merged": 121, "reviews": 365})

    def test_merges_can_exceed_openings_in_a_window(self):
        self.payload["data"]["monthMerged"]["issueCount"] = 100
        _, metrics = activity.parse_activity(self.payload, self.today)
        self.assertGreater(metrics[30]["merged"], metrics[30]["opened"])

    def test_invalid_or_missing_metric_is_not_replaced_by_zero(self):
        for count in (-1, True, "3", None):
            with self.subTest(count=count):
                payload = activity_payload(self.today)
                payload["data"]["monthMerged"]["issueCount"] = count
                with self.assertRaises(ValueError):
                    activity.parse_activity(payload, self.today)
        del self.payload["data"]["user"]["month"]["totalCommitContributions"]
        with self.assertRaises(KeyError):
            activity.parse_activity(self.payload, self.today)

    def test_request_uses_matching_utc_windows_and_public_authored_merges(self):
        request = activity.activity_request(profile.USER, datetime(2026, 11, 13, 8, tzinfo=timezone.utc))
        variables = request["variables"]
        self.assertEqual(variables["to"], "2026-11-13T08:00:00Z")
        for period, start in [(7, "2026-11-07"), (30, "2026-10-15"), (365, "2025-11-14")]:
            self.assertEqual(variables[f"from{period}"], f"{start}T00:00:00Z")
            query = variables[f"merged{period}"]
            self.assertIn("is:public", query)
            self.assertIn("author:Patrick-Kappen", query)
            self.assertIn(f"merged:{start}..2026-11-13", query)
        self.assertIn("totalPullRequestReviewContributions", request["query"])
        self.assertIn("issueCount", request["query"])

    def test_request_normalizes_timezone_before_choosing_dates(self):
        now = datetime(2026, 11, 14, 0, 30, tzinfo=timezone(timedelta(hours=2)))
        variables = activity.activity_request(profile.USER, now)["variables"]
        self.assertEqual(variables["to"], "2026-11-13T22:30:00Z")
        self.assertEqual(variables["from7"], "2026-11-07T00:00:00Z")
        with self.assertRaises(ValueError):
            activity.activity_request(profile.USER, now.replace(tzinfo=None))

    def test_both_svgs_are_transparent_accessible_and_have_identical_data(self):
        texts = []
        for theme in activity.ACTIVITY_ASSETS:
            svg = activity.render_activity_svg(self.days, self.metrics, theme)
            root = ET.fromstring(svg)
            self.assertIsNotNone(root.find(NS + "title"))
            self.assertIn("not just commits", root.find(NS + "desc").text)
            self.assertIsNone(root.find(NS + "rect"))  # No full-canvas background.
            for rect in root.iter(NS + "rect"):
                self.assertLess(float(rect.get("width")), 200)  # No counter panel backgrounds.
            self.assertNotIn('rx="', svg)
            self.assertNotIn("<script", svg)
            self.assertNotIn("foreignObject", svg)
            self.assertNotIn('href="http', svg)
            visible = [node.text for node in root.iter(NS + "text")]
            for _, name in activity.METRICS:
                self.assertIn(name, visible)
            self.assertIn("The bigger picture", visible)
            self.assertIn("2026-11-13 · UTC", visible)
            self.assertNotIn("EXAMPLE", " ".join(visible))
            for removed in ("Monthly GitHub contributions", "Merged =", "GitHub counting/visibility",
                            "Not a productivity leaderboard"):
                self.assertNotIn(removed, " ".join(visible))
            texts.append(visible)
        self.assertEqual(texts[0], texts[1])

    def test_all_zero_data_renders_without_nan_or_fake_activity(self):
        days, metrics = activity.parse_activity(activity_payload(self.today, zero=True), self.today)
        for theme in activity.ACTIVITY_ASSETS:
            svg = activity.render_activity_svg(days, metrics, theme)
            ET.fromstring(svg)
            self.assertNotIn("nan", svg.lower())
            self.assertTrue(all(count == 0 for counts in metrics.values() for count in counts.values()))

    def test_themed_text_meets_contrast_on_github_backgrounds(self):
        for theme, background in [("dark", "#0d1117"), ("light", "#ffffff")]:
            root = ET.fromstring(activity.render_activity_svg(self.days, self.metrics, theme))
            for node in root.iter(NS + "text"):
                foreground, surface = luminance(node.get("fill")), luminance(background)
                contrast = (max(foreground, surface) + .05) / (min(foreground, surface) + .05)
                self.assertGreaterEqual(contrast, 4.5, (theme, node.text))

    def test_shared_accents_stay_orange(self):
        for palette in activity.THEMES.values():
            for color in (palette["accent"], palette["label"], *palette["bars"]):
                red, green, blue = (int(color[index:index + 2], 16) for index in (1, 3, 5))
                self.assertGreaterEqual(red, green)
                self.assertGreaterEqual(green, blue)

    def test_successful_refresh_writes_both_themes_from_one_request_and_removes_legacy(self):
        now = datetime(2026, 11, 13, 8, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as directory, patch.object(
            profile, "fetch", return_value=json.dumps(self.payload).encode()
        ) as fetch:
            root = Path(directory)
            legacy = root / activity.LEGACY_ACTIVITY_ASSET
            legacy.parent.mkdir(parents=True)
            legacy.write_text("Obsolete opaque chart")
            self.assertTrue(profile.update_activity(root, now))
            for theme, asset in activity.ACTIVITY_ASSETS.items():
                self.assertEqual((root / asset).read_text(), activity.render_activity_svg(self.days, self.metrics, theme))
            self.assertFalse(legacy.exists())
            self.assertEqual(fetch.call_count, 1)
            self.assertEqual(fetch.call_args.args[0], f"{profile.API}/graphql")
            variables = json.loads(fetch.call_args.kwargs["data"])["variables"]
            self.assertEqual(variables["from365"], "2025-11-14T00:00:00Z")
            self.assertEqual(variables["to"], "2026-11-13T08:00:00Z")

    def test_failed_or_partial_response_preserves_both_themes(self):
        partial = activity_payload(self.today)
        del partial["data"]["monthMerged"]
        responses = [None, b'{"errors": [{"message": "denied"}]}', b'{}', json.dumps(partial).encode()]
        for response in responses:
            with self.subTest(response=response), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for theme, asset in activity.ACTIVITY_ASSETS.items():
                    path = root / asset
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(f"Last good {theme}")
                kwargs = {"side_effect": OSError("offline")} if response is None else {"return_value": response}
                with patch.object(profile, "fetch", **kwargs), contextlib.redirect_stderr(io.StringIO()):
                    self.assertTrue(profile.update_activity(root))
                for theme, asset in activity.ACTIVITY_ASSETS.items():
                    self.assertEqual((root / asset).read_text(), f"Last good {theme}")

    def test_render_failure_cannot_publish_one_new_and_one_old_theme(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for asset in activity.ACTIVITY_ASSETS.values():
                path = root / asset
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("Last good version")
            with patch.object(profile, "fetch", return_value=json.dumps(self.payload).encode()), \
                 patch.object(profile, "render_activity_svg", side_effect=["New dark", ValueError("bad light")]), \
                 contextlib.redirect_stderr(io.StringIO()):
                self.assertTrue(profile.update_activity(root, datetime(2026, 11, 13, tzinfo=timezone.utc)))
            for asset in activity.ACTIVITY_ASSETS.values():
                self.assertEqual((root / asset).read_text(), "Last good version")

    def test_missing_theme_is_not_advertised_as_a_complete_fallback(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(
            profile, "fetch", side_effect=OSError("offline")
        ), contextlib.redirect_stderr(io.StringIO()):
            root = Path(directory)
            self.assertFalse(profile.update_activity(root))
            dark = root / activity.ACTIVITY_ASSETS["dark"]
            dark.parent.mkdir(parents=True)
            dark.write_text("Only a dark version")
            self.assertFalse(profile.update_activity(root))
            self.assertFalse((root / activity.ACTIVITY_ASSETS["light"]).exists())

    def test_full_daily_refresh_is_idempotent_and_references_both_generated_images(self):
        original = (
            "Static intro\n<!-- projects:start -->\nOld cards\n<!-- projects:end -->\n"
            "<!-- auto:start -->\nOld telemetry\n<!-- auto:end -->\n"
            "<!-- site:start -->\nOld tools\n<!-- site:end -->\nStatic footer\n"
        )
        now = datetime(2026, 11, 13, 8, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            readme = root / "README.md"
            readme.write_text(original)
            with patch.object(profile, "__file__", str(root / ".github/scripts/update_readme.py")), \
                 patch.object(profile, "datetime", wraps=datetime) as clock, \
                 patch.object(profile, "fetch", return_value=json.dumps(self.payload).encode()), \
                 patch.object(profile, "load", return_value={"now": {"updated": "2026-11-13", "now": []}}), \
                 patch.object(profile, "merged_pull_requests", return_value=[]), \
                 patch.object(profile, "open_pull_requests", return_value=[]), \
                 patch.object(profile, "releases", return_value=[]), \
                 patch.object(profile, "writing", return_value=[]), \
                 patch.object(profile, "render_site", return_value="Tools"):
                clock.now.return_value = now
                profile.main()
                first = readme.read_text()
                profile.main()
                self.assertEqual(first, readme.read_text())
            self.assertTrue(first.startswith("Static intro\n"))
            self.assertTrue(first.endswith("Static footer\n"))
            for asset in activity.ACTIVITY_ASSETS.values():
                self.assertIn(asset, first)
                ET.parse(root / asset)
            self.assertNotIn(activity.LEGACY_ACTIVITY_ASSET, first)

    def test_picture_uses_both_themes_with_full_width_light_fallback(self):
        now = {"updated": "2026-10-02", "now": ["Testing restores"]}
        with patch.object(profile, "shipped", return_value=[]), patch.object(profile, "writing", return_value=[]):
            result = profile.render(now, Path("unused"), activity_available=True)
        self.assertIn('<picture>', result)
        for theme, asset in activity.ACTIVITY_ASSETS.items():
            self.assertIn(f'media="(prefers-color-scheme: {theme})" srcset="{asset}"', result)
        self.assertIn(f'src="{activity.ACTIVITY_ASSETS["light"]}" width="100%"', result)
        self.assertIn(profile.section_heading("git-log"), result)
        self.assertNotIn("Recently shipped", result)


if __name__ == "__main__":
    unittest.main()
