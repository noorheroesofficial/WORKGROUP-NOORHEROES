# K-09 — Parent Story Insights (In-App Parent Area)

## 1. Feature Context
The in-app Parent Area view of a child's story activity: stories watched, time spent, quiz scores, morals learned. Strictly confined to the Parent Area navigation graph (behind the existing Parent PIN/Biometric Gate) — never duplicated into the child's own view in a way that exposes analytics framing to the child.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
2.9 Parent Story Insights (In-App Parent Area) (ID: **K-09**)

## 4. Objective
Build the Parent Story Insights list and per-story detail screens inside the existing Parent Area navigation graph, consuming B-10, with correct empty/offline-staleness states.

## 5. Business Requirements
- FR-20: shows stories watched, time spent, quiz scores, morals learned; accessible only from the Parent Area, never duplicated into the child's own view.
- §1.12 Empty States: "Once [Child] watches their first story, you'll see their progress here."
- §1.14 Offline States: shows last-synced data with a "may not reflect today's offline activity yet" note if relevant.

## 6. Existing Architecture
Lives inside the existing Parent Area navigation graph (established by C.20 Parent Dashboard / C.22 Per-Child Reports), not the child-facing `feature:stories` navigation graph — confirm the exact existing Parent Area module structure and follow it rather than placing this under the child Stories tab.

## 7. Existing Code to Reuse
- Existing Parent Area navigation graph/shell (from C.20/C.22 — locate and extend, do not create a parallel parent-facing navigation structure)
- `core-ui`: `LoadStateContent`, `EmptyStateView`
- `core-designsystem`: `NoorHeroesTheme`

## 8. Files to Create
- `feature/stories/parent/ParentStoryInsightsScreen.kt`
- `feature/stories/parent/ParentStoryInsightDetailScreen.kt`
- `feature/stories/data/ParentStoryInsightsRepository.kt` (B-10 client)
- `feature/stories/viewmodel/ParentStoryInsightsViewModel.kt` (+ State/Event files)
- `test/feature/stories/ParentStoryInsightsViewModelTest.kt`
- `androidTest/feature/stories/ParentStoryInsightsScreenTest.kt`

## 9. Files to Modify
- Existing Parent Area `Route.kt`/navigation graph — add `ParentStoryInsightsRoute(childId)`, `ParentStoryInsightDetailRoute(childId, episodeId)` (confirm exact file location within the existing Parent Area module before modifying)

## 10. KMP Requirements
- `ParentStoryInsightsViewModel.load(childId)`: calls B-10, renders empty state on zero-activity, renders a "may not reflect today's offline activity yet" note when the response indicates stale/last-synced data.
- Detail screen navigates from a list item to the full moral + quiz score view for that specific story.
- This screen is reachable exclusively from the Parent Area's existing navigation entry points (Parent Dashboard → Child Progress → Stories) — never linked from anywhere in the child-facing `feature:stories` module.

## 11. Required API
**User API (parent-scoped)** — B-10 `GET /v1/children/{id}/story-insights`.

## 12. Offline First
Cache-first read from the last-synced insights response (via `core-datastore`), with the staleness note rendered whenever the cached data's timestamp indicates it may not reflect the most recent offline child activity.

## 13. Local Data
Last-synced insights response cached locally per `child_id`.

## 14. Localization
All UI copy sourced from shared localization resources across EN/HI/AR/UR.

## 15. RTL
List and detail layouts mirror correctly.

## 16. Analytics
Emit `parent_story_insights_viewed` via `AnalyticsTracker`.

## 17. Performance
Standard list/detail performance practices — `LazyColumn` with stable keys, no special considerations beyond what's already established elsewhere in the Parent Area.

## 18. Security
This screen is only reachable through the Parent Area's existing access-control path (behind the Parent PIN/Biometric Gate at the Parent Area entry point) — this sub-feature does not need to re-implement gating, only correctly nest within the existing gated navigation graph.

## 19. Testing
- Unit: empty-state and staleness-note derivation logic.
- UI: list-to-detail navigation, empty state matches PRD copy exactly.
- Regression: confirm this screen/route is unreachable from anywhere in the child-facing `feature:stories` navigation graph (an explicit navigation-graph test asserting no edge exists from any child-facing route to `ParentStoryInsightsRoute`).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Locate the Existing Parent Area Navigation Graph**
Objective: Confirm the exact module/file (from C.20/C.22) before adding routes. Definition of Done: correct insertion point identified and documented.

**Task 02 — Add `ParentStoryInsightsRoute`/`ParentStoryInsightDetailRoute`**
Objective: Route registration within the Parent Area graph only. Dependencies: Task 01. Tests: navigation-graph isolation test (no reachability from child-facing graph). Definition of Done: isolation test passes.

**Task 03 — Implement `ParentStoryInsightsRepository`**
Objective: B-10 client with cache-first-offline read. Follow: `core-network`/`core-datastore` conventions. Tests: cache-fallback test. Definition of Done: test passes.

**Task 04 — Implement `ParentStoryInsightsViewModel`**
Objective: Empty-state and staleness-note derivation. Follow: `BaseViewModel`. Dependencies: Task 03. Tests: empty-state and staleness-note unit tests. Definition of Done: tests pass.

**Task 05 — Implement `ParentStoryInsightsScreen` and Detail Screen**
Objective: List + per-story detail (moral + quiz score) UI. Dependencies: Task 04. Tests: UI tests per §19. Definition of Done: all states render correctly.

**Task 06 — Add Analytics Instrumentation**
Objective: `parent_story_insights_viewed`. Tests: fake-tracker assertion. Definition of Done: exactly one call site.

**Task 07 — Full RTL Pass**
Objective: Verify mirroring. Tests: RTL snapshot tests. Definition of Done: baselines captured.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §19, including the navigation-graph isolation regression test. Definition of Done: all green.

**Task 09 — Final Code Review**
Objective: Confirm this screen is genuinely unreachable from the child-facing Stories module under any navigation path. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] Screen lives exclusively within the existing Parent Area navigation graph
- [ ] Confirmed unreachable from any child-facing `feature:stories` route (explicit isolation test)
- [ ] Empty state matches PRD copy exactly ("Once [Child] watches their first story...")
- [ ] Offline/stale data shows the "may not reflect today's offline activity yet" note when applicable
- [ ] List-to-detail navigation works correctly, showing moral + quiz score
- [ ] `parent_story_insights_viewed` analytics event fires correctly
- [ ] Full RTL mirroring verified

## 22. Definition of Done
Parents get an accurate, appropriately-gated, gracefully-degrading view of their child's story activity nested correctly within the existing Parent Area — with zero leakage of analytics framing into the child's own experience.
