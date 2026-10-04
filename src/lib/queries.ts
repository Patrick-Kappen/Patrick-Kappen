import { getCollection } from "astro:content";
import { fill } from "./text";
import {
  getMachines,
  getPage,
  getProjects,
  getSite,
  getToolGroups,
  getTopics,
  type Machine,
  type Page,
  type Tool,
} from "./content";
import { publishedPosts } from "./posts";

export { publishedPosts };

const words: Record<number, string> = { 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six" };

export async function allTools(): Promise<Tool[]> {
  return (await getToolGroups()).flatMap((group) => group.tools);
}

export async function toolCount(): Promise<number> {
  return (await allTools()).length;
}

export async function highlightTools(): Promise<Tool[]> {
  return (await allTools())
    .filter((tool) => tool.highlight !== undefined)
    .sort((a, b) => (a.highlight ?? 0) - (b.highlight ?? 0));
}

export async function topicsWithCounts(published: { topic: string }[]) {
  return (await getTopics()).map((topic) => ({
    ...topic,
    count: published.filter((card) => card.topic === topic.key).length,
  }));
}

export function driveLines(machine: Machine): string[] {
  return machine.drives.map((drive) => {
    if (drive.redundancy === "none") return `${drive.count} × ${drive.sizeTb} TB ${drive.type}`;
    const pairs = drive.count / 2;
    return `${drive.count} × ${drive.sizeTb} TB ${drive.type} in ${words[pairs] ?? pairs} mirrored ${pairs === 1 ? "pair" : "pairs"}`;
  });
}

export async function machineGroups(area: "desk" | "lab") {
  const machines = (await getMachines()).filter((machine) => machine.area === area);
  const groups: { title: string; machines: (Machine & { lines: string[] })[] }[] = [];
  for (const machine of machines) {
    let group = groups.find((candidate) => candidate.title === machine.group);
    if (!group) {
      group = { title: machine.group, machines: [] };
      groups.push(group);
    }
    group.machines.push({ ...machine, lines: [...machine.specs, ...driveLines(machine)] });
  }
  return groups;
}

export async function homelabFacts() {
  const [machines, site] = await Promise.all([getMachines(), getSite()]);
  const drives = machines.flatMap((machine) => machine.drives);
  const driveCount = drives.reduce((total, drive) => total + drive.count, 0);
  const storageTb = drives.reduce(
    (total, drive) => total + (drive.redundancy === "mirror" ? (drive.count * drive.sizeTb) / 2 : drive.count * drive.sizeTb),
    0,
  );
  const nodes = machines
    .filter((machine) => machine.kind === "cluster")
    .reduce((total, machine) => total + (machine.count ?? 1), 0);
  return { nixosMachines: site.nixosMachines, drives: driveCount, storageTb, nodes, facts: site.homelab };
}

export async function tokens(): Promise<Record<string, string | number>> {
  const [site, lab, tools, projects] = await Promise.all([getSite(), homelabFacts(), toolCount(), getProjects()]);
  return {
    name: site.name,
    firstName: site.firstName,
    role: site.role,
    title: site.title,
    company: site.company,
    companyNote: site.companyNote,
    location: site.location,
    email: site.email,
    tagline: site.tagline,
    intro: site.intro,
    studying: site.studying.join(" · "),
    nixos: lab.nixosMachines,
    drives: lab.drives,
    storageTb: lab.storageTb,
    nodes: lab.nodes,
    tools,
    certifications: site.certifications.length,
    projects: projects.length,
  };
}

export async function pageText(id: string, extra: Record<string, string | number> = {}) {
  const [page, base] = await Promise.all([getPage(id), tokens()]);
  const values = { ...base, ...(page.focusLine ? { focusLine: page.focusLine } : {}), ...extra };
  const f = (text: string, more: Record<string, string | number> = {}) => fill(text, { ...values, ...more });
  return { page, f, values };
}

export type { Page };

export interface Work {
  title: string;
  summary: string;
  context: string;
  status: string;
  topic: string;
  tags: string[];
  problem: string;
  approach: string;
  link?: string;
  image?: { src: string; alt: string; width: number; height: number };
  featured: boolean;
}

export async function workItems(): Promise<Work[]> {
  const entries = await getCollection("posts", (entry) => entry.data.kind === "work" && entry.data.status === "published");
  return entries
    .sort((a, b) => (a.data.order ?? 0) - (b.data.order ?? 0))
    .map(({ data }) => ({
      title: data.title,
      summary: data.description,
      context: data.context!,
      status: data.progress!,
      topic: data.topic,
      tags: data.tags,
      problem: data.problem!,
      approach: data.approach!,
      link: data.link,
      image: data.workImage,
      featured: data.featured,
    }));
}

export async function featuredWork(): Promise<Work[]> {
  return (await workItems()).filter((item) => item.featured);
}
