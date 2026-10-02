export interface Link {
  label: string;
  href: string;
}

export interface Tool {
  name: string;
  logo?: string;
}

export interface ToolGroup {
  title: string;
  tools: Tool[];
}

export interface Belief {
  title: string;
  body: string;
}

export interface Focus {
  title: string;
  icon: string;
  body: string;
  tags: string[];
}

export const profile = {
  name: "Patrick Kappen",
  firstName: "Patrick",
  role: "Platform & security engineer",
  title: "Senior DevOps Engineer",
  company: "SLTN",
  companyNote: "Azure Expert MSP",
  location: "the Netherlands",
  photo: "/assets/patrick.jpg",
  email: "patrick@kappen.io",
  tagline: "I build the platforms other people deploy to, and the guard rails around them.",
  intro:
    "Here I write about Azure, identity, delivery and AI infrastructure, and what I learn along the way.",
  short:
    "I build the platforms other people deploy to, and the guard rails around them. Azure, identity and delivery as code, and AI agents with boundaries.",
  certifications: ["AZ-900", "AZ-104", "AZ-400"],
  studying: ["GitHub Actions", "AI-103"],
  stack: [
    {
      title: "Cloud",
      tools: [
        { name: "Azure", logo: "/assets/logos/azure.svg" },
        { name: "AWS", logo: "/assets/logos/aws.svg" },
        { name: "Google Cloud", logo: "/assets/logos/google-cloud.svg" },
        { name: "IBM Cloud" },
        { name: "Cloudflare", logo: "/assets/logos/cloudflare.svg" },
      ],
    },
    {
      title: "Datacenter & virtualisation",
      tools: [
        { name: "Azure Local", logo: "/assets/logos/azure-local.svg" },
        { name: "Azure Arc", logo: "/assets/logos/azure-arc.svg" },
        { name: "Windows Server", logo: "/assets/logos/windows-server.svg" },
        { name: "Hyper-V", logo: "/assets/logos/hyper-v.svg" },
        { name: "Proxmox", logo: "/assets/logos/proxmox.svg" },
        { name: "HPE" },
      ],
    },
    {
      title: "Automation & delivery",
      tools: [
        { name: "Bicep", logo: "/assets/logos/bicep.svg" },
        { name: "Terraform", logo: "/assets/logos/terraform.svg" },
        { name: "Ansible", logo: "/assets/logos/ansible.svg" },
        { name: "PowerShell", logo: "/assets/logos/powershell.svg" },
        { name: "Bash", logo: "/assets/logos/bash.svg" },
        { name: "Git", logo: "/assets/logos/git.svg" },
        { name: "Azure DevOps", logo: "/assets/logos/azure-devops.svg" },
        { name: "GitHub Actions", logo: "/assets/logos/github-actions.svg" },
        { name: "GitHub Copilot", logo: "/assets/logos/github-copilot.svg" },
      ],
    },
    {
      title: "NixOS & deployment",
      tools: [
        { name: "NixOS", logo: "/assets/logos/nixos.svg" },
        { name: "Home Manager" },
        { name: "deploy-rs" },
        { name: "comin" },
        { name: "disko" },
      ],
    },
    {
      title: "Identity & secrets",
      tools: [
        { name: "Entra ID" },
        { name: "Authentik", logo: "/assets/logos/authentik.svg" },
        { name: "Keycloak", logo: "/assets/logos/keycloak.svg" },
        { name: "Pocket ID", logo: "/assets/logos/pocket-id.svg" },
        { name: "Vaultwarden", logo: "/assets/logos/vaultwarden.svg" },
        { name: "1Password", logo: "/assets/logos/1password.svg" },
        { name: "sops" },
      ],
    },
    {
      title: "Containers & orchestration",
      tools: [
        { name: "Podman", logo: "/assets/logos/podman.svg" },
        { name: "Docker", logo: "/assets/logos/docker.svg" },
        { name: "Kubernetes", logo: "/assets/logos/kubernetes.svg" },
        { name: "Helm", logo: "/assets/logos/helm.svg" },
        { name: "Argo CD", logo: "/assets/logos/argo-cd.svg" },
        { name: "Cilium", logo: "/assets/logos/cilium.svg" },
        { name: "Nomad", logo: "/assets/logos/nomad.svg" },
      ],
    },
    {
      title: "Networking",
      tools: [
        { name: "UniFi", logo: "/assets/logos/unifi.svg" },
        { name: "VLANs" },
        { name: "WireGuard", logo: "/assets/logos/wireguard.svg" },
        { name: "Tailscale", logo: "/assets/logos/tailscale.svg" },
        { name: "Technitium", logo: "/assets/logos/technitium.png" },
        { name: "Traefik", logo: "/assets/logos/traefik.svg" },
        { name: "Caddy", logo: "/assets/logos/caddy.svg" },
        { name: "Let's Encrypt", logo: "/assets/logos/lets-encrypt.svg" },
      ],
    },
    {
      title: "Storage & backup",
      tools: [
        { name: "TrueNAS", logo: "/assets/logos/truenas.svg" },
        { name: "OpenZFS", logo: "/assets/logos/openzfs.svg" },
        { name: "btrfs" },
        { name: "S3" },
        { name: "PostgreSQL", logo: "/assets/logos/postgresql.svg" },
        { name: "Borg", logo: "/assets/logos/borg.svg" },
        { name: "Proxmox Backup Server", logo: "/assets/logos/proxmox.svg" },
      ],
    },
    {
      title: "Monitoring",
      tools: [
        { name: "Prometheus", logo: "/assets/logos/prometheus.svg" },
        { name: "Grafana", logo: "/assets/logos/grafana.svg" },
        { name: "Loki", logo: "/assets/logos/loki.png" },
        { name: "Uptime Kuma", logo: "/assets/logos/uptime-kuma.svg" },
      ],
    },
    {
      title: "Self-hosted apps",
      tools: [
        { name: "Home Assistant", logo: "/assets/logos/home-assistant.svg" },
        { name: "Nextcloud", logo: "/assets/logos/nextcloud.svg" },
        { name: "Immich", logo: "/assets/logos/immich.svg" },
      ],
    },
    {
      title: "AI",
      tools: [
        { name: "Claude", logo: "/assets/logos/claude.svg" },
        { name: "Codex" },
        { name: "pi" },
        { name: "LiteLLM", logo: "/assets/logos/litellm.png" },
        { name: "Phoenix", logo: "/assets/logos/phoenix.svg" },
        { name: "Langfuse", logo: "/assets/logos/langfuse.svg" },
        { name: "vLLM", logo: "/assets/logos/vllm.svg" },
        { name: "llama.cpp" },
      ],
    },
    {
      title: "Workstation & languages",
      tools: [
        { name: "Hyprland", logo: "/assets/logos/hyprland.svg" },
        { name: "niri", logo: "/assets/logos/niri.svg" },
        { name: "Umbriel" },
        { name: "Neovim", logo: "/assets/logos/neovim.svg" },
        { name: "VS Code", logo: "/assets/logos/vscode.svg" },
        { name: "Dev Containers", logo: "/assets/logos/devcontainers.png" },
        { name: "tmux", logo: "/assets/logos/tmux.svg" },
        { name: "Python", logo: "/assets/logos/python.svg" },
        { name: "Go", logo: "/assets/logos/go.svg" },
        { name: "Rust", logo: "/assets/logos/rust.svg" },
        { name: "YAML", logo: "/assets/logos/yaml.svg" },
      ],
    },
  ] satisfies ToolGroup[],
  highlights: ["Azure", "Terraform", "Bicep", "GitHub Actions", "PowerShell", "NixOS", "Kubernetes", "Proxmox", "Grafana", "Claude"],
  links: [
    { label: "LinkedIn", href: "https://www.linkedin.com/in/patrick-kappen/" },
    { label: "GitHub", href: "https://github.com/Patrick-Kappen" },
    { label: "RSS", href: "/rss.xml" },
  ] satisfies Link[],
};

export const about = {
  headline: "and I like guard rails.",
  focusLine: "Azure platform, identity and delivery as code",
  paragraphs: [
    "I'm a **Senior DevOps Engineer at SLTN** in the Netherlands, working on our Azure cloud practice. My favourite moment in this job is when a manual, slightly scary process turns into a pull request that anyone on the team can read, review and repeat.",
    "Most of my evenings go into the same ideas in a different setting: a homelab I run like production, a NixOS fleet that rebuilds from Git, and a lot of experimenting with open AI models and how to let agents help without giving them the keys.",
    "I'm growing towards a **technical lead** role, where I can set direction on platform and security and help a team feel at home with this way of working.",
  ],
  focus: [
    {
      title: "Platform & delivery",
      icon: "M4 17 12 3l8 14-8 4-8-4Z M4 17l8-4 8 4M12 3v10",
      body: "Azure environments and landing zones defined in code, pipelines without stored secrets, and every change planned and approved before it is applied.",
      tags: ["Azure", "Terraform", "Bicep", "GitHub Actions"],
    },
    {
      title: "Identity & security",
      icon: "M12 3 4 7v6c0 4.5 3.4 7.6 8 8 4.6-.4 8-3.5 8-8V7l-8-4Z M9 12l2 2 4-4",
      body: "Least-privilege access across customer tenants, just-in-time elevation instead of standing admin rights, and security policy turned into automation.",
      tags: ["Entra ID", "PIM", "OIDC", "Zero Trust"],
    },
    {
      title: "AI infrastructure",
      icon: "M9 3h6v3H9z M5 6h14v12H5z M9 11h.01M15 11h.01M9 15h6M12 18v3",
      body: "Open models benchmarked and tuned as coding agents, and agents that work inside sandboxes with scoped access and human approval.",
      tags: ["vLLM", "LiteLLM", "Python", "Sandboxing"],
    },
  ] satisfies Focus[],
  beliefs: [
    { title: "If it isn't in Git, it doesn't exist.", body: "Portal clicks are drift with extra steps. If it matters, it is versioned and reviewed." },
    { title: "A backup you haven't restored is a rumour.", body: "Recovery is tested on a schedule, or it isn't really there." },
    { title: "Standing admin access is a bug.", body: "People, pipelines and agents get just enough rights, just in time, and lose them again." },
    { title: "AI agents get the intern treatment.", body: "A sandbox, a reviewer and no production keys. Useful work, inside clear boundaries." },
  ] satisfies Belief[],
  contact: {
    title: "Fancy a chat?",
    body: "Whether it's about platforms, identity, AI infrastructure or working together, drop me a line.",
  },
};

export const externalLink = (href: string) =>
  href.startsWith("http") ? { target: "_blank", rel: "noopener noreferrer" } : {};
