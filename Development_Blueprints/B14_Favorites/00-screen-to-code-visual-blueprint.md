# Visual & System Blueprint: B14 Favorites

## 1. Feature Context & Metadata
- **Feature Directory**: `Development_Blueprints/B14_Favorites/`
- **Target Feature ID**: B14
- **Related PRD Document**: `PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md`
- **Mapped Screen Count**: 9 Screens Total
- **Primary User Role**: Child Learner
- **Feature Purpose**: Bookmarked Stories, Duas, Quizzes & Offline Cache

---

## 2. Mandatory AI Implementation Directives (Multi-Image Rule)
> **CRITICAL MANDATORY AI INSTRUCTION:**
> For any screen or flow represented by multiple images in this feature, the AI coding agent **MUST read and inspect ALL constituent screen images collectively** before generating any UI, ViewModel, or API binding code.
> The agent must **NOT** implement a partial screen from a single image. It must synthesize all visual states (Initial, Populated, Active Input, Validation Error, Dialogs, Loading Spinners, and Empty States) into a single cohesive, production-ready component.

---

## 3. Exhaustive Screen Inventory & Exact File Paths (9 Screens Total)

| # | Exact Screen Image File Path | Screen Title / Visual State | UI Role | Primary API Dependency |
|---|---|---|---|---|
| 01 | `Screens/Mobile App/Favorites/Favorites-01.png` | Favorites 01 | Child Learner | Sourced from Backend/KMP task files |
| 02 | `Screens/Mobile App/Favorites/Favorites-02.png` | Favorites 02 | Child Learner | Sourced from Backend/KMP task files |
| 03 | `Screens/Mobile App/Favorites/Favorites-03.png` | Favorites 03 | Child Learner | Sourced from Backend/KMP task files |
| 04 | `Screens/Mobile App/Favorites/Favorites-04.png` | Favorites 04 | Child Learner | Sourced from Backend/KMP task files |
| 05 | `Screens/Mobile App/Favorites/Favorites-05.png` | Favorites 05 | Child Learner | Sourced from Backend/KMP task files |
| 06 | `Screens/Mobile App/Favorites/Favorites-06.png` | Favorites 06 | Child Learner | Sourced from Backend/KMP task files |
| 07 | `Screens/Mobile App/Favorites/Favorites-07.png` | Favorites 07 | Child Learner | Sourced from Backend/KMP task files |
| 08 | `Screens/Mobile App/Favorites/Favorites-08.png` | Favorites 08 | Child Learner | Sourced from Backend/KMP task files |
| 09 | `Screens/Mobile App/Favorites/Favorites-09.png` | Favorites 09 | Child Learner | Sourced from Backend/KMP task files |

---

## 4. Comprehensive 24-Point Screen Specifications (Applied to All Mapped Screens)

For every screen listed above, future AI coding agents must strictly adhere to the following 24-point implementation contract:

1. **Platform**: Defined per exact image path (Mobile App: Compose Multiplatform / M3; Parent/Admin Web: Next.js 14 App Router / Tailwind / shadcn/ui).
2. **Exact Screen Image Path**: Referenced individually in Section 3 and Section 5 below.
3. **Related PRD Document**: Sourced directly from `PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md`.
4. **Related PRD Section/Feature**: Specified in the corresponding feature task markdown files.
5. **Purpose of the Screen**: Accurate visual and interactive reproduction of the design mockups.
6. **User Role**: `Child Learner`.
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

### Screen 01: `Favorites-01.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Favorites/Favorites-01.png`
- **3. Related PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md`
- **4. Purpose**: Render Favorites 01 with full visual fidelity to design assets.
- **5. User Role**: Child Learner
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 02: `Favorites-02.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Favorites/Favorites-02.png`
- **3. Related PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md`
- **4. Purpose**: Render Favorites 02 with full visual fidelity to design assets.
- **5. User Role**: Child Learner
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 03: `Favorites-03.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Favorites/Favorites-03.png`
- **3. Related PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md`
- **4. Purpose**: Render Favorites 03 with full visual fidelity to design assets.
- **5. User Role**: Child Learner
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 04: `Favorites-04.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Favorites/Favorites-04.png`
- **3. Related PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md`
- **4. Purpose**: Render Favorites 04 with full visual fidelity to design assets.
- **5. User Role**: Child Learner
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 05: `Favorites-05.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Favorites/Favorites-05.png`
- **3. Related PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md`
- **4. Purpose**: Render Favorites 05 with full visual fidelity to design assets.
- **5. User Role**: Child Learner
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 06: `Favorites-06.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Favorites/Favorites-06.png`
- **3. Related PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md`
- **4. Purpose**: Render Favorites 06 with full visual fidelity to design assets.
- **5. User Role**: Child Learner
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 07: `Favorites-07.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Favorites/Favorites-07.png`
- **3. Related PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md`
- **4. Purpose**: Render Favorites 07 with full visual fidelity to design assets.
- **5. User Role**: Child Learner
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 08: `Favorites-08.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Favorites/Favorites-08.png`
- **3. Related PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md`
- **4. Purpose**: Render Favorites 08 with full visual fidelity to design assets.
- **5. User Role**: Child Learner
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 09: `Favorites-09.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Favorites/Favorites-09.png`
- **3. Related PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md`
- **4. Purpose**: Render Favorites 09 with full visual fidelity to design assets.
- **5. User Role**: Child Learner
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

---

## 6. Future AI Code Generation Instructions
1. Inspect every image listed above in `Screens/` before generating UI code.
2. Implement backend schemas and endpoints in `Backend/` first.
3. Implement KMP / Next.js client models, repositories, and state machines second.
4. Build the UI composables / React components with exact visual fidelity to the provided designs.
