# Patrick Kappen

```nix
{
  patrick = {
    role     = "Platform & security engineer";
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

- Moving a whole organisation from Azure DevOps to GitHub, with OIDC instead of stored secrets
- Turning GDAP, Lighthouse and PIM/JIT access into Terraform
- Studying for GitHub Actions and AI-103
- Building a blog on patrick.kappen.io

_Last changed Oct 2026._

### Recently shipped

**[graft](https://github.com/Patrick-Kappen/graft)** · TOML-driven Podman Quadlet containers, built from the Nix store.

- 🐛 **[Make rootless notify protocol fixture runnable](https://github.com/Patrick-Kappen/graft/pull/367)** · Aug 2026 · +22 −22\
  Install the protocol fixture's user services through `systemd.user.services`, avoiding the generated `/etc/systemd/user` collision.
- 🐛 **[Retain user Quadlet readiness through conmon handoff](https://github.com/Patrick-Kappen/graft/pull/366)** · Aug 2026 · +257 −30\
  Fixes the rootless Quadlet notify-attribution race that blocked the v0.4.0-alpha.1 release candidate.
- 🐛 **[Keep relaxed user manifests loadable](https://github.com/Patrick-Kappen/graft/pull/357)** · Aug 2026 · +366 −76\
  Keeps relaxed user manifest publication readable by the installed worker and prevents tolerated default ACLs from making newly created Graft directories unusable.
- 🐛 **[Finalize publication base-directory policy](https://github.com/Patrick-Kappen/graft/pull/355)** · Aug 2026 · +503 −141\
  Finalizes secure user publication directory handling while supporting NAS and permission-less filesystems through an explicit opt-in compatibility mode.
- ✨ **[Install worker sockets and services](https://github.com/Patrick-Kappen/graft/pull/319)** · Aug 2026 · +277 −14\
  Installs the documented system and user Graft worker services and sockets with fixed, Nix-expanded manifest paths, target/manager/UID policy, producer identity, and local-only…
- ✨ **[Publish Home Manager user manifests atomically](https://github.com/Patrick-Kappen/graft/pull/318)** · Aug 2026 · +260 −22\
  Implements Home Manager-only immutable manifest/endpoint publication through `$XDG_CONFIG_HOME/graft/current`, using its own validated user activation lock and atomic pointer…

<!-- auto:end -->
<!-- markdownlint-enable MD013 -->

## Toolbox

- **Cloud:** Azure · IBM Cloud · AWS · Proxmox
- **IaC & delivery:** Terraform/OpenTofu · Bicep · GitHub Actions · Azure
  DevOps · Ansible · Nix
- **Identity & security:** Entra ID · PIM/JIT · GDAP · Lighthouse · OIDC · Key
  Vault · SOPS
- **Containers:** Kubernetes · Talos · Podman/Quadlet · Docker · Helm
- **Code:** PowerShell · Python · TypeScript · Rust · Bash
- **AI:** vLLM · Ollama · llama.cpp · LiteLLM · LangGraph · Langfuse · Phoenix

## Certifications

- **Certified:** AZ-900 · AZ-104 · AZ-400
- **Working towards:** GitHub Actions · GitHub Administration · AI-103 (Azure AI
  Apps and Agents)
