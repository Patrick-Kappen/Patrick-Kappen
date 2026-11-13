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
Banner, project cards and telemetry all have transparent light/dark variants,
selected by README `<picture>` elements. Banner and telemetry use the available
README width, with no outer frame. GitHub controls the profile's maximum width.

Large images have a fixed intrinsic canvas height, not an indefinitely scaling
aspect ratio: the control-room banner is **240px**, telemetry **420px**. At viewport
widths up to **600px**, compact variants use **160px** and **220px** respectively.
The outer SVG has `width="100%"`, an absolute height and **no viewBox**.
This works without README CSS, including hosts that set `img { height: auto }`.
Content reflows across the real available width, not a fixed-width drawing
centered inside a wider, empty canvas:

- The desktop banner has independent copy, rack and intern viewports at 0%,
  50% and 70%. Their individual viewBoxes limit the illustrations' height;
  the copy stays left, the rack moves with its column and the intern stays right.
  The compact banner keeps the original complete composition fitted into 160px.
- Telemetry uses four 25%-wide counter columns and a chart spanning 94% of the
  image. Bar widths, month positions, gridlines and comparison rows use percentage
  coordinates. Vertical geometry and fonts are fixed pixel sizes for each variant;
  **no chart or counter ancestor has a viewBox**, so wider screens cannot zoom them.

Full HD, QHD and 4K therefore spread the content horizontally without increasing
height, text size or illustration size. GitHub still controls its profile-column
width; the images do not bypass that host limit.

`CONTAINED_IMAGES` in `profile_visuals.py` owns those limits. `<picture>` selects
compact sources before the ordinary theme sources. No fixed HTML image height
is added, because that would override the compact SVG's smaller intrinsic height.
Other images already have numeric width caps: chapter banners are at most
560px wide / 144px tall, project cards 270px wide / 198px tall, tool logos 36px.

`profile_visuals.py` owns the shared palette and original PK/circuit artwork.
Each chapter uses a centered `headings/<key>-dark.svg` / `<key>-light.svg` banner
containing **both the logo and title**, not a separate HTML label and icon.
The approved layout uses 3px strokes on a 64px icon grid, a 56px displayed icon,
a 28px logo/title gap and 144px-tall transparent canvases. Long titles receive
a wider canvas so neither the lettering nor the end ticks are clipped.

Centered paragraph wrappers preserve section IDs and image alt text contains
the chapter title. Native H1/H2 wrappers are deliberately avoided because GitHub
adds automatic gray underlines to them. The SVGs contain no gray separator
rules, and the README has no footer rule; whitespace separates the sections. `HEADING_METRICS` stores the static Noto Sans
Bold 30px widths/baselines, and SVG `textLength` fixes horizontal alignment
across font fallbacks. Update those metrics alongside any label changes; the
daily renderer needs no installed fonts or image packages. The small accordion
icon remains decorative with empty alt text. Third-party tool logos keep their
original branding and are not recolored.

The editable banner source is `.github/art/control-room.svg`. Its semantic
`data-fill`, `data-stroke` and `data-stop-color` roles are resolved into the
palette when generating `control-room-dark.svg` and `control-room-light.svg`.
Its three `data-region` groups define the independently positioned desktop scenes;
their original coordinates also preserve the compact composition.
The drawing has no canvas background or opaque device panels. Banner variants
and `.github/assets/{icons,headings}/*.svg` regenerate without API access on
each profile refresh; obsolete files in those generated folders are removed.

`.github/scripts/update_readme.py` updates the marked README sections from the
content repository and public GitHub activity. `profile_activity.py` renders
`.github/assets/git-activity-dark.svg` and `git-activity-light.svg`, plus their
`git-activity-compact-<theme>.svg` variants, from a single GitHub GraphQL snapshot.
All four SVGs have transparent backgrounds, including the counter areas. A README `<picture>` selects the light/dark palette, with the
light image as fallback. Orange accents and text remain readable on the
corresponding GitHub backgrounds; the SVGs do not inherit GitHub CSS.

The four counters are **commits**, **PRs opened**, **PRs merged** and **reviews**.
The main values cover the last **30 days**, with **7-day** and **365-day** values
beneath each. All windows include today (UTC); these are rolling windows, not
calendar weeks or months. Commits, opened PRs and reviews follow GitHub's
contribution-counting and viewer-visibility rules. Merged PRs are public PRs
**authored by the profile owner** that merged during the window, not PRs the
owner merged for other authors. The opened/merged populations can overlap;
a PR can also merge in a different period from when it was opened.

The monthly bars remain the aggregate GitHub **contribution calendar**, which
includes other activity too, not a sum of the four counters or a productivity
score. They partition the same 365-day window; the edge months may be partial.
These definitions stay in documentation/accessibility text, not visible help
paragraphs below the graph.

The existing `GITHUB_TOKEN` authenticates the request; no additional secret is
needed for public activity. Counts depend on that token's visibility; this does
not grant access to all private work. Only aggregate counts are stored, never
private repository names or contents. The updater validates all periods before
rendering any variant, keeps all four last-good images (with their date) on API errors,
and never substitutes zero for missing data. A successful update removes the
obsolete opaque `git-activity.svg` asset.

`profile_projects.py` generates `project-1-dark.svg` / `project-1-light.svg`
through `project-3-dark.svg` / `project-3-light.svg`, plus the
`projects:start` / `projects:end` README block from recent public open/merged PRs
and releases. Open PRs show their update date and are labelled **OPEN PR**; they
never appear under **Recently shipped**. Repository names, descriptions, fork labels and activity dates come
from GitHub, not the website content's curated project list. Routine CI/sync
changes are filtered out, archived/private/disabled repositories are excluded,
and fork/upstream families appear only once. The cards link to the actual
repository where the activity happened; the Git log links to the PR or release.
Both themes are rendered before replacing any cards. A failed refresh preserves
the previous cards, links and refresh date. Successful updates remove obsolete
single-theme cards. The `shipped:start` / `shipped:end` block preserves recent
work on API errors without depending on heading text or formatting.

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
