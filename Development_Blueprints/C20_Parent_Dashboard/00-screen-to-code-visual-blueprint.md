# Visual & System Blueprint: C20 Parent Dashboard

## 1. Feature Context & Metadata
- **Feature Directory**: `Development_Blueprints/C20_Parent_Dashboard/`
- **Target Feature ID**: C20
- **Related PRD Document**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C20_Parent_Dashboard.md`
- **Mapped Screen Count**: 10 Screens Total
- **Primary User Role**: Parent / Guardian
- **Feature Purpose**: Family Learning Overview & Multi-Child Dashboard

---

## 2. Mandatory AI Implementation Directives (Multi-Image Rule)
> **CRITICAL MANDATORY AI INSTRUCTION:**
> For any screen or flow represented by multiple images in this feature, the AI coding agent **MUST read and inspect ALL constituent screen images collectively** before generating any UI, ViewModel, or API binding code.
> The agent must **NOT** implement a partial screen from a single image. It must synthesize all visual states (Initial, Populated, Active Input, Validation Error, Dialogs, Loading Spinners, and Empty States) into a single cohesive, production-ready component.

---

## 3. Exhaustive Screen Inventory & Exact File Paths (10 Screens Total)

| # | Exact Screen Image File Path | Screen Title / Visual State | UI Role | Primary API Dependency |
|---|---|---|---|---|
| 01 | `Screens/Mobile App/Parent Area/Parent Dashboard-01.png` | Parent Dashboard 01 | Parent / Guardian | Sourced from Backend/KMP task files |
| 02 | `Screens/Mobile App/Parent Area/Parent Dashboard-02.png` | Parent Dashboard 02 | Parent / Guardian | Sourced from Backend/KMP task files |
| 03 | `Screens/Mobile App/Parent Area/Parent Dashboard-03.png` | Parent Dashboard 03 | Parent / Guardian | Sourced from Backend/KMP task files |
| 04 | `Screens/Mobile App/Parent Area/Parent Dashboard-04.png` | Parent Dashboard 04 | Parent / Guardian | Sourced from Backend/KMP task files |
| 05 | `Screens/Mobile App/Parent Area/Parent Dashboard-05.png` | Parent Dashboard 05 | Parent / Guardian | Sourced from Backend/KMP task files |
| 06 | `Screens/Mobile App/Parent Area/Parent Dashboard-06.png` | Parent Dashboard 06 | Parent / Guardian | Sourced from Backend/KMP task files |
| 07 | `Screens/Mobile App/Parent Area/Who is Learning?-01.png` | Who is Learning? 01 | Parent / Guardian | Sourced from Backend/KMP task files |
| 08 | `Screens/Mobile App/Parent Area/Who is Learning?-02.png` | Who is Learning? 02 | Parent / Guardian | Sourced from Backend/KMP task files |
| 09 | `Screens/Mobile App/Parent Area/Who is Learning?-03.png` | Who is Learning? 03 | Parent / Guardian | Sourced from Backend/KMP task files |
| 10 | `Screens/Mobile App/Parent Area/Who is Learning?-04.png` | Who is Learning? 04 | Parent / Guardian | Sourced from Backend/KMP task files |

---

## 4. Comprehensive 24-Point Screen Specifications (Applied to All Mapped Screens)

For every screen listed above, future AI coding agents must strictly adhere to the following 24-point implementation contract:

1. **Platform**: Defined per exact image path (Mobile App: Compose Multiplatform / M3; Parent/Admin Web: Next.js 14 App Router / Tailwind / shadcn/ui).
2. **Exact Screen Image Path**: Referenced individually in Section 3 and Section 5 below.
3. **Related PRD Document**: Sourced directly from `PRD_Documents/Parent Area In-App (19-26)/Feature_C20_Parent_Dashboard.md`.
4. **Related PRD Section/Feature**: Specified in the corresponding feature task markdown files.
5. **Purpose of the Screen**: Accurate visual and interactive reproduction of the design mockups.
6. **User Role**: `Parent / Guardian`.
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

### Screen 01: `Parent Dashboard-01.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Parent Area/Parent Dashboard-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C20_Parent_Dashboard.md`
- **4. Purpose**: Render Parent Dashboard 01 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 02: `Parent Dashboard-02.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Parent Area/Parent Dashboard-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C20_Parent_Dashboard.md`
- **4. Purpose**: Render Parent Dashboard 02 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 03: `Parent Dashboard-03.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Parent Area/Parent Dashboard-03.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C20_Parent_Dashboard.md`
- **4. Purpose**: Render Parent Dashboard 03 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 04: `Parent Dashboard-04.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Parent Area/Parent Dashboard-04.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C20_Parent_Dashboard.md`
- **4. Purpose**: Render Parent Dashboard 04 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 05: `Parent Dashboard-05.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Parent Area/Parent Dashboard-05.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C20_Parent_Dashboard.md`
- **4. Purpose**: Render Parent Dashboard 05 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 06: `Parent Dashboard-06.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Parent Area/Parent Dashboard-06.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C20_Parent_Dashboard.md`
- **4. Purpose**: Render Parent Dashboard 06 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 07: `Who is Learning?-01.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Parent Area/Who is Learning?-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C20_Parent_Dashboard.md`
- **4. Purpose**: Render Who is Learning? 01 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 08: `Who is Learning?-02.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Parent Area/Who is Learning?-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C20_Parent_Dashboard.md`
- **4. Purpose**: Render Who is Learning? 02 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 09: `Who is Learning?-03.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Parent Area/Who is Learning?-03.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C20_Parent_Dashboard.md`
- **4. Purpose**: Render Who is Learning? 03 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 10: `Who is Learning?-04.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Parent Area/Who is Learning?-04.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C20_Parent_Dashboard.md`
- **4. Purpose**: Render Who is Learning? 04 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

---

## 6. Future AI Code Generation Instructions
1. Inspect every image listed above in `Screens/` before generating UI code.
2. Implement backend schemas and endpoints in `Backend/` first.
3. Implement KMP / Next.js client models, repositories, and state machines second.
4. Build the UI composables / React components with exact visual fidelity to the provided designs.
