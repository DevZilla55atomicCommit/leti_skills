// scripts/verify-assets.mjs — asset gate: every /images/* ref in code must
// resolve to a real, non-stub, magic-byte-valid file. No deps. Run: npm run verify:assets
import { readFileSync, existsSync, statSync, readdirSync } from 'node:fs';
import { join, extname } from 'node:path';

import { fileURLToPath } from 'node:url';

const ROOT = join(fileURLToPath(new URL('..', import.meta.url)), '/');
const BYTE_FLOOR = 2048; // under this = stub/placeholder text posing as image
const MAGIC = {
  '.jpg': ['ffd8ff'], '.jpeg': ['ffd8ff'],
  '.png': ['89504e47'], '.webp': ['52494646'], '.avif': ['000000'], // avif checked loosely
};
const SKIP_DIRS = ['node_modules', '.next', '.git', 'scripts'];

function* walk(dir) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith('.') && e.name !== '.claude') continue;
    const p = join(dir, e.name);
    if (e.isDirectory()) {
      if (SKIP_DIRS.includes(e.name)) continue;
      yield* walk(p);
    } else if (/\.(tsx?|jsx?|css|md|json)$/.test(e.name) && !p.includes('assets/manifest.json')) {
      yield p;
    }
  }
}

const errors = [];
const warnings = [];
for (const file of walk(ROOT)) {
  const text = readFileSync(file, 'utf8');
  const refs = [...text.matchAll(/\/images\/[A-Za-z0-9_.\-]+\.(jpg|jpeg|png|webp|avif)/g)].map(m => m[0]);
  for (const ref of new Set(refs)) {
    const abs = join(ROOT, 'public', ref.replace('/images/', 'images/'));
    const rel = `${file.replace(ROOT, '')} -> ${ref}`;
    if (!existsSync(abs)) { errors.push(`MISSING: ${rel}`); continue; }
    const size = statSync(abs).size;
    if (size < BYTE_FLOOR) { errors.push(`STUB (${size}b < ${BYTE_FLOOR}b floor): ${rel}`); continue; }
    const ext = extname(abs).toLowerCase();
    const head = readFileSync(abs).subarray(0, 4).toString('hex');
    const valid = (MAGIC[ext] || []).some(m => head.startsWith(m));
    if (!valid && ext !== '.avif') errors.push(`CORRUPT (magic ${head}, expected ${MAGIC[ext]}): ${rel}`);
  }
}

// manifest drift: referenced-but-unlisted warns, doesn't fail
try {
  const manifest = JSON.parse(readFileSync(join(ROOT, 'assets/manifest.json'), 'utf8'));
  const listed = new Set((manifest.assets || []).map(a => '/images/' + a.file.split('/').pop()));
  for (const file of walk(ROOT)) {
    const text = readFileSync(file, 'utf8');
    for (const m of text.matchAll(/\/images\/[A-Za-z0-9_.\-]+\.(jpg|jpeg|png|webp|avif)/g)) {
      if (!listed.has(m[0])) warnings.push(`UNLISTED (in code, not in manifest): ${m[0]} @ ${file.replace(ROOT, '')}`);
    }
  }
} catch { warnings.push('manifest unreadable, drift check skipped'); }

for (const w of new Set(warnings)) console.log('WARN ' + w);
if (errors.length) {
  for (const e of errors) console.log('FAIL ' + e);
  console.log(`\nverify:assets FAILED — ${errors.length} broken ref(s). Download the file or remove the ref; never commit a dangling ref.`);
  process.exit(1);
}
console.log('verify:assets PASSED — zero broken refs.');
