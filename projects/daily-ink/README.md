# Daily Ink

A micro-prompt for writing, every day. No accounts, no tracking, no backend.
Installable as a PWA on your phone.

- One screen: a prompt, an editor, autosave.
- Drafts autosave to localStorage. Saved entries persist.
- Export any entry as Markdown.
- Offline-first (service worker, installable).
- Dark/light theme follows system.

## Stack

- Vite + Vanilla TypeScript (no framework UI)
- vite-plugin-pwa (Workbox under the hood)
- Biome for formatting/lint
- ~50KB gzipped total

## Local dev

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```

Output goes to `dist/`. Deploy `dist/` to GitHub Pages.

## Deployment

The repo includes a GitHub Actions workflow that builds and deploys to GitHub
Pages on every push to `main`. After enabling Pages on the repo, set the source
to "GitHub Actions" in the repo settings.

## Storage

All data lives in localStorage under the keys:

- `daily-ink:entries` — array of saved entries
- `daily-ink:draft` — current in-progress draft for today

Clear with `localStorage.clear()` in DevTools. None of it leaves the device.

## Prompts

A curated list of ~60 prompts rotates deterministically by date, so the same day
always shows the same prompt. Edit `src/prompts.ts` to add your own.

## License

MIT
