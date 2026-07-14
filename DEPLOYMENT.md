# Website development and deployment

This is a static Vite website configured for Cloudflare Pages.

## Local development

Requires Node.js 22 or newer.

```bash
npm install
npm run dev
```

Vite will print the local URL. Create a production build with:

```bash
npm run build
npm run preview
```

The production output is written to `dist/`.

## Deploy with Cloudflare Pages

1. Open **Workers & Pages** in the Cloudflare dashboard.
2. Select **Create > Pages > Connect to Git** and choose this repository.
3. Use these build settings:
   - Framework preset: **Vite**
   - Build command: `npm run build`
   - Build output directory: `dist`
   - Node.js version: `22`
4. Save and deploy.

Cloudflare will build every new commit automatically. The `.node-version` file,
`wrangler.jsonc`, and `public/_headers` file provide the runtime, Pages output,
and response-header configuration.

## Optional CLI deployment

After creating the Pages project and authenticating Wrangler:

```bash
npx wrangler login
npm run deploy
```
