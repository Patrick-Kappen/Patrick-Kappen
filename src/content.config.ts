import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";
import { topicKeys, type TopicKey } from "@content/data/topics";

const blog = defineCollection({
  loader: glob({ base: "./content/blog", pattern: "**/*.md" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    topic: z.enum(topicKeys as [TopicKey, ...TopicKey[]]),
    tags: z.array(z.string()).default([]),
    image: z.string().optional(),
    imageAlt: z.string().default(""),
    imageCredit: z.string().optional(),
    imageCreditUrl: z.string().url().optional(),
    series: z.object({ name: z.string(), part: z.number().int().positive() }).optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
