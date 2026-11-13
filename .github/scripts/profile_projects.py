"""Generate current project cards from public GitHub activity, not fixed copy."""

import html
import re
import textwrap
from datetime import datetime, timezone
from pathlib import Path

from profile_copy import PROJECTS_INTRO
from profile_visuals import THEMES, section_heading, themed_picture

PROJECT_START = "<!-- projects:start -->"
PROJECT_END = "<!-- projects:end -->"
PROJECT_LIMIT = 3
ASSETS = Path(".github/assets")


def select_projects(entries, api, user):
    """Pick recent active repository families, without showing fork + upstream twice."""
    selected, families, repositories = [], set(), {}
    for entry in sorted(entries, key=lambda item: item["when"], reverse=True):
        if entry["repo"] not in repositories:
            repositories[entry["repo"]] = api(f"repos/{entry['repo']}")
        repo = repositories[entry["repo"]]
        if repo.get("private") or repo.get("archived") or repo.get("disabled"):
            continue
        full_name = repo["full_name"]
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", full_name):
            raise ValueError("Invalid GitHub repository name")
        family = repo.get("source", repo.get("parent", repo))["full_name"].casefold()
        if family in families or full_name.casefold() == f"{user}/{user}".casefold():
            continue
        families.add(family)
        selected.append({"repo": repo, "activity": entry})
        if len(selected) == PROJECT_LIMIT:
            break
    return selected


def wrapped(text, width, limit):
    lines = textwrap.wrap(" ".join(text.split()), width=width, break_on_hyphens=False)
    if len(lines) > limit:
        lines = lines[:limit]
        last = lines[-1][:width - 1].rstrip()
        if " " in last:
            last = last.rsplit(" ", 1)[0]
        lines[-1] = last.rstrip(".,;:") + "…"
    return lines


def render_project_svg(project, index, theme="dark"):
    palette = THEMES[theme]
    text, muted = palette["text"], palette["muted"]
    accent, label = palette["accent"], palette["label"]
    repo, activity = project["repo"], project["activity"]
    name = repo["full_name"]
    owner, title = name.split("/", 1)
    description = repo.get("description") or "No repository description provided."
    when = datetime.fromisoformat(activity["when"].replace("Z", "+00:00"))
    if activity.get("state") == "open":
        kind = "OPEN PR"
    else:
        kind = "RELEASE" if "/releases/" in activity["url"] else "MERGED PR"
    # These are facts about this repository/activity, not invented project statuses.
    role = "FORK" if repo.get("fork") else "REPOSITORY"
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="264" '
        'viewBox="0 0 360 264" role="img" aria-labelledby="title desc">',
        f'<title id="title">{html.escape(name)}</title>',
        f'<desc id="desc">{html.escape(description)} Latest activity: '
        f'{html.escape(activity["title"])}. {kind} on {when.strftime("%Y-%m-%d")}.</desc>',
        '<g font-family="Verdana, Arial, sans-serif">',
        f'<text x="22" y="28" fill="{accent}" font-size="14" letter-spacing="1">'
        f'{index:02d} / {role}</text>',
        f'<text x="22" y="50" fill="{muted}" font-size="15">{html.escape(owner)}</text>',
        f'<path d="M317 18v30m0-16c17 0 17-5 17-14" fill="none" stroke="{accent}" stroke-width="2"/>',
        f'<g fill="{accent}"><circle cx="317" cy="18" r="3"/><circle cx="317" cy="48" r="3"/>'
        '<circle cx="334" cy="18" r="3"/></g>',
    ]
    for line, y in zip(wrapped(title, 18, 2), (82, 114)):
        svg.append(f'<text x="22" y="{y}" fill="{accent}" font-size="30" '
                   f'font-weight="700">{html.escape(line)}</text>')
    for line, y in zip(wrapped(description, 29, 2), (145, 168)):
        svg.append(f'<text x="22" y="{y}" fill="{text}" font-family="monospace" '
                   f'font-size="18">{html.escape(line)}</text>')
    svg.append(f'<text x="22" y="197" fill="{label}" font-size="13" letter-spacing="1">'
               f'{kind} · {when.strftime("%d %b %Y")}</text>')
    for line, y in zip(wrapped(activity["title"], 30, 2), (224, 247)):
        svg.append(f'<text x="22" y="{y}" fill="{text}" font-family="monospace" '
                   f'font-size="17">{html.escape(line)}</text>')
    svg.append('</g></svg>')
    return "\n".join(svg) + "\n"


def update_projects(root, entries, api, user, today=None):
    """Fetch/render first; return the README block and selected projects."""
    projects = select_projects(entries, api, user)
    rendered = {
        f"project-{index}-{theme}.svg": render_project_svg(project, index, theme)
        for index, project in enumerate(projects, 1) for theme in THEMES
    }
    today = today or datetime.now(timezone.utc).date()
    lines = []
    if projects:
        lines = [
            section_heading("projects"),
            "", PROJECTS_INTRO, "",
            '<p align="center">',
        ]
        for index, project in enumerate(projects, 1):
            repo = project["repo"]
            stem = (ASSETS / f"project-{index}").as_posix()
            alt = f"{repo['full_name']}: {repo.get('description') or 'Public GitHub activity'}"
            lines.append(themed_picture(stem, alt, width="270", href=f"https://github.com/{repo['full_name']}"))
        lines += [
            '</p>',
            "",
            '<sub>Selected from recent public PRs and releases. '
            f'Automatically refreshed {today.isoformat()} · UTC.</sub>',
        ]
    assets = root / ASSETS
    assets.mkdir(parents=True, exist_ok=True)
    expected = set(rendered)
    for name, svg in rendered.items():
        (assets / name).write_text(svg)
    # These files are generated exclusively by this module, including old static cards.
    for path in assets.glob("project-*.svg"):
        if path.name not in expected:
            path.unlink()
    return "\n".join(lines), projects
