---
name: developer-workflows-management
description: "Manages the Developer Workflows vault category."
---

## Overview
This skill governs the organization and growth of the `Developer Workflows` repository. It ensures all technical documentation (Next.js, Python, Styling) is indexed correctly in the Memory Map.

## Directory Structure
The following standard hierarchy applies to the `Developer Workflows/` folder:

- **NextJS/**: Architecture, Server Components (RSC), Data Fetching, and Middleware patterns.
- **Styling_Tailwind/**: CSS standardizations, Flex/Grid logic, and component tokens.
- **HTML5_Basics/**: Semantic standards, A11y, and fundamental DOM structure.
- **Interactive_Motion/**: Specialized methods for scroll-based animation (Lenis, GSAP), Framer Motion integration, and performance profiling.

## Workflow & Maintenance
### 1. Repository Updates
Whenever a new resource is added to the vault:
1. **Identification:** Research the "Gold Standard" documentation.
2. **Formatting:** Convert to Markdown using:
    *   `| Table |` for comparative analysis/comparisons.
    *   `` ```codeblock``` `` for production-ready, tested snippets.
3. **Reference Tracking:** Ensure a corresponding entry is added to `/Developer Workflows/Memory.md`.

### 2. The Memory Map (`Memory.md`)
The `Memory.md` file behaves as the dashboard of the repository. All new primary categories or significant file additions must be registered here immediately to ensure high discoverability via search tools.

## Success Metrics
- **Standard:** Is the documentation production-ready?
- **Cleanliness:** Does it follow our standard directory structure?
- **Access:** Can this result in a "How-To" for future sessions without further research?
