# Visual & System Blueprint: F36 Ramadan Mode

## 1. Feature Context & Metadata
- **Feature Directory**: `Development_Blueprints/F36_Ramadan_Mode/`
- **Target Feature ID**: F36
- **Related PRD Document**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **Mapped Screen Count**: 28 Screens Total
- **Primary User Role**: Child & Parent
- **Feature Purpose**: 30-Night Ramadan Journey, Fasting Tracker, Eid Cards & Report

---

## 2. Mandatory AI Implementation Directives (Multi-Image Rule)
> **CRITICAL MANDATORY AI INSTRUCTION:**
> For any screen or flow represented by multiple images in this feature, the AI coding agent **MUST read and inspect ALL constituent screen images collectively** before generating any UI, ViewModel, or API binding code.
> The agent must **NOT** implement a partial screen from a single image. It must synthesize all visual states (Initial, Populated, Active Input, Validation Error, Dialogs, Loading Spinners, and Empty States) into a single cohesive, production-ready component.

---

## 3. Exhaustive Screen Inventory & Exact File Paths (28 Screens Total)

| # | Exact Screen Image File Path | Screen Title / Visual State | UI Role | Primary API Dependency |
|---|---|---|---|---|
| 01 | `Screens/Mobile App/Ramadan Mode/Eid Card Generator.png` | Eid Card Generator | Child & Parent | Sourced from Backend/KMP task files |
| 02 | `Screens/Mobile App/Ramadan Mode/Eid Countdown.png` | Eid Countdown | Child & Parent | Sourced from Backend/KMP task files |
| 03 | `Screens/Mobile App/Ramadan Mode/Eid Home.png` | Eid Home | Child & Parent | Sourced from Backend/KMP task files |
| 04 | `Screens/Mobile App/Ramadan Mode/Eid Reward Reveal.png` | Eid Reward Reveal | Child & Parent | Sourced from Backend/KMP task files |
| 05 | `Screens/Mobile App/Ramadan Mode/Fasting Tracker-01.png` | Fasting Tracker 01 | Child & Parent | Sourced from Backend/KMP task files |
| 06 | `Screens/Mobile App/Ramadan Mode/Fasting Tracker-02.png` | Fasting Tracker 02 | Child & Parent | Sourced from Backend/KMP task files |
| 07 | `Screens/Mobile App/Ramadan Mode/Journey Map (Lanterns).png` | Journey Map (Lanterns) | Child & Parent | Sourced from Backend/KMP task files |
| 08 | `Screens/Mobile App/Ramadan Mode/Laylatul Qadr Reflection.png` | Laylatul Qadr Reflection | Child & Parent | Sourced from Backend/KMP task files |
| 09 | `Screens/Mobile App/Ramadan Mode/Mission Detail.png` | Mission Detail | Child & Parent | Sourced from Backend/KMP task files |
| 10 | `Screens/Mobile App/Ramadan Mode/Night Recap.png` | Night Recap | Child & Parent | Sourced from Backend/KMP task files |
| 11 | `Screens/Mobile App/Ramadan Mode/Parent-Family Aggregate.png` | Parent Family Aggregate | Child & Parent | Sourced from Backend/KMP task files |
| 12 | `Screens/Mobile App/Ramadan Mode/Parent-Family Member Invite.png` | Parent Family Member Invite | Child & Parent | Sourced from Backend/KMP task files |
| 13 | `Screens/Mobile App/Ramadan Mode/Parent-Family Report.png` | Parent Family Report | Child & Parent | Sourced from Backend/KMP task files |
| 14 | `Screens/Mobile App/Ramadan Mode/Parent-Family Report⑲ Conversion Card (Day 28-30).png` | Parent Family Report⑲ Conversion Card (Day 28 30) | Child & Parent | Sourced from Backend/KMP task files |
| 15 | `Screens/Mobile App/Ramadan Mode/Parent-Ramadan Dashboard.png` | Parent Ramadan Dashboard | Child & Parent | Sourced from Backend/KMP task files |
| 16 | `Screens/Mobile App/Ramadan Mode/Parent-Ramadan Settings.png` | Parent Ramadan Settings | Child & Parent | Sourced from Backend/KMP task files |
| 17 | `Screens/Mobile App/Ramadan Mode/Post-Eid Keep the Habit.png` | Post Eid Keep the Habit | Child & Parent | Sourced from Backend/KMP task files |
| 18 | `Screens/Mobile App/Ramadan Mode/Prep-Countdown.png` | Prep Countdown | Child & Parent | Sourced from Backend/KMP task files |
| 19 | `Screens/Mobile App/Ramadan Mode/Ramadan Certificate.png` | Ramadan Certificate | Child & Parent | Sourced from Backend/KMP task files |
| 20 | `Screens/Mobile App/Ramadan Mode/Ramadan Home.png` | Ramadan Home | Child & Parent | Sourced from Backend/KMP task files |
| 21 | `Screens/Mobile App/Ramadan Mode/Story Player.png` | Story Player | Child & Parent | Sourced from Backend/KMP task files |
| 22 | `Screens/Admin Web/Ramadan Mode/01-Campaign Manager.png` | 01 Campaign Manager | Admin & Scholar | Sourced from Backend/KMP task files |
| 23 | `Screens/Admin Web/Ramadan Mode/02-30-Night Content .png` | 02 30 Night Content  | Admin & Scholar | Sourced from Backend/KMP task files |
| 24 | `Screens/Admin Web/Ramadan Mode/03-Laylatul Qadr Set -01.png` | 03 Laylatul Qadr Set  01 | Admin & Scholar | Sourced from Backend/KMP task files |
| 25 | `Screens/Admin Web/Ramadan Mode/03-Laylatul Qadr Set -02.png` | 03 Laylatul Qadr Set  02 | Admin & Scholar | Sourced from Backend/KMP task files |
| 26 | `Screens/Admin Web/Ramadan Mode/04-Eid Package Manager.png` | 04 Eid Package Manager | Admin & Scholar | Sourced from Backend/KMP task files |
| 27 | `Screens/Admin Web/Ramadan Mode/05-Analytics Dashboard.png` | 05 Analytics Dashboard | Admin & Scholar | Sourced from Backend/KMP task files |
| 28 | `Screens/Admin Web/Ramadan Mode/06-Deadline Tracker.png` | 06 Deadline Tracker | Admin & Scholar | Sourced from Backend/KMP task files |

---

## 4. Comprehensive 24-Point Screen Specifications (Applied to All Mapped Screens)

For every screen listed above, future AI coding agents must strictly adhere to the following 24-point implementation contract:

1. **Platform**: Defined per exact image path (Mobile App: Compose Multiplatform / M3; Parent/Admin Web: Next.js 14 App Router / Tailwind / shadcn/ui).
2. **Exact Screen Image Path**: Referenced individually in Section 3 and Section 5 below.
3. **Related PRD Document**: Sourced directly from `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`.
4. **Related PRD Section/Feature**: Specified in the corresponding feature task markdown files.
5. **Purpose of the Screen**: Accurate visual and interactive reproduction of the design mockups.
6. **User Role**: `Child & Parent`.
7. **Entry Point**: Mapped in the feature navigation graph.
8. **Previous Screen**: Documented in navigation state flow.
9. **Next Screen(s)**: Forward navigation destinations upon primary action completion.
10. **Navigation Conditions**: Validated against user authentication state, permissions, and network connectivity.
11. **Required API(s)**: Documented in the `Backend/` task files within this directory.
12. **Required Request Data**: Validated via Pydantic / Zod schemas.
13. **Required Response Data**: Serialized into immutable Kotlin / TypeScript DTOs.
14. **Required UI States**: Full support for Initial Loading, Populated Data, Empty State, Error State, and Action Spinners.
15. **Business Logic**: Enforced via clean architecture domain repositories and use cases.
16. **Validation Rules**: Client-side instant format feedback + authoritative server-side validation.
17. **Error Handling**: Non-blocking toasts or localized error cards with "Retry" buttons.
18. **Loading Behavior**: Shimmer/Skeleton loaders matching the exact card aspect ratios.
19. **Empty-State Behavior**: Themed Islamic illustration with encouraging empty state copy and primary CTA.
20. **Success Behavior**: Smooth animated transition with optional celebratory reward badges / XP particle effects.
21. **Edge Cases**: Long text wrapping, null fields, rapid double-tapping prevention, and graceful offline degradation.
22. **Authentication / Authorization**: Child session token or Parent PIN verification or Admin RBAC permission check.
23. **Permissions**: Camera/Microphone/Storage permissions requested just-in-time with clear parental explanations.
24. **Dependencies**: Upstream services and local SQLite / SQLDelight cache tables.

---

## 5. Detailed Screen-by-Screen Specifications

### Screen 01: `Eid Card Generator.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Eid Card Generator.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Eid Card Generator with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 02: `Eid Countdown.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Eid Countdown.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Eid Countdown with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 03: `Eid Home.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Eid Home.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Eid Home with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 04: `Eid Reward Reveal.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Eid Reward Reveal.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Eid Reward Reveal with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 05: `Fasting Tracker-01.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Fasting Tracker-01.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Fasting Tracker 01 with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 06: `Fasting Tracker-02.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Fasting Tracker-02.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Fasting Tracker 02 with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 07: `Journey Map (Lanterns).png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Journey Map (Lanterns).png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Journey Map (Lanterns) with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 08: `Laylatul Qadr Reflection.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Laylatul Qadr Reflection.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Laylatul Qadr Reflection with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 09: `Mission Detail.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Mission Detail.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Mission Detail with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 10: `Night Recap.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Night Recap.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Night Recap with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 11: `Parent-Family Aggregate.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Parent-Family Aggregate.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Parent Family Aggregate with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 12: `Parent-Family Member Invite.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Parent-Family Member Invite.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Parent Family Member Invite with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 13: `Parent-Family Report.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Parent-Family Report.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Parent Family Report with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 14: `Parent-Family Report⑲ Conversion Card (Day 28-30).png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Parent-Family Report⑲ Conversion Card (Day 28-30).png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Parent Family Report⑲ Conversion Card (Day 28 30) with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 15: `Parent-Ramadan Dashboard.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Parent-Ramadan Dashboard.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Parent Ramadan Dashboard with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 16: `Parent-Ramadan Settings.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Parent-Ramadan Settings.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Parent Ramadan Settings with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 17: `Post-Eid Keep the Habit.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Post-Eid Keep the Habit.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Post Eid Keep the Habit with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 18: `Prep-Countdown.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Prep-Countdown.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Prep Countdown with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 19: `Ramadan Certificate.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Ramadan Certificate.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Ramadan Certificate with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 20: `Ramadan Home.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Ramadan Home.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Ramadan Home with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 21: `Story Player.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Ramadan Mode/Story Player.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render Story Player with full visual fidelity to design assets.
- **5. User Role**: Child & Parent
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 22: `01-Campaign Manager.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/Ramadan Mode/01-Campaign Manager.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render 01 Campaign Manager with full visual fidelity to design assets.
- **5. User Role**: Admin & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 23: `02-30-Night Content .png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/Ramadan Mode/02-30-Night Content .png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render 02 30 Night Content  with full visual fidelity to design assets.
- **5. User Role**: Admin & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 24: `03-Laylatul Qadr Set -01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/Ramadan Mode/03-Laylatul Qadr Set -01.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render 03 Laylatul Qadr Set  01 with full visual fidelity to design assets.
- **5. User Role**: Admin & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 25: `03-Laylatul Qadr Set -02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/Ramadan Mode/03-Laylatul Qadr Set -02.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render 03 Laylatul Qadr Set  02 with full visual fidelity to design assets.
- **5. User Role**: Admin & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 26: `04-Eid Package Manager.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/Ramadan Mode/04-Eid Package Manager.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render 04 Eid Package Manager with full visual fidelity to design assets.
- **5. User Role**: Admin & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 27: `05-Analytics Dashboard.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/Ramadan Mode/05-Analytics Dashboard.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render 05 Analytics Dashboard with full visual fidelity to design assets.
- **5. User Role**: Admin & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 28: `06-Deadline Tracker.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/Ramadan Mode/06-Deadline Tracker.png`
- **3. Related PRD**: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`
- **4. Purpose**: Render 06 Deadline Tracker with full visual fidelity to design assets.
- **5. User Role**: Admin & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

---

## 6. Future AI Code Generation Instructions
1. Inspect every image listed above in `Screens/` before generating UI code.
2. Implement backend schemas and endpoints in `Backend/` first.
3. Implement KMP / Next.js client models, repositories, and state machines second.
4. Build the UI composables / React components with exact visual fidelity to the provided designs.
