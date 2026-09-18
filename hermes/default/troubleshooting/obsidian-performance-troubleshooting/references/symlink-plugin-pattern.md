# Why Symlinks Work for Obsidian Plugins

## The Mechanism

Obsidian is built on Electron (Node.js + Chromium). Plugin loading uses Node.js's `require()` system:

```javascript
// Simplified Obsidian plugin loader
const pluginPath = `${vaultPath}/.obsidian/plugins/${pluginId}/main.js`;
const pluginModule = require(pluginPath);
```

### Symlink Resolution in Node.js

When `require()` encounters a symlink:
1. **Node.js does NOT resolve symlinks by default** — it loads the symlink target directly
2. The `fs.realpathSync()` is NOT called during `require()`
3. The module cache key is the **requested path** (the symlink path), not the real path

This means:
- `require('/vault/.obsidian/plugins/heavy/main.js')` works even if `heavy` → `/fast/heavy`
- Module caching uses the symlink path as key
- No performance penalty — kernel handles redirection in VFS layer

### Verification

```bash
# Test that Node.js follows symlinks for require()
mkdir -p /tmp/test-plugin
echo "module.exports = { hello: 'world' }" > /tmp/test-plugin/main.js

mkdir -p /tmp/vault/.obsidian/plugins
ln -s /tmp/test-plugin /tmp/vault/.obsidian/plugins/test-plugin

node -e "console.log(require('/tmp/vault/.obsidian/plugins/test-plugin/main.js'))"
# Output: { hello: 'world' }
```

## Obsidian-Specific Behavior

### What Works
- Symlinked plugin directories in `.obsidian/plugins/`
- Symlinked individual files (`main.js`, `manifest.json`, `styles.css`)
- Nested symlinks

### What Doesn't Work
- Symlinks pointing to non-existent targets (obviously)
- Broken symlinks cause plugin load errors
- Relative symlinks that break when vault moves

### Best Practice: Absolute Target, Relative Link

```bash
# GOOD: Absolute target, link in vault plugins dir
ln -s /Users/you/Library/Application\ Support/obsidian-plugins/heavy \
      /Volumes/USB/vault/.obsidian/plugins/heavy

# RISKY: Relative target (breaks if vault moves)
ln -s ../../../../fast/heavy \
      /Volumes/USB/vault/.obsidian/plugins/heavy
```

## Why This Is Safe

1. **Obsidian never writes to plugin directories** — they're read-only at runtime
2. **No file watchers on plugin dirs** — Obsidian watches vault notes, not `.obsidian/plugins/`
3. **Updates via BRAT/community store** — these write to the real path; symlink stays valid
4. **Zero config changes** — Obsidian doesn't know or care about the symlink

## Caveats

- **Plugin updates**: If using BRAT or manual update, it writes to the real path (fast storage). Symlink remains valid.
- **Vault portability**: If moving vault to another machine, the symlink target must exist there too.
- **Backup**: Backing up the vault alone misses plugins on fast storage. Back up both locations.
- **Dev repos masquerading as plugins**: Some "plugins" (like graphify-core) are actually full source repositories with tests/, docs/, .git/, and no built `main.js`. They will appear to load but provide no functionality. **Fix**: Build them (`npm run build` in the plugin dir) or install the published version via BRAT/community store. Verify by checking for `main.js` and `manifest.json` in the plugin root.