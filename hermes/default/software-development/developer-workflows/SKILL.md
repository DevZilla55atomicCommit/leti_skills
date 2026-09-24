---
name: developer-workflows
description: Professional software engineering and web development workflow management.
tags: [web-dev, nextjs, python, automation, architecture]
---

# Developer Workflows

This skill governs the engineering standards for our joint-development projects within the **Developer Workflows** directory. It ensures that all solutions are production-ready, scalable, and optimized for high performance (Low Latency / High Fidelity).

## Software Engineering Mandates
*   **Focus:** Strictly Web Development & Software Architecture. 
*   **Media Separation:** Videography/Photography concepts should only be addressed when they directly impact the technical implementation of a web feature (e.g., 'How to stream an MP4 efficiently').
*   **Development Depth:** Prioritize architectural integrity, state management (TanStack Query / Zustand), and API design over surface-level tutorials.

## Categories of Expertise
1.  **State & Data Plumbing:** Management of server vs client state, real-time data synchronization, and local cache invalidation.
2.  **Interactive Motion Engineering:** High-performance scroll interactions (Lenis, GSAP) utilizing hardware acceleration and smooth 60fps execution.
3.  **Platform Standards:** Implementation of Next.js App Router best practices, Tailwind CSS Design Systems, and accessible HTML5 structures.
4.  **Automation & Scripting:** Python-driven task automation for data retrieval, media conversion (strictly for technical use), and developer utility scripts.

## Execution Rituals

**When encountering terminal/tool failures, escalate in this order:**
1. **write_file FIRST** — Direct file writing works 100% while terminal fails interactively (syntax issues causing command loops)
2. **browser_navigate/visual inspection** — Tools work when used directly vs via delegation layers
3. **Fallback strategy**: Use write_file → browser_snapshot → verify syntax → test

*    **The "Best Practices" Standard:** Every file added to the library must include a "Best Practice" section or "Pro-Tip," specifically highlighting common pitfalls found in high-traffic production environments.
*    **Technical Integrity Check:** All code snippets must be valid, modern (Next.js/Python 3.x), and tested for standard performance bottlenecks like "re-renders" or "blocking calls."

## Interaction Guidelines (Professional Focus)
When requested to provide a solution:
- **Primary Goal:** Direct execution. Provide the technical path immediately, then offer the reasoning.
- **Accuracy over Verbosity:** Be targeted. Avoid unnecessary fluff. If a specific command is needed, deliver it; if an architecture is required, explain the *why* before the *how*.
- **Proactive Measurement:** For any "Awwwards" level design request, always mention performance implications (Core Web Vitals) for that specific motion or layout.

---

## Workflow Modules (Directory Structure)
The library is organized into following high-level umbrellas:
1.  **NextJS/HTML5 Foundations**
2.  **Styling_Tailwind**
3.  **Interactive_Motion**
4.  **State_Management**
5.  **API_Design**
6.  **Python_Automation**

## Pitfalls & Constraints
- **NO MEDIA BLEND:** Protect the workspace from becoming a photography tutorial space. Keep it strictly on-software.
- **STAY PRODUCTION-READY:** Avoid "tutorial hell" examples (e.g., simple counters). Only provide code/logic that would be safe and performant in a production codebase.
