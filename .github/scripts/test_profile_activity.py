"""Contribution window, chart and refresh checks; no network access required."""

import contextlib
import io
import json
import re
import tempfile
import unittest
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import profile_activity as activity
import update_readme as profile


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


class ActivityTests(unittest.TestCase):
    def setUp(self):
        self.today = date(2026, 11, 13)
        self.payload = calendar_payload(self.today)
        self.days = activity.calendar_days(self.payload, self.today)

    def test_totals_are_inclusive_rolling_windows(self):
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
        raw_days(self.payload).extend([
            {"date": (self.today + timedelta(days=1)).isoformat(), "contributionCount": 9999},
            {"date": (self.today - timedelta(days=365)).isoformat(), "contributionCount": 9999},
        ])
        self.assertEqual(activity.calendar_days(self.payload, self.today), self.days)

    def test_incomplete_data_is_not_silently_zero_filled(self):
        raw_days(self.payload).pop()
        with self.assertRaisesRegex(ValueError, "complete"):
            activity.calendar_days(self.payload, self.today)

    def test_duplicates_and_bad_counts_are_rejected(self):
        for count in (-1, True, "3", None):
            with self.subTest(count=count):
                payload = calendar_payload(self.today)
                raw_days(payload)[0]["contributionCount"] = count
                with self.assertRaises(ValueError):
                    activity.calendar_days(payload, self.today)
        raw_days(self.payload).append(raw_days(self.payload)[0])
        with self.assertRaises(ValueError):
            activity.calendar_days(self.payload, self.today)

    def test_graphql_errors_and_missing_user_are_rejected(self):
        for payload in ({"errors": [{"message": "rate limited"}]}, {"data": {"user": None}}):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                activity.calendar_days(payload, self.today)

    def test_monthly_bars_sum_to_the_year_total(self):
        months = activity.monthly_totals(self.days)
        self.assertEqual(len(months), 13)
        self.assertEqual(months[0][0], date(2025, 11, 1))
        self.assertEqual(months[-1][0], date(2026, 11, 1))
        self.assertEqual(sum(count for _, count in months), activity.activity_totals(self.days)[365])

    def test_svg_is_accessible_and_zero_safe(self):
        for days in (self.days, activity.calendar_days(calendar_payload(self.today, lambda _: 0), self.today)):
            with self.subTest(total=sum(count for _, count in days)):
                svg = activity.render_activity_svg(days)
                root = ET.fromstring(svg)
                namespace = {"svg": "http://www.w3.org/2000/svg"}
                self.assertIsNotNone(root.find("svg:title", namespace))
                background = root.find("svg:rect", namespace)
                self.assertNotIn("rx", background.attrib)
                self.assertNotIn("stroke", background.attrib)
                self.assertNotIn('rx="', svg)
                self.assertEqual(len(root.findall(".//svg:polyline", namespace)), 3)
                self.assertIn("not just commits", root.find("svg:desc", namespace).text)
                self.assertIn(self.today.isoformat(), svg)
                self.assertNotIn("nan", svg.lower())
                self.assertNotIn("<script", svg)
                self.assertNotIn("foreignObject", svg)
                self.assertNotIn('href="http', svg)

    def test_artwork_keeps_the_industrial_palette(self):
        assets = Path(__file__).resolve().parents[1] / "assets"
        artwork = {
            path.name: path.read_text()
            for path in assets.glob("*.svg")
            if path.name != "git-activity.svg"
        }
        artwork["generated chart"] = activity.render_activity_svg(self.days)
        for name, svg in artwork.items():
            with self.subTest(asset=name):
                root = ET.fromstring(svg)
                colors = {
                    value for node in root.iter()
                    for attribute in ("fill", "stroke", "stop-color")
                    for value in [node.get(attribute, "")]
                    if re.fullmatch(r"#[0-9a-fA-F]{6}", value)
                }
                self.assertTrue(colors)
                for color in colors:
                    red, green, blue = (int(color[i:i + 2], 16) for i in (1, 3, 5))
                    self.assertGreaterEqual(red, green, color)
                    self.assertGreaterEqual(green, blue, color)
                self.assertIn("#f58220", svg)

    def test_successful_refresh_posts_query_and_writes_chart(self):
        now = datetime(2026, 11, 13, 8, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as directory, patch.object(
            profile, "fetch", return_value=json.dumps(self.payload).encode()
        ) as fetch:
            root = Path(directory)
            self.assertTrue(profile.update_activity(root, now))
            self.assertIn("LAST 365 DAYS", (root / activity.ACTIVITY_ASSET).read_text())
            self.assertEqual(fetch.call_args.args[0], f"{profile.API}/graphql")
            variables = json.loads(fetch.call_args.kwargs["data"])["variables"]
            self.assertEqual(variables["login"], profile.USER)
            self.assertEqual(variables["from"], "2025-11-14T00:00:00Z")
            self.assertEqual(variables["to"], "2026-11-13T08:00:00+00:00")

    def test_failed_refresh_keeps_last_good_chart(self):
        for response in (None, b'{"errors": [{"message": "denied"}]}', b'{}'):
            with self.subTest(response=response), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                path = root / activity.ACTIVITY_ASSET
                path.parent.mkdir(parents=True)
                path.write_text("Last good chart")
                kwargs = {"side_effect": OSError("offline")} if response is None else {"return_value": response}
                with patch.object(profile, "fetch", **kwargs), contextlib.redirect_stderr(io.StringIO()):
                    self.assertTrue(profile.update_activity(root))
                self.assertEqual(path.read_text(), "Last good chart")

    def test_failed_first_refresh_does_not_make_a_fake_chart(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(
            profile, "fetch", side_effect=OSError("offline")
        ), contextlib.redirect_stderr(io.StringIO()):
            root = Path(directory)
            self.assertFalse(profile.update_activity(root))
            self.assertFalse((root / activity.ACTIVITY_ASSET).exists())

    def test_chart_can_be_shown_without_recent_pull_requests(self):
        now = {"updated": "2026-10-02", "now": ["Testing restores"]}
        with patch.object(profile, "shipped", return_value=[]), patch.object(profile, "writing", return_value=[]):
            result = profile.render(now, Path("unused"), activity_available=True)
        self.assertIn(f'src="{activity.ACTIVITY_ASSET}" width="100%"', result)
        self.assertIn("## 📊 The Git log", result)
        self.assertNotIn("Recently shipped", result)


if __name__ == "__main__":
    unittest.main()
