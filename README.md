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
- **A backup you haven't restored is a rumour.** Recovery gets tested, or it isn't there.
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

- [Patrick-Kappen/graft#362](https://github.com/Patrick-Kappen/graft/pull/362): release: prepare 0.4.0-alpha.1 · Aug 2026
- [Patrick-Kappen/graft#357](https://github.com/Patrick-Kappen/graft/pull/357): fix(worker): keep relaxed user manifests loadable · Aug 2026
- [Patrick-Kappen/graft#355](https://github.com/Patrick-Kappen/graft/pull/355): fix(worker): finalize publication base-directory policy · Aug 2026
- [Patrick-Kappen/graft#319](https://github.com/Patrick-Kappen/graft/pull/319): feat(nix): install worker sockets and services · Aug 2026
- [Patrick-Kappen/graft#318](https://github.com/Patrick-Kappen/graft/pull/318): feat(nix): publish Home Manager user manifests atomically · Aug 2026

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
