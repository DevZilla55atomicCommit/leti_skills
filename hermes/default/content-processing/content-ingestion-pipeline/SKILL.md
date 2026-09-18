---
name: content-ingestion-pipeline
description: A meta-workflow skill that processes multi-modal, diverse inputs (PDFs, Images, Videos, Links) by systematically calling free-of-cost native tools and synthesizing them into a single, highly structured Markdown output ready for LLM consumption. This is the primary skill for synthesizing complex information from disparate sources.
---

# Content Ingestion Pipeline (CI-Pipeline) Skill Definition

## Core Purpose:
To execute a resilient, multi-source data pipeline that transforms diverse raw content—whether it's an image, a PDF snippet, or a web article segment—into one unified, highly structured Markdown document optimized for deep analysis and educational synthesis. **This skill is the mandatory workflow manager for all complex content summarization tasks.**

## ⚙️ Execution Protocol (The Three Phases)
When engaged, follow these three sequential phases:

### Phase 1: Input Analysis & Determination
First, analyze all provided inputs to determine their types (File/Text $\rightarrow$ PDF; Visual $\rightarrow$ Image/Video; Remote $\rightarrow$ URL). Log the potential failure points for later resilience.

### Phase 2: Iterative Extraction (The Tool Calling)
Execute specialized tools based on the input type using a specific, free-of-cost internal logic flow:

1.  **For Visual Assets (Images/Videos):** The sole tool required is **`vision_analyze()`**. The prompt to this tool must be extremely detailed in the `question` field (e.g., "Analyze composition, mood, subject details, and technical lighting characteristics...") to maximize descriptive output into Markdown format.
2.  **For Documents/Text Files (PDFs):** Priority is given to free native tools like `read_file`. If dependency failure occurs, the *fallback* procedure is immediately triggered: use the **`vision_analyze()`** tool in a text-mode fallback wrapper on the first page image to capture structural data that plain text extraction misses.
3.  **For Remote Content (URLs/Videos):** Use `web_extract`, `youtube-content`, or other web tools. The raw output is treated as a temporary content buffer, not the final source.

### Phase 3: Synthesis & Structuring (The Final Output)
This is the critical step where intelligence resides. Do **NOT** simply concatenate the tool outputs. You must act as a Master Editor and follow this synthesis mandate:

1.  **Consolidate:** Gather all raw text buffers (Image descriptions, Text extractions, Web summaries).
2.  **Structure:** Reorganize the information into logical Markdown sections using proper headers (`#`, `##`). A recommended default lesson plan flow is:
    *   `# Primary Title:` (Based on source meta-data)
    *   `## Summary of Findings:` (The highest-level take-aways).
    *   `## Detailed Evidence / Components:` (Where image descriptions and raw text are segmented under headings like "Visual Analysis" or "Supporting Text").
    *   `## Critical Synthesis / Lesson Point:` (Your final, synthesized conclusion that connects concepts from different sources).

### 🛑 Error Handling & Resilience Mandate
If *any* tool fails due to an external dependency, permission issue, or API key blockade:
1.  Report the specific failure clearly (e.g., "API Key Missing for YouTube Transcripts").
2.  **Immediately shift focus:** Do not halt the entire process. Report the failure AND then continue processing all other successful inputs/buffers to deliver *the maximum amount of useful Markdown possible*.

---
**Use Case Trigger:** Use this skill whenever a piece of information requires combining textual extraction, visual understanding, and source synthesis into one cohesive narrative.