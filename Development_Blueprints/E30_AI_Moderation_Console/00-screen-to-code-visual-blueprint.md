# Visual & System Blueprint: E30 AI Moderation Console

## 1. Feature Context & Metadata
- **Feature Directory**: `Development_Blueprints/E30_AI_Moderation_Console/`
- **Target Feature ID**: E30
- **Related PRD Document**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **Mapped Screen Count**: 26 Screens Total
- **Primary User Role**: AI Safety Officer & Scholar
- **Feature Purpose**: AI Moderation Queue, Flagged Interactions, Eval Harness & Kill Switches

---

## 2. Mandatory AI Implementation Directives (Multi-Image Rule)
> **CRITICAL MANDATORY AI INSTRUCTION:**
> For any screen or flow represented by multiple images in this feature, the AI coding agent **MUST read and inspect ALL constituent screen images collectively** before generating any UI, ViewModel, or API binding code.
> The agent must **NOT** implement a partial screen from a single image. It must synthesize all visual states (Initial, Populated, Active Input, Validation Error, Dialogs, Loading Spinners, and Empty States) into a single cohesive, production-ready component.

---

## 3. Exhaustive Screen Inventory & Exact File Paths (26 Screens Total)

| # | Exact Screen Image File Path | Screen Title / Visual State | UI Role | Primary API Dependency |
|---|---|---|---|---|
| 01 | `Screens/Admin Web/46-AI Moderation Queue-01.png` | 46 AI Moderation Queue 01 | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 02 | `Screens/Admin Web/46-AI Moderation Queue-02.png` | 46 AI Moderation Queue 02 | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 03 | `Screens/Admin Web/47-AI Moderation Flagged Interaction-01.png` | 47 AI Moderation Flagged Interaction 01 | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 04 | `Screens/Admin Web/47-AI Moderation Flagged Interaction-02.png` | 47 AI Moderation Flagged Interaction 02 | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 05 | `Screens/Admin Web/47-AI Moderation Flagged Interaction-03.png` | 47 AI Moderation Flagged Interaction 03 | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 06 | `Screens/Admin Web/47-AI Moderation Flagged Interaction-04.png` | 47 AI Moderation Flagged Interaction 04 | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 07 | `Screens/Admin Web/47-AI Moderation Flagged Interaction-05.png` | 47 AI Moderation Flagged Interaction 05 | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 08 | `Screens/Admin Web/47-AI Moderation Flagged Interaction-06.png` | 47 AI Moderation Flagged Interaction 06 | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 09 | `Screens/Admin Web/47-AI Moderation Flagged Interaction-07.png` | 47 AI Moderation Flagged Interaction 07 | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 10 | `Screens/Admin Web/47-AI Moderation Flagged Interaction-08.png` | 47 AI Moderation Flagged Interaction 08 | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 11 | `Screens/Admin Web/48-AI Moderation Flagged Content Gap Escalation.png` | 48 AI Moderation Flagged Content Gap Escalation | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 12 | `Screens/Admin Web/49-AI Moderation Content Gap escalation submit.png` | 49 AI Moderation Content Gap escalation submit | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 13 | `Screens/Admin Web/50-AI Moderation flagged evaluation case .png` | 50 AI Moderation flagged evaluation case  | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 14 | `Screens/Admin Web/51-AI Moderation Full Transcript View-01.png` | 51 AI Moderation Full Transcript View 01 | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 15 | `Screens/Admin Web/51-AI Moderation Full Transcript View-02.png` | 51 AI Moderation Full Transcript View 02 | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 16 | `Screens/Admin Web/87-Evaluation Harness.png` | 87 Evaluation Harness | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 17 | `Screens/Admin Web/88-Evaluation Run run-01.png` | 88 Evaluation Run run 01 | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 18 | `Screens/Admin Web/88-Evaluation Run run-02.png` | 88 Evaluation Run run 02 | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 19 | `Screens/Admin Web/89-Release Gate Decision.png` | 89 Release Gate Decision | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 20 | `Screens/Admin Web/90-False-Positive Feedback Log.png` | 90 False Positive Feedback Log | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 21 | `Screens/Admin Web/91-Model Version & Blocked Topics Registry.png` | 91 Model Version & Blocked Topics Registry | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 22 | `Screens/Admin Web/92-Model Deployed .png` | 92 Model Deployed  | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 23 | `Screens/Admin Web/93-Active Kill Switches-01.png` | 93 Active Kill Switches 01 | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 24 | `Screens/Admin Web/93-Active Kill Switches-02.png` | 93 Active Kill Switches 02 | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 25 | `Screens/Admin Web/93-Active Kill Switches-03.png` | 93 Active Kill Switches 03 | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |
| 26 | `Screens/Admin Web/94-Feature Flags.png` | 94 Feature Flags | AI Safety Officer & Scholar | Sourced from Backend/KMP task files |

---

## 4. Comprehensive 24-Point Screen Specifications (Applied to All Mapped Screens)

For every screen listed above, future AI coding agents must strictly adhere to the following 24-point implementation contract:

1. **Platform**: Defined per exact image path (Mobile App: Compose Multiplatform / M3; Parent/Admin Web: Next.js 14 App Router / Tailwind / shadcn/ui).
2. **Exact Screen Image Path**: Referenced individually in Section 3 and Section 5 below.
3. **Related PRD Document**: Sourced directly from `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`.
4. **Related PRD Section/Feature**: Specified in the corresponding feature task markdown files.
5. **Purpose of the Screen**: Accurate visual and interactive reproduction of the design mockups.
6. **User Role**: `AI Safety Officer & Scholar`.
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

### Screen 01: `46-AI Moderation Queue-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/46-AI Moderation Queue-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 46 AI Moderation Queue 01 with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 02: `46-AI Moderation Queue-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/46-AI Moderation Queue-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 46 AI Moderation Queue 02 with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 03: `47-AI Moderation Flagged Interaction-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/47-AI Moderation Flagged Interaction-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 47 AI Moderation Flagged Interaction 01 with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 04: `47-AI Moderation Flagged Interaction-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/47-AI Moderation Flagged Interaction-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 47 AI Moderation Flagged Interaction 02 with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 05: `47-AI Moderation Flagged Interaction-03.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/47-AI Moderation Flagged Interaction-03.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 47 AI Moderation Flagged Interaction 03 with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 06: `47-AI Moderation Flagged Interaction-04.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/47-AI Moderation Flagged Interaction-04.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 47 AI Moderation Flagged Interaction 04 with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 07: `47-AI Moderation Flagged Interaction-05.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/47-AI Moderation Flagged Interaction-05.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 47 AI Moderation Flagged Interaction 05 with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 08: `47-AI Moderation Flagged Interaction-06.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/47-AI Moderation Flagged Interaction-06.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 47 AI Moderation Flagged Interaction 06 with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 09: `47-AI Moderation Flagged Interaction-07.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/47-AI Moderation Flagged Interaction-07.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 47 AI Moderation Flagged Interaction 07 with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 10: `47-AI Moderation Flagged Interaction-08.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/47-AI Moderation Flagged Interaction-08.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 47 AI Moderation Flagged Interaction 08 with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 11: `48-AI Moderation Flagged Content Gap Escalation.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/48-AI Moderation Flagged Content Gap Escalation.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 48 AI Moderation Flagged Content Gap Escalation with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 12: `49-AI Moderation Content Gap escalation submit.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/49-AI Moderation Content Gap escalation submit.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 49 AI Moderation Content Gap escalation submit with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 13: `50-AI Moderation flagged evaluation case .png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/50-AI Moderation flagged evaluation case .png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 50 AI Moderation flagged evaluation case  with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 14: `51-AI Moderation Full Transcript View-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/51-AI Moderation Full Transcript View-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 51 AI Moderation Full Transcript View 01 with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 15: `51-AI Moderation Full Transcript View-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/51-AI Moderation Full Transcript View-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 51 AI Moderation Full Transcript View 02 with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 16: `87-Evaluation Harness.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/87-Evaluation Harness.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 87 Evaluation Harness with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 17: `88-Evaluation Run run-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/88-Evaluation Run run-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 88 Evaluation Run run 01 with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 18: `88-Evaluation Run run-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/88-Evaluation Run run-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 88 Evaluation Run run 02 with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 19: `89-Release Gate Decision.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/89-Release Gate Decision.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 89 Release Gate Decision with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 20: `90-False-Positive Feedback Log.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/90-False-Positive Feedback Log.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 90 False Positive Feedback Log with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 21: `91-Model Version & Blocked Topics Registry.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/91-Model Version & Blocked Topics Registry.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 91 Model Version & Blocked Topics Registry with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 22: `92-Model Deployed .png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/92-Model Deployed .png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 92 Model Deployed  with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 23: `93-Active Kill Switches-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/93-Active Kill Switches-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 93 Active Kill Switches 01 with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 24: `93-Active Kill Switches-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/93-Active Kill Switches-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 93 Active Kill Switches 02 with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 25: `93-Active Kill Switches-03.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/93-Active Kill Switches-03.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 93 Active Kill Switches 03 with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 26: `94-Feature Flags.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/94-Feature Flags.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
- **4. Purpose**: Render 94 Feature Flags with full visual fidelity to design assets.
- **5. User Role**: AI Safety Officer & Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

---

## 6. Future AI Code Generation Instructions
1. Inspect every image listed above in `Screens/` before generating UI code.
2. Implement backend schemas and endpoints in `Backend/` first.
3. Implement KMP / Next.js client models, repositories, and state machines second.
4. Build the UI composables / React components with exact visual fidelity to the provided designs.
