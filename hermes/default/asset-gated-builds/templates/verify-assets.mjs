// Starter verifier for asset-gated builds: scans code for /images/* refs and
// FAILS on MISSING / STUB / CORRUPT files; WARNs on manifest drift. No deps.
// Customize: REF_PREFIX + PUBLIC_DIR + MANIFEST if your layout differs.
// Usage: node scripts/verify-assets.mjs (wire as `verify:assets` in package.json)
import { readFileSync, existsSync, statSync, readdirSync } from 'node:fs';
import { join, extname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(fileURLToPath(new URL('..', import.meta.url)), '/');
const REF_PREFIX = '/images/';
const PUBLIC_DIR = 'public/images/';
const MANIFEST = 'assets/manifest.json';
const BYTE_FLOOR = 2048; // under this = stub/placeholder text posing as an image
const MAGIC = {
  '.jpg': ['ffd8ff'], '.jpeg': ['ffd8ff'],
  '.png': ['89504e47'], '.webp': ['52494646'],
  '.mp4': null, // checked at offset 4 for 'ftyp' below
  '.pdf': ['25504446'],
};
const SKIP_DIRS = ['node_modules', '.next', '.git', 'scripts'];

function* walk(dir) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith('.') && e.name !== '.claude') continue;
    const p = join(dir, e.name);
    if (e.isDirectory()) {
      if (SKIP_DIRS.includes(e.name)) continue;
      yield* walk(p);
    } else if (/\.(tsx?|jsx?|css|md|json)$/.test(e.name) && !p.endsWith(MANIFEST)) {
      yield p;
    }
  }
}

const errors = [];
const warnings = [];
const refRe = new RegExp(
  REF_PREFIX.replace('/', '\\/') + '[A-Za-z0-9_.\\-]+\\.(jpg|jpeg|png|webp|mp4|pdf)', 'g');
for (const file of walk(ROOT)) {
  const text = readFileSync(file, 'utf8');
  for (const ref of new Set([...text.matchAll(refRe)].map(m => m[0]))) {
    if (ref.endsWith('/')) continue; // directory mention in prose, not a ref
    const abs = join(ROOT, PUBLIC_DIR, ref.slice(REF_PREFIX.length));
    const rel = `${file.replace(ROOT, '')} -> ${ref}`;
    if (!existsSync(abs)) { errors.push(`MISSING: ${rel}`); continue; }
    const size = statSync(abs).size;
    if (size < BYTE_FLOOR) { errors.push(`STUB (${size}b < floor): ${rel}`); continue; }
    const ext = extname(abs).toLowerCase();
    const buf = readFileSync(abs);
    const head = buf.subarray(0, 4).toString('hex');
    const ok = ext === '.mp4'
      ? buf.subarray(4, 8).toString() === 'ftyp'
      : (MAGIC[ext] || []).some(m => head.startsWith(m));
    if (!ok) errors.push(`CORRUPT (magic ${head}): ${rel}`);
  }
}

try {
  const manifest = JSON.parse(readFileSync(join(ROOT, MANIFEST), 'utf8'));
  const listed = new Set((manifest.assets || []).map(a => REF_PREFIX + a.file.split('/').pop()));
  for (const file of walk(ROOT)) {
    const text = readFileSync(file, 'utf8');
    for (const m of [...text.matchAll(refRe)].map(x => x[0])) {
      if (!m.endsWith('/') && !listed.has(m))
        warnings.push(`UNLISTED (in code, not in manifest): ${m} @ ${file.replace(ROOT, '')}`);
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
