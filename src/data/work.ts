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
    tags: ["GitHub", "GitHub Actions", "Azure DevOps", "OIDC", "Entra ID"],
    problem: "Pipelines spread across Azure DevOps, with long-lived service principal secrets to store and rotate.",
    approach: "Moving repositories and pipelines to GitHub, replacing stored secrets with OIDC workload identity, and managing governance as code.",
    featured: true,
  },
  {
    title: "Least-privilege access across tenants",
    summary: "Scoped, delegated access with just-in-time elevation instead of standing admin rights, defined in Terraform together with the CISO.",
    context: "At SLTN",
    status: "In progress",
    topic: "identity",
    tags: ["Entra ID", "PIM", "Terraform", "Security"],
    problem: "Managing many customer tenants tends to accumulate broad, permanent admin rights.",
    approach: "Scoped, delegated access with just-in-time elevation and approval, defined in Terraform together with the CISO.",
    featured: true,
  },
  {
    title: "Disaster recovery you can prove",
    summary: "Automated test failovers in GitHub Actions that check machines come up and can reach each other, report the result and always clean up.",
    context: "At SLTN",
    status: "In use",
    topic: "azure",
    tags: ["Azure", "Site Recovery", "GitHub Actions"],
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
    tags: ["AI", "vLLM", "Python"],
    problem: "Model choices for agentic coding are usually based on leaderboards, not on the actual workload.",
    approach: "My own benchmarks for tool calling, long agent tasks, long context and concurrent agents, with vLLM serving tuned on measured numbers.",
    featured: true,
  },
  {
    title: "Graft",
    summary: "A few lines of TOML; Nix builds the root filesystem and generates the Podman Quadlet units. No hand-written boilerplate.",
    context: "Open source",
    status: "Alpha",
    topic: "containers",
    tags: ["Nix", "Rust", "Podman"],
    problem: "Containers on NixOS hosts need hand-written systemd units and ad-hoc package installs.",
    approach: "A few lines of TOML; Nix builds the root filesystem and generates the Podman Quadlet units.",
    link: "https://github.com/Patrick-Kappen/graft",
    featured: true,
  },
  {
    title: "Homelab & NixOS fleet",
    summary: "My machines at home, all declared in one Git repository and deployed from code. Next up: Kubernetes on NixOS, my own CI runners and a NAS.",
    context: "Personal",
    status: "In progress",
    topic: "homelab",
    tags: ["NixOS", "Nix", "deploy-rs", "sops"],
    problem: "Machines that are set up by hand drift apart, and after a while nobody remembers how they were built.",
    approach: "One flake for every machine, with shared server profiles, deploy-rs for roll-outs, a build cache, sops secrets with keys sealed to the TPM, and containers through Graft.",
  },
];

export const featuredWork = work.filter((item) => item.featured);
