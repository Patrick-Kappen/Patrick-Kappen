<!-- markdownlint-disable MD013 MD033 -->

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset=".github/assets/control-room-compact-dark.svg">
  <source media="(prefers-color-scheme: light) and (max-width: 600px)" srcset=".github/assets/control-room-compact-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/control-room-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/control-room-light.svg">
  <img src=".github/assets/control-room-light.svg" width="100%" alt="Patrick&#x27;s control room: a homelab rack and an AI robot trying to reach a locked production button.">
</picture>
</p>

<p align="center" id="intro">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/headings/intro-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/headings/intro-light.svg">
  <img src=".github/assets/headings/intro-light.svg" width="500" alt="Hey, I&#x27;m Patrick">
</picture>
</p>

<p align="center">
  <strong>I build the platforms other people deploy to.</strong><br>
  At home, I recreate the same problems with my own electricity bill.
</p>

<p align="center">
  <a href="https://patrick.kappen.io"><strong>🌍 Website</strong></a> &nbsp;·&nbsp;
  <a href="https://patrick.kappen.io/blog/">✍️ Blog</a> &nbsp;·&nbsp;
  <a href="https://www.linkedin.com/in/patrick-kappen/">💬 LinkedIn</a> &nbsp;·&nbsp;
  <a href="https://patrick.kappen.io/rss.xml">📡 RSS</a>
</p>

Senior DevOps, AI and security engineer at **SLTN**, an Azure Expert MSP.
My day job is Azure, identity and delivery as code: fewer portal clicks,
fewer standing admins, fewer secrets hiding in pipelines.

After hours: NixOS, a homelab with production ambitions, and open-weight
coding agents. The agents get a sandbox and a reviewer. Not the keys.

```nix
patrick = {
  infrastructure = "as code";
  agents.productionKeys = false;
  restores = "actually tested";
  "just-one-more-server" = true;
};
```

<!-- projects:start -->

<p align="center" id="projects">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/headings/projects-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/headings/projects-light.svg">
  <img src=".github/assets/headings/projects-light.svg" width="500" alt="Builds &amp; side quests">
</picture>
</p>

<p align="center">
<a href="https://github.com/Patrick-Kappen/PiG">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/project-1-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/project-1-light.svg">
  <img src=".github/assets/project-1-light.svg" width="270" alt="Patrick-Kappen/PiG: PiG (Pi in Go) is a faithful Go port of upstream Pi, the TypeScript codebase behind the Pi coding agent. It is a parity-bound translation, not a rewrite: upstream behavior is the contract, and Go is the implementation language.">
</picture>
</a>
<a href="https://github.com/Patrick-Kappen/paseo">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/project-2-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/project-2-light.svg">
  <img src=".github/assets/project-2-light.svg" width="270" alt="Patrick-Kappen/paseo: Orchestrate multiple coding agents from desktop and mobile">
</picture>
</a>
<a href="https://github.com/oxsecurity/megalinter">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/project-3-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/project-3-light.svg">
  <img src=".github/assets/project-3-light.svg" width="270" alt="oxsecurity/megalinter: 🦙 MegaLinter analyzes 50 languages, 22 formats, 21 tooling formats, excessive copy-pastes, spelling mistakes and security issues in your repository sources with a GitHub Action, other CI tools or locally.">
</picture>
</a>
</p>

<sub>Selected from recent public PRs and releases. Automatically refreshed 2026-11-13 · UTC.</sub>

<!-- projects:end -->

<details>
<summary><strong><img src=".github/assets/icons/rules.svg" width="20" height="20" align="middle" alt="" /> House rules (yes, the robots have to read these too)</strong></summary>

- **If it's not in Git, it doesn't exist.** Portal clicks are drift with extra steps.
- **Standing admin access is a bug.** Permissions should have an expiry date.
- **AI agents get the intern treatment.** A sandbox, a reviewer, no production keys.
- **Boring in production, interesting in design.** The exciting part should be the pull request.

I've watched an automated PR merge a feature, revert it, and still announce it
in the release notes. So yes, there is a reviewer.

</details>

<!-- auto:start -->

<p align="center" id="git-log">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/headings/git-log-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/headings/git-log-light.svg">
  <img src=".github/assets/headings/git-log-light.svg" width="500" alt="The Git log">
</picture>
</p>

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset=".github/assets/git-activity-compact-dark.svg">
  <source media="(prefers-color-scheme: light) and (max-width: 600px)" srcset=".github/assets/git-activity-compact-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/git-activity-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/git-activity-light.svg">
  <img src=".github/assets/git-activity-light.svg" width="100%" alt="Commits, opened PRs, merged PRs and reviews over 7, 30 and 365 days, plus the yearly contribution chart.">
</picture>

<p align="center" id="shipped">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/headings/shipped-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/headings/shipped-light.svg">
  <img src=".github/assets/headings/shipped-light.svg" width="420" alt="Recently shipped">
</picture>
</p>

<!-- shipped:start -->

- 🔧 **[Expose ordered input in tool_result handlers](https://github.com/Patrick-Kappen/PiG/pull/39)**<br><sub>PiG · Nov 2026</sub>
- ✨ **[Keep Nix builds from updating themselves](https://github.com/Patrick-Kappen/paseo/pull/3)**<br><sub>paseo · Nov 2026</sub>
- 🐛 **[Honor SARIF_REPORTER_NORMALIZE_LINTERS_OUTPUT in combined SARIF report](https://github.com/oxsecurity/megalinter/pull/9338)**<br><sub>oxsecurity/megalinter · Oct 2026</sub>

<!-- shipped:end -->

<p align="center" id="now">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/headings/now-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/headings/now-light.svg">
  <img src=".github/assets/headings/now-light.svg" width="500" alt="On the radar">
</picture>
</p>

- Studying for GitHub Actions and AI-103
- Building a blog on patrick.kappen.io

_Updated Oct 2026. Side quests subject to change._

<p align="center" id="writing">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/headings/writing-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/headings/writing-light.svg">
  <img src=".github/assets/headings/writing-light.svg" width="560" alt="Notes from the rabbit hole">
</picture>
</p>

- [Contributing to a Terraform provider: preparation](https://patrick.kappen.io/blog/contributing-to-a-terraform-provider-preparation/)
- [Two GitHub accounts, one machine, zero switching](https://patrick.kappen.io/blog/two-github-accounts-by-directory/)

<!-- auto:end -->

<!-- site:start -->

<p align="center" id="tools">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/headings/tools-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/headings/tools-light.svg">
  <img src=".github/assets/headings/tools-light.svg" width="500" alt="Things I reach for">
</picture>
</p>

<p>
  <img src="public/assets/logos/azure.svg" alt="Azure" title="Azure" width="36" height="36" /> &nbsp;
  <img src="public/assets/logos/terraform.svg" alt="Terraform" title="Terraform" width="36" height="36" /> &nbsp;
  <img src="public/assets/logos/bicep.svg" alt="Bicep" title="Bicep" width="36" height="36" /> &nbsp;
  <img src="public/assets/logos/github-actions.svg" alt="GitHub Actions" title="GitHub Actions" width="36" height="36" /> &nbsp;
  <img src="public/assets/logos/nixos.svg" alt="NixOS" title="NixOS" width="36" height="36" /> &nbsp;
  <img src="public/assets/logos/kubernetes.svg" alt="Kubernetes" title="Kubernetes" width="36" height="36" /> &nbsp;
  <img src="public/assets/logos/powershell.svg" alt="PowerShell" title="PowerShell" width="36" height="36" /> &nbsp;
  <img src="public/assets/logos/podman.svg" alt="Podman" title="Podman" width="36" height="36" /> &nbsp;
  <img src="public/assets/logos/litellm.png" alt="LiteLLM" title="LiteLLM" width="36" height="36" /> &nbsp;
  <img src="public/assets/logos/proxmox.svg" alt="Proxmox" title="Proxmox" width="36" height="36" /> &nbsp;
</p>

<details>
<summary><strong>The longer version, including the certificates</strong></summary>

<p align="center" id="toolbox">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/headings/toolbox-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/headings/toolbox-light.svg">
  <img src=".github/assets/headings/toolbox-light.svg" width="420" alt="Toolbox">
</picture>
</p>

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

<p align="center" id="certifications">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/headings/certifications-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/headings/certifications-light.svg">
  <img src=".github/assets/headings/certifications-light.svg" width="420" alt="Certifications">
</picture>
</p>

- **Certified:**
  [AZ-900](https://www.credly.com/badges/c864e7a2-1536-4183-9e0c-c5cd841b2088) ·
  [AZ-104](https://www.credly.com/badges/103f1099-a80a-4544-8c95-45b80edbf2ad) ·
  [AZ-400](https://www.credly.com/badges/5bd5f444-199c-4ee5-8177-43427a8ad8ce)
- **Working towards:** GitHub Actions · AI-103

</details>

<!-- site:end -->

<sub>Every change reviewed. Every restore tested. Every “quick experiment” suspicious.</sub>

<!-- markdownlint-enable MD013 MD033 -->
