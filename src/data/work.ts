import type { TopicKey } from "./topics";

export interface WorkImage {
  src: string;
  alt: string;
  width: number;
  height: number;
}

export interface Work {
  title: string;
  summary: string;
  context: string;
  status: string;
  topic: TopicKey;
  tags: string[];
  problem: string;
  approach: string;
  link?: string;
  image?: WorkImage;
  featured?: boolean;
}

export const work: Work[] = [
  {
    title: "GitHub and secret-free pipelines",
    summary: "Moving a whole organisation from Azure DevOps to GitHub, and replacing stored service principal secrets with OIDC workload identity on the way.",
    context: "At SLTN",
    status: "In progress",
    topic: "identity",
    tags: ["GitHub", "OIDC"],
    problem: "Pipelines spread across Azure DevOps, with long-lived service principal secrets to store and rotate.",
    approach: "Moving repositories and pipelines to GitHub, replacing stored secrets with OIDC workload identity, and managing governance as code.",
    featured: true,
  },
  {
    title: "Least-privilege access across tenants",
    summary: "Scoped, delegated access with just-in-time elevation instead of standing admin rights, defined in Terraform together with the CISO.",
    context: "At SLTN",
    status: "In progress",
    topic: "security",
    tags: ["Entra ID", "PIM"],
    problem: "Managing many customer tenants tends to accumulate broad, permanent admin rights.",
    approach: "Scoped, delegated access with just-in-time elevation and approval, defined in Terraform together with the CISO.",
    featured: true,
  },
  {
    title: "Disaster recovery you can prove",
    summary: "Automated test failovers in GitHub Actions that check machines come up and can reach each other, report the result and always clean up.",
    context: "At SLTN",
    status: "In use",
    topic: "recovery",
    tags: ["Azure", "ASR"],
    problem: "Recovery plans existed, but testing them was manual, slow and therefore rare.",
    approach: "Automated test failovers in GitHub Actions that check machines come up and can reach each other, report the result and always clean up.",
    featured: true,
  },
  {
    title: "Open models as coding agents",
    summary: "My own benchmarks for tool calling, long agent tasks, long context and concurrent agents, with vLLM serving tuned on measured numbers.",
    context: "Research",
    status: "Ongoing",
    topic: "ai",
    tags: ["vLLM", "Python"],
    problem: "Model choices for agentic coding are usually based on leaderboards, not on the actual workload.",
    approach: "My own benchmarks for tool calling, long agent tasks, long context and concurrent agents, with vLLM serving tuned on measured numbers.",
    featured: true,
  },
  {
    title: "Graft",
    summary: "A few lines of TOML; Nix builds the root filesystem and generates the Podman Quadlet units. No hand-written boilerplate.",
    context: "Open source",
    status: "Alpha",
    topic: "nix",
    tags: ["Rust", "Nix"],
    problem: "Containers on NixOS hosts need hand-written systemd units and ad-hoc package installs.",
    approach: "A few lines of TOML; Nix builds the root filesystem and generates the Podman Quadlet units.",
    link: "https://github.com/Patrick-Kappen/graft",
    image: { src: "/assets/graft-flow.svg", alt: "Graft workflow from TOML through Nix to a Podman Quadlet", width: 1280, height: 320 },
    featured: true,
  },
  {
    title: "Homelab & NixOS fleet",
    summary: "Where ideas get tested before they reach real work.",
    context: "Personal",
    status: "Running",
    topic: "nix",
    tags: ["Proxmox", "Talos", "NixOS"],
    problem: "Ideas need a place to be tested properly before they reach real work.",
    approach: "Proxmox, Talos Kubernetes and GitOps with 3-2-1 backups and monitoring; my own machines are a NixOS fleet rebuilt from Git with signed commits.",
    image: { src: "/assets/homelab-map.svg", alt: "Homelab map with edge, compute, storage and telemetry", width: 1280, height: 430 },
  },
];

export const featuredWork = work.filter((item) => item.featured);
