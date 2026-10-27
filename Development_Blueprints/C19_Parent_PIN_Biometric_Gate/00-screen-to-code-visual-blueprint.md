# Visual & System Blueprint: C19 Parent PIN Biometric Gate

## 1. Feature Context & Metadata
- **Feature Directory**: `Development_Blueprints/C19_Parent_PIN_Biometric_Gate/`
- **Target Feature ID**: C19
- **Related PRD Document**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C19_Parent_PIN_Biometric_Gate.md`
- **Mapped Screen Count**: 7 Screens Total
- **Primary User Role**: Parent / Guardian
- **Feature Purpose**: Secure 4-Digit Parent PIN & Biometric Gateway

---

## 2. Mandatory AI Implementation Directives (Multi-Image Rule)
> **CRITICAL MANDATORY AI INSTRUCTION:**
> For any screen or flow represented by multiple images in this feature, the AI coding agent **MUST read and inspect ALL constituent screen images collectively** before generating any UI, ViewModel, or API binding code.
> The agent must **NOT** implement a partial screen from a single image. It must synthesize all visual states (Initial, Populated, Active Input, Validation Error, Dialogs, Loading Spinners, and Empty States) into a single cohesive, production-ready component.

---

## 3. Exhaustive Screen Inventory & Exact File Paths (7 Screens Total)

| # | Exact Screen Image File Path | Screen Title / Visual State | UI Role | Primary API Dependency |
|---|---|---|---|---|
| 01 | `Screens/Mobile App/Parent Area/Parent Gate-01.png` | Parent Gate 01 | Parent / Guardian | Sourced from Backend/KMP task files |
| 02 | `Screens/Mobile App/Parent Area/Parent Gate-02.png` | Parent Gate 02 | Parent / Guardian | Sourced from Backend/KMP task files |
| 03 | `Screens/Mobile App/Parent Area/Profile Lock.png` | Profile Lock | Parent / Guardian | Sourced from Backend/KMP task files |
| 04 | `Screens/Mobile App/Parent Area/Who is Learning_-01.png` | Who is Learning (Default State) | Child / Parent | `GET /v1/family/children` |
| 05 | `Screens/Mobile App/Parent Area/Who is Learning_-02.png` | Who is Learning (Scrolled / Add Child & Banner) | Child / Parent | `GET /v1/family/children` |
| 06 | `Screens/Mobile App/Parent Area/Who is Learning_-03.png` | Who is Learning (Loading Shimmer Grid) | Child / Parent | `GET /v1/family/children` |
| 07 | `Screens/Mobile App/Parent Area/Who is Learning_-04.png` | Who is Learning (Offline Cached State) | Child / Parent | `GET /v1/family/children` |

---

## 4. Comprehensive 24-Point Screen Specifications (Applied to All Mapped Screens)

For every screen listed above, future AI coding agents must strictly adhere to the following 24-point implementation contract:

1. **Platform**: Defined per exact image path (Mobile App: Compose Multiplatform / M3; Parent/Admin Web: Next.js 14 App Router / Tailwind / shadcn/ui).
2. **Exact Screen Image Path**: Referenced individually in Section 3 and Section 5 below.
3. **Related PRD Document**: Sourced directly from `PRD_Documents/Parent Area In-App (19-26)/Feature_C19_Parent_PIN_Biometric_Gate.md`.
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

### Screen 01: `Parent Gate-01.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Parent Area/Parent Gate-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C19_Parent_PIN_Biometric_Gate.md`
- **4. Purpose**: Render Parent Gate 01 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 02: `Parent Gate-02.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Parent Area/Parent Gate-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C19_Parent_PIN_Biometric_Gate.md`
- **4. Purpose**: Render Parent Gate 02 with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 03: `Profile Lock.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Parent Area/Profile Lock.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C19_Parent_PIN_Biometric_Gate.md`
- **4. Purpose**: Render Profile Lock with full visual fidelity to design assets.
- **5. User Role**: Parent / Guardian
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 04: `Who is Learning_-01.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Parent Area/Who is Learning_-01.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C19_Parent_PIN_Biometric_Gate.md` (FR-1 to FR-3)
- **4. Purpose**: Landing profile selection surface showing active children + Parent Profile tile + lock status overlays.
- **5. User Role**: Child / Parent
- **6. Navigation**: Entry point for returning sessions; routes to `ChildLockRoute` (locked), `ChildHomeRoute` / `FirstMissionRoute` (unlocked), or `ParentGateRoute` (Parent Profile).
- **7. UI State Handling**: Populated responsive grid (`PopulatedProfilesGrid`).
- **8. Design System Tokens**: Night sky gradient, serif header, 24dp card radii, semantic tokens, full RTL support.

### Screen 05: `Who is Learning_-02.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Parent Area/Who is Learning_-02.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C19_Parent_PIN_Biometric_Gate.md` (FR-1)
- **4. Purpose**: Scrolled profile picker view showing Add Child tile (gated behind Parent Gate) and personalized educational journey banner.
- **5. User Role**: Child / Parent
- **6. Navigation**: Tapping Add Child triggers `ParentGateRoute("add_child")`.
- **7. UI State Handling**: Dashed profile card + full-width journey card (`PersonalizedJourneyBanner`).
- **8. Design System Tokens**: Dashed border with round caps, 16dp journey banner radii, semantic tokens.

### Screen 06: `Who is Learning_-03.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Parent Area/Who is Learning_-03.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C19_Parent_PIN_Biometric_Gate.md`
- **4. Purpose**: Responsive shimmer loading placeholder grid while `observeChildren()` fetches from local cache or remote server.
- **5. User Role**: Child / Parent
- **6. Navigation**: Non-interactive transient loading state.
- **7. UI State Handling**: Shimmer Skeleton grid (`LoadingShimmerGrid`) with 4 cards in `0.88f` aspect ratio.
- **8. Design System Tokens**: `NoorSkeleton` with `radius24`.

### Screen 07: `Who is Learning_-04.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Parent Area/Who is Learning_-04.png`
- **3. Related PRD**: `PRD_Documents/Parent Area In-App (19-26)/Feature_C19_Parent_PIN_Biometric_Gate.md` (FR-15)
- **4. Purpose**: Offline connectivity banner alert overlay showing cached profile availability without network disruption.
- **5. User Role**: Child / Parent
- **6. Navigation**: Fully operational local navigation supported offline.
- **7. UI State Handling**: Offline banner (`ProfilePickerOfflineBanner`) rendered above the profile grid.
- **8. Design System Tokens**: Rounded amber card, warning semantic token color, exclamation emblem.

---

## 6. Future AI Code Generation Instructions
1. Inspect every image listed above in `Screens/` before generating UI code.
2. Implement backend schemas and endpoints in `Backend/` first.
3. Implement KMP / Next.js client models, repositories, and state machines second.
4. Build the UI composables / React components with exact visual fidelity to the provided designs.
