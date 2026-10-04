import sitemap from "@astrojs/sitemap";
import { existsSync, realpathSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { defineConfig } from "astro/config";

const contentPath = fileURLToPath(new URL("./content", import.meta.url));
if (!existsSync(contentPath)) {
  throw new Error(
    "The content directory is missing. Link a website_content worktree with: npm run content:link -- <path>, or: ln -sfn ../../website_content/main content",
  );
}
const content = realpathSync(contentPath);

export default defineConfig({
  site: "https://patrick.kappen.io",
  integrations: [sitemap()],
  markdown: {
    syntaxHighlight: "prism",
  },
  build: {
    inlineStylesheets: "never",
  },
  vite: {
    server: {
      fs: { allow: [".", content] },
    },
    build: {
      assetsInlineLimit: 0,
    },
  },
});
