# Visual & System Blueprint: C26 Privacy Consent Account Security Data Rights

## 1. Feature Context & Metadata
- **Feature Directory**: `Development_Blueprints/C26_Privacy_Consent_Account_Security_Data_Rights/`
- **Target Feature ID**: C26
- **Related PRD Document**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md`
- **Mapped Screen Count**: 14 Screens Total
- **Primary User Role**: Parent / Guardian
- **Feature Purpose**: COPPA/GDPR-K Legal Consents, Audit Logs & Instant AI Purge

---

## 2. Mandatory AI Implementation Directives (Multi-Image Rule)
> **CRITICAL MANDATORY AI INSTRUCTION:**
> For any screen or flow represented by multiple images in this feature, the AI coding agent **MUST read and inspect ALL constituent screen images collectively** before generating any UI, ViewModel, or API binding code.
> The agent must **NOT** implement a partial screen from a single image. It must synthesize all visual states (Initial, Populated, Active Input, Validation Error, Dialogs, Loading Spinners, and Empty States) into a single cohesive, production-ready component.

---

## 3. Exhaustive Screen Inventory & Exact File Paths (14 Screens Total)

| # | Exact Screen Image File Path | Screen Title / Visual State | UI Role | Primary API Dependency |
|---|---|---|---|---|
| 01 | `Screens/Mobile App/Privacy/AI History-01.png` | AI History 01 | Parent / Guardian | Sourced from Backend/KMP task files |
| 02 | `Screens/Mobile App/Privacy/AI History-02.png` | AI History 02 | Parent / Guardian | Sourced from Backend/KMP task files |
| 03 | `Screens/Mobile App/Privacy/AI History-03.png` | AI History 03 | Parent / Guardian | Sourced from Backend/KMP task files |
| 04 | `Screens/Mobile App/Privacy/Consent Log-01.png` | Consent Log 01 | Parent / Guardian | Sourced from Backend/KMP task files |
| 05 | `Screens/Mobile App/Privacy/Consent Log-02.png` | Consent Log 02 | Parent / Guardian | Sourced from Backend/KMP task files |
| 06 | `Screens/Mobile App/Privacy/Consent Log-03.png` | Consent Log 03 | Parent / Guardian | Sourced from Backend/KMP task files |
| 07 | `Screens/Mobile App/Privacy/Consent Log-04.png` | Consent Log 04 | Parent / Guardian | Sourced from Backend/KMP task files |
| 08 | `Screens/Mobile App/Privacy/Consent Log-05.png` | Consent Log 05 | Parent / Guardian | Sourced from Backend/KMP task files |
| 09 | `Screens/Mobile App/Privacy/Consent Log-06.png` | Consent Log 06 | Parent / Guardian | Sourced from Backend/KMP task files |
| 10 | `Screens/Mobile App/Privacy/Privacy & Data-01.png` | Privacy & Data 01 | Parent / Guardian | Sourced from Backend/KMP task files |
| 11 | `Screens/Mobile App/Privacy/Privacy & Data-02.png` | Privacy & Data 02 | Parent / Guardian | Sourced from Backend/KMP task files |
| 12 | `Screens/Mobile App/Privacy/Privacy & Data-03.png` | Privacy & Data 03 | Parent / Guardian | Sourced from Backend/KMP task files |
| 13 | `Screens/Mobile App/Privacy/Privacy & Data-04.png` | Privacy & Data 04 | Parent / Guardian | Sourced from Backend/KMP task files |
| 14 | `Screens/Mobile App/Privacy/Privacy & Data-05.png` | Privacy & Data 05 | Parent / Guardian | Sourced from Backend/KMP task files |

---

## 4. Comprehensive 24-Point Screen Specifications (Applied to All Mapped Screens)

For every screen listed above, future AI coding agents must strictly adhere to the following 24-point implementation contract:

1. **Platform**: Defined per exact image path (Mobile App: Compose Multiplatform / M3; Parent/Admin Web: Next.js 14 App Router / Tailwind / shadcn/ui).
2. **Exact Screen Image Path**: Referenced individually in Section 3 and Section 5 below.
3. **Related PRD Document**: Sourced directly from `PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md`.
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

### Screen 01: `AI History-01.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Privacy/AI History-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md`
- **4. Purpose**: Render AI History 01 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 02: `AI History-02.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Privacy/AI History-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md`
- **4. Purpose**: Render AI History 02 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 03: `AI History-03.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Privacy/AI History-03.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md`
- **4. Purpose**: Render AI History 03 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 04: `Consent Log-01.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Privacy/Consent Log-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md`
- **4. Purpose**: Render Consent Log 01 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 05: `Consent Log-02.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Privacy/Consent Log-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md`
- **4. Purpose**: Render Consent Log 02 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 06: `Consent Log-03.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Privacy/Consent Log-03.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md`
- **4. Purpose**: Render Consent Log 03 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 07: `Consent Log-04.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Privacy/Consent Log-04.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md`
- **4. Purpose**: Render Consent Log 04 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 08: `Consent Log-05.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Privacy/Consent Log-05.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md`
- **4. Purpose**: Render Consent Log 05 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 09: `Consent Log-06.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Privacy/Consent Log-06.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md`
- **4. Purpose**: Render Consent Log 06 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 10: `Privacy & Data-01.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Privacy/Privacy & Data-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md`
- **4. Purpose**: Render Privacy & Data 01 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 11: `Privacy & Data-02.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Privacy/Privacy & Data-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md`
- **4. Purpose**: Render Privacy & Data 02 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 12: `Privacy & Data-03.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Privacy/Privacy & Data-03.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md`
- **4. Purpose**: Render Privacy & Data 03 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 13: `Privacy & Data-04.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Privacy/Privacy & Data-04.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md`
- **4. Purpose**: Render Privacy & Data 04 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 14: `Privacy & Data-05.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Privacy/Privacy & Data-05.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md`
- **4. Purpose**: Render Privacy & Data 05 with full visual fidelity to design assets.
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
