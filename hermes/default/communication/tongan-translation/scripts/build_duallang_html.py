#!/usr/bin/env python3
"""Build dual-language Come Follow Me lesson: English prose + official Tongan scripture."""
from pathlib import Path

src = Path("/Users/alfredkamisese/Desktop/Come Follow Me 2026/2026-08-Week4_Psalms_Aug17-23/Psalms_Lesson_Final.html")
out = Path("/Users/alfredkamisese/Desktop/Come Follow Me 2026/2026-08-Week4_Psalms_Aug17-23/Psalms_Lesson_Tongan.html")

html = src.read_text(encoding="utf-8")

tongan_scriptures = {
    '"The Lord is my shepherd; I shall not want."':
        '<em class="to-scripture">KO hoku tauhi a Jihova; e ikai teu majiva. (S\u0101me 23:1)</em>',
    '"The Lord is my shepherd"':
        '<em class="to-scripture">Ko hoku Tauhi a Jihova. (S\u0101me 23:1)</em>',
    '"The Lord is my light and my salvation"':
        '<em class="to-scripture">Ko eku m\u0101ma mo hoku fakamoui a Jihova. (S\u0101me 27:1)</em>',
    '"Unto thee will I cry, O Lord my rock"':
        '<em class="to-scripture">TEU tagi kiate koe, E Jihova ko hoku makatuu. (S\u0101me 28:1)</em>',
    '"Thou art my Son, this day have I begotten thee"':
        '<em class="to-scripture">Ko hoku Alo koe; kuou fakatubu koe i he aho ni. (S\u0101me 2:7)</em>',
    '"My God, my God, why hast thou forsaken me?"':
        '<em class="to-scripture">E HOKU Otua, E hoku Otua, koeha kuo ke liaki ai au? (S\u0101me 22:1)</em>',
    '"Unto thee, O Lord, do I lift up my soul"':
        '<em class="to-scripture">E JIHOVA, oku ou hiki hake hoku laumalie kiate koe. (S\u0101me 25:1)</em>',
    '"Be still and know"':
        '<em class="to-scripture">Mou logo be, bea ilo ko au koe Otua. (S\u0101me 46:10)</em>',
    '"Be still and know I am God"':
        '<em class="to-scripture">Mou logo be, bea ilo ko au koe Otua. (S\u0101me 46:10)</em>',
}

style_add = """
        .to-scripture {
            display: block;
            color: #7a3d1a;
            font-style: italic;
            margin-top: 6px;
            padding: 6px 10px;
            background: #fdf3e7;
            border-left: 3px solid #d4a537;
            border-radius: 0 4px 4px 0;
        }
"""

html = html.replace("</style>", style_add + "\n    </style>", 1)

count = 0
for eng, to in tongan_scriptures.items():
    if eng in html:
        html = html.replace(eng, eng + "<br>" + to, 1)
        count += 1

html = html.replace("lang=" + '"en"', "lang=" + '"to"', 1)

note_parts = [
    '<div style="background:#fff8e6;border:2px dashed #d4a537;padding:12px 16px;margin:15px 0;border-radius:8px;">',
    '<strong>Ko e l\u0113soni \u02bbi he lea faka-Tonga mo e lea faka-p\u0101langi:</strong>',
    'Ko e konga S\u0101me \u02bboku \u02bbi he lea faka-Tonga (mei he Tohi Tabu ofisa).',
    'Ko e fakamatala \u02bbo e akonaki \u02bboku kei \u02bbi he lea faka-p\u0101langi.',
    '<br><em>(Bilingual: scripture in official Tongan; teaching prose in English pending full translation.)</em>',
    '</div>',
]
note = "\n".join(note_parts)

old_body = "<body>\n    <div class=" + '"page"' + ">"
new_body = "<body>\n    <div class=" + '"page"' + ">\n" + note + "\n"
html = html.replace(old_body, new_body, 1)

out.write_text(html, encoding="utf-8")
print("Applied", count, "official Tongan scripture quotations.")
print("Note present:", note.splitlines()[1].strip() in html)
print("lang=to:", 'lang="to"' in html)
print("Saved:", out)