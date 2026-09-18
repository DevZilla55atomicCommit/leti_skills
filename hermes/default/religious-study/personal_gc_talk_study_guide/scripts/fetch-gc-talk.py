#!/usr/bin/env python3
"""
fetch-gc-talk.py — Extract General Conference talk content from churchofjesuschrist.org

Usage:
    python fetch-gc-talk.py "Elder Jorge T. Becerra" "Tithing—Putting God First" "April 2026"
    python fetch-gc-talk.py --url "https://www.churchofjesuschrist.org/study/general-conference/2026/04/tithing-putting-god-first?lang=eng"

Requires: playwright (pip install playwright && playwright install chromium)
"""

import asyncio
import json
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime
from urllib.parse import quote_plus


async def fetch_talk_via_search(page, speaker, title, conference):
    """Search for talk and navigate to it."""
    search_query = quote_plus(f"{speaker} {title} {conference}")
    search_url = f"https://www.churchofjesuschrist.org/search?query={search_query}&lang=eng"
    
    await page.goto(search_url, wait_until="networkidle")
    await page.wait_for_timeout(3000)
    
    # Click first result
    try:
        first_result = page.locator('listitem >> link').first
        await first_result.click()
        await page.wait_for_timeout(3000)
        return True
    except Exception as e:
        print(f"Search click failed: {e}", file=sys.stderr)
        return False


async def fetch_talk_direct(page, url):
    """Navigate directly to talk URL."""
    await page.goto(url, wait_until="networkidle")
    await page.wait_for_timeout(3000)
    return True


async def extract_talk_content(page):
    """Extract all content from the talk page."""
    # Wait for article to load
    await page.wait_for_selector('article', timeout=10000)
    await page.wait_for_timeout(2000)
    
    # Get full page content
    content = await page.evaluate("""() => {
        const article = document.querySelector('article');
        if (!article) return null;
        
        // Get all text content
        const paragraphs = Array.from(article.querySelectorAll('p, h1, h2, h3, h4, h5, h6'))
            .map(el => el.innerText.trim())
            .filter(t => t.length > 0);
        
        // Get scripture links
        const scriptureLinks = Array.from(article.querySelectorAll('a[href*="/scriptures/"]'))
            .map(a => ({
                text: a.innerText.trim(),
                href: a.href,
                title: a.title || ''
            }));
        
        // Get hero image
        const heroImg = article.querySelector('img') || document.querySelector('sectionheader img');
        const heroImage = heroImg ? heroImg.src : null;
        
        // Get title
        const titleEl = document.querySelector('sectionheader h1, article h1, h1');
        const title = titleEl ? titleEl.innerText.trim() : '';
        
        // Get speaker from page
        const speakerMatch = document.body.innerText.match(/by\\s+(Elder|Bishop|President|Sister|Brother)\\s+([^.]+)/i);
        const speaker = speakerMatch ? speakerMatch[0].replace('by ', '').trim() : '';
        
        return {
            title: title,
            speaker: speaker,
            paragraphs: paragraphs,
            scriptureLinks: scriptureLinks,
            heroImage: heroImage,
            fullText: paragraphs.join('\\n\\n')
        };
    }""")
    
    return content


def parse_scripture_refs(scripture_links):
    """Parse scripture links into structured references."""
    refs = []
    for link in scripture_links:
        # Extract book, chapter, verse from URL
        match = re.search(r'/scriptures/(\w+)/(\w+)/(\d+)\?lang=eng(?:&id=([^&]+))?', link['href'])
        if match:
            volume, book, chapter, verses = match.groups()
            refs.append({
                'text': link['text'],
                'volume': volume,
                'book': book,
                'chapter': int(chapter),
                'verses': verses,
                'url': link['href']
            })
    return refs


def build_gospel_library_url(volume, book, chapter, verses=None):
    """Build Gospel Library URL from components."""
    path_map = {
        'ot': 'ot', 'nt': 'nt', 'bofm': 'bofm', 'dc': 'dc', 'pgp': 'pgp'
    }
    base = f"https://www.churchofjesuschrist.org/study/scriptures/{path_map.get(volume, volume)}/{book}/{chapter}?lang=eng"
    if verses:
        base += f"&id={verses}"
    return base


def slugify(text):
    """Create filesystem-safe slug."""
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)


async def main():
    parser = argparse.ArgumentParser(description='Fetch GC talk content')
    parser.add_argument('speaker', nargs='?', help='Speaker name (e.g., "Elder Jorge T. Becerra")')
    parser.add_argument('title', nargs='?', help='Talk title (e.g., "Tithing—Putting God First")')
    parser.add_argument('conference', nargs='?', help='Conference (e.g., "April 2026")')
    parser.add_argument('--url', help='Direct talk URL')
    parser.add_argument('--output-dir', default='~/Desktop/GC Personal Study', help='Output directory')
    
    args = parser.parse_args()
    
    if not args.url and not (args.speaker and args.title and args.conference):
        parser.error("Provide either --url or speaker + title + conference")
    
    # Import playwright
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Playwright not installed. Run: pip install playwright && playwright install chromium", file=sys.stderr)
        sys.exit(1)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            if args.url:
                await fetch_talk_direct(page, args.url)
            else:
                await fetch_talk_via_search(page, args.speaker, args.title, args.conference)
            
            content = await extract_talk_content(page)
            
            if not content:
                print("Failed to extract talk content", file=sys.stderr)
                sys.exit(1)
            
            # Parse scripture references
            scripture_refs = parse_scripture_refs(content['scriptureLinks'])
            
            # Build output structure
            conference_slug = slugify(args.conference) if args.conference else slugify(page.url)
            talk_slug = slugify(content['title'] or args.title)
            folder_name = f"{conference_slug}_{talk_slug}_{slugify(content['speaker'] or args.speaker)}"
            
            output_dir = Path(args.output_dir).expanduser() / folder_name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Prepare data for template
            data = {
                'title': content['title'],
                'speaker': content['speaker'],
                'conference': args.conference or 'General Conference',
                'date': datetime.now().strftime('%B %d, %Y'),
                'scripture_refs': scripture_refs,
                'hero_image': content['heroImage'],
                'full_text': content['fullText'],
                'source_url': page.url,
                'fetched_at': datetime.now().isoformat()
            }
            
            # Save raw data
            (output_dir / 'talk-data.json').write_text(json.dumps(data, indent=2))
            
            # Save sources.md
            sources_md = f"""# Sources for {content['title']}

## Primary Source
- **Talk**: {content['title']}
- **Speaker**: {content['speaker']}
- **Conference**: {args.conference or 'General Conference'}
- **URL**: {page.url}
- **Accessed**: {datetime.now().strftime('%B %d, %Y')}

## Scripture References
"""
            for ref in scripture_refs:
                sources_md += f"- {ref['text']}: {ref['url']}\n"
            
            (output_dir / 'sources.md').write_text(sources_md)
            
            # Load and populate template
            template_path = Path(__file__).parent / 'templates' / 'personal-reflection-template.html'
            if template_path.exists():
                template = template_path.read_text()
                
                # Replace placeholders
                html = template.replace('[TALK TITLE]', content['title'] or args.title)
                html = html.replace('[SPEAKER]', content['speaker'] or args.speaker)
                html = html.replace('[CONFERENCE]', args.conference or 'General Conference')
                html = html.replace('[DATE]', datetime.now().strftime('%B %d, %Y'))
                
                # Inject scripture references into Lectio prompt
                scripture_list = ', '.join([ref['text'] for ref in scripture_refs])
                html = html.replace('e.g., Malachi 3:10', f'e.g., {scripture_list}' if scripture_list else 'e.g., Malachi 3:10')
                
                (output_dir / 'personal-reflection.html').write_text(html)
                
                # Also create printable version (same but cleaner)
                (output_dir / 'reflection-printable.html').write_text(html)
            
            # Create covenant tracker standalone
            tracker_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Covenant Tracker - """ + (content['title'] or args.title) + """</title>
    <style>
        body { font-family: Georgia, serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background: #1a3c5e; color: white; }
        input[type="range"] { width: 100%; }
        .pulse-list { list-style: none; padding: 0; }
        .pulse-list li { border: 1px solid #ddd; border-radius: 8px; padding: 12px; margin: 8px 0; }
    </style>
</head>
<body>
    <h1>Personal Covenant Tracker</h1>
    <p><em>Talk: """ + (content['title'] or args.title) + """ by """ + (content['speaker'] or args.speaker) + """</em></p>
    
    <h2>Covenant Alignment Grid</h2>
    <table>
        <thead><tr><th>My Covenant</th><th>This Talk's Principle</th><th>Alignment (1–5)</th><th>Action This Week</th></tr></thead>
        <tbody>
            <tr><td>Baptism (take His name)</td><td>Tithing = bearing His name in finances</td><td><input type="range" min="1" max="5" value="3"></td><td><input type="text"></td></tr>
            <tr><td>Sacrament (remember Him)</td><td>"Put God first" = remember Him in budget</td><td><input type="range" min="1" max="5" value="3"></td><td><input type="text"></td></tr>
            <tr><td>Temple (consecration)</td><td>All increase = His</td><td><input type="range" min="1" max="5" value="3"></td><td><input type="text"></td></tr>
            <tr><td>Ministering (love as He loves)</td><td>Fast offerings = love in action</td><td><input type="range" min="1" max="5" value="3"></td><td><input type="text"></td></tr>
        </tbody>
    </table>
    
    <h2>Monthly Covenant Pulse</h2>
    <ul class="pulse-list">
        <li><label><input type="checkbox"> I pay tithing FIRST, not last — Date: <input type="date"></label></li>
        <li><label><input type="checkbox"> Fast offering = sacrifice, not surplus — Date: <input type="date"></label></li>
        <li><label><input type="checkbox"> Taught this to family — Date: <input type="date"></label></li>
        <li><label><input type="checkbox"> Shared testimony of this — Date: <input type="date"></label></li>
        <li><label><input type="checkbox"> Spending aligns with "God first" — Date: <input type="date"></label></li>
    </ul>
</body>
</html>"""
            (output_dir / 'covenant-tracker.html').write_text(tracker_html)
            
            # Create full talk HTML with Gospel Library links
            talk_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{content['title'] or args.title}</title>
    <style>
        body {{ font-family: Georgia, serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.8; }}
        h1 {{ color: #1a3c5e; border-bottom: 2px solid #d4a537; padding-bottom: 10px; }}
        .meta {{ color: #666; font-style: italic; margin-bottom: 30px; }}
        .scripture-link {{ color: #2c5f7c; text-decoration: none; border-bottom: 1px dotted #d4a537; }}
        .scripture-link:hover {{ color: #d4a537; }}
        p {{ margin: 1em 0; }}
    </style>
</head>
<body>
    <h1>{content['title'] or args.title}</h1>
    <p class="meta">by {content['speaker'] or args.speaker} · {args.conference or 'General Conference'}</p>
    <div>{content['fullText'].replace(chr(10), '</p><p>')}</div>
    <hr>
    <h2>Scripture References</h2>
    <ul>
"""
            for ref in scripture_refs:
                talk_html += f'        <li><a class="scripture-link" href="{ref["url"]}" target="_blank">{ref["text"]}</a></li>\n'
            
            talk_html += """    </ul>
</body>
</html>"""
            (output_dir / 'talk-full.html').write_text(talk_html)
            
            print(f"✅ Talk saved to: {output_dir}")
            print(f"   - personal-reflection.html")
            print(f"   - reflection-printable.html")
            print(f"   - talk-full.html")
            print(f"   - covenant-tracker.html")
            print(f"   - sources.md")
            print(f"   - talk-data.json")
            
        finally:
            await browser.close()


if __name__ == '__main__':
    asyncio.run(main())