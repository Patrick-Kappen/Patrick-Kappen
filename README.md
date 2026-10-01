# Patrick Kappen

<!-- markdownlint-disable MD036 -->

**Platform & security engineer · Azure · Terraform · GitHub · Entra · Nix · AI infrastructure**

<!-- markdownlint-enable MD036 -->

I build platforms and the tooling around them. Identity, delivery, recovery and
AI infrastructure, all defined as code and all written by me: Terraform, Bicep,
PowerShell, Python, TypeScript, Rust and Nix.

What I care about most is what happens after the deploy. Can someone review the
change before it lands? Can we see what the system is doing? Can we rebuild it
from scratch when something breaks? And does every identity, whether it is a
person, a pipeline or an AI agent, have exactly the access it needs and nothing
more?

[patrick.kappen.io](https://patrick.kappen.io)

## At work

I am a Senior DevOps Engineer at **SLTN**, one of the largest Dutch Microsoft
partners and an Azure Expert MSP. I own the platform code that our cloud teams
and customer tenants run on, and I work closely with our CISO to turn security
policy into automation instead of documents.

Right now that means moving the whole organisation from Azure DevOps to GitHub,
and replacing every stored pipeline secret with OIDC workload identity on the
way. Customer access runs through GDAP, Azure Lighthouse and PIM with
just-in-time elevation, and GitHub, Entra and that access model are all
managed in Terraform, so a change to who can do what goes through a pull
request like any other change.

On top of that I build automated landing zones, so new customer environments
start standardised and policy-checked, and automated disaster recovery drills
with Azure Site Recovery. Those drills fail over the full recovery plan,
check that the machines actually come up and can reach each other, report the
result and always clean up afterwards. A recovery plan you have never tested is
only a hope.

## AI infrastructure

Outside my day job I work on running open models as coding agents, and on
making that measurable. I select and screen open-weight models, tune their
serving on vLLM with INT4 quantisation, speculative decoding and KV-cache
settings, and keep a production profile that is backed by measured numbers
rather than impressions.

To make those choices I wrote my own benchmark suite: tool calling, multi-step
agent tasks, long-context retrieval, coding quality and many agents working at
once. The goal is that the model follows the workload, not the leaderboard.
When the benchmarks turn up problems in vLLM itself, I write diagnostics patches
and issue reports.

The other half is keeping agents within bounds: sandboxed execution with
bubblewrap, scoped credentials, Git changes that a human approves before they
are promoted, and agent profiles declared with Nix so every setup is
reproducible.

## Platform & homelab

My homelab is run like production. Proxmox, Talos Kubernetes, Nomad, GitOps,
OpenTofu and Ansible on the platform side; TrueNAS, Proxmox Backup Server and
3-2-1 backups on a 10 Gbit backplane for storage; Prometheus, Grafana and Loki
to see what is going on.

My workstations and servers form a NixOS fleet. Secrets live in sops-nix, every
commit is SSH-signed, and the fleet is designed so that a compromised GitHub
account is not enough to get code onto it.

## Projects

**[Graft](https://github.com/Patrick-Kappen/graft)** turns a few lines of TOML
into Podman Quadlet containers built from the Nix store. You describe what a
container needs; Nix builds the root filesystem and generates the Quadlet units.
No hand-written boilerplate and no packages installed by hand inside a
container.

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
