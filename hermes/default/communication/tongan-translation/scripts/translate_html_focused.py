#!/usr/bin/env python3
"""
Translate key sections of the Come Follow Me HTML lesson to Tongan.
Focuses on main content: questions, answers, key points, cheat sheet.
"""

import json
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

# Add the skill scripts to path
SKILL_DIR = Path.home() / ".hermes" / "skills" / "communication" / "tongan-translation"
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from translate_with_pack import translate


def translate_text(text):
    """Translate a single text segment, handling escalation."""
    # Clean the text for translation
    clean_text = re.sub(r'\s+', ' ', text.strip())
    
    # Skip if it's mostly numbers/punctuation
    if len(re.sub(r'[^a-zA-Z]', '', clean_text)) < 3:
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
    """Translate HTML file to Tongan - focused on main content."""
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
        result = translate_text(title_tag.string)
        if not result.get('escalate') and 'tongan' in result:
            title_tag.string = result['tongan']
        else:
            title_tag.string = f"[ESCALATED] {title_tag.string}"
    
    # Translate main content areas
    translated = 0
    escalated = 0
    
    # 1. Translate h1, h2, h3 headings
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4']):
        text = heading.get_text(strip=True)
        if text:
            print(f"  Translating heading: {text[:60]}...")
            result = translate_text(text)
            if result.get('escalated'):
                escalated += 1
                heading.string = f"[ESCALATED] {text}"
            elif 'tongan' in result and result['tongan'] != text:
                translated += 1
                heading.string = result['tongan']
    
    # 2. Translate key-point divs
    for kp in soup.find_all('div', class_='key-point'):
        text = kp.get_text(strip=True)
        if text:
            print(f"  Translating key-point: {text[:60]}...")
            result = translate_text(text)
            if result.get('escalated'):
                escalated += 1
                # Replace content but keep strong tags
                kp.clear()
                kp.append(f"[ESCALATED] {text}")
            elif 'tongan' in result and result['tongan'] != text:
                translated += 1
                kp.clear()
                kp.append(result['tongan'])
    
    # 3. Translate question-box content (questions and answers)
    for qb in soup.find_all('div', class_='question-box'):
        # Question text
        q_text_elem = qb.find('div', class_='question-text')
        if q_text_elem:
            text = q_text_elem.get_text(strip=True)
            if text:
                print(f"  Translating question: {text[:60]}...")
                result = translate_text(text)
                if result.get('escalated'):
                    escalated += 1
                    q_text_elem.string = f"[ESCALATED] {text}"
                elif 'tongan' in result and result['tongan'] != text:
                    translated += 1
                    q_text_elem.string = result['tongan']
        
        # Answer text
        a_text_elem = qb.find('div', class_='answer-text')
        if a_text_elem:
            text = a_text_elem.get_text(strip=True)
            if text:
                print(f"  Translating answer: {text[:60]}...")
                result = translate_text(text)
                if result.get('escalated'):
                    escalated += 1
                    a_text_elem.clear()
                    a_text_elem.append(f"[ESCALATED] {text}")
                elif 'tongan' in result and result['tongan'] != text:
                    translated += 1
                    a_text_elem.clear()
                    a_text_elem.append(result['tongan'])
    
    # 4. Translate podcast-insight content
    for pi in soup.find_all('div', class_='podcast-insight'):
        text = pi.get_text(strip=True)
        if text and len(text) > 50:
            print(f"  Translating podcast insight...")
            result = translate_text(text[:500])  # Limit length
            if result.get('escalated'):
                escalated += 1
            elif 'tongan' in result and result['tongan'] != text[:500]:
                translated += 1
                pi.clear()
                pi.append(result['tongan'] + "...")
    
    # 5. Translate takeaway-box
    for tb in soup.find_all('div', class_='takeaway-box'):
        text = tb.get_text(strip=True)
        if text:
            print(f"  Translating takeaway...")
            result = translate_text(text[:500])
            if result.get('escalated'):
                escalated += 1
            elif 'tongan' in result and result['tongan'] != text[:500]:
                translated += 1
                tb.clear()
                tb.append(result['tongan'])
    
    # 6. Translate cheat-sheet cards
    for card in soup.find_all('div', class_='cheat-card'):
        text = card.get_text(strip=True)
        if text and len(text) > 10:
            print(f"  Translating cheat card...")
            result = translate_text(text)
            if result.get('escalated'):
                escalated += 1
            elif 'tongan' in result and result['tongan'] != text:
                translated += 1
                card.clear()
                card.append(result['tongan'])
    
    # 7. Translate table cells (td, th) - simple content only
    for cell in soup.find_all(['td', 'th']):
        text = cell.get_text(strip=True)
        if text and len(text) > 3 and len(text) < 200:
            # Skip if it's mostly scripture references
            if not re.search(r'^\d+:\d+', text) and 'Psalm' not in text and 'Matthew' not in text and 'Acts' not in text:
                print(f"  Translating table cell: {text[:60]}...")
                result = translate_text(text)
                if result.get('escalated'):
                    escalated += 1
                elif 'tongan' in result and result['tongan'] != text:
                    translated += 1
                    cell.clear()
                    cell.append(result['tongan'])
    
    print(f"\nTranslated: {translated}, Escalated: {escalated}")
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
    
    print(f"Saved to {output_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python translate_html_focused.py <input.html> <output.html>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    create_tongan_html(input_path, output_path)


if __name__ == '__main__':
    main()