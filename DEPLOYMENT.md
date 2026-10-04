# Website development and deployment

This is a static Astro website configured for the `patrickkappen` Cloudflare
Worker using Static Assets.

## Local development

Requires Node.js 22 or newer, and the private `Patrick-Kappen/website-content`
repository checked out or linked as `content/`.

```bash
ln -s ../../website-content/main content
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

All text lives in the private `website-content` repository, under `content/`;
this repository only lays it out. A section disappears
when its list is empty.

| File | What it holds |
|---|---|
| `data/profile.ts` | Name, role, intro, photo, links, certifications, stack, and the About page text, focus, beliefs and contact |
| `data/topics.ts` | Topics with name, short description, icon and colours |
| `data/work.ts` | Work items; `featured` ones also appear on the home page |
| `data/planned.ts` | Planned posts, shown as "Coming up" until a post with the same title is published |
| `now.json` | The Now list in the sidebar, also published as `/now.json` for the profile README |
| `blog/*.md` | Blog posts |

Posts have `title`, `description`, `date`, `topic`, `tags` and `draft` in the
front matter. Drafts show up in `npm run dev` but are left out of production
builds and the RSS feed. Reading time is calculated from the text.

## Deploy through GitHub Actions

`.github/workflows/build.yml` checks out this repository and `website-content`
into `content/`, builds the site, and on `main` deploys `dist/` with
`npx wrangler deploy`. A push to `main` in `website-content` triggers the same
workflow through a `content-updated` repository dispatch.

Secrets in this repository:

- `WEBSITE_CONTENT_KEY`: private half of a read-only deploy key on `website-content`
- `CLOUDFLARE_API_TOKEN`: token with *Workers Scripts: Edit* for the account
- `CLOUDFLARE_ACCOUNT_ID`: the Cloudflare account ID

The Git integration of the `patrickkappen` Worker in Cloudflare stays off, so
only this workflow deploys.

The `assets.directory` setting in `wrangler.jsonc` tells Wrangler to upload
`dist/` as the Worker's static assets. The custom-domain route provisions
`patrick.kappen.io`, including its Cloudflare DNS record and TLS certificate.

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
