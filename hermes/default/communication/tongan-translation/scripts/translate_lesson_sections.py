#!/usr/bin/env python3
"""
Quick translate key sections for Tongan Come Follow Me lesson.
Uses a simpler approach with pre-extracted text.
"""

import json
import re
import sys
from pathlib import Path

# Add the skill scripts to path
SKILL_DIR = Path.home() / ".hermes" / "skills" / "communication" / "tongan-translation"
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from translate_with_pack import translate


def translate_text(text):
    """Translate a single text segment."""
    clean_text = re.sub(r'\s+', ' ', text.strip())
    
    if len(re.sub(r'[^a-zA-Z]', '', clean_text)) < 3:
        return {'tongan': text, 'escalated': False, 'skipped': True}
    
    result = translate(clean_text)
    
    if 'error' in result:
        return {'tongan': text, 'escalated': False, 'error': result['error']}
    
    if result.get('escalate', False):
        return {
            'tongan': text,
            'escalated': True,
            'escalate_reason': result.get('escalate_reason', 'Unknown'),
        }
    
    return {
        'tongan': result.get('tongan', text),
        'escalated': False,
        'frame': result.get('frame'),
        'confidence': result.get('confidence'),
    }


def main():
    """Translate key sections from the Psalms lesson."""
    
    # Key sections to translate
    sections = {
        'title': 'Come, Follow Me',
        'subtitle1': 'The Lord Is My Shepherd',
        'subtitle2': 'Psalms 1–2; 8; 19–33; 40; 46',
        'subtitle3': 'August 17–23, 2026 • Old Testament 2026',
        'section1': 'The Psalms in Three Sentences',
        'key1': 'The Psalms are Israel\'s hymnbook — 150 prayers, praises, and laments that Jesus Himself quoted more than any other Old Testament book.',
        'key2': 'This week\'s selection forms a thematic arc: the two ways → creation\'s witness → Messianic prophecy → the Good Shepherd → temple access → God as refuge.',
        'key3': 'The Psalms teach us to bring our whole selves to God — joy, grief, anger, doubt, trust — and find that He is our Shepherd, Rock, Fortress, and Refuge in every season.',
        'core_msg': 'The Psalms are a playlist for every season of life. They give us words when we have none — words of praise, lament, trust, and hope. "The Lord is my shepherd; I shall not want."',
        'q1': 'What invitations to trust the Lord do you find in Psalms 1; 23; 26–28; 46?',
        'a1': 'Key invitations: Psalm 1: Delight in God\'s law, be like a tree planted by waters. Psalm 23: The Lord is my shepherd, green pastures, still waters, restored soul. Psalm 26: Examine me O Lord, walk in integrity. Psalm 27: The Lord is my light and salvation, wait on the Lord. Psalm 28: Unto thee will I cry, He hears, He helps. Psalm 46: God is our refuge and strength, be still and know He is God.',
        'q2': 'What words describe God, and what words describe the peace and strength He provides?',
        'a2': 'Words for God: Shepherd, Light, Salvation, Rock, Fortress, Deliverer, Refuge, Strength, King, Judge, Creator. Words for His blessings: green pastures, still waters, restored soul, paths of righteousness, rod and staff comfort, table prepared, anointed head, overflowing cup, goodness and mercy following, dwelling in His house forever.',
        'q3': 'What words describe people who trust Him?',
        'a3': 'Blessed. Planted by waters, fruitful, leaf never withers. Walk in integrity. Wait on the Lord, courageous. Cry unto Him, lifted up. Still, knowing He is God.',
        'q4': 'Psalm 23 imagery — green pastures, still waters, rod and staff, cup runs over — what do they mean?',
        'a4': 'Green pastures and still waters: spiritual nourishment, peace, rest from anxiety. Paths of righteousness: guidance toward right choices. Rod and staff: rod protects against predators; staff guides with gentle correction. Table before enemies: divine provision in opposition. Anointed head and overflowing cup: consecration, abundance. Goodness and mercy follow: Hebrew radaph means pursue/chase — God\'s love actively hunts us down.',
        'cheat1': 'What is Psalm 1 about? Two ways: righteous (tree by water) vs wicked (chaff).',
        'cheat2': 'Psalm 2 = ? Messianic: God\'s Anointed King; nations rage but He reigns.',
        'cheat3': 'Psalm 8 main point? Creation declares God\'s glory; He\'s mindful of us.',
        'cheat4': 'Psalm 19 = ? Two books: Creation (v.1–6) + Law/Word (v.7–11). Both declare glory.',
        'cheat5': 'Psalm 22 = ? Cross prophecy: forsaken, pierced, garments divided, It is finished.',
        'cheat6': 'Psalm 23 = ? Shepherd: provides, guides, protects, restores, anoints, pursues with mercy.',
        'cheat7': 'Rod vs Staff? Rod = protection (club); Staff = guidance (crook to rescue).',
        'cheat8': 'Psalm 24 = ? Ascend hill of Lord = temple; clean hands + pure heart = worthiness.',
        'cheat9': 'Psalm 33 = ? Creation by His word; He fashions hearts; trust Him not horses.',
        'cheat10': 'Psalm 40 = ? Waited patiently → new song; I delight to do Thy will.',
        'cheat11': 'Psalm 46 = ? God = refuge/strength; Be still and know I am God; chaos can\'t shake Him.',
        'cheat12': 'Jesus quoted Psalms? More than any OT book! Cross: Ps 22:1; 31:5. Last Supper: Ps 113–118 (Hallel).',
    }
    
    results = {}
    total = len(sections)
    
    for i, (key, text) in enumerate(sections.items(), 1):
        print(f"[{i}/{total}] {key}...")
        result = translate_text(text)
        results[key] = result
        
        if result.get('escalated'):
            print(f"  ⚠ ESCALATED: {result.get('escalate_reason', 'Unknown')}")
        elif result.get('skipped'):
            print(f"  ⏭ SKIPPED")
        else:
            print(f"  ✓ {result.get('tongan', '')[:80]}")
    
    # Save results
    output = {
        'source': 'Psalms_Lesson_Final.html (Come Follow Me Aug 17-23, 2026)',
        'translated_sections': results,
        'summary': {
            'total': total,
            'translated': sum(1 for r in results.values() if not r.get('escalated') and not r.get('skipped') and 'tongan' in r),
            'escalated': sum(1 for r in results.values() if r.get('escalated')),
            'skipped': sum(1 for r in results.values() if r.get('skipped')),
        }
    }
    
    with open('tongan_translations.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved to tongan_translations.json")
    print(f"Translated: {output['summary']['translated']}, Escalated: {output['summary']['escalated']}, Skipped: {output['summary']['skipped']}")


if __name__ == '__main__':
    main()