import { topicKeys, type TopicKey } from "@content/data/topics";
import { publishedPosts } from "./posts";

export async function topicsWithPosts(): Promise<Set<TopicKey>> {
  const posts = await publishedPosts();
  return new Set(topicKeys.filter((key) => posts.some((post) => post.data.topic === key)));
}

export const topicHref = (key: TopicKey) => `/blog/topics/${key}/`;
