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

**[pi-git](https://github.com/Patrick-Kappen/pi-git)** · pi extension that commits, pushes and opens PRs with a helper agent, and watches CI until the PR is green

- ✨ **[Lock git changes by default](https://github.com/Patrick-Kappen/pi-git/pull/5)** · Oct 2026 · +895 −18\
  Stacked on #4; merge that first.
- ✨ **[Add helper-assisted repository checks](https://github.com/Patrick-Kappen/pi-git/pull/4)** · Oct 2026 · +412 −6\
  Stacked on #3; merge that first.
- ✨ **[Add a PR watcher for CI and conflicts](https://github.com/Patrick-Kappen/pi-git/pull/3)** · Oct 2026 · +1640 −48\
  Stacked on #2; merge that first.
- ✨ **[Add guarded commit and PR workflow](https://github.com/Patrick-Kappen/pi-git/pull/2)** · Oct 2026 · +3912 −45\
  Add the `git_pr` tool to stage changes, run hooks, commit, push, and open or update a PR.

**[pi-skills](https://github.com/Patrick-Kappen/pi-skills)** · pi agent skills in a Nix flake, loaded per repository by the repo-skills extension

- ✨ **[Skill for git and GitHub work](https://github.com/Patrick-Kappen/pi-skills/pull/7)** · Oct 2026 · +390 −5\
  A `git` skill: rules and workflow for git and GitHub work, with references.

**[pi-rules](https://github.com/Patrick-Kappen/pi-rules)** · pi extension that applies rules per repository: instructions, permissions and hooks

- 🐛 **[Override minimatch to ^11.0.1 for GHSA-g3hv-75wg-m249](https://github.com/Patrick-Kappen/pi-rules/pull/5)** · Oct 2026 · +14 −5\
  minimatch 10.2.6 comes in through the `@earendil-works/pi-coding-agent` dev dependency, and `security` (osv-scanner) now fails on…

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
