import { getCollection, type CollectionEntry } from "astro:content";

export type Post = CollectionEntry<"blog">;

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
