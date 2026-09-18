#!/usr/bin/env python3
"""
Regenerate all mapping/export files for DaVinci_Knowledge_Base vault
"""

import json
import csv
import os
from pathlib import Path
from datetime import datetime

VAULT_ROOT = Path("/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base")

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
    print("Scanning vault...")
    
    # 1. Scan all markdown files
    all_files = []
    all_folders = set()
    
    for md_file in VAULT_ROOT.rglob("*.md"):
        if md_file.name.startswith("."):
            continue
        try:
            rel_path = md_file.relative_to(VAULT_ROOT)
            stat = md_file.stat()
            content = md_file.read_text()
            fm = read_frontmatter(content)
            
            # Determine folder
            folder = str(rel_path.parent) if rel_path.parent != Path(".") else "ROOT"
            all_files.append({
                "path": str(rel_path),
                "full_path": str(md_file),
                "folder": folder,
                "filename": md_file.name,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "frontmatter": fm,
                "preview": content[:500] if len(content) > 500 else content
            })
            all_folders.add(folder)
        except Exception as e:
            print(f"Error reading {md_file}: {e}")
    
    print(f"Found {len(all_files)} markdown files")
    print(f"Found {len(all_folders)} folders")
    
    # 2. Generate knowledge_base_export.json
    kb_export = {
        "metadata": {
            "generated": datetime.now().isoformat(),
            "vault_path": str(VAULT_ROOT),
            "total_markdown_files": len(all_files),
            "total_folders": len(all_folders),
            "folders_sorted": sorted(all_folders)
        },
        "folders": sorted(all_folders),
        "files": all_files
    }
    
    with open(VAULT_ROOT / "knowledge_base_export.json", "w") as f:
        json.dump(kb_export, f, indent=2)
    print(f"Generated knowledge_base_export.json")
    
    # 3. Generate knowledge_base_export.csv
    with open(VAULT_ROOT / "knowledge_base_export.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["path", "full_path", "folder", "filename", "size", "modified", "title", "video_id", "collection", "resolve_page", "tags"])
        for file in all_files:
            fm = file["frontmatter"]
            writer.writerow([
                file["path"],
                file["full_path"],
                file["folder"],
                file["filename"],
                file["size"],
                file["modified"],
                fm.get("title", ""),
                fm.get("video_id", ""),
                fm.get("collection", ""),
                fm.get("resolve_page", ""),
                ";".join(fm.get("tags", [])) if isinstance(fm.get("tags"), list) else fm.get("tags", "")
            ])
    print(f"Generated knowledge_base_export.csv")
    
    # 4. Scan skills
    skills_dir = VAULT_ROOT / "skills"
    skills = []
    if skills_dir.exists():
        for skill_file in skills_dir.glob("*.md"):
            if skill_file.name.startswith("."):
                continue
            try:
                content = skill_file.read_text()
                fm = read_frontmatter(content)
                stat = skill_file.stat()
                skills.append({
                    "skill_name": fm.get("name", skill_file.stem),
                    "title": fm.get("title", skill_file.name),
                    "description": fm.get("description", ""),
                    "tags": fm.get("tags", []),
                    "category": fm.get("category", "creative"),
                    "filename": skill_file.name,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "frontmatter": fm,
                    "preview": content[:500] if len(content) > 500 else content
                })
            except Exception as e:
                print(f"Error reading skill {skill_file}: {e}")
    
    print(f"Found {len(skills)} skills")
    
    # 5. Generate skills_export.json
    skills_export = {
        "metadata": {
            "generated": datetime.now().isoformat(),
            "skills_dir": str(skills_dir),
            "total_skills": len(skills)
        },
        "skills": skills
    }
    
    with open(VAULT_ROOT / "skills_export.json", "w") as f:
        json.dump(skills_export, f, indent=2)
    print(f"Generated skills_export.json")
    
    # 6. Generate skills_export.csv
    with open(VAULT_ROOT / "skills_export.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["skill_name", "title", "description", "tags", "category", "filename", "size", "modified", "video_id", "page", "difficulty", "trigger"])
        for skill in skills:
            fm = skill["frontmatter"]
            writer.writerow([
                skill["skill_name"],
                skill["title"],
                skill["description"],
                ";".join(fm.get("tags", [])) if isinstance(fm.get("tags"), list) else fm.get("tags", ""),
                fm.get("category", "creative"),
                skill["filename"],
                skill["size"],
                skill["modified"],
                fm.get("video_id", ""),
                fm.get("page", ""),
                fm.get("difficulty", ""),
                fm.get("trigger", "")
            ])
    print(f"Generated skills_export.csv")
    
    # 7. Generate VISION_PROGRESS summary
    analysis_dir = VAULT_ROOT / "analysis"
    analysis_count = 0
    if analysis_dir.exists():
        analysis_count = len([d for d in analysis_dir.iterdir() if d.is_dir()])
    
    media_count = len(list((VAULT_ROOT / "media").glob("*.gif"))) if (VAULT_ROOT / "media").exists() else 0
    tags_count = len(list((VAULT_ROOT / "tags").glob("*.md"))) if (VAULT_ROOT / "tags").exists() else 0
    collections_count = len(list((VAULT_ROOT / "collections").glob("*.md"))) if (VAULT_ROOT / "collections").exists() else 0
    skills_count = len(list((VAULT_ROOT / "skills").glob("*.md"))) if (VAULT_ROOT / "skills").exists() else 0
    
    # Domain folder counts
    domain_folders = [
        "Color Grading & Looks", "Camera Theory", "Lighting", "Fusion",
        "Photography_Videography", "Post_Production", "Video_Effects"
    ]
    domain_counts = {}
    for domain in domain_folders:
        domain_path = VAULT_ROOT / domain
        if domain_path.exists():
            domain_counts[domain] = len(list(domain_path.glob("*.md")))
    
    print("\n=== VAULT SUMMARY ===")
    print(f"Total markdown files: {len(all_files)}")
    print(f"Total folders: {len(all_files)}")
    print(f"Skills: {skills_count}")
    print(f"Analysis dirs: {analysis_count}")
    print(f"Media GIFs: {media_count}")
    print(f"Tags: {len(list((VAULT_ROOT / 'tags').glob('*.md'))) if (VAULT_ROOT / 'tags').exists() else 0}")
    print(f"Collections: {collections_count}")
    print(f"Domain folders: {domain_counts}")
    
    print("\nAll mapping files regenerated!")

if __name__ == "__main__":
    main()