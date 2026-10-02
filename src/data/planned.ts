import type { TopicKey } from "./topics";

export interface PlannedPost {
  title: string;
  description: string;
  topic: TopicKey;
}

export const planned: PlannedPost[] = [
  {
    title: "From secrets to OIDC: GitHub, Azure and Entra",
    description: "Why every stored pipeline secret is a liability, and how workload identity federation replaces them.",
    topic: "identity",
  },
  {
    title: "Least privilege for a CSP: GDAP, Lighthouse and PIM",
    description: "Getting rid of standing admin rights across customer tenants, and keeping it in code.",
    topic: "security",
  },
  {
    title: "Azure DevOps to GitHub: what doesn't migrate by itself",
    description: "The parts of a migration that tools don't cover, from service connections to governance.",
    topic: "delivery",
  },
  {
    title: "Proving disaster recovery with Azure Site Recovery",
    description: "Automated test failovers that check machines really come back, and always clean up.",
    topic: "recovery",
  },
  {
    title: "Choosing open models for coding agents on measured numbers",
    description: "Benchmarks for tool calling, long tasks and concurrency, instead of leaderboards.",
    topic: "ai",
  },
  {
    title: "Two GitHub accounts, one machine, zero switching",
    description: "I split my GitHub life in two and refused to switch accounts by hand ever again. Nix made it easy, git and gh made it interesting.",
    topic: "nix",
  },
];
