# Visual & System Blueprint: D27 Parent Web Account Portal

## 1. Feature Context & Metadata
- **Feature Directory**: `Development_Blueprints/D27_Parent_Web_Account_Portal/`
- **Target Feature ID**: D27
- **Related PRD Document**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **Mapped Screen Count**: 46 Screens Total
- **Primary User Role**: Parent / Guardian
- **Feature Purpose**: Parent Web Account, Device, Billing & Data Rights Portal

---

## 2. Mandatory AI Implementation Directives (Multi-Image Rule)
> **CRITICAL MANDATORY AI INSTRUCTION:**
> For any screen or flow represented by multiple images in this feature, the AI coding agent **MUST read and inspect ALL constituent screen images collectively** before generating any UI, ViewModel, or API binding code.
> The agent must **NOT** implement a partial screen from a single image. It must synthesize all visual states (Initial, Populated, Active Input, Validation Error, Dialogs, Loading Spinners, and Empty States) into a single cohesive, production-ready component.

---

## 3. Exhaustive Screen Inventory & Exact File Paths (46 Screens Total)

| # | Exact Screen Image File Path | Screen Title / Visual State | UI Role | Primary API Dependency |
|---|---|---|---|---|
| 01 | `Screens/Parent Web/01-Sign in to your account-01.png` | 01 Sign in to your account 01 | Parent / Guardian | Sourced from Backend/KMP task files |
| 02 | `Screens/Parent Web/01-Sign in to your account-02.png` | 01 Sign in to your account 02 | Parent / Guardian | Sourced from Backend/KMP task files |
| 03 | `Screens/Parent Web/02-signin-otp-01.png` | 02 signin otp 01 | Parent / Guardian | Sourced from Backend/KMP task files |
| 04 | `Screens/Parent Web/02-signin-otp-02.png` | 02 signin otp 02 | Parent / Guardian | Sourced from Backend/KMP task files |
| 05 | `Screens/Parent Web/03-Account Home.png` | 03 Account Home | Parent / Guardian | Sourced from Backend/KMP task files |
| 06 | `Screens/Parent Web/04-Account & Security-01.png` | 04 Account & Security 01 | Parent / Guardian | Sourced from Backend/KMP task files |
| 07 | `Screens/Parent Web/04-Account & Security-02.png` | 04 Account & Security 02 | Parent / Guardian | Sourced from Backend/KMP task files |
| 08 | `Screens/Parent Web/04-Account & Security-03.png` | 04 Account & Security 03 | Parent / Guardian | Sourced from Backend/KMP task files |
| 09 | `Screens/Parent Web/04-Account & Security-04.png` | 04 Account & Security 04 | Parent / Guardian | Sourced from Backend/KMP task files |
| 10 | `Screens/Parent Web/04-Account & Security-05.png` | 04 Account & Security 05 | Parent / Guardian | Sourced from Backend/KMP task files |
| 11 | `Screens/Parent Web/04-Account & Security-06.png` | 04 Account & Security 06 | Parent / Guardian | Sourced from Backend/KMP task files |
| 12 | `Screens/Parent Web/04-Account & Security-07.png` | 04 Account & Security 07 | Parent / Guardian | Sourced from Backend/KMP task files |
| 13 | `Screens/Parent Web/04-Account & Security-08.png` | 04 Account & Security 08 | Parent / Guardian | Sourced from Backend/KMP task files |
| 14 | `Screens/Parent Web/04-Account & Security-09.png` | 04 Account & Security 09 | Parent / Guardian | Sourced from Backend/KMP task files |
| 15 | `Screens/Parent Web/05-Connected Devices-01.png` | 05 Connected Devices 01 | Parent / Guardian | Sourced from Backend/KMP task files |
| 16 | `Screens/Parent Web/05-Connected Devices-02.png` | 05 Connected Devices 02 | Parent / Guardian | Sourced from Backend/KMP task files |
| 17 | `Screens/Parent Web/05-Connected Devices-03.png` | 05 Connected Devices 03 | Parent / Guardian | Sourced from Backend/KMP task files |
| 18 | `Screens/Parent Web/05-Connected Devices-04.png` | 05 Connected Devices 04 | Parent / Guardian | Sourced from Backend/KMP task files |
| 19 | `Screens/Parent Web/06-Subscription & Invoices-01.png` | 06 Subscription & Invoices 01 | Parent / Guardian | Sourced from Backend/KMP task files |
| 20 | `Screens/Parent Web/06-Subscription & Invoices-02.png` | 06 Subscription & Invoices 02 | Parent / Guardian | Sourced from Backend/KMP task files |
| 21 | `Screens/Parent Web/06-Subscription & Invoices-03.png` | 06 Subscription & Invoices 03 | Parent / Guardian | Sourced from Backend/KMP task files |
| 22 | `Screens/Parent Web/06-Subscription & Invoices-04.png` | 06 Subscription & Invoices 04 | Parent / Guardian | Sourced from Backend/KMP task files |
| 23 | `Screens/Parent Web/06-Subscription & Invoices-05.png` | 06 Subscription & Invoices 05 | Parent / Guardian | Sourced from Backend/KMP task files |
| 24 | `Screens/Parent Web/06-Subscription & Invoices-06.png` | 06 Subscription & Invoices 06 | Parent / Guardian | Sourced from Backend/KMP task files |
| 25 | `Screens/Parent Web/06-Subscription & Invoices-07.png` | 06 Subscription & Invoices 07 | Parent / Guardian | Sourced from Backend/KMP task files |
| 26 | `Screens/Parent Web/07-Consent & Privacy-01.png` | 07 Consent & Privacy 01 | Parent / Guardian | Sourced from Backend/KMP task files |
| 27 | `Screens/Parent Web/07-Consent & Privacy-02.png` | 07 Consent & Privacy 02 | Parent / Guardian | Sourced from Backend/KMP task files |
| 28 | `Screens/Parent Web/07-Consent & Privacy-03.png` | 07 Consent & Privacy 03 | Parent / Guardian | Sourced from Backend/KMP task files |
| 29 | `Screens/Parent Web/07-Consent & Privacy-04.png` | 07 Consent & Privacy 04 | Parent / Guardian | Sourced from Backend/KMP task files |
| 30 | `Screens/Parent Web/07-Consent & Privacy-05.png` | 07 Consent & Privacy 05 | Parent / Guardian | Sourced from Backend/KMP task files |
| 31 | `Screens/Parent Web/08-Data Export-01.png` | 08 Data Export 01 | Parent / Guardian | Sourced from Backend/KMP task files |
| 32 | `Screens/Parent Web/08-Data Export-02.png` | 08 Data Export 02 | Parent / Guardian | Sourced from Backend/KMP task files |
| 33 | `Screens/Parent Web/08-Data Export-03.png` | 08 Data Export 03 | Parent / Guardian | Sourced from Backend/KMP task files |
| 34 | `Screens/Parent Web/08-Data Export-04.png` | 08 Data Export 04 | Parent / Guardian | Sourced from Backend/KMP task files |
| 35 | `Screens/Parent Web/08-Data Export-05.png` | 08 Data Export 05 | Parent / Guardian | Sourced from Backend/KMP task files |
| 36 | `Screens/Parent Web/08-Data Export-06.png` | 08 Data Export 06 | Parent / Guardian | Sourced from Backend/KMP task files |
| 37 | `Screens/Parent Web/08-Data Export-07.png` | 08 Data Export 07 | Parent / Guardian | Sourced from Backend/KMP task files |
| 38 | `Screens/Parent Web/09-Account Deletion-01.png` | 09 Account Deletion 01 | Parent / Guardian | Sourced from Backend/KMP task files |
| 39 | `Screens/Parent Web/09-Account Deletion-02.png` | 09 Account Deletion 02 | Parent / Guardian | Sourced from Backend/KMP task files |
| 40 | `Screens/Parent Web/09-Account Deletion-03.png` | 09 Account Deletion 03 | Parent / Guardian | Sourced from Backend/KMP task files |
| 41 | `Screens/Parent Web/09-Account Deletion-04.png` | 09 Account Deletion 04 | Parent / Guardian | Sourced from Backend/KMP task files |
| 42 | `Screens/Parent Web/09-Account Deletion-05.png` | 09 Account Deletion 05 | Parent / Guardian | Sourced from Backend/KMP task files |
| 43 | `Screens/Parent Web/10-Account Deletion Pending-01.png` | 10 Account Deletion Pending 01 | Parent / Guardian | Sourced from Backend/KMP task files |
| 44 | `Screens/Parent Web/10-Account Deletion Pending-02.png` | 10 Account Deletion Pending 02 | Parent / Guardian | Sourced from Backend/KMP task files |
| 45 | `Screens/Parent Web/11-Support-01.png` | 11 Support 01 | Parent / Guardian | Sourced from Backend/KMP task files |
| 46 | `Screens/Parent Web/11-Support-02.png` | 11 Support 02 | Parent / Guardian | Sourced from Backend/KMP task files |

---

## 4. Comprehensive 24-Point Screen Specifications (Applied to All Mapped Screens)

For every screen listed above, future AI coding agents must strictly adhere to the following 24-point implementation contract:

1. **Platform**: Defined per exact image path (Mobile App: Compose Multiplatform / M3; Parent/Admin Web: Next.js 14 App Router / Tailwind / shadcn/ui).
2. **Exact Screen Image Path**: Referenced individually in Section 3 and Section 5 below.
3. **Related PRD Document**: Sourced directly from `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`.
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

### Screen 01: `01-Sign in to your account-01.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/01-Sign in to your account-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 01 Sign in to your account 01 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 02: `01-Sign in to your account-02.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/01-Sign in to your account-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 01 Sign in to your account 02 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 03: `02-signin-otp-01.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/02-signin-otp-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 02 signin otp 01 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 04: `02-signin-otp-02.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/02-signin-otp-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 02 signin otp 02 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 05: `03-Account Home.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/03-Account Home.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 03 Account Home with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 06: `04-Account & Security-01.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/04-Account & Security-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 04 Account & Security 01 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 07: `04-Account & Security-02.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/04-Account & Security-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 04 Account & Security 02 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 08: `04-Account & Security-03.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/04-Account & Security-03.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 04 Account & Security 03 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 09: `04-Account & Security-04.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/04-Account & Security-04.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 04 Account & Security 04 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 10: `04-Account & Security-05.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/04-Account & Security-05.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 04 Account & Security 05 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 11: `04-Account & Security-06.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/04-Account & Security-06.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 04 Account & Security 06 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 12: `04-Account & Security-07.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/04-Account & Security-07.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 04 Account & Security 07 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 13: `04-Account & Security-08.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/04-Account & Security-08.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 04 Account & Security 08 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 14: `04-Account & Security-09.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/04-Account & Security-09.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 04 Account & Security 09 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 15: `05-Connected Devices-01.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/05-Connected Devices-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 05 Connected Devices 01 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 16: `05-Connected Devices-02.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/05-Connected Devices-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 05 Connected Devices 02 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 17: `05-Connected Devices-03.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/05-Connected Devices-03.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 05 Connected Devices 03 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 18: `05-Connected Devices-04.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/05-Connected Devices-04.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 05 Connected Devices 04 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 19: `06-Subscription & Invoices-01.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/06-Subscription & Invoices-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 06 Subscription & Invoices 01 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 20: `06-Subscription & Invoices-02.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/06-Subscription & Invoices-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 06 Subscription & Invoices 02 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 21: `06-Subscription & Invoices-03.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/06-Subscription & Invoices-03.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 06 Subscription & Invoices 03 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 22: `06-Subscription & Invoices-04.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/06-Subscription & Invoices-04.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 06 Subscription & Invoices 04 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 23: `06-Subscription & Invoices-05.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/06-Subscription & Invoices-05.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 06 Subscription & Invoices 05 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 24: `06-Subscription & Invoices-06.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/06-Subscription & Invoices-06.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 06 Subscription & Invoices 06 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 25: `06-Subscription & Invoices-07.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/06-Subscription & Invoices-07.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 06 Subscription & Invoices 07 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 26: `07-Consent & Privacy-01.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/07-Consent & Privacy-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 07 Consent & Privacy 01 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 27: `07-Consent & Privacy-02.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/07-Consent & Privacy-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 07 Consent & Privacy 02 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 28: `07-Consent & Privacy-03.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/07-Consent & Privacy-03.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 07 Consent & Privacy 03 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 29: `07-Consent & Privacy-04.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/07-Consent & Privacy-04.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 07 Consent & Privacy 04 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 30: `07-Consent & Privacy-05.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/07-Consent & Privacy-05.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 07 Consent & Privacy 05 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 31: `08-Data Export-01.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/08-Data Export-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 08 Data Export 01 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 32: `08-Data Export-02.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/08-Data Export-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 08 Data Export 02 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 33: `08-Data Export-03.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/08-Data Export-03.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 08 Data Export 03 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 34: `08-Data Export-04.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/08-Data Export-04.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 08 Data Export 04 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 35: `08-Data Export-05.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/08-Data Export-05.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 08 Data Export 05 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 36: `08-Data Export-06.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/08-Data Export-06.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 08 Data Export 06 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 37: `08-Data Export-07.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/08-Data Export-07.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 08 Data Export 07 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 38: `09-Account Deletion-01.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/09-Account Deletion-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 09 Account Deletion 01 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 39: `09-Account Deletion-02.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/09-Account Deletion-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 09 Account Deletion 02 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 40: `09-Account Deletion-03.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/09-Account Deletion-03.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 09 Account Deletion 03 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 41: `09-Account Deletion-04.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/09-Account Deletion-04.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 09 Account Deletion 04 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 42: `09-Account Deletion-05.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/09-Account Deletion-05.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 09 Account Deletion 05 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 43: `10-Account Deletion Pending-01.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/10-Account Deletion Pending-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 10 Account Deletion Pending 01 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 44: `10-Account Deletion Pending-02.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/10-Account Deletion Pending-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 10 Account Deletion Pending 02 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 45: `11-Support-01.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/11-Support-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 11 Support 01 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 46: `11-Support-02.png`
- **1. Platform**: Parent Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Parent Web/11-Support-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Web Portal (27)/Feature_D27_Parent_Web_Account_Portal.md`
- **4. Purpose**: Render 11 Support 02 with full visual fidelity to design assets.
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
