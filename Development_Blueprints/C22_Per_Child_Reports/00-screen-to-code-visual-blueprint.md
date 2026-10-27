# Visual & System Blueprint: C22 Per Child Reports

## 1. Feature Context & Metadata
- **Feature Directory**: `Development_Blueprints/C22_Per_Child_Reports/`
- **Target Feature ID**: C22
- **Related PRD Document**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`
- **Mapped Screen Count**: 16 Screens Total
- **Primary User Role**: Parent / Guardian
- **Feature Purpose**: In-Depth Weekly Learning Analytics & Milestones

---

## 2. Mandatory AI Implementation Directives (Multi-Image Rule)
> **CRITICAL MANDATORY AI INSTRUCTION:**
> For any screen or flow represented by multiple images in this feature, the AI coding agent **MUST read and inspect ALL constituent screen images collectively** before generating any UI, ViewModel, or API binding code.
> The agent must **NOT** implement a partial screen from a single image. It must synthesize all visual states (Initial, Populated, Active Input, Validation Error, Dialogs, Loading Spinners, and Empty States) into a single cohesive, production-ready component.

---

## 3. Exhaustive Screen Inventory & Exact File Paths (16 Screens Total)

| # | Exact Screen Image File Path | Screen Title / Visual State | UI Role | Primary API Dependency |
|---|---|---|---|---|
| 01 | `Screens/Mobile App/Child Reports/Per-Child Report-01.png` | Per Child Report 01 | Parent / Guardian | Sourced from Backend/KMP task files |
| 02 | `Screens/Mobile App/Child Reports/Per-Child Report-02.png` | Per Child Report 02 | Parent / Guardian | Sourced from Backend/KMP task files |
| 03 | `Screens/Mobile App/Child Reports/Per-Child Report-03.png` | Per Child Report 03 | Parent / Guardian | Sourced from Backend/KMP task files |
| 04 | `Screens/Mobile App/Child Reports/Per-Child Report-04.png` | Per Child Report 04 | Parent / Guardian | Sourced from Backend/KMP task files |
| 05 | `Screens/Mobile App/Child Reports/Per-Child Report-05.png` | Per Child Report 05 | Parent / Guardian | Sourced from Backend/KMP task files |
| 06 | `Screens/Mobile App/Child Reports/Per-Child Report-06.png` | Per Child Report 06 | Parent / Guardian | Sourced from Backend/KMP task files |
| 07 | `Screens/Mobile App/Child Reports/Per-Child Report-07.png` | Per Child Report 07 | Parent / Guardian | Sourced from Backend/KMP task files |
| 08 | `Screens/Mobile App/Child Reports/Per-Child Report-08.png` | Per Child Report 08 | Parent / Guardian | Sourced from Backend/KMP task files |
| 09 | `Screens/Mobile App/Child Reports/Per-Child Report-09.png` | Per Child Report 09 | Parent / Guardian | Sourced from Backend/KMP task files |
| 10 | `Screens/Mobile App/Child Reports/Per-Child Report-10.png` | Per Child Report 10 | Parent / Guardian | Sourced from Backend/KMP task files |
| 11 | `Screens/Mobile App/Child Reports/Per-Child Report-11.png` | Per Child Report 11 | Parent / Guardian | Sourced from Backend/KMP task files |
| 12 | `Screens/Mobile App/Child Reports/Per-Child Report-12.png` | Per Child Report 12 | Parent / Guardian | Sourced from Backend/KMP task files |
| 13 | `Screens/Mobile App/Child Reports/Screenshot 2026-08-25 at 1.49.50 PM.png` | Screenshot 2026 08 25 at 1.49.50 PM | Parent / Guardian | Sourced from Backend/KMP task files |
| 14 | `Screens/Mobile App/Child Reports/Screenshot 2026-08-25 at 1.49.59 PM.png` | Screenshot 2026 08 25 at 1.49.59 PM | Parent / Guardian | Sourced from Backend/KMP task files |
| 15 | `Screens/Mobile App/Child Reports/Screenshot 2026-08-25 at 1.50.16 PM.png` | Screenshot 2026 08 25 at 1.50.16 PM | Parent / Guardian | Sourced from Backend/KMP task files |
| 16 | `Screens/Mobile App/Child Reports/Screenshot 2026-08-25 at 1.50.22 PM.png` | Screenshot 2026 08 25 at 1.50.22 PM | Parent / Guardian | Sourced from Backend/KMP task files |

---

## 4. Comprehensive 24-Point Screen Specifications (Applied to All Mapped Screens)

For every screen listed above, future AI coding agents must strictly adhere to the following 24-point implementation contract:

1. **Platform**: Defined per exact image path (Mobile App: Compose Multiplatform / M3; Parent/Admin Web: Next.js 14 App Router / Tailwind / shadcn/ui).
2. **Exact Screen Image Path**: Referenced individually in Section 3 and Section 5 below.
3. **Related PRD Document**: Sourced directly from `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`.
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

### Screen 01: `Per-Child Report-01.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Child Reports/Per-Child Report-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`
- **4. Purpose**: Render Per Child Report 01 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 02: `Per-Child Report-02.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Child Reports/Per-Child Report-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`
- **4. Purpose**: Render Per Child Report 02 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 03: `Per-Child Report-03.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Child Reports/Per-Child Report-03.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`
- **4. Purpose**: Render Per Child Report 03 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 04: `Per-Child Report-04.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Child Reports/Per-Child Report-04.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`
- **4. Purpose**: Render Per Child Report 04 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 05: `Per-Child Report-05.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Child Reports/Per-Child Report-05.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`
- **4. Purpose**: Render Per Child Report 05 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 06: `Per-Child Report-06.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Child Reports/Per-Child Report-06.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`
- **4. Purpose**: Render Per Child Report 06 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 07: `Per-Child Report-07.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Child Reports/Per-Child Report-07.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`
- **4. Purpose**: Render Per Child Report 07 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 08: `Per-Child Report-08.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Child Reports/Per-Child Report-08.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`
- **4. Purpose**: Render Per Child Report 08 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 09: `Per-Child Report-09.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Child Reports/Per-Child Report-09.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`
- **4. Purpose**: Render Per Child Report 09 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 10: `Per-Child Report-10.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Child Reports/Per-Child Report-10.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`
- **4. Purpose**: Render Per Child Report 10 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 11: `Per-Child Report-11.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Child Reports/Per-Child Report-11.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`
- **4. Purpose**: Render Per Child Report 11 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 12: `Per-Child Report-12.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Child Reports/Per-Child Report-12.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`
- **4. Purpose**: Render Per Child Report 12 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 13: `Screenshot 2026-08-25 at 1.49.50 PM.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Child Reports/Screenshot 2026-08-25 at 1.49.50 PM.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`
- **4. Purpose**: Render Screenshot 2026 08 25 at 1.49.50 PM with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 14: `Screenshot 2026-08-25 at 1.49.59 PM.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Child Reports/Screenshot 2026-08-25 at 1.49.59 PM.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`
- **4. Purpose**: Render Screenshot 2026 08 25 at 1.49.59 PM with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 15: `Screenshot 2026-08-25 at 1.50.16 PM.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Child Reports/Screenshot 2026-08-25 at 1.50.16 PM.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`
- **4. Purpose**: Render Screenshot 2026 08 25 at 1.50.16 PM with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 16: `Screenshot 2026-08-25 at 1.50.22 PM.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Child Reports/Screenshot 2026-08-25 at 1.50.22 PM.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C22_Per_Child_Reports.md`
- **4. Purpose**: Render Screenshot 2026 08 25 at 1.50.22 PM with full visual fidelity to design assets.
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
