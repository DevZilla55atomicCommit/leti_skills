#!/usr/bin/env python3
"""
Build the Tongan version of the Come Follow Me HTML lesson
using the translations we have.
"""

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Load translations
with open('/Users/alfredkamisese/tongan_translations_final.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Load original HTML
with open('/Users/alfredkamisese/Desktop/Come Follow Me 2026/2026-08-Week4_Psalms_Aug17-23/Psalms_Lesson_Final.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Update lang attribute
html_tag = soup.find('html')
if html_tag:
    html_tag['lang'] = 'to'

# Helper to replace text in an element
def replace_text(element, new_text):
    """Replace all text in an element while preserving child tags."""
    if element.string:
        element.string.replace_with(new_text)
    else:
        # Clear and add new text
        for child in list(element.children):
            if isinstance(child, str):
                child.replace_with('')
        element.append(new_text)

# Apply translations
# Title
title_tag = soup.find('title')
if title_tag:
    title_tag.string = f"[ESCALATED] {title_tag.string}"  # Title wasn't translated

# Main h1
h1 = soup.find('h1')
if h1:
    replace_text(h1, translations['title'])

# Subtitles (p.subtitle)
subtitles = soup.find_all('p', class_='subtitle')
if len(subtitles) >= 3:
    replace_text(subtitles[0], translations['subtitle1'])
    replace_text(subtitles[1], translations['subtitle2'])
    replace_text(subtitles[2], translations['subtitle3'])

# Section headings h2
for h2 in soup.find_all('h2'):
    text = h2.get_text(strip=True)
    if text == 'The Psalms in Three Sentences':
        replace_text(h2, translations['section1'])
    elif text == 'The Core Message':
        replace_text(h2, 'Core Message')  # Will translate
    elif text == 'Every Question from the Lesson — Answered Simply':
        replace_text(h2, 'Every Question from the Lesson — Answered Simply')  # Need translation
    elif text == 'Scripture Helps (Extra Questions from Lesson)':
        replace_text(h2, 'Scripture Helps (Extra Questions from Lesson)')
    elif text == 'Ideas for Teaching Children':
        replace_text(h2, 'Ideas for Teaching Children')
    elif 'Podcast' in text:
        replace_text(h2, 'Podcast Insights for This Week')
    elif 'BYU Studies' in text:
        replace_text(h2, 'BYU Studies Articles for Deeper Study')
    elif 'One-Page Cheat Sheet' in text:
        replace_text(h2, 'One-Page Cheat Sheet for Class')
    elif 'Simple Answer' in text:
        replace_text(h2, 'Simple Answer for Your Class')

# Key points (div.key-point)
key_points = soup.find_all('div', class_='key-point')
key_texts = ['key1', 'key2', 'key3']
for i, kp in enumerate(key_points):
    if i < len(key_texts):
        kp.clear()
        kp.append(translations[key_texts[i]])

# Core message (div.takeaway-box - first one)
takeaway = soup.find('div', class_='takeaway-box')
if takeaway:
    # Find the p tag inside
    p = takeaway.find('p')
    if p:
        p.clear()
        p.append(translations['core_msg'])

# Question boxes
question_boxes = soup.find_all('div', class_='question-box')
q_keys = ['q1', 'q2', 'q3', 'q4']
a_keys = ['a1', 'a2', 'a3', 'a4']

for i, qb in enumerate(question_boxes):
    if i < len(q_keys):
        # Question
        q_elem = qb.find('div', class_='question-text')
        if q_elem:
            q_elem.clear()
            q_elem.append(translations[q_keys[i]])
        
        # Answer
        a_elem = qb.find('div', class_='answer-text')
        if a_elem:
            a_elem.clear()
            a_elem.append(translations[a_keys[i]])

# Cheat sheet cards
cheat_cards = soup.find_all('div', class_='cheat-card')
cheat_keys = ['cheat1', 'cheat2', 'cheat3', 'cheat4', 'cheat5', 'cheat6', 
              'cheat7', 'cheat8', 'cheat9', 'cheat10', 'cheat11', 'cheat12']

for i, card in enumerate(cheat_cards):
    if i < len(cheat_keys):
        q_elem = card.find('div', class_='cheat-question')
        a_elem = card.find('div', class_='cheat-answer')
        
        # Split the translation into question and answer
        full = translations[cheat_keys[i]]
        if '?' in full:
            q_part, a_part = full.split('?', 1)
            q_part += '?'
            a_part = a_part.strip()
        else:
            q_part = full
            a_part = ''
        
        if q_elem:
            q_elem.clear()
            q_elem.append(q_part)
        if a_elem:
            a_elem.clear()
            a_elem.append(a_part)

# Takeaway box at the end (second one)
takeaway_boxes = soup.find_all('div', class_='takeaway-box')
if len(takeaway_boxes) > 1:
    p = takeaway_boxes[1].find('p')
    if p:
        p.clear()
        p.append('[Tongan translation needed] The Psalms are a playlist for every season — they give us words when we have none. Whether we\'re praising, lamenting, trusting, or doubting, the Psalms meet us there and point us to the Shepherd who provides, guides, protects, and pursues us with goodness and mercy all our days.')

# Save
output_path = '/Users/alfredkamisese/Desktop/Come Follow Me 2026/2026-08-Week4_Psalms_Aug17-23/Psalms_Lesson_Tongan.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(str(soup.prettify()))

print(f"Saved to {output_path}")