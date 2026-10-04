# Website development and deployment

This is a static Astro website configured for the `patrickkappen` Cloudflare
Worker using Static Assets.

## Local development

Requires Node.js 22 or newer, and the private `Patrick-Kappen/website_content`
repository checked out or linked as `content/`.

```bash
ln -s ../../website_content/main content
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

All text lives in the private `website_content` repository, under `content/`;
this repository only lays it out. A section disappears
when its list is empty.

| File | What it holds |
|---|---|
| `data/profile.ts` | Name, role, intro, photo, links, certifications, stack, and the About page text, focus, beliefs and contact |
| `data/topics.ts` | Topics with name, short description, icon and colours |
| `data/work.ts` | Work items; `featured` ones also appear on the home page |
| `data/hardware.ts` | Machines and homelab services for the Setup page |
| `data/planned.ts` | Planned posts, shown as "Coming up" until a post with the same title is published |
| `now.json` | The Now list in the sidebar, also published as `/now.json` for the profile README |
| `blog/*.md` | Blog posts |

Posts have `title`, `description`, `date`, `topic`, `tags` and `draft` in the
front matter. Drafts show up in `npm run dev` but are left out of production
builds and the RSS feed. Reading time is calculated from the text.

Optional front matter:

- `image`, `imageAlt`, `imageCredit`, `imageCreditUrl`: a cover image.
- `series: { name, part }`: posts with the same series name are linked
  with a "Part N of M" box and previous/next links.

Share images live in `public/assets/og/`. A post uses `<slug>.png` when it
exists and `default.png` otherwise. Render one with:

```bash
nix shell nixpkgs#librsvg nixpkgs#python3 -c \
  python3 scripts/og-image.py public/assets/og/<slug>.png "Post title" "Topic · Blog"
```

## Deploy through GitHub Actions

`.github/workflows/build.yml` checks out this repository and `website_content`
into `content/`, builds the site, and on `main` deploys `dist/` with
`npx wrangler deploy`. A push to `main` in `website_content` triggers the same
workflow through a `content-updated` repository dispatch.

Both repositories use the `website-ci` GitHub App, installed on
`Patrick-Kappen/Patrick-Kappen` and `Patrick-Kappen/website_content` with
*Contents: read and write*. Each run asks for a short-lived token with only
the permission it needs.

In both repositories:

- variable `WEBSITE_APP_CLIENT_ID`: the app's client ID
- secret `WEBSITE_APP_PRIVATE_KEY`: a private key of the app

Secrets in this repository:

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
