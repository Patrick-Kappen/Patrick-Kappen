"""Original circuit-style profile pictograms, not recolored official brand assets."""

import html
from pathlib import Path

from profile_visuals import ASSETS, THEMES

TOOL_SIZE = 140
TOOL_HEIGHT = 104
TOOL_STEM = f"{ASSETS}/tools"

# Original artwork on the same 64px / 3px grid as the chapter icons. Names make
# the deliberately stylised symbols unambiguous; website brand logos stay intact.
TOOL_ICONS = {
    "azure": ("Azure", '<path d="m11 52 18-40h12L25 52zm17-16h13L52 52H28"/>'),
    "terraform": ("Terraform", '<path d="m9 8 18 10v20L9 28zm23 13 18-10v20L32 41zm-23 14 18 10v17L9 52z"/>'),
    "bicep": ("Bicep", '<path d="M23 10h-5v16l-7 6 7 6v16h5M41 10h5v16l7 6-7 6v16h-5M27 38l10-12"/>'),
    "github-actions": ("GitHub Actions", '<rect x="6" y="7" width="18" height="18"/><rect x="40" y="8" width="17" height="17"/><rect x="40" y="40" width="17" height="17"/><path d="M24 16h16M15 25v23h25m-25-9h15V16m15 30 4 4 5-7"/>'),
    "nixos": ("NixOS", ''.join(f'<g transform="rotate({angle} 32 32)"><path d="M32 8v48m-9-42 9 6 9-6m-18 36 9-6 9 6"/></g>' for angle in (0, 60, 120))),
    "kubernetes": ("Kubernetes", '<circle cx="32" cy="32" r="23"/><circle cx="32" cy="32" r="9"/>' + ''.join(f'<path d="M32 9v14" transform="rotate({angle} 32 32)"/>' for angle in range(0, 360, 45))),
    "powershell": ("PowerShell", '<path d="M8 11h48v42H8zm12 13 11 8-11 8m17 2h10"/>'),
    "podman": ("Podman", '<path d="m10 19 22-10 22 10v27L32 57 10 46zm0 0 22 11 22-11M32 30v27M18 34v7m28-7v7"/>'),
    "litellm": ("LiteLLM", '<path d="M15 10h34v23H32l-9 8v-8h-8zm17 31v12M10 53h44M10 48v10m44-10v10"/><circle cx="25" cy="22" r="2"/><circle cx="39" cy="22" r="2"/>'),
    "proxmox": ("Proxmox", '<rect x="9" y="9" width="46" height="18"/><rect x="9" y="37" width="46" height="18"/><path d="M17 18h15m-15 28h15M45 16v4m0 24v4M25 27l14 10m0-10L25 37"/>'),
    "ubuntu": ("Ubuntu", '<circle cx="32" cy="32" r="17"/><circle cx="32" cy="8" r="4"/><circle cx="11" cy="44" r="4"/><circle cx="53" cy="44" r="4"/><path d="M32 12v3M15 42l3-2m28 0 3 2"/>'),
    "azure-devops": ("Azure DevOps", '<path d="M32 22c-11-15-25-9-25 10s14 25 25 10l9-14c11-15 16-10 16 4s-8 20-16 10L23 22"/>'),
    "ansible": ("Ansible", '<circle cx="32" cy="32" r="25"/><path d="m18 49 14-34 15 34-24-14"/>'),
    "phoenix": ("Phoenix", '<path d="M33 6c2 17 15 16 15 31a16 16 0 0 1-32 0c0-8 5-15 9-18-1 10 2 13 6 15-3-12 7-14 2-28zm-6 34c-4 5-1 12 5 12s9-7 4-13"/>'),
    "grafana": ("Grafana", '<path d="m14 41-7-8 8-8-1-10 12-2 6-7 8 6 11 2 1 11 6 8-7 8"/><circle cx="32" cy="36" r="17"/><path d="M22 40a11 11 0 0 1 20 0M32 39l8-12"/>'),
    "truenas": ("TrueNAS", '<ellipse cx="32" cy="14" rx="22" ry="8"/><path d="M10 14v36c0 10 44 10 44 0V14M10 31c0 10 44 10 44 0M10 47c0 10 44 10 44 0"/>'),
    "tailscale": ("Tailscale", ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="currentColor"/>' for y in (16, 32, 48) for x in (16, 32, 48))),
    "traefik": ("Traefik", '<rect x="24" y="6" width="16" height="16"/><rect x="7" y="43" width="16" height="15"/><rect x="41" y="43" width="16" height="15"/><path d="M32 22v10H15v11m17-11h17v11m-38-5 4 5 4-5m26 0 4 5 4-5"/>'),
    "entra-id": ("Entra ID", '<path d="m32 6 25 26-25 26L7 32zm-25 26h12m26 0h12"/><circle cx="32" cy="26" r="6"/><path d="M22 43v-4c0-10 20-10 20 0v4"/>'),
    "home-manager": ("Home Manager", '<path d="M6 28 32 7l26 21M13 24v33h38V24M25 57V38h14v19M26 26h12m-6-6v12"/>'),
    "sops": ("sops", '<path d="M15 6h25l10 10v42H15zm25 0v12h10"/><rect x="22" y="32" width="21" height="17"/><path d="M26 32v-6a7 7 0 0 1 14 0v6M32 39v4"/>'),
    "llama-cpp": ("llama.cpp", '<path d="M18 56V30L10 19l4-13 9 15 5-15h7l3 16 14 5v12l-15 4v13M39 35h12"/><circle cx="42" cy="29" r="1" fill="currentColor"/>'),
    "codex": ("Codex", '<path d="M7 10h50v44H7zm0 11h50M23 30l-8 7 8 7m18-14 8 7-8 7M35 29l-6 17"/>'),
    "pi": ("pi", '<path d="M12 19h41M23 19v27c0 7-4 10-9 10M43 19v30c0 5 4 7 9 5M12 19l4-8h36"/>'),
    "pig": ("PiG", '<path d="m14 23-4-14 17 8m23 6 4-14-17 8"/><ellipse cx="32" cy="35" rx="23" ry="20"/><rect x="22" y="34" width="20" height="13" rx="4"/><circle cx="22" cy="27" r="1" fill="currentColor"/><circle cx="42" cy="27" r="1" fill="currentColor"/><path d="M28 39v3m8-3v3"/>'),
}


def render_tool_svg(key, theme="dark"):
    name, artwork = TOOL_ICONS[key]
    palette = THEMES[theme]
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{TOOL_SIZE}" height="{TOOL_HEIGHT}" '
        f'viewBox="0 0 {TOOL_SIZE} {TOOL_HEIGHT}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{html.escape(name)}</title>',
        f'<desc id="desc">Original orange circuit-style profile pictogram for {html.escape(name)}; not an official brand logo.</desc>',
        f'<g transform="translate(44 8) scale(.8125)" fill="none" stroke="{palette["accent"]}" '
        f'color="{palette["accent"]}" stroke-width="3" stroke-linecap="square" stroke-linejoin="miter">',
        artwork,
        '</g>',
        f'<text x="70" y="85" text-anchor="middle" fill="{palette["text"]}" '
        f'font-family="Noto Sans, Arial, sans-serif" font-size="13" font-weight="600">{html.escape(name)}</text>',
        '</svg>',
    ]) + "\n"


def update_tool_icons(root):
    """Render every theme before touching files; only manage our own asset folder."""
    rendered = {f"{key}-{theme}.svg": render_tool_svg(key, theme)
                for key in TOOL_ICONS for theme in THEMES}
    folder = Path(root) / TOOL_STEM
    folder.mkdir(parents=True, exist_ok=True)
    for name, svg in rendered.items():
        (folder / name).write_text(svg)
    for path in folder.glob("*.svg"):
        if path.name not in rendered:
            path.unlink()
