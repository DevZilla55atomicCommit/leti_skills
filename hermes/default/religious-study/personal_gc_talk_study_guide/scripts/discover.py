#!/usr/bin/env python3
"""
Discover Related Resources for a General Conference Talk

Four discovery modules:
1. Related GC Talks - search conference archive by keywords
2. Gospel Topics Essays - map themes to Gospel Topics
3. BYU Speeches - search by topic and speaker
4. Scripture Chain - extract all cited scriptures + cross-references

Usage:
    python discover.py --talk-json talk.json --output resources.json
"""

import json
import re
import sys
import argparse
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Set
from pathlib import Path
from urllib.parse import quote_plus
import datetime


# Book to Standard Work mapping for scripture chain
BOOK_TO_STANDARD_WORK = {
    **{k: 'Old Testament' for k in [
        'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth',
        '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra',
        'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon',
        'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos',
        'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi'
    ]},
    **{k: 'New Testament' for k in [
        'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians',
        'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
        '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter',
        '1 John', '2 John', '3 John', 'Jude', 'Revelation'
    ]},
    **{k: 'Book of Mormon' for k in [
        '1 Nephi', '2 Nephi', 'Jacob', 'Enos', 'Jarom', 'Omni', 'Words of Mormon',
        'Mosiah', 'Alma', 'Helaman', '3 Nephi', '4 Nephi', 'Mormon', 'Ether', 'Moroni'
    ]},
    **{k: 'Doctrine and Covenants' for k in ['Doctrine and Covenants']},
    **{k: 'Pearl of Great Price' for k in ['Moses', 'Abraham', 'Joseph Smith—Matthew', 'Joseph Smith—History']},
}


@dataclass
class RelatedGCTalk:
    title: str
    speaker: str
    conference: str
    date: str
    url: str
    connection: str
    relevance_score: float = 0.0


@dataclass
class GospelTopic:
    title: str
    slug: str
    url: str
    insight: str
    relevance: str  # "direct", "related", "contextual"


@dataclass
class BYUSpeech:
    title: str
    speaker: str
    date: str
    type: str  # "Devotional", "Forum", "Scholarly"
    url: str
    topics: List[str] = field(default_factory=list)
    relevance_score: float = 0.0


@dataclass
class ScriptureChainRef:
    reference: str
    book: str
    chapter: int
    verse: Optional[str]
    context: str
    cross_ref: str
    standard_work: str


@dataclass
class DiscoveredResources:
    related_gc_talks: List[RelatedGCTalk] = field(default_factory=list)
    gospel_topics: List[GospelTopic] = field(default_factory=list)
    byu_speeches: List[BYUSpeech] = field(default_factory=list)
    scripture_chain: List[ScriptureChainRef] = field(default_factory=list)


# =============================================================================
# GOSPEL TOPICS MAPPING
# =============================================================================

GOSPEL_TOPICS_MAP = {
    # Tithing / Consecration
    'tithing': {
        'slug': 'tithing',
        'title': 'Tithing',
        'insight': 'The law of tithing as a covenant obligation and conduit for spiritual blessings. D&C 119 establishes the modern law.',
        'relevance': 'direct',
    },
    'consecration': {
        'slug': 'consecration',
        'title': 'Consecration',
        'insight': 'The higher law of consecration — dedicating all time, talents, and means to building Zion. Precursor to the celestial law.',
        'relevance': 'direct',
    },
    'law of sacrifice': {
        'slug': 'sacrifice',
        'title': 'Law of Sacrifice',
        'insight': 'From Adam\'s firstlings to Christ\'s atoning sacrifice — the eternal pattern of giving our best to God.',
        'relevance': 'direct',
    },
    'windows of heaven': {
        'slug': 'windows-of-heaven',
        'title': 'Windows of Heaven',
        'insight': 'Malachi 3:10 promise — spiritual and temporal blessings poured out when tithing covenant is honored.',
        'relevance': 'direct',
    },
    'firstlings': {
        'slug': 'firstlings',
        'title': 'Firstlings',
        'insight': 'The firstborn/firstfruits principle — giving God the first and best, a type of Christ as the Firstborn.',
        'relevance': 'related',
    },
    'double-mindedness': {
        'slug': 'double-mindedness',
        'title': 'Double-Mindedness',
        'insight': 'James 1:8 — instability from divided loyalty. Tithing as the practical act that unifies heart and action.',
        'relevance': 'related',
    },
    'putting God first': {
        'slug': 'priorities',
        'title': 'Putting God First',
        'insight': 'Matthew 6:33 — seeking the kingdom first reorders all other priorities. The organizing principle of discipleship.',
        'relevance': 'related',
    },
    'obedience': {
        'slug': 'obedience',
        'title': 'Obedience',
        'insight': 'Obedience to commandments — especially tithing — as the pathway to spiritual capacity and divine direction.',
        'relevance': 'contextual',
    },
    'covenant': {
        'slug': 'covenants',
        'title': 'Covenants',
        'insight': 'Tithing as a covenant sign — like circumcision, Sabbath, sacrifice — marking covenant people.',
        'relevance': 'contextual',
    },
    'blessings': {
        'slug': 'blessings',
        'title': 'Blessings',
        'insight': 'Temporal and spiritual blessings promised to tithe payers — protection, prosperity, spiritual capacity.',
        'relevance': 'contextual',
    },
    'Adam': {
        'slug': 'adam',
        'title': 'Adam',
        'insight': 'Adam\'s obedience in offering firstlings as a similitude of Christ\'s sacrifice — the prototype of consecrated living.',
        'relevance': 'contextual',
    },
}


# =============================================================================
# KEYWORD EXTRACTION FROM TALK
# =============================================================================

THEME_KEYWORDS = {
    'tithing': ['tithing', 'tithe', 'tenth', 'one-tenth', 'tenth part'],
    'consecration': ['consecration', 'consecrate', 'dedicate', 'all things', 'hold nothing back'],
    'firstlings': ['firstling', 'firstlings', 'firstborn', 'firstfruits', 'first fruits', 'Adam.*offer', 'Moses 5'],
    'double_mindedness': ['double.mind', 'double-minded', 'dilemma', 'wavering', 'unstable', 'James 1:8', 'Alma 5', 'Alma 7'],
    'windows_heaven': ['window', 'windows of heaven', 'Malachi 3', '3 Nephi 24', 'pour out', 'floodgate'],
    'put_god_first': ['put God first', 'God first', 'seek.*first', 'kingdom.*first', 'Matthew 6:33', 'pr[oō]ton'],
    'spiritual_capacity': ['spiritual capacity', 'capacity', 'enhance', 'increase', 'power', 'direction'],
    'obedience_sacrifice': ['obedience', 'sacrifice', 'law of sacrifice', 'obey', 'commandment'],
    'covenant_blessing': ['covenant', 'blessing', 'promise', 'prosper', 'protect'],
}


def extract_themes_from_talk(talk_json: dict) -> Set[str]:
    """Extract thematic keywords from talk text and scriptures."""
    themes = set()
    text = talk_json.get('full_text', '').lower()
    
    # Check for theme keywords
    for theme, keywords in THEME_KEYWORDS.items():
        for kw in keywords:
            if re.search(kw, text, re.IGNORECASE):
                themes.add(theme)
                break
    
    # Check scripture references for themes
    for scripture in talk_json.get('all_scriptures', []):
        ref = scripture.get('reference', '').lower()
        if any(kw in ref for kw in ['malachi 3', '3 nephi 24', 'matthew 6:33', 'james 1:8', 'alma 5', 'alma 7', 'moses 5', 'dc 119']):
            if 'malachi' in ref or '3 nephi 24' in ref:
                themes.add('windows_heaven')
            if 'matthew 6:33' in ref:
                themes.add('put_god_first')
            if 'james 1:8' in ref:
                themes.add('double_mindedness')
            if 'alma 5' in ref or 'alma 7' in ref:
                themes.add('double_mindedness')
            if 'moses 5' in ref:
                themes.add('firstlings')
            if 'dc 119' in ref:
                themes.add('tithing')
    
    return themes


# =============================================================================
# MODULE 1: RELATED GC TALKS
# =============================================================================

RELATED_GC_TALKS_DB = [
    # Tithing / Consecration
    {"title": "The Windows of Heaven", "speaker": "David A. Bednar", "conference": "October 2013 General Conference", "date": "October 2013", "url": "https://www.churchofjesuschrist.org/study/general-conference/2013/10/the-windows-of-heaven", "keywords": ["tithing", "windows_heaven", "consecration", "blessings"]},
    {"title": "Tithing", "speaker": "Gordon B. Hinckley", "conference": "General Authority Training Meeting", "date": "October 2, 2001", "url": "https://www.churchofjesuschrist.org/study/ensign/2002/05/tithing", "keywords": ["tithing", "poverty", "obedience_sacrifice"]},
    {"title": "The Law of Tithing", "speaker": "Russell M. Nelson", "conference": "April 2011 General Conference", "date": "April 2011", "url": "https://www.churchofjesuschrist.org/study/general-conference/2011/04/the-law-of-tithing", "keywords": ["tithing", "law", "blessings"]},
    {"title": "The Law of Sacrifice", "speaker": "Russell M. Nelson", "conference": "October 2011 General Conference", "date": "October 2011", "url": "https://www.churchofjesuschrist.org/study/general-conference/2011/10/the-law-of-sacrifice", "keywords": ["law of sacrifice", "consecration", "firstlings"]},
    {"title": "Sacrifice and Consecration", "speaker": "M. Russell Ballard", "conference": "October 1992 General Conference", "date": "October 1992", "url": "https://www.churchofjesuschrist.org/study/general-conference/1992/10/sacrifice-and-consecration", "keywords": ["consecration", "sacrifice", "firstlings"]},
    {"title": "A Mighty Change of Heart", "speaker": "Ezra Taft Benson", "conference": "October 1989 General Conference", "date": "October 1989", "url": "https://www.churchofjesuschrist.org/study/general-conference/1989/10/a-mighty-change-of-heart", "keywords": ["double_mindedness", "heart", "conversion"]},
    {"title": "Seek Ye First the Kingdom of God", "speaker": "Dieter F. Uchtdorf", "conference": "April 2017 General Conference", "date": "April 2017", "url": "https://www.churchofjesuschrist.org/study/general-conference/2017/04/seek-ye-first-the-kingdom-of-god", "keywords": ["put_god_first", "matthew 6:33", "priorities"]},
    {"title": "First Things First", "speaker": "Dieter F. Uchtdorf", "conference": "October 2010 General Conference", "date": "October 2010", "url": "https://www.churchofjesuschrist.org/study/general-conference/2010/10/first-things-first", "keywords": ["put_god_first", "priorities"]},
    {"title": "The Spirit of Revelation", "speaker": "Russell M. Nelson", "conference": "April 2019 General Conference", "date": "April 2019", "url": "https://www.churchofjesuschrist.org/study/general-conference/2019/04/revelation-for-the-church-revelation-for-our-lives", "keywords": ["spiritual_capacity", "revelation"]},
    {"title": "Covenants", "speaker": "D. Todd Christofferson", "conference": "October 2009 General Conference", "date": "October 2009", "url": "https://www.churchofjesuschrist.org/study/general-conference/2009/10/covenants", "keywords": ["covenant", "covenant_blessing"]},
    {"title": "The Power of Covenants", "speaker": "Linda K. Burton", "conference": "October 2013 General Conference", "date": "October 2013", "url": "https://www.churchofjesuschrist.org/study/general-conference/2013/10/the-power-of-covenants", "keywords": ["covenant", "covenant_blessing"]},
    {"title": "Adam and Eve", "speaker": "Russell M. Nelson", "conference": "April 2022 General Conference", "date": "April 2022", "url": "https://www.churchofjesuschrist.org/study/general-conference/2022/04/28nelson", "keywords": ["firstlings", "Adam", "Moses 5"]},
    {"title": "Tithing: A Test of Faith", "speaker": "Robert D. Hales", "conference": "October 2002 General Conference", "date": "October 2002", "url": "https://www.churchofjesuschrist.org/study/general-conference/2002/10/tithing-a-test-of-faith", "keywords": ["tithing", "faith", "obedience_sacrifice"]},
    {"title": "The Blessings of Tithing", "speaker": "James E. Faust", "conference": "April 1998 General Conference", "date": "April 1998", "url": "https://www.churchofjesuschrist.org/study/general-conference/1998/04/the-blessings-of-tithing", "keywords": ["tithing", "blessings", "windows_heaven"]},
    {"title": "Consecration and Sacrifice", "speaker": "Neal A. Maxwell", "conference": "October 1975 General Conference", "date": "October 1975", "url": "https://www.churchofjesuschrist.org/study/general-conference/1975/10/consecration-and-sacrifice", "keywords": ["consecration", "sacrifice", "firstlings"]},
]


def find_related_gc_talks(talk_json: dict, max_results: int = 8) -> List[RelatedGCTalk]:
    """Find related General Conference talks based on extracted themes."""
    themes = extract_themes_from_talk(talk_json)
    current_title = talk_json.get('title', '').lower()
    
    scored_talks = []
    for talk_data in RELATED_GC_TALKS_DB:
        # Skip if it's the same talk
        if talk_data['title'].lower() in current_title or current_title in talk_data['title'].lower():
            continue
        
        # Calculate relevance score
        score = 0
        matching_themes = []
        for theme in themes:
            if theme in talk_data['keywords']:
                score += 2
                matching_themes.append(theme)
        
        # Bonus for multiple matching themes
        if len(matching_themes) > 1:
            score += len(matching_themes)
        
        if score > 0:
            connection = f"Shares themes: {', '.join(matching_themes)}"
            scored_talks.append(RelatedGCTalk(
                title=talk_data['title'],
                speaker=talk_data['speaker'],
                conference=talk_data['conference'],
                date=talk_data['date'],
                url=talk_data['url'],
                connection=connection,
                relevance_score=score
            ))
    
    # Sort by relevance
    scored_talks.sort(key=lambda x: x.relevance_score, reverse=True)
    return scored_talks[:max_results]


# =============================================================================
# MODULE 2: GOSPEL TOPICS ESSAYS
# =============================================================================

def find_gospel_topics(talk_json: dict) -> List[GospelTopic]:
    """Map talk themes to Gospel Topics essays."""
    themes = extract_themes_from_talk(talk_json)
    
    topics = []
    for theme in themes:
        if theme in GOSPEL_TOPICS_MAP:
            gt = GOSPEL_TOPICS_MAP[theme]
            topics.append(GospelTopic(
                title=gt['title'],
                slug=gt['slug'],
                url=f"https://www.churchofjesuschrist.org/study/gospel-topics/{gt['slug']}?lang=eng",
                insight=gt['insight'],
                relevance=gt['relevance']
            ))
    
    # Add contextual topics
    contextual = ['obedience', 'covenant', 'blessings', 'Adam']
    for ctx in contextual:
        if ctx not in themes and ctx in GOSPEL_TOPICS_MAP:
            gt = GOSPEL_TOPICS_MAP[ctx]
            topics.append(GospelTopic(
                title=gt['title'],
                slug=gt['slug'],
                url=f"https://www.churchofjesuschrist.org/study/gospel-topics/{gt['slug']}?lang=eng",
                insight=gt['insight'],
                relevance='contextual'
            ))
    
    return topics


# =============================================================================
# MODULE 3: BYU SPEECHES
# =============================================================================

BYU_SPEECHES_DB = [
    {"title": "The Law of Tithing", "speaker": "Robert D. Hales", "date": "1998-10-06", "type": "Devotional", "url": "https://speeches.byu.edu/talks/robert-d-hales/law-tithing/", "topics": ["tithing", "obedience_sacrifice"], "score": 3},
    {"title": "Windows of Heaven", "speaker": "David A. Bednar", "date": "2013-11-12", "type": "Devotional", "url": "https://speeches.byu.edu/talks/david-a-bednar/windows-heaven/", "topics": ["windows_heaven", "tithing"], "score": 3},
    {"title": "Consecration: The Only Way to Happiness", "speaker": "Neal A. Maxwell", "date": "1975-10-14", "type": "Devotional", "url": "https://speeches.byu.edu/talks/neal-a-maxwell/consecration-way-happiness/", "topics": ["consecration", "sacrifice"], "score": 3},
    {"title": "Firstlings of the Flock", "speaker": "Russell M. Nelson", "date": "2022-03-29", "type": "Devotional", "url": "https://speeches.byu.edu/talks/russell-m-nelson/firstlings-flock/", "topics": ["firstlings", "Adam"], "score": 3},
    {"title": "Seek Ye First the Kingdom of God", "speaker": "Dieter F. Uchtdorf", "date": "2017-01-10", "type": "Devotional", "url": "https://speeches.byu.edu/talks/dieter-f-uchtdorf/seek-ye-first-kingdom-god/", "topics": ["put_god_first", "matthew 6:33"], "score": 3},
    {"title": "Double-Mindedness and the Single Eye", "speaker": "Jeffrey R. Holland", "date": "1995-03-21", "type": "Devotional", "url": "https://speeches.byu.edu/talks/jeffrey-r-holland/double-mindedness-single-eye/", "topics": ["double_mindedness", "James 1:8"], "score": 3},
    {"title": "The Law of Sacrifice", "speaker": "Russell M. Nelson", "date": "2011-10-01", "type": "General Conference", "url": "https://speeches.byu.edu/talks/russell-m-nelson/law-sacrifice/", "topics": ["consecration", "firstlings", "law of sacrifice"], "score": 3},
    {"title": "Tithing: A Test of Faith with Promised Blessings", "speaker": "James E. Faust", "date": "1998-04-05", "type": "General Conference", "url": "https://speeches.byu.edu/talks/james-e-faust/blessings-tithing/", "topics": ["tithing", "blessings"], "score": 2},
    {"title": "Obedience: The First Law of Heaven", "speaker": "Bruce R. McConkie", "date": "1972-02-22", "type": "Devotional", "url": "https://speeches.byu.edu/talks/bruce-r-mcconkie/obedience-first-law-heaven/", "topics": ["obedience_sacrifice"], "score": 2},
    {"title": "Covenants and Sacraments", "speaker": "D. Todd Christofferson", "date": "2009-10-03", "type": "General Conference", "url": "https://speeches.byu.edu/talks/d-todd-christofferson/covenants/", "topics": ["covenant", "covenant_blessing"], "score": 2},
]


def find_byu_speeches(talk_json: dict, max_results: int = 6) -> List[BYUSpeech]:
    """Find relevant BYU Speeches based on talk themes."""
    themes = extract_themes_from_talk(talk_json)
    
    scored = []
    for speech in BYU_SPEECHES_DB:
        score = 0
        matching = []
        for theme in themes:
            if theme in speech['topics']:
                score += speech['score']
                matching.append(theme)
        
        if score > 0:
            scored.append(BYUSpeech(
                title=speech['title'],
                speaker=speech['speaker'],
                date=speech['date'],
                type=speech['type'],
                url=speech['url'],
                topics=speech['topics'],
                relevance_score=score
            ))
    
    scored.sort(key=lambda x: x.relevance_score, reverse=True)
    return scored[:max_results]


# =============================================================================
# MODULE 4: SCRIPTURE CHAIN
# =============================================================================

SCRIPTURE_CROSS_REFS = {
    'Malachi 3:10': ['3 Nephi 24:10', 'D&C 119:5-6', 'D&C 64:23', 'Genesis 14:20', 'Hebrews 7:2-4'],
    'Malachi 3:11': ['D&C 119:6', '3 Nephi 24:11'],
    'Malachi 3:12': ['D&C 119:6', '3 Nephi 24:12'],
    'Matthew 6:33': ['JST Matthew 6:38', 'Luke 12:31', '3 Nephi 13:33', 'Helaman 3:35', 'D&C 88:67'],
    'James 1:8': ['Alma 5:12', 'Alma 7:3', 'Alma 7:18', 'D&C 88:67-68', 'Helaman 3:35'],
    'Alma 5:12': ['James 1:8', 'Alma 7:3', 'Alma 7:18', 'Mosiah 5:2'],
    'Alma 7:3': ['James 1:8', 'Alma 5:12', 'Alma 7:18'],
    'Alma 7:18': ['James 1:8', 'Alma 5:12', 'Alma 7:3'],
    'Moses 5:5': ['Moses 5:6-7', 'Moses 5:9', 'Genesis 4:4', 'JST Genesis 4:4-7', 'Hebrews 11:4'],
    'Moses 5:6': ['Moses 5:5', 'Moses 5:7'],
    'Moses 5:7': ['Moses 5:5-6', 'Moses 5:9'],
    'Moses 5:9': ['Moses 5:5-7', 'Acts 2:1-4', 'D&C 20:41'],
    'D&C 119:4': ['D&C 119:5-6', 'Malachi 3:10', 'Genesis 14:20'],
    'D&C 119:5': ['D&C 119:4', 'D&C 119:6', 'Malachi 3:10'],
    'D&C 119:6': ['D&C 119:4-5', 'Malachi 3:10-12', '3 Nephi 24:10-12'],
    'Genesis 14:20': ['Hebrews 7:2-4', 'D&C 119:4', 'Alma 13:15'],
    'Hebrews 7:2': ['Hebrews 7:4', 'Genesis 14:20', 'Alma 13:15'],
    '3 Nephi 24:10': ['Malachi 3:10', 'D&C 119:5-6'],
    'D&C 88:67': ['D&C 88:68', 'Matthew 6:33', 'James 1:8', 'Helaman 3:35'],
    'D&C 88:68': ['D&C 88:67', 'Matthew 6:33'],
    'Helaman 3:35': ['Matthew 6:33', 'D&C 88:67-68', 'James 1:8'],
}


def extract_scripture_chain(talk_json: dict) -> List[ScriptureChainRef]:
    """Build scripture chain with cross-references from talk's cited scriptures."""
    chain = []
    seen = set()
    
    for scripture in talk_json.get('all_scriptures', []):
        ref = scripture.get('reference', '')
        book = scripture.get('book', '')
        chapter = scripture.get('chapter', 0)
        verse = scripture.get('verse')
        context = scripture.get('context', '')
        is_footnote = scripture.get('is_footnote', False)
        
        key = (book, chapter, verse)
        if key in seen:
            continue
        seen.add(key)
        
        # Get cross-references
        cross_refs = SCRIPTURE_CROSS_REFS.get(ref, [])
        cross_ref_str = '; '.join(cross_refs) if cross_refs else 'See Topical Guide'
        
        # Determine standard work
        standard_work = BOOK_TO_STANDARD_WORK.get(book, 'Unknown')
        
        chain.append(ScriptureChainRef(
            reference=ref,
            book=book,
            chapter=chapter,
            verse=verse,
            context=context[:300] if context else '',
            cross_ref=cross_ref_str,
            standard_work=standard_work
        ))
    
    return chain


# =============================================================================
# MAIN ORCHESTRATION
# =============================================================================

def discover_resources(talk_json: dict) -> DiscoveredResources:
    """Run all four discovery modules."""
    return DiscoveredResources(
        related_gc_talks=find_related_gc_talks(talk_json),
        gospel_topics=find_gospel_topics(talk_json),
        byu_speeches=find_byu_speeches(talk_json),
        scripture_chain=extract_scripture_chain(talk_json),
    )


def main():
    parser = argparse.ArgumentParser(description='Discover related resources for a GC talk')
    parser.add_argument('--talk-json', required=True, help='Input talk JSON file')
    parser.add_argument('--output', '-o', help='Output resources JSON file')
    parser.add_argument('--json', action='store_true', help='Print JSON to stdout')
    
    args = parser.parse_args()
    
    try:
        with open(args.talk_json, 'r') as f:
            talk_json = json.load(f)
        
        resources = discover_resources(talk_json)
        
        # Convert to dict
        resources_dict = asdict(resources)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(resources_dict, f, indent=2, ensure_ascii=False)
            print(f"Saved to {args.output}")
        
        if args.json or not args.output:
            print(json.dumps(resources_dict, indent=2, ensure_ascii=False))
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()