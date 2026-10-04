import { defineCollection } from "astro:content";
import { file, glob } from "astro/loaders";
import { z } from "astro/zod";

const posts = defineCollection({
  loader: glob({ base: "./content/posts", pattern: "**/*.md" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    kind: z.enum(["post", "work"]),
    status: z.enum(["draft", "planned", "published"]),
    date: z.coerce.date().optional(),
    topic: z.string(),
    tags: z.array(z.string()).default([]),
    image: z.string().optional(),
    imageAlt: z.string().default(""),
    imageCredit: z.string().optional(),
    imageCreditUrl: z.string().url().optional(),
    series: z.object({ name: z.string(), part: z.number().int().positive() }).optional(),
    order: z.number().optional(),
    context: z.string().optional(),
    progress: z.string().optional(),
    problem: z.string().optional(),
    approach: z.string().optional(),
    link: z.string().optional(),
    workImage: z.object({ src: z.string(), alt: z.string(), width: z.number(), height: z.number() }).optional(),
    featured: z.boolean().default(false),
  }).superRefine((data, context) => {
    if (data.kind === "post" && data.status !== "planned" && !data.date) {
      context.addIssue({ code: "custom", message: "A post that is not planned needs a date", path: ["date"] });
    }
    if (data.kind === "work" && !(data.context && data.progress && data.problem && data.approach)) {
      context.addIssue({ code: "custom", message: "Work needs context, progress, problem and approach", path: ["kind"] });
    }
  }),
});

const topics = defineCollection({
  loader: glob({ base: "./content/topics", pattern: "*.yaml" }),
  schema: z.object({
    order: z.number(),
    name: z.string(),
    blurb: z.string(),
    icon: z.string(),
    hue: z.tuple([z.string(), z.string()]),
  }),
});

const toolGroups = defineCollection({
  loader: file("content/tool-groups.yaml"),
  schema: z.object({ order: z.number(), title: z.string() }),
});

const tools = defineCollection({
  loader: file("content/tools.yaml"),
  schema: z.object({
    order: z.number(),
    name: z.string(),
    group: z.string(),
    logo: z.string().optional(),
    highlight: z.number().int().positive().optional(),
  }),
});

const machines = defineCollection({
  loader: glob({ base: "./content/machines", pattern: "*.yaml" }),
  schema: z.object({
    order: z.number(),
    area: z.enum(["desk", "lab"]),
    group: z.string(),
    name: z.string(),
    kind: z.enum(["desktop", "laptop", "handheld", "server", "nas", "cluster", "gpu", "network"]),
    role: z.string(),
    specs: z.array(z.string()).default([]),
    os: z.string(),
    status: z.string().optional(),
    count: z.number().int().positive().optional(),
    drives: z
      .array(
        z.object({
          count: z.number().int().positive(),
          sizeTb: z.number().positive(),
          type: z.string(),
          redundancy: z.enum(["mirror", "none"]),
        }),
      )
      .default([]),
  }),
});

const services = defineCollection({
  loader: file("content/services.yaml"),
  schema: z.object({ order: z.number(), area: z.string(), value: z.string() }),
});

const projects = defineCollection({
  loader: glob({ base: "./content/projects", pattern: "*.yaml" }),
  schema: z.object({
    order: z.number(),
    name: z.string(),
    text: z.string(),
    status: z.string(),
    href: z.string(),
  }),
});

const link = z.object({ label: z.string(), href: z.string() });

const site = defineCollection({
  loader: glob({ base: "./content", pattern: "site.yaml" }),
  schema: z.object({
    name: z.string(),
    firstName: z.string(),
    role: z.string(),
    title: z.string(),
    company: z.string(),
    companyNote: z.string(),
    location: z.string(),
    photo: z.string(),
    email: z.string(),
    tagline: z.string(),
    intro: z.string(),
    short: z.string(),
    certifications: z.array(z.string()),
    studying: z.array(z.string()),
    links: z.array(link),
    nixosMachines: z.number().int().positive(),
    homelab: z.array(z.object({ label: z.string(), value: z.string() })),
    now: z.object({ updated: z.string(), now: z.array(z.string()), feed: z.string() }),
  }),
});

const pages = defineCollection({
  loader: glob({ base: "./content/pages", pattern: "*.md" }),
  schema: z.object({
    title: z.string().optional(),
    description: z.string().optional(),
    eyebrow: z.string().optional(),
    heading: z.string().optional(),
    lead: z.string().optional(),
    focusLine: z.string().optional(),
    stats: z.array(z.object({ value: z.string(), label: z.string() })).default([]),
    facts: z.array(z.object({ label: z.string(), value: z.string() })).default([]),
    sections: z
      .array(z.object({ id: z.string(), label: z.string(), topic: z.string(), text: z.string() }))
      .default([]),
    focus: z
      .array(z.object({ title: z.string(), topic: z.string(), icon: z.string(), body: z.string(), tags: z.array(z.string()) }))
      .default([]),
    beliefs: z.array(z.object({ title: z.string(), body: z.string() })).default([]),
    elsewhere: z.array(z.object({ title: z.string(), text: z.string(), href: z.string() })).default([]),
    reasons: z.array(z.object({ title: z.string(), text: z.string() })).default([]),
    actions: z
      .array(z.object({ label: z.string(), href: z.string(), primary: z.boolean().default(false), arrow: z.boolean().default(false) }))
      .default([]),
    nav: z.array(z.object({ label: z.string(), href: z.string(), match: z.string() })).default([]),
    labels: z.record(z.string(), z.string()).default({}),
  }),
});

export const collections = { posts, topics, toolGroups, tools, machines, services, projects, site, pages };
