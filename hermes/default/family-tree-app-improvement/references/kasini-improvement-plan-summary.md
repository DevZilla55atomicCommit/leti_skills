# Kasini Improvement Plan Summary

## 🎯 Vision
> Build the most focused, cross‑platform family tree app — the "Kasini" tool that lets users map relationships, check cousin matches, and export trees — without ceremony or translation overhead. Keep it tight, fun, and ready for iOS/Android/Web.

## 📦 Core Components (Essential)
| Component | What It Does |
|-----------|--------------|
| **Visual Tree Canvas** | Interactive tree that mirrors Episode 6 fidelity (relative positioning, yellow highlight). |
| **Kasini Calculator** | Tap any two people → "Safe to date?" 💚 / 🚨 badge + shareable card. |
| **Smart Search** | Find ancestors by name, birth year, village, or tag. |
| **Export / Share** | One‑tap PDF or image of the tree + Kasini result. |
| **Cross‑Platform Engine** | Expo + React Native + Web (iOS/Android/Web from same codebase). |
| **Offline‑First Sync** | SQLite persistence + Convex real‑time sync (optional). |

## 🚀 Phase 1: Core Tree & Kasini Calculator (Weeks 1‑3)
| Sprint | Owner | Done When |
|--------|-------|-----------|
| **Week 1** – Scaffold & Render | Set up Expo, NativeWind, Skia; build `PersonNode` with photo, name, badge; pan/zoom canvas. | `npm install && npm run dev` runs without errors. |
| **Week 2** – Anchor‑First Flow & Calculator | Implement "tap person → Parent/Spouse/Child → auto‑position" + Kasini path animation + result badge. | Shareable `Kasini Card` PNG export works. |
| **Week 3** – Beta Onboarding & Polish | Create guided 3‑min onboarding, add share button, test on iOS/Android simulators. | 5 test users can build a tree of ≥5 people. |

## 🎮 Phase 2: Gamified Discovery (Weeks 4‑6)
| Feature | Mechanics |
|---------|-----------|
| **Daily "Who's My Kasini?"** | Push: "You're X cousins with [famous Tongan]" → screenshot → TikTok. |
| **Family Quest** | "Add 3 ancestors from Mu'a" → unlock badge. |
| **Kasini Roulette** | Spin → random relative → learn one fact → group chat share. |
| **Meme Generator** | "When your crush is your 4th cousin" → Instagram Story template. |

## 📱 Phase 3: Cross‑Platform Delivery (Weeks 7‑9)
| Task | Target |
|------|--------|
| **iOS TestFlight + Android Internal** | 20 FOUA beta families testing with zero crashes. |
| **Web PWA** | Offline‑first token stored in localStorage; same tree logic. |
| **Accessibility** | VoiceOver/TalkBack labels, Dynamic Type scaling, contrast ≥ 4.5:1. |

## 📊 Success Metrics (First 90 Days)
| Metric | Target |
|--------|--------|
| Active Families (≥3 people) | 100 |
| Weekly Retention | 50 % |
| Kasini Checks/week | 2 000 |
| Youth Users (13‑25) | 35 % of active |
| Zero Critical Crashes | ✅ |

## ⏱️ Immediate Next Steps (This Week)
| # | Action | Owner | Time |
|---|--------|-------|------|
| 1 | `cd kasini-tree-app && npm install && npm run dev` | Dev | 15 min |
| 2 | Design system in Figma (tokens + 3 screens) | Designer | Day 2 |
| 3 | Build `PersonNode` (Skia) with photo, name, kasini badge | Dev | Day 3 |
| 4 | Implement anchor‑first add flow (tap → Parent/Spouse/Child → animate) | Dev | Day 4 |
| 5 | Add Kasini Calculator (graph traversal + share card) | Dev | Day 5 |
| 6 | Beta signup form (Typeform → Airtable) → comment on Ep 6 | You | Today |
| 7 | Record 60‑sec "Kasini Calculator Demo" video | You | Weekend |

## ✅ Review & Confirm
- **Language:** English only; Tongan terms (kasini, fānau) used as cultural flavor.  
- **Scope:** Core tree + Kasini calculator only — no ceremony, no translation layer.  
- **Team:** You will watch Ep 6 to extract decisions; dev will set up scaffold; designer will draft tokens.  

*Let me know if any step needs reshaping before we start execution.*

## 📦 Core Components
1. **Extended Data Model**: GEDCOM 7.0 + TGE (Tongan Genealogy Extension) with:
   - `ha_a` (clan), `fonua` (village/land), `hereditary_title`, `koeuhi` (chant)
2. **UX Paradigms**:
   - Fonua-first navigation (village view)
   - Kava Circle collaboration
   - Title succession tracker
3. **Audio Preservation**: Koeuhi engine with interlinear transcription
4. **Design System**: Tongan colors, typography, ngatu patterns
5. **Deployment**: Offline-first React Native + Convex backend, Cloudflare R2 CDN

## 🛠️ Implementation Steps (High Level)
1. Build TGE schema in PostgreSQL
2. Create React Native components: Fonua Picker, Koeuhi Player
3. Implement offline map tiles for Tonga
4. Set up Whisper.cpp for Tongan STT
5. Design beta signup flow for Ep 6 viewers

## 📋 Immediate Next Steps
| # | Action | Owner | Done When |
|---|--------|-------|-----------|
| 1 | **Watch Ep 6 + extract decisions** — watch video, note data model choices | You | Today |
| 2 | `cd kasini-tree-app && npm install && npm run dev` | Dev | Today |
| 3 | **Design system in Figma** — tokens + 5 screens | Designer | Day 2 |
| 4 | **Beta signup form** (Typeform → Airtable) → post in Ep 6 comments | You | Day 2 |
| 5 | **Fonua picker** with offline typeahead | Dev | Day 4 |
| 6 | **Record Koeuhi demo** with elder (permission required) | You/Community | Week 2 |
| 7 | **Add testing**: run `npm test` and fix any failing tests | Dev | End of day 2 |

## ✅ Support Files (References)
- `references/kasini-data-model.md` - Detailed schema
- `templates/expo-project-scaffold.zip` - Pre‑configured Expo starter
- `scripts/verify-schema.js` - Schema validation script
- `references/Kasini_Improvement_Plan.md` - Full improvement plan

## 🔁 Revision History
- v1.0 (2026-07-12): Initial creation from Kasini Ep 6 analysis