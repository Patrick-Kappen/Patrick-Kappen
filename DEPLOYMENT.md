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

| Path | What it holds |
|---|---|
| `site.yaml` | Name, role, intro, photo, links, certifications, Now list (also published as `/now.json`) |
| `pages/*.md` | The fixed texts of every page, navigation and footer |
| `posts/*.md` | Blog posts (`kind: post`) and work items (`kind: work`); `featured` work also appears on the home page |
| `topics/*.yaml` | Topics with name, short description, icon and colours |
| `tools.yaml`, `tool-groups.yaml` | The toolbox |
| `machines/*.yaml`, `services.yaml` | Machines and homelab services for the Setup page |
| `projects/*.yaml` | Open-source projects |

The folders and fields are described in the README of `website_content`.
Posts have `title`, `description`, `date`, `topic`, `tags` and `status`
(`draft`, `planned` or `published`) in the front matter. Drafts show up in
`npm run dev` but are left out of production
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

## GitHub profile

`README.md` is the GitHub profile, separate from the Astro website. Its banner
and project cards live in `.github/assets/` and need no external image service.
Banner and telemetry use the available README width, with square corners and
no outer outline. GitHub controls the maximum width of the profile itself.

`.github/scripts/update_readme.py` updates the marked README sections from the
content repository and public GitHub activity. `profile_activity.py` renders
`.github/assets/git-activity.svg` from GitHub's GraphQL contribution calendar.
The existing `GITHUB_TOKEN` authenticates the request; no additional secret is
needed for public activity. Only daily aggregate counts are used, not private
repository names or contents.

The counters cover the last **7, 30 and 365 days**, including today (UTC), not
calendar weeks or months. The monthly bars partition that same 365-day window;
the first and last calendar months can be partial. These are GitHub
**contributions**, not just commits or a measure of productivity. The chart
includes its refresh date and keeps the last successful version if the API
fails; missing data is never replaced by invented zeroes.

`profile_projects.py` generates `project-1.svg` through `project-3.svg` and the
`projects:start` / `projects:end` README block from recent public open/merged PRs
and releases. Open PRs show their update date and are labelled **OPEN PR**; they
never appear under **Recently shipped**. Repository names, descriptions, fork labels and activity dates come
from GitHub, not the website content's curated project list. Routine CI/sync
changes are filtered out, archived/private/disabled repositories are excluded,
and fork/upstream families appear only once. The cards link to the actual
repository where the activity happened; the Git log links to the PR or release.
A failed refresh preserves the previous cards and their refresh date.

The daily README workflow commits the README and all generated assets, including
when only an image changed or an obsolete card was removed. Run the offline
tests with PyYAML installed:

```bash
python3 -m unittest discover -s .github/scripts -p 'test_*.py'
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
