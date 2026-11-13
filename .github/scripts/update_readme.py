"""Rewrite the generated parts of README.md from the content repository and public GitHub activity."""

import html
import json
import os
import re
import sys
import textwrap
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from functools import cache
from pathlib import Path

import yaml

from profile_activity import ACTIVITY_ASSET, CALENDAR_QUERY, DAYS, calendar_days, render_activity_svg
from profile_projects import PROJECT_END, PROJECT_START, select_projects, update_projects

USER = "Patrick-Kappen"
PROFILE_REPO = f"{USER}/{USER}"
API = "https://api.github.com"
SHIPPED_LIMIT = 3
ACTIVITY_CANDIDATE_LIMIT = 12
WRITING_LIMIT = 3
TOOL_LOGO_LIMIT = 10
START = "<!-- auto:start -->"
END = "<!-- auto:end -->"
SITE_URL = "https://patrick.kappen.io"
SITE_START = "<!-- site:start -->"
SITE_END = "<!-- site:end -->"
WRAP = 80

KINDS = {
    "feat": "✨",
    "fix": "🐛",
    "perf": "⚡",
    "security": "🔒",
}
IGNORED_KINDS = {"build", "chore", "ci", "docs", "style", "sync", "test"}
RELEASE_ICON = "🚀"
CONVENTIONAL = re.compile(r"^(?P<kind>[a-z]+)(\([^)]*\))?!?:\s*(?P<rest>.+)$")


def fetch(url, accept="application/vnd.github+json", data=None):
    headers = {"Accept": accept, "User-Agent": USER}
    if data is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, headers=headers, data=data)
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith(API):
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


def api(path):
    return json.loads(fetch(f"{API}/{path}"))


def update_activity(root, now=None):
    """Refresh the chart, keeping the last successful SVG if GitHub is unavailable."""
    now = now or datetime.now(timezone.utc)
    today = now.date()
    start = today - timedelta(days=DAYS - 1)
    path = root / ACTIVITY_ASSET
    payload = {
        "query": CALENDAR_QUERY,
        "variables": {
            "login": USER,
            "from": f"{start.isoformat()}T00:00:00Z",
            "to": now.isoformat(timespec="seconds"),
        },
    }
    try:
        response = json.loads(fetch(f"{API}/graphql", data=json.dumps(payload).encode()))
        svg = render_activity_svg(calendar_days(response, today))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Contribution chart kept unchanged: {error}", file=sys.stderr)
        return path.is_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg)
    return True


def parse_time(timestamp):
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))


def month(timestamp):
    return parse_time(timestamp).strftime("%b %Y")


def readable(title):
    match = CONVENTIONAL.match(title.strip())
    if not match:
        return None, title.strip()
    rest = match["rest"].strip()
    return match["kind"], rest[:1].upper() + rest[1:]


def pull_requests(state):
    query = urllib.parse.quote(
        f"is:pr author:{USER} is:{state} is:public -repo:{PROFILE_REPO}"
    )
    items = api(f"search/issues?q={query}&sort=updated&order=desc&per_page=100")["items"]
    entries = []
    # For merged PRs, closed_at is the merge date, not a later comment date.
    # Open cards show the PR's latest update; they never appear as shipped.
    date_key = "closed_at" if state == "merged" else "updated_at"
    for item in sorted(items, key=lambda item: item[date_key], reverse=True):
        kind, title = readable(item["title"])
        if kind in IGNORED_KINDS:
            continue
        if kind in {"main", "performance"} and re.match(r"(?:upstream|fork)\b", title, re.IGNORECASE):
            continue
        repo = item["repository_url"].split("/repos/")[1]
        if any(entry["repo"] == repo for entry in entries):
            continue
        entries.append(
            {
                "repo": repo,
                "when": item[date_key],
                "state": state,
                "icon": KINDS.get(kind, "🔧"),
                "title": title,
                "url": item["html_url"],
            }
        )
        if len(entries) == ACTIVITY_CANDIDATE_LIMIT:
            break
    return entries


def merged_pull_requests():
    return pull_requests("merged")


def open_pull_requests():
    return pull_requests("open")


def releases():
    entries = []
    for repo in api(f"users/{USER}/repos?type=owner&sort=pushed&per_page=30"):
        if repo["fork"] or repo["private"] or repo["full_name"] == PROFILE_REPO:
            continue
        for release in api(f"repos/{repo['full_name']}/releases?per_page=3"):
            if release["draft"]:
                continue
            name = release["name"] or release["tag_name"]
            if release["tag_name"] not in name:
                name = f"{release['tag_name']}: {name}"
            entries.append(
                {
                    "repo": repo["full_name"],
                    "when": release["published_at"],
                    "icon": RELEASE_ICON,
                    "title": name.replace(" — ", ": "),
                    "url": release["html_url"],
                }
            )
    return entries


def shipped(entries=None):
    if entries is None:
        entries = merged_pull_requests() + releases()
    entries = sorted(entries, key=lambda entry: parse_time(entry["when"]), reverse=True)
    lines = []
    seen = set()
    for entry in entries:
        if entry.get("state") == "open":
            continue
        repo = entry["repo"]
        if repo in seen:
            continue
        seen.add(repo)
        name = repo.split("/")[1] if repo.startswith(f"{USER}/") else repo
        lines.append(
            f"- {entry['icon']} **[{entry['title']}]({entry['url']})**<br>"
            f"<sub>{html.escape(name)} · {month(entry['when'])}</sub>"
        )
        if len(lines) == SHIPPED_LIMIT:
            break
    return lines


def writing(content):
    posts = []
    for path in (content / "posts").glob("*.md"):
        front = yaml.safe_load(path.read_text().split("---", 2)[1])
        if front.get("kind") == "post" and front.get("status") == "published":
            posts.append((str(front["date"]), front["title"], path.stem))
    posts.sort(reverse=True)
    return [f"- [{title}]({SITE_URL}/blog/{slug}/)" for _, title, slug in posts[:WRITING_LIMIT]]


def load(content, name):
    return yaml.safe_load((content / name).read_text())


def bullet(label, items):
    text = f"- **{label}:** " + " · ".join(items)
    return textwrap.fill(
        text, WRAP, subsequent_indent="  ", break_long_words=False, break_on_hyphens=False
    )


def render_site(content):
    site = load(content, "site.yaml")
    groups = sorted(load(content, "tool-groups.yaml"), key=lambda group: group["order"])
    tools = sorted(
        (tool for tool in load(content, "tools.yaml") if tool.get("highlight") is not None),
        key=lambda tool: tool["highlight"],
    )
    lines = ["## 🧰 Things I reach for", ""]
    logos = [tool for tool in tools if tool.get("logo", "").startswith("/assets/logos/")]
    if logos:
        lines += ["<p>"]
        for tool in logos[:TOOL_LOGO_LIMIT]:
            name = html.escape(tool["name"], quote=True)
            src = html.escape(f"public{tool['logo']}", quote=True)
            lines.append(
                f'  <img src="{src}" alt="{name}" title="{name}" width="36" height="36" /> &nbsp;'
            )
        lines += ["</p>", ""]
    lines += [
        "<details>",
        "<summary><strong>The longer version, including the certificates</strong></summary>",
        "",
        "### Toolbox",
        "",
    ]
    for group in groups:
        names = [tool["name"] for tool in tools if tool["group"] == group["id"]]
        if names:
            lines.append(bullet(group["title"], names))
    lines += [
        "",
        "### Certifications",
        "",
        bullet("Certified", [cert if isinstance(cert, str) else f"[{cert['code']}]({cert['url']})" for cert in site["certifications"]]),
        bullet("Working towards", site["studying"]),
        "",
        "</details>",
    ]
    return "\n".join(lines)


def render(now, content, activity_available=False, work=None):
    parts = []
    if work is None:
        try:
            work = shipped()
        except OSError as error:
            print(f"GitHub activity skipped: {error}", file=sys.stderr)
            work = []
    if activity_available or work:
        parts += ["## 📊 The Git log", ""]
    if activity_available:
        parts += [
            f'<a href="https://github.com/{USER}?tab=overview">'
            f'<img src="{ACTIVITY_ASSET}" width="100%" '
            'alt="GitHub contributions over 7, 30 and 365 days, with monthly totals" /></a>',
            "",
        ]
    if work:
        parts += ["### 🚢 Recently shipped", "", *work, ""]

    parts += ["## 📡 Currently on the workbench", ""]
    parts += [f"- {entry}" for entry in now["now"]]
    parts += ["", f"_Updated {month(now['updated'] + 'T00:00:00Z')}. Side quests subject to change._"]

    posts = writing(content)
    if posts:
        parts += ["", "## ✍️ Notes from the rabbit hole", "", *posts]

    return "\n".join(parts)


def replace_block(text, start, end, body, path):
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(text):
        sys.exit(f"{path} has no {start} ... {end} block")
    return pattern.sub(lambda _: f"{start}\n\n{body}\n\n{end}", text)


def main():
    root = Path(__file__).resolve().parents[2]
    readme_path = root / "README.md"
    content = Path(os.environ.get("CONTENT_DIR", root / "content"))
    now = load(content, "site.yaml")["now"]
    now["updated"] = str(now["updated"])
    readme = readme_path.read_text()
    activity_available = update_activity(root)
    work = None
    try:
        entries = merged_pull_requests() + releases()
        repository_api = cache(api)
        project_body, _ = update_projects(root, entries + open_pull_requests(), repository_api, USER)
        shipped_projects = select_projects(entries, repository_api, USER)
        work = shipped([project["activity"] for project in shipped_projects])
        readme = replace_block(readme, PROJECT_START, PROJECT_END, project_body, readme_path)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Project cards kept unchanged: {error}", file=sys.stderr)
        previous = re.search(r"### 🚢 Recently shipped\n\n(.*?)(?=\n\n##|\n\n<!-- auto:end -->)", readme, re.DOTALL)
        work = previous[1].splitlines() if previous else []
    readme = replace_block(readme, START, END, render(now, content, activity_available, work), readme_path)
    readme = replace_block(readme, SITE_START, SITE_END, render_site(content), readme_path)
    readme_path.write_text(readme)


if __name__ == "__main__":
    main()
