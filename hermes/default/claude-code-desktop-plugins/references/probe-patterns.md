# Probe Patterns — proving a skill actually resolved

A model can confabulate a plausible skill description without loading the file, so only **verbatim section text** counts as resolved.

## Quote-back probe (primary)

```
Use the <plugin>:<skill> skill. Quote back its Section <N> verbatim — title plus all items.
```

- Returns the exact section text → resolved. Proceed.
- Returns SKILL NOT FOUND → resolution failed. If the plugin is installed, the name is wrong — qualify to `<plugin>:<skill>` and retry once.
- Returns a fluent generic description (no verbatim text) → treat as NOT resolved. Re-run the probe with a narrower demand (one numbered section, "verbatim or SKILL NOT FOUND").

## Startup-check pattern (for build skills)

Require the app to quote back project facts from files (not memory) in its first reply — e.g. project name, address, and an `ls | wc -l` count cross-checked against the manifest. A correct quote proves both skill load and file access; anything missing means STOP before writing code.

## Negative control

Probe the bare skill name once (`Use the <skill> skill ...`). SKILL NOT FOUND is the *expected* result and confirms namespaced invocation is required — record the working form in the project docs so the next session uses it first try.
