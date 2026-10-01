"""Rewrite the generated part of README.md from now.json and public GitHub activity."""

import json
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ElementTree
from datetime import datetime
from pathlib import Path

USER = "Patrick-Kappen"
PROFILE_REPO = f"{USER}/{USER}"
SKIPPED_PREFIXES = ("chore", "test", "docs", "ci", "build", "style", "refactor")
SHIPPED_LIMIT = 5
WRITING_LIMIT = 3
START = "<!-- auto:start -->"
END = "<!-- auto:end -->"


def fetch(url, accept="application/vnd.github+json"):
    request = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": USER})
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


def month(timestamp):
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime("%b %Y")


def shipped():
    query = urllib.parse.quote(f"is:pr author:{USER} is:merged is:public -repo:{PROFILE_REPO}")
    url = f"https://api.github.com/search/issues?q={query}&sort=updated&order=desc&per_page=50"
    items = json.loads(fetch(url))["items"]
    lines = []
    for item in items:
        title = item["title"].strip()
        if title.lower().startswith(SKIPPED_PREFIXES):
            continue
        repo = item["repository_url"].split("/repos/")[1]
        lines.append(
            f"- [{repo}#{item['number']}]({item['html_url']}): {title} · {month(item['closed_at'])}"
        )
        if len(lines) == SHIPPED_LIMIT:
            break
    return lines


def writing(feed):
    if not feed:
        return []
    root = ElementTree.fromstring(fetch(feed, accept="application/rss+xml"))
    lines = []
    for item in root.iter("item"):
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        if title and link:
            lines.append(f"- [{title}]({link})")
        if len(lines) == WRITING_LIMIT:
            break
    return lines


def render(now):
    parts = ["### Now", ""]
    parts += [f"- {entry}" for entry in now["now"]]
    parts += ["", f"_Last changed {month(now['updated'] + 'T00:00:00Z')}._"]

    try:
        posts = writing(now.get("feed"))
    except OSError as error:
        print(f"feed skipped: {error}", file=sys.stderr)
        posts = []
    if posts:
        parts += ["", "### Latest writing", "", *posts]

    try:
        prs = shipped()
    except OSError as error:
        print(f"GitHub activity skipped: {error}", file=sys.stderr)
        prs = []
    if prs:
        parts += ["", "### Recently shipped", "", *prs]

    return "\n".join(parts)


def main():
    root = Path(__file__).resolve().parents[2]
    readme_path = root / "README.md"
    now = json.loads((root / "now.json").read_text())
    readme = readme_path.read_text()
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if not pattern.search(readme):
        sys.exit(f"{readme_path} has no {START} ... {END} block")
    block = f"{START}\n\n{render(now)}\n\n{END}"
    readme_path.write_text(pattern.sub(lambda _: block, readme))


if __name__ == "__main__":
    main()
