# K-07 — Parent Area Search Experience

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). This is the previously-missing KMP consumer of B-05's `GET /v1/parent/search` — the Screen Inventory's item #11, "Parent Area Search (reports/stories/habits)," entry point "Parent Dashboard search entry." Confirmed via C.20 (Parent Dashboard)'s own PRD, which explicitly scopes itself to child selector, weekly AI report card, activity timeline preview, and screen-time summary only — it does not own or build a search feature. Building this UI is therefore B.13's own responsibility, not something inherited from C.20.

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
K-07 — Parent Area Search Experience

## 4. Objective
Build the Parent Mode search screen reachable from the Parent Dashboard, letting a parent search their own family's reports, stories, and habits, consuming `GET /v1/parent/search` (B-05) — architecturally and visually distinct from the child-facing Search module (K-01–K-06), never sharing state, ViewModel, or navigation graph with it.

## 5. Business Requirements
- FR-11: parent-facing search surface within the Parent Area, distinct from child search, scoped to parent-session-authenticated data only.
- Acceptance Criteria: results scoped strictly to the parent's own family — never another family's data, never the unrestricted Admin search surface.
- §1.18 Screen Inventory #11: entry point "Parent Dashboard search entry," exit points "Relevant report/progress detail screen."
- C.19's Visibility Rule (inherited context): this screen exists only behind the verified Parent PIN/Biometric Gate, never reachable from a child session — "Parent dashboard APIs reject any child-mode token outright" applies identically here since this screen calls a parent-mode-only endpoint.
- C.20's no-sibling-ranking guarantee: if search results span multiple children, results must present each child's data neutrally, never in a comparative/ranked framing.

## 6. Existing Architecture
New screen inside the existing Parent Area module structure (the same module housing C.20 Parent Dashboard, C.21 Multi-Child Management, C.22 Per-Child Reports, etc. — confirm the exact existing module name, e.g. `feature-parent`, per that module's own established blueprint) — **not** part of `feature-search` (K-01–K-06's child-facing module). This is a deliberate module boundary matching B-05's backend isolation from B-01: the two search experiences must never share a Compose navigation graph, ViewModel, or repository.

## 7. Existing Code to Reuse
- C.19's Parent PIN/Biometric Gate — this screen is reachable only downstream of that gate; no separate auth check is reimplemented here beyond relying on the existing gated Parent Area navigation graph.
- C.20 Parent Dashboard's existing module-shortcut pattern (the same UI convention used for its other module shortcuts — Reports, Settings, etc.) — the search entry point is added as one more shortcut affordance on the Dashboard, not a new navigation paradigm.
- `core-designsystem`, `core-analytics`, `core-navigation` — same core modules as the rest of the app, but the Parent Area's own screen-composition conventions (calm, jargon-free tone per C.20 §1.1) are followed here, not K-01–K-06's child-oriented visual language.
- `core-network`'s `HttpClient` (Ktor) for the `GET /v1/parent/search` call.

## 8. Files to Create
- `feature-parent/src/commonMain/kotlin/.../search/ParentSearchScreen.kt`.
- `feature-parent/src/commonMain/kotlin/.../search/ParentSearchViewModel.kt`.
- `feature-parent/src/commonMain/kotlin/.../search/ParentSearchUiState.kt`.
- `feature-parent/src/commonMain/kotlin/.../search/components/ParentSearchResultRow.kt` (typed by `source_type`: report/story_activity/habit, with a per-child label, never a ranked/comparative layout).
- `core-network/src/commonMain/kotlin/.../api/ParentSearchApi.kt` (Ktor client for `GET /v1/parent/search`).
- `feature-parent-domain/.../ParentSearchRepository.kt` (interface) + impl.
- `feature-parent/src/commonTest/kotlin/.../ParentSearchViewModelTest.kt`.
- `feature-parent/src/commonTest/kotlin/.../ParentSearchModuleIsolationTest.kt`.

## 9. Files to Modify
- C.20 Parent Dashboard's screen — add a "Search" module-shortcut affordance navigating into `ParentSearchScreen`.
- `feature-parent`'s Koin module — register `ParentSearchApi`, `ParentSearchRepository`, `ParentSearchViewModel`.

## 10. Backend Requirements
Consumes B-05 exclusively: `GET /v1/parent/search?q=`.

## 11. KMP Requirements
- `ParentSearchViewModel` exposes `StateFlow<ParentSearchUiState>` (query input, loading, results, error).
- Debounced query submission, same 300–400ms convention as K-02, for consistency of feel even though this is a structurally separate module.
- `ParentSearchResultRow` renders each result with its `source_type` badge (report/story_activity/habit), the relevant child's name/avatar label, and navigates on tap to the corresponding existing detail screen (C.22 Per-Child Reports for report-type results, A.3's story-activity view, A.7's habit detail — reusing each destination's existing screen, not building new ones).
- **Multi-child neutrality:** when results span more than one child, they are grouped or labeled per-child but never sorted/framed in a way that implies comparison or ranking between siblings (C.20's inherited guarantee).
- Empty state: calm, jargon-free copy consistent with C.20's established tone (distinct copy from K-02's child-facing empty state, which uses a different illustration/tone register entirely).
- This screen's `ViewModel`/repository/navigation graph must have **zero shared code** with `feature-search`'s child-facing components (K-01–K-06) — verified by a module-isolation test, mirroring B-05's own backend isolation test.

## 12. NextJS Requirements
N/A — Parent Area is a KMP in-app surface (confirmed via C.20's PRD), not part of the separate D.27 Parent Web Portal (NextJS). If a future requirement extends parent search to the Web Portal, that would be a distinct sub-feature against D.27's own architecture, out of scope here.

## 13. API Contract
`GET /v1/parent/search?q=` → `{ results: [{ source_type, child_id, title, reference_id }], result_count }` per B-05 §13.

## 14. Database Requirements
None client-side — no local caching of parent-search results in this blueprint (unlike K-04's recent-searches cache for child search); parent search results are always fetched fresh, consistent with the Parent Area's existing reports/dashboard screens which are not offline-cached either (per C.20/C.22's own architecture).

## 15. Validation
Query max-length guard matching B-05's server-side bound.

## 16. Authentication
Relies entirely on the Parent Area's existing gated session (post-C.19 PIN/biometric verification) — the app-wide parent-mode bearer token is used by `core-network`'s interceptor; no additional auth handling here.

## 17. Authorization
N/A beyond the existing Parent Area gate — `family_id` scoping is enforced server-side by B-05.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Zero results | Calm, jargon-free empty state, consistent with C.20's tone |
| API failure | Non-alarming error state with retry, consistent with Parent Area's existing error-handling conventions |
| Navigated to without passing through C.19's gate | Not reachable — this screen only exists inside the already-gated Parent Area navigation graph, so this scenario is structurally prevented rather than handled |

## 19. Offline First
Not offline-capable, by design — consistent with the rest of the Parent Area's reporting screens (C.20/C.22), which require connectivity.

## 20. Local Data
None (see §14).

## 21. Localization
All strings localized (English/Hindi/Arabic/Urdu), matching the calm/jargon-free register established by C.20.

## 22. RTL
Standard RTL layout mirroring, consistent with the rest of the Parent Area's screens.

## 23. Analytics
`parent_search_performed` — fired client-side on a successful call to `GET /v1/parent/search`, per the parent PRD's §1.19 event taxonomy.

## 24. Performance
Debounced submission; result list is typically small (bounded by a single family's data) so no pagination/virtualization concern expected.

## 25. Security
**Module isolation from `feature-search` (K-01–K-06) is this blueprint's defining guarantee**, mirroring B-05's backend isolation from B-01 — verified by an automated test confirming zero shared ViewModel/repository/navigation-graph code between the two.

## 26. Library Requirements
Jetpack Compose, Ktor (via `core-network`), Koin. Same stack as the rest of the app — no new library.

## 27. Testing
- Unit: debounce logic, loading/error/empty state branching.
- **Module isolation test:** confirm `ParentSearchViewModel`/`ParentSearchRepository` share no class, import, or navigation-graph entry with `feature-search`'s `SearchViewModel`/`SearchRepository`.
- Multi-child neutrality test: fixture result set spanning two children, assert no sort/label implies ranking or comparison.
- Navigation test: confirms this screen is only reachable via the Parent Dashboard's gated navigation graph, not via any deep link bypassing C.19.

## 28. Documentation
KDoc explicitly noting this screen is the client-side consumer of B-05 and is a structurally separate module from `feature-search`'s child-facing screens.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Implement ParentSearchApi (Ktor)**
Files to create: `ParentSearchApi.kt`.

**Task 02 — Implement ParentSearchRepository**
Files to create: `ParentSearchRepository.kt` + impl.
Do not change: no dependency on `feature-search`'s repository/API classes.

**Task 03 — Implement ParentSearchViewModel & UiState**
Files to create: `ParentSearchUiState.kt`, `ParentSearchViewModel.kt`.
Business rules: multi-child neutral presentation, no ranking/comparison framing.

**Task 04 — Build ParentSearchScreen & ParentSearchResultRow**
Objective: calm, jargon-free tone consistent with C.20; per-`source_type` result routing to existing destination screens (C.22, A.3, A.7).
Files to create: `ParentSearchScreen.kt`, `ParentSearchResultRow.kt`.

**Task 05 — Add Search Entry Point to Parent Dashboard**
Files to modify: C.20's Dashboard screen — add the module-shortcut affordance.

**Task 06 — Add Module Isolation Test (highest priority)**
Files to create: `ParentSearchModuleIsolationTest.kt`.

**Task 07 — Add Full Test Suite & Wire Analytics**

**Task 08 — Final Review**
Objective: confirm zero shared code with `feature-search`; confirm this screen is unreachable except through C.19's gate; confirm multi-child result presentation is neutral.

## 30. Definition of Done
- Parent Area Search reachable from the Parent Dashboard, functional against B-05.
- Module isolation from child-facing search verified by test.
- Multi-child neutrality verified by test.
- Full localization and RTL support.

## 31. Final Verification Checklist
- [ ] Zero shared ViewModel/repository/navigation-graph code with `feature-search` (K-01–K-06) — verified by test.
- [ ] Screen only reachable via the Parent Dashboard's already-gated (C.19) navigation graph.
- [ ] Multi-child results never sorted/framed as a comparison or ranking between siblings.
- [ ] Tone/copy consistent with C.20's calm, jargon-free register — distinct from the child-facing empty state.
- [ ] Results route correctly to each `source_type`'s existing destination screen (C.22/A.3/A.7).
- [ ] Localization and RTL verified.
