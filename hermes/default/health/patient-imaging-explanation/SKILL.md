---
name: patient-imaging-explanation
description: Explain imaging reports to patients with risk tables, PDFs.
trigger: User provides imaging report asking for plain-language explanation or risk assessment.
---

## Patient-Facing Imaging Explanation Workflow

### When to Use
- User is the patient asking to understand their own imaging results
- User needs risk assessment, timeline if untreated, concrete next steps
- User wants a printable PDF for appointments

### Core Principle
**Translate radiology jargon → plain English → actionable plan.** Never leave the patient wondering "so what do I do?"

---

## Workflow Steps

### 1. Extract & Parse the Report
- Read report text (image OCR, PDF extraction, or user paste)
- Identify: exam type, indication, technique, findings, impression, radiologist
- **Critical:** Capture exact measurements, laterality, qualitative descriptors

### 2. Build Plain-Language Findings Table
| Area | Radiology Result | Plain English Meaning |
|------|------------------|----------------------|
| Liver | Unremarkable | Normal — nothing to worry about |
| Right pelvis | 7 cm cystic mass, calcified rim | Giant aneurysm — main pelvic artery has 7 cm bulge |

**Define every radiology term used** (see Reference Glossary below).

### 3. Risk Stratification by the Numbers
**Always include a size-risk table** when measurements exist.

Example for internal iliac artery aneurysm:
| Category | Diameter | Annual Rupture Risk | Standard of Care |
|----------|----------|---------------------|------------------|
| Normal | 4–6 mm | ~0% | None |
| Small | < 2 cm | < 2% | Surveillance q6–12mo |
| Medium | 2–3 cm | 2–5% | Individualized |
| Large | 3–5 cm | 5–15%+ | Repair recommended |
| **Giant** | **> 5 cm** | **20–40%+** | **Urgent repair** |
| **Patient** | **7 cm** | **VERY HIGH** | **Emergency repair** |

Cite guideline sources (SVS, SIR, ACC/AHA).

### 4. Timeline: If Left Untreated
Walk through natural history:
- **Now:** Current state, symptom correlation
- **Days/weeks:** Wall stress increases (Laplace's Law: T = P × r)
- **Weeks/months:** Growth, possible sentinel bleed
- **Rupture event:** Clinical presentation, mortality
- **Emergency surgery:** What happens, mortality
- **Elective repair (if done now):** Procedure, mortality, recovery

### 5. Action Plan with Deadlines
| Step | Action | Deadline | Owner |
|------|--------|----------|-------|
| 1 | Call ordering doctor for urgent referral | **TODAY** | Patient |
| 2 | Specialist orders confirmatory imaging (CTA) | **THIS WEEK** | Specialist |
| 3 | Surgery scheduled (endovascular preferred) | **WITHIN 2 WEEKS** | Surgeon |
| 4 | Activity restrictions | **IMMEDIATELY** | Patient |

### 6. Exact Questions for Specialist Visit
Give 8–10 verbatim questions:
1. "You've seen the [X cm] measurement — do you agree?"
2. "What is the exact maximum diameter on your measurement?"
3. "Is this a true aneurysm or pseudoaneurysm?"
4. "Can this be fixed endovascularly (coils/stent via groin)?"
5. "If endovascular isn't possible, what's the open surgery plan?"
6. "How soon can we schedule? I need this within 2 weeks."
7. "Should I be on bed rest or just activity restriction until surgery?"
8. "What blood pressure target?" (Typically <130/80)
9. "Do I need a CTA or is this imaging enough for planning?"
10. "What is your personal experience with [condition] repair?"

### 7. Emergency Symptoms (Condition-Specific)
Red-flag list with "Call 911 if..." — tailored to the pathology.

### 8. Output Formats
**Always provide:**
1. **Chat response** — structured, scannable, immediate
2. **PDF report** — formatted, color-coded, multi-page, printable

**PDF Generation:** Use `execute_code` + `reportlab`
- Title with critical banner if urgent
- Tables with color coding (red = urgent, green = safe, yellow = caution)
- Page breaks handled automatically
- Emergency symptoms highlighted
- Footer with disclaimer

---

## Reference Glossary: Radiology Terms → Plain English

| Radiology Term | Plain English | Worry Level |
|----------------|---------------|-------------|
| Unremarkable / Normal / Within normal limits | "Looks fine, nothing to see here" | ✅ Good |
| No acute abnormality | "Nothing urgent or dangerous" | ✅ Good |
| Hypoattenuating / Hypodense | "Darker/less dense — usually a benign cyst (fluid sac)" | 🟡 Usually benign |
| Hyperattenuating / Hyperdense | "Brighter/more dense — could be blood, calcium, or contrast" | 🟡 Context-dependent |
| Enhancing / Enhancement | "Lights up with IV contrast = solid tissue with blood supply" | 🟡 Needs context |
| Non-enhancing | "Doesn't light up = likely fluid/cyst" | ✅ Usually benign |
| Lymphadenopathy | "Enlarged lymph nodes (>1 cm)" | 🟡 Infection, inflammation, or cancer spread |
| Fat stranding / Fat haziness | "Fuzzy fat = inflammation spreading through fat" | 🟡 Sign of nearby problem |
| Free fluid / Pelvic fluid | "Fluid where it shouldn't be" | 🟡 Small = normal; Large = concern |
| Hydronephrosis | "Kidney swollen with backed-up urine = blockage" | 🔴 Needs urology |
| Wall thickening | "Organ wall abnormally thick" | 🟡 Infection, inflammation, tumor |
| Mass / Lesion / Nodule | "A lump/spot — non-specific term" | 🟡 Always needs context |
| Indeterminate | "Can't tell what this is on this scan alone" | 🟡 → Get another test |
| Stable | "Same as last scan" | ✅ Very good |
| Progressive / Increasing / Enlarging | "Getting bigger/worse" | 🔴 Concerning |
| Aggressive osseous lesion | "Bone destruction that looks like cancer" | 🔴 Urgent oncology |
| Lytic / Sclerotic | Bone eaten away / extra bone laid down | 🟡 Context-dependent |

---

## Aneurysm-Specific Knowledge (Internal Iliac)

### Physics
- **Laplace's Law**: Wall Tension = Pressure × Radius
- At 7 cm radius → tension ~12–17× normal
- Pelvis = rigid closed box → rupture = instant venous compression → cardiac collapse

### Size Thresholds (Internal Iliac Artery)
| Category | Diameter | Rupture Risk/yr | Action |
|----------|----------|-----------------|--------|
| Normal | 4–6 mm | ~0% | None |
| Small | < 2 cm | < 2% | Surveillance |
| Medium | 2–3 cm | 2–5% | Individualized |
| Large | 3–5 cm | 5–15%+ | Repair recommended |
| Giant | > 5 cm | 20–40%+ | **Urgent repair** |

### Mortality Data
- Elective endovascular: **< 1–2%**
- Elective open: **2–5%**
- Emergency post-rupture: **40–70%**
- No treatment (rupture at home): **> 90%**

### Repair Options
1. **Endovascular coil embolization** (preferred) — groin puncture, coils block flow into sac
2. **Endovascular stent-graft** — excludes aneurysm from circulation
3. **Open surgical ligation** — backup if endovascular fails

---

## Tools & Patterns

| Task | Tool |
|------|------|
| PDF text extraction | `execute_code` + `pdfplumber` / `PyMuPDF` |
| Image OCR | `computer_use` with Preview app |
| Literature search | `web_search` / `browser_navigate` to NCBI/StatPearls |
| PDF generation | `execute_code` + `reportlab` |
| Anatomical diagrams | Text-based tables (ASCII) in chat; reportlab tables in PDF |

---

## Pitfalls to Avoid

- ❌ Don't diagnose — only explain findings and correlate with symptoms
- ❌ Don't recommend specific medications/dosing
- ❌ Don't minimize findings the radiologist flagged
- ❌ Don't use medical jargon without defining it
- ❌ Don't give false reassurance on large aneurysms (>3 cm internal iliac)
- ❌ Don't skip the "what happens if untreated" timeline
- ❌ Don't omit exact questions for the specialist
- ❌ Don't forget emergency symptoms list
- ❌ Don't output only chat — always offer PDF when user wants it
- ✅ Always flag: "Discuss with your treating physician/specialist"
- ✅ Always include red-flag symptoms for ED
- ✅ Always provide exact questions for the specialist visit
- ✅ Generate PDF when user asks — formatted, printable, complete
- ✅ State uncertainties explicitly ("radiologist wasn't certain")
- ✅ Distinguish: "explains symptoms" vs "incidental" vs "unknown significance"

---

## Example Output Structure (Chat)

```
## Your [Exam] Report — Plain Language Summary

### The Scan
[Exam type, indication, key facts]

### What They Found (table)
[Area | Result | Plain English]

### The Bottom Line
[1-sentence conclusion]

### What This Means for You
[Anatomy, condition explanation, reassuring/concerning details]

### 🔴 / 🟡 / 🟢 Risk Assessment
[Color-coded urgency]

### If Untreated — Timeline
[Now → Rupture → Emergency vs. Elective]

### Mortality Numbers
[Table: Elective vs Emergency vs None]

### Immediate Action Plan
[Table with deadlines]

### Questions for Your [Specialist]
[Numbered verbatim questions]

### 🚨 Emergency Symptoms
[Bulleted red flags with "Call 911 if..."]
```

---

## PDF Template Structure

1. **Title page** — Critical banner if urgent, patient name (redacted), date, size
2. **Scan details** — Table
3. **Findings** — Color-coded table (key finding highlighted)
4. **What X cm Means** — Size-risk table with patient row highlighted
5. **If Untreated Timeline** — Table with risk levels
6. **Mortality Numbers** — Table with color-coded rates
7. **Why This Size Is Different** — Physics, anatomy, guidelines
8. **Action Plan** — Steps with deadlines
9. **Questions for Surgeon** — Numbered list
10. **Emergency Symptoms** — Red-highlighted
11. **Summary** — One bold sentence
12. **Footer** — Source, disclaimer, generation info