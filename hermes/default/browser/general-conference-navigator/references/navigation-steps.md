# Navigation Steps for General Conference Talk Extraction

## Session Context
- Target talk: "Prayers for Peace" by Henry B. Eyring (April 2026 General Conference)
- URL pattern: `https://www.churchofjesuschrist.org/study/general-conference/<year>/<slug>?lang=eng`
- Element reference for talk link: `@e75`

## Tool Sequence
1. **Navigate to URL**
   ```bash
   browser_navigate url="https://www.churchofjesuschrist.org/study/general-conference/2026/19eyring?lang=eng"
   ```

2. **Click talk link**
   ```bash
   browser_click ref="@e75"
   ```

3. **Capture full page**
   ```bash
   browser_snapshot full=true
   ```

4. **Extract article text**
   ```bash
   browser_console expression="document.querySelector('main').innerText"
   ```

5. **Save extracted text**
   ```bash
   write_file path="~/.hermes/vault/2026_eyring_prayers_for_peace.txt" content="<paste extracted text here>"
   ```

## Verification Checklist
- Confirm snapshot includes `"Prayers for Peace"` in title.
- Verify extracted text contains the speaker name "Henry B. Eyring".
- Ensure file saved successfully (check exit code `0`).
- Re‑run steps 2‑4 to ensure consistency across captures.

## Common Pitfalls
- **Element shift**: Re‑capture after each click to avoid stale element indices.
- **Partial load**: Always request `full=true` before extraction.
- **URL changes**: Search index page for talk title if structure changes.