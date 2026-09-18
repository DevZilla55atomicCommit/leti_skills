# Top Web Development Skills Reference (Quick Reference)

## Core Development Skills
| Skill | Purpose | Key Features |
|-------|---------|--------------|
| `frontend-ui-engineering` | Accessibility, design systems, responsive design | WCAG AAA, fluid typography, progressive enhancement, loading states |
| `spec-driven-development` | Specs before code, gated workflow | Dependency graphs, vertical slicing, feature flags |
| `test-driven-development` | RED/GREEN/REFACTOR workflow | Prove-It bug pattern, mock services, DevTools debugging |
| `incremental-implementation` | Risk-first, feature flags | Vertical slices, commit-per-slice, trunk-based dev |
| `code-review-and-quality` | 5-axis review | Correctness, readability, architecture, security, performance |

## Design & Interaction
| Skill | Purpose | Key Features |
|-------|---------|--------------|
| `modern-web-design` | 2024-25 design trends | Bold minimalism, scrollytelling, glassmorphism, cursor UX |
| `gsap-scrolltrigger` | Scroll-driven animations | Pinning, scrubbing, batching, performance optimization |
| `motion-framer` | React animations | Layout animations, shared-element transitions, physics |
| `locomotive-scroll` | Smooth scroll | Momentum scrolling, parallax, train Approach |
| `barba-js` | Page transitions | SPA transitions, preloaders, custom effects |

## 3D & Advanced Visuals
| Skill | Purpose | Key Features |
|-------|---------|--------------|
| `threejs-webgl` | Custom 3D scenes | WebGL/WebGPU, scene graph, materials, lights, shadows |
| `react-three-fiber` | Declarative 3D | JSX components, hooks, Drei helpers, state management |
| `lightweight-3d-effects` | Background effects | Vanta.js, Zdog, tilt effects, performance-friendly |
| `playcanvas-engine` | Full 3D engine | Physics, networking, particle systems |

## Installation Checklist
1. Verify `claude code` is installed and authenticated
2. Install core skills from addyosmani/agent-skills repo
3. Install design skills from freshtechbro/claudedesignskills
4. Verify installations with `claude code list`
5. Add references to `~/.claude/skills/` for quick access
6. Schedule quarterly verification of skill relevance

## Common Pitfalls
- **Missing Python**: Some skills require `python3` - install via `brew install python`
- **Trusted Workspace**: For new repo installs, run `git trust` to avoid timeout
- **Model Conflicts**: When using NVIDIA API, ensure `base_url` points to `https://integrate.api.nvidia.com/v1` (not local Ollama)
- **Shadow DOM**: When using Web Components in R3F, ensure proper encapsulation