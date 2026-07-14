# Website development and deployment

This is a static Vite website configured for Cloudflare Workers Static Assets.

## Local development

Requires Node.js 22 or newer.

```bash
npm install
npm run dev
```

Vite will print the local URL. Create and inspect a production build with:

```bash
npm run build
npm run preview
```

The production output is written to `dist/`.

## Deploy through Cloudflare

The connected Cloudflare build should use:

- Build command: `npm run build`
- Deploy command: `npx wrangler deploy`
- Node.js version: `22`

The `assets.directory` setting in `wrangler.jsonc` tells Wrangler to upload
`dist/` as the Worker's static assets. Cloudflare will build and deploy every
new commit automatically.

## Optional local CLI deployment

After authenticating Wrangler:

```bash
npx wrangler login
npm run deploy
```

The `public/_headers` file is copied into `dist/` by Vite and configures the
security headers for static responses.
