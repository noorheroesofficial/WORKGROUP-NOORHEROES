# K-03 — AI Interaction History Screen

## 1. Feature Context
Part of Feature C.26. The client half of B-02's extended AI history read API — a calm, deliberately non-chat-like safety-transparency surface, visually the same family as C.22's AI Safety Log but at a fuller depth.

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**K-03 — AI Interaction History Screen**

## 4. Objective
Render a filterable, redacted AI interaction list sourced from B-02's extended endpoint, reusing C.22's established "never chat-bubble-shaped" UI test pattern and visual language rather than inventing a new one.

## 5. Business Requirements
- FR-6/FR-7: redacted summaries, `model_version`, `policy_result` icon, no raw content ever.
- Edge Case 4/8: "no interactions this period" vs. "AI always off" distinct empty states.
- §2.2 Screen: filterable by child/date, calm icon per `policy_result`.
- §7 Android AI Code-Generation Prompt item 3: reuse C.22's exact structural UI test pattern.

## 6. Existing Architecture
**Depends on B-02's cross-feature resolution being adopted** (extending C.22's `ai_safety_event`-backed endpoint rather than a new table/route) — if unresolved, this screen has no confirmed data contract to build against; do not implement independently of that resolution. Once resolved, this screen is visually and structurally a sibling to C.22 K-03 (`AiInteractionHistoryScreen`) — reuse its Composable patterns/visual tokens directly rather than redesigning.

## 7. Existing Code to Reuse
- C.22 K-03's `AiInteractionHistoryScreen` Composable structure and the "no chat-bubble-shaped component" UI test pattern — reused verbatim, not reinvented, per the Android AI Code-Generation Prompt's explicit instruction.
- `AiHistoryRepository` — new for this feature, but modeled directly on C.22's equivalent repository consuming the same (extended) endpoint.
- `:core:design-system`'s neutral status icons (checkmark/shield/arrow for allowed/blocked/redirected).

## 8. Files to Create
- `feature/parent-settings/src/commonMain/kotlin/.../AiInteractionHistoryScreen.kt`
- `feature/parent-settings/src/commonMain/kotlin/.../AiInteractionDetailScreen.kt`
- `feature/parent-settings/src/commonMain/kotlin/.../AiHistoryViewModel.kt`
- `core-data/.../AiHistoryRepository.kt` (interface) + impl

## 9. Files to Modify
- `ParentSettingsNavGraph.kt` (K-01) — wire routes.

## 10. Backend Requirements
Consumes B-02's extended `GET /v1/children/{id}/ai-history` exclusively.

## 11. KMP Requirements
- Filter row: child selector + date-range chips.
- List: each entry shows redacted summary, small neutral `policy_result` icon, `model_version` in muted text, date — **no chat-bubble shape, no quoted-text-as-a-message-bubble rendering anywhere in this composable tree.**
- Two distinct empty states: "AI has been off for this child the entire time" (`ai_never_enabled: true` from B-02) vs. "No AI interactions in this period" (empty `entries` with `ai_never_enabled: false`).
- Detail screen shows the full redacted entry — still never a raw transcript, since none exists to show.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes B-02's contract as documented in that blueprint (pending its cross-feature resolution).

## 14. Database Requirements
Local cache of the last-fetched history list, per §19/§20.

## 15. Validation
Date-range filter validated client-side (`from <= to`) before firing the request.

## 16. Authentication
Parent session (no step-up required — this is a read-only view, consistent with §1.15 Permission States).

## 17. Authorization
None beyond standard parent-child family-ownership, enforced server-side.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| API failure | Empty-state fallback with retry, never a raw error dump |
| Invalid date range selected | Inline validation message, request not sent |
| Zero entries | Correct one of the two distinct empty states (§11) |

## 19. Offline First
Renders last-cached data offline; filter changes requiring a new fetch are blocked with a clear offline indicator if no connectivity.

## 20. Local Data
Cached in `:core:offline-cache`, keyed by child + date range.

## 21. Localization
Redacted summary text is already server-localized (per B-02/C.22's design); UI chrome (filter labels, empty-state copy) sourced via string resources.

## 22. RTL
Full RTL mirroring, including icon placement relative to text.

## 23. Analytics
`ai_interaction_history_viewed`, `ai_interaction_detail_viewed`, `ai_history_empty_state_shown` (with `reason: never_enabled|no_interactions_period`).

## 24. Performance
Lazy-loaded list for potentially large histories; stable, immutable list-item state to avoid unnecessary recomposition.

## 25. Security
This screen's defining guarantee is purely visual/structural (no chat-bubble rendering that could imply a transcript exists) — the actual data-safety guarantee lives entirely in B-02/C.22's backend; this screen must not undermine that by rendering redacted text in a way that visually suggests more content exists than is shown.

## 26. Library Requirements
No new libraries.

## 27. Testing
- **Highest-priority UI test (reused from C.22's pattern):** no chat-bubble-shaped component or quoted-text rendering exists anywhere in this screen's composition tree.
- UI test: both empty states render correctly and distinctly for their respective conditions.
- Integration test: filter by child/date range correctly re-queries B-02.
- Offline test: last-cached list renders correctly with no network.

## 28. Documentation
KDoc noting this screen intentionally mirrors C.22 K-03's visual/structural pattern and depends on B-02's resolved data contract.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm B-02's Contract Is Resolved**
- **Objective:** Do not start without B-02's cross-feature sign-off finalized.

**Task 02 — `AiHistoryRepository`**
- **Files to Create:** interface + impl.

**Task 03 — `AiInteractionHistoryScreen` with Reused C.22 Pattern**
- **Files to Create:** screen composable.
- **Tests:** the highest-priority chat-bubble-absence test, ported from C.22's existing test.

**Task 04 — Two Distinct Empty States**
- **Definition of Done:** Both conditions render distinguishably, verified by test.

**Task 05 — Detail Screen, Filtering, Offline Caching**

**Task 06 — Localization, RTL, Analytics**

**Task 07 — Full Test Suite**

## 30. Definition of Done
AI Interaction History renders fully redacted entries with zero chat-like presentation, both empty states correctly distinguished, filtering works, and the screen depends cleanly on B-02's resolved (not duplicated) data contract.

## 31. Final Verification Checklist
- [ ] B-02's contract confirmed resolved before implementation
- [ ] Chat-bubble-absence signature test passes (ported from C.22)
- [ ] Both empty states correctly distinguished
- [ ] Filter by child/date functions correctly
- [ ] Full localization and RTL verified
- [ ] Offline last-cached rendering verified
