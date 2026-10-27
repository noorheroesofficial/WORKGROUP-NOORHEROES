# K-11 — Habit Tracker Analytics & Cross-Platform Event Instrumentation

## 1. Feature Context
NoorHeroes KMP app. Final wiring and verification pass ensuring the complete PRD §1.19 event taxonomy is correctly instrumented across every Habit Tracker screen built in K-01–K-10.

## 2. Parent Feature
A.7 Habit Tracker — KMP App (Android/iOS)

## 3. Sub-feature
K-11 Habit Tracker Analytics & Cross-Platform Event Instrumentation

## 4. Objective
Verify and complete the full analytics event taxonomy across all Habit Tracker screens, including the two ethically-important funnels (main engagement funnel and recovery-path funnel), with aggregate-only schema enforcement carried through to the analytics layer for Family Garden events.

## 5. Business Requirements
- Full event taxonomy per PRD §1.19 wired across every relevant screen (cross-cutting verification task, not new UI).
- Main funnel: `habit_builder_viewed` → `habit_checked_in` → `streak_state_changed` (to active) → `family_streak_milestone_reached` (if applicable).
- Recovery funnel: `streak_broken_shown` → `recovery_mission_started` → `recovery_mission_completed` — this validates the feature's core ethical-design hypothesis (does mercy/recovery design actually re-engage children).
- Family Garden/aggregate events remain schema-aggregate-only, mirroring B-06's structural guarantee even at the analytics layer.

## 6. Existing Architecture
Uses the existing `core-analytics` `AnalyticsTracker` interface (`logEvent(name, params)`) — this sub-feature is an audit/completion pass, not a new module.

## 7. Existing Code to Reuse
`AnalyticsTracker` from `core-analytics`; existing NoorHeroes analytics event-parameter validation conventions (if a schema-validation utility already exists elsewhere in the codebase, reuse it for the aggregate-only event verification).

## 8. Files to Create
- `feature-habits/src/commonTest/kotlin/.../HabitAnalyticsEventCoverageTest.kt` (asserts every §1.19 event is fired from at least one code path)
- `feature-habits/src/commonTest/kotlin/.../FamilyGardenEventSchemaTest.kt` (asserts Family Garden event params contain no per-child fields)

## 9. Files to Modify
Any K-01–K-10 file found missing an event during the audit (tracked per-finding, not pre-enumerated here since it depends on audit results).

## 10. Backend Requirements
None directly (analytics events are client-emitted; backend event-bus ingestion is existing shared infrastructure).

## 11. KMP Requirements
- Audit every screen built in K-01–K-10 against the full PRD §1.19 event list: `habit_builder_viewed`, `habit_checked_in`, `habit_checkin_duplicate_ignored`, `habit_unchecked` (if toggle-off supported), `dhikr_counter_opened`, `dhikr_target_reached`, `dhikr_target_changed_midday`, `fasting_tracker_logged`, `good_deed_category_selected`, `good_deed_note_added`, `streak_state_changed`, `streak_shield_applied`, `streak_broken_shown`, `recovery_mission_started`, `recovery_mission_completed`, `recovery_window_expired`, `mercy_suggestion_shown`, `mercy_suggestion_accepted`, `family_streak_milestone_reached`, `noor_garden_viewed`, `parent_habit_visibility_configured`, `parent_verification_requested`, `parent_verification_completed`, `weekly_habit_report_viewed`, `ramadan_mode_checklist_activated`, `ramadan_mode_checklist_deactivated`, `timezone_change_grace_applied` (server-emitted, verify client surfaces it if needed), `backfilled_checkin_synced`.
- Verify event-parameter shapes match documented fields (`habit_type`, `local_date`, `from_state`, `to_state`, `streak_type`, etc.).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
N/A (client-side analytics instrumentation task).

## 14. Database Requirements (Local)
None.

## 15. Validation
Mandatory: event-coverage test enumerating the full §1.19 list against the actual call sites found in K-01–K-10; any missing event fails the test and must be added.

## 16. Authentication
N/A.

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Analytics call fails | Never blocks or delays the underlying user action; fire-and-forget with existing `core-analytics` retry/queue behavior |

## 19. Offline First
Analytics events queue via existing `core-analytics` offline-tolerant dispatch, consistent with the rest of the app.

## 20. Local Data
N/A beyond existing `core-analytics` queuing.

## 21. Localization
N/A (event names/params are not user-facing).

## 22. RTL
N/A.

## 23. Analytics
This sub-feature's entire scope is analytics; see §11 for the full list.

## 24. Performance
Event firing must not introduce perceptible UI latency (standard `core-analytics` async dispatch).

## 25. Security
`family_streak_milestone_reached`/Family Garden events verified free of any per-child parameter, mirroring B-06/K-05's structural guarantees.

## 26. Library Requirements
`core-analytics`.

## 27. Testing
- Mandatory: full event-coverage test against §1.19 list.
- Mandatory: Family Garden event schema test (no per-child params).
- Funnel verification: manual/QA trace of both documented funnels end-to-end in staging.

## 28. Documentation
Document the complete event taxonomy and its owning screen/file in a single reference table for future maintainers (append to `feature-habits`'s module-level README or KDoc index).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Audit Existing Event Instrumentation Against §1.19**
- Objective: Identify gaps between the documented taxonomy and actual K-01–K-10 implementations.
- Files to Create: `HabitAnalyticsEventCoverageTest.kt`
- Definition of Done: test enumerates every documented event and asserts a firing call site exists for each.

**Task 02 — Fill Identified Gaps**
- Files to Modify: whichever K-0x files the audit identifies as missing an event.
- Definition of Done: coverage test passes 100%.

**Task 03 — Write Family Garden Event Schema Test**
- Files to Create: `FamilyGardenEventSchemaTest.kt`
- Definition of Done: test confirms no per-child parameter exists in any Family Garden-related event payload.

**Task 04 — Verify Both Funnels End-to-End**
- Action: Manual/QA staging trace of the main funnel and recovery funnel.
- Definition of Done: both funnels observable and correctly sequenced in the analytics dashboard.

**Task 05 — Final Code Review**
- Expected Result: PR merge-ready, both mandatory tests green.

## 30. Definition of Done
Full PRD §1.19 event taxonomy verified as correctly instrumented across all Habit Tracker screens; both funnels verified end-to-end; Family Garden events confirmed schema-clean.

## 31. Final Verification Checklist
- [ ] Every event in PRD §1.19 has a verified firing call site
- [ ] Event-coverage test passes 100% (mandatory)
- [ ] Family Garden event schema test passes (no per-child params, mandatory)
- [ ] Main engagement funnel traceable end-to-end in staging
- [ ] Recovery-path funnel traceable end-to-end in staging
- [ ] Event parameter shapes match documented fields
