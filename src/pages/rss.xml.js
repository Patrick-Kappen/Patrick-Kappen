import rss from "@astrojs/rss";
import { publishedPosts } from "../lib/posts";

export async function GET(context) {
  const posts = await publishedPosts();
  return rss({
    title: "Patrick Kappen",
    description: "Notes on platforms, identity, delivery and AI infrastructure.",
    site: context.site,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.date,
      link: `/blog/${post.id}/`,
    })),
  });
}
