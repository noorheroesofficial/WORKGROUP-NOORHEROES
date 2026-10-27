# Visual & System Blueprint: E29 Content CMS Scholar Review Workflow

## 1. Feature Context & Metadata
- **Feature Directory**: `Development_Blueprints/E29_Content_CMS_Scholar_Review_Workflow/`
- **Target Feature ID**: E29
- **Related PRD Document**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **Mapped Screen Count**: 41 Screens Total
- **Primary User Role**: Content Author & Islamic Scholar
- **Feature Purpose**: Interactive Story Editor, Media Uploads & Multi-Tier Scholar Review

---

## 2. Mandatory AI Implementation Directives (Multi-Image Rule)
> **CRITICAL MANDATORY AI INSTRUCTION:**
> For any screen or flow represented by multiple images in this feature, the AI coding agent **MUST read and inspect ALL constituent screen images collectively** before generating any UI, ViewModel, or API binding code.
> The agent must **NOT** implement a partial screen from a single image. It must synthesize all visual states (Initial, Populated, Active Input, Validation Error, Dialogs, Loading Spinners, and Empty States) into a single cohesive, production-ready component.

---

## 3. Exhaustive Screen Inventory & Exact File Paths (41 Screens Total)

| # | Exact Screen Image File Path | Screen Title / Visual State | UI Role | Primary API Dependency |
|---|---|---|---|---|
| 01 | `Screens/Admin Web/27-Content Library.png` | 27 Content Library | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 02 | `Screens/Admin Web/28-Story Editor-01.png` | 28 Story Editor 01 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 03 | `Screens/Admin Web/28-Story Editor-02.png` | 28 Story Editor 02 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 04 | `Screens/Admin Web/28-Story Editor-03.png` | 28 Story Editor 03 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 05 | `Screens/Admin Web/28-Story Editor-04.png` | 28 Story Editor 04 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 06 | `Screens/Admin Web/28-Story Editor-05.png` | 28 Story Editor 05 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 07 | `Screens/Admin Web/28-Story Editor-06.png` | 28 Story Editor 06 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 08 | `Screens/Admin Web/28-Story Editor-07.png` | 28 Story Editor 07 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 09 | `Screens/Admin Web/28-Story Editor-08.png` | 28 Story Editor 08 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 10 | `Screens/Admin Web/28-Story Editor-09.png` | 28 Story Editor 09 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 11 | `Screens/Admin Web/28-Story Editor-10.png` | 28 Story Editor 10 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 12 | `Screens/Admin Web/28-Story Editor-11.png` | 28 Story Editor 11 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 13 | `Screens/Admin Web/28-Story Editor-12.png` | 28 Story Editor 12 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 14 | `Screens/Admin Web/28-Story Editor-13.png` | 28 Story Editor 13 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 15 | `Screens/Admin Web/28-Story Editor-14.png` | 28 Story Editor 14 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 16 | `Screens/Admin Web/29-Story Editor-upload media-01.png` | 29 Story Editor upload media 01 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 17 | `Screens/Admin Web/29-Story Editor-upload media-02.png` | 29 Story Editor upload media 02 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 18 | `Screens/Admin Web/29-Story Editor-upload media-03.png` | 29 Story Editor upload media 03 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 19 | `Screens/Admin Web/29-Story Editor-upload media-04.png` | 29 Story Editor upload media 04 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 20 | `Screens/Admin Web/29-Story Editor-upload media-05.png` | 29 Story Editor upload media 05 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 21 | `Screens/Admin Web/30-Story Editor-version-history-01.png` | 30 Story Editor version history 01 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 22 | `Screens/Admin Web/30-Story Editor-version-history-02.png` | 30 Story Editor version history 02 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 23 | `Screens/Admin Web/31-Quiz Builder.png` | 31 Quiz Builder | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 24 | `Screens/Admin Web/32-Question Editor-01.png` | 32 Question Editor 01 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 25 | `Screens/Admin Web/32-Question Editor-02.png` | 32 Question Editor 02 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 26 | `Screens/Admin Web/32-Question Editor-03.png` | 32 Question Editor 03 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 27 | `Screens/Admin Web/32-Question Editor-04.png` | 32 Question Editor 04 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 28 | `Screens/Admin Web/33-Quiz Preview.png` | 33 Quiz Preview | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 29 | `Screens/Admin Web/34-Media Library.png` | 34 Media Library | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 30 | `Screens/Admin Web/35-Quran Proposal-01.png` | 35 Quran Proposal 01 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 31 | `Screens/Admin Web/35-Quran Proposal-02.png` | 35 Quran Proposal 02 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 32 | `Screens/Admin Web/35-Quran Proposal-03.png` | 35 Quran Proposal 03 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 33 | `Screens/Admin Web/36-Quran Scholar Review.png` | 36 Quran Scholar Review | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 34 | `Screens/Admin Web/38-Scholar Review Queue.png` | 38 Scholar Review Queue | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 35 | `Screens/Admin Web/39-Scholar Queue-accuracy review-01.png` | 39 Scholar Queue accuracy review 01 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 36 | `Screens/Admin Web/39-Scholar Queue-accuracy review-02.png` | 39 Scholar Queue accuracy review 02 | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 37 | `Screens/Admin Web/40-Scholar Queue-accuracy review-confirm review.png` | 40 Scholar Queue accuracy review confirm review | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 38 | `Screens/Admin Web/41-Scholar Queue-accuracy review decision recorded.png` | 41 Scholar Queue accuracy review decision recorded | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 39 | `Screens/Admin Web/42-Scholar Queue-accuracy review version history.png` | 42 Scholar Queue accuracy review version history | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 40 | `Screens/Admin Web/52-Editorial Review Queue.png` | 52 Editorial Review Queue | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |
| 41 | `Screens/Admin Web/53-Scholar Review Queue.png` | 53 Scholar Review Queue | Content Author & Islamic Scholar | Sourced from Backend/KMP task files |

---

## 4. Comprehensive 24-Point Screen Specifications (Applied to All Mapped Screens)

For every screen listed above, future AI coding agents must strictly adhere to the following 24-point implementation contract:

1. **Platform**: Defined per exact image path (Mobile App: Compose Multiplatform / M3; Parent/Admin Web: Next.js 14 App Router / Tailwind / shadcn/ui).
2. **Exact Screen Image Path**: Referenced individually in Section 3 and Section 5 below.
3. **Related PRD Document**: Sourced directly from `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`.
4. **Related PRD Section/Feature**: Specified in the corresponding feature task markdown files.
5. **Purpose of the Screen**: Accurate visual and interactive reproduction of the design mockups.
6. **User Role**: `Content Author & Islamic Scholar`.
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

### Screen 01: `27-Content Library.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/27-Content Library.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 27 Content Library with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 02: `28-Story Editor-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/28-Story Editor-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 28 Story Editor 01 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 03: `28-Story Editor-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/28-Story Editor-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 28 Story Editor 02 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 04: `28-Story Editor-03.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/28-Story Editor-03.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 28 Story Editor 03 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 05: `28-Story Editor-04.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/28-Story Editor-04.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 28 Story Editor 04 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 06: `28-Story Editor-05.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/28-Story Editor-05.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 28 Story Editor 05 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 07: `28-Story Editor-06.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/28-Story Editor-06.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 28 Story Editor 06 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 08: `28-Story Editor-07.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/28-Story Editor-07.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 28 Story Editor 07 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 09: `28-Story Editor-08.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/28-Story Editor-08.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 28 Story Editor 08 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 10: `28-Story Editor-09.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/28-Story Editor-09.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 28 Story Editor 09 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 11: `28-Story Editor-10.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/28-Story Editor-10.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 28 Story Editor 10 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 12: `28-Story Editor-11.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/28-Story Editor-11.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 28 Story Editor 11 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 13: `28-Story Editor-12.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/28-Story Editor-12.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 28 Story Editor 12 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 14: `28-Story Editor-13.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/28-Story Editor-13.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 28 Story Editor 13 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 15: `28-Story Editor-14.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/28-Story Editor-14.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 28 Story Editor 14 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 16: `29-Story Editor-upload media-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/29-Story Editor-upload media-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 29 Story Editor upload media 01 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 17: `29-Story Editor-upload media-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/29-Story Editor-upload media-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 29 Story Editor upload media 02 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 18: `29-Story Editor-upload media-03.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/29-Story Editor-upload media-03.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 29 Story Editor upload media 03 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 19: `29-Story Editor-upload media-04.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/29-Story Editor-upload media-04.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 29 Story Editor upload media 04 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 20: `29-Story Editor-upload media-05.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/29-Story Editor-upload media-05.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 29 Story Editor upload media 05 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 21: `30-Story Editor-version-history-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/30-Story Editor-version-history-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 30 Story Editor version history 01 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 22: `30-Story Editor-version-history-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/30-Story Editor-version-history-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 30 Story Editor version history 02 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 23: `31-Quiz Builder.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/31-Quiz Builder.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 31 Quiz Builder with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 24: `32-Question Editor-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/32-Question Editor-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 32 Question Editor 01 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 25: `32-Question Editor-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/32-Question Editor-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 32 Question Editor 02 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 26: `32-Question Editor-03.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/32-Question Editor-03.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 32 Question Editor 03 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 27: `32-Question Editor-04.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/32-Question Editor-04.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 32 Question Editor 04 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 28: `33-Quiz Preview.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/33-Quiz Preview.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 33 Quiz Preview with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 29: `34-Media Library.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/34-Media Library.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 34 Media Library with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 30: `35-Quran Proposal-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/35-Quran Proposal-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 35 Quran Proposal 01 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 31: `35-Quran Proposal-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/35-Quran Proposal-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 35 Quran Proposal 02 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 32: `35-Quran Proposal-03.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/35-Quran Proposal-03.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 35 Quran Proposal 03 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 33: `36-Quran Scholar Review.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/36-Quran Scholar Review.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 36 Quran Scholar Review with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 34: `38-Scholar Review Queue.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/38-Scholar Review Queue.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 38 Scholar Review Queue with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 35: `39-Scholar Queue-accuracy review-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/39-Scholar Queue-accuracy review-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 39 Scholar Queue accuracy review 01 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 36: `39-Scholar Queue-accuracy review-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/39-Scholar Queue-accuracy review-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 39 Scholar Queue accuracy review 02 with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 37: `40-Scholar Queue-accuracy review-confirm review.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/40-Scholar Queue-accuracy review-confirm review.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 40 Scholar Queue accuracy review confirm review with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 38: `41-Scholar Queue-accuracy review decision recorded.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/41-Scholar Queue-accuracy review decision recorded.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 41 Scholar Queue accuracy review decision recorded with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 39: `42-Scholar Queue-accuracy review version history.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/42-Scholar Queue-accuracy review version history.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 42 Scholar Queue accuracy review version history with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 40: `52-Editorial Review Queue.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/52-Editorial Review Queue.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 52 Editorial Review Queue with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 41: `53-Scholar Review Queue.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/53-Scholar Review Queue.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E29_Content_CMS_Scholar_Review_Workflow.md`
- **4. Purpose**: Render 53 Scholar Review Queue with full visual fidelity to design assets.
- **5. User Role**: Content Author & Islamic Scholar
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

---

## 6. Future AI Code Generation Instructions
1. Inspect every image listed above in `Screens/` before generating UI code.
2. Implement backend schemas and endpoints in `Backend/` first.
3. Implement KMP / Next.js client models, repositories, and state machines second.
4. Build the UI composables / React components with exact visual fidelity to the provided designs.
