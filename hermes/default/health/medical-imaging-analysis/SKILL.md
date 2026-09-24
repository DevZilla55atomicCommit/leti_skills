---
name: medical-imaging-analysis
description: Analyze imaging PDFs, correlate findings to symptoms.
trigger: User provides imaging reports asking for interpretation or symptom correlation.
---

## Medical Imaging Analysis Workflow

### 1. Extract & Parse Reports
- Use `execute_code` + `pdfplumber` to extract full text from PDF reports
- Capture: study type, date, clinical indication, comparison, findings, impression, reading physicians
- Preserve exact measurements, laterality, qualitative descriptors ("string sign", "patent", "stenosis vs occlusion")

### 2. Build Anatomical Map
- Create table mapping each venous/arterial/organ segment across all studies
- Note discrepancies between reports (different radiologists, phases)
- Track: patency, stenosis severity, measurements, thrombus vs valve vs artifact

### 3. Correlate Findings to Symptoms
- Map each abnormal finding to the anatomical territory it drains/supplies
- Example: Right IJV stenosis → right face/neck/scalp/orbit edema
- Distinguish primary vs compensatory findings (collaterals = compensation)

### 4. Determine Etiology & Chronicity
- Use clinical history (prior access, surgery, catheters, trauma) to infer cause
- Compare with prior imaging: stable = chronic/fibrotic; new = acute/thrombotic
- "String sign" = chronic fibrotic stenosis with patent lumen

### 5. Research Evidence Base (when needed)
- Search NCBI Bookshelf/StatPearls for pathophysiology, management guidelines
- Key searches: "[vessel] stenosis treatment", "[condition] endovascular management", "KDOQI venous stenosis"
- Prioritize guidelines (KDOQI, SIR, SVS) over case reports

### 6. Produce Structured Output
**Always include:**
- Executive summary table (findings + significance)
- Anatomical drainage map (text-based diagram)
- Symptom-to-finding correlation table
- Severity assessment (acute danger? SVC syndrome risk? transplant impact?)
- Concrete next steps (specialist referral, specific tests, conservative measures)
- Red flags for urgent care
- One-paragraph provider summary for referral

### 7. Communication Style
- Direct, technical but accessible
- No false reassurance; state uncertainties explicitly
- "Unverified" if imaging finding not confirmed by gold standard
- Distinguish: "explains symptoms" vs "incidental" vs "unknown significance"

---

## Tools & Patterns

| Task | Tool |
|------|------|
| PDF text extraction | `execute_code` + `pdfplumber` |
| Multi-study correlation | Manual table building in analysis |
| Literature search | `browser_navigate` to NCBI Bookshelf/StatPearls |
| Anatomical reference | StatPearls anatomy chapters |
| Guideline lookup | Search "[society] guideline [condition]" |

---

## Pitfalls to Avoid

- ❌ Don't diagnose — only correlate imaging findings with symptoms
- ❌ Don't recommend specific medications/dosing
- ❌ Don't minimize findings the radiologist flagged
- ❌ Don't assume "stable since 2021" = benign (symptoms may be new)
- ❌ Don't skip collateral assessment — they explain "unexpected" symptom locations
- ✅ Always flag: "Discuss with your treating physician/specialist"
- ✅ Always include red-flag symptoms for ED