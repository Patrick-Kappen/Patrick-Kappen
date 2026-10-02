# Website development and deployment

This is a static Astro website configured for the `patrickkappen` Cloudflare
Worker using Static Assets.

## Local development

Requires Node.js 22 or newer.

```bash
npm install
npm run dev
```

Astro will print the local URL. Create and inspect a production build with:

```bash
npm run build
npm run preview
```

The production output is written to `dist/`.

## Content

All text lives in data files; the pages only lay it out. A section disappears
when its list is empty.

| File | What it holds |
|---|---|
| `src/data/profile.ts` | Name, role, intro, photo, links, certifications, stack, and the About page text, focus, beliefs and contact |
| `src/data/topics.ts` | Topics with name, short description, icon and colours |
| `src/data/work.ts` | Work items; `featured` ones also appear on the home page |
| `src/data/planned.ts` | Planned posts, shown as "Coming up" until a post with the same title is published |
| `now.json` | The Now list in the sidebar, also used by the profile README |
| `src/content/blog/*.md` | Blog posts |

Posts have `title`, `description`, `date`, `topic`, `tags` and `draft` in the
front matter. Drafts show up in `npm run dev` but are left out of production
builds and the RSS feed. Reading time is calculated from the text.

## Deploy through Cloudflare

The connected Cloudflare build should use:

- Build command: `npm run build`
- Deploy command: `npx wrangler deploy`
- Node.js version: `22`

The `assets.directory` setting in `wrangler.jsonc` tells Wrangler to upload
`dist/` as the Worker's static assets. The custom-domain route provisions
`patrick.kappen.io`, including its Cloudflare DNS record and TLS certificate.
Cloudflare will build and deploy every new commit automatically.

To redirect plain HTTP requests to HTTPS, enable **SSL/TLS > Edge Certificates >
Always Use HTTPS** for the `kappen.io` zone. This setting applies to the entire
zone; use a hostname-specific Redirect Rule instead if other hostnames must keep
serving HTTP.

## Local DNS

The public hostname must resolve through Cloudflare. If a local authoritative
DNS zone or wildcard sends `*.kappen.io` to the homelab proxy, exclude
`patrick.kappen.io` from that override or forward it to public DNS. Otherwise,
clients on the local network will reach Traefik instead of the Cloudflare Worker.

## Optional local CLI deployment

After authenticating Wrangler:

```bash
npx wrangler login
npm run deploy
```

The `public/_headers` file is copied into `dist/` by Astro and configures the
security headers for static responses.
