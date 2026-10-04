import { labStats, nixosMachines } from "@content/data/hardware";
import { homelab, profile } from "@content/data/profile";
import { topicKeys, topics } from "@content/data/topics";
import { publishedPosts } from "./posts";

export { publishedPosts };

export const allTools = profile.stack.flatMap((group) => group.tools);

export const toolCount = allTools.length;

export function homelabFacts() {
  return { nixosMachines, facts: homelab, stats: labStats };
}

export function topicsWithCounts(published: { topic: string }[]) {
  return topicKeys.map((key) => ({
    key,
    ...topics[key],
    count: published.filter((card) => card.topic === key).length,
  }));
}
