---
name: personal_gc_talk_study_guide
title: Personal General Conference Talk Study Guide
description: "Create GC talk guide: 5 threads, hue Q&A, tiered doctrine."
category: religious-study
version: "1.0.0"
author: "Helios"
license: "MIT"
tags: [lds, general-conference, study-guide, personal-study, doctrine, tithing]
related_skills: [come-follow-me-study-guide, come-follow-me-lesson-prep, churchofjesuschrist-navigation]
metadata:
  hermes:
    tags: [lds, general-conference, study-guide, personal-study, doctrine, tithing]
    related_skills: [come-follow-me-study-guide, come-follow-me-lesson-prep, churchofjesuschrist-navigation]
---

# Personal General Conference Talk Study Guide

## When to Use
Use when creating a personal study guide for a single General Conference talk. Output is structured data (JSON/YAML) ready for template injection - not a full HTML document. Designed for rapid personal use, not class teaching. Trigger: "create study guide for [GC talk]" or "analyze [speaker] [talk title]".

## Trigger
Use when creating a personal study guide for a single General Conference talk. Output is structured data (JSON/YAML) ready for template injection - not a full HTML document. Designed for rapid personal use, not class teaching.

## Core Principle
**One talk -> Five threads -> Hue-coded Q&A pairs -> Tiered deep doctrine**  
Each thread has a spectral hue (doctrinal color), 3-5 Q&A pairs with exact citations, cross-reference cluster, and a deep doctrine addendum in three tiers.

---

# ELDER JORGE T. BECERRA - "TITHING-PUTTING GOD FIRST" (APRIL 2026)

## Talk Metadata
```yaml
talk:
  speaker: "Elder Jorge T. Becerra"
  title: "Tithing-Putting God First"
  session: "Saturday Morning Session"
  date: "April 2026"
  url: "https://www.churchofjesuschrist.org/study/general-conference/2026/04/18becerra?lang=eng"
  core_thesis: "Tithing is not merely a financial commandment but a spiritual practice of putting God first, overcoming double-mindedness through the ancient pattern of offering firstlings, which expands spiritual capacity and opens the windows of heaven."
  personal_anecdote: "Selling his car to pay tithing during financial hardship - obedience before outcome."
  closing_witness: "Jesus Christ is the perfect example of putting God first (Gethsemane, Cross)."
```

---

## THREAD 1: TITHING LAW - HUE: #1A3C5E (DEEP NAVY - FOUNDATIONAL LAW)
**Spectral Position**: 220 - The bedrock; all other threads build on this legal/covenantal framework.

### Q&A Pairs
```yaml
thread_1_tithing_law:
  hue: "#1A3C5E"
  label: "Tithing Law"
  qa_pairs:
    - q: "What is the legal/covenantal basis for tithing in this dispensation?"
      a: "Doctrine and Covenants 119 - revealed July 8, 1838, in answer to Joseph Smith's prayer: 'O Lord, show unto thy servants how much thou requirest of the properties of thy people for a tithing?' The Lord answered: all surplus property first, then one-tenth of interest annually - 'a standing law unto them forever' (D&C 119:4)."
      citations:
        - "D&C 119:1-7"
        - "D&C 120 (Council on Disposition of Tithes)"
    - q: "Does tithing replace the law of consecration?"
      a: "No. Section 119 restates consecration (D&C 42:33, 54) and defines surplus as one-tenth. It is 'the beginning of the tithing of my people' (D&C 119:1) - implementation, not replacement. President Hinckley: 'the law of sacrifice and the law of consecration were not done away with and are still in effect.'"
      citations:
        - "D&C 119:1-4"
        - "D&C 42:30-39"
        - "D&C 104:4-9 (United Firm != law of consecration)"
    - q: "What does Malachi 3 teach about the tithing covenant?"
      a: "Post-exilic context: temple rebuilt but hearts cold. 'Return unto me, and I will return unto you' (v. 7). Tithing is the diagnostic - 'Will a man rob God?' (v. 8). The promise: windows opened, devourer rebuked, all nations call you blessed (vv. 10-12)."
      citations:
        - "Malachi 3:7-12"
        - "3 Nephi 24:7-12 (Nephite repetition)"
    - q: "What is the 'Council on the Disposition of the Tithes' and why does it matter?"
      a: "D&C 120: First Presidency, Quorum of Twelve, Presiding Bishopric authorize expenditure. Reestablished 1943 after 1838 revelation. Demonstrates living revelation - tithes are sacred, disposition is revelatory, not bureaucratic."
      citations:
        - "D&C 120:1-3"
        - "BYU Studies: 'The Development of the Council on the Disposition of the Tithes'"
  cross_refs:
    - "D&C 119 (full section)"
    - "D&C 120 (full section)"
    - "Malachi 3:7-12"
    - "3 Nephi 24:7-12"
    - "D&C 64:23-24 (tithing and the poor)"
    - "D&C 85:3 (tithing and inheritance in Zion)"
```

---

## THREAD 2: FIRSTLINGS / ADAM - HUE: #D4A537 (GOLD - PRIESTLY PATTERN)
**Spectral Position**: 45 - The archetypal pattern; priestly, sacrificial, typological.

### Q&A Pairs
```yaml
thread_2_firstlings_adam:
  hue: "#D4A537"
  label: "Firstlings / Adam's Offering"
  qa_pairs:
    - q: "What did Adam offer and why does it matter?"
      a: "Moses 5:5 - 'Adam was obedient... I know not, save the Lord commanded me.' He offered firstlings of the flock. The angel explained: 'This thing is a similitude of the sacrifice of the Only Begotten of the Father, which is full of grace and truth' (Moses 5:7). Obedience *precedes* understanding."
      citations:
        - "Moses 5:5-7"
        - "Abraham 3:25 (premortal test of obedience)"
    - q: "What does 'firstlings' (bekorah) mean in Hebrew?"
      a: "bekorah = firstborn, birthright, preeminence, priority. Not '10%' - the **first, the best, the representative whole**. The firstling *stands for* the entire flock. Tithing restores this pattern when stewardship-based consecration isn't institutionally administered."
      citations:
        - "Genesis 4:4 (Abel's firstlings)"
        - "Exodus 13:2, 12-13 (firstborn consecrated)"
        - "Colossians 1:15 (Christ as Firstborn of creation)"
    - q: "How does the firstling pattern connect to Christ?"
      a: "Typological arc: Abel's accepted offering (Heb 11:4) -> Firstborn consecrated in Egypt (Ex 13) -> Christ as 'Firstborn among many brethren' (Rom 8:29) -> 'Firstborn of every creature' (Col 1:15) -> We offer our 'firstlings' (time, talent, treasure) as participation in His consecration."
      citations:
        - "Hebrews 11:4"
        - "Romans 8:29"
        - "Colossians 1:15-18"
        - "D&C 93:21 (Christ as Firstborn)"
    - q: "What do the Nauvoo 1842 consecration affidavits reveal?"
      a: "20 handwritten affidavits (June-July 1842) prove consecration was actively taught and practiced in Nauvoo - *after* the supposed 'replacement' by tithing. The 'higher law/lower law' folk memory is historically false. Consecration = celestial law; tithing = standing implementation."
      citations:
        - "BYU Studies: 'Myself... I Consecrate to the God of Heaven' (20 affidavits)"
        - "D&C 119:1 (tithing = 'beginning' of consecration)"
  cross_refs:
    - "Moses 5:5-7 (full passage)"
    - "Genesis 4:1-8 (Cain and Abel)"
    - "Exodus 13:1-16 (firstborn law)"
    - "Leviticus 27:26-27 (firstlings holy to Lord)"
    - "Hebrews 11:4"
    - "Romans 8:28-30"
    - "Colossians 1:15-20"
    - "D&C 93:21-22"
    - "BYU Studies: Nauvoo affidavits article"
```

---

## THREAD 3: DOUBLE-MINDEDNESS - HUE: #8B6914 (AMBER - DIAGNOSTIC WARNING)
**Spectral Position**: 35 - The contamination; mixed loyalties produce instability (mud).

### Q&A Pairs
```yaml
thread_3_double_mindedness:
  hue: "#8B6914"
  label: "Double-Mindedness"
  qa_pairs:
    - q: "What does 'double-minded' mean in James 1:8?"
      a: "dipsychos = two-souled, divided loyalty. 'A double minded man is unstable in all his ways' (akatastatos = unstable, inconstant, restless). Context: asking God for wisdom *in faith, nothing wavering* (James 1:5-6). The double mind cannot receive because it's tuned to two frequencies."
      citations:
        - "James 1:5-8"
        - "James 4:8 ('purify your hearts, ye double minded')"
    - q: "How does Alma use 'double-minded' and 'awful dilemma'?"
      a: "Alma 5:12 - 'Have ye spiritually been born of God?' - mighty change = unified heart. Alma 7:3,18 - 'awful dilemma' = double bind of competing loyalties (pride vs. humility, God vs. world). Alma 5:28 - garments washed white through blood of Christ = resolution. The dilemma is resolved *only* through atonement."
      citations:
        - "Alma 5:12-14, 28"
        - "Alma 7:3, 18-19"
        - "Alma 5:46-48 (Alma's own witness)"
    - q: "How does tithing overcome double-mindedness?"
      a: "Tithing is the **faith-action that collapses the wavefunction**. Elder Becerra: he sold his car *before* the buyer appeared. Obedience *before* outcome. 'One way to overcome double-mindedness is to learn to put God first' (talk). Tithing forces a binary choice: God first, or something else first. No third state."
      citations:
        - "Matthew 6:22-24 (single eye vs. two masters)"
        - "Alma 32:21-43 (faith as experiment -> evidence)"
        - "D&C 88:67-68 (sanctify yourselves, single eye)"
    - q: "What is the relationship between pride and double-mindedness?"
      a: "Alma 7:3,18 links them. Pride = 'lifted up' - competing loyalty to self. Double-mindedness = wavering between God and self. Both are *fragmentation* of the soul. The cure in both cases: 'humble yourselves' (Alma 7:23) / 'put God first' (Matt 6:33)."
      citations:
        - "Alma 7:3, 18, 23"
        - "Proverbs 16:18"
        - "3 Nephi 12:3 (poor in spirit)"
  cross_refs:
    - "James 1:5-8; 4:8"
    - "Alma 5:12-14, 28, 46-48"
    - "Alma 7:3, 18-19, 23"
    - "Matthew 6:22-24"
    - "D&C 88:67-68"
    - "Psalm 119:113 ('I hate vain thoughts: but thy law do I love')"
    - "1 Kings 18:21 ('halt ye between two opinions')"
```

---

## THREAD 4: GOD FIRST / PROTON - HUE: #2C5F7C (TEAL - ORGANIZING PRINCIPLE)
**Spectral Position**: 195 - The reference white; everything aligns to this.

### Q&A Pairs
```yaml
thread_4_god_first_proton:
  hue: "#2C5F7C"
  label: "God First / Proton"
  qa_pairs:
    - q: "What does 'first' (proton) mean in Matthew 6:33?"
      a: "proton = first in time, place, rank, importance. Not sequential ('first, then others') but **architectonic** - the organizing principle that orders all else. JST Matthew 6:38: 'Seek ye first the kingdom of God' - Christ *is* the Kingdom. To seek Him first is to align every decision to His will."
      citations:
        - "Matthew 6:33"
        - "JST Matthew 6:38 (footnote b)"
        - "3 Nephi 13:33 (identical)"
    - q: "How is 'putting God first' a covenantal identity?"
      a: "Baptismal covenant: 'willing to take upon [us] the name of Christ' (D&C 20:37; Moroni 6:3). This is identity reorientation - *who I am* determines *what I do*. Tithing is the tangible expression of that identity. 'Where your treasure is, there will your heart be also' (Matt 6:21)."
      citations:
        - "D&C 20:37"
        - "Moroni 6:3"
        - "Matthew 6:19-21"
        - "Mosiah 5:7-12 (name of Christ)"
    - q: "What does Christ's example teach about 'first'?"
      a: "Gethsemane: 'not my will, but thine, be done' (Luke 22:42) - the **firstling of His will**. Cross: 'Father, into thy hands I commend my spirit' (Luke 23:46) - total consecration. He is 'the firstborn among many brethren' (Rom 8:29) - the pattern we follow. 'Jesus Christ is the perfect example of how to put God first' (Becerra)."
      citations:
        - "Luke 22:42"
        - "Luke 23:46"
        - "Romans 8:29"
        - "John 4:34 ('my meat is to do the will of him that sent me')"
        - "John 6:38"
    - q: "How does 'God first' reorder practical decisions?"
      a: "Elder Becerra's car: he needed it for business, but calculated what he owed on tithing + car loan, sold it. The buyer (dealer) paid exactly that amount. 'I want to be clear that Elder Cutler did not ask me to sell my car. This came to me after pondering and desiring to put God first.' The principle: *identify your firstling, offer it, trust the outcome*."
      citations:
        - "Talk: personal anecdote (car sale)"
        - "1 Samuel 15:22 ('to obey is better than sacrifice')"
        - "D&C 98:13-15 (trial of faith)"
  cross_refs:
    - "Matthew 6:33 (and JST 6:38)"
    - "3 Nephi 13:33"
    - "Luke 22:42; 23:46"
    - "John 4:34; 6:38"
    - "Romans 8:29"
    - "D&C 20:37; 98:13-15"
    - "Mosiah 5:7-12"
    - "Talk: car sale anecdote"
```

---

## THREAD 5: WINDOWS OF HEAVEN / SPIRITUAL CAPACITY - HUE: #3D7A9E (LIGHT BLUE - RECEPTIVE CAPACITY)
**Spectral Position**: 200 - The aperture; capacity to receive, hold, channel light.

### Q&A Pairs
```yaml
thread_5_windows_capacity:
  hue: "#3D7A9E"
  label: "Windows of Heaven / Spiritual Capacity"
  qa_pairs:
    - q: "What does 'windows of heaven' (arubbah) mean in Malachi 3:10?"
      a: "arubbah = floodgates, sluices, lattice windows - **categorical opening**, not a trickle. Used in Genesis 7:11 (flood), 8:2 (rain stopped), 2 Kings 7:2,19 (Elisha's prophecy). The metaphor: God's blessing is not metered; it's a deluge when the covenant channel is open."
      citations:
        - "Malachi 3:10"
        - "Genesis 7:11; 8:2"
        - "2 Kings 7:2, 19"
        - "3 Nephi 24:10"
    - q: "What is 'spiritual capacity' in Elder Becerra's teaching?"
      a: "Capacity = dynamic range - the distance between noise floor (double-mindedness, competing loyalties) and highlight clipping (fulness of joy). Tithing expands capacity by: (1) lowering noise floor (removing divided loyalty), (2) aligning heart to God (single eye), (3) inviting heavenly power ('enhance our spiritual capacity'). It's not transactional; it's *transformational*."
      citations:
        - "Talk: 'enhance our spiritual capacity'"
        - "D&C 88:67-68 (capacity to receive)"
        - "Alma 32:28-34 (faith expands capacity)"
        - "D&C 121:45-46 (confidence wax strong)"
    - q: "How does the 'devourer rebuked' (Mal 3:11) protect capacity?"
      a: "The devourer consumes *increase* - fruit, productivity, spiritual growth. Tithing invites divine protection over what you're trying to build. 'I will rebuke the devourer for your sakes, and he shall not destroy the fruits of your ground.' Temporal AND spiritual fruit preserved."
      citations:
        - "Malachi 3:11"
        - "3 Nephi 24:11"
        - "D&C 64:23-24 (tithing protects the poor)"
    - q: "What is the relationship between witness and capacity?"
      a: "Elder Becerra's mother: 'All we need to see is the very hand of Jehovah Himself to have any greater assurance that He is blessing us by our payment of tithing.' **Witness precedes understanding** - Alma 32 faith cycle. Capacity grows *through* the experiment, not before it."
      citations:
        - "Talk: mother's testimony"
        - "Alma 32:21-43 (full faith cycle)"
        - "Ether 12:6 ('trial of your faith')"
        - "D&C 93:1 ('see my face and know that I am')"
  cross_refs:
    - "Malachi 3:10-12 (full passage)"
    - "3 Nephi 24:10-12"
    - "Genesis 7:11; 8:2 (arubbah usage)"
    - "2 Kings 7:2, 19"
    - "Alma 32:21-43"
    - "Ether 12:6, 27-28"
    - "D&C 88:67-68"
    - "D&C 93:1"
    - "D&C 121:45-46"
    - "Talk: mother's testimony quote"
```

---

## DEEP DOCTRINE ADDENDUM - TIERED RESOURCES

### TIER 1: ESSENTIAL (Read First - Directly on Topic)
```yaml
tier_1_essential:
  - title: "Section 119 - Doctrine and Covenants Contexts"
    source: "BYU Studies"
    url: "https://byustudies.byu.edu/online-book/doctrine-and-covenants-contexts/1341"
    key_insight: "Tithing = restatement of consecration, not replacement; 'standing law forever' (D&C 119:4). Heading error created 'higher/lower law' myth."
  - title: "The Laws of Consecration, Stewardship and Tithing"
    author: "Craig J. Ostler"
    source: "Sperry Symposium Classics: D&C (2004), 155-175"
    key_insight: "Tithing as *law of sacrifice*; consecration extends beyond temporal. Tithing may require greater sacrifice than early consecration."
  - title: "'All Things Are the Lord's': The Law of Consecration in the D&C"
    author: "Steven C. Harper"
    source: "Sperry Symposium 2008, 212-27"
    key_insight: "Consecration = celestial law; D&C 119 implements, doesn't replace. 'Folk memory' of higher/lower law challenged."
  - title: "Myself... I Consecrate to the God of Heaven"
    source: "BYU Studies (20 Nauvoo affidavits, 1842)"
    url: "https://byustudies.byu.edu/article/myself-i-consecrate-to-the-god-of-heaven-twenty-affidavits-of-consecration-in-nauvoo-junejuly-1842"
    key_insight: "Primary evidence consecration practiced in Nauvoo 1842. Consecration never rescinded."
  - title: "Consecration Brings Forth Zion, Not Just Disaster Relief"
    source: "Interpreter: A Journal of Mormon Scripture 26 (2017)"
    url: "https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=1559&context=interpreter"
    key_insight: "Defends traditional understanding; tithing as consecration compliance; united order = organized method."
  - title: "Appropriating Our Lives to Sacred Uses"
    author: "Stephen B. Oveson"
    source: "Religious Educator 3, no. 1 (2002): 9-16"
    url: "https://rsc.byu.edu/vol-3-no-1-2002/appropriating-our-lives-sacred-uses-observations-personal-consecration"
    key_insight: "Consecration = time, talents, will - not just money. 'Submission of one's will is the only uniquely personal thing we have to place on God's altar' (Maxwell)."
```

### TIER 2: DEEPENING (Historical, Typological, Linguistic)
```yaml
tier_2_deepening:
  - title: "The Development of the Council on the Disposition of the Tithes"
    source: "BYU Studies"
    url: "https://byustudies.byu.edu/article/the-development-of-the-council-on-the-disposition-of-the-tithes"
    focus: "D&C 120 implementation history - 1838 to 1943 reestablishment."
  - title: "The Atonement in the Old Testament"
    source: "Sperry Symposium (various years)"
    focus: "Typology of firstlings -> Christ. Abel, Passover lamb, Levitical system."
  - title: "Come Follow Me - Old Testament / Moses 5"
    source: "BYU Studies Come Follow Me index"
    url: "https://byustudies.byu.edu/come-follow-me/old-testament"
    focus: "Scholarly articles on Moses 5 (Adam's sacrifice, angel's explanation)."
  - title: "Hebrew Word Studies: Bekorah, Arubbah, Dipsychos"
    focus: "Lexical depth for firstlings, windows, double-mindedness."
```

### TIER 3: PODCAST INTEGRATION (Audio/Video for Different Learning Styles)
```yaml
tier_3_podcast:
  - podcast: "followHIM"
    season: "2026 Old Testament"
    episodes: ["Elder Becerra talk reaction", "Tithing/Consecration episodes"]
    guests: ["Scholars, General Authorities"]
    strength: "Hebrew insights, Restoration connections"
  - podcast: "Scripture Insights"
    hosts: "Taylor Halverson & Mike Harris"
    episodes: ["Malachi 3 deep dive", "Moses 5 structure", "5-part Psalms structure applicable"]
    strength: "Literary analysis, temple themes"
  - podcast: "Don't Miss This"
    hosts: "Dave & Cali Black"
    strength: "Practical application - 'firstlings in modern life'"
  - podcast: "Certain Women"
    hosts: "Becky Squire & Tess Frame"
    strength: "Women's voices on sacrifice/consecration, grace perspective"
  - podcast: "Latter-Day Insight"
    strength: "5-act structure - Consecration as Act 4 (Covenants/Purity)"
```

---

## OUTPUT FORMAT FOR TEMPLATE INJECTION

### JSON Structure (ready for template engine)
```json
{
  "talk": { ... },
  "threads": [
    {
      "id": "tithing_law",
      "hue": "#1A3C5E",
      "label": "Tithing Law",
      "qa_pairs": [...],
      "cross_refs": [...]
    },
    {
      "id": "firstlings_adam",
      "hue": "#D4A537",
      "label": "Firstlings / Adam",
      "qa_pairs": [...],
      "cross_refs": [...]
    },
    {
      "id": "double_mindedness",
      "hue": "#8B6914",
      "label": "Double-Mindedness",
      "qa_pairs": [...],
      "cross_refs": [...]
    },
    {
      "id": "god_first_proton",
      "hue": "#2C5F7C",
      "label": "God First / Proton",
      "qa_pairs": [...],
      "cross_refs": [...]
    },
    {
      "id": "windows_capacity",
      "hue": "#3D7A9E",
      "label": "Windows / Capacity",
      "qa_pairs": [...],
      "cross_refs": [...]
    }
  ],
  "deep_doctrine_addendum": {
    "tier_1_essential": [...],
    "tier_2_deepening": [...],
    "tier_3_podcast": [...]
  }
}
```

### YAML Front-Matter for Markdown Template
```yaml
---
talk:
  speaker: "Elder Jorge T. Becerra"
  title: "Tithing-Putting God First"
  date: "April 2026"
threads:
  - id: tithing_law
    hue: "#1A3C5E"
    label: "Tithing Law"
    qa_pairs: [...]
    cross_refs: [...]
  - id: firstlings_adam
    hue: "#D4A537"
    label: "Firstlings / Adam"
    qa_pairs: [...]
    cross_refs: [...]
  - id: double_mindedness
    hue: "#8B6914"
    label: "Double-Mindedness"
    qa_pairs: [...]
    cross_refs: [...]
  - id: god_first_proton
    hue: "#2C5F7C"
    label: "God First / Proton"
    qa_pairs: [...]
    cross_refs: [...]
  - id: windows_capacity
    hue: "#3D7A9E"
    label: "Windows / Capacity"
    qa_pairs: [...]
    cross_refs: [...]
deep_doctrine:
  tier_1_essential: [...]
  tier_2_deepening: [...]
  tier_3_podcast: [...]
---
```

---

## USAGE WORKFLOW

1. **Fetch talk** -> extract text, identify 5 threads
2. **Map each thread** -> hue + 3-5 Q&A + cross-refs
3. **Curate addendum** -> tier 1/2/3 resources
4. **Export structured data** -> JSON/YAML for template
5. **Inject into template** -> personal study guide (Markdown/HTML/PDF)

---

## TEMPLATE COMPATIBILITY

Designed to work with:
- Obsidian Dataview queries (YAML front-matter)
- Jinja2 / Liquid templates (JSON)
- Custom HTML/CSS (hue variables as CSS custom properties)
- Notion database import (CSV/JSON)

Color variables for template:
```css
:root {
  --hue-tithing-law: #1A3C5E;
  --hue-firstlings: #D4A537;
  --hue-double-minded: #8B6914;
  --hue-god-first: #2C5F7C;
  --hue-windows: #3D7A9E;
}
```

---

## VERIFICATION CHECKLIST

Before finalizing a talk guide:
- [ ] 5 threads cover talk's full doctrinal scope
- [ ] Each thread has distinct hue (no spectral overlap)
- [ ] Every Q&A has exact scripture citations (book/chapter/verse)
- [ ] Cross-refs span all 4 standard works + modern prophets
- [ ] Tier 1 resources are directly on-topic (tithing/consecration/sacrifice)
- [ ] Tier 2 adds historical/typological/linguistic depth
- [ ] Tier 3 podcasts are current season or highly relevant archive
- [ ] Personal anecdote from talk integrated into at least one Q&A
- [ ] Core thesis stated in talk metadata
- [ ] Output validates against JSON/YAML schema