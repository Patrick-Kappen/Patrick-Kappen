"""Fetch separate GitHub activity counts and render transparent, themed SVGs."""

from collections import defaultdict
from datetime import date, timedelta, timezone

from profile_visuals import THEMES, image_height

DAYS = 365
PERIODS = (("week", 7), ("month", 30), ("year", DAYS))
ACTIVITY_STEM = ".github/assets/git-activity"
ACTIVITY_ASSETS = {theme: f"{ACTIVITY_STEM}-{theme}.svg" for theme in THEMES}
ACTIVITY_VARIANTS = {
    (theme, compact): f"{ACTIVITY_STEM}{'-compact' if compact else ''}-{theme}.svg"
    for compact in (False, True) for theme in THEMES
}
LEGACY_ACTIVITY_ASSET = ".github/assets/git-activity.svg"
METRICS = (("commits", "COMMITS"), ("opened", "PRs OPENED"),
           ("merged", "PRs MERGED"), ("reviews", "REVIEWS"))
ACTIVITY_QUERY = """
query ProfileActivity(
  $login: String!, $from7: DateTime!, $from30: DateTime!, $from365: DateTime!, $to: DateTime!,
  $merged7: String!, $merged30: String!, $merged365: String!
) {
  user(login: $login) {
    week: contributionsCollection(from: $from7, to: $to) {
      totalCommitContributions totalPullRequestContributions totalPullRequestReviewContributions
    }
    month: contributionsCollection(from: $from30, to: $to) {
      totalCommitContributions totalPullRequestContributions totalPullRequestReviewContributions
    }
    year: contributionsCollection(from: $from365, to: $to) {
      totalCommitContributions totalPullRequestContributions totalPullRequestReviewContributions
      contributionCalendar { weeks { contributionDays { date contributionCount } } }
    }
  }
  weekMerged: search(type: ISSUE, query: $merged7) { issueCount }
  monthMerged: search(type: ISSUE, query: $merged30) { issueCount }
  yearMerged: search(type: ISSUE, query: $merged365) { issueCount }
}
"""


def activity_request(user, now):
    """Use identical inclusive UTC date windows for all four metrics."""
    if now.tzinfo is None:
        raise ValueError("Activity refresh requires a timezone-aware datetime")
    now = now.astimezone(timezone.utc)
    today = now.date()
    variables = {"login": user, "to": now.isoformat(timespec="seconds").replace("+00:00", "Z")}
    for _, period in PERIODS:
        start = today - timedelta(days=period - 1)
        variables[f"from{period}"] = f"{start.isoformat()}T00:00:00Z"
        variables[f"merged{period}"] = (
            f"is:pr is:public author:{user} is:merged merged:{start.isoformat()}..{today.isoformat()}"
        )
    return {"query": ACTIVITY_QUERY, "variables": variables}


def user_data(payload):
    if not isinstance(payload, dict) or payload.get("errors"):
        raise ValueError("GitHub returned invalid data or GraphQL errors")
    data = payload.get("data")
    user = data.get("user") if isinstance(data, dict) else None
    if not isinstance(user, dict):
        raise ValueError("GitHub user was not found")
    return user


def calendar_days(payload, today):
    """Require a complete rolling year; never turn missing days into fake zeros."""
    calendar = user_data(payload)["contributionsCollection"]["contributionCalendar"]
    start = today - timedelta(days=DAYS - 1)
    days = {}
    for week in calendar["weeks"]:
        for day in week["contributionDays"]:
            when = date.fromisoformat(day["date"])
            if not start <= when <= today:
                continue
            count = day["contributionCount"]
            if type(count) is not int or count < 0 or when in days:
                raise ValueError("Invalid or duplicate contribution day")
            days[when] = count
    if len(days) != DAYS:
        raise ValueError("GitHub did not return a complete contribution year")
    return sorted(days.items())


def parse_activity(payload, today):
    user = user_data(payload)
    metrics = {}
    for alias, period in PERIODS:
        collection = user[alias]
        counts = {
            "commits": collection["totalCommitContributions"],
            "opened": collection["totalPullRequestContributions"],
            "merged": payload["data"][f"{alias}Merged"]["issueCount"],
            "reviews": collection["totalPullRequestReviewContributions"],
        }
        if any(type(count) is not int or count < 0 for count in counts.values()):
            raise ValueError("GitHub returned an invalid activity count")
        metrics[period] = counts
    calendar = {"data": {"user": {"contributionsCollection": user["year"]}}}
    return calendar_days(calendar, today), metrics


def activity_totals(days):
    return {period: sum(count for _, count in days[-period:]) for _, period in PERIODS}


def monthly_totals(days):
    months = defaultdict(int)
    for when, count in days:
        months[when.replace(day=1)] += count
    return sorted(months.items())


def render_activity_svg(days, metrics, theme="dark", compact=False):
    """Reflow counters and bars horizontally; keep vertical geometry/fonts fixed."""
    scale = .6 if compact else image_height(ACTIVITY_STEM, compact) / 710
    row_offset = 132 if compact else 0

    def px(value):
        return f"{value * scale:.2f}"

    def chart_y(value):
        return f"{value * scale + row_offset:.2f}"

    def chart_font(value):
        # Thirteen month labels must still fit a phone; counters use larger type.
        return f"{value * (.42 if compact else scale):.2f}"

    palette = THEMES[theme]
    text, muted, line = palette["text"], palette["muted"], palette["line"]
    accent, label = palette["accent"], palette["label"]
    months = monthly_totals(days)
    start, today = days[0][0], days[-1][0]
    description = "; ".join(
        f"{name.lower()}: {metrics[30][key]:,} in 30 days, "
        f"{metrics[7][key]:,} in 7 days, {metrics[DAYS][key]:,} in 365 days"
        for key, name in METRICS
    )
    description += (
        ". Merged PRs are public PRs authored by the profile owner; opened and merged counts overlap. "
        f"Monthly bars cover {start.isoformat()} to {today.isoformat()}: "
        f"{sum(count for _, count in days):,} GitHub contributions, not just commits. "
        "The edge months may be partial. GitHub counting and visibility rules apply."
    )
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="{image_height(ACTIVITY_STEM, compact)}" '
        'role="img" aria-labelledby="title desc">',
        '<title id="title">GitHub activity: commits, opened PRs, merged PRs and reviews</title>',
        f'<desc id="desc">{description}</desc>',
        '<g font-family="Verdana, Arial, sans-serif">',
        '<svg x="3%" width="94%" height="100%">',
        f'<text x="0" y="{px(48)}" fill="{text}" font-size="{px(22)}" font-weight="700" '
        f'letter-spacing="{px(3)}">SIDE QUEST TELEMETRY</text>',
        f'<text x="0" y="{px(82)}" fill="{muted}" font-size="{px(18)}">'
        'Last 30 days in focus · 7 and 365 days for context</text>',
    ]
    for index, (key, name) in enumerate(METRICS):
        columns = 2 if compact else 4
        x = index % columns * (100 // columns)
        y = index // columns * row_offset
        svg += [
            f'<svg class="counter" x="{x}%" y="{y}" width="{100 // columns}%" height="{px(320)}">',
            f'<rect x="0" y="{px(122)}" width="{px(3)}" height="{px(92)}" fill="{accent}"/>',
            f'<text x="{px(20)}" y="{px(139)}" fill="{label}" font-size="{px(16)}" '
            f'font-weight="700" letter-spacing="{px(1)}">{name}</text>',
            f'<text x="{px(20)}" y="{px(195)}" fill="{accent}" font-size="{px(48)}" '
            f'font-weight="700">{metrics[30][key]:,}</text>',
            f'<text x="{px(20)}" y="{px(220)}" fill="{muted}" font-size="{px(16)}">last 30 days</text>',
            f'<line x1="{px(20)}" x2="94%" y1="{px(237)}" y2="{px(237)}" stroke="{line}"/>',
            f'<text x="{px(20)}" y="{px(266)}" fill="{muted}" font-size="{px(17)}">7 days</text>',
            f'<text x="94%" y="{px(266)}" text-anchor="end" fill="{text}" '
            f'font-size="{px(20)}" font-weight="700">{metrics[7][key]:,}</text>',
            f'<text x="{px(20)}" y="{px(297)}" fill="{muted}" font-size="{px(17)}">365 days</text>',
            f'<text x="94%" y="{px(297)}" text-anchor="end" fill="{text}" '
            f'font-size="{px(20)}" font-weight="700">{metrics[DAYS][key]:,}</text>',
            '</svg>',
        ]
    svg.append(f'<text x="0" y="{chart_y(365)}" fill="{text}" font-size="{px(24)}" '
               'font-weight="700">The bigger picture</text>')
    maximum = max(1, max(count for _, count in months))
    slot, baseline, chart_height = 100 / len(months), 621, 210
    for fraction in (0, .5, 1):
        y = chart_y(baseline - fraction * chart_height)
        svg.append(f'<line x1="0" x2="100%" y1="{y}" y2="{y}" stroke="{line}" stroke-dasharray="3 7"/>')
    for index, (when, count) in enumerate(months):
        x, width = index * slot + slot * .16, slot * .68
        height = count / maximum * chart_height
        center = x + width / 2
        color = palette["bars"][index % len(palette["bars"])]
        svg += [
            f'<rect class="month-bar" x="{x:.6f}%" y="{chart_y(baseline - height)}" width="{width:.6f}%" '
            f'height="{px(height)}" fill="{color}">'
            f'<title>{when.strftime("%B %Y")}: {count:,} contributions in this window</title></rect>',
            f'<text x="{center:.6f}%" y="{chart_y(baseline - height - 10)}" '
            f'text-anchor="middle" fill="{color}" font-size="{chart_font(17)}" font-weight="700">{count:,}</text>',
            f'<text x="{center:.6f}%" y="{chart_y(647)}" text-anchor="middle" '
            f'fill="{text}" font-size="{chart_font(17)}">{when.strftime("%b")}</text>',
        ]
        if index == 0 or when.month == 1:
            svg.append(f'<text x="{center:.6f}%" y="{chart_y(669)}" text-anchor="middle" '
                       f'fill="{muted}" font-size="{chart_font(15)}">{when.year}</text>')
    svg += [
        f'<text x="100%" y="{chart_y(698)}" text-anchor="end" fill="{muted}" '
        f'font-size="{chart_font(15)}">{today.isoformat()} · UTC</text>',
        '</svg></g></svg>',
    ]
    return "\n".join(svg) + "\n"
