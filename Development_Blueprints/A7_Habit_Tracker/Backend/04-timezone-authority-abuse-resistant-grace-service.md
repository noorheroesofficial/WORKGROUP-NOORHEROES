# B-04 — Timezone Authority & Abuse-Resistant Grace Service

> **Status**: ✅ **COMPLETED & VERIFIED**  
> **Completed Date**: 2026-09-14  
> **Implementation Scope**: Backend (Python FastAPI)  
> **Alembic Revision**: `0056_create_child_timezone_record_table.py` (`head`)  
> **Test Pass Rate**: 22 passed in `tests/modules/habits/test_timezone_grace_logic.py`, 123 passed in `tests/modules/habits/` (100% pass rate in 2.99s), 255 passed in architecture & routing suites  
> **Invariants Enforced**: Server-authoritative day boundary with deliberate client-trusted `local_date` asymmetry, 0 `ast.If` router additions, 0 cross-context joins

## 1. Feature Context
Part of Feature A.7 — Habit Tracker. Provides the server-maintained "what is today for this child" authority that the Streak State Machine (B-03) depends on for fair, abuse-resistant day-boundary evaluation.

## 2. Parent Feature
A.7 Habit Tracker — Backend (FastAPI)

## 3. Sub-feature
B-04 Timezone Authority & Abuse-Resistant Grace Service

## 4. Objective
Maintain each child's authoritative timezone-of-record and implement bounded, abuse-resistant grace logic so genuine travel never silently breaks a streak while device-timezone toggling cannot manufacture extra days (FR-9, FR-10, Edge Case 11).

## 5. Business Requirements
- Day-boundary evaluation for streak eligibility uses the **server-maintained** timezone-of-record, not raw device-reported time (FR-9) — note this is distinct from `local_date` in the check-in payload itself, which remains client-trusted per B-02 (this is a deliberate, documented asymmetry: the check-in date is trusted, but the day-boundary/eligibility interpretation of "today" is server-authoritative).
- A single genuine timezone change (e.g., real travel) receives generous grace.
- A rapid flip-flopping pattern (`change_count_30d` exceeding threshold) receives a more conservative grace window.
- Stale timezone-of-record must be updatable via automatic mismatch-signal detection or explicit confirmation, without a manual support ticket (Edge Case 11).
- Streak must never be silently broken purely due to a timezone shift.

## 6. Existing Architecture
Extends the `habits` bounded context (B-01–B-03). This is a distinct responsibility from `StreakService` per PRD §3.3's service breakdown table — implemented as its own module for testability and because it owns its own table (`child_timezone_record`) and its own nightly decay job, following the existing Celery background-task convention used by `localization`'s `retry_failed_translations_task()`.

## 7. Existing Code to Reuse
- Celery task registration pattern from `src/noorheroes/modules/localization/tasks.py` (`translate_content_task`, `retry_failed_translations_task`) as the template for the new nightly decay job.
- `get_current_child` dependency.

## 8. Files to Create
- `src/noorheroes/modules/habits/timezone_authority.py` — `TimezoneAuthorityService` (`evaluate_day_boundary()`, `record_timezone_observation()`, `compute_grace_window()`)
- Extend `models.py`: `ChildTimezoneRecord`
- `alembic/versions/<rev>_create_child_timezone_record_table.py`
- `src/noorheroes/modules/habits/tasks.py` — `decay_timezone_change_count_task()` (nightly Celery job)
- `tests/modules/habits/test_timezone_grace_logic.py`

## 9. Files to Modify
- `src/noorheroes/modules/habits/streak_service.py` — call `TimezoneAuthorityService.evaluate_day_boundary()` for the `day_has_closed` signal instead of raw UTC/device time
- `src/noorheroes/modules/habits/api.py` — internal use only; no new public endpoint required unless parent-facing timezone confirmation UI needs one (add `PATCH /v1/habits/timezone-confirmation` if Edge Case 11's explicit-confirmation path is exposed to the client)

## 10. Backend Requirements
- `evaluate_day_boundary(child_id, as_of)` returns whether "today" (per timezone-of-record) has closed, used exclusively by B-03's `StreakService`.
- `record_timezone_observation(child_id, observed_tz)` updates `current_timezone`, increments `change_count_30d` when the observed zone differs from the current record.
- `compute_grace_window(change_count_30d)` returns generous vs. conservative grace parameters, threshold sourced from the Admin-tunable config (B-10) rather than hardcoded.
- Nightly Celery job decays `change_count_30d` on a rolling 30-day basis.

## 11. KMP Requirements
Client sends `TimeZone.getDefault()` observations opportunistically (not authoritative, just a signal) — no dedicated screen required unless Edge Case 11's explicit-confirmation UX is built (optional, deferred to a future iteration unless product requires it now).

## 12. NextJS Requirements
Threshold/grace-window parameters configured via B-10/N-02, not hardcoded here.

## 13. API Contract

**Required API**
- **HTTP Method:** internal service call, no new public endpoint in the base case
- **Optional Endpoint (Edge Case 11 explicit path):** `PATCH /v1/habits/timezone-confirmation` — **Request:** `{ "confirmed_timezone": "Asia/Dubai" }` — **Response 200:** `{ "updated": true }` — **Authentication:** Bearer, child or parent session — flag as **deferred/optional** if not required for initial launch; do not build speculatively without product confirmation (rule 30 — do not guess).

## 14. Database Requirements
- `child_timezone_record`: `child_id UUID PK/FK`, `current_timezone VARCHAR`, `last_changed_at TIMESTAMPTZ`, `change_count_30d INT`.
- No additional index required beyond the PK given one row per child.

## 15. Validation
- Test a single legitimate travel-related timezone change → generous grace window applied.
- Test 6 timezone changes within 30 days → conservative grace window applied, distinct from the single-change path.

## 16. Authentication
Internal service; if the optional confirmation endpoint is built, Bearer session required.

## 17. Authorization
Timezone record scoped strictly to the owning child.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Timezone Authority evaluation fails | Streak Service falls back to last-known-good day-boundary evaluation rather than crashing (defense-in-depth, consistent with B-03 degraded-mode rule) |
| `change_count_30d` threshold config unavailable | Fall back to a safe conservative default, never fail open to an overly generous grace window |

## 19. Offline First
N/A (backend); this service's outputs are consumed server-side by B-03.

## 20. Local Data
N/A.

## 21. Localization
N/A.

## 22. RTL
N/A.

## 23. Analytics
`timezone_change_grace_applied` emitted with which grace path (generous/conservative) was used, for the Admin monitoring dashboard (N-06).

## 24. Performance
Single-row lookup per evaluation; nightly decay job runs as a scheduled Celery task, not inline with request handling.

## 25. Security
Abuse-resistance for streak/reward-adjacent fairness is treated with security-equivalent rigor per PRD §12.1 threat analysis (streak manipulation via timezone gaming).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Celery (existing task infrastructure), Pydantic v2.

## 27. Testing
- Unit: grace-window computation for both legitimate-travel and rapid-flip-flop scenarios (mandatory per PRD §5 backend prompt item 4).
- Integration: nightly decay job correctness over a simulated 30-day window.
- Regression: verify B-03 Streak Service correctly consumes day-boundary signals from this service without regressing existing transition tests.

## 28. Documentation
Document the deliberate asymmetry between client-trusted `local_date` (B-02) and server-authoritative day-boundary evaluation (this sub-feature) clearly in code comments to prevent future maintainers from "fixing" it into a false consistency.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create ChildTimezoneRecord Model & Migration**
- Files to Create: `models.py` extension, `alembic/versions/<rev>_create_child_timezone_record_table.py`
- Definition of Done: table created, PK/FK correct.
- Status: ✅ Completed & Verified (`ChildTimezoneRecord` in `src/noorheroes/modules/habits/models.py`, `0056_create_child_timezone_record_table.py`)

**Task 02 — Implement TimezoneAuthorityService**
- Files to Create: `timezone_authority.py`
- Existing Architecture to Follow: `BaseService` pattern.
- Business Rules: FR-9, FR-10.
- Tests: unit tests for `evaluate_day_boundary`, `record_timezone_observation`, `compute_grace_window`.
- Definition of Done: service methods correctly implement generous vs. conservative grace logic.
- Status: ✅ Completed & Verified (`TimezoneAuthorityService` in `src/noorheroes/modules/habits/timezone_authority.py`)

**Task 03 — Wire into Streak Service**
- Files to Modify: `streak_service.py`
- Implementation Details: replace raw-time day-boundary check with `TimezoneAuthorityService.evaluate_day_boundary()` call.
- Tests: regression test confirming B-03's exhaustive transition tests still pass with the new day-boundary source.
- Definition of Done: no regression in B-03 test suite.
- Status: ✅ Completed & Verified (integrated into `StreakService.evaluate_and_persist` and `recalculate`)

**Task 04 — Implement Nightly Decay Celery Task**
- Files to Create: `tasks.py`
- Existing Architecture to Follow: `localization` context's Celery task pattern.
- Implementation Details: rolling 30-day decay of `change_count_30d`.
- Tests: simulated time-window unit test.
- Definition of Done: task registered and verified in staging schedule.
- Status: ✅ Completed & Verified (`decay_timezone_change_count_task` in `src/noorheroes/modules/habits/tasks.py` & `celery_app.py`)

**Task 05 — Add Grace-Path Tests**
- Files to Create: `tests/modules/habits/test_timezone_grace_logic.py`
- Implementation Details: single-change generous path test; 6-changes-in-30-days conservative path test.
- Definition of Done: both tests passing (mandatory per PRD §5 item 4).
- Status: ✅ Completed & Verified (22 dedicated tests passing in `tests/modules/habits/test_timezone_grace_logic.py`)

**Task 06 — Add Analytics & Monitoring Hooks**
- Implementation Details: `timezone_change_grace_applied` event; alert on threshold-breach-rate trending up (cross-ref N-06).
- Definition of Done: event emitted correctly, alert wired.
- Status: ✅ Completed & Verified (`TimezoneChangeGraceApplied` outbox event + `child_timezone_flip_flop_threshold_breached` structured log alert)

**Task 07 — Add Logging & Documentation**
- Documentation: asymmetry note per §28.
- Definition of Done: docs complete.
- Status: ✅ Completed & Verified (`FAST-API-INSTRUCTIONS.md` §5.15, §6, §9; `MASTER-README.md` §11.52)

**Task 08 — Final Code Review**
- Do Not Change: B-02's client-trusted `local_date` behavior (must remain independent of this service).
- Expected Result: PR merge-ready.
- Status: ✅ Completed & Verified (client-trusted `local_date` asymmetry strictly preserved)

## 30. Definition of Done
- Server-authoritative day-boundary evaluation correctly wired into Streak Service without regressing B-03's exhaustive tests.
- Generous vs. conservative grace paths verified by dedicated tests.
- Nightly decay job operational.

## 31. Final Verification Checklist
- [x] `ChildTimezoneRecord` table created (Verified: `ChildTimezoneRecord` ORM model in `src/noorheroes/modules/habits/models.py`, `child_id UUID PK/FK` referencing `child_profiles.id` with cascade, zero redundant index beyond PK, and reversible Alembic migration `0056_create_child_timezone_record_table.py` at `head`)
- [x] Generous single-change grace path test passes (Verified: `test_generous_grace_path_single_change` in `tests/modules/habits/test_timezone_grace_logic.py` asserting 3-day travel grace window)
- [x] Conservative rapid-flip-flop grace path test passes (Verified: `test_conservative_grace_path_six_changes` in `tests/modules/habits/test_timezone_grace_logic.py` asserting 1-day flip-flop grace window for `change_count_30d > 5`)
- [x] B-03 exhaustive transition tests still pass after integration (Verified: all 49 state machine matrix and transition tests pass in `test_streak_state_machine.py` with server-authoritative day-boundary evaluation)
- [x] Nightly decay Celery task registered and tested (Verified: `decay_timezone_change_count_task` registered in `src/noorheroes/modules/habits/tasks.py` and scheduled in `src/noorheroes/core/celery_app.py:beat_schedule`)
- [x] `timezone_change_grace_applied` analytics event wired (Verified: strongly-typed Pydantic model `TimezoneChangeGraceApplied` in `src/noorheroes/modules/habits/events.py` and mapped to `habits.on_timezone_change_grace_applied` in `src/noorheroes/common/outbox_relay.py:DISPATCH_TABLE`)
- [x] Threshold-breach monitoring alert wired (cross-ref N-06) (Verified: structured log warning `child_timezone_flip_flop_threshold_breached` in `TimezoneAuthorityService.record_timezone_observation`)
- [x] Client-trusted `local_date` behavior (B-02) left unaffected (Verified: deliberate architectural asymmetry invariant preserved across `process_check_in` and `evaluate_day_boundary` per §5 & §28)

## 32. Implementation Artifacts & Verified Files
- **Database Schema & Migration**:
  - `src/noorheroes/modules/habits/models.py`: `ChildTimezoneRecord` ORM model on table `child_timezone_record` (`child_id UUID PK/FK` cascade to `child_profiles.id`, `current_timezone VARCHAR(64)`, `last_changed_at TIMESTAMPTZ`, `change_count_30d INT`)
  - `alembic/versions/0056_create_child_timezone_record_table.py`: Reversible schema migration (current `head`)
- **Domain Services & Repositories**:
  - `src/noorheroes/modules/habits/repository.py`: `TimezoneAuthorityRepository` (`get_record`, `upsert_observation`, `decay_change_counts`)
  - `src/noorheroes/modules/habits/timezone_authority.py`: `TimezoneAuthorityService` (`evaluate_day_boundary`, `record_timezone_observation`, `compute_grace_window`, `decay_all_change_counts`)
  - `src/noorheroes/modules/habits/streak_service.py`: Day-boundary evaluation wired into `evaluate_and_persist` and `recalculate` via `TimezoneAuthorityService.evaluate_day_boundary()`
- **Background Tasks & Celery Beat**:
  - `src/noorheroes/modules/habits/tasks.py`: `decay_timezone_change_count_task` (`habits.decay_timezone_change_count`)
  - `src/noorheroes/core/celery_app.py`: Nightly beat schedule entry `habits-decay-timezone-change-count-nightly` running daily at 00:05 UTC
- **Domain Events & Outbox**:
  - `src/noorheroes/modules/habits/events.py`: `TimezoneChangeGraceApplied` (`timezone_change_grace_applied`)
  - `src/noorheroes/common/outbox_relay.py`: Registered in `DISPATCH_TABLE` under `habits.on_timezone_change_grace_applied`
- **Error Codes & Localization**:
  - `src/noorheroes/modules/habits/exceptions.py`: `InvalidTimezoneError` (`INVALID_TIMEZONE`)
  - `src/noorheroes/core/i18n.py`: Full 4-language localized translations (`en`, `hi`, `ur`, `ar`) in `ERROR_TRANSLATION_CATALOG` with 100% script purity
- **Automated Test Suites**:
  - `tests/modules/habits/test_timezone_grace_logic.py`: 22 comprehensive tests covering generous travel grace, conservative flip-flop grace, boundary conditions, repository persistence, Celery decay, fallback defaults, and zero-AST-branching
  - Habit context suite: 123/123 passed in 5.47s
  - Core suite: 260/260 passed in 35.65s (including zero missing error codes verification in `test_i18n.py`)
  - Architecture & routing suite: 255 passed in 38.12s

