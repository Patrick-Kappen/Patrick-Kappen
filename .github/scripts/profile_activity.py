"""Turn GitHub's contribution calendar into a self-hosted, dependency-free SVG."""

from collections import defaultdict
from datetime import date, timedelta

DAYS = 365
ACTIVITY_ASSET = ".github/assets/git-activity.svg"
COLORS = ("#d96b22", "#f58220", "#ffa45b", "#f58220")

CALENDAR_QUERY = """
query ProfileActivity($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def calendar_days(payload, today):
    """Require a complete rolling year; missing data must never become fake zeros."""
    if payload.get("errors"):
        raise ValueError("GitHub returned GraphQL errors")
    user = payload.get("data", {}).get("user")
    if not user:
        raise ValueError("GitHub user was not found")
    calendar = user["contributionsCollection"]["contributionCalendar"]
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


def activity_totals(days):
    return {period: sum(count for _, count in days[-period:]) for period in (7, 30, DAYS)}


def monthly_totals(days):
    months = defaultdict(int)
    for when, count in days:
        months[when.replace(day=1)] += count
    return sorted(months.items())


def render_activity_svg(days):
    """Three rolling totals and monthly bars covering exactly the same 365 days."""
    totals = activity_totals(days)
    months = monthly_totals(days)
    start, today = days[0][0], days[-1][0]
    description = (
        f"GitHub contributions: {totals[7]:,} in the last 7 days, "
        f"{totals[30]:,} in the last 30 days, {totals[DAYS]:,} in the last 365 days. "
        f"Monthly bars cover {start.isoformat()} to {today.isoformat()}; "
        "the first and last month can be partial. Contributions are not just commits."
    )
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="650" '
        'viewBox="0 0 1200 650" role="img" aria-labelledby="title desc">',
        '<title id="title">The Git log · a year of side quests</title>',
        f'<desc id="desc">{description}</desc>',
        '<defs>',
        '<linearGradient id="bg" x2="1" y2="1"><stop stop-color="#151515"/>'
        '<stop offset=".6" stop-color="#1c1c1c"/><stop offset="1" stop-color="#262626"/></linearGradient>',
        '</defs>',
        '<rect width="1200" height="650" fill="url(#bg)"/>',
        '<g font-family="Verdana, Arial, sans-serif">',
        '<text x="36" y="51" fill="#f2f0ed" font-size="22" font-weight="700" '
        'letter-spacing="3">SIDE QUEST TELEMETRY</text>',
        f'<text x="1164" y="51" fill="#b9b7b4" font-size="18" text-anchor="end">'
        f'Updated {today.isoformat()} · UTC</text>',
    ]
    for index, (period, label, color) in enumerate([
        (7, "LAST 7 DAYS", "#f58220"),
        (30, "LAST 30 DAYS", "#f58220"),
        (DAYS, "LAST 365 DAYS", "#ffa45b"),
    ]):
        x = 36 + index * 382
        svg += [
            f'<rect x="{x}" y="80" width="364" height="140" fill="#111111"/>',
            f'<rect x="{x}" y="98" width="4" height="104" fill="{color}"/>',
            f'<text x="{x + 24}" y="112" fill="{color}" font-size="17" '
            f'font-weight="700" letter-spacing="2">{label}</text>',
            f'<text x="{x + 24}" y="169" fill="{color}" font-size="48" '
            f'font-weight="700">{totals[period]:,}</text>',
            f'<text x="{x + 24}" y="199" fill="#b9b7b4" font-size="17">contributions</text>',
        ]
        values = [count for _, count in days[-period:]]
        peak = max(1, max(values))
        points = " ".join(
            f"{x + 212 + day * 128 / (len(values) - 1):.1f},{185 - count / peak * 48:.1f}"
            for day, count in enumerate(values)
        )
        svg += [
            f'<path d="M{x + 212} 185H{x + 340}" stroke="#393735"/>',
            f'<polygon points="{x + 212},185 {points} {x + 340},185" '
            f'fill="{color}" fill-opacity=".10"/>',
            f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2" '
            'stroke-linejoin="round" stroke-linecap="round"/>',
            f'<text x="{x + 340}" y="205" fill="#b9b7b4" font-size="12" '
            'text-anchor="end">daily trend</text>',
        ]
    svg += [
        '<text x="36" y="266" fill="#f2f0ed" font-size="24" font-weight="700">'
        'A year of building (and occasional yak shaving)</text>',
        '<text x="36" y="295" fill="#b9b7b4" font-size="17">'
        'Monthly totals across the same rolling year · edge months may be partial</text>',
    ]
    maximum = max(1, max(count for _, count in months))
    # A rolling year usually touches 13 calendar months, including two partial ones.
    slot = 1128 / len(months)
    baseline, chart_height = 514, 170
    for fraction in (0, .5, 1):
        y = baseline - fraction * chart_height
        svg.append(f'<path d="M36 {y}H1164" stroke="#45413d" stroke-dasharray="3 7"/>')
    for index, (when, count) in enumerate(months):
        x = 36 + index * slot + slot * .16
        width = slot * .68
        height = count / maximum * chart_height
        color = COLORS[index % len(COLORS)]
        center = x + width / 2
        svg += [
            f'<rect x="{x:.1f}" y="{baseline - height:.1f}" width="{width:.1f}" '
            f'height="{height:.1f}" fill="{color}">'
            f'<title>{when.strftime("%B %Y")}: {count:,} contributions in this window</title></rect>',
            f'<text x="{center:.1f}" y="{baseline - height - 10:.1f}" '
            f'text-anchor="middle" fill="{color}" font-size="17" font-weight="700">{count:,}</text>',
            f'<text x="{center:.1f}" y="540" text-anchor="middle" '
            f'fill="#f2f0ed" font-size="17">{when.strftime("%b")}</text>',
        ]
        if index == 0 or when.month == 1:
            svg.append(f'<text x="{center:.1f}" y="561" text-anchor="middle" '
                       f'fill="#b9b7b4" font-size="15">{when.year}</text>')
    svg += [
        '<path d="M36 582H1164" stroke="#45413d"/>',
        '<text x="36" y="612" fill="#b9b7b4" font-size="17">'
        'GitHub contributions, not just commits. Not a productivity leaderboard.</text>',
        f'<text x="1164" y="636" fill="#b9b7b4" font-size="15" text-anchor="end">'
        f'{start.isoformat()} → {today.isoformat()} · today is still in progress</text>',
        '</g></svg>',
    ]
    return "\n".join(svg) + "\n"
