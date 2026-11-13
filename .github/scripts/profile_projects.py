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
PROJECT_LIMIT = 6
CARD_WIDTH = 420
DISPLAY_WIDTH = 390
ASSETS = Path(".github/assets")


def select_projects(entries, api, user, limit=PROJECT_LIMIT):
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
        relationship = ("FORK" if repo.get("fork") else "OWN REPOSITORY"
                        if full_name.split("/")[0].casefold() == user.casefold()
                        else "UPSTREAM CONTRIBUTION")
        selected.append({"repo": repo, "activity": entry, "relationship": relationship})
        if limit is not None and len(selected) == limit:
            break
    return selected


def wrapped(text, width, limit=None):
    lines = textwrap.wrap(" ".join(text.split()), width=width, break_on_hyphens=False)
    if limit is not None and len(lines) > limit:
        lines = lines[:limit]
        last = lines[-1][:width - 1].rstrip()
        if " " in last:
            last = last.rsplit(" ", 1)[0]
        lines[-1] = last.rstrip(".,;:") + "…"
    return lines


def card_layout(project):
    title = project["repo"]["full_name"].split("/", 1)[1]
    description = project["repo"].get("description") or "No repository description provided."
    names = textwrap.wrap(title, width=21, break_on_hyphens=True)
    descriptions = wrapped(description, 34)
    title_y = 84
    description_y = title_y + (len(names) - 1) * 34 + 34
    footer_y = description_y + (len(descriptions) - 1) * 23 + 34
    return names, descriptions, description_y, footer_y + 82


def render_project_svg(project, index, theme="dark", height=None):
    palette = THEMES[theme]
    text, muted = palette["text"], palette["muted"]
    accent, label = palette["accent"], palette["label"]
    repo, activity = project["repo"], project["activity"]
    name = repo["full_name"]
    owner, _ = name.split("/", 1)
    description = repo.get("description") or "No repository description provided."
    when = datetime.fromisoformat(activity["when"].replace("Z", "+00:00"))
    kind = ("OPEN PR" if activity.get("state") == "open" else
            "RELEASE" if "/releases/" in activity["url"] else "MERGED PR")
    role = project.get("relationship", "FORK" if repo.get("fork") else "REPOSITORY")
    names, descriptions, description_y, minimum = card_layout(project)
    height = max(minimum, height or minimum)
    footer_y = height - 82
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_WIDTH}" height="{height}" '
        f'viewBox="0 0 {CARD_WIDTH} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{html.escape(name)}</title>',
        f'<desc id="desc">{html.escape(description)} Latest activity: '
        f'{html.escape(activity["title"])}. {kind} on {when.strftime("%Y-%m-%d")}.</desc>',
        '<g font-family="Verdana, Arial, sans-serif">',
        f'<text x="22" y="28" fill="{accent}" font-size="12" letter-spacing=".7">'
        f'{index:02d} / {role}</text>',
        f'<text x="22" y="51" fill="{muted}" font-size="15">{html.escape(owner)}</text>',
        f'<path d="M377 18v30m0-16c17 0 17-5 17-14" fill="none" stroke="{accent}" stroke-width="2"/>',
        f'<g fill="{accent}"><circle cx="377" cy="18" r="3"/><circle cx="377" cy="48" r="3"/>'
        '<circle cx="394" cy="18" r="3"/></g>',
    ]
    for index_line, line in enumerate(names):
        svg.append(f'<text x="22" y="{84 + index_line * 34}" fill="{accent}" font-family="monospace" '
                   f'font-size="28" font-weight="700">{html.escape(line)}</text>')
    for index_line, line in enumerate(descriptions):
        svg.append(f'<text class="description" x="22" y="{description_y + index_line * 23}" fill="{text}" '
                   f'font-family="monospace" font-size="18">{html.escape(line)}</text>')
    svg.append(f'<text x="22" y="{footer_y}" fill="{label}" font-size="13" letter-spacing=".5">'
               f'{kind} · {when.strftime("%d %b %Y")}</text>')
    for line, y in zip(wrapped(activity["title"], 38, 2), (footer_y + 28, footer_y + 50)):
        svg.append(f'<text x="22" y="{y}" fill="{text}" font-family="monospace" '
                   f'font-size="16">{html.escape(line)}</text>')
    svg.append('</g></svg>')
    return "\n".join(svg) + "\n"


def update_projects(root, entries, api, user, today=None):
    """Fetch/render first; return the README block and selected projects."""
    projects = select_projects(entries, api, user)
    heights = [card_layout(project)[-1] for project in projects]
    row_heights = [max(heights[index:index + 2]) for index in range(0, len(heights), 2)]
    rendered = {
        f"project-{index}-{theme}.svg": render_project_svg(project, index, theme, row_heights[(index - 1) // 2])
        for index, project in enumerate(projects, 1) for theme in THEMES
    }
    today = today or datetime.now(timezone.utc).date()
    lines = []
    if projects:
        lines = [
            section_heading("projects"),
            "", PROJECTS_INTRO, "",
        ]
        for index, project in enumerate(projects, 1):
            if index % 2 == 1:
                lines.append('<p align="center">')
            repo = project["repo"]
            stem = (ASSETS / f"project-{index}").as_posix()
            alt = f"{repo['full_name']}: {repo.get('description') or 'Public GitHub activity'}"
            lines.append(themed_picture(stem, alt, width=str(DISPLAY_WIDTH), href=f"https://github.com/{repo['full_name']}"))
            if index % 2 == 0 or index == len(projects):
                lines += ['</p>', ""]
        lines += [
            f'<sub>Automatically refreshed {today.isoformat()} · UTC · scheduled every 30 minutes.</sub>',
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
