# Come Follow Me Study Guide Template — API Reference

## Overview

The `study-guide-template.html` is a **mobile-first, interactive HTML template** for Come Follow Me weekly study guides. It's designed to be:

- **Single-file** — no external dependencies (CDN-free)
- **Mobile-first** — 16pt+ base font, 48px tap targets, single column
- **Interactive** — collapsible sections, dark/light mode, localStorage reflections
- **Print-ready** — beautiful PDF output via browser print
- **Deep-linkable** — Gospel Library (churchofjesuschrist.org) links throughout

---

## Integration Pattern

Helios (cron job) → generates lesson data JSON → runs `generate_study_guide.py` → outputs HTML to:
- `~/Desktop/Elders Quorum Lessons 2025.2026/2026/04/Teacher Lessons/`
- `~/Desktop/Elders Quorum Lessons 2025.2026/2026/04/Personal Study/`

---

## Data Schema (JSON)

```json
{
  "lessonId": "2026-04-week-14",
  "title": "\"Yet Will I Trust in Him\"",
  "weekDate": "April 5–11, 2026",
  "scriptures": "Job 1–3; 12–14; 19; 21–24; 38–40; 42",
  "scripture": "<p>Full scripture text or summary...</p>",
  "commentary": "<p>Commentary with insights from followHIM, BYU Studies, etc.</p>",
  "application": "<p>Personal application prompts and action items.</p>",
  "scriptureLinks": [
    { "label": "Job 1–3 (Gospel Library)", "url": "https://www.churchofjesuschrist.org/study/scriptures/ot/job/1?lang=eng" },
    { "label": "BYU Studies — Job", "url": "https://byustudies.byu.edu/come-follow-me/old-testament/33" }
  ],
  "commentaryLinks": [
    { "label": "followHIM Podcast — Job", "url": "https://followhim.co/old-testament-2026" },
    { "label": "Scripture Insights — Job", "url": "https://www.youtube.com/@ScriptureInsights" }
  ],
  "applicationLinks": [
    { "label": "Personal Study Guide", "url": "https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-individuals-and-families" }
  ],
  "generationDate": "April 5, 2026",
  "personal": false
}
```

### Field Descriptions

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `lessonId` | ✅ | string | Unique identifier (used for localStorage key) |
| `title` | ✅ | string | Lesson title (shown in header & toolbar) |
| `weekDate` | ✅ | string | Week range display |
| `scriptures` | ✅ | string | Scripture references (displayed in meta) |
| `scripture` | | string | HTML content for Scripture section |
| `commentary` | | string | HTML content for Commentary section |
| `application` | | string | HTML content for Application section |
| `scriptureLinks` | | array | Deep links for Scripture section |
| `commentaryLinks` | | array | Deep links for Commentary section |
| `applicationLinks` | | array | Deep links for Application section |
| `generationDate` | | string | Auto-filled if omitted |
| `personal` | | boolean | Personal vs Teacher mode (affects filename) |

---

## JavaScript API: `window.CFMTemplate`

The template exposes a global API for programmatic control:

### `CFMTemplate.setLessonData(data)`

Injects lesson data into the template. Call after DOMContentLoaded.

```javascript
window.CFMTemplate.setLessonData({
    title: "Lesson Title",
    weekDate: "April 5–11, 2026",
    scriptures: "Job 1–3; 12–14...",
    scripture: "<p>Content...</p>",
    commentary: "<p>Content...</p>",
    application: "<p>Content...</p>",
    scriptureLinks: [{ label: "Link", url: "https://..." }],
    commentaryLinks: [{ label: "Link", url: "https://..." }],
    applicationLinks: [{ label: "Link", url: "https://..." }],
    lessonId: "2026-04-week-14"
});
```

### `CFMTemplate.getReflections()`

Returns saved reflection data from localStorage.

```javascript
const reflections = window.CFMTemplate.getReflections();
// { "reflection-input-1": "My thoughts...", "reflection-input-2": "..." }
```

### `CFMTemplate.clearReflections()`

Clears all reflection data for current lesson.

```javascript
window.CFMTemplate.clearReflections();
```

---

## localStorage Schema

Reflections are auto-saved per lesson:

```
Key: cfm_study_guide_[lessonId]
Value: {
  "reflection-input-1": "What impressed you most...",
  "reflection-input-2": "How can you apply this...",
  "reflection-input-3": "What questions do you have..."
}
```

---

## Section Structure

The template has 4 collapsible sections (in order):

1. **Scripture** (`section-scripture`) — Scripture passage + Gospel Library links
2. **Commentary** (`section-commentary`) — Insights, podcast links, scholarly resources
3. **Reflection** (`section-reflection`) — 3 prompted textarea inputs (auto-saved)
4. **Application** (`section-application`) — Action items, personal application

Each section:
- Has a unique `id="section-{name}"`
- Has `aria-labelledby` pointing to its header
- Content region has `role="region"` with `aria-label`
- Toggle button has `aria-expanded` and `aria-controls`

---

## Deep Link Format

Deep links use the `.deep-link` component:

```html
<a href="https://www.churchofjesuschrist.org/study/scriptures/ot/job/1?lang=eng" 
   class="deep-link" target="_blank" rel="noopener" role="listitem">
    <svg>...</svg>
    Job 1 (Gospel Library)
</a>
```

**Requirements:**
- `target="_blank" rel="noopener"` for external links
- `role="listitem"` inside container with `role="list"`
- Minimum 48px height (tap target)
- Icon + label format

---

## Gospel Library URL Patterns

| Content Type | URL Pattern |
|--------------|-------------|
| Old Testament | `https://www.churchofjesuschrist.org/study/scriptures/ot/[book]/[chapter]?lang=eng` |
| New Testament | `https://www.churchofjesuschrist.org/study/scriptures/nt/[book]/[chapter]?lang=eng` |
| Book of Mormon | `https://www.churchofjesuschrist.org/study/scriptures/bofm/[book]/[chapter]?lang=eng` |
| D&C | `https://www.churchofjesuschrist.org/study/scriptures/dc-testament/dc/[section]?lang=eng` |
| Pearl of Great Price | `https://www.churchofjesuschrist.org/study/scriptures/pgp/[book]/[chapter]?lang=eng` |
| General Conference | `https://www.churchofjesuschrist.org/study/general-conference/[year]/[month]/[speaker]?lang=eng` |
| Come Follow Me Manual | `https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-individuals-and-families/[year]/[week]?lang=eng` |
| BYU Studies | `https://byustudies.byu.edu/come-follow-me/[volume]/[lesson-number]` |

---

## CSS Custom Properties (Theming)

All colors/spacing controlled via CSS variables:

```css
:root {
  --bg-primary: #fdfbf7;
  --bg-secondary: #ffffff;
  --bg-tertiary: #f5f0e8;
  --bg-card: #ffffff;
  --bg-toolbar: rgba(255, 255, 255, 0.95);
  --text-primary: #1a3c5e;
  --text-secondary: #2c5f7c;
  --text-muted: #5a7a8a;
  --accent-primary: #d4a537;
  --accent-secondary: #b8952e;
  --accent-light: #fef9f0;
  --border-color: #e8e0d4;
  --font-base: 16px;        /* Scales up on larger screens */
  --tap-target: 48px;       /* Minimum touch target */
  --toolbar-height: 60px;   /* Fixed header height */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
}

[data-theme="dark"] {
  --bg-primary: #0f1a22;
  --bg-secondary: #15232d;
  /* ... dark overrides ... */
}
```

---

## Print/PDF Output

The template includes `@media print` styles for beautiful PDF generation:

- Toolbar, TOC, toggles, textareas **hidden**
- Sections expanded (`display: block !important`)
- Serif font stack, proper margins
- Colorful accent bars preserved
- Page breaks optimized (`break-inside: avoid`)

**To generate PDF:** Open HTML in browser → Print → Save as PDF

---

## Accessibility Features

- Semantic HTML5 (`header`, `main`, `section`, `nav`, `footer`)
- ARIA labels, roles, and states throughout
- Focus visible states on all interactive elements
- `prefers-reduced-motion` support
- `prefers-contrast: high` support
- Keyboard navigation (Escape closes TOC)
- Screen reader announcements for saved reflections
- Sufficient color contrast (WCAG AA)

---

## Browser Support

- iOS Safari 14+
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

Uses only modern, widely-supported features:
- CSS Custom Properties
- Flexbox/Grid
- IntersectionObserver
- localStorage
- `matchMedia` for dark mode

---

## Cron Job Integration (Helios)

```bash
# Monday 7 AM PDT cron entry
0 7 * * 1 /usr/bin/python3 /path/to/generate_study_guide.py \
  --data /path/to/lesson_data.json \
  --output-dir ~/Desktop/Elders\ Quorum\ Lessons\ 2025.2026/2026/04/Teacher\ Lessons

0 7 * * 1 /usr/bin/python3 /path/to/generate_study_guide.py \
  --data /path/to/lesson_data.json \
  --output-dir ~/Desktop/Elders\ Quorum\ Lessons\ 2025.2026/2026/04/Personal\ Study \
  --personal
```

---

## File Structure

```
come-follow-me-study-guide/
├── templates/
│   └── study-guide-template.html    # Main template (this file)
├── scripts/
│   └── generate_study_guide.py      # Generator script
├── references/
│   ├── byu-studies-url-pattern.md
│   ├── podcast-source-list.md
│   └── lesson-template.md
└── TEMPLATE_API.md                  # This document
```