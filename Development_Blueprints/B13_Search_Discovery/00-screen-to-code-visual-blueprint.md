# Visual & System Blueprint: B13 Search Discovery

## 1. Feature Context & Metadata
- **Feature Directory**: `Development_Blueprints/B13_Search_Discovery/`
- **Target Feature ID**: B13
- **Related PRD Document**: `PRD_Documents/Child App Supporting (13-18)/Feature_B13_Search_Discovery.md`
- **Mapped Screen Count**: 5 Screens Total
- **Primary User Role**: Child Learner
- **Feature Purpose**: Multi-Modal Voice & Text Search with Instant Discovery

---

## 2. Mandatory AI Implementation Directives (Multi-Image Rule)
> **CRITICAL MANDATORY AI INSTRUCTION:**
> For any screen or flow represented by multiple images in this feature, the AI coding agent **MUST read and inspect ALL constituent screen images collectively** before generating any UI, ViewModel, or API binding code.
> The agent must **NOT** implement a partial screen from a single image. It must synthesize all visual states (Initial, Populated, Active Input, Validation Error, Dialogs, Loading Spinners, and Empty States) into a single cohesive, production-ready component.

---

## 3. Exhaustive Screen Inventory & Exact File Paths (5 Screens Total)

| # | Exact Screen Image File Path | Screen Title / Visual State | UI Role | Primary API Dependency |
|---|---|---|---|---|
| 01 | `Screens/Mobile App/Search/Results.png` | Results | Child Learner | `GET /v1/search` (`Backend/01-child-search-query-api.md` - ✅ Completed & Verified) |
| 02 | `Screens/Mobile App/Search/Search-01.png` | Search 01 (Initial / Recents) | Child Learner | `GET /v1/search/recent`, `DELETE /v1/search/recent`, `DELETE /v1/search/recent/{search_id}` (`Backend/04-recent-search-history-management.md` - ✅ Completed & Verified) & `GET /v1/search` (`Backend/01-child-search-query-api.md` - ✅ Completed & Verified) |
| 03 | `Screens/Mobile App/Search/Search-02.png` | Search 02 (Active Input) | Child Learner | `GET /v1/search` (`Backend/01-child-search-query-api.md` - ✅ Completed & Verified) |
| 04 | `Screens/Mobile App/Search/Voice Search-01.png` | Voice Search 01 (Listening) | Child Learner | `POST /v1/search/voice` (`Backend/03-voice-search-transcription-service.md` - ✅ Completed & Verified) |
| 05 | `Screens/Mobile App/Search/Voice Search-02.png` | Voice Search 02 (Clarification) | Child Learner | `POST /v1/search/voice` (`Backend/03-voice-search-transcription-service.md` - ✅ Completed & Verified) |
| -- | `Screens/Mobile App/Parent Area/Parent Dashboard-*.png` | Parent Area Search (Existing Surface) | Parent / Guardian | `GET /v1/parent/search` (`Backend/05-parent-area-search-api.md` - ✅ Completed & Verified) |
| -- | `noorheroes-admin/src/app/(admin)/content/search/page.tsx` | Admin Content Search Surface | Admin Staff / Content Editor | `GET /admin/v1/search` (`Backend/06-admin-content-search-api.md` - ✅ Completed & Verified) |
| -- | `noorheroes-admin/src/app/(admin)/search/monitoring/page.tsx` | Admin Search Operations Monitoring | Admin / Operations / AI Ops | `GET /admin/v1/search/index-health`, `/rejected-items`, `/zero-result-report`, `/voice-quality` (`Backend/07-admin-search-operations-monitoring-api.md` - ✅ Completed & Verified) |

---

## 4. Comprehensive 24-Point Screen Specifications (Applied to All Mapped Screens)

For every screen listed above, future AI coding agents must strictly adhere to the following 24-point implementation contract:

1. **Platform**: Defined per exact image path (Mobile App: Compose Multiplatform / M3; Parent/Admin Web: Next.js 14 App Router / Tailwind / shadcn/ui).
2. **Exact Screen Image Path**: Referenced individually in Section 3 and Section 5 below.
3. **Related PRD Document**: Sourced directly from `PRD_Documents/Child App Supporting (13-18)/Feature_B13_Search_Discovery.md`.
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

### Screen 01: `Results.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Search/Results.png`
- **3. Related PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B13_Search_Discovery.md`
- **4. Purpose**: Render Results with full visual fidelity to design assets.
- **5. User Role**: Child Learner
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 02: `Search-01.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Search/Search-01.png`
- **3. Related PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B13_Search_Discovery.md` (FR-10, PRD Edge Cases 1 & 4)
- **4. Purpose**: Render Search 01 (initial discovery, recent search history chips with individual dismiss affordances, "Clear all" action, and search bar) with full visual fidelity to design assets.
- **5. User Role**: Child Learner
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State (no recents / suggested categories), Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.
- **9. Endpoints & Operations**:
  - `GET /v1/search/recent`: Lists up to 20 past search queries in reverse chronological order for authenticated child.
  - `DELETE /v1/search/recent`: Clears all recent searches ("Clear all" button) returning HTTP 204 No Content.
  - `DELETE /v1/search/recent/{search_id}`: Dismisses an individual search query chip (`✖` button) returning HTTP 204 No Content.
  - `GET /v1/search?q={query}`: Replays search query upon tapping chip. Server enforces dynamic age-band hard filter.
- **10. Sibling Isolation Invariant**: History is strictly scoped to authenticated `child_ctx.child_id` with zero cross-sibling leakage on shared tablets.
- **11. Verification Status**: ✅ Completed & Verified (39/39 tests in `test_recent_search.py`, 152/152 tests in `tests/modules/search`).

### Screen 03: `Search-02.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Search/Search-02.png`
- **3. Related PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B13_Search_Discovery.md`
- **4. Purpose**: Render Search 02 with full visual fidelity to design assets.
- **5. User Role**: Child Learner
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 04: `Voice Search-01.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Search/Voice Search-01.png`
- **3. Related PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B13_Search_Discovery.md`
- **4. Purpose**: Render Voice Search 01 with full visual fidelity to design assets.
- **5. User Role**: Child Learner
- **6. Navigation**: Part of the core feature user journey flow.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 05: `Voice Search-02.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Search/Voice Search-02.png`
- **3. Related PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B13_Search_Discovery.md`
- **4. Purpose**: Render Voice Search 02 with full visual fidelity to design assets.
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
