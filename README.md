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

**[paseo](https://github.com/Patrick-Kappen/paseo)** · Orchestrate multiple coding agents from desktop and mobile

- ✨ **[Keep Nix builds from updating themselves](https://github.com/Patrick-Kappen/paseo/pull/3)** · Nov 2026 · +28 −1\
  Brings the change of #2 into azure-devops: #2 was merged into feat/azure-devops-forge after #1 had already been merged, so it never reached azure-devops.
- ✨ **[Keep Nix builds from updating themselves](https://github.com/Patrick-Kappen/paseo/pull/2)** · Nov 2026 · +28 −1\
  The Nix desktop package on macOS is a packaged Electron app, so the in-app updater would download the official release and replace the build, dropping the fork's changes until…
- ✨ **[Add an Azure DevOps forge adapter](https://github.com/Patrick-Kappen/paseo/pull/1)** · Nov 2026 · +2127 −0\
  Closes #

**[oxsecurity/megalinter](https://github.com/oxsecurity/megalinter)** · 🦙 MegaLinter analyzes 50 languages, 22 formats, 21 tooling formats, excessive copy-pastes, spelling mistakes and security issues in your repository sources with a GitHub Action, other CI tools or locally.

- 🐛 **[Honor SARIF_REPORTER_NORMALIZE_LINTERS_OUTPUT in combined SARIF report](https://github.com/oxsecurity/megalinter/pull/9338)** · Oct 2026 · +92 −3\
  The per-linter SARIF reports already check `SARIF_REPORTER_NORMALIZE_LINTERS_OUTPUT` before stripping the workspace prefix (`megalinter/utils_sarif.py`), but the combined report…
- 🐛 **[Count a linter stopped by a signal as failed (#9257)](https://github.com/oxsecurity/megalinter/pull/9258)** · Oct 2026 · +87 −2\
  Python gives a sub-process that a signal stops (for example an out-of-memory kill) a negative return code.

**[terraform-provider-azuredevops](https://github.com/Patrick-Kappen/terraform-provider-azuredevops)** · Terraform Azure DevOps provider

- ✨ **[Add repository Advanced Security resource](https://github.com/Patrick-Kappen/terraform-provider-azuredevops/pull/2)** · Oct 2026 · +835 −0\
  Adds `azuredevops_git_repository_advanced_security` to manage GitHub Advanced Security for Azure DevOps on a Git repository: Secret Protection (`secret_protection_enabled`,…

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
