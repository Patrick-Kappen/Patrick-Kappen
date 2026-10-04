import sitemap from "@astrojs/sitemap";
import { realpathSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { defineConfig } from "astro/config";

const content = realpathSync(fileURLToPath(new URL("./content", import.meta.url)));

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
    resolve: {
      alias: { "@content": content },
    },
    server: {
      fs: { allow: [".", content] },
    },
    build: {
      assetsInlineLimit: 0,
    },
  },
});
