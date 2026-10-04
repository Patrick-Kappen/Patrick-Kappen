import { getTopics, type TopicKey } from "./content";
import { publishedPosts } from "./posts";

export async function topicsWithPosts(): Promise<Set<TopicKey>> {
  const [posts, topics] = await Promise.all([publishedPosts(), getTopics()]);
  return new Set(topics.map((topic) => topic.key).filter((key) => posts.some((post) => post.data.topic === key)));
}

export const topicHref = (key: TopicKey) => `/blog/topics/${key}/`;
