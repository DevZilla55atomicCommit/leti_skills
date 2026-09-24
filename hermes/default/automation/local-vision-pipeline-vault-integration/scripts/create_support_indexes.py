#!/usr/bin/env python3
"""
Create index.md mapping files for all support folders
"""

from pathlib import Path
from datetime import datetime

VAULT_ROOT = Path("/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base")

SUPPORT_FOLDERS = {
    "analysis": {
        "pattern": "*/analysis.json",
        "title": "Vision Analysis Reports",
        "columns": ["Video ID", "Collection", "Frames", "Date"]
    },
    "media": {
        "pattern": "*.gif",
        "title": "Media Library (GIFs)",
        "columns": ["GIF Name", "Video ID", "Size"]
    },
    "skills": {
        "pattern": "*.md",
        "title": "Hermes Skills Library",
        "columns": ["Skill Name", "Video ID", "Page", "Category", "Tags"]
    },
    "collections": {
        "pattern": "*.md",
        "title": "Collections Index",
        "columns": ["Collection", "Technique Count", "Description"]
    },
    "tags": {
        "pattern": "*.md",
        "title": "Tags Index",
        "columns": ["Tag", "Technique Count", "Description"]
    },
    "transcripts": {
        "pattern": "*.txt",
        "title": "Transcripts Library",
        "columns": ["Transcript", "Video ID", "Size"]
    }
}

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
    for folder_name, config in SUPPORT_FOLDERS.items():
        folder_path = VAULT_ROOT / folder_name
        if not folder_path.exists():
            print(f"Skipping {folder_name} - not found")
            continue
        
        print(f"Processing {folder_name}...")
        
        entries = []
        
        if folder_name == "analysis":
            for video_dir in sorted(folder_path.iterdir()):
                if video_dir.is_dir():
                    analysis_file = video_dir / "analysis.json"
                    if analysis_file.exists():
                        try:
                            import json
                            with open(analysis_file) as f:
                                data = json.load(f)
                            entries.append({
                                "name": video_dir.name,
                                "video_id": data.get("video_id", video_dir.name),
                                "collection": data.get("collection", ""),
                                "frames": data.get("frames_analyzed", 0),
                                "date": data.get("analyzed_at", "")
                            })
                        except:
                            pass
        
        elif folder_name == "media":
            for gif_file in sorted(folder_path.glob("*.gif")):
                stat = gif_file.stat()
                vid = gif_file.stem.replace("_technique", "")
                entries.append({
                    "name": gif_file.name,
                    "video_id": vid,
                    "size_mb": round(stat.st_size / 1024 / 1024, 2)
                })
        
        elif folder_name == "skills":
            for skill_file in sorted(folder_path.glob("*.md")):
                if skill_file.name.startswith("."):
                    continue
                try:
                    content = skill_file.read_text()
                    fm = read_frontmatter(content)
                    entries.append({
                        "name": skill_file.name,
                        "title": fm.get("title", skill_file.stem),
                        "video_id": fm.get("video_id", ""),
                        "page": fm.get("page", ""),
                        "category": fm.get("category", "creative"),
                        "tags": fm.get("tags", [])
                    })
                except:
                    pass
        
        elif folder_name == "collections":
            for coll_file in sorted(folder_path.glob("*.md")):
                if coll_file.name.startswith("."):
                    continue
                try:
                    content = coll_file.read_text()
                    fm = read_frontmatter(content)
                    entries.append({
                        "name": coll_file.name,
                        "collection": fm.get("collection", coll_file.stem),
                        "description": fm.get("description", "")
                    })
                except:
                    pass
        
        elif folder_name == "tags":
            for tag_file in sorted(folder_path.glob("*.md")):
                if tag_file.name.startswith("."):
                    continue
                try:
                    content = tag_file.read_text()
                    fm = read_frontmatter(content)
                    entries.append({
                        "name": tag_file.name,
                        "tag": fm.get("tag", tag_file.stem),
                        "description": content.split("---", 2)[-1].strip() if "---" in content else ""
                    })
                except:
                    pass
        
        elif folder_name == "transcripts":
            for txt_file in sorted(folder_path.glob("*.txt")):
                if txt_file.name.startswith("."):
                    continue
                stat = txt_file.stat()
                vid = txt_file.stem
                entries.append({
                    "name": txt_file.name,
                    "video_id": vid,
                    "size_kb": round(stat.st_size / 1024, 1)
                })
        
        # Generate index.md
        columns = config["columns"]
        header = "| " + " | ".join(columns) + " |"
        separator = "| " + " | ".join(["---"] * len(columns)) + " |"
        
        index_content = f"""---
title: "{config['title']}"
folder: "{folder_name}"
generated: {datetime.now().isoformat()}
total_entries: {len(entries)}
---

# {config['title']}

> Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
> Total entries: {len(entries)}

| {' | '.join(columns)} |
| {' | '.join(['---'] * len(columns))} |
"""
        
        for e in entries:
            row = []
            for col in columns:
                key = col.lower().replace(" ", "_").replace("(", "").replace(")", "")
                if key == "name":
                    row.append(f"[[{e.get('name', '')}]]")
                elif key == "video_id":
                    row.append(e.get("video_id", ""))
                elif key == "collection":
                    row.append(e.get("collection", ""))
                elif key == "frames":
                    row.append(str(e.get("frames", "")))
                elif key == "date":
                    row.append(e.get("date", "")[:10] if e.get("date") else "")
                elif key == "size_mb":
                    row.append(f"{e.get('size_mb', 0)} MB")
                elif key == "size_kb":
                    row.append(f"{e.get('size_kb', 0)} KB")
                elif key == "skill_name":
                    row.append(f"[[{e.get('name', '')}]]")
                elif key == "title":
                    row.append(e.get("title", ""))
                elif key == "page":
                    row.append(e.get("page", ""))
                elif key == "category":
                    row.append(e.get("category", ""))
                elif key == "tags":
                    tags = e.get("tags", [])
                    row.append(", ".join(tags) if isinstance(tags, list) else str(tags))
                elif key == "collection":
                    row.append(e.get("collection", ""))
                elif key == "technique_count":
                    row.append("—")
                elif key == "description":
                    row.append(e.get("description", "")[:50] if e.get("description") else "")
                elif key == "tag":
                    row.append(f"[[#{e.get('tag', '')}]]")
                elif key == "size":
                    row.append(f"{e.get('size_mb', e.get('size_kb', ''))}")
                else:
                    row.append("")
            index_content += "| " + " | ".join(row) + " |\n"
        
        index_path = VAULT_ROOT / folder_name / "index.md"
        index_path.write_text(index_content)
        print(f"Created index.md for {folder_name} ({len(entries)} entries)")

if __name__ == "__main__":
    main()