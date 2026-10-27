# K-03 — Good Deed Logging & Fasting Tracker Flow

## 1. Feature Context
NoorHeroes KMP app. Two lighter-weight habit-type flows: Good Deed category logging with optional note, and the parent-controlled Fasting Tracker.

## 2. Parent Feature
A.7 Habit Tracker — KMP App (Android/iOS)

## 3. Sub-feature
K-03 Good Deed Logging & Fasting Tracker Flow

## 4. Objective
Build the Good Deed category selector + optional note entry, and the Fasting Tracker screen (parent-enabled only), backing FR-4 and FR-17.

## 5. Business Requirements
- Good deed note is always optional, never required (FR-4).
- Fasting Tracker only renders if parent-enabled for the child (FR-17), with linked age-appropriate fasting education content.
- Both flows fully offline-capable for logging.

## 6. Existing Architecture
Extends `feature-habits`/`feature-habits-domain` (K-01). Uses `core-navigation` for modal/sheet presentation of the category selector.

## 7. Existing Code to Reuse
- `HabitRepository`/check-in use case (K-01)
- `content` context-backed fasting-education content reference, consumed via existing `feature-learn`/`feature-stories` content-fetch pattern if applicable (reuse rather than build a new content pipeline)

## 8. Files to Create
- `feature-habits/src/commonMain/kotlin/.../gooddeed/GoodDeedCategorySelector.kt` (Modal/Sheet)
- `feature-habits/src/commonMain/kotlin/.../gooddeed/GoodDeedNoteEntryScreen.kt`
- `feature-habits/src/commonMain/kotlin/.../fasting/FastingTrackerScreen.kt`
- `feature-habits/src/commonMain/kotlin/.../gooddeed/GoodDeedViewModel.kt`
- `feature-habits/src/commonTest/kotlin/.../GoodDeedOptionalNoteTest.kt`

## 9. Files to Modify
- `HabitBuilderScreen.kt` (K-01) — wire good-deed and fasting habit-row taps to these flows

## 10. Backend Requirements
Consumes `POST /v1/habits/check-ins` with `note_category` (B-02); fasting visibility sourced from `GET /v1/habits` (B-01)'s `fasting_tracker_enabled` gating.

## 11. KMP Requirements
- Category selector as a Modal/Sheet on good-deed habit tap.
- Optional note entry screen, clearly skippable (no forced text field).
- Fasting Tracker screen only rendered when `fasting_tracker_enabled=true` in the catalog response; linked fasting-education content entry point.
- Both flows check in via the standard `CheckInHabitUseCase` (K-01) with the appropriate `note_category`.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`POST /v1/habits/check-ins` (B-02) with `note_category` field populated for good deeds.

## 14. Database Requirements (Local)
Reuses K-06's offline outbox for both flows' check-in writes; no additional local tables required.

## 15. Validation
Test asserting the note entry screen can be skipped/dismissed without blocking check-in completion.

## 16. Authentication
Shared `core-network` Bearer token attachment.

## 17. Authorization
N/A at UI layer; fasting visibility is server-enforced (B-01), not just client-hidden.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Good deed check-in offline | Queued via K-06 outbox, same as any other habit type |
| Fasting habit not enabled | Screen/row simply absent, not shown-then-blocked |
| Fasting education content fails to load | Fasting check-in still functional; content shown as unavailable with retry, not a blocking error |

## 19. Offline First
Both flows fully offline-capable for the check-in action itself, per K-06's shared outbox mechanism.

## 20. Local Data
Shared with K-01/K-06's offline outbox; no separate local persistence needed beyond in-flight UI state.

## 21. Localization
Good-deed category labels and fasting-education content fully localized (EN/HI/AR/UR).

## 22. RTL
Category selector grid/list and note entry field mirror correctly.

## 23. Analytics
`good_deed_category_selected`, `good_deed_note_added`, `fasting_tracker_logged` via `AnalyticsTracker`.

## 24. Performance
Modal/sheet presentation should not block the underlying checklist's responsiveness; note entry is a lightweight text field, no heavy processing.

## 25. Security
Optional note content is standard child-generated content, not specially sensitive; never required, minimizing collection by design (FR-4 cross-ref PRD §12.6).

## 26. Library Requirements
Compose Multiplatform, Koin, Ktor, Room (shared outbox from K-06).

## 27. Testing
- Unit: skip-note-and-check-in-succeeds test.
- Unit: fasting row absent when not parent-enabled.
- UI: category selector and note entry Compose tests.

## 28. Documentation
KDoc noting that the note field must never be made required in any future change (ties to FR-4 and the platform's minimal-data-collection principle).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Build Good Deed Category Selector & Note Entry**
- Objective: Modal/sheet + optional note screen.
- Files to Create: `GoodDeedCategorySelector.kt`, `GoodDeedNoteEntryScreen.kt`, `GoodDeedViewModel.kt`
- Business Rules: FR-4 (note always optional).
- Tests: skip-note test (mandatory).
- Do Not Change: do not make the note field required under any future iteration without explicit product sign-off.
- Definition of Done: flow completes correctly with and without a note.

**Task 02 — Build Fasting Tracker Screen with Visibility Gating**
- Objective: Parent-enabled-only fasting flow with linked education content.
- Files to Create: `FastingTrackerScreen.kt`
- Business Rules: FR-17.
- Existing Files to Reuse: existing content-fetch pattern from `feature-learn`/`feature-stories`.
- Tests: visibility-gating unit test.
- Definition of Done: screen only appears when enabled; education content links correctly.

**Task 03 — Wire Both Flows into Habit Builder**
- Files to Modify: `HabitBuilderScreen.kt`
- Definition of Done: taps correctly route to the respective flow.

**Task 04 — Add Analytics & Localization**
- Definition of Done: events wired, all strings localized, RTL verified.

**Task 05 — Final Code Review**
- Expected Result: PR merge-ready.

## 30. Definition of Done
Good Deed and Fasting Tracker flows live, fully offline-capable, correctly gated by parent configuration, note always optional.

## 31. Final Verification Checklist
- [ ] Good deed note entry is always skippable
- [ ] Fasting Tracker only renders when parent-enabled
- [ ] Both flows check in via the shared offline outbox
- [ ] Fasting education content linked correctly
- [ ] Localization and RTL verified
- [ ] Analytics events wired
