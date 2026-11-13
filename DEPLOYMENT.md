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

The fuller introduction covers day-to-day DevOps work, Azure landing zones,
Bicep/Terraform and working through difficult design problems, without client
cases. Provider, Nix, coding-agent and personal GitHub stories add concrete
examples from published work without hardcoded PR statuses. These and the visible
**How I build things** section live outside all generated blocks, so scheduled
updates preserve their copy. The latter uses the
same combined PK/circuit logo-and-title SVG pattern as the other sections.
`profile_copy.py` supplies narrative introductions to the generated project,
writing and tool sections. Published article summaries come from front matter
`description`, with a plain link fallback when absent; drafts and work items
are never listed. Project cards and telemetry remain live, without manually
invented contribution descriptions or statuses.

**On the radar** reads authored priorities from `site.yaml` in the content repo,
not inferred tasks from GitHub events. `Learning:`, `Building:`, `Writing:` and
`Exploring:` strings receive decorative orange chapter-style icons and visible
labels; legacy plain strings still work. The strings remain compatible with the
website sidebar and `/now.json`.

Large images have a fixed intrinsic canvas height, not an indefinitely scaling
aspect ratio: the control-room banner is **450px**, telemetry **760px**. At viewport
widths up to **600px**, compact variants use **400px** and **560px** respectively.
These are intentionally prominent sections, not thumbnail-sized widgets.
The outer SVG has `width="100%"`, an absolute height and **no viewBox**.
This works without README CSS, including hosts that set `img { height: auto }`.
Content reflows across the real available width, not a fixed-width drawing
centered inside a wider, empty canvas:

- The desktop banner has independent copy, rack and intern viewports at 0%,
  50% and 70%. Their individual viewBoxes limit the illustrations' height;
  the copy stays left, the rack moves with its column and the intern stays right.
  Tighter scene bounds, a narrower terminal and a wrapped caption allow the actual
  artwork and lettering to grow in GitHub's roughly 838px README column; increasing
  only the canvas height would leave the old width-limited artwork small. Rack
  sparkles can overflow the tighter device viewport without being cropped.
  The phone banner stacks the copy above the rack/intern rather than shrinking
  the entire desktop composition into a tiny strip.
- Telemetry uses four 25%-wide counter columns on desktop and two rows of two
  50%-wide counters on phones, with a chart spanning 94% of the image. Desktop
  main values are about 51px, phone main values about 29px. The desktop chart is
  about 225px tall (previously 104px); phone month labels remain smaller to fit
  thirteen months. Bar widths, month positions, gridlines and comparison rows use percentage
  coordinates. Vertical geometry and fonts are fixed pixel sizes for each variant;
  **no chart or counter ancestor has a viewBox**, so wider screens cannot zoom them.

Full HD, QHD and 4K therefore spread the content horizontally without increasing
height, text size or illustration size. GitHub still controls its profile-column
width; the images do not bypass that host limit.

`CONTAINED_IMAGES` in `profile_visuals.py` owns those limits. `<picture>` selects
compact sources before the ordinary theme sources. No fixed HTML image height
is added, because that would override the compact SVG's smaller intrinsic height.
Other images already have numeric width caps: chapter banners are at most
560px wide / 144px tall, project cards 390px wide, themed tool pictograms 140px
wide / 104px tall (unknown-tool brand-logo fallbacks remain 36px). Project-card
height follows the complete repository description and title; each pair shares
its height so rows align without truncating the project description.

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
scheduled renderer needs no installed fonts or image packages.

`profile_tool_icons.py` supplies 25 original labelled circuit-style tool pictograms
on the same 64px / 3px square-ended grid, with transparent light/dark variants in
`.github/assets/tools/`. These are explicitly not official brand logos. Their
rendering is deterministic, needs no API/fonts/image package, and cleans only
its own generated folder. All themes are rendered before files are replaced.
The website’s original `public/assets/logos/` files are never modified.

The profile shows **all** highlighted tools, without the old ten-logo cap.
`profileToolExtras` in content `site.yaml` adds further IDs from `tools.yaml`
without altering website homepage highlights. The seven approved additions are
Entra ID, Home Manager, sops, llama.cpp, Codex, pi and PiG. Unknown configured IDs
fail rather than creating broken images; unknown artwork falls back only to
an existing local brand-logo reference. Adding PiG to the catalogue also makes
it available in the website toolbox, without inventing an official logo.

The editable banner source is `.github/art/control-room.svg`. Its semantic
`data-fill`, `data-stroke` and `data-stop-color` roles are resolved into the
palette when generating `control-room-dark.svg` and `control-room-light.svg`.
Its three `data-region` groups define the independently positioned desktop scenes;
their original coordinates also support the stacked phone composition.
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
through `project-6-dark.svg` / `project-6-light.svg`, plus the
`projects:start` / `projects:end` README block from recent public open/merged PRs
and releases. Up to six automatically selected projects appear in three rows
of two larger cards (one per line when a mobile viewport is too narrow).
Repository descriptions are shown in full. Relationship labels distinguish
**OWN REPOSITORY**, **FORK** and **UPSTREAM CONTRIBUTION**, using ownership and
fork metadata rather than claiming authorship or maintainership.
Open PRs show their update date and are labelled **OPEN PR**; they
never appear under **Recent work**. Repository names, descriptions, fork labels and activity dates come
from GitHub, not the website content's curated project list. Routine CI/sync
changes are filtered out, archived/private/disabled repositories are excluded,
and fork/upstream families appear only once. The cards link to the actual
repository where the activity happened; the Git log links to the PR or release.
Both themes are rendered before replacing any cards. A failed refresh preserves
the previous cards, links and refresh date. Successful updates remove obsolete
single-theme cards. The `shipped:start` / `shipped:end` block preserves recent
work on API errors without depending on heading text or formatting.

`profile_work.py` renders up to eight completed public activities, with at most
two distinct changes per repository. This selection is independent of the six
featured-card limit. Exact dates, PR/release links and **MERGED PR** / **RELEASE**
labels avoid treating a merge as a published release. Open PRs stay on project
cards, never in completed work. Duplicate URLs/titles and routine upstream-sync
activity are filtered. The collector checks up to three search pages per state,
retaining a varied candidate pool rather than one change per repository.

Short explanations are excerpts of actual PR/release descriptions, not inferred
impact or AI-generated claims. Recognised summary sections take precedence;
problem/outcome sections prefer the outcome. Code fences, tracking links,
checklists, images and HTML are excluded; inline code identifiers are preserved
and output is escaped. Missing usable descriptions fall back to the original
title/link without inventing an explanation. No extra per-PR API calls are needed:
the bodies are already present in search/release responses.

The README workflow runs every half hour at minutes **17 and 47 UTC**
(`17,47 * * * *`), as well as after website builds, on generator changes and via
manual dispatch. GitHub may delay scheduled runs and image caches can lag.
It commits the README and all generated assets only when something changed,
including when only an image changed or an obsolete card was removed. Generated
refresh labels use dates, not a changing run timestamp, to avoid empty churn. Run the offline
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
