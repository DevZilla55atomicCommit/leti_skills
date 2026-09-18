# USCIS Alerts Monitoring Workflow

## Overview
Systematically monitor USCIS Newsroom alerts for immigration policy updates, court rulings, and policy changes.

## Step-by-Step Process

1. **Initial Load**
   - Open browser to `https://www.uscis.gov/newsroom/alerts`
   - Capture full page snapshot with `browser_snapshot(full=true)`
   - Identify all article elements using ref IDs

2. **Content Extraction**
   - For each article link (e.g., `@e70`, `@e71`), click and capture snapshot
   - Extract key fields:
     - Release Date (`time` element)
     - Headline (`heading` element)
     - Summary Text (`paragraph` elements)
     - Key Policy Details (bulleted lists)
     - Related Links

3. **Structured Logging**
   - Create markdown entry in vault with frontmatter:
     ```yaml
     ---
     date: YYYY-MM-DD
     title: [Short Summary]
     type: uscis-alert
     tag: [policy-category]
     ---
     ## Summary
     [Concise summary of announcement]
     
     ## Details
     - **Release Date**: [Date]
     - **Key Policies**: [Bullet list]
     - **Related Initiatives**: [Links]
     
     ## Source
     [URL and screenshot reference]
     ```

4. **Archive & Reference**
   - Save full HTML snapshot to `archives/uscis-alerts/YYYY-MM-DD.html`
   - Add entry to `uscis-alerts-index.md` with:
     - Date
     - Title
     - Link to full snapshot
     - Tags

5. **Daily Check**
   - Repeat steps 1-4 each business day
   - Filter for new content using date comparison
   - Flag items requiring follow-up (e.g., "Court Order", "New Policy")

## Key Element Selectors
- Article Container: `article` tag within main content
- Headline: `heading` elements with level 1-3
- Date: `time` element with `datetime` attribute
- Summary: `paragraph` elements immediately following headline
- Bullet Lists: `list` elements with `ListMarker` items
- Related Links: `link` elements with `href` attributes

## Example Captured Structure
```html
<article>
  <heading level="1" ref="e59">Court Issues Administrative Stay...</heading>
  <time ref="e63">07/23/2026</time>
  <paragraph>On July 21, 2026, the U.S. District Court...</paragraph>
  <list>
    <listitem>• Portion of July 2025 FRN</listitem>
    <listitem>• March 2026 website Update</listitem>
    <listitem>• April 2026 IFR</listitem>
  </list>
</article>
```