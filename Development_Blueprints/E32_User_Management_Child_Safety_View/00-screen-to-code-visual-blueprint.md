# Visual & System Blueprint: E32 User Management Child Safety View

## 1. Feature Context & Metadata
- **Feature Directory**: `Development_Blueprints/E32_User_Management_Child_Safety_View/`
- **Target Feature ID**: E32
- **Related PRD Document**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **Mapped Screen Count**: 34 Screens Total
- **Primary User Role**: Support Agent & Safety Officer
- **Feature Purpose**: User Management, Dual-Operator PII Unmasking & Child Safety Console

---

## 2. Mandatory AI Implementation Directives (Multi-Image Rule)
> **CRITICAL MANDATORY AI INSTRUCTION:**
> For any screen or flow represented by multiple images in this feature, the AI coding agent **MUST read and inspect ALL constituent screen images collectively** before generating any UI, ViewModel, or API binding code.
> The agent must **NOT** implement a partial screen from a single image. It must synthesize all visual states (Initial, Populated, Active Input, Validation Error, Dialogs, Loading Spinners, and Empty States) into a single cohesive, production-ready component.

---

## 3. Exhaustive Screen Inventory & Exact File Paths (34 Screens Total)

| # | Exact Screen Image File Path | Screen Title / Visual State | UI Role | Primary API Dependency |
|---|---|---|---|---|
| 01 | `Screens/Admin Web/09-User Management — Search-01.png` | 09 User Management — Search 01 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 02 | `Screens/Admin Web/09-User Management — Search-02.png` | 09 User Management — Search 02 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 03 | `Screens/Admin Web/10-Unmask Approval Queue.png` | 10 Unmask Approval Queue | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 04 | `Screens/Admin Web/11-Unmask Request Review-01.png` | 11 Unmask Request Review 01 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 05 | `Screens/Admin Web/11-Unmask Request Review-02.png` | 11 Unmask Request Review 02 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 06 | `Screens/Admin Web/12-Unmask Request Review-request-reject.png` | 12 Unmask Request Review request reject | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 07 | `Screens/Admin Web/13-Unmask Request Review-request-approved.png` | 13 Unmask Request Review request approved | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 08 | `Screens/Admin Web/16-Support Case Queue-01.png` | 16 Support Case Queue 01 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 09 | `Screens/Admin Web/16-Support Case Queue-02.png` | 16 Support Case Queue 02 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 10 | `Screens/Admin Web/17-Support Case Queue-01.png` | 17 Support Case Queue 01 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 11 | `Screens/Admin Web/17-Support Case Queue-02.png` | 17 Support Case Queue 02 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 12 | `Screens/Admin Web/17-Support Case Queue-03.png` | 17 Support Case Queue 03 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 13 | `Screens/Admin Web/18-View Parent Account Detail-01.png` | 18 View Parent Account Detail 01 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 14 | `Screens/Admin Web/18-View Parent Account Detail-02.png` | 18 View Parent Account Detail 02 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 15 | `Screens/Admin Web/18-View Parent Account Detail-03.png` | 18 View Parent Account Detail 03 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 16 | `Screens/Admin Web/18-View Parent Account Detail-04.png` | 18 View Parent Account Detail 04 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 17 | `Screens/Admin Web/18-View Parent Account Detail-05.png` | 18 View Parent Account Detail 05 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 18 | `Screens/Admin Web/19-Unmask Request Submission-01.png` | 19 Unmask Request Submission 01 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 19 | `Screens/Admin Web/19-Unmask Request Submission-02.png` | 19 Unmask Request Submission 02 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 20 | `Screens/Admin Web/19-Unmask Request Submission-03.png` | 19 Unmask Request Submission 03 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 21 | `Screens/Admin Web/20-Inspect Entitlements.png` | 20 Inspect Entitlements | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 22 | `Screens/Admin Web/21-Edit Support-Safe Metadata-01.png` | 21 Edit Support Safe Metadata 01 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 23 | `Screens/Admin Web/21-Edit Support-Safe Metadata-02.png` | 21 Edit Support Safe Metadata 02 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 24 | `Screens/Admin Web/21-Edit Support-Safe Metadata-03.png` | 21 Edit Support Safe Metadata 03 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 25 | `Screens/Admin Web/22-Initiate Account Recovery-01.png` | 22 Initiate Account Recovery 01 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 26 | `Screens/Admin Web/22-Initiate Account Recovery-02.png` | 22 Initiate Account Recovery 02 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 27 | `Screens/Admin Web/23-Initiate Account Recovery-03.png` | 23 Initiate Account Recovery 03 | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 28 | `Screens/Admin Web/24-Child Safety View-Full History.png` | 24 Child Safety View Full History | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 29 | `Screens/Admin Web/24-Child Safety View.png` | 24 Child Safety View | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 30 | `Screens/Admin Web/25-Child Safety View-Full History.png` | 25 Child Safety View Full History | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 31 | `Screens/Admin Web/26-Legacy Admin Users.png` | 26 Legacy Admin Users | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 32 | `Screens/Admin Web/43-Child-Safety Queue.png` | 43 Child Safety Queue | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 33 | `Screens/Admin Web/44-Child-Safety queue review.png` | 44 Child Safety queue review | Support Agent & Safety Officer | Sourced from Backend/KMP task files |
| 34 | `Screens/Admin Web/45-Child-Safety queue review passed.png` | 45 Child Safety queue review passed | Support Agent & Safety Officer | Sourced from Backend/KMP task files |

---

## 4. Comprehensive 24-Point Screen Specifications (Applied to All Mapped Screens)

For every screen listed above, future AI coding agents must strictly adhere to the following 24-point implementation contract:

1. **Platform**: Defined per exact image path (Mobile App: Compose Multiplatform / M3; Parent/Admin Web: Next.js 14 App Router / Tailwind / shadcn/ui).
2. **Exact Screen Image Path**: Referenced individually in Section 3 and Section 5 below.
3. **Related PRD Document**: Sourced directly from `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`.
4. **Related PRD Section/Feature**: Specified in the corresponding feature task markdown files.
5. **Purpose of the Screen**: Accurate visual and interactive reproduction of the design mockups.
6. **User Role**: `Support Agent & Safety Officer`.
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

### Screen 01: `09-User Management — Search-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/09-User Management — Search-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 09 User Management — Search 01 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 02: `09-User Management — Search-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/09-User Management — Search-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 09 User Management — Search 02 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 03: `10-Unmask Approval Queue.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/10-Unmask Approval Queue.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 10 Unmask Approval Queue with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 04: `11-Unmask Request Review-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/11-Unmask Request Review-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 11 Unmask Request Review 01 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 05: `11-Unmask Request Review-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/11-Unmask Request Review-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 11 Unmask Request Review 02 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 06: `12-Unmask Request Review-request-reject.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/12-Unmask Request Review-request-reject.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 12 Unmask Request Review request reject with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 07: `13-Unmask Request Review-request-approved.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/13-Unmask Request Review-request-approved.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 13 Unmask Request Review request approved with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 08: `16-Support Case Queue-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/16-Support Case Queue-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 16 Support Case Queue 01 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 09: `16-Support Case Queue-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/16-Support Case Queue-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 16 Support Case Queue 02 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 10: `17-Support Case Queue-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/17-Support Case Queue-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 17 Support Case Queue 01 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 11: `17-Support Case Queue-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/17-Support Case Queue-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 17 Support Case Queue 02 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 12: `17-Support Case Queue-03.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/17-Support Case Queue-03.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 17 Support Case Queue 03 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 13: `18-View Parent Account Detail-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/18-View Parent Account Detail-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 18 View Parent Account Detail 01 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 14: `18-View Parent Account Detail-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/18-View Parent Account Detail-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 18 View Parent Account Detail 02 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 15: `18-View Parent Account Detail-03.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/18-View Parent Account Detail-03.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 18 View Parent Account Detail 03 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 16: `18-View Parent Account Detail-04.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/18-View Parent Account Detail-04.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 18 View Parent Account Detail 04 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 17: `18-View Parent Account Detail-05.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/18-View Parent Account Detail-05.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 18 View Parent Account Detail 05 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 18: `19-Unmask Request Submission-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/19-Unmask Request Submission-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 19 Unmask Request Submission 01 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 19: `19-Unmask Request Submission-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/19-Unmask Request Submission-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 19 Unmask Request Submission 02 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 20: `19-Unmask Request Submission-03.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/19-Unmask Request Submission-03.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 19 Unmask Request Submission 03 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 21: `20-Inspect Entitlements.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/20-Inspect Entitlements.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 20 Inspect Entitlements with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 22: `21-Edit Support-Safe Metadata-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/21-Edit Support-Safe Metadata-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 21 Edit Support Safe Metadata 01 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 23: `21-Edit Support-Safe Metadata-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/21-Edit Support-Safe Metadata-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 21 Edit Support Safe Metadata 02 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 24: `21-Edit Support-Safe Metadata-03.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/21-Edit Support-Safe Metadata-03.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 21 Edit Support Safe Metadata 03 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 25: `22-Initiate Account Recovery-01.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/22-Initiate Account Recovery-01.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 22 Initiate Account Recovery 01 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 26: `22-Initiate Account Recovery-02.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/22-Initiate Account Recovery-02.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 22 Initiate Account Recovery 02 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 27: `23-Initiate Account Recovery-03.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/23-Initiate Account Recovery-03.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 23 Initiate Account Recovery 03 with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 28: `24-Child Safety View-Full History.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/24-Child Safety View-Full History.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 24 Child Safety View Full History with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 29: `24-Child Safety View.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/24-Child Safety View.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 24 Child Safety View with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 30: `25-Child Safety View-Full History.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/25-Child Safety View-Full History.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 25 Child Safety View Full History with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 31: `26-Legacy Admin Users.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/26-Legacy Admin Users.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 26 Legacy Admin Users with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 32: `43-Child-Safety Queue.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/43-Child-Safety Queue.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 43 Child Safety Queue with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 33: `44-Child-Safety queue review.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/44-Child-Safety queue review.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 44 Child Safety queue review with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 34: `45-Child-Safety queue review passed.png`
- **1. Platform**: Admin Web (Next.js 14 / Tailwind / shadcn/ui)
- **2. Exact Image Path**: `Screens/Admin Web/45-Child-Safety queue review passed.png`
- **3. Related PRD**: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E32_User_Management_Child_Safety_View.md`
- **4. Purpose**: Render 45 Child Safety queue review passed with full visual fidelity to design assets.
- **5. User Role**: Support Agent & Safety Officer
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

---

## 6. Future AI Code Generation Instructions
1. Inspect every image listed above in `Screens/` before generating UI code.
2. Implement backend schemas and endpoints in `Backend/` first.
3. Implement KMP / Next.js client models, repositories, and state machines second.
4. Build the UI composables / React components with exact visual fidelity to the provided designs.
