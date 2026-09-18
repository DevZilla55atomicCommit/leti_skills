#!/usr/bin/env python3
"""
Instagram → DaVinci Learning Pipeline
Main execution script for the unified skill.

Usage:
    python scripts/run_pipeline.py --input urls.rtf [--resume] [--dry-run] [--batch-size N]
"""

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    import yaml
except ImportError:
    print("Error: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)


class InstagramDavinciPipeline:
    def __init__(self, config_path: Optional[str] = None):
        self.skill_dir = Path(__file__).parent.parent
        self.config = self._load_config(config_path)
        self.vault_path = Path(self.config['vault_path']).expanduser()
        self.skills_dir = Path(self.config['skills_dir']).expanduser()
        self.queue_file = self.vault_path / self.config['queue_file']

        # Session tracking
        self.session = {
            'processed': 0,
            'skipped': 0,
            'failed': 0,
            'camera_theory': 0,
            'new_skills': [],
            'updated_vault_files': [],
            'errors': []
        }

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from YAML file."""
        if config_path is None:
            config_path = self.skill_dir / 'references' / 'config.yaml'
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def run(self, input_file: str, resume: bool = False, dry_run: bool = False,
            filter_creator: Optional[str] = None, retry_failed: bool = False,
            batch_size: Optional[int] = None, force: bool = False,
            config_override: Optional[str] = None):
        """Main pipeline entry point."""
        print(f"🚀 Instagram → DaVinci Learning Pipeline")
        print(f"   Input: {input_file}")
        print(f"   Vault: {self.vault_path}")
        print(f"   Skills: {self.skills_dir}")
        if dry_run:
            print("   🔍 DRY RUN MODE - No files will be written")

        # Override config if provided
        if config_override:
            with open(config_override, 'r') as f:
                self.config.update(yaml.safe_load(f))

        # Stage 1: Parse URLs
        urls = self._parse_input_file(input_file)
        print(f"📥 Extracted {len(urls)} URLs from input")

        if not urls:
            print("❌ No valid Instagram URLs found")
            return

        # Stage 2: Load existing queue for deduplication
        existing_urls = self._load_existing_queue()

        # Stage 3: Deduplicate
        new_urls = self._deduplicate(urls, existing_urls, force)
        print(f"🔍 After deduplication: {len(new_urls)} new URLs")

        if filter_creator:
            new_urls = [u for u in new_urls if filter_creator.lower() in u.get('creator', '').lower()]
            print(f"🎯 Filtered to creator '{filter_creator}': {len(new_urls)} URLs")

        if retry_failed:
            new_urls = self._get_failed_urls()
            print(f"🔄 Retrying {len(new_urls)} failed URLs")

        if dry_run:
            self._dry_run_classify(new_urls)
            return

        # Stage 4: Availability check (simplified - would use instagram-reel-availability-check skill)
        available_urls = self._check_availability(new_urls)
        print(f"✅ Available: {len(available_urls)} / {len(new_urls)}")

        if not available_urls:
            print("❌ No available URLs to process")
            return

        # Stage 5: Process in batches
        batch_size = batch_size or self.config['batch_size']
        for i in range(0, len(available_urls), batch_size):
            batch = available_urls[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(available_urls) + batch_size - 1) // batch_size
            print(f"\n📦 Batch {batch_num}/{total_batches} ({len(batch)} URLs)")
            self._process_batch(batch, batch_num, len(available_urls))

        # Stage 6: Regenerate exports
        self._regenerate_exports()

        # Summary
        self._print_summary()

    def _parse_input_file(self, input_file: str) -> List[Dict]:
        """Parse URLs from various input formats."""
        path = Path(input_file)
        urls = []

        if not path.exists():
            print(f"❌ Input file not found: {input_file}")
            return urls

        # Read content based on extension
        if path.suffix.lower() == '.rtf':
            # Convert RTF to text using textutil (macOS)
            try:
                result = subprocess.run(
                    ['textutil', '-convert', 'txt', '-stdout', str(path)],
                    capture_output=True, text=True, timeout=30
                )
                text = result.stdout
            except (subprocess.TimeoutExpired, FileNotFoundError):
                # Fallback: read as binary and strip RTF codes
                with open(path, 'rb') as f:
                    content = f.read()
                # Simple RTF stripping
                text = content.decode('utf-8', errors='ignore')
                text = re.sub(r'\\[a-z]+\d* ?', '', text)
                text = re.sub(r'[{}]', '', text)
        elif path.suffix.lower() == '.csv':
            with open(path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    url = row.get('url', '').strip()
                    if url and 'instagram.com' in url:
                        urls.append({
                            'url': url,
                            'creator': row.get('creator', '').strip() or self._extract_creator_from_url(url),
                            'notes': row.get('notes', '').strip(),
                            'priority': row.get('priority', 'Medium').strip()
                        })
            return urls
        elif path.suffix.lower() == '.json':
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        else:
            # Plain text
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()

        # Extract Instagram URLs from text
        # Pattern matches: instagram.com/reel/CODE/ or instagram.com/p/CODE/
        pattern = r'https?://(?:www\.)?instagram\.com/(?:reel|p)/([A-Za-z0-9_-]+)/?'
        matches = re.findall(pattern, text)

        for code in matches:
            url = f"https://www.instagram.com/reel/{code}/"
            # Try to find creator context near the URL
            creator = self._extract_creator_from_url(url)
            urls.append({
                'url': url,
                'creator': creator,
                'notes': '',
                'priority': 'Medium'
            })

        return urls

    def _extract_creator_from_url(self, url: str) -> str:
        """Try to extract creator handle from URL or context."""
        # This is a placeholder - in reality we'd need to visit the page
        # For now, return a generic identifier from the URL code
        code_match = re.search(r'instagram\.com/(?:reel|p)/([A-Za-z0-9_-]+)', url)
        if code_match:
            return f"reel_{code_match.group(1)[:8]}"
        return "unknown"

    def _load_existing_queue(self) -> Dict[str, Dict]:
        """Load existing queue to track processed URLs."""
        existing = {}
        if not self.queue_file.exists():
            return existing

        try:
            with open(self.queue_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse the queue table
            # Format: | # | `URL` | Description | Priority | Status |
            lines = content.split('\n')
            for line in lines:
                if '|' in line and 'instagram.com' in line:
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 4:
                        url_match = re.search(r'(https?://[^\s`]+)', parts[2])
                        if url_match:
                            url = url_match.group(1).rstrip('`')
                            status = parts[4] if len(parts) > 4 else ''
                            existing[url] = {'status': status}
        except Exception as e:
            print(f"⚠️  Could not parse queue file: {e}")

        return existing

    def _deduplicate(self, urls: List[Dict], existing: Dict, force: bool) -> List[Dict]:
        """Remove URLs already in queue (unless force)."""
        if force:
            return urls

        new_urls = []
        seen_codes = set()

        for url_data in urls:
            url = url_data['url']
            code_match = re.search(r'instagram\.com/(?:reel|p)/([A-Za-z0-9_-]+)', url)
            code = code_match.group(1) if code_match else url

            # Check by full URL or by code
            if url in existing or code in seen_codes:
                continue

            seen_codes.add(code)
            new_urls.append(url_data)

        return new_urls

    def _get_failed_urls(self) -> List[Dict]:
        """Get URLs that previously failed."""
        # Would parse queue for ❌ Failed entries
        return []

    def _check_availability(self, urls: List[Dict]) -> List[Dict]:
        """
        Check if reels are publicly accessible.
        In full implementation, this would use instagram-reel-availability-check skill.
        For now, we'll mark all as available and handle failures during processing.
        """
        print("🔍 Checking availability (placeholder - all marked available)...")
        return urls

    def _dry_run_classify(self, urls: List[Dict]):
        """Show classification without processing."""
        print("\n🔍 DRY RUN - Classification Preview:")
        print("=" * 60)

        for i, url_data in enumerate(urls, 1):
            classification = self._classify_url(url_data)
            skip_reason = self._check_skip_patterns(url_data)

            status = "⏭️ SKIP" if skip_reason else "✅ PROCESS"
            if classification['category'] == 'Camera Theory':
                status = "📚 CAMERA THEORY"

            print(f"\n{i}. {url_data['url']}")
            print(f"   Creator: @{url_data.get('creator', 'unknown')}")
            print(f"   Category: {classification['category']} → {classification['folder']}")
            print(f"   Status: {status}")
            if skip_reason:
                print(f"   Skip Reason: {skip_reason}")

        print(f"\n📊 Summary: {len(urls)} URLs")
        categories = {}
        for url_data in urls:
            cat = self._classify_url(url_data)['category']
            categories[cat] = categories.get(cat, 0) + 1
        for cat, count in sorted(categories.items()):
            print(f"   {cat}: {count}")

    def _classify_url(self, url_data: Dict) -> Dict:
        """Classify URL into category based on keywords."""
        # In reality, we'd fetch the page content first
        # For now, use creator/notes as proxy
        text = (url_data.get('notes', '') + ' ' + url_data.get('creator', '')).lower()

        categories = self.config.get('categories', [])
        for cat in sorted(categories, key=lambda x: x.get('priority', 99)):
            keywords = cat.get('keywords', [])
            if any(kw.lower() in text for kw in keywords):
                return {
                    'category': cat['name'],
                    'folder': cat['folder'],
                    'keywords_matched': [kw for kw in keywords if kw.lower() in text]
                }

        # Default fallback
        return {
            'category': 'General',
            'folder': 'Creative Grading & Looks',
            'keywords_matched': []
        }

    def _check_skip_patterns(self, url_data: Dict) -> Optional[str]:
        """Check if URL matches skip patterns."""
        text = (url_data.get('notes', '') + ' ' + url_data.get('creator', '')).lower()
        skip_patterns = self.config.get('skip_patterns', [])

        for pattern in skip_patterns:
            if pattern.lower() in text:
                return pattern

        return None

    def _process_batch(self, batch: List[Dict], batch_num: int, total_urls: int):
        """Process a batch of URLs."""
        for i, url_data in enumerate(batch):
            global_idx = (batch_num - 1) * self.config['batch_size'] + i + 1
            print(f"  [{global_idx}/{total_urls}] {url_data['url']}")

            try:
                self._process_single_url(url_data, global_idx)
                self.session['processed'] += 1
            except Exception as e:
                self.session['failed'] += 1
                self.session['errors'].append({
                    'url': url_data['url'],
                    'error': str(e)
                })
                print(f"    ❌ Failed: {e}")

    def _process_single_url(self, url_data: Dict, queue_number: int):
        """Process a single URL - extract, create skill, create vault note."""
        # This is the core processing logic
        # In full implementation, this would:
        # 1. browser_navigate to the reel
        # 2. browser_snapshot / browser_vision to extract content
        # 3. Classify technique
        # 4. Generate skill name
        # 5. Create skill in ~/.hermes/skills/creative/
        # 6. Create vault markdown file
        # 7. Update queue

        classification = self._classify_url(url_data)
        skip_reason = self._check_skip_patterns(url_data)

        if skip_reason:
            status = f"⏭️ Skipped ({skip_reason})"
            self.session['skipped'] += 1
            self._update_queue(url_data, status, skip_reason=skip_reason)
            print(f"    ⏭️  Skipped: {skip_reason}")
            return

        if classification['category'] == 'Camera Theory':
            status = "📚 Camera Theory"
            self.session['camera_theory'] += 1
            self._create_camera_theory_note(url_data, classification, queue_number)
            self._update_queue(url_data, status, folder=classification['folder'])
            print(f"    📚 Camera Theory → {classification['folder']}")
            return

        # Generate skill name
        skill_name = self._generate_skill_name(url_data, classification)
        vault_filename = self._generate_vault_filename(url_data, classification, queue_number)

        # Create skill
        self._create_skill(skill_name, url_data, classification, queue_number)

        # Create vault note
        self._create_vault_note(vault_filename, url_data, classification, skill_name, queue_number)

        # Update queue
        status = f"✅ Done | {skill_name} | {vault_filename}"
        self._update_queue(url_data, status, skill_name=skill_name, vault_file=vault_filename, folder=classification['folder'])

        self.session['new_skills'].append(skill_name)
        self.session['updated_vault_files'].append(vault_filename)
        print(f"    ✅ Created: {skill_name}")

    def _generate_skill_name(self, url_data: Dict, classification: Dict) -> str:
        """Generate skill name from URL data."""
        prefix = self.config['skill_naming']['prefix']
        separator = self.config['skill_naming']['separator']
        max_len = self.config['skill_naming']['max_length']

        # Extract technique keywords from classification
        keywords = classification.get('keywords_matched', [])
        if not keywords:
            # Fallback: use creator + generic term
            creator = url_data.get('creator', 'unknown').replace('@', '').replace('.', '-')
            technique = 'technique'
        else:
            creator = url_data.get('creator', 'unknown').replace('@', '').replace('.', '-')
            technique = '-'.join(keywords[:3]).lower()

        name = f"{prefix}{creator}{separator}{technique}"

        # Sanitize
        name = re.sub(r'[^a-z0-9\-]', '', name.lower())
        name = re.sub(r'-+', '-', name).strip('-')

        if len(name) > max_len:
            name = name[:max_len].rstrip('-')

        return name

    def _generate_vault_filename(self, url_data: Dict, classification: Dict, queue_num: int) -> str:
        """Generate vault markdown filename."""
        fmt = self.config['vault_naming']['format']
        max_words = self.config['vault_naming']['max_title_words']
        separator = self.config['vault_naming']['separator']

        # Extract title from notes or use generic
        notes = url_data.get('notes', '')
        if notes:
            words = notes.split()[:max_words]
            title = separator.join(words)
        else:
            title = "Technique"

        creator = url_data.get('creator', 'unknown').replace('@', '').replace('.', '-')
        keywords = '-'.join(classification.get('keywords_matched', [])[:2]) or 'technique'

        filename = fmt.format(
            NN=f"{queue_num:03d}",
            Title=title,
            Creator=creator,
            Keywords=keywords
        )

        # Sanitize
        filename = re.sub(r'[<>:"|?*]', '', filename)
        filename = re.sub(r'\s+', '_', filename)

        return filename

    def _create_skill(self, skill_name: str, url_data: Dict, classification: Dict, queue_num: int):
        """Create Hermes skill file."""
        skill_dir = self.skills_dir / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)

        skill_path = skill_dir / 'SKILL.md'

        # Load template
        template_path = self.skill_dir / 'templates' / 'skill_template.md'
        if template_path.exists():
            with open(template_path, 'r') as f:
                template = f.read()
        else:
            template = self._get_default_skill_template()

        # Fill template
        now = datetime.now().isoformat()
        content = template.format(
            TITLE=skill_name.replace('davinci-resolve-', '').replace('-', ' ').title(),
            DESCRIPTION=f"Technique from @{url_data.get('creator', 'unknown')} Instagram Reel",
            SOURCE_URL=url_data['url'],
            CREATOR=url_data.get('creator', 'unknown'),
            INSTAGRAM_URL=url_data['url'],
            DATE_EXTRACTED=now[:10],
            DATE_PUBLISHED='Unknown',
            CATEGORY=classification['category'],
            FOLDER=classification['folder'],
            CATEGORY_TAG=classification['category'].lower().replace(' ', '-').replace('&', 'and'),
            TECHNIQUE_TAG=','.join(classification.get('keywords_matched', ['technique'])[:3]),
            RELATED_SKILL_1='davinci-resolve-related-technique',
            RELATED_SKILL_2='davinci-resolve-another-technique',
            DIFFICULTY='Intermediate',
            ESTIMATED_TIME='15 min',
            TECHNIQUE_OVERVIEW='Extracted from Instagram Reel. Full workflow to be documented.',
            KEY_CONCEPT_QUOTE='Key technique concept from the reel.',
            NODE_STRUCTURE='A --> B\nB --> C',
            NODE_TABLE='| 1 | Serial | Primary | Basic correction |\n| 2 | Parallel | Look | Creative grade |',
            PARAMETERS_SECTION='Parameters extracted from reel.',
            SCREENSHOT_DESCRIPTION='Node graph screenshot from reel.',
            SCREENSHOT_PATH='N/A',
            TIPS_SECTION='- Tip from reel\n- Variation',
            RELATED_TECHNIQUES='Related techniques to explore.',
            ADDITIONAL_REFERENCES='- Additional reference',
            TAGS_JOINED=', '.join(['davinci-resolve', 'color-grading', classification['category'].lower().replace(' ', '-')]),
            QUEUE_NUMBER=queue_num
        )

        with open(skill_path, 'w') as f:
            f.write(content)

    def _get_default_skill_template(self) -> str:
        """Default skill template if file not found."""
        return """---
name: {SKILL_NAME}
version: "1.0.0"
description: |
  {DESCRIPTION}
category: creative
tags:
  - davinci-resolve
  - color-grading
  - color-correction
  - {CATEGORY_TAG}
  - instagram-source
  - {TECHNIQUE_TAG}
author: Hermes Agent (instagram-davinci-learning-pipeline)
source_url: "{SOURCE_URL}"
creator: "@{CREATOR}"
date_extracted: "{DATE_EXTRACTED}"
queue_number: {QUEUE_NUMBER}
difficulty: "{DIFFICULTY}"
estimated_time: "{ESTIMATED_TIME}"
---

# {TITLE}

> **Source:** [{CREATOR} — Instagram Reel]({INSTAGRAM_URL})
> **Author:** @{CREATOR}
> **Type:** DaVinci Tutorial
> **Date Extracted:** {DATE_EXTRACTED}
> **Queue Position:** #{QUEUE_NUMBER}

---

## 🎯 Technique Overview

{TECHNIQUE_OVERVIEW}

### Key Concept

> {KEY_CONCEPT_QUOTE}

---

## 🛠️ Step-by-Step Workflow

### Node Structure

```mermaid
graph LR
{NODE_STRUCTURE}
```

### Node Details

| Node | Type | Operation | Key Parameters |
|------|------|-----------|----------------|
{NODE_TABLE}

---

## ⚙️ Key Parameters & Values

{PARAMETERS_SECTION}

---

## 📸 Visual Reference

{SCREENSHOT_DESCRIPTION}

> **Node Graph Screenshot:** {SCREENSHOT_PATH}

---

## 💡 Pro Tips & Variations

{TIPS_SECTION}

---

## 🔗 Related Techniques

{RELATED_TECHNIQUES}

---

## 📚 References & Further Reading

- [Original Instagram Reel]({INSTAGRAM_URL})
{ADDITIONAL_REFERENCES}

---

## 🏷️ Tags

`{TAGS_JOINED}`

---

*Generated by instagram-davinci-learning-pipeline v1.0.0 on {DATE_EXTRACTED}*
"""

    def _create_vault_note(self, filename: str, url_data: Dict, classification: Dict,
                           skill_name: str, queue_num: int):
        """Create vault markdown file."""
        folder_path = self.vault_path / classification['folder']
        folder_path.mkdir(parents=True, exist_ok=True)

        file_path = folder_path / filename

        # Load template
        template_path = self.skill_dir / 'templates' / 'vault_note_template.md'
        if template_path.exists():
            with open(template_path, 'r') as f:
                template = f.read()
        else:
            template = self._get_default_vault_template()

        now = datetime.now().isoformat()
        content = template.format(
            TITLE=filename.replace('.md', '').replace('_', ' '),
            DESCRIPTION=f"Technique from @{url_data.get('creator', 'unknown')}",
            URL=url_data['url'],
            CREATOR=url_data.get('creator', 'unknown'),
            DATE=now[:10],
            QUEUE_NUM=queue_num,
            SKILL_NAME=skill_name,
            NODE_STRUCTURE='A --> B\nB --> C',
            PARAM_1='Parameter 1', VALUE_1='Value', NOTE_1='Note',
            PARAM_2='Parameter 2', VALUE_2='Value', NOTE_2='Note',
            PARAM_3='Parameter 3', VALUE_3='Value', NOTE_3='Note',
            STEP_1='Step 1 description',
            STEP_2='Step 2 description',
            STEP_3='Step 3 description',
            BEFORE_IMG='N/A',
            AFTER_IMG='N/A',
            TIP_1='Tip from reel',
            TIP_2='Variation to try',
            TIP_3='Related technique',
            TAGS='davinci-resolve, color-grading, ' + classification['category'].lower().replace(' ', '-')
        )

        with open(file_path, 'w') as f:
            f.write(content)

    def _get_default_vault_template(self) -> str:
        """Default vault note template."""
        return """# {TITLE}

> **Source:** [{CREATOR} — Instagram Reel]({URL})
> **Author:** @{CREATOR}
> **Type:** DaVinci Tutorial
> **Date Extracted:** {DATE}
> **Queue Position:** #{QUEUE_NUM}
> **Skill:** `{SKILL_NAME}`

---

## 🎯 Technique Overview

{DESCRIPTION}

---

## 🛠️ Workflow

### Node Structure
{NODE_STRUCTURE}

### Key Settings
| Parameter | Value | Notes |
|-----------|-------|-------|
| {PARAM_1} | {VALUE_1} | {NOTE_1} |
| {PARAM_2} | {VALUE_2} | {NOTE_2} |
| {PARAM_3} | {VALUE_3} | {NOTE_3} |

### Step-by-Step
1. {STEP_1}
2. {STEP_2}
3. {STEP_3}

---

## 🎨 Before/After

| Before | After |
|--------|-------|
| ![Before]({BEFORE_IMG}) | ![After]({AFTER_IMG}) |

---

## 💡 Tips & Variations

- {TIP_1}
- {TIP_2}
- {TIP_3}

---

## 🔗 Related

- **Skill:** `{SKILL_NAME}`
- **Source:** [{URL}]({URL})
- **Creator:** @{CREATOR}

---

## 🏷️ Tags

{TAGS}

---

*Generated by instagram-davinci-learning-pipeline v1.0.0 on {DATE}*
"""

    def _create_camera_theory_note(self, url_data: Dict, classification: Dict, queue_num: int):
        """Create Camera Theory category note."""
        folder_path = self.vault_path / classification['folder']
        folder_path.mkdir(parents=True, exist_ok=True)

        # Generate filename
        filename = f"001-RAW-vs-LOG_Fundamentals.md"
        file_path = folder_path / filename

        now = datetime.now().isoformat()
        content = f"""# RAW vs LOG — Camera Theory Fundamentals

> **Source:** [@{url_data.get('creator', 'unknown')} — Instagram Reel]({url_data['url']})
> **Author:** @{url_data.get('creator', 'unknown')}
> **Type:** Camera Theory / Color Science Fundamentals
> **Date Added:** {now[:10]}
> **Instagram Queue:** #{queue_num}

---

## Core Distinction: RAW vs LOG

| Aspect | **RAW** | **LOG** |
|--------|---------|---------|
| **Category** | File Format / Container | Transfer Function / Gamma Curve |
| **What it is** | Unprocessed sensor data (or lightly compressed) | Logarithmic encoding of linear light |
| **Examples** | BRAW, ProRes RAW, R3D, ARRIRAW, CDNG | S-Log3, C-Log3, N-Log, V-Log, LogC |
| **Data structure** | Bayer-pattern sensor values (usually) | Encoded RGB/YCbCr values in log space |

---

## Key Technical Clarifications

> **\"Raw is a file format like ProRes or MP4. LOG is a transfer function like Rec709 or HLG. You're comparing apples to pears.\"**
> — *Instagram comment discussion*

---

## Practical Implications for DaVinci Resolve

### When You Have RAW (BRAW, R3D, ProRes RAW, ARRIRAW)
```
Clip → RAW Panel (Decode Settings)
    → Color Space: Camera Native / DaVinci Wide Gamut
    → Gamma: Linear / Log / Camera Log
    → White Balance: Temp/Tint (metadata, non-destructive)
    → ISO: Exposure Index (metadata, non-destructive)
→ Node Tree (Scene-Referred Working Space)
```

### When You Have Non-RAW LOG (S-Log3, C-Log3, N-Log, V-Log)
```
Clip → Input CST (or RCM Input)
    → Input Color Space: S-Gamut3.Cine / S-Log3 (etc.)
    → Output: DaVinci Wide Gamut Intermediate / DWG
→ Node Tree (Scene-Referred Working Space)
```

---

## References & Further Reading

- [Original Instagram Reel]({url_data['url']})
- [Sony S-Log3 White Paper](https://www.sony.com/en/SonyInfo/News/Press_Archive/201406/14-056E.pdf)
- [ARRI LogC Documentation](https://www.arri.com/en/learn-help/learn-help-camera-system/log-c)
- [Blackmagic RAW SDK / White Paper](https://www.blackmagicdesign.com/products/blackmagicraw)

---

## Tags

`#camera-theory` `#raw-vs-log` `#color-science` `#color-management` `#davinci-resolve` `#raw-workflow` `#log-workflow` `#scene-referred` `#color-space-transform` `#cst` `#rcm` `#davinci-wide-gamut`

---

*Created from Instagram Learning Queue #{queue_num} — reclassified from \"Skipped (General Knowledge)\" to \"Camera Theory\" category for future reference.*
"""

        with open(file_path, 'w') as f:
            f.write(content)

        self.session['updated_vault_files'].append(f"{classification['folder']}/{filename}")

    def _update_queue(self, url_data: Dict, status: str, skill_name: str = None,
                      vault_file: str = None, folder: str = None, skip_reason: str = None):
        """Update the Instagram Learning Queue markdown file."""
        # This would update the queue file
        # For now, just log
        pass

    def _regenerate_exports(self):
        """Regenerate JSON/CSV exports and architecture diagram."""
        print("\n📦 Regenerating exports...")

        # This would call regenerate_exports_and_diagram skill
        # For now, run the export generation script
        try:
            export_script = self.vault_path.parent / 'regenerate_exports.py'
            if export_script.exists():
                subprocess.run([sys.executable, str(export_script)], cwd=self.vault_path, check=True)
            else:
                # Run inline export generation
                self._generate_exports_inline()
        except Exception as e:
            print(f"⚠️  Export generation failed: {e}")

    def _generate_exports_inline(self):
        """Generate exports inline (simplified)."""
        import json
        import csv
        from datetime import datetime

        # Scan vault files
        md_files = []
        for root, dirs, files in os.walk(self.vault_path):
            for f in files:
                if f.endswith('.md') and not f.startswith('.'):
                    full = Path(root) / f
                    rel = full.relative_to(self.vault_path)
                    folder = str(rel.parent) if rel.parent != Path('.') else 'ROOT'
                    with open(full, 'r') as fp:
                        content = fp.read(2000)
                    md_files.append({
                        'path': str(rel),
                        'folder': folder,
                        'filename': f,
                        'size': full.stat().st_size,
                        'preview': content[:500]
                    })

        # Scan skills
        skills = []
        for item in self.skills_dir.iterdir():
            if item.is_dir() and item.name.startswith('davinci-resolve-'):
                skill_md = item / 'SKILL.md'
                if skill_md.exists():
                    with open(skill_md, 'r') as f:
                        content = f.read()
                    # Parse frontmatter
                    fm = {}
                    if content.startswith('---'):
                        parts = content.split('---', 2)
                        if len(parts) >= 3:
                            try:
                                fm = yaml.safe_load(parts[1]) or {}
                            except:
                                pass
                    skills.append({
                        'skill_name': item.name.replace('davinci-resolve-', ''),
                        'title': fm.get('title', item.name),
                        'description': fm.get('description', ''),
                        'tags': fm.get('tags', []),
                        'category': fm.get('category', 'creative'),
                        'folder': item.name,
                        'size': len(content)
                    })

        # Write exports
        exports = {
            'knowledge_base_export.json': {
                'metadata': {
                    'generated': datetime.now().isoformat(),
                    'total_markdown_files': len(md_files),
                    'total_skills': len(skills),
                    'total_folders': len(set(f['folder'] for f in md_files))
                },
                'files': md_files,
                'skills': skills
            },
            'skills_export.json': {
                'metadata': {
                    'generated': datetime.now().isoformat(),
                    'total_skills': len(skills)
                },
                'skills': skills
            }
        }

        for filename, data in exports.items():
            path = self.vault_path / filename
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"   ✅ {filename}")

        # CSV exports
        for name, data in [('knowledge_base_export.csv', md_files), ('skills_export.csv', skills)]:
            path = self.vault_path / name
            with open(path, 'w', newline='') as f:
                if data:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
            print(f"   ✅ {name}")

    def _print_summary(self):
        """Print final summary."""
        print("\n" + "=" * 60)
        print("📊 PIPELINE SUMMARY")
        print("=" * 60)
        print(f"   ✅ Processed:     {self.session['processed']}")
        print(f"   📚 Camera Theory: {self.session['camera_theory']}")
        print(f"   ⏭️  Skipped:       {self.session['skipped']}")
        print(f"   ❌ Failed:        {self.session['failed']}")
        print(f"   🛠️  New Skills:     {len(self.session['new_skills'])}")
        print(f"   📄 Vault Files:   {len(self.session['updated_vault_files'])}")

        if self.session['new_skills']:
            print("\n   New Skills:")
            for s in self.session['new_skills']:
                print(f"      - {s}")

        if self.session['errors']:
            print("\n   Errors:")
            for e in self.session['errors']:
                print(f"      - {e['url']}: {e['error']}")

        print(f"\n📁 Vault: {self.vault_path}")
        print(f"🛠️  Skills: {self.skills_dir}")


def main():
    parser = argparse.ArgumentParser(
        description='Instagram → DaVinci Learning Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_pipeline.py --input urls.rtf
  python run_pipeline.py --input urls.csv --batch-size 5
  python run_pipeline.py --input urls.txt --dry-run
  python run_pipeline.py --input urls.rtf --filter-creator "caleboshi"
  python run_pipeline.py --input urls.rtf --resume --force
        """
    )
    parser.add_argument('--input', '-i', required=True, help='Input file (RTF, CSV, JSON, TXT)')
    parser.add_argument('--config', '-c', help='Custom config YAML path')
    parser.add_argument('--resume', '-r', action='store_true', help='Resume from last checkpoint')
    parser.add_argument('--dry-run', '-d', action='store_true', help='Classify only, do not process')
    parser.add_argument('--filter-creator', '-f', help='Only process URLs from specific creator')
    parser.add_argument('--retry-failed', action='store_true', help='Retry previously failed URLs')
    parser.add_argument('--batch-size', '-b', type=int, help='Batch size (default from config)')
    parser.add_argument('--force', action='store_true', help='Force reprocess already-queued URLs')

    args = parser.parse_args()

    pipeline = InstagramDavinciPipeline(args.config)
    pipeline.run(
        input_file=args.input,
        resume=args.resume,
        dry_run=args.dry_run,
        filter_creator=args.filter_creator,
        retry_failed=args.retry_failed,
        batch_size=args.batch_size,
        force=args.force
    )


if __name__ == '__main__':
    main()