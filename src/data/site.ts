export const profile = {
  name: "Patrick Kappen",
  role: "Platform & security engineer",
  title: "Senior DevOps Engineer",
  company: "SLTN",
  companyNote: "Azure Expert MSP",
  location: "the Netherlands",
  photo: "/assets/patrick.jpg",
  email: "patrick@kappen.io",
  short:
    "I build the platforms other people deploy to, and the guard rails around them. Azure, identity and delivery as code, and AI agents with boundaries.",
  certifications: ["AZ-900", "AZ-104", "AZ-400"],
  studying: ["GitHub Actions", "AI-103"],
  stack: ["Azure", "Terraform", "Bicep", "GitHub Actions", "Entra ID", "Nix", "Kubernetes", "Python", "PowerShell", "vLLM"],
  links: [
    { label: "LinkedIn", href: "https://www.linkedin.com/in/patrick-kappen/" },
    { label: "GitHub", href: "https://github.com/Patrick-Kappen" },
    { label: "RSS", href: "/rss.xml" },
  ],
};

export type TopicKey = "identity" | "security" | "delivery" | "recovery" | "ai" | "nix";

export const topics: Record<TopicKey, { name: string; blurb: string; icon: string; hue: [string, string] }> = {
  identity: {
    name: "Identity",
    blurb: "OIDC, Entra ID and secret-free pipelines",
    icon: "M6 11h12v9H6z M8 11V8a4 4 0 0 1 8 0v3 M12 15v2",
    hue: ["#3cc8e8", "#7c9cff"],
  },
  security: {
    name: "Security",
    blurb: "Least privilege, PIM and just-in-time access",
    icon: "M12 3 4 7v6c0 4.5 3.4 7.6 8 8 4.6-.4 8-3.5 8-8V7l-8-4Z M9 12l2 2 4-4",
    hue: ["#7c9cff", "#b38cff"],
  },
  delivery: {
    name: "Delivery",
    blurb: "GitHub, pipelines and infrastructure as code",
    icon: "M4 17 12 3l8 14-8 4-8-4Z M4 17l8-4 8 4M12 3v10",
    hue: ["#3cc8e8", "#45e0b0"],
  },
  recovery: {
    name: "Recovery",
    blurb: "Disaster recovery you can actually prove",
    icon: "M4 12a8 8 0 1 0 2.3-5.7 M4 4v4h4",
    hue: ["#45e0b0", "#3cc8e8"],
  },
  ai: {
    name: "AI",
    blurb: "Open models, agents and benchmarks",
    icon: "M9 3h6v3H9z M5 6h14v12H5z M9 11h.01 M15 11h.01 M9 15h6",
    hue: ["#b38cff", "#3cc8e8"],
  },
  nix: {
    name: "Nix",
    blurb: "NixOS, flakes and reproducible machines",
    icon: "M12 2v20 M3.3 7l17.4 10 M20.7 7 3.3 17",
    hue: ["#7c9cff", "#3cc8e8"],
  },
};

export const projects = [
  {
    name: "Graft",
    note: "Open source · alpha",
    text: "Containers from a few lines of TOML, built by Nix.",
    href: "https://github.com/Patrick-Kappen/graft",
  },
  {
    name: "Homelab & NixOS fleet",
    note: "Personal",
    text: "Where ideas get tested before they reach real work.",
    href: "/about/#work",
  },
];
