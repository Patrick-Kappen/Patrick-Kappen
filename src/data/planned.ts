import type { TopicKey } from "./topics";

export interface PlannedPost {
  title: string;
  description: string;
  topic: TopicKey;
}

export const planned: PlannedPost[] = [];
