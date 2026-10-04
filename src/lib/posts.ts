import { getCollection, type CollectionEntry } from "astro:content";
import { getTopics, type TopicKey } from "./content";
import { formatDate, tagSlug } from "./format";

export type Post = CollectionEntry<"posts"> & { data: { date: Date } };

export interface Card {
  title: string;
  topic: TopicKey;
  href?: string;
  date?: string;
  minutes?: number;
  image?: string;
  description?: string;
}

async function checkedPosts(filter: (post: CollectionEntry<"posts">) => boolean) {
  const [posts, topics] = await Promise.all([getCollection("posts", filter), getTopics()]);
  const known = new Set(topics.map((topic) => topic.key));
  for (const post of posts) {
    if (!known.has(post.data.topic)) throw new Error(`${post.id} refers to the unknown topic ${post.data.topic}`);
  }
  return posts;
}

export async function publishedPosts(): Promise<Post[]> {
  const posts = (await checkedPosts(
    (post) => post.data.kind === "post" && (import.meta.env.DEV ? post.data.status !== "planned" : post.data.status === "published"),
  )) as Post[];
  return posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

export function readingMinutes(post: Post): number {
  const words = (post.body ?? "").split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(words / 220));
}

export function postDate(post: Post, draftLabel: string): string {
  return `${formatDate(post.data.date)}${post.data.status === "draft" ? ` · ${draftLabel}` : ""}`;
}

export async function blogIndex(draftLabel = "draft") {
  const posts = await publishedPosts();
  const published: Card[] = posts.map((post) => ({
    title: post.data.title,
    topic: post.data.topic,
    href: `/blog/${post.id}/`,
    date: postDate(post, draftLabel),
    minutes: readingMinutes(post),
    image: post.data.image,
    description: post.data.description,
  }));
  const planned = await checkedPosts((post) => post.data.kind === "post" && post.data.status === "planned");
  const upcoming: Card[] = planned.map((item) => ({ title: item.data.title, topic: item.data.topic }));
  return { posts, published, upcoming };
}

export async function postsByTag() {
  const posts = await publishedPosts();
  const tags = new Map<string, { name: string; posts: Post[] }>();
  for (const post of posts) {
    for (const tag of post.data.tags) {
      const slug = tagSlug(tag);
      const entry = tags.get(slug) ?? { name: tag, posts: [] };
      entry.posts.push(post);
      tags.set(slug, entry);
    }
  }
  return tags;
}

export async function seriesFor(post: Post) {
  const series = post.data.series;
  if (!series) return undefined;
  const posts = (await publishedPosts())
    .filter((other) => other.data.series?.name === series.name)
    .sort((a, b) => (a.data.series?.part ?? 0) - (b.data.series?.part ?? 0));
  const index = posts.findIndex((other) => other.id === post.id);
  return {
    name: series.name,
    part: series.part,
    parts: posts.map((other) => ({ title: other.data.title, href: `/blog/${other.id}/`, part: other.data.series?.part ?? 0, current: other.id === post.id })),
    previous: index > 0 ? posts[index - 1] : undefined,
    next: index >= 0 && index < posts.length - 1 ? posts[index + 1] : undefined,
  };
}
