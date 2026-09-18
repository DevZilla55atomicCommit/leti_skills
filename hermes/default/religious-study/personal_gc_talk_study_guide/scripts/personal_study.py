#!/usr/bin/env python3
"""
Personal GC Talk Study Guide — CLI Pipeline

Full pipeline: fetch → discover → render → inject → export

Usage:
    python -m personal_gc_talk_study build \
        --talk-url "https://www.churchofjesuschrist.org/study/general-conference/2026/04/18becerra?lang=eng" \
        --output-dir "~/Desktop/Elders Quorum Lessons 2025.2026/2026/04/Personal Study" \
        --export-pdf
"""

import json
import sys
import subprocess
import shutil
import argparse
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Optional
import tempfile

# Add scripts to path
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

# Import from existing scripts
from fetch_gc_talk import fetch_gc_talk, GCTalk
from discover import discover_resources, DiscoveredResources
from inject_links import inject_links, DEFAULT_SCRIPTURE_REFS, make_gospel_library_url


# Hero image for tithing/firstlings talks
HERO_IMAGE_URL = "https://www.churchofjesuschrist.org/imgs/https%3A%2F%2Fwww.churchofjesuschrist.org%2Fimgs%2Fvhim4s8mgfwn4545eb0ocmrzqypgqr4diifdgxvz%2Ffull%2F%2521768%252C%2F0%2Fdefault/full/!250,/0/default"


def slugify(text: str) -> str:
    """Create a URL-safe slug from text."""
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')


def load_helios_data() -> dict:
    """Load Helios' doctrinal thread data for Becerra talk."""
    helios_skill = Path("/Users/alfredkamisese/.hermes/profiles/helios/skills/religious-study/personal_gc_talk_study_guide/SKILL.md")
    # Since the skill has the data embedded, we'll use it directly
    return {
        "threads": [
            {
                "id": "tithing_law",
                "hue": "#1A3C5E",
                "label": "Tithing Law",
                "qa_pairs": [
                    {
                        "q": "What is the legal/covenantal basis for tithing in this dispensation?",
                        "a": "Doctrine and Covenants 119 — revealed July 8, 1838, in answer to Joseph Smith's prayer: 'O Lord, show unto thy servants how much thou requirest of the properties of thy people for a tithing?' The Lord answered: all surplus property first, then one-tenth of interest annually — 'a standing law unto them forever' (D&C 119:4).",
                        "citations": ["D&C 119:1-7", "D&C 120 (Council on Disposition of Tithes)"]
                    },
                    {
                        "q": "Does tithing replace the law of consecration?",
                        "a": "No. Section 119 restates consecration (D&C 42:33, 54) and defines surplus as one-tenth. It is 'the beginning of the tithing of my people' (D&C 119:1) — implementation, not replacement. President Hinckley: 'the law of sacrifice and the law of consecration were not done away with and are still in effect.'",
                        "citations": ["D&C 119:1-4", "D&C 42:30-39", "D&C 104:4-9 (United Firm != law of consecration)"]
                    },
                    {
                        "q": "What does Malachi 3 teach about the tithing covenant?",
                        "a": "Post-exilic context: temple rebuilt but hearts cold. 'Return unto me, and I will return unto you' (v. 7). Tithing is the diagnostic — 'Will a man rob God?' (v. 8). The promise: windows opened, devourer rebuked, all nations call you blessed (vv. 10-12).",
                        "citations": ["Malachi 3:7-12", "3 Nephi 24:7-12 (Nephite repetition)"]
                    },
                    {
                        "q": "What is the 'Council on the Disposition of the Tithes' and why does it matter?",
                        "a": "D&C 120: First Presidency, Quorum of Twelve, Presiding Bishopric authorize expenditure. Reestablished 1943 after 1838 revelation. Demonstrates living revelation — tithes are sacred, disposition is revelatory, not bureaucratic.",
                        "citations": ["D&C 120:1-3", "BYU Studies: 'The Development of the Council on the Disposition of the Tithes'"]
                    }
                ],
                "cross_refs": [
                    "D&C 119 (full section)", "D&C 120 (full section)",
                    "Malachi 3:7-12", "3 Nephi 24:7-12",
                    "D&C 64:23-24 (tithing and the poor)", "D&C 85:3 (tithing and inheritance in Zion)"
                ]
            },
            {
                "id": "firstlings_adam",
                "hue": "#D4A537",
                "label": "Firstlings / Adam's Offering",
                "qa_pairs": [
                    {
                        "q": "What did Adam offer and why does it matter?",
                        "a": "Moses 5:5 — 'Adam was obedient... I know not, save the Lord commanded me.' He offered firstlings of the flock. The angel explained: 'This thing is a similitude of the sacrifice of the Only Begotten of the Father, which is full of grace and truth' (Moses 5:7). Obedience *precedes* understanding.",
                        "citations": ["Moses 5:5-7", "Abraham 3:25 (premortal test of obedience)"]
                    },
                    {
                        "q": "What does 'firstlings' (bekorah) mean in Hebrew?",
                        "a": "bekorah = firstborn, birthright, preeminence, priority. Not '10%' — the **first, the best, the representative whole**. The firstling *stands for* the entire flock. Tithing restores this pattern when stewardship-based consecration isn't institutionally administered.",
                        "citations": ["Genesis 4:4 (Abel's firstlings)", "Exodus 13:2, 12-13 (firstborn consecrated)", "Colossians 1:15 (Christ as Firstborn of creation)"]
                    },
                    {
                        "q": "How does the firstling pattern connect to Christ?",
                        "a": "Typological arc: Abel's accepted offering (Heb 11:4) -> Firstborn consecrated in Egypt (Ex 13) -> Christ as 'Firstborn among many brethren' (Rom 8:29) -> 'Firstborn of every creature' (Col 1:15) -> We offer our 'firstlings' (time, talent, treasure) as participation in His consecration.",
                        "citations": ["Hebrews 11:4", "Romans 8:29", "Colossians 1:15-18", "D&C 93:21 (Christ as Firstborn)"]
                    },
                    {
                        "q": "What do the Nauvoo 1842 consecration affidavits reveal?",
                        "a": "20 handwritten affidavits (June-July 1842) prove consecration was actively taught and practiced in Nauvoo — *after* the supposed 'replacement' by tithing. The 'higher law/lower law' folk memory is historically false. Consecration = celestial law; tithing = standing implementation.",
                        "citations": ["BYU Studies: 'Myself... I Consecrate to the God of Heaven' (20 affidavits)", "D&C 119:1 (tithing = 'beginning' of consecration)"]
                    }
                ],
                "cross_refs": [
                    "Moses 5:5-7 (full passage)", "Genesis 4:1-8 (Cain and Abel)",
                    "Exodus 13:1-16 (firstborn law)", "Leviticus 27:26-27 (firstlings holy to Lord)",
                    "Hebrews 11:4", "Romans 8:28-30", "Colossians 1:15-20",
                    "D&C 93:21-22", "BYU Studies: Nauvoo affidavits article"
                ]
            },
            {
                "id": "double_mindedness",
                "hue": "#8B6914",
                "label": "Double-Mindedness",
                "qa_pairs": [
                    {
                        "q": "What does 'double-minded' mean in James 1:8?",
                        "a": "dipsychos = two-souled, divided loyalty. 'A double minded man is unstable in all his ways' (akatastatos = unstable, inconstant, restless). Context: asking God for wisdom *in faith, nothing wavering* (James 1:5-6). The double mind cannot receive because it's tuned to two frequencies.",
                        "citations": ["James 1:5-8", "James 4:8 ('purify your hearts, ye double minded')"]
                    },
                    {
                        "q": "How does Alma use 'double-minded' and 'awful dilemma'?",
                        "a": "Alma 5:12 — 'Have ye spiritually been born of God?' — mighty change = unified heart. Alma 7:3,18 — 'awful dilemma' = double bind of competing loyalties (pride vs. humility, God vs. world). Alma 5:28 — garments washed white through blood of Christ = resolution. The dilemma is resolved *only* through atonement.",
                        "citations": ["Alma 5:12-14, 28", "Alma 7:3, 18-19", "Alma 5:46-48 (Alma's own witness)"]
                    },
                    {
                        "q": "How does tithing overcome double-mindedness?",
                        "a": "Tithing is the **faith-action that collapses the wavefunction**. Elder Becerra: he sold his car *before* the buyer appeared. Obedience *before* outcome. 'One way to overcome double-mindedness is to learn to put God first' (talk). Tithing forces a binary choice: God first, or something else first. No third state.",
                        "citations": ["Matthew 6:22-24 (single eye vs. two masters)", "Alma 32:21-43 (faith as experiment -> evidence)", "D&C 88:67-68 (sanctify yourselves, single eye)"]
                    },
                    {
                        "q": "What is the relationship between pride and double-mindedness?",
                        "a": "Alma 7:3,18 links them. Pride = 'lifted up' — competing loyalty to self. Double-mindedness = wavering between God and self. Both are *fragmentation* of the soul. The cure in both cases: 'humble yourselves' (Alma 7:23) / 'put God first' (Matt 6:33).",
                        "citations": ["Alma 7:3, 18, 23", "Proverbs 16:18", "3 Nephi 12:3 (poor in spirit)"]
                    }
                ],
                "cross_refs": [
                    "James 1:5-8; 4:8", "Alma 5:12-14, 28, 46-48",
                    "Alma 7:3, 18-19, 23", "Matthew 6:22-24",
                    "D&C 88:67-68", "Psalm 119:113", "1 Kings 18:21"
                ]
            },
            {
                "id": "god_first_proton",
                "hue": "#2C5F7C",
                "label": "God First / Prōton",
                "qa_pairs": [
                    {
                        "q": "What does 'first' (prōton) mean in Matthew 6:33?",
                        "a": "prōton = first in time, place, rank, importance. Not sequential ('first, then others') but **architectonic** — the organizing principle that orders all else. JST Matthew 6:38: 'Seek ye first the kingdom of God' — Christ *is* the Kingdom. To seek Him first is to align every decision to His will.",
                        "citations": ["Matthew 6:33", "JST Matthew 6:38 (footnote b)", "3 Nephi 13:33 (identical)"]
                    },
                    {
                        "q": "How is 'putting God first' a covenantal identity?",
                        "a": "Baptismal covenant: 'willing to take upon [us] the name of Christ' (D&C 20:37; Moroni 6:3). This is identity reorientation — *who I am* determines *what I do*. Tithing is the tangible expression of that identity. 'Where your treasure is, there will your heart be also' (Matt 6:21).",
                        "citations": ["D&C 20:37", "Moroni 6:3", "Matthew 6:19-21", "Mosiah 5:7-12 (name of Christ)"]
                    },
                    {
                        "q": "What does Christ's example teach about 'first'?",
                        "a": "Gethsemane: 'not my will, but thine, be done' (Luke 22:42) — the **firstling of His will**. Cross: 'Father, into thy hands I commend my spirit' (Luke 23:46) — total consecration. He is 'the firstborn among many brethren' (Rom 8:29) — the pattern we follow. 'Jesus Christ is the perfect example of how to put God first' (Becerra).",
                        "citations": ["Luke 22:42", "Luke 23:46", "Romans 8:29", "John 4:34 ('my meat is to do the will of him that sent me')", "John 6:38"]
                    },
                    {
                        "q": "How does 'God first' reorder practical decisions?",
                        "a": "Elder Becerra's car: he needed it for business, but calculated what he owed on tithing + car loan, sold it. The buyer (dealer) paid exactly that amount. 'I want to be clear that Elder Cutler did not ask me to sell my car. This came to me after pondering and desiring to put God first.' The principle: *identify your firstling, offer it, trust the outcome*.",
                        "citations": ["Talk: personal anecdote (car sale)", "1 Samuel 15:22 ('to obey is better than sacrifice')", "D&C 98:13-15 (trial of faith)"]
                    }
                ],
                "cross_refs": [
                    "Matthew 6:33 (and JST 6:38)", "3 Nephi 13:33",
                    "Luke 22:42; 23:46", "John 4:34; 6:38",
                    "Romans 8:29", "D&C 20:37; 98:13-15", "Mosiah 5:7-12", "Talk: car sale anecdote"
                ]
            },
            {
                "id": "windows_capacity",
                "hue": "#3D7A9E",
                "label": "Windows of Heaven / Spiritual Capacity",
                "qa_pairs": [
                    {
                        "q": "What does 'windows of heaven' (arubbah) mean in Malachi 3:10?",
                        "a": "arubbah = floodgates, sluices, lattice windows — **categorical opening**, not a trickle. Used in Genesis 7:11 (flood), 8:2 (rain stopped), 2 Kings 7:2,19 (Elisha's prophecy). The metaphor: God's blessing is not metered; it's a deluge when the covenant channel is open.",
                        "citations": ["Malachi 3:10", "Genesis 7:11; 8:2", "2 Kings 7:2, 19", "3 Nephi 24:10"]
                    },
                    {
                        "q": "What is 'spiritual capacity' in Elder Becerra's teaching?",
                        "a": "Capacity = dynamic range — the distance between noise floor (double-mindedness, competing loyalties) and highlight clipping (fulness of joy). Tithing expands capacity by: (1) lowering noise floor (removing divided loyalty), (2) aligning heart to God (single eye), (3) inviting heavenly power ('enhance our spiritual capacity'). It's not transactional; it's *transformational*.",
                        "citations": ["Talk: 'enhance our spiritual capacity'", "D&C 88:67-68 (capacity to receive)", "Alma 32:28-34 (faith expands capacity)", "D&C 121:45-46 (confidence wax strong)"]
                    },
                    {
                        "q": "How does the 'devourer rebuked' (Mal 3:11) protect capacity?",
                        "a": "The devourer consumes *increase* — fruit, productivity, spiritual growth. Tithing invites divine protection over what you're trying to build. 'I will rebuke the devourer for your sakes, and he shall not destroy the fruits of your ground.' Temporal AND spiritual fruit preserved.",
                        "citations": ["Malachi 3:11", "3 Nephi 24:11", "D&C 64:23-24 (tithing protects the poor)"]
                    },
                    {
                        "q": "What is the relationship between witness and capacity?",
                        "a": "Elder Becerra's mother: 'All we need to see is the very hand of Jehovah Himself to have any greater assurance that He is blessing us by our payment of tithing.' **Witness precedes understanding** — Alma 32 faith cycle. Capacity grows *through* the experiment, not before it.",
                        "citations": ["Talk: mother's testimony", "Alma 32:21-43 (full faith cycle)", "Ether 12:6 ('trial of your faith')", "D&C 93:1 ('see my face and know that I am')"]
                    }
                ],
                "cross_refs": [
                    "Malachi 3:10-12 (full passage)", "3 Nephi 24:10-12",
                    "Genesis 7:11; 8:2 (arubbah usage)", "2 Kings 7:2, 19",
                    "Alma 32:21-43", "Ether 12:6, 27-28",
                    "D&C 88:67-68", "D&C 93:1", "D&C 121:45-46", "Talk: mother's testimony quote"
                ]
            }
        ],
        "deep_doctrine": {
            "tier_1_essential": [
                {"title": "Section 119 - Doctrine and Covenants Contexts", "source": "BYU Studies", "url": "https://byustudies.byu.edu/online-book/doctrine-and-covenants-contexts/1341", "key_insight": "Tithing = restatement of consecration, not replacement; 'standing law forever' (D&C 119:4). Heading error created 'higher/lower law' myth."},
                {"title": "The Laws of Consecration, Stewardship and Tithing", "author": "Craig J. Ostler", "source": "Sperry Symposium Classics: D&C (2004), 155-175", "key_insight": "Tithing as *law of sacrifice*; consecration extends beyond temporal. Tithing may require greater sacrifice than early consecration."},
                {"title": "'All Things Are the Lord's': The Law of Consecration in the D&C", "author": "Steven C. Harper", "source": "Sperry Symposium 2008, 212-27", "key_insight": "Consecration = celestial law; D&C 119 implements, doesn't replace. 'Folk memory' of higher/lower law challenged."},
                {"title": "Myself... I Consecrate to the God of Heaven", "source": "BYU Studies (20 Nauvoo affidavits, 1842)", "url": "https://byustudies.byu.edu/article/myself-i-consecrate-to-the-god-of-heaven-twenty-affidavits-of-consecration-in-nauvoo-junejuly-1842", "key_insight": "Primary evidence consecration practiced in Nauvoo 1842. Consecration never rescinded."},
                {"title": "Consecration Brings Forth Zion, Not Just Disaster Relief", "source": "Interpreter: A Journal of Mormon Scripture 26 (2017)", "url": "https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=1559&context=interpreter", "key_insight": "Defends traditional understanding; tithing as consecration compliance; united order = organized method."},
                {"title": "Appropriating Our Lives to Sacred Uses", "author": "Stephen B. Oveson", "source": "Religious Educator 3, no. 1 (2002): 9-16", "url": "https://rsc.byu.edu/vol-3-no-1-2002/appropriating-our-lives-sacred-uses-observations-personal-consecration", "key_insight": "Consecration = time, talents, will — not just money. 'Submission of one's will is the only uniquely personal thing we have to place on God's altar' (Maxwell)."}
            ],
            "tier_2_deepening": [
                {"title": "The Development of the Council on the Disposition of the Tithes", "source": "BYU Studies", "url": "https://byustudies.byu.edu/article/the-development-of-the-council-on-the-disposition-of-the-tithes", "focus": "D&C 120 implementation history - 1838 to 1943 reestablishment."},
                {"title": "The Atonement in the Old Testament", "source": "Sperry Symposium (various years)", "focus": "Typology of firstlings -> Christ. Abel, Passover lamb, Levitical system."},
                {"title": "Come Follow Me - Old Testament / Moses 5", "source": "BYU Studies Come Follow Me index", "url": "https://byustudies.byu.edu/come-follow-me/old-testament", "focus": "Scholarly articles on Moses 5 (Adam's sacrifice, angel's explanation)."},
                {"title": "Hebrew Word Studies: Bekorah, Arubbah, Dipsychos", "focus": "Lexical depth for firstlings, windows, double-mindedness."}
            ],
            "tier_3_podcast": [
                {"podcast": "followHIM", "season": "2026 Old Testament", "episodes": ["Elder Becerra talk reaction", "Tithing/Consecration episodes"], "guests": ["Scholars, General Authorities"], "strength": "Hebrew insights, Restoration connections"},
                {"podcast": "Scripture Insights", "hosts": "Taylor Halverson & Mike Harris", "episodes": ["Malachi 3 deep dive", "Moses 5 structure", "5-part Psalms structure applicable"], "strength": "Literary analysis, temple themes"},
                {"podcast": "Don't Miss This", "hosts": "Dave & Cali Black", "strength": "Practical application - 'firstlings in modern life'"},
                {"podcast": "Certain Women", "hosts": "Becky Squire & Tess Frame", "strength": "Women's voices on sacrifice/consecration, grace perspective"},
                {"podcast": "Latter-Day Insight", "strength": "5-act structure - Consecration as Act 4 (Covenants/Purity)"}
            ]
        }
    }


def load_hestia_reflection() -> dict:
    """Load Hestia's Lectio Divina reflection framework."""
    return {
        "lectio": {
            "title": "LECTIO — Read (10–15 min)",
            "prompts": [
                "Read the talk slowly, paragraph by paragraph. Let the words settle.",
                "Identify the scripture anchor for each doctrinal thread — which verses ground the teaching?",
                "Note the personal anecdote (car sale). What did Elder Becerra *feel*? What did he *do*?",
                "Mark every occurrence of 'first' / 'firstlings' / 'double-minded' / 'windows' / 'capacity'.",
                "Read the mother's testimony aloud. What does 'the very hand of Jehovah' evoke for you?"
            ]
        },
        "meditatio": {
            "title": "MEDITATIO — Meditate (15–30 min)",
            "prompts": [
                "Thread 1 (Tithing Law): Where in your life is the 'tithing covenant' active? Where is it dormant?",
                "Thread 2 (Firstlings): What is your 'firstling' right now — time, talent, treasure, attention? Are you offering it or holding it back?",
                "Thread 3 (Double-Mindedness): Where do you feel the 'awful dilemma' of competing loyalties? Name the two masters.",
                "Thread 4 (God First): If prōton is the organizing principle, what in your life is currently *misaligned* to it?",
                "Thread 5 (Windows/Capacity): What is the 'noise floor' in your spiritual life? What would 'opening the floodgates' feel like?"
            ]
        },
        "oratio": {
            "title": "ORATIO — Pray (10–15 min)",
            "prompts": [
                "Thread 1: 'Lord, teach me to see tithing not as a bill but as a covenant signature. Align my finances to my witness.'",
                "Thread 2: 'Father, help me identify my firstling — the thing I value most — and offer it freely, like Adam.'",
                "Thread 3: 'Jesus, my heart is divided between You and [name the rival]. Unite my heart to fear Thy name (Psalm 86:11).'",
                "Thread 4: 'Holy Spirit, reorganize my priorities around Christ as prōton. Let every decision flow from Him first.'",
                "Thread 5: 'Father, expand my spiritual capacity. Lower the noise. Open the floodgates. Let me see Thy hand.'"
            ]
        },
        "contemplatio": {
            "title": "CONTEMPLATIO — Contemplate (5–20 min)",
            "prompts": [
                "Sit in silence with the anchor phrase: 'Put God first.' Let it echo without analysis.",
                "Visualize the windows of heaven opening over your life — not as metaphor, as reality.",
                "Hold the image of Adam on the altar: obedience before understanding. Rest in that pattern.",
                "End by whispering: 'Thy will be done.' Carry that into the rest of your day."
            ]
        },
        "application_challenges": {
            "seed": [
                "This week: Pay tithing *first* — before any other bill. Note the internal resistance.",
                "Identify one 'double-minded' area. Make one decisive choice toward God.",
                "Offer a 'firstling' of your time: 15 min daily scripture study *before* phone/email."
            ],
            "root": [
                "Calculate your 'firstling' budget item. Adjust so tithing is truly first.",
                "Teach the firstlings principle to your family (FHE object lesson: first fruit = Christ).",
                "Fast with purpose: skip two meals, donate fast offering = firstling of your hunger."
            ],
            "branch": [
                "Share your tithing testimony with someone struggling — be the witness you needed.",
                "Audit monthly spending: Does every category align with 'God first'? Adjust one.",
                "Serve in a way that stretches your capacity — temple, ministering, welfare assignment."
            ],
            "fruit": [
                "Write your 'tithing covenant' statement. Sign it. Review annually at conference.",
                "Mentor someone in the faith-action of tithing obedience before outcome.",
                "Let your financial life be a living testimony: 'All we have is His first.'"
            ]
        },
        "journaling": {
            "daily": [
                "What did I put first today? (2 min)",
                "Where did I feel double-minded? (2 min)",
                "Where did I see God's hand? (2 min)"
            ],
            "weekly": [
                "How did 'God first' reorder my decisions this week? (15 min)",
                "What 'firstling' did I offer? What was the outcome? (15 min)",
                "What is my noise floor? What would silence it? (15 min)"
            ],
            "monthly": [
                "Covenant alignment review: Baptism/Sacrament/Temple/Ministering — rate 1-5. (30 min)",
                "Capacity check: Has my spiritual dynamic range expanded? Evidence? (30 min)",
                "Witness journal: Where did I see 'the very hand of Jehovah' this month? (30 min)"
            ]
        },
        "covenant_tracker": {
            "alignment_grid": [
                {"covenant": "Baptism (take His name)", "principle": "Tithing = bearing His name in finances", "alignment": 3, "action": ""},
                {"covenant": "Sacrament (remember Him)", "principle": "\"Put God first\" = remember Him in budget", "alignment": 3, "action": ""},
                {"covenant": "Temple (consecration)", "principle": "All increase = His", "alignment": 3, "action": ""},
                {"covenant": "Ministering (love as He loves)", "principle": "Fast offerings = love in action", "alignment": 3, "action": ""}
            ],
            "monthly_pulse": [
                "I pay tithing FIRST, not last",
                "Fast offering = sacrifice, not surplus",
                "Taught this to family",
                "Shared testimony of this",
                "Spending aligns with 'God first'"
            ]
        }
    }


def generate_talk_summary(talk: GCTalk, title: str = "") -> str:
    """Generate a concise summary of the entire talk from its full text."""
    if not talk.full_text:
        return ""
    
    # Use provided title or extract from talk
    title = title or talk.title
    if not title:
        title = "Tithing—Putting God First"  # fallback
    
    # Extract key points from the talk
    paragraphs = [p.strip() for p in talk.full_text.split('\n\n') if p.strip() and len(p.strip()) > 100]
    
    # Key themes to look for
    themes = []
    text = talk.full_text.lower()
    
    if 'tithing' in text or 'tithe' in text:
        themes.append("the law of tithing")
    if 'firstling' in text:
        themes.append("offering firstlings as a similitude of Christ's sacrifice")
    if 'double.mind' in text or 'double-minded' in text:
        themes.append("overcoming double-mindedness through putting God first")
    if 'first' in text and 'god' in text and 'seek' in text:
        themes.append("putting God first as the organizing principle of life (Matthew 6:33)")
    if 'window' in text and 'heaven' in text:
        themes.append("the windows of heaven opening for spiritual capacity")
    if 'adam' in text and 'eve' in text:
        themes.append("Adam and Eve's example of offering firstlings")
    if 'car' in text and 'sold' in text:
        themes.append("personal sacrifice of selling his car to pay tithing")
    if 'mother' in text and 'testimony' in text:
        themes.append("his mother's testimony of seeing Jehovah's hand through tithing")
    if 'hinckley' in text:
        themes.append("President Hinckley's promise about tithing and poverty")
    if 'holy ghost' in text or 'spiritual capacity' in text:
        themes.append("enhanced spiritual capacity through the Holy Ghost")
    
    # Build summary
    # Use the speaker's last name
    speaker_last = talk.speaker.split()[-1] if talk.speaker else "Becerra"
    
    summary_parts = [
        f"Elder {speaker_last}'s talk \"{title}\" teaches that tithing is not merely a financial obligation but a spiritual practice of putting God first."
    ]
    
    if themes:
        summary_parts.append(
            "Drawing from Alma's warning about the 'awful dilemma' of double-mindedness (Alma 7:3,18; James 1:8), "
            + ", ".join(themes[:-1]) + ", and " + themes[-1] + "."
        )
    
    summary_parts.append(
        "He shares a personal experience of selling his only car to pay tithing, after which the Lord provided another vehicle — illustrating the principle that when we offer our 'firstlings' (Moses 5:5-7), the Lord opens the windows of heaven (Malachi 3:10) and pours out spiritual capacity through the Holy Ghost (Moses 5:9; D&C 88:67-68)."
    )
    
    summary_parts.append(
        "Elder Becerra testifies that Jesus Christ is the perfect example of putting God first, and invites all to put God first in their lives through faithful tithing and offerings."
    )
    
    return " ".join(summary_parts)


def prepare_template_data(talk: GCTalk, resources: DiscoveredResources) -> dict:
    """Prepare all data for template rendering."""
    
    helios = load_helios_data()
    hestia = load_hestia_reflection()
    
    # Core message
    core_message = {
        "one_sentence": "Paying tithing puts God first, collapsing the double-minded dilemma and opening the windows of heaven for spiritual capacity.",
        "supporting": "Elder Becerra teaches that tithing is not merely financial — it's the practical act that unifies heart and action, following Adam's pattern of offering firstlings as a similitude of Christ.",
        "key_verse_text": "Seek ye first the kingdom of God, and his righteousness",
        "key_verse_ref": "Matthew 6:33",
    }
    
    # Doctrinal threads from Helios
    doctrinal_threads = []
    for thread in load_helios_data()["threads"]:
        doctrinal_threads.append({
            "id": thread["id"],
            "name": thread["label"],
            "short_name": thread["label"].split("/")[0].strip(),
            "hue": thread["hue"],
            "cdl": thread["qa_pairs"][0]["a"][:120] + "..." if thread["qa_pairs"] else "",
            "summary": thread["qa_pairs"][0]["a"][:300] + "..." if thread["qa_pairs"] else "",
            "key_scriptures": [c for qa in thread["qa_pairs"] for c in qa["citations"]][:6],
            "qa_pairs": thread["qa_pairs"],
            "cross_refs": thread["cross_refs"]
        })
    
    # Talk outline from sections
    talk_outline = []
    for section in talk.sections:
        if section.content.strip():
            talk_outline.append({
                "title": section.title,
                "content": section.content[:2000] + ("..." if len(section.content) > 2000 else "")
            })
    
    # Key quotes
    key_quotes = [{"text": q, "context": f"From \"{talk.title}\""} for q in talk.key_quotes[:8]]
    
    # Resources
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
    
    # Deep doctrine
    deep_doctrine = load_helios_data()["deep_doctrine"]
    
    # Discussion/reflection questions
    reflection_questions = []
    for thread in load_helios_data()["threads"]:
        for qa in thread["qa_pairs"]:
            reflection_questions.append({
                "question": qa["q"],
                "prompt": qa["a"][:300] + "..." if len(qa["a"]) > 300 else qa["a"],
                "scripture": "; ".join(qa["citations"][:2])
            })
    
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
    
    # Full talk text (for the talk-content section)
    talk_paragraphs = []
    for section in talk.sections:
        if section.content.strip():
            for para in section.content.split('\n\n'):
                para = para.strip()
                if para:
                    talk_paragraphs.append(para)
    
    # Also include main talk text if sections don't cover it
    if not talk_paragraphs and talk.full_text:
        for para in talk.full_text.split('\n\n'):
            para = para.strip()
            if len(para) > 50:
                talk_paragraphs.append(para)
    
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
        "discussion_questions": reflection_questions[:10],
        "application_challenge": application_challenge,
        "generation_date": datetime.now().strftime("%B %d, %Y"),
        "output_url": "Generated by personal_gc_talk_study_guide skill",
        # Also include top-level variables for template compatibility
        "speaker_name": talk.speaker,
        "speaker_title": talk.speaker_calling or "Of the Seventy",
        "talk_title": talk.title,
        "conference": talk.conference,
        "session": talk.session,
        "date": talk.date,
        "speaker_photo": HERO_IMAGE_URL,
        # Talk summary for the new summary section
        "talk_summary": core_message.get("supporting", "") if isinstance(core_message, dict) else str(core_message)[:500],
        "hestia": load_hestia_reflection(),
        "talk_paragraphs": talk_paragraphs,
        "full_talk_text": talk.full_text,
    }


def render_template(template_path: Path, data: dict) -> str:
    """Render template using Jinja2."""
    try:
        from jinja2 import Environment, FileSystemLoader, select_autoescape
    except ImportError:
        print("Jinja2 not installed. Install with: pip install jinja2", file=sys.stderr)
        # Fallback to basic string replacement
        with open(template_path, 'r') as f:
            template = f.read()
        # Simple replacement for critical variables
        import re
        def replace_var(match):
            path = match.group(1).strip()
            keys = path.split('.')
            value = data
            for k in keys:
                if '[' in k and ']' in k:
                    base, idx = k.split('[')
                    idx = int(idx.rstrip(']'))
                    value = value.get(base, [])[idx] if value.get(base) else ''
                else:
                    value = value.get(k, '') if isinstance(value, dict) else ''
            return str(value) if value else ''
        template = re.sub(r'\{\{\s*([^}]+)\s*\}\}', replace_var, template)
        return template
    
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
        chrome_paths = [
            'google-chrome',
            'chrome',
            'chromium',
            'chromium-browser',
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Chromium.app/Contents/MacOS/Chromium',
        ]
        
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


async def build_lesson(talk_url: str, output_dir: Path, export_pdf_flag: bool = False) -> dict:
    """Run the full pipeline."""
    
    output_dir = Path(output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate folder name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    talk_slug = slugify(talk_url.split('/')[-1].replace('?lang=eng', ''))
    folder_name = f"{datetime.now().strftime('%Y-%m')}_{talk_slug}_Becerra_PersonalStudy"
    lesson_dir = output_dir / folder_name
    lesson_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Output directory: {lesson_dir}")
    
    # Step 1: Load pre-built mobile data (includes all 6 questions, callouts, threads, etc.)
    print("📂 Loading pre-built mobile study data...")
    mobile_data_path = SCRIPTS_DIR.parent / "references" / "becerra_tithing_mobile_april2026.json"
    with open(mobile_data_path, 'r') as f:
        mobile_data = json.load(f)
    
    # Step 2: Fetch talk (for metadata and scripture refs)
    print("🔍 Fetching General Conference talk...")
    talk = await fetch_gc_talk_async(talk_url)
    
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
    
    # Talk summary
    print("📝 Generating talk summary...")
    talk_summary = generate_talk_summary(talk, title=mobile_data["talk_title"])
    
    # Convert markdown to HTML for template
    try:
        import markdown
        talk_summary_html = markdown.markdown(talk_summary, extensions=['tables', 'fenced_code', 'codehilite'])
    except ImportError:
        talk_summary_html = talk_summary
    print(f"   ✅ Summary generated ({len(talk_summary)} chars)")
    
    # Step 2: Discover resources
    print("🔗 Discovering related resources...")
    resources = discover_resources(talk_dict)
    
    resources_json_path = lesson_dir / "resources.json"
    with open(resources_json_path, 'w') as f:
        json.dump(dataclasses.asdict(resources), f, indent=2, ensure_ascii=False)
    print(f"   ✅ Resources saved to {resources_json_path}")
    print(f"   📚 Found {len(resources.related_gc_talks)} related GC talks, {len(resources.gospel_topics)} Gospel Topics, {len(resources.byu_speeches)} BYU speeches, {len(resources.scripture_chain)} scripture chain refs")
    
    # Step 3: Prepare template data from mobile data
    print("🎨 Preparing template data...")
    template_data = {
        "speaker_name": mobile_data["speaker_name"],
        "speaker_title": mobile_data["speaker_title"],
        "talk_title": mobile_data["talk_title"],
        "conference": mobile_data["conference"],
        "session": mobile_data["session"],
        "date": mobile_data["date"],
        "hero_artwork": mobile_data["hero_artwork"],
        "callouts": mobile_data["callouts"],
        "threads": mobile_data["threads"],
        "resources": mobile_data["resources"],
        "reflections": mobile_data["reflections"],
        "generation_date": datetime.now().strftime("%B %d, %Y"),
        "output_url": "Generated by personal_gc_talk_study_guide skill",
        # Add generated talk summary
        "talk_summary": talk_summary,
        "talk_summary_html": talk_summary_html,
    }
    
    # Step 4: Render HTML template
    print("📝 Rendering HTML template...")
    
    html = render_template(SCRIPTS_DIR.parent / "templates" / "personal-study.html", template_data)
    
    html_path = lesson_dir / "study-guide.html"
    with open(html_path, 'w') as f:
        f.write(html)
    print(f"   ✅ Study guide: {html_path}")
    
    # Step 3: Inject Gospel Library links (using the mobile data's scripture refs)
    print("🔗 Injecting Gospel Library links...")
    
    scripture_refs = DEFAULT_SCRIPTURE_REFS.copy()
    for thread in mobile_data["threads"]:
        for qa in thread.get("qa_pairs", []):
            if qa.get("scripture"):
                for cite in qa["scripture"].split("; "):
                    # Parse citation into components
                    parts = cite.strip().split(" ")
                    if len(parts) >= 2:
                        book = " ".join(parts[:-1])
                        chapter_verse = parts[-1]
                        if ":" in chapter_verse:
                            chapter, verse = chapter_verse.split(":")
                            scripture_refs[cite.strip()] = (book.lower(), int(chapter), verse)
    
    for item in mobile_data["callouts"]:
        if item.get("scripture"):
            for cite in item["scripture"].split("; "):
                parts = cite.strip().split(" ")
                if len(parts) >= 2:
                    book = " ".join(parts[:-1])
                    chapter_verse = parts[-1]
                    if ":" in chapter_verse:
                        chapter, verse = chapter_verse.split(":")
                        scripture_refs[cite.strip()] = (book.lower(), int(chapter), verse)
    
    with open(html_path, 'r') as f:
        html = f.read()
    processed = inject_links(html, scripture_refs)
    with open(html_path, 'w') as f:
        f.write(processed)
    print(f"   ✅ Links injected")
    
    # Step 4: Copy assets
    print("📦 Copying assets...")
    assets_src = SCRIPTS_DIR.parent / "assets"
    assets_dst = lesson_dir / "assets"
    if assets_src.exists():
        shutil.copytree(assets_src, assets_dst, dirs_exist_ok=True)
        print(f"   ✅ Assets copied to {assets_dst}")
    
    # Step 5: Export PDF
    pdf_results = {}
    if export_pdf_flag:
        print("📄 Exporting PDF...")
        pdf_file = lesson_dir / "study-guide.pdf"
        if export_pdf(html_path, pdf_file):
            pdf_results["study-guide"] = str(pdf_file)
            print(f"   ✅ study-guide.pdf exported")
        else:
            print(f"   ⚠️  PDF export failed")
    
    # Step 6: Create sources.md
    sources_path = lesson_dir / "sources.md"
    with open(sources_path, 'w') as f:
        f.write(f"# Sources for \"{mobile_data['talk_title']}\"\n\n")
        f.write(f"**Talk:** {mobile_data['talk_title']} by {mobile_data['speaker_name']}\n")
        f.write(f"**Conference:** {mobile_data['conference']} ({mobile_data['session']})\n")
        f.write(f"**Date:** {mobile_data['date']}\n")
        f.write(f"**URL:** https://www.churchofjesuschrist.org/study/general-conference/2026/04/18becerra?lang=eng\n\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
        f.write("## Related General Conference Talks\n\n")
        for r in mobile_data["resources"]:
            f.write(f"- [{r['title']}]({r['url']}) — {r['author']}, {r['source']}\n")
        f.write("\n## Scripture References\n\n")
        for thread in mobile_data["threads"]:
            for qa in thread.get("qa_pairs", []):
                if qa.get("scripture"):
                    for cite in qa["scripture"].split("; "):
                        f.write(f"- {cite.strip()}\n")
        for callout in mobile_data["callouts"]:
            if callout.get("scripture"):
                for cite in callout["scripture"].split("; "):
                    f.write(f"- {cite.strip()}\n")
    
    print(f"   ✅ Sources documented: {sources_path}")
    
    return {
        "lesson_dir": str(lesson_dir),
        "study_guide": str(html_path),
        "pdfs": pdf_results,
        "sources": str(sources_path),
    }


async def fetch_gc_talk_async(talk_url: str) -> GCTalk:
    """Async wrapper for fetch_gc_talk using the existing sync function in a thread."""
    # Run the sync fetch_gc_talk in a thread pool
    loop = asyncio.get_event_loop()
    talk = await loop.run_in_executor(None, fetch_gc_talk, talk_url)
    return talk


def main():
    parser = argparse.ArgumentParser(description='Personal GC Talk Study Guide Builder')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build complete study guide from talk URL')
    build_parser.add_argument('--talk-url', required=True, help='General Conference talk URL')
    build_parser.add_argument('--output-dir', default='~/Desktop/Elders Quorum Lessons 2025.2026', help='Output directory')
    build_parser.add_argument('--export-pdf', action='store_true', help='Export PDF (requires Chrome/Chromium)')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'build':
            result = asyncio.run(build_lesson(args.talk_url, Path(args.output_dir), args.export_pdf))
            print("\n✅ Build complete!")
            print(f"📁 Study folder: {result['lesson_dir']}")
            for key, val in result.items():
                if key != 'lesson_dir':
                    print(f"   {key}: {val}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()