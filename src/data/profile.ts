export interface Link {
  label: string;
  href: string;
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
  stack: ["Azure", "Terraform", "Bicep", "GitHub Actions", "Entra ID", "Nix", "Kubernetes", "Python", "PowerShell", "vLLM"],
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
