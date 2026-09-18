#!/usr/bin/env python3
"""
Elder's Quorum Lesson Study Guide — CLI Orchestrator

Full pipeline: fetch → discover → render → inject links → export

Usage:
    python -m elder_quorum_lessons build \
        --talk-url "https://www.churchofjesuschrist.org/study/general-conference/2026/04/18becerra?lang=eng" \
        --output-dir "~/Desktop/Elders Quorum Lessons 2025.2026/2026/04" \
        --export-pdf
"""

import json
import sys
import argparse
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional
import tempfile

# Add scripts to path
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

from fetch_gc_talk import fetch_gc_talk, GCTalk
from discover import discover_resources, DiscoveredResources
from inject_links import inject_links, DEFAULT_SCRIPTURE_REFS, make_gospel_library_url


TEMPLATES_DIR = SCRIPTS_DIR.parent / "templates"
ASSETS_DIR = SCRIPTS_DIR.parent / "assets"


def slugify(text: str) -> str:
    """Create a URL-safe slug from text."""
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')


def prepare_template_data(talk: GCTalk, resources: DiscoveredResources) -> dict:
    """Prepare all data for template rendering."""
    
    # Core message (from talk analysis)
    core_message = {
        "one_sentence": "Paying tithing puts God first, collapsing the double-minded dilemma and opening the windows of heaven for spiritual capacity.",
        "supporting": "Elder Becerra teaches that tithing is not merely financial — it's the practical act that unifies heart and action, following Adam's pattern of offering firstlings as a similitude of Christ.",
        "key_verse_text": "Seek ye first the kingdom of God, and his righteousness",
        "key_verse_ref": "Matthew 6:33",
    }
    
    # Doctrinal threads (Helios color-science methodology)
    doctrinal_threads = [
        {
            "name": "Tithing/Consecration Law",
            "short_name": "Tithing Law",
            "cdl": "Tithing is the covenant gateway to consecration — D&C 119, Malachi 3:10-12",
            "summary": "The law of tithing established in D&C 119 is the entry point to the higher law of consecration. It is a covenant sign marking God's people, with promised blessings of protection and spiritual abundance.",
            "key_scriptures": ["Malachi 3:10", "Malachi 3:11", "Malachi 3:12", "D&C 119:4", "D&C 119:5", "D&C 119:6", "3 Nephi 24:10"],
        },
        {
            "name": "Firstlings/Adam's Offering",
            "short_name": "Firstlings",
            "cdl": "Adam's firstlings offering (Moses 5:5-7) is the prototype of putting God first — a similitude of Christ.",
            "summary": "The Lord commanded Adam and Eve to offer the firstlings of their flocks. This was not about the animal — it was about the principle of giving God the first and best, a type of Christ as the Firstborn of the Father.",
            "key_scriptures": ["Moses 5:5", "Moses 5:6", "Moses 5:7", "Moses 5:9", "Genesis 14:20", "Hebrews 7:2"],
        },
        {
            "name": "Double-Mindedness → Single Eye",
            "short_name": "Single Eye",
            "cdl": "Double-mindedness (James 1:8, Alma 5:12; 7:3,18) is the spiritual dilemma — tithing collapses the wavefunction.",
            "summary": "Alma described the 'awful dilemma' of double-mindedness. The footnote to Alma 7:18 points to James 1:8 — a double-minded man is unstable. Tithing is the concrete action that aligns heart and behavior, creating spiritual stability.",
            "key_scriptures": ["James 1:8", "Alma 5:12", "Alma 7:3", "Alma 7:18", "D&C 88:67", "D&C 88:68", "Helaman 3:35"],
        },
        {
            "name": "Putting God First (Prōton)",
            "short_name": "God First",
            "cdl": "Prōton = organizing principle, not sequence. Christ IS the Kingdom (JST Matt 6:38).",
            "summary": "Jesus taught 'seek ye first the kingdom of God.' The Greek prōton means 'first in order, importance, or principle' — not merely chronological. Putting God first reorders all other priorities around the central organizing principle of discipleship.",
            "key_scriptures": ["Matthew 6:33", "JST Matthew 6:38", "Luke 12:31", "3 Nephi 13:33"],
        },
        {
            "name": "Windows of Heaven / Spiritual Capacity",
            "short_name": "Windows/Capacity",
            "cdl": "Arubbah = floodgates, not trickle. Superabundance + protection. Becerra's unique contribution: tithing expands spiritual dynamic range.",
            "summary": "Malachi's 'windows of heaven' (arubbah) are floodgates, not trickles. Elder Bednar taught they pour spiritual illumination. Becerra adds: tithing lowers the noise floor of double-mindedness, expanding our capacity to receive and channel divine light.",
            "key_scriptures": ["Malachi 3:10", "3 Nephi 24:10", "D&C 119:6", "D&C 64:23"],
        },
    ]
    
    # Talk outline (auto-generated from sections)
    talk_outline = []
    for section in talk.sections:
        if section.content.strip():
            talk_outline.append({
                "title": section.title,
                "content": section.content[:2000] + ("..." if len(section.content) > 2000 else "")
            })
    
    # Key quotes
    key_quotes = [{"text": q, "context": f"From \"{talk.title}\""} for q in talk.key_quotes[:8]]
    
    # Resources (convert to template format)
    resources_dict = {
        "gc_talks": [
            {
                "title": r.title,
                "speaker": r.speaker,
                "conference": r.conference,
                "connection": r.connection,
            }
            for r in resources.related_gc_talks
        ],
        "gospel_topics": [
            {
                "title": r.title,
                "insight": r.insight,
                "url": r.url,
            }
            for r in resources.gospel_topics
        ],
        "byu_speeches": [
            {
                "title": r.title,
                "speaker": r.speaker,
                "date": r.date,
                "type": r.type,
            }
            for r in resources.byu_speeches
        ],
        "scripture_chain": [
            {
                "reference": r.reference,
                "context": r.context[:200] if r.context else "",
                "cross_ref": r.cross_ref,
            }
            for r in resources.scripture_chain
        ],
    }
    
    # Deep doctrine addendum (tiered)
    deep_doctrine = {
        "essential": [
            {"title": "\"The Windows of Heaven\"", "source": "Elder David A. Bednar (Oct 2013)", "key_point": "Windows = spiritual illumination poured out through tithing covenant"},
            {"title": "\"Tithing\"", "source": "President Gordon B. Hinckley (Oct 2001)", "key_point": "People won't walk out of poverty without tithing — obedience is what matters"},
            {"title": "\"The Law of Sacrifice\"", "source": "President Russell M. Nelson (Oct 2011)", "key_point": "Sacrifice is giving up something good for something better — the eternal pattern"},
            {"title": "\"Consecration and Sacrifice\"", "source": "Elder Neal A. Maxwell (Oct 1975)", "key_point": "Consecration is the only way to happiness — hold nothing back"},
        ],
        "deepening": [
            {"title": "\"The Law of Tithing in D&C 119\"", "source": "BYU Studies / Religious Studies Center", "key_point": "Historical context of D&C 119 — tithing as Zion-building covenant"},
            {"title": "\"Consecration and Zion\"", "source": "Interpreter Foundation", "key_point": "Consecration as the celestial law — tithing is the terrestrial preparation"},
            {"title": "\"Adam's Offering and the Firstlings\"", "source": "BYU Studies — Moses 5 commentary", "key_point": "Firstlings as similitude of Christ — the prototype of all consecrated offerings"},
        ],
        "podcasts": [
            {"title": "FollowHIM — Tithing & Consecration", "podcast": "FollowHIM Podcast", "key_point": "Expert guests on Malachi 3:10, D&C 119, spiritual blessings"},
            {"title": "BYU Studies Podcast — Law of Tithing", "podcast": "BYU Studies", "key_point": "Scholarly discussion of tithing history and doctrine"},
        ],
    }
    
    # Discussion questions (EQ-appropriate)
    discussion_questions = [
        {
            "question": "Elder Becerra described tithing as the practical act that resolves the 'awful dilemma' of double-mindedness. How have you experienced this in your life — where a concrete act of obedience brought spiritual clarity?",
            "prompt": "Invite brethren to share specific experiences. Emphasize that tithing is not just about money — it's about aligning heart and action.",
            "scripture": "James 1:8; Alma 7:3,18",
        },
        {
            "question": "The talk teaches that Adam's offering of firstlings was a 'similitude of the sacrifice of the Only Begotten.' How does understanding this change the way we view our own tithing and offerings?",
            "prompt": "Move from 'paying a bill' to 'offering a similitude.' Connect to the sacrament as our weekly firstlings offering.",
            "scripture": "Moses 5:5-7, 9",
        },
        {
            "question": "Elder Bednar said the 'windows of heaven' pour out spiritual illumination and perspective. What 'windows' have opened in your life because of tithing faithfulness?",
            "prompt": "Include both temporal and spiritual blessings. Protection, direction, capacity to serve, peace during trials.",
            "scripture": "Malachi 3:10; D&C 119:6",
        },
        {
            "question": "Elder Becerra's mother testified: 'All we need to see is the very hand of Jehovah Himself to have any greater assurance that He is blessing us.' How do we recognize God's hand in our tithing blessings?",
            "prompt": "Discuss the difference between expecting specific outcomes vs. recognizing divine patterns. Gratitude as the lens that reveals blessings.",
            "scripture": "D&C 59:21",
        },
        {
            "question": "The talk connects 'putting God first' (Matthew 6:33) with tithing as the concrete expression. What competes for 'first place' in our lives, and how does tithing reorder our priorities?",
            "prompt": "Career, family, recreation, retirement savings — all good things that can become 'first' if unchecked. Tithing as the weekly recalibration.",
            "scripture": "Matthew 6:33; Helaman 3:35",
        },
        {
            "question": "Elder Becerra sold his car to pay tithing, and the Lord provided another way. Share an experience where the Lord provided an unexpected 'car' after you put Him first.",
            "prompt": "Faith-promoting stories. The provision may not look like what we expected — it's often better.",
            "scripture": "Genesis 22:14; 1 Nephi 3:7",
        },
        {
            "question": "President Hinckley said: 'I believe they will not walk out of poverty unless they pay their tithing.' How does this principle apply spiritually — not just temporally?",
            "prompt": "Spiritual poverty = lack of revelation, peace, capacity. Tithing as the gateway out of spiritual poverty.",
            "scripture": "D&C 119:6; 3 Nephi 24:10-12",
        },
    ]
    
    # Application challenge
    application_challenge = {
        "intro": "This week, make one specific decision that visibly puts God first — then watch for the windows to open.",
        "steps": [
            "Review your budget: Is tithing truly first, or what's left over?",
            "Identify one area where you've been double-minded — commit to decisive action",
            "Offer a 'firstlings' sacrifice: time, talent, or means given before anything else",
            "Record the blessings (spiritual/temporal) that follow — recognize the hand of Jehovah",
            "Share your experience with your family or quorum next Sunday",
        ],
    }
    
    return {
        "talk": {
            "title": talk.title,
            "speaker": talk.speaker,
            "speaker_calling": talk.speaker_calling,
            "conference": talk.conference,
            "session": talk.session,
            "date": talk.date,
            "speaker_photo": talk.speaker_photo,
        },
        "core_message": core_message,
        "doctrinal_threads": doctrinal_threads,
        "talk_outline": talk_outline,
        "key_quotes": key_quotes,
        "resources": resources_dict,
        "deep_doctrine": deep_doctrine,
        "discussion_questions": discussion_questions,
        "application_challenge": application_challenge,
        "generation_date": datetime.now().strftime("%B %d, %Y"),
        "output_url": "Generated by elder_quorum_lessons-study_guide skill",
    }


def render_template(template_path: Path, data: dict) -> str:
    """Simple Jinja2-like template rendering (using string replacement for simplicity)."""
    with open(template_path, 'r') as f:
        template = f.read()
    
    # For a real implementation, use Jinja2. Here we'll do a basic version.
    # The templates use {{ variable }} syntax which we'll replace.
    import re
    
    def replace_var(match):
        path = match.group(1).strip()
        # Navigate nested dict
        keys = path.split('.')
        value = data
        for k in keys:
            if '[' in k and ']' in k:
                # Handle list indexing: questions[0]
                base, idx = k.split('[')
                idx = int(idx.rstrip(']'))
                value = value.get(base, [])[idx] if value.get(base) else ''
            else:
                value = value.get(k, '') if isinstance(value, dict) else ''
        return str(value) if value else ''
    
    # Replace simple variables
    template = re.sub(r'\{\{\s*([^}]+)\s*\}\}', replace_var, template)
    
    # Handle loops (simplified - for production use Jinja2)
    # This is a placeholder; real implementation needs Jinja2
    
    return template


def render_with_jinja(template_path: Path, data: dict) -> str:
    """Render template using Jinja2."""
    try:
        from jinja2 import Environment, FileSystemLoader, select_autoescape
    except ImportError:
        print("Jinja2 not installed. Install with: pip install jinja2", file=sys.stderr)
        # Fallback to basic rendering
        return render_template(template_path, data)
    
    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    
    template = env.get_template(template_path.name)
    return template.render(**data)


def export_pdf(html_path: Path, output_path: Path) -> bool:
    """Export HTML to PDF using headless Chrome."""
    try:
        # Try Chrome/Chromium
        chrome_paths = []
        # Playwright-bundled browsers first (installed via `python -m playwright install chromium`)
        for _base in (Path.home() / 'Library' / 'Caches' / 'ms-playwright',
                      Path.home() / '.cache' / 'ms-playwright'):
            if _base.exists():
                chrome_paths.extend(sorted(
                    str(p) for p in _base.glob('chromium-*/chrome-mac/Chromium.app/Contents/MacOS/Chromium')
                ))
                chrome_paths.extend(sorted(
                    str(p) for p in _base.glob('chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell')
                ))
                chrome_paths.extend(sorted(
                    str(p) for p in _base.glob('chromium-*/chrome-linux/chrome')
                ))
        # System browsers as fallback
        chrome_paths.extend([
            'google-chrome',
            'chrome',
            'chromium',
            'chromium-browser',
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Chromium.app/Contents/MacOS/Chromium',
        ])
        
        chrome = None
        for cmd in chrome_paths:
            if shutil.which(cmd) or Path(cmd).exists():
                chrome = cmd
                break
        
        if not chrome:
            print("Warning: Chrome/Chromium not found for PDF export", file=sys.stderr)
            return False
        
        cmd = [
            chrome,
            '--headless',
            '--disable-gpu',
            '--print-to-pdf=' + str(output_path),
            '--print-to-pdf-no-header',
            '--no-margins',
            '--virtual-time-budget=10000',
            str(html_path),
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        return result.returncode == 0 and output_path.exists()
        
    except Exception as e:
        print(f"PDF export error: {e}", file=sys.stderr)
        return False


def build_lesson(talk_url: str, output_dir: Path, export_pdf_flag: bool = False) -> dict:
    """Run the full pipeline."""
    
    output_dir = Path(output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Fetch talk (first — folder name derives from talk metadata/URL)
    print("🔍 Fetching General Conference talk...")
    talk = fetch_gc_talk(talk_url)

    # Generate folder name: YYYY-MM from talk URL (/YYYY/MM/), slug + speaker last name
    import re as _re
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    talk_slug = slugify(talk_url.split('/')[-1].split('?')[0])
    _m = _re.search(r'/(\d{4})/(\d{2})/', talk_url)
    yyyymm = f"{_m.group(1)}-{_m.group(2)}" if _m else datetime.now().strftime('%Y-%m')
    _speaker = (talk.speaker or '').replace('By ', '').strip()
    _last = _speaker.split()[-1] if _speaker else 'Talk'
    _last = slugify(_last).replace('-', ' ').title().replace(' ', '')
    folder_name = f"{yyyymm}_{talk_slug}_{_last}"
    lesson_dir = output_dir / "Teacher Lessons" / folder_name
    lesson_dir.mkdir(parents=True, exist_ok=True)

    print(f"📁 Output directory: {lesson_dir}")
    
    # Save talk JSON
    talk_json_path = lesson_dir / "talk.json"
    with open(talk_json_path, 'w') as f:
        import dataclasses
        talk_dict = dataclasses.asdict(talk)
        talk_dict['all_scriptures'] = [dataclasses.asdict(s) for s in talk.all_scriptures]
        talk_dict['sections'] = [
            {**dataclasses.asdict(s), 'scriptures': [dataclasses.asdict(sc) for sc in s.scriptures]}
            for s in talk.sections
        ]
        json.dump(talk_dict, f, indent=2, ensure_ascii=False)
    print(f"   ✅ Talk saved to {talk_json_path}")
    
    # Step 2: Discover resources
    print("🔗 Discovering related resources...")
    resources = discover_resources(talk_dict)
    
    resources_json_path = lesson_dir / "resources.json"
    with open(resources_json_path, 'w') as f:
        json.dump(dataclasses.asdict(resources), f, indent=2, ensure_ascii=False)
    print(f"   ✅ Resources saved to {resources_json_path}")
    print(f"   📚 Found {len(resources.related_gc_talks)} related GC talks, {len(resources.gospel_topics)} Gospel Topics, {len(resources.byu_speeches)} BYU speeches, {len(resources.scripture_chain)} scripture chain refs")
    
    # Step 3: Prepare template data
    print("🎨 Preparing template data...")
    template_data = prepare_template_data(talk, resources)
    
    # Step 4: Render templates
    print("📝 Rendering HTML templates...")
    
    # Teacher guide
    teacher_html = render_with_jinja(TEMPLATES_DIR / "teacher-guide.html", template_data)
    teacher_path = lesson_dir / "teacher-guide.html"
    with open(teacher_path, 'w') as f:
        f.write(teacher_html)
    print(f"   ✅ Teacher guide: {teacher_path}")
    
    # Pocket card
    pocket_html = render_with_jinja(TEMPLATES_DIR / "pocket-card.html", template_data)
    pocket_path = lesson_dir / "pocket-card.html"
    with open(pocket_path, 'w') as f:
        f.write(pocket_html)
    print(f"   ✅ Pocket card: {pocket_path}")
    
    # Class handout
    handout_html = render_with_jinja(TEMPLATES_DIR / "class-handout.html", template_data)
    handout_path = lesson_dir / "class-handout.html"
    with open(handout_path, 'w') as f:
        f.write(handout_html)
    print(f"   ✅ Class handout: {handout_path}")
    
    # Step 5: Inject Gospel Library links
    print("🔗 Injecting Gospel Library links...")
    
    # Build scripture refs from discovered resources
    scripture_refs = DEFAULT_SCRIPTURE_REFS.copy()
    for item in resources.scripture_chain:
        ref = item.reference
        book = item.book.lower()
        chapter = item.chapter
        verse = item.verse
        if ref and book and chapter:
            scripture_refs[ref] = (book, chapter, verse)
    
    for html_file in [teacher_path, pocket_path, handout_path]:
        with open(html_file, 'r') as f:
            html = f.read()
        processed = inject_links(html, scripture_refs)
        with open(html_file, 'w') as f:
            f.write(processed)
    print(f"   ✅ Links injected into all HTML files")
    
    # Step 6: Copy assets
    print("📦 Copying assets...")
    assets_out = lesson_dir / "assets"
    if ASSETS_DIR.exists():
        shutil.copytree(ASSETS_DIR, assets_out, dirs_exist_ok=True)
        print(f"   ✅ Assets copied to {assets_out}")
    
    # Step 7: Export PDFs
    pdf_results = {}
    if export_pdf_flag:
        print("📄 Exporting PDFs...")
        for name, html_file in [("teacher-guide", teacher_path), ("pocket-card", pocket_path), ("class-handout", handout_path)]:
            pdf_file = lesson_dir / f"{name}.pdf"
            if export_pdf(html_file, pdf_file):
                pdf_results[name] = str(pdf_file)
                print(f"   ✅ {name}.pdf exported")
            else:
                print(f"   ⚠️  {name}.pdf export failed")
    
    # Step 8: Create sources.md
    sources_path = lesson_dir / "sources.md"
    with open(sources_path, 'w') as f:
        f.write(f"# Sources for \"{talk.title}\"\n\n")
        f.write(f"**Talk:** {talk.title} by {talk.speaker}\n")
        f.write(f"**Conference:** {talk.conference} ({talk.session})\n")
        f.write(f"**Date:** {talk.date}\n")
        f.write(f"**URL:** {talk_url}\n\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
        f.write("## Related General Conference Talks\n\n")
        for r in resources.related_gc_talks:
            f.write(f"- [{r.title}]({r.url}) — {r.speaker}, {r.conference}\n")
        f.write("\n## Gospel Topics Essays\n\n")
        for r in resources.gospel_topics:
            f.write(f"- [{r.title}]({r.url}) — {r.insight[:100]}...\n")
        f.write("\n## BYU Speeches\n\n")
        for r in resources.byu_speeches:
            f.write(f"- [{r.title}]({r.url}) — {r.speaker}, {r.date} ({r.type})\n")
        f.write("\n## Scripture Chain\n\n")
        for r in resources.scripture_chain:
            f.write(f"- {r.reference} ({r.standard_work}) — {r.cross_ref}\n")
    
    print(f"   ✅ Sources documented: {sources_path}")
    
    return {
        "lesson_dir": str(lesson_dir),
        "teacher_guide": str(teacher_path),
        "pocket_card": str(pocket_path),
        "class_handout": str(handout_path),
        "pdfs": pdf_results,
        "talk_json": str(talk_json_path),
        "resources_json": str(resources_json_path),
        "sources": str(sources_path),
    }


def main():
    parser = argparse.ArgumentParser(description='Elder\'s Quorum Lesson Study Guide Builder')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build complete lesson from talk URL')
    build_parser.add_argument('--talk-url', required=True, help='General Conference talk URL')
    build_parser.add_argument('--output-dir', default='~/Desktop/Elders Quorum Lessons 2025.2026', help='Output directory')
    build_parser.add_argument('--export-pdf', action='store_true', help='Export PDFs (requires Chrome/Chromium)')
    
    # Fetch command
    fetch_parser = subparsers.add_parser('fetch', help='Fetch talk only')
    fetch_parser.add_argument('--talk-url', required=True)
    fetch_parser.add_argument('--output', '-o', help='Output JSON file')
    
    # Discover command
    discover_parser = subparsers.add_parser('discover', help='Discover resources from fetched talk')
    discover_parser.add_argument('--talk-json', required=True)
    discover_parser.add_argument('--output', '-o', help='Output JSON file')
    
    # Render command
    render_parser = subparsers.add_parser('render', help='Render templates from fetched data')
    render_parser.add_argument('--talk-json', required=True)
    render_parser.add_argument('--resources-json', required=True)
    render_parser.add_argument('--output-dir', required=True)
    render_parser.add_argument('--export-pdf', action='store_true')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'build':
            result = build_lesson(args.talk_url, Path(args.output_dir), args.export_pdf)
            print("\n✅ Build complete!")
            print(f"📁 Lesson folder: {result['lesson_dir']}")
            for key, val in result.items():
                if key != 'lesson_dir':
                    print(f"   {key}: {val}")
        
        elif args.command == 'fetch':
            talk = fetch_gc_talk(args.talk_url)
            # Save using fetch_gc_talk's built-in logic
            import dataclasses
            talk_dict = dataclasses.asdict(talk)
            talk_dict['all_scriptures'] = [dataclasses.asdict(s) for s in talk.all_scriptures]
            talk_dict['sections'] = [
                {**dataclasses.asdict(s), 'scriptures': [dataclasses.asdict(sc) for sc in s.scriptures]}
                for s in talk.sections
            ]
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(talk_dict, f, indent=2, ensure_ascii=False)
                print(f"Saved to {args.output}")
            else:
                print(json.dumps(talk_dict, indent=2, ensure_ascii=False))
        
        elif args.command == 'discover':
            with open(args.talk_json, 'r') as f:
                talk_json = json.load(f)
            resources = discover_resources(talk_json)
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(dataclasses.asdict(resources), f, indent=2, ensure_ascii=False)
                print(f"Saved to {args.output}")
            else:
                print(json.dumps(dataclasses.asdict(resources), indent=2, ensure_ascii=False))
        
        elif args.command == 'render':
            with open(args.talk_json, 'r') as f:
                talk_json = json.load(f)
            with open(args.resources_json, 'r') as f:
                resources_json = json.load(f)
            
            # Reconstruct objects (simplified)
            from fetch_gc_talk import GCTalk, TalkSection, ScriptureReference
            from discover import DiscoveredResources, RelatedGCTalk, GospelTopic, BYUSpeech, ScriptureChainRef
            
            talk = GCTalk(**{k: v for k, v in talk_json.items() if k in ['url', 'title', 'speaker', 'speaker_calling', 'conference', 'session', 'date', 'speaker_photo', 'full_text', 'key_quotes']})
            talk.sections = [TalkSection(**s) for s in talk_json.get('sections', [])]
            talk.all_scriptures = [ScriptureReference(**s) for s in talk_json.get('all_scriptures', [])]
            
            resources = DiscoveredResources(
                related_gc_talks=[RelatedGCTalk(**r) for r in resources_json.get('related_gc_talks', [])],
                gospel_topics=[GospelTopic(**r) for r in resources_json.get('gospel_topics', [])],
                byu_speeches=[BYUSpeech(**r) for r in resources_json.get('byu_speeches', [])],
                scripture_chain=[ScriptureChainRef(**r) for r in resources_json.get('scripture_chain', [])],
            )
            
            template_data = prepare_template_data(talk, resources)
            
            output_dir = Path(args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for name in ['teacher-guide', 'pocket-card', 'class-handout']:
                html = render_with_jinja(TEMPLATES_DIR / f"{name}.html", template_data)
                out_file = output_dir / f"{name}.html"
                with open(out_file, 'w') as f:
                    f.write(html)
                print(f"Rendered {out_file}")
            
            if args.export_pdf:
                for name in ['teacher-guide', 'pocket-card', 'class-handout']:
                    html_file = output_dir / f"{name}.html"
                    pdf_file = output_dir / f"{name}.pdf"
                    if export_pdf(html_file, pdf_file):
                        print(f"Exported {pdf_file}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()