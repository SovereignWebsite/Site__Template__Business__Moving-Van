// Take the chooser's screenshots: each design's first screen at 1280x800, saved at 640x400 in site/assets/designs/.
// Run after building:  python3 tools/designs/build.py && node .github/ci/build.mjs && node tools/designs/shots.mjs
// Uses the Playwright already in the container (PLAYWRIGHT_DIR overrides where to find it).
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { createRequire } from 'node:module';
const req = createRequire(import.meta.url);
const pwDir = process.env.PLAYWRIGHT_DIR || (() => { try { return path.dirname(req.resolve('playwright/package.json')); } catch { return '/opt/node-tools/node_modules/playwright'; } })();
const { chromium } = await import(path.join(pwDir, 'index.mjs'));
const root = path.resolve('_site');
const content = JSON.parse(fs.readFileSync('site/data/content/en.json', 'utf8'));
const types = { '.css': 'text/css', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.json': 'application/json' };
const srv = http.createServer((q, r) => { let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
  const f = path.join(root, p); if (!f.startsWith(root) || !fs.existsSync(f)) { r.statusCode = 404; return r.end(); }
  r.setHeader('content-type', types[path.extname(f)] || 'text/html'); r.end(fs.readFileSync(f)); }).listen(0);
const port = srv.address().port;
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 0.5, colorScheme: 'light' });
for (const d of content.designs) {
  const p = await ctx.newPage(); await p.goto(`http://localhost:${port}${d.path}`);
  await p.screenshot({ path: `site/assets/designs/${d.slug}.png` }); await p.close();
  console.log(`site/assets/designs/${d.slug}.png`);
}
await b.close(); srv.close();
