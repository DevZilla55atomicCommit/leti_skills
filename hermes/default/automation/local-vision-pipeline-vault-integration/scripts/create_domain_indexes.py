#!/usr/bin/env python3
"""
Create index.md mapping files for domain folders
"""

from pathlib import Path
from datetime import datetime

VAULT_ROOT = Path("/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base")

DOMAIN_FOLDERS = [
    "Color Grading & Looks",
    "Camera Theory", 
    "Lighting",
    "Fusion",
    "Photography_Videography",
    "Post_Production",
    "Video_Effects"
]

def read_frontmatter(content):
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    fm_text = parts[1]
    fm = {}
    for line in fm_text.strip().split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm

def main():
    for domain in DOMAIN_FOLDERS:
        domain_path = VAULT_ROOT / domain
        if not domain_path.exists():
            print(f"Skipping {domain} - not found")
            continue
        
        # Find all .md files in domain folder
        techniques = []
        for md_file in domain_path.glob("*.md"):
            if md_file.name == "index.md" or md_file.name.startswith("."):
                continue
            try:
                content = md_file.read_text()
                fm = read_frontmatter(content)
                techniques.append({
                    "file": md_file.name,
                    "title": fm.get("title", md_file.stem),
                    "video_id": fm.get("video_id", ""),
                    "collection": fm.get("collection", ""),
                    "resolve_page": fm.get("resolve_page", ""),
                    "tags": fm.get("tags", []),
                    "skill": fm.get("skill", ""),
                    "analysis": fm.get("analysis", ""),
                    "difficulty": fm.get("difficulty", ""),
                    "node_graph": fm.get("node_graph", ""),
                })
            except Exception as e:
                print(f"Error reading {md_file}: {e}")
        
        # Sort by title
        techniques.sort(key=lambda x: x["title"].lower())
        
        # Generate index.md
        index_content = f"""---
title: "{domain} Index"
folder: "{domain}"
generated: {datetime.now().isoformat()}
total_techniques: {len(techniques)}
---

# {domain} — Technique Index

> Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
> Total techniques: {len(techniques)}

| Technique | Video ID | Collection | Page | Tags | Skill | Analysis | Difficulty |
|-----------|----------|------------|------|------|-------|----------|------------|
"""
        
        for t in techniques:
            tags_str = ", ".join(t["tags"]) if isinstance(t["tags"], list) else str(t["tags"])
            skill_link = f"[[{t['skill']}]]" if t["skill"] else "—"
            analysis_link = f"[[{t['analysis']}]]" if t["analysis"] else "—"
            
            index_content += f"| [[{t['file']}]] | {t['video_id']} | {t['collection']} | {t['resolve_page']} | {tags_str} | {skill_link} | {analysis_link} | {t['difficulty']} |\n"
        
        # Write index.md
        index_path = VAULT_ROOT / domain / "index.md"
        index_path.write_text(index_content)
        print(f"Created index.md for {domain} ({len(techniques)} techniques)")

if __name__ == "__main__":
    main()