# Plugin Marketplace Packaging (Claude Code)

Portable way to ship skills to every runtime (CLI + Desktop app) and every machine. One registry repo, installed once per machine.

## Layout

```
<marketplace-repo>/
├── .claude-plugin/marketplace.json      # registry: lists every plugin in the repo
└── plugins/<plugin-name>/
    ├── .claude-plugin/plugin.json       # name, description, version, skills path
    └── skills/<skill-name>/SKILL.md      # frontmatter: name + description
```

## marketplace.json (minimal)

```json
{
  "name": "<marketplace-name>",
  "owner": { "name": "<you>", "url": "https://github.com/<you>" },
  "metadata": { "description": "<what this library is>", "version": "1.0.0" },
  "plugins": [
    {
      "name": "<plugin-name>",
      "source": "./plugins/<plugin-name>",
      "description": "<what it provides>",
      "version": "1.0.0",
      "strict": true
    }
  ]
}
```

## plugin.json (minimal)

```json
{
  "name": "<plugin-name>",
  "description": "<what it provides>",
  "version": "1.0.0",
  "author": { "name": "<you>", "url": "https://github.com/<you>" },
  "license": "MIT",
  "skills": "./skills/"
}
```

## Install sequence (per machine, in order — each step gates the next)

```bash
claude plugin marketplace add <owner>/<repo>   # register; expect "Successfully added marketplace"
claude plugin validate <cache-path>            # validate marketplace.json before installing
claude plugin install <plugin>@<marketplace>   # expect "Successfully installed" + ✔ enabled in `plugin list`
```

Validate both JSON files (`python3 -c "import json; json.load(open(...))"`) before committing — a trailing comma fails silently at install time.

## Skill naming

Installed skills resolve as `<plugin>:<skill>`. Keep the skill name generic (it is global once installed — a project-named skill confuses future unrelated builds). Project folders keep their own local copy under `.claude/skills/` with the project-specific name; the two stay in sync by convention, not by tooling.
