import type { TopicKey } from "./site";

export const upcoming: { title: string; description: string; topic: TopicKey; minutes: number }[] = [
  {
    title: "From secrets to OIDC: GitHub, Azure and Entra",
    description: "Why every stored pipeline secret is a liability, and how workload identity federation replaces them.",
    topic: "identity",
    minutes: 8,
  },
  {
    title: "Least privilege for a CSP: GDAP, Lighthouse and PIM",
    description: "Getting rid of standing admin rights across customer tenants, and keeping it in code.",
    topic: "security",
    minutes: 10,
  },
  {
    title: "Azure DevOps to GitHub: what doesn't migrate by itself",
    description: "The parts of a migration that tools don't cover, from service connections to governance.",
    topic: "delivery",
    minutes: 9,
  },
  {
    title: "Proving disaster recovery with Azure Site Recovery",
    description: "Automated test failovers that check machines really come back, and always clean up.",
    topic: "recovery",
    minutes: 7,
  },
  {
    title: "Choosing open models for coding agents on measured numbers",
    description: "Benchmarks for tool calling, long tasks and concurrency, instead of leaderboards.",
    topic: "ai",
    minutes: 12,
  },
  {
    title: "Why my NixOS fleet doesn't trust GitHub",
    description: "Signed commits, a trust anchor and a verifier between fetch and build.",
    topic: "nix",
    minutes: 8,
  },
];
