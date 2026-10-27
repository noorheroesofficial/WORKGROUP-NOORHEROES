# K-06 — Cross-Domain Parent Mastery Summary

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). The Parent Area screen that renders B-08's cross-domain mastery rollup — giving parents one consistent, trustworthy view of progress across every domain a child engages with, rather than checking each domain's report separately.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
K-06 — Cross-Domain Parent Mastery Summary (Parent Area Screen)

## 4. Objective
Build the Parent Area screen consuming B-08's `GET /v1/children/{id}/mastery-summary`, rendering concept-level summaries (skill labels + state + trend) grouped by domain, with an optional domain filter and drill-through to domain-specific detail (e.g., A.5's existing Quran/Arabic report).

## 5. Business Requirements
- FR-11: domain-agnostic Parent Report contract — concept-level summaries, never a raw aggregate score as headline.
- User Story: "As a parent, I want every learning domain in the app to report progress in the same consistent, trustworthy way."
- Screen Inventory #8: Parent Cross-Domain Mastery Summary — entry point Parent Dashboard → Child Progress → Learning (aggregated across domains); exit point domain-specific detail (e.g., A.5's Quran/Arabic report).

## 6. Existing Architecture
Kotlin, Jetpack Compose, MVVM. Parent Area screens already exist in the app (A.5's `K-12 Parent Progress Report In-App` is the direct precedent for a domain-specific parent report; this sub-feature is the cross-domain rollup sitting above it).

## 7. Existing Code to Reuse
- A.5's `K-12 Parent Progress Report In-App` — reuse its concept-level card/list rendering components where the visual language overlaps, rather than building parallel report UI components.
- Parent-session auth/navigation guards already established for Parent Area screens.
- K-01's `MasteryRepository` (extended to include `getParentMasterySummary`, or a small addition to the repository interface if not already covered).

## 8. Files to Create
- `core/mastery-engine/src/commonMain/kotlin/.../presentation/CrossDomainMasterySummaryScreen.kt`
- `core/mastery-engine/src/commonMain/kotlin/.../presentation/CrossDomainMasterySummaryViewModel.kt`
- `core/mastery-engine/src/commonMain/kotlin/.../data/dto/MasterySummaryDto.kt` (if not already added in K-01)
- `core/mastery-engine/src/commonTest/kotlin/.../CrossDomainMasterySummaryViewModelTest.kt`
- `core/mastery-engine/src/androidInstrumentedTest/kotlin/.../CrossDomainMasterySummaryScreenUiTest.kt`

## 9. Files to Modify
- K-01's `MasteryRepository`/`MasteryApi` — add `getMasterySummary(childId, domain?)` mapping to B-08's endpoint, if not already scaffolded.
- Parent Area navigation graph — add entry point `Parent Dashboard → Child Progress → Learning`, and drill-through exit points into domain-specific detail screens (e.g., A.5's report).

## 10. Backend Requirements
N/A (consumes B-08).

## 11. KMP Requirements
- **`CrossDomainMasterySummaryViewModel`:** fetches `MasteryRepository.getMasterySummary(childId, domain = null)` on entry for the full rollup; supports re-fetching with a specific `domain` filter when the parent taps a domain-filter chip.
- **Screen layout:** grouped-by-domain sections, each showing concept-level skill cards (label + state + trend) — never a numeric aggregate score as the page's headline element.
- **Drill-through:** tapping a domain section (or a "view full report" affordance) navigates to that domain's existing detailed report screen (e.g., A.5's `K-12`) — this screen is a rollup/entry-point, not a replacement for domain-specific depth.
- **Empty state:** child with zero evidence in any domain shows an appropriate "just getting started" empty state, not an error or blank screen.

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes B-08's `GET /v1/children/{id}/mastery-summary?domain=` response shape exactly.

## 14. Database Requirements
N/A (may optionally cache last-fetched summary for quick redisplay, consistent with K-01's general caching philosophy — not required for correctness since this is a parent-initiated, online-context view).

## 15. Validation
`childId` must be a valid child in the parent's family (enforced server-side by B-08; client just surfaces the resulting `403` gracefully if somehow reached with an invalid child).

## 16. Authentication
Reuses the existing parent-session Bearer token attachment (distinct from child-session, per B-08's auth requirement).

## 17. Authorization
N/A at this layer (server enforces family scoping).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Fetch fails (network/server error) | Error state with retry affordance |
| Child has zero evidence in any domain | "Just getting started" empty state, not an error |
| Domain filter selected with zero data for that domain | Empty state scoped to that domain, with an easy way back to "all domains" |

## 19. Offline First
Not required to be fully offline-capable (parent-initiated report view, expected to be used online); may show a last-cached summary with a "may be outdated" indicator if implemented, but this is an enhancement, not a hard requirement for this sub-feature.

## 20. Local Data
Optional last-fetched cache (see §14) — not required.

## 21. Localization
All labels, state names, trend descriptors, and empty-state copy localized EN/HI/AR/UR.

## 22. RTL
Full RTL layout support for the grouped-section/card layout.

## 23. Analytics
`cross_domain_mastery_summary_viewed` fired via K-05's `MasteryAnalytics` on successful load.

## 24. Performance
Standard list/section rendering performance considerations — avoid unnecessary recomposition when domain-filter selection changes (scope the re-fetch/re-render to the affected section, not the whole screen, where practical).

## 25. Security
No raw score exposure (consistent with B-08's structural guarantee); parent-session-scoped auth prevents cross-family access.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: ViewModel fetch/filter logic, empty-state branching.
- UI test: grouped-by-domain rendering, domain-filter interaction, drill-through navigation trigger.
- UI test: no numeric score displayed anywhere in the screen's semantics tree.

## 28. Documentation
KDoc noting this screen's relationship to A.5's existing domain-specific report (rollup entry point, not a replacement).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend MasteryRepository with getMasterySummary()**
- Task ID: K-06-T01
- Objective: Client-side data access for B-08.
- Why This Is Required: This screen's sole data dependency.
- Existing Architecture to Follow: K-01's existing repository pattern.
- Existing Files to Reuse: `MasteryApi`, `MasteryRepository` (K-01).
- Files to Create: `dto/MasterySummaryDto.kt` (if not already present).
- Files to Modify: `MasteryApi.kt`, `MasteryRepository.kt`, `MasteryRepositoryImpl.kt` (all K-01 files).
- Implementation Details: `getMasterySummary(childId: String, domain: String? = null): MasterySummaryDto`.
- Business Rules: No score field in the DTO (same structural guarantee as K-01's other DTOs).
- Validation: N/A. Error Handling: Standard typed exception on failure.
- Security: Reuses parent-session auth interceptor. Performance: N/A.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: Extend `MasteryRepositoryTest.kt`.
- Documentation: KDoc.
- Dependencies: K-01, B-08.
- Do Not Change: Existing `getSkillStates`/`getResult` methods.
- Expected Result: New repository method ready.
- Definition of Done: Unit test green.

**Task 02 — Build CrossDomainMasterySummaryViewModel + Screen**
- Task ID: K-06-T02
- Objective: Full screen implementation.
- Why This Is Required: The core deliverable.
- Existing Architecture to Follow: A.5's `K-12` parent-report screen structure, reused component library.
- Existing Files to Reuse: A.5's concept-level card components, if reusable as-is.
- Files to Create: `CrossDomainMasterySummaryScreen.kt`, `CrossDomainMasterySummaryViewModel.kt`.
- Files to Modify: None.
- Implementation Details: Fetch on entry, domain-filter chip interaction re-fetches or client-filters the already-fetched full rollup (whichever is more efficient — prefer client-side filtering of an already-fetched full rollup to avoid redundant network calls, unless the dataset is large enough that server-side filtering is meaningfully cheaper).
- Business Rules: Grouped-by-domain layout, drill-through navigation, empty-state handling.
- Validation: N/A. Error Handling: Per §18.
- Security: N/A. Performance: Scoped recomposition on filter change.
- Localization: Full string coverage. RTL: Full mirroring.
- Analytics: `cross_domain_mastery_summary_viewed` via K-05.
- Tests: `CrossDomainMasterySummaryViewModelTest.kt`, `CrossDomainMasterySummaryScreenUiTest.kt`.
- Documentation: KDoc per §28.
- Dependencies: Task 01, K-05.
- Do Not Change: A.5's `K-12` screen itself (this is additive, drill-through target, not a replacement).
- Expected Result: Working cross-domain summary screen.
- Definition of Done: All tests green including empty-state and drill-through navigation.

**Task 03 — Wire Parent Area Navigation Entry/Exit Points**
- Task ID: K-06-T03
- Objective: Correct navigation graph placement.
- Why This Is Required: Screen Inventory #8's specified entry/exit points.
- Existing Architecture to Follow: Existing Parent Area navigation graph conventions.
- Existing Files to Reuse: Parent Area nav graph.
- Files to Create: None.
- Files to Modify: Parent Area navigation graph.
- Implementation Details: Entry from `Parent Dashboard → Child Progress → Learning`; exit to domain-specific detail (e.g., A.5's `K-12`) on drill-through.
- Business Rules: N/A. Validation/Error Handling/Security/Performance: N/A.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: Navigation integration test (entry point reachable, drill-through lands on correct domain screen).
- Documentation: N/A (wiring task).
- Dependencies: Task 02.
- Do Not Change: A.5's existing navigation destinations (only add new edges into/out of them).
- Expected Result: Screen reachable and correctly linked.
- Definition of Done: Navigation integration test green.

## 30. Definition of Done
Cross-Domain Parent Mastery Summary screen live in the Parent Area, correctly grouping concept-level progress by domain, supporting domain filtering, drilling through to existing domain-specific reports, with full localization/RTL/empty-state handling and no raw score exposure.

## 31. Final Verification Checklist
- [ ] Screen reachable via `Parent Dashboard → Child Progress → Learning`
- [ ] Grouped-by-domain rendering correct for a multi-domain child
- [ ] Domain filter interaction working
- [ ] Drill-through to domain-specific report (e.g., A.5's `K-12`) working
- [ ] Empty state for zero-evidence child correct, not an error
- [ ] No numeric score displayed anywhere (semantics-tree scan)
- [ ] Full EN/HI/AR/UR localization + RTL verified
- [ ] `cross_domain_mastery_summary_viewed` analytics event firing correctly
