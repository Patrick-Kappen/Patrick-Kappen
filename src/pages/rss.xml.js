import rss from "@astrojs/rss";
import { getSite } from "../lib/content";
import { publishedPosts } from "../lib/posts";

export async function GET(context) {
  const profile = await getSite();
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
