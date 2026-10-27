# K-05 — Habit Tracker Reminder Suggestion Integration

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. Consumes B-06's real outbox-emitted `dua_marked_learned` event (consumed by the `habits` context per B-06's coordination) and deep-links into A.7's real habit-creation flow, likely `A7_Habit_Tracker/KMP/07-habit-reminder-deep-link-quiet-hours-landing.md`'s existing deep-link target — **confirm the exact deep-link URI/param contract from that file before wiring, do not invent it.**

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
K-05 — Habit Tracker Reminder Suggestion Integration

## 4. Objective
Show a dismissible inline suggestion card after server-confirmed mark-as-learned, deep-linking into A.7's real habit-creation flow pre-filled with the dua's reference, with per-dua dismissal persistence via the real datastore module.

## 5. Business Requirements
FR-9; dismissed flag persists per dua but allows re-suggestion if no habit was ever created; Edge Case 11 (un-marking never deletes an existing habit — enforced by B-06 never emitting an "unlearned" event, nothing for this file to additionally guard against).

## 6. Existing Architecture
Local persistence via the real `com.noorheroes.core.datastore.store`/`PreferenceManager` (per `CORE_DATASTORE_INSTRUCTIONS.md`), not a generic `:core:datastore` placeholder. Deep-link target owned by A.7 — confirm its actual URI scheme/params (Task 01).

## 7. Existing Code to Reuse
- `core/datastore`'s `PreferenceManager` — per-dua dismissed-flag storage
- `Navigator.navigateTo()` (real navigation API) for the deep-link hand-off
- A.7's real habit-creation deep-link target (pending confirmation)

## 8. Files to Create
- `feature/dua/src/commonMain/kotlin/.../habit/HabitReminderSuggestionCard.kt`
- `feature/dua/src/commonTest/kotlin/.../HabitSuggestionDismissalTest.kt`
- `feature/dua/src/androidUiTest/kotlin/.../HabitReminderSuggestionCardTest.kt`

## 9. Files to Modify
- `DuaCardDetailScreen.kt` (K-02) — mount the card post-server-confirmed mark-as-learned

## 10. Backend Requirements
Relies on B-06's eligibility-gated outbox event, consumed by `habits`; no direct backend call from this file beyond checking habit-existence (if A.7 exposes such a query — confirm, per rule 30).

## 11. KMP Requirements
- Card shown only after server-confirmed mark-as-learned (K-02's `DuaCardUiState`, not optimistic local state)
- Primary action calls `Navigator.navigateTo(NavigationAction.ToHabitCreation(prefill = duaId))` or A.7's actual real equivalent (Task 01)
- Dismissed flag persisted per-dua via `PreferenceManager`
- Re-suggestion allowed if child re-visits the dua's own detail screen and the habit was never actually created (requires A.7's habit-existence query — confirm it exists before assuming)

## 12. NextJS Requirements
N/A.

## 13. API Contract
Owned by A.7 — not restated here to avoid drift.

## 14. Database Requirements
Local `PreferenceManager` entry keyed by `dua_id`.

## 15. Validation
N/A beyond dua_id validity (inherited from K-02's already-loaded context).

## 16. Authentication
Inherited child-mode session.

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Deep-link into A.7 fails | Fallback to in-app navigation to the Habit Tracker tab via `Navigator` |
| Habit-existence check unavailable | Default to showing the suggestion (fail-open, since suppressing a valid suggestion is worse UX than an occasional redundant one) |

## 19. Offline First
Dismissed-flag read/write works fully offline via `PreferenceManager`.

## 20. Local Data
Per-dua dismissed flag.

## 21. Localization / 22. RTL
Suggestion copy fully localized, RTL-correct.

## 23. Analytics
`dua_habit_reminder_suggested`, `dua_habit_reminder_accepted`, `dua_habit_reminder_dismissed` via `AnalyticsTracker`.

## 24. Performance
Lightweight; no heavy computation.

## 25. Security
No new sensitive data; deep-link payload limited to a dua reference id.

## 26. Library Requirements
`core/datastore` (`PreferenceManager`), `core/navigation` (`Navigator`) — existing dependencies only.

## 27. Testing
- Unit: dismissed-flag persistence and re-suggestion logic
- UI: card visibility across dismissed/never-created/eligible states
- Integration: mark-as-learned confirmation → card appears → deep link → A.7's real flow receives the correct prefill (verified against A.7's actual contract, not a mock of an assumed one)

## 28. Documentation
Record the confirmed A.7 deep-link contract (Task 01's finding).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm A.7's Real Deep-Link & Habit-Existence Contract**
Task ID: K-05-T01. Objective: read `A7_Habit_Tracker/KMP/07-habit-reminder-deep-link-quiet-hours-landing.md` (and any habit-existence query it or a sibling file exposes) before wiring anything. Definition of Done: contract confirmed and documented, or flagged as an open dependency if not yet built.

**Task 02 — Implement Dismissal Persistence**
Task ID: K-05-T02. Files to Create: `HabitReminderSuggestionCard.kt` (dismissal logic portion). Existing Files to Reuse: `PreferenceManager`. Definition of Done: persistence unit tests pass.

**Task 03 — Implement Suggestion Card**
Task ID: K-05-T03. Dependencies: Task 01. Definition of Done: correct deep-link payload verified against the real A.7 contract.

**Task 04 — Implement Visibility Logic**
Task ID: K-05-T04. Definition of Done: dismissed×habit-exists matrix all correct.

**Task 05 — Mount Post-Server-Confirmation**
Task ID: K-05-T05. Files to Modify: `DuaCardDetailScreen.kt`. Definition of Done: card only appears after server confirmation.

**Task 06 — Add Fallback Navigation**
Task ID: K-05-T06. Definition of Done: fallback test passes.

**Task 07 — Add Analytics & Tests**
Task ID: K-05-T07. Definition of Done: all §27 scenarios covered.

**Task 08 — Final Code Review**
Task ID: K-05-T08. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
Suggestion card correctly surfaces post-confirmation, respects dismissal nuance, and hands off correctly into A.7's real (confirmed, not assumed) flow.

## 31. Final Verification Checklist
- [ ] A.7's real deep-link contract confirmed before implementation, not assumed
- [ ] Card shown only after server-confirmed mark-as-learned
- [ ] Dismissed flag suppresses repeats; re-suggestion works when habit never created
- [ ] Uses real `PreferenceManager`/`Navigator`, not invented placeholders

## 32. Addendum — What Changed From the Original Draft
Corrected from a generic `:core:datastore` placeholder to the real `com.noorheroes.core.datastore.store`/`PreferenceManager`, and from an assumed deep-link contract to an explicit confirm-before-build task against A.7's real, already-existing `KMP/07-habit-reminder-deep-link-quiet-hours-landing.md` file.
