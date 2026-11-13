"""Factual public-work summaries and a varied, linked work log; no generated claims."""

import html
import re
from collections import Counter
from datetime import datetime

WORK_LIMIT = 8
WORK_PER_REPO = 2


def summary_from_body(body):
    """Quote a short prose excerpt from GitHub, never infer outcomes or productivity."""
    if not isinstance(body, str):
        return ""
    body = re.sub(r"<!--[\s\S]*?-->", "", body)
    sections, current, fenced = {"": []}, "", False
    for line in body.splitlines():
        if re.match(r"^\s*(```|~~~)", line):
            fenced = not fenced
            continue
        if fenced:
            continue
        heading = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if heading:
            current = re.sub(r"[^a-z ]", "", heading[1].casefold()).strip()
            sections.setdefault(current, [])
        else:
            sections[current].append(line)
    order = ("summary", "what changed", "whats changed", "description", "problem and outcome", "")
    for section in order:
        paragraphs = re.split(r"\n\s*\n", "\n".join(sections.get(section, [])))
        if section == "problem and outcome":
            paragraphs.reverse()  # These descriptions usually finish with the actual outcome.
        for paragraph in paragraphs:
            lines = [line.strip() for line in paragraph.splitlines() if line.strip()]
            lines = [line for line in lines if not re.match(
                r"(?i)^(tracking\s*:|independent check\s*:|brings the change of #|cherry-picks?\b|(?:fixes|closes|resolves|related)\b|https?://|[-*] \[[ xX]\])", line)]
            value = " ".join(lines)
            value = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", value)
            value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
            value = re.sub(r"`([^`]+)`", lambda match: html.escape(match[1], quote=False), value)
            value = re.sub(r"<(script|style)\b[^>]*>[\s\S]*?</\1>", "", value, flags=re.IGNORECASE)
            value = re.sub(r"<[^>]*>", "", value)
            for pattern in (r"\*\*(.+?)\*\*", r"__(.+?)__", r"(?<!\w)\*([^*]+)\*(?!\w)"):
                value = re.sub(pattern, r"\1", value)
            value = re.sub(r"^[-*+]\s+", "", value)
            value = " ".join(html.unescape(value).split())
            if len(value) < 30:
                continue
            if len(value) > 280:
                value = value[:277].rsplit(" ", 1)[0].rstrip(".,;:") + "…"
            return value
    return ""


def recent_entries(entries, limit=WORK_LIMIT, per_repo=WORK_PER_REPO):
    selected, seen, seen_titles, counts = [], set(), set(), Counter()
    for entry in sorted(entries, key=lambda item: item["when"], reverse=True):
        repo, url = entry["repo"], entry["url"]
        key = (repo.casefold(), "/releases/" in url, entry["title"].casefold())
        if (entry.get("state") == "open" or url in seen or key in seen_titles
                or counts[repo.casefold()] >= per_repo):
            continue
        selected.append(entry)
        seen.add(url)
        seen_titles.add(key)
        counts[repo.casefold()] += 1
        if len(selected) == limit:
            break
    return selected


def render_work_log(entries, limit=WORK_LIMIT):
    lines = []
    for entry in recent_entries(entries, limit=limit):
        release = "/releases/" in entry["url"]
        kind = "RELEASE" if release else "MERGED PR"
        number = re.search(r"/pull/(\d+)(?:$|[?#])", entry["url"])
        if number and not release:
            kind += f" #{number[1]}"
        when = datetime.fromisoformat(entry["when"].replace("Z", "+00:00"))
        title = html.escape(entry["title"])
        url, repo = html.escape(entry["url"], quote=True), html.escape(entry["repo"])
        block = (f'<p><strong>{kind}</strong> · <code>{repo}</code> · {when.strftime("%d %b %Y")}<br>'
                 f'<a href="{url}"><strong>{title}</strong></a>')
        if entry.get("summary"):
            block += "<br>" + html.escape(entry["summary"])
        lines.append(block + "</p>")
    return lines
