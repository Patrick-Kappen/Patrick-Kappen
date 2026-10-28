# Patrick Kappen

```nix
{
  patrick = {
    role     = "Senior DevOps, AI and security engineer";
    at       = "SLTN, Azure Expert MSP";
    builds   = [ "identity" "delivery" "recovery" "AI infrastructure" ];
    writes   = [ "Terraform" "Bicep" "PowerShell" "Python" "Rust" "Nix" ];
    believes = "every change reviewed, nobody over-privileged";
    home     = "https://patrick.kappen.io";
  };
}
```

I build the platforms other people deploy to, and the guard rails around them.
Most of my work sits where infrastructure, identity and automation meet, and
lately a good part of it is about letting AI agents in without handing them the
keys.

## Things I believe

- **If it's not in Git, it doesn't exist.** Portal clicks are drift with extra
  steps.
- **A backup you haven't restored is a rumour.** Recovery gets tested, or it
  isn't there.
- **Standing admin access is a bug, not a convenience.** Rights are granted just
  in time and expire on their own.
- **AI agents get the intern treatment.** A sandbox, a reviewer, and no
  production keys. I've watched an automated PR merge a feature, revert it, and
  still announce it in the release notes.
- **Boring in production, interesting in design.** The exciting part should be
  the pull request, not the incident.

## At work

At **SLTN** I own the platform code that our cloud teams and customer tenants
run on, and I work with our CISO to turn security policy into automation
instead of documents.

That currently means moving the whole organisation from Azure DevOps to GitHub
and swapping every stored pipeline secret for OIDC on the way. Customer access
runs through GDAP, Azure Lighthouse and PIM, all in Terraform, so changing who
can do what is a pull request like any other. Around that sit automated landing
zones and disaster recovery drills that fail over a full Azure Site Recovery
plan, prove the machines come back, and always clean up after themselves.

## After hours

**Open models as coding agents.** I pick, benchmark and tune open-weight
models on vLLM, with my own suite for tool calling, long agent tasks, long
context and many agents at once. Models are chosen on measured numbers for the
actual workload, not on a leaderboard.

**Agents with boundaries.** Sandboxed execution, scoped credentials,
human-approved Git promotion and agent setups declared in Nix, so every one of
them can be rebuilt and audited.

**A homelab run like production.** Proxmox, Talos Kubernetes, GitOps, OpenTofu
and Ansible; TrueNAS and Proxmox Backup Server with 3-2-1 backups on 10 Gbit;
Prometheus, Grafana and Loki watching it all. My machines are a NixOS fleet
with signed commits, built so that a compromised GitHub account can't push code
onto them.

**[Graft](https://github.com/Patrick-Kappen/graft)** turns a few lines of TOML
into Podman Quadlet containers built from the Nix store. Describe what the
container needs; Nix builds the rest.

<!-- markdownlint-disable MD013 -->
<!-- auto:start -->

### Now

- Studying for GitHub Actions and AI-103
- Building a blog on patrick.kappen.io

_Last changed Oct 2026._

### Latest writing

- [Contributing to a Terraform provider: preparation](https://patrick.kappen.io/blog/contributing-to-a-terraform-provider-preparation/)
- [Two GitHub accounts, one machine, zero switching](https://patrick.kappen.io/blog/two-github-accounts-by-directory/)

### Recently shipped

**[zerodawn-pi](https://github.com/Patrick-Kappen/zerodawn-pi)** · pi extensions: bash jobs in a PTY, compact git, recipes, context pruning, tidy UI

- 🚀 **[v0.19.1](https://github.com/Patrick-Kappen/zerodawn-pi/releases/tag/v0.19.1)** · Oct 2026 · release\
  /ide finds the Neovide window by its nvim socket; docs: add astra latency task and guard block measurement.
- 🚀 **[v0.19.0](https://github.com/Patrick-Kappen/zerodawn-pi/releases/tag/v0.19.0)** · Oct 2026 · release\
  projects: /switch picker, /ide pair, pi-tui-kit dependency; docs: split open work in TODO.md and BACKLOG.md.
- 🚀 **[v0.18.0](https://github.com/Patrick-Kappen/zerodawn-pi/releases/tag/v0.18.0)** · Oct 2026 · release\
  accept a rebuttal, fixed limit per user message; a step for the user is not an open point.

**[oxsecurity/megalinter](https://github.com/oxsecurity/megalinter)** · 🦙 MegaLinter analyzes 50 languages, 22 formats, 21 tooling formats, excessive copy-pastes, spelling mistakes and security issues in your repository sources with a GitHub Action, other CI tools or locally.

- 🐛 **[Honor SARIF_REPORTER_NORMALIZE_LINTERS_OUTPUT in combined SARIF report](https://github.com/oxsecurity/megalinter/pull/9338)** · Oct 2026 · +92 −3\
  The per-linter SARIF reports already check `SARIF_REPORTER_NORMALIZE_LINTERS_OUTPUT` before stripping the workspace prefix (`megalinter/utils_sarif.py`), but the combined report…

**[zerodawn-nvim](https://github.com/Patrick-Kappen/zerodawn-nvim)** · Neovim addons in Lua, packaged as a Nix flake

- 🚀 **[v0.1.2](https://github.com/Patrick-Kappen/zerodawn-nvim/releases/tag/v0.1.2)** · Oct 2026 · release\
  block a tmux switch once, not once for each hook.

**[zerodawn-tmux](https://github.com/Patrick-Kappen/zerodawn-tmux)** · tmux addons in shell, packaged as a Nix flake

- 🚀 **[v0.1.1](https://github.com/Patrick-Kappen/zerodawn-tmux/releases/tag/v0.1.1)** · Oct 2026 · release\
  start the agent as the window command, not as typed keys.

<!-- auto:end -->
<!-- markdownlint-enable MD013 -->

<!-- site:start -->

## Toolbox

- **Cloud:** Azure
- **Automation & delivery:** Terraform · Bicep · GitHub Actions · PowerShell ·
  Azure DevOps · Ansible
- **NixOS & deployment:** NixOS
- **Linux:** Ubuntu
- **Containers & orchestration:** Kubernetes · Podman
- **AI:** LiteLLM · Phoenix
- **Datacenter & virtualisation:** Proxmox
- **Networking:** Tailscale · Traefik
- **Storage & backup:** TrueNAS
- **Monitoring:** Grafana

## Certifications

- **Certified:**
  [AZ-900](https://www.credly.com/badges/c864e7a2-1536-4183-9e0c-c5cd841b2088) ·
  [AZ-104](https://www.credly.com/badges/103f1099-a80a-4544-8c95-45b80edbf2ad) ·
  [AZ-400](https://www.credly.com/badges/5bd5f444-199c-4ee5-8177-43427a8ad8ce)
- **Working towards:** GitHub Actions · AI-103

<!-- site:end -->
