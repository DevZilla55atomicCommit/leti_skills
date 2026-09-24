---
name: provider-research-pattern
description: Research lockable container options on provider sites.
category: desktop
---

# Provider Research Pattern (Lockable Container Inquiry)

When the user needs to query a waste‑service provider (e.g., Recology San Mateo County) to discover:
- lockable dumpster / container options (keypad / code access)
- monthly pricing / fee structure
- contact details for commercial/multi‑family sales
- compliance documentation (AB 1826, AB 341, SB 1383)

follow this standardized **browser‑first workflow**. The pattern was distilled from the Menlo Park (1165‑1169 Willow Rd) investigation on 2026‑07‑27.

## 1. Navigate to Provider Contact Page
```text
browser_navigate URL: <provider_contact_url>
browser_snapshot capture_after=true   # verify landing page loads
```

## 2. Locate & Click “Contact Us” / “Sales” Link
- Identify the link element by its AX index (`ref=<eN>`) from the snapshot.
- Click with `browser_click ref=<eN>`.
- **Verify** the click succeeded (`effect: 'confirmed'`) and capture again to expose the contact details section.

## 3. Extract Core Contact Information
- Use `read_file` on any linked PDF/CSV or extract phone numbers from the captured snapshot.
- Typical phone: `650‑595‑3900`; Manager: `Marcus Mirt`.

## 4. Search Provider Site for Specific Keywords
- Construct query URLs (e.g., `https://www.recology.com/search/?q=lockable%20container`).
- Repeat steps 1‑3 for each result page.
- Scan page headings for “Lockable”, “Compost”, “Commercial”, “Multi‑Family”.

## 5. Verify Container Options & Pricing
- Look for explicit mention of **lockable containers**, **keypad access**, **security**, or **restricted use**.
- Note container **size** (2 yd, 3 yd, 4 yd, 6 yd) and **pickup frequency** (1×/wk, 2×/wk, etc.).
- Record **monthly rate** if listed, or flag “price on request – call sales”.

## 6. Capture & Store Findings
- Save phone numbers, URLs, and any PDFs to `references/` sub‑directory for future retrieval.
- Add a concise markdown entry in `references/provider‑notes.md` summarizing:
  - Provider name
  - Service area (e.g., Menlo Park, CA)
  - Confirmed lockable container availability
  - Pricing model (flat fee, variable, request‑quote)
  - Contact person & phone

## 7. Pitfalls & Auto‑Recovery
- **AJAX‑loaded content** – wait for dynamic elements; use `browser_snapshot` after 2‑3 s.
- **Scroll‑hidden links** – invoke `browser_scroll direction=down` before clicking.
- **Cookie banners** – dismiss programmatically (`browser_click` on dismiss button) before capture.
- **Element index shifts** after locale or language change – re‑capture and re‑click with new indices.
- **Background Unavailable** – if an action returns `effect: 'suspected_noop'` or `code: 'background_unavailable'`, re‑navigate and retry with a fresh snapshot.

## 8. Verification Checklist

- [ ] Click executed without `effect: 'suspected_noop'` or `code: 'background_unavailable'`.
- [ ] Post‑click capture shows the expected element (e.g., phone number, address, manager name).
- [ ] All subsequent steps use refreshed element indices from a fresh `browser_snapshot`.
- [ ] No stray pop‑ups remain (e.g., consent dialogs); close them if needed before proceeding.

## 8. Example Session (Recology San Mateo County)

```text
1. browser_navigate URL: https://www.recology.com/recology-san-mateo-county/contact/
2. browser_snapshot capture_after=true  # verify landing page
3. browser_click ref: e18  # click “Contact Us”
4. browser_snapshot capture_after=true  # verify contact details
5. read_file path: /tmp/phone.txt   # extract 650‑595‑3900
6. # optionally search for lockable containers
7. browser_navigate URL: https://www.recology.com/search/?q=lockable%20container
8. ... repeat capture/click pattern as needed
```

## 9. References (Session‑Specific)

- **Recology San Mateo County Contact Page**: https://www.recology.com/recology-san-mateo-county/contact/
- **lockable container search results**: https://www.recology.com/search/?q=lockable%20container
- **DuckDuckGo search for lockable container**: https://duckduckgo.com/?q=Recology+San+Mateo+County+lockable+container+commercial

--- 

*This skill is intentionally generic; replace placeholder URLs and indices with the concrete values observed in each provider’s page. The workflow scales to any commercial waste‑service or municipal provider search.*