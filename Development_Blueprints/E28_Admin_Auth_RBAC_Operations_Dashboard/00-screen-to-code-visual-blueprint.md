# Visual & System Blueprint: E28 Admin Auth RBAC Operations Dashboard

## 1. Feature Context & Metadata
- **Feature Directory**: `Development_Blueprints/E28_Admin_Auth_RBAC_Operations_Dashboard/`
- **Target Feature ID**: E28
- **Related PRD Document**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **Mapped Screen Count**: 25 Screens Total
- **Primary User Role**: Super Admin & Ops
- **Feature Purpose**: Admin Auth, 9-Role RBAC Matrix, Operations KPIs & Service Health

---

## 2. Mandatory AI Implementation Directives (Multi-Image Rule)
> **CRITICAL MANDATORY AI INSTRUCTION:**
> For any screen or flow represented by multiple images in this feature, the AI coding agent **MUST read and inspect ALL constituent screen images collectively** before generating any UI, ViewModel, or API binding code.
> The agent must **NOT** implement a partial screen from a single image. It must synthesize all visual states (Initial, Populated, Active Input, Validation Error, Dialogs, Loading Spinners, and Empty States) into a single cohesive, production-ready component.

---

## 3. Exhaustive Screen Inventory & Exact File Paths (25 Screens Total)

| # | Exact Screen Image File Path | Screen Title / Visual State | UI Role | Primary API Dependency |
|---|---|---|---|---|
| 01 | `Screens/Admin Web/01-login.png` | 01 login | Super Admin & Ops | Sourced from Backend/KMP task files |
| 02 | `Screens/Admin Web/02-Two-Factor Authentication.png` | 02 Two Factor Authentication | Super Admin & Ops | Sourced from Backend/KMP task files |
| 03 | `Screens/Admin Web/03-Two-Factor Verification.png` | 03 Two Factor Verification | Super Admin & Ops | Sourced from Backend/KMP task files |
| 04 | `Screens/Admin Web/04-Account Recovery.png` | 04 Account Recovery | Super Admin & Ops | Sourced from Backend/KMP task files |
| 05 | `Screens/Admin Web/05-Operations Dashboard-01.png` | 05 Operations Dashboard 01 | Super Admin & Ops | Sourced from Backend/KMP task files |
| 06 | `Screens/Admin Web/05-Operations Dashboard-02.png` | 05 Operations Dashboard 02 | Super Admin & Ops | Sourced from Backend/KMP task files |
| 07 | `Screens/Admin Web/06.1-Incidents.png` | 06.1 Incidents | Super Admin & Ops | Sourced from Backend/KMP task files |
| 08 | `Screens/Admin Web/06.2-Incidents-Media CDN — Elevated Latency.png` | 06.2 Incidents Media CDN — Elevated Latency | Super Admin & Ops | Sourced from Backend/KMP task files |
| 09 | `Screens/Admin Web/07-Service Health.png` | 07 Service Health | Super Admin & Ops | Sourced from Backend/KMP task files |
| 10 | `Screens/Admin Web/08-Job Failures.png` | 08 Job Failures | Super Admin & Ops | Sourced from Backend/KMP task files |
| 11 | `Screens/Admin Web/100-Feature Flag Change reject.png` | 100 Feature Flag Change reject | Super Admin & Ops | Sourced from Backend/KMP task files |
| 12 | `Screens/Admin Web/101-Audit Log.png` | 101 Audit Log | Super Admin & Ops | Sourced from Backend/KMP task files |
| 13 | `Screens/Admin Web/14-Operator Accounts.png` | 14 Operator Accounts | Super Admin & Ops | Sourced from Backend/KMP task files |
| 14 | `Screens/Admin Web/15-Provision Operator Account-01.png` | 15 Provision Operator Account 01 | Super Admin & Ops | Sourced from Backend/KMP task files |
| 15 | `Screens/Admin Web/15-Provision Operator Account-02.png` | 15 Provision Operator Account 02 | Super Admin & Ops | Sourced from Backend/KMP task files |
| 16 | `Screens/Admin Web/15-Provision Operator Account-03.png` | 15 Provision Operator Account 03 | Super Admin & Ops | Sourced from Backend/KMP task files |
| 17 | `Screens/Admin Web/15-Provision Operator Account-04.png` | 15 Provision Operator Account 04 | Super Admin & Ops | Sourced from Backend/KMP task files |
| 18 | `Screens/Admin Web/95-Roles & Permissions-01.png` | 95 Roles & Permissions 01 | Super Admin & Ops | Sourced from Backend/KMP task files |
| 19 | `Screens/Admin Web/95-Roles & Permissions-02.png` | 95 Roles & Permissions 02 | Super Admin & Ops | Sourced from Backend/KMP task files |
| 20 | `Screens/Admin Web/96-Permission Matrix Super Admin-01.png` | 96 Permission Matrix Super Admin 01 | Super Admin & Ops | Sourced from Backend/KMP task files |
| 21 | `Screens/Admin Web/96-Permission Matrix Super Admin-02.png` | 96 Permission Matrix Super Admin 02 | Super Admin & Ops | Sourced from Backend/KMP task files |
| 22 | `Screens/Admin Web/97-Maker-Checker Approval Queue-01.png` | 97 Maker Checker Approval Queue 01 | Super Admin & Ops | Sourced from Backend/KMP task files |
| 23 | `Screens/Admin Web/97-Maker-Checker Approval Queue-02.png` | 97 Maker Checker Approval Queue 02 | Super Admin & Ops | Sourced from Backend/KMP task files |
| 24 | `Screens/Admin Web/98-Feature Flag Change.png` | 98 Feature Flag Change | Super Admin & Ops | Sourced from Backend/KMP task files |
| 25 | `Screens/Admin Web/99-Feature Flag Change approved.png` | 99 Feature Flag Change approved | Super Admin & Ops | Sourced from Backend/KMP task files |

---

## 4. Comprehensive 24-Point Screen Specifications (Applied to All Mapped Screens)

For every screen listed above, future AI coding agents must strictly adhere to the following 24-point implementation contract:

1. **Platform**: Defined per exact image path (Mobile App: Compose Multiplatform / M3; Parent/Admin Web: Next.js 14 App Router / Tailwind / shadcn/ui).
2. **Exact Screen Image Path**: Referenced individually in Section 3 and Section 5 below.
3. **Related PRD Document**: Sourced directly from `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`.
4. **Related PRD Section/Feature**: Specified in the corresponding feature task markdown files.
5. **Purpose of the Screen**: Accurate visual and interactive reproduction of the design mockups.
6. **User Role**: `Super Admin & Ops`.
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

### Screen 01: `01-login.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/01-login.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 01 login with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 02: `02-Two-Factor Authentication.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/02-Two-Factor Authentication.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 02 Two Factor Authentication with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 03: `03-Two-Factor Verification.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/03-Two-Factor Verification.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 03 Two Factor Verification with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 04: `04-Account Recovery.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/04-Account Recovery.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 04 Account Recovery with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 05: `05-Operations Dashboard-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/05-Operations Dashboard-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 05 Operations Dashboard 01 with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 06: `05-Operations Dashboard-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/05-Operations Dashboard-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 05 Operations Dashboard 02 with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 07: `06.1-Incidents.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/06.1-Incidents.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 06.1 Incidents with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 08: `06.2-Incidents-Media CDN — Elevated Latency.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/06.2-Incidents-Media CDN — Elevated Latency.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 06.2 Incidents Media CDN — Elevated Latency with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 09: `07-Service Health.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/07-Service Health.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 07 Service Health with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 10: `08-Job Failures.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/08-Job Failures.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 08 Job Failures with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 11: `100-Feature Flag Change reject.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/100-Feature Flag Change reject.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 100 Feature Flag Change reject with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 12: `101-Audit Log.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/101-Audit Log.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 101 Audit Log with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 13: `14-Operator Accounts.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/14-Operator Accounts.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 14 Operator Accounts with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 14: `15-Provision Operator Account-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/15-Provision Operator Account-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 15 Provision Operator Account 01 with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 15: `15-Provision Operator Account-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/15-Provision Operator Account-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 15 Provision Operator Account 02 with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 16: `15-Provision Operator Account-03.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/15-Provision Operator Account-03.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 15 Provision Operator Account 03 with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 17: `15-Provision Operator Account-04.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/15-Provision Operator Account-04.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 15 Provision Operator Account 04 with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 18: `95-Roles & Permissions-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/95-Roles & Permissions-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 95 Roles & Permissions 01 with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow (`/platform/roles-permissions`).
- **7. Implementation Files**: `src/app/(dashboard)/platform/roles-permissions/page.tsx`, `src/features/roles-permissions/components/roles-permissions-view.tsx`, `roles-table.tsx`, `create-role-dialog.tsx`.
- **8. API Binding**: `GET /v1/admin/roles` (role listing), `POST /v1/admin/roles` (Super Admin role creation).
- **9. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **10. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 19: `95-Roles & Permissions-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/95-Roles & Permissions-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 95 Roles & Permissions 02 (Create Role modal with permission checkboxes and 2FA toggle).
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Triggered via "Create New Role" in `/platform/roles-permissions`.
- **7. Implementation Files**: `src/features/roles-permissions/components/create-role-dialog.tsx`, `use-roles.ts` (`useCreateRoleMutation`).
- **8. API Binding**: `POST /v1/admin/roles` (Super Admin role creation with composite permissions).
- **9. UI State Handling**: Form validation errors, slug auto-generation, custom scope builder, submit loading spinner, 409 Conflict banner.
- **10. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.


### Screen 20: `96-Permission Matrix Super Admin-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/96-Permission Matrix Super Admin-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 96 Permission Matrix Super Admin 01 with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 21: `96-Permission Matrix Super Admin-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/96-Permission Matrix Super Admin-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 96 Permission Matrix Super Admin 02 with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 22: `97-Maker-Checker Approval Queue-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/97-Maker-Checker Approval Queue-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 97 Maker Checker Approval Queue 01 with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 23: `97-Maker-Checker Approval Queue-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/97-Maker-Checker Approval Queue-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 97 Maker Checker Approval Queue 02 with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 24: `98-Feature Flag Change.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/98-Feature Flag Change.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 98 Feature Flag Change with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 25: `99-Feature Flag Change approved.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/99-Feature Flag Change approved.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`
- **4. Purpose**: Render 99 Feature Flag Change approved with full visual fidelity to design assets.
- **5. User Role**: Super Admin & Ops
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

---

## 6. Future AI Code Generation Instructions
1. Inspect every image listed above in `Screens/` before generating UI code.
2. Implement backend schemas and endpoints in `Backend/` first.
3. Implement KMP / Next.js client models, repositories, and state machines second.
4. Build the UI composables / React components with exact visual fidelity to the provided designs.
