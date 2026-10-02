import rss from "@astrojs/rss";
import { profile } from "../data/profile";
import { publishedPosts } from "../lib/posts";

export async function GET(context) {
  const posts = await publishedPosts();
  return rss({
    title: profile.name,
    description: profile.intro,
    site: context.site,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.date,
      link: `/blog/${post.id}/`,
    })),
  });
}
