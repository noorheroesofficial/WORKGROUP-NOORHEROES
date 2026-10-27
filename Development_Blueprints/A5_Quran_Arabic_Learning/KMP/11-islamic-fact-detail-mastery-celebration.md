# K-11 — Islamic Fact Detail & Mastery Celebration

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Two lightweight, high-delight screens: an Islamic Fact detail view linked from lesson/quiz content, and a celebratory modal shown when a skill node crosses the mastery threshold.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
K-11 — Islamic Fact Detail & Mastery Celebration

## 4. Objective
Render Islamic Fact detail content with full scholar-approval metadata and source references, and a Mastery Badge/Node-Unlock Celebration modal triggered by a `mastered` state transition.

## 5. Business Requirements
- FR-19: Islamic Facts must carry locale/age-banded text, topic/related-content linkage, primary/secondary source references, scholar approval and version, an explanation, a linked quiz item, and jurisprudential-scope/exclusion notes where relevant.

## 6. Existing Architecture
`feature-learn` module conventions per K-01–K-10. Islamic Fact content is sourced from the `content` context (existing catalog-style API per architecture doc §6 item 4); Mastery Celebration is purely a client-side reaction to K-01's skill-tree state data, no dedicated backend endpoint.

## 7. Existing Code to Reuse
- `content` context's existing content-detail fetch pattern (confirm exact endpoint before assuming a new one is needed).
- K-01's `SkillTreeViewModel` — detects `mastered` transitions from the skill-tree response diff to trigger the celebration modal.
- `core-designsystem` celebratory-modal pattern if one already exists elsewhere in the app (e.g., reward/badge celebrations in Feature A.11) — reuse rather than rebuild.

## 8. Files to Create
- `feature-learn/.../facts/IslamicFactDetailScreen.kt` + ViewModel
- `feature-learn/.../celebration/MasteryCelebrationModal.kt` (Composable)
- `feature-learn-domain/.../GetIslamicFactUseCase.kt`
- `feature-learn/src/commonTest/kotlin/.../IslamicFactDetailTest.kt`

## 9. Files to Modify
- `LearnRoute` — add `IslamicFactDetail` destination.
- K-01's `SkillTreeViewModel` — emit a celebration trigger event on detected `mastered` transitions.

## 10. Backend Requirements
Islamic Fact content: `content` context's existing fact/content-detail endpoint (confirm exact path). Mastery Celebration: no dedicated endpoint, purely derived from B-01's existing state data.

## 11. KMP Requirements
- **Islamic Fact Detail**: renders locale/age-banded text, topic and related-content linkage (navigable), primary/secondary source references, scholar-approval badge + version, an explanation, a linked quiz item (routes into K-08's quiz flow for that specific item if supported by A.8's contract), and jurisprudential-scope/exclusion notes where present.
- **Mastery Celebration**: `MasteryCelebrationModal` triggered when `SkillTreeViewModel` detects a node transitioning to `mastered` (comparing before/after skill-tree fetch results, or a dedicated event emitted by the mutation flow that caused the transition — e.g., B-03's attempt-submission response, if it surfaces the resulting state change); dismissible, routes back to Skill Tree.
- Reuse existing celebratory-modal visual pattern from elsewhere in the app if present (e.g., Rewards feature) rather than introducing a new one-off celebration UI paradigm.

## 12. NextJS Requirements
N/A directly; Islamic Fact content authored/approved via the existing `content` context's admin surface (not part of this feature's NextJS scope).

## 13. API Contract
Islamic Fact: existing `content` context detail endpoint (confirm exact path per Rule 30). Mastery Celebration: none (derived client-side).

## 14. Database Requirements
No new local persistence; fact content cached via the existing content-caching pattern if `content` context already provides one.

## 15. Validation
N/A client-side.

## 16. Authentication
Reuses existing child-session auth.

## 17. Authorization
N/A beyond authenticated child session.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Fact content load failure | Friendly error state, does not block navigation back |
| Celebration trigger ambiguity (unclear which mutation caused mastery) | Fall back to comparing consecutive skill-tree fetches rather than skipping the celebration entirely |

## 19. Offline First
Fact content offline-cacheable if `content` context supports it generally; Mastery Celebration works offline trivially since it's derived from already-cached skill-tree state.

## 20. Local Data
Reuses `content` context's existing caching pattern if present.

## 21. Localization
Fact text and all metadata fields localized/age-banded per `core-common/localization`.

## 22. RTL
Full RTL layout for both screens.

## 23. Analytics
`islamic_fact_linked_viewed`, `mastery_celebration_shown` via `AnalyticsTracker`.

## 24. Performance
Lightweight screens, no special performance concerns.

## 25. Security
No sensitive data.

## 26. Library Requirements
Koin, Ktor, Compose Multiplatform.

## 27. Testing
- Unit: Islamic Fact detail correctly surfaces all required metadata fields (scholar approval/version, source references, jurisprudential-scope notes when present).
- Unit: Mastery Celebration trigger logic correctly detects `mastered` transitions without false-triggering on unrelated state changes.
- UI test: linked quiz item and related-content navigation work correctly.

## 28. Documentation
KDoc noting the full metadata-field requirement for Islamic Fact content per FR-19, so future contributors don't silently drop a required field.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Islamic Fact Content API**
- Task ID: K-11-T01
- Objective: Verify the `content` context's fact-detail endpoint shape.
- Dependencies: None (verification task).
- Definition of Done: Endpoint confirmed and documented in §13.

**Task 02 — Build `IslamicFactDetailScreen`**
- Task ID: K-11-T02
- Implementation Details: All FR-19 metadata fields rendered.
- Dependencies: K-11-T01.
- Definition of Done: Screen renders correctly with a full fixture fact object in Compose Preview.

**Task 03 — Implement Mastery-Transition Detection & `MasteryCelebrationModal`**
- Task ID: K-11-T03
- Implementation Details: Detects `mastered` transitions from K-01's state flow; reuses existing celebratory-modal pattern if present in the app.
- Dependencies: K-01.
- Definition of Done: Modal correctly triggers on a simulated mastery transition in testing.

**Task 04 — Tests**
- Task ID: K-11-T04
- Dependencies: K-11-T01–T03.
- Definition of Done: All green in CI.

## 30. Definition of Done
Both screens live; Islamic Fact detail surfaces all required FR-19 metadata; Mastery Celebration correctly and only triggers on genuine mastery transitions; fully tested.

## 31. Final Verification Checklist
- [ ] Islamic Fact detail includes all FR-19 required fields (scholar approval/version, sources, jurisprudential-scope notes where applicable)
- [ ] Mastery Celebration triggers only on genuine `mastered` transitions, no false positives
- [ ] Linked quiz item and related-content navigation function correctly
- [ ] RTL/localization verified
- [ ] Full test suite green in CI
