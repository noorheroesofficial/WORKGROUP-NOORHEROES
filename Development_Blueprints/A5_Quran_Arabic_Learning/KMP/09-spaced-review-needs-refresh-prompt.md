# K-09 — Spaced Review & Needs-Refresh Prompt

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). A gentle, capped review-reminder component rendered on the Skill Tree for nodes B-06's scheduler has marked due.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
K-09 — Spaced Review & Needs-Refresh Prompt

## 4. Objective
Render the "Needs Refresh" prompt component on K-01's Skill Tree, respecting the server-provided daily cap, framed consistently as a gentle review invitation rather than a failure signal.

## 5. Business Requirements
- FR-4: `Needs Refresh` surfaces as a gentle "let's review this together" prompt, never framed as regression/failure.
- Edge Case 6: multiple due nodes capped per day (server-enforced by B-06), remainder queued for subsequent days without being dumped simultaneously.

## 6. Existing Architecture
`feature-learn` module conventions per K-01–K-08. This is a component embedded within K-01's `SkillTreeScreen`, not a standalone screen.

## 7. Existing Code to Reuse
- K-01's `SkillTreeViewModel`/`SkillTreeUiState` — the `needs_refresh` node list and cap are already part of B-01's response (post-B-06 scheduling), no separate fetch required.
- `core-designsystem` amber "needs refresh" iconography token (K-01-T08).

## 8. Files to Create
- `feature-learn/.../skilltree/NeedsRefreshPromptComponent.kt` (Composable)
- `feature-learn/src/commonTest/kotlin/.../NeedsRefreshPromptTest.kt`

## 9. Files to Modify
- `feature-learn/.../skilltree/SkillTreeScreen.kt` — embed the prompt component for `needs_refresh`-state nodes.

## 10. Backend Requirements
Consumes the `needs_refresh`-state nodes already present in B-01's `GET /v1/learning/paths` response (populated by B-06's nightly scheduler) — no separate endpoint needed.

## 11. KMP Requirements
- **Rendering**: gentle prompt component (per §2.1 design tokens — amber ring + gentle refresh icon, never alarming red) shown inline on due nodes within the Skill Tree.
- **Cap respected**: the prompt only renders for nodes the server has already marked `shown_today`/`needs_refresh` in the response — no client-side re-capping or re-computation of which nodes to show.
- **Framing**: copy consistently reads as "let's review this together" or equivalent gentle language — never regression/failure wording, verified via a copy-review checklist item as well as UI test string assertions.
- **Routing**: tapping the prompt routes to the relevant node-type screen (Surah Learning, Arabic Letters, Tajweed, or a Quran Game mode) based on the node's `node_type`, reusing K-03/K-05/K-06/K-07's existing navigation entry points — no new practice-screen logic introduced here.

## 12. NextJS Requirements
N/A.

## 13. API Contract
No dedicated endpoint — consumes B-01's existing response shape (nodes already carry `state: "needs_refresh"`).

## 14. Database Requirements
No new local persistence — rendered directly from K-01's already-cached skill-tree data.

## 15. Validation
N/A (purely presentational component).

## 16. Authentication
N/A (no separate network call).

## 17. Authorization
N/A (no separate network call).

## 18. Error Handling
N/A beyond K-01's existing skill-tree fetch error handling (this component simply doesn't render if the parent screen has no data).

## 19. Offline First
Renders from K-01's cached skill-tree data, consistent with K-01's offline/cache-fallback behavior.

## 20. Local Data
N/A beyond K-01's existing cache.

## 21. Localization
Prompt copy localized via `core-common/localization`, with locale-appropriate gentle phrasing (not a literal machine translation of "let's review this together" without tone review per locale).

## 22. RTL
Full RTL layout for the prompt component.

## 23. Analytics
`needs_refresh_prompt_shown`, `needs_refresh_review_completed` via `AnalyticsTracker`.

## 24. Performance
No special concerns — lightweight component embedded in K-01's existing render pass.

## 25. Security
N/A (no sensitive data, no separate network call).

## 26. Library Requirements
Compose Multiplatform only, consistent with K-01.

## 27. Testing
- Unit: routing logic correctly maps `node_type` to the right destination screen.
- UI test: prompt copy asserted against a gentle-language allowlist / against a negative-language blocklist (no "failed," "wrong," "regressed," etc.).
- Integration: prompt only renders for nodes the server marked `needs_refresh`, never client-computed.

## 28. Documentation
KDoc noting this component performs zero independent capping/scheduling logic — it is purely a presentational layer over B-06/B-01's already-computed state.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Build `NeedsRefreshPromptComponent`**
- Task ID: K-09-T01
- Implementation Details: Presentational component consuming `needs_refresh` nodes from K-01's existing `SkillTreeUiState`.
- Existing Files to Reuse: K-01's `SkillTreeViewModel`, `core-designsystem` amber iconography token.
- Dependencies: K-01, K-01-T08.
- Definition of Done: Component renders correctly in Compose Preview.

**Task 02 — Wire Routing to Node-Type Screens**
- Task ID: K-09-T02
- Implementation Details: Reuses K-03/K-05/K-06/K-07's existing navigation routes based on `node_type`.
- Dependencies: K-09-T01, K-03, K-05, K-06, K-07.
- Definition of Done: Tapping the prompt correctly routes to each node type in manual testing.

**Task 03 — Embed in `SkillTreeScreen`**
- Task ID: K-09-T03
- Files to Modify: `SkillTreeScreen.kt`.
- Dependencies: K-09-T01, K-09-T02.
- Definition of Done: Prompt renders inline for due nodes within the full Skill Tree screen.

**Task 04 — Tests**
- Task ID: K-09-T04
- Objective: Full coverage per §27, including the gentle-language copy assertion.
- Dependencies: K-09-T01–T03.
- Definition of Done: All green in CI.

## 30. Definition of Done
Needs-Refresh prompt live within the Skill Tree, correctly routed by node type, gentle framing verified, zero independent capping logic, fully tested.

## 31. Final Verification Checklist
- [ ] Prompt renders only for server-marked `needs_refresh` nodes, no client-side re-capping
- [ ] Copy consistently gentle, never regression/failure-framed (verified via string assertion test)
- [ ] Tap-routing correctly maps to each node type's existing screen
- [ ] RTL layout verified
- [ ] Full test suite green in CI
