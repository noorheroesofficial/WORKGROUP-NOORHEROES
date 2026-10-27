# Visual & System Blueprint: E34 Localization Management

## 1. Feature Context & Metadata
- **Feature Directory**: `Development_Blueprints/E34_Localization_Management/`
- **Target Feature ID**: E34
- **Related PRD Document**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E34_Localization_Management.md`
- **Mapped Screen Count**: 15 Screens Total
- **Primary User Role**: Localization Lead & Translators
- **Feature Purpose**: Multi-Language String Tables, RTL Preview & Translation Coverage

---

## 2. Mandatory AI Implementation Directives (Multi-Image Rule)
> **CRITICAL MANDATORY AI INSTRUCTION:**
> For any screen or flow represented by multiple images in this feature, the AI coding agent **MUST read and inspect ALL constituent screen images collectively** before generating any UI, ViewModel, or API binding code.
> The agent must **NOT** implement a partial screen from a single image. It must synthesize all visual states (Initial, Populated, Active Input, Validation Error, Dialogs, Loading Spinners, and Empty States) into a single cohesive, production-ready component.

---

## 3. Exhaustive Screen Inventory & Exact File Paths (15 Screens Total)

| # | Exact Screen Image File Path | Screen Title / Visual State | UI Role | Primary API Dependency |
|---|---|---|---|---|
| 01 | `Screens/Admin Web/102-App Configuration-01.png` | 102 App Configuration 01 | Localization Lead & Translators | Sourced from Backend/KMP task files |
| 02 | `Screens/Admin Web/102-App Configuration-02.png` | 102 App Configuration 02 | Localization Lead & Translators | Sourced from Backend/KMP task files |
| 03 | `Screens/Admin Web/103-String Table Editor-01.png` | 103 String Table Editor 01 | Localization Lead & Translators | Sourced from Backend/KMP task files |
| 04 | `Screens/Admin Web/103-String Table Editor-02.png` | 103 String Table Editor 02 | Localization Lead & Translators | Sourced from Backend/KMP task files |
| 05 | `Screens/Admin Web/103-String Table Editor-03.png` | 103 String Table Editor 03 | Localization Lead & Translators | Sourced from Backend/KMP task files |
| 06 | `Screens/Admin Web/104-String table String Detail-01.png` | 104 String table String Detail 01 | Localization Lead & Translators | Sourced from Backend/KMP task files |
| 07 | `Screens/Admin Web/104-String table String Detail-02.png` | 104 String table String Detail 02 | Localization Lead & Translators | Sourced from Backend/KMP task files |
| 08 | `Screens/Admin Web/105-Translation Coverage Dashboard-01.png` | 105 Translation Coverage Dashboard 01 | Localization Lead & Translators | Sourced from Backend/KMP task files |
| 09 | `Screens/Admin Web/105-Translation Coverage Dashboard-02.png` | 105 Translation Coverage Dashboard 02 | Localization Lead & Translators | Sourced from Backend/KMP task files |
| 10 | `Screens/Admin Web/106-RTL Preview.png` | 106 RTL Preview | Localization Lead & Translators | Sourced from Backend/KMP task files |
| 11 | `Screens/Admin Web/107-Locale Activation- Urdu (ur).png` | 107 Locale Activation  Urdu (ur) | Localization Lead & Translators | Sourced from Backend/KMP task files |
| 12 | `Screens/Admin Web/108-Locale List-01.png` | 108 Locale List 01 | Localization Lead & Translators | Sourced from Backend/KMP task files |
| 13 | `Screens/Admin Web/108-Locale List-02.png` | 108 Locale List 02 | Localization Lead & Translators | Sourced from Backend/KMP task files |
| 14 | `Screens/Admin Web/109-Locale Chain Configuration.png` | 109 Locale Chain Configuration | Localization Lead & Translators | Sourced from Backend/KMP task files |
| 15 | `Screens/Admin Web/110-Coverage-Drop Alert Monitor.png` | 110 Coverage Drop Alert Monitor | Localization Lead & Translators | Sourced from Backend/KMP task files |

---

## 4. Comprehensive 24-Point Screen Specifications (Applied to All Mapped Screens)

For every screen listed above, future AI coding agents must strictly adhere to the following 24-point implementation contract:

1. **Platform**: Defined per exact image path (Mobile App: Compose Multiplatform / M3; Parent/Admin Web: Next.js 14 App Router / Tailwind / shadcn/ui).
2. **Exact Screen Image Path**: Referenced individually in Section 3 and Section 5 below.
3. **Related PRD Document**: Sourced directly from `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E34_Localization_Management.md`.
4. **Related PRD Section/Feature**: Specified in the corresponding feature task markdown files.
5. **Purpose of the Screen**: Accurate visual and interactive reproduction of the design mockups.
6. **User Role**: `Localization Lead & Translators`.
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

### Screen 01: `102-App Configuration-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/102-App Configuration-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E34_Localization_Management.md`
- **4. Purpose**: Render 102 App Configuration 01 with full visual fidelity to design assets.
- **5. User Role**: Localization Lead & Translators
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 02: `102-App Configuration-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/102-App Configuration-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E34_Localization_Management.md`
- **4. Purpose**: Render 102 App Configuration 02 with full visual fidelity to design assets.
- **5. User Role**: Localization Lead & Translators
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 03: `103-String Table Editor-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/103-String Table Editor-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E34_Localization_Management.md`
- **4. Purpose**: Render 103 String Table Editor 01 with full visual fidelity to design assets.
- **5. User Role**: Localization Lead & Translators
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 04: `103-String Table Editor-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/103-String Table Editor-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E34_Localization_Management.md`
- **4. Purpose**: Render 103 String Table Editor 02 with full visual fidelity to design assets.
- **5. User Role**: Localization Lead & Translators
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 05: `103-String Table Editor-03.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/103-String Table Editor-03.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E34_Localization_Management.md`
- **4. Purpose**: Render 103 String Table Editor 03 with full visual fidelity to design assets.
- **5. User Role**: Localization Lead & Translators
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 06: `104-String table String Detail-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/104-String table String Detail-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E34_Localization_Management.md`
- **4. Purpose**: Render 104 String table String Detail 01 with full visual fidelity to design assets.
- **5. User Role**: Localization Lead & Translators
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 07: `104-String table String Detail-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/104-String table String Detail-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E34_Localization_Management.md`
- **4. Purpose**: Render 104 String table String Detail 02 with full visual fidelity to design assets.
- **5. User Role**: Localization Lead & Translators
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 08: `105-Translation Coverage Dashboard-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/105-Translation Coverage Dashboard-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E34_Localization_Management.md`
- **4. Purpose**: Render 105 Translation Coverage Dashboard 01 with full visual fidelity to design assets.
- **5. User Role**: Localization Lead & Translators
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 09: `105-Translation Coverage Dashboard-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/105-Translation Coverage Dashboard-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E34_Localization_Management.md`
- **4. Purpose**: Render 105 Translation Coverage Dashboard 02 with full visual fidelity to design assets.
- **5. User Role**: Localization Lead & Translators
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 10: `106-RTL Preview.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/106-RTL Preview.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E34_Localization_Management.md`
- **4. Purpose**: Render 106 RTL Preview with full visual fidelity to design assets.
- **5. User Role**: Localization Lead & Translators
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 11: `107-Locale Activation- Urdu (ur).png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/107-Locale Activation- Urdu (ur).png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E34_Localization_Management.md`
- **4. Purpose**: Render 107 Locale Activation  Urdu (ur) with full visual fidelity to design assets.
- **5. User Role**: Localization Lead & Translators
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 12: `108-Locale List-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/108-Locale List-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E34_Localization_Management.md`
- **4. Purpose**: Render 108 Locale List 01 with full visual fidelity to design assets.
- **5. User Role**: Localization Lead & Translators
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 13: `108-Locale List-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/108-Locale List-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E34_Localization_Management.md`
- **4. Purpose**: Render 108 Locale List 02 with full visual fidelity to design assets.
- **5. User Role**: Localization Lead & Translators
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 14: `109-Locale Chain Configuration.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/109-Locale Chain Configuration.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E34_Localization_Management.md`
- **4. Purpose**: Render 109 Locale Chain Configuration with full visual fidelity to design assets.
- **5. User Role**: Localization Lead & Translators
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 15: `110-Coverage-Drop Alert Monitor.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/110-Coverage-Drop Alert Monitor.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E34_Localization_Management.md`
- **4. Purpose**: Render 110 Coverage Drop Alert Monitor with full visual fidelity to design assets.
- **5. User Role**: Localization Lead & Translators
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

---

## 6. Future AI Code Generation Instructions
1. Inspect every image listed above in `Screens/` before generating UI code.
2. Implement backend schemas and endpoints in `Backend/` first.
3. Implement KMP / Next.js client models, repositories, and state machines second.
4. Build the UI composables / React components with exact visual fidelity to the provided designs.
