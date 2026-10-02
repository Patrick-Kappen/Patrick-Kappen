import sitemap from "@astrojs/sitemap";
import { defineConfig } from "astro/config";

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
    build: {
      assetsInlineLimit: 0,
    },
  },
});
