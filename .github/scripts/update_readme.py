"""Rewrite the generated parts of README.md from the content repository and public GitHub activity."""

import json
import os
import re
import sys
import textwrap
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ElementTree
from datetime import datetime
from pathlib import Path

import yaml

USER = "Patrick-Kappen"
PROFILE_REPO = f"{USER}/{USER}"
API = "https://api.github.com"
SHIPPED_LIMIT = 6
WRITING_LIMIT = 3
SUMMARY_LENGTH = 180
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
RELEASE_ICON = "🚀"
CONVENTIONAL = re.compile(r"^(?P<kind>[a-z]+)(\([^)]*\))?!?:\s*(?P<rest>.+)$")
CLOSING_REFERENCE = re.compile(r"\b(closes|fixes|resolves)\s+#\d+\.?", re.IGNORECASE)


def fetch(url, accept="application/vnd.github+json"):
    request = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": USER})
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith(API):
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


def api(path):
    return json.loads(fetch(f"{API}/{path}"))


def parse_time(timestamp):
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))


def month(timestamp):
    return parse_time(timestamp).strftime("%b %Y")


def shorten(text):
    text = " ".join(text.split())
    if len(text) <= SUMMARY_LENGTH:
        return text
    return text[: SUMMARY_LENGTH - 1].rsplit(" ", 1)[0] + "…"


def first_sentence(markdown):
    """The first prose sentence, or else the first bullet, without headings or closing references."""
    first_bullet = ""
    for block in re.split(r"\n\s*\n", markdown or ""):
        lines = [line for line in block.strip().splitlines() if not line.startswith("#")]
        block = "\n".join(lines).strip()
        if not block or block.startswith(("|", "```", "<!--")):
            continue
        if block.startswith(("-", "*")):
            if not first_bullet:
                bullet = re.sub(r"^[-*]\s+", "", lines[0].strip())
                first_bullet = bullet[:1].upper() + bullet[1:]
            continue
        block = CLOSING_REFERENCE.sub("", block).strip()
        if block:
            sentence = re.split(r"(?<=[.!?])\s", block, maxsplit=1)[0]
            return shorten(sentence)
    return shorten(first_bullet.rstrip(".") + ".") if first_bullet else ""


def highlights(markdown, count=2):
    """The first bullets of release notes, joined into one line."""
    bullets = [
        re.sub(r"^[-*]\s+", "", line.strip()).rstrip(".")
        for line in (markdown or "").splitlines()
        if re.match(r"^\s*[-*]\s+\S", line)
    ]
    return shorten("; ".join(bullets[:count]) + ".") if bullets else first_sentence(markdown)


def readable(title):
    match = CONVENTIONAL.match(title.strip())
    if not match:
        return None, title.strip()
    rest = match["rest"].strip()
    return match["kind"], rest[:1].upper() + rest[1:]


def merged_pull_requests():
    query = urllib.parse.quote(
        f"is:pr author:{USER} is:merged is:public -repo:{PROFILE_REPO}"
    )
    items = api(f"search/issues?q={query}&sort=updated&order=desc&per_page=50")["items"]
    entries = []
    for item in items:
        kind, title = readable(item["title"])
        if kind not in KINDS:
            continue
        repo = item["repository_url"].split("/repos/")[1]
        pull = api(f"repos/{repo}/pulls/{item['number']}")
        entries.append(
            {
                "repo": repo,
                "when": pull["merged_at"] or item["closed_at"],
                "icon": KINDS[kind],
                "title": title,
                "url": item["html_url"],
                "summary": first_sentence(item.get("body")),
                "size": f"+{pull['additions']} −{pull['deletions']}",
            }
        )
        if len(entries) == SHIPPED_LIMIT:
            break
    return entries


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
                    "summary": highlights(release.get("body")),
                    "size": "pre-release" if release["prerelease"] else "release",
                }
            )
    return entries


def shipped():
    entries = merged_pull_requests() + releases()
    entries.sort(key=lambda entry: parse_time(entry["when"]), reverse=True)
    entries = entries[:SHIPPED_LIMIT]

    by_repo = {}
    for entry in entries:
        by_repo.setdefault(entry["repo"], []).append(entry)

    lines = []
    for repo, repo_entries in by_repo.items():
        description = api(f"repos/{repo}").get("description") or ""
        name = repo.split("/")[1] if repo.startswith(f"{USER}/") else repo
        heading = f"**[{name}](https://github.com/{repo})**"
        lines += ["", f"{heading} · {description}" if description else heading, ""]
        for entry in repo_entries:
            line = (
                f"- {entry['icon']} **[{entry['title']}]({entry['url']})**"
                f" · {month(entry['when'])} · {entry['size']}"
            )
            if entry["summary"]:
                lines += [line + "\\", f"  {entry['summary']}"]
            else:
                lines.append(line)
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
    lines = ["## Toolbox", ""]
    for group in groups:
        names = [tool["name"] for tool in tools if tool["group"] == group["id"]]
        if names:
            lines.append(bullet(group["title"], names))
    lines += [
        "",
        "## Certifications",
        "",
        bullet("Certified", site["certifications"]),
        bullet("Working towards", site["studying"]),
    ]
    return "\n".join(lines)


def render(now, content):
    parts = ["### Now", ""]
    parts += [f"- {entry}" for entry in now["now"]]
    parts += ["", f"_Last changed {month(now['updated'] + 'T00:00:00Z')}._"]

    posts = writing(content)
    if posts:
        parts += ["", "### Latest writing", "", *posts]

    try:
        work = shipped()
    except OSError as error:
        print(f"GitHub activity skipped: {error}", file=sys.stderr)
        work = []
    if work:
        parts += ["", "### Recently shipped", *work]

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
    readme = replace_block(readme, START, END, render(now, content), readme_path)
    readme = replace_block(readme, SITE_START, SITE_END, render_site(content), readme_path)
    readme_path.write_text(readme)


if __name__ == "__main__":
    main()
