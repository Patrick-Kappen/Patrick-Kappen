import { getCollection, getEntry, type CollectionEntry } from "astro:content";

export type TopicKey = string;
export type MachineKind = CollectionEntry<"machines">["data"]["kind"];
export type Site = CollectionEntry<"site">["data"];
export type MachineData = CollectionEntry<"machines">["data"];
export type Page = CollectionEntry<"pages">["data"] & { body: string };

export interface Topic {
  key: TopicKey;
  name: string;
  blurb: string;
  icon: string;
  hue: [string, string];
}

export interface Tool {
  id: string;
  name: string;
  logo?: string;
  highlight?: number;
  group: string;
}

export interface Machine extends Omit<MachineData, "drives" | "specs"> {
  id: string;
  specs: string[];
  drives: MachineData["drives"];
}

export interface Project {
  name: string;
  text: string;
  status: string;
  href: string;
}

export async function getSite(): Promise<Site> {
  const entry = await getEntry("site", "site");
  if (!entry) throw new Error("content/site.yaml is missing");
  return entry.data;
}

export async function getPage(id: string): Promise<Page> {
  const entry = await getEntry("pages", id);
  if (!entry) throw new Error(`content/pages/${id}.md is missing`);
  return { ...entry.data, body: entry.body ?? "" };
}

export async function getTopics(): Promise<Topic[]> {
  const entries = await getCollection("topics");
  return entries
    .sort((a, b) => a.data.order - b.data.order)
    .map((entry) => ({ key: entry.id, name: entry.data.name, blurb: entry.data.blurb, icon: entry.data.icon, hue: entry.data.hue }));
}

export async function getTopicMap(): Promise<Record<TopicKey, Topic>> {
  return Object.fromEntries((await getTopics()).map((topic) => [topic.key, topic]));
}

export async function getToolGroups() {
  const [groups, tools] = await Promise.all([getCollection("toolGroups"), getCollection("tools")]);
  const known = new Set(groups.map((group) => group.id));
  for (const tool of tools) {
    if (!known.has(tool.data.group)) throw new Error(`Tool ${tool.id} refers to the unknown group ${tool.data.group}`);
  }
  return groups
    .sort((a, b) => a.data.order - b.data.order)
    .map((group) => ({
    id: group.id,
    title: group.data.title,
    tools: tools
      .filter((tool) => tool.data.group === group.id)
      .sort((a, b) => a.data.order - b.data.order)
      .map((tool): Tool => ({ id: tool.id, ...tool.data })),
  }));
}

export async function getMachines(): Promise<Machine[]> {
  const entries = await getCollection("machines");
  return entries.sort((a, b) => a.data.order - b.data.order).map((entry) => ({ id: entry.id, ...entry.data }));
}

export async function getServices() {
  return (await getCollection("services")).sort((a, b) => a.data.order - b.data.order).map((entry) => ({ area: entry.data.area, value: entry.data.value }));
}

export async function getProjects(): Promise<Project[]> {
  const entries = await getCollection("projects");
  return entries
    .sort((a, b) => a.data.order - b.data.order)
    .map(({ data: { name, text, status, href } }) => ({ name, text, status, href }));
}
