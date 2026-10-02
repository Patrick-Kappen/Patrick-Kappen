export type TopicKey = "nix" | "homelab" | "containers" | "ai" | "azure" | "identity" | "delivery" | "workstation";

export const topics: Record<TopicKey, { name: string; blurb: string; icon: string; hue: [string, string] }> = {
  nix: {
    name: "NixOS",
    blurb: "The basics, flakes, my fleet and secrets",
    icon: "M12 2v20 M3.3 7l17.4 10 M20.7 7 3.3 17",
    hue: ["#7c9cff", "#3cc8e8"],
  },
  homelab: {
    name: "Homelab",
    blurb: "Hardware, the NAS, runners and Kubernetes",
    icon: "M4 4h16v6H4z M4 14h16v6H4z M8 7h.01 M8 17h.01",
    hue: ["#45e0b0", "#3cc8e8"],
  },
  containers: {
    name: "Containers",
    blurb: "Docker, Podman, Graft and Kubernetes",
    icon: "M12 3 3 7.5v9L12 21l9-4.5v-9L12 3Z M3 7.5 12 12l9-4.5 M12 12v9",
    hue: ["#3cc8e8", "#45e0b0"],
  },
  ai: {
    name: "AI",
    blurb: "LiteLLM, Phoenix, local models and agents",
    icon: "M9 3h6v3H9z M5 6h14v12H5z M9 11h.01 M15 11h.01 M9 15h6",
    hue: ["#b38cff", "#3cc8e8"],
  },
  azure: {
    name: "Azure",
    blurb: "Landing zones, Site Recovery and verified modules",
    icon: "M7 18a4 4 0 0 1-.6-8A6 6 0 0 1 18 9a4.5 4.5 0 0 1-.5 9Z",
    hue: ["#3cc8e8", "#7c9cff"],
  },
  identity: {
    name: "Identity & security",
    blurb: "OIDC, Entra ID, PIM and least privilege",
    icon: "M12 3 4 7v6c0 4.5 3.4 7.6 8 8 4.6-.4 8-3.5 8-8V7l-8-4Z M9 12l2 2 4-4",
    hue: ["#7c9cff", "#b38cff"],
  },
  delivery: {
    name: "Delivery",
    blurb: "GitHub, Actions and pipelines",
    icon: "M4 17 12 3l8 14-8 4-8-4Z M4 17l8-4 8 4M12 3v10",
    hue: ["#3cc8e8", "#45e0b0"],
  },
  workstation: {
    name: "Workstation",
    blurb: "niri, Neovim, dev shells and coding agents",
    icon: "M3 4h18v12H3z M8 20h8 M12 16v4",
    hue: ["#b38cff", "#7c9cff"],
  },
};

export const topicKeys = Object.keys(topics) as TopicKey[];
