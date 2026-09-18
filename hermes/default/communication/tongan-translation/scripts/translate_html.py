#!/usr/bin/env python3
"""
Translate the Come Follow Me HTML lesson to Tongan using the Lea Faka-Tonga pack.
Handles escalation by keeping English with [ESCALATED] marker.
"""

import json
import re
import sys
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

# Add the skill scripts to path
SKILL_DIR = Path.home() / ".hermes" / "skills" / "communication" / "tongan-translation"
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from translate_with_pack import translate


def extract_translatable_text(soup):
    """Extract text nodes that should be translated, with their context."""
    texts = []
    
    # Elements to skip entirely
    skip_tags = {'script', 'style', 'code', 'pre', 'img', 'svg', 'path', 'meta', 'link'}
    
    # Only translate these tags (main content)
    translate_tags = {'h1', 'h2', 'h3', 'h4', 'p', 'li', 'td', 'th', 'div', 'span', 'strong', 'em', 'blockquote', 'q'}
    
    for element in soup.find_all(True):
        if element.name in skip_tags:
            continue
        
        # Skip if element has no text content or only whitespace
        if not element.get_text(strip=True):
            continue
        
        # Skip purely decorative elements (class-based)
        if element.get('class'):
            classes = ' '.join(element.get('class'))
            if any(x in classes for x in ['hero', 'footer', 'section-divider', 'page-break', 'subtitle', 'resource-tag', 'cheat-scripture']):
                continue
        
        # Get direct text nodes
        for text_node in element.find_all(string=True, recursive=False):
            text = text_node.strip()
            if text and len(text) > 3:
                # Check if parent is a text-containing element we should translate
                parent = text_node.parent
                if parent and parent.name not in skip_tags:
                    # Check if this is a meaningful text segment
                    if parent.name in translate_tags or parent.name in ['body']:
                        texts.append({
                            'element': parent,
                            'text_node': text_node,
                            'text': text,
                            'original_html': str(parent)
                        })
    
    return texts


def translate_text(text):
    """Translate a single text segment, handling escalation."""
    # Clean the text for translation
    # Remove extra whitespace
    clean_text = re.sub(r'\s+', ' ', text.strip())
    
    # Skip if it's mostly numbers/punctuation
    if len(re.sub(r'[^a-zA-Z]', '', clean_text)) < 3:
        return {'tongan': text, 'escalated': False, 'skipped': True}
    
    # Skip common UI/navigation text
    skip_patterns = [
        r'^(◆|◇|—|–|•|★|☆|●|○|■|□|▶|▷|◆|◇|★)$',
        r'^(August|January|February|March|April|May|June|July|September|October|November|December)\s+\d+',
        r'^\d+[–-]\d+',  # Date ranges
        r'^[A-Z][a-z]+ \d{4}$',  # Month Year
        r'^Psalms?\s+[\d\s;–-]+$',
        r'^(Old|New)\s+Testament\s+\d{4}$',
        r'^(📖|🎧|📚|✨|◆|◇|—)',
    ]
    
    for pattern in skip_patterns:
        if re.search(pattern, clean_text, re.IGNORECASE):
            return {'tongan': text, 'escalated': False, 'skipped': True}
    
    result = translate(clean_text)
    
    if 'error' in result:
        return {'tongan': text, 'escalated': False, 'error': result['error']}
    
    if result.get('escalate', False):
        return {
            'tongan': text,  # Keep English
            'escalated': True,
            'escalate_reason': result.get('escalate_reason', 'Unknown'),
            'original_english': text
        }
    
    return {
        'tongan': result.get('tongan', text),
        'escalated': False,
        'frame': result.get('frame'),
        'confidence': result.get('confidence'),
        'notes': result.get('notes')
    }


def create_tongan_html(input_path, output_path):
    """Translate HTML file to Tongan."""
    print(f"Reading {input_path}...")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Update lang attribute
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = 'to'
    
    # Update title
    title_tag = soup.find('title')
    if title_tag:
        result = translate(title_tag.string)
        if not result.get('escalate') and 'tongan' in result:
            title_tag.string = result['tongan']
        else:
            title_tag.string = f"[ESCALATED] {title_tag.string}"
    
    # Extract all translatable text
    texts = extract_translatable_text(soup)
    print(f"Found {len(texts)} text segments to translate")
    
    # Translate each segment
    translated_count = 0
    escalated_count = 0
    
    for i, item in enumerate(texts):
        text = item['text']
        if not text or len(text) < 3:
            continue
        
        # Skip certain patterns that shouldn't be translated
        if re.match(r'^[\d\s\.\,\:\;\-\(\)]+$', text):  # Only numbers/punctuation
            continue
        if text.startswith('http') or '@' in text:  # URLs/emails
            continue
        if text.lower() in ['and', 'or', 'the', 'a', 'an', 'to', 'of', 'in', 'for', 'with', 'by']:
            continue
        
        print(f"  [{i+1}/{len(texts)}] Translating: {text[:80]}...")
        result = translate_text(text)
        
        if result.get('skipped'):
            continue
        
        if result.get('escalated'):
            escalated_count += 1
            # Replace with English + marker
            new_text = f"[ESCALATED] {text}"
            item['text_node'].replace_with(new_text)
        elif 'tongan' in result and result['tongan'] != text:
            translated_count += 1
            item['text_node'].replace_with(result['tongan'])
        
        # Small delay to not overwhelm the model
        if i % 5 == 0 and i > 0:
            import time
            time.sleep(1)
    
    print(f"\nTranslated: {translated_count}, Escalated: {escalated_count}")
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
    
    print(f"Saved to {output_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python translate_html.py <input.html> <output.html>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    create_tongan_html(input_path, output_path)


if __name__ == '__main__':
    main()