import { getCollection, type CollectionEntry } from "astro:content";
import { planned } from "@content/data/planned";
import type { TopicKey } from "@content/data/topics";

export type Post = CollectionEntry<"blog">;

export interface Card {
  title: string;
  topic: TopicKey;
  href?: string;
  date?: string;
  minutes?: number;
  image?: string;
  description?: string;
}

export async function publishedPosts(): Promise<Post[]> {
  const posts = await getCollection(
    "blog",
    (post: Post) => import.meta.env.DEV || !post.data.draft,
  );
  return posts.sort(
    (a: Post, b: Post) => b.data.date.valueOf() - a.data.date.valueOf(),
  );
}

export function formatDate(date: Date): string {
  return date.toLocaleDateString("en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

export function readingMinutes(post: Post): number {
  const words = (post.body ?? "").split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(words / 220));
}

export async function blogIndex() {
  const posts = await publishedPosts();
  const titles = new Set(posts.map((post) => post.data.title));
  const published: Card[] = posts.map((post) => ({
    title: post.data.title,
    topic: post.data.topic,
    href: `/blog/${post.id}/`,
    date: `${formatDate(post.data.date)}${post.data.draft ? " · draft" : ""}`,
    minutes: readingMinutes(post),
    image: post.data.image,
    description: post.data.description,
  }));
  const upcoming: Card[] = planned
    .filter((item) => !titles.has(item.title))
    .map((item) => ({ title: item.title, topic: item.topic }));
  return { posts, published, upcoming };
}

export function tagSlug(tag: string): string {
  return tag.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
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
