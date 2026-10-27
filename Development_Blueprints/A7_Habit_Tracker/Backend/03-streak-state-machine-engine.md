# B-03 — Streak State Machine Engine

> **Status**: ✅ **COMPLETED & VERIFIED**  
> **Completed Date**: 2026-09-14  
> **Implementation Scope**: Backend (Python FastAPI)  
> **Alembic Revision**: `0055_create_streak_table.py` (`head`)  
> **Test Pass Rate**: 49 passed in `tests/modules/habits/test_streak_state_machine.py`, 101 passed in `tests/modules/habits` (100% pass rate in 10.2s), 110 passed in habits + routing suites, 246 passed in architecture suite  
> **Thin Gateway Invariant**: 0 `ast.If` nodes in `src/noorheroes/modules/habits/api.py` (enforced by `tests/api/v1/test_routing.py`)

## 1. Feature Context
Part of Feature A.7 — Habit Tracker. The feature's most safety-critical logic: a deterministic, exhaustively-tested 6-state streak machine that must never skip states or produce an illegal transition (PRD FR-7).

## 2. Parent Feature
A.7 Habit Tracker — Backend (FastAPI)

## 3. Sub-feature
B-03 Streak State Machine Engine

## 4. Objective
Implement the canonical Streak Service as a pure state-transition function plus `GET /v1/habits/streaks/{child_id}`, encoding the exact state diagram from PRD §1.17 with zero approximation.

## 5. Business Requirements
- States: `inactive, active, at_risk, protected, broken, recovery` — exactly these six, no others (FR-7).
- Transitions exactly as diagrammed: `inactive→active` (activity); `active→active` (next eligible day); `active→at_risk` (day nearing end, no activity); `at_risk→active` (activity completes); `at_risk→protected` (shield available); `at_risk→broken` (day closes, no shield); `broken→recovery` (child returns/engages); `recovery→active` (recovery mission completed); `recovery→inactive` (recovery window expires).
- "Meaningful activity" = completed lesson, story past engagement threshold, quiz, or approved habit check-in — not low-value repeat taps (FR-8).
- Given identical input history, computed state must always be identical (deterministic/reproducible — NFR Reliability).
- Streak shield (`protected`) is earned through consistency, never purchasable (FR-11, hard anti-monetization rule).

## 6. Existing Architecture
- Extends the `habits` bounded context established in B-01/B-02.
- **Important distinction from existing code:** `src/noorheroes/core/security/streak.py` → `StreakCalculator` already exists and computes generic "active child learning streak days" for the `learning` context. This is a **different, simpler mechanism** (a day-counter) and is explicitly **not** the Habit Tracker streak engine — do not extend or repurpose `StreakCalculator` for this feature; it must remain untouched and continue serving `learning` context as-is. Build a new, separate `HabitStreakStateMachine` inside `habits/streak_service.py`. Cross-reference this distinction in code comments to prevent future confusion between the two streak concepts.
- Reuse `BaseService` pattern.

## 7. Existing Code to Reuse
- `HabitRepository`/`HabitLog` (from B-02) as the activity-source data
- `get_current_child` / `get_current_parent` dependencies

## 8. Files to Create
- `src/noorheroes/modules/habits/streak_state_machine.py` — pure function `compute_next_state(current_state, has_meaningful_activity_today, day_has_closed, shield_available) -> new_state`
- `src/noorheroes/modules/habits/streak_service.py` — `StreakService` orchestrating persistence + the pure function
- Extend `models.py`: `Streak` model
- `alembic/versions/<rev>_create_streak_table.py`
- Extend `schemas.py`: `StreakResponse`
- Extend `api.py`: `GET /v1/habits/streaks/{child_id}`
- `tests/modules/habits/test_streak_state_machine.py` (exhaustive transition table tests)

## 9. Files to Modify
- `src/noorheroes/modules/habits/service.py` — call `StreakService.recalculate()` after a successful check-in (completes the `# TODO(B-03)` hook left in B-02)

## 10. Backend Requirements
- `compute_next_state()` implemented as a **pure function** with no side effects, independently unit-testable against every cell of the transition table.
- A wrapping `StreakService.evaluate_and_persist()` reads current `Streak` row, gathers activity/day-closed/shield signals, calls the pure function, persists the new state.
- Illegal-transition-impossibility test: enumerate all `6 × 2 × 2 × 2 = 48` input combinations and assert only the documented transitions are reachable.
- Day-boundary/"day nearing end"/"day closes" signals sourced from B-04 (Timezone Authority) — this sub-feature depends on B-04 for the day-boundary determination but implements the state machine independently and testably with injected boundary signals (do not couple the pure function to timezone logic directly).

## 11. KMP Requirements
Not applicable directly; K-04 renders streak state, mirroring server state only (never independently computing transitions client-side).

## 12. NextJS Requirements
Not applicable directly.

## 13. API Contract

**Required API**
- **HTTP Method:** GET
- **Endpoint:** `/v1/habits/streaks/{child_id}`
- **Response 200:**
```json
{ "streak_type": "daily_overall", "current_count": 6, "best_count": 14, "state": "active", "history": [] }
```
- **Authentication:** Bearer, child-mode (own child) or parent-mode (own child)
- **Validation:** `child_id` ownership check
- **Error Responses:** `401`, `403`; on Streak Service degradation, return last-known cached state rather than an error (§18)

## 14. Database Requirements
- `streak`: `streak_id UUID PK`, `child_id UUID FK`, `streak_type VARCHAR`, `current_count INT`, `best_count INT`, `last_eligible_date DATE`, `state VARCHAR CHECK IN ('inactive','active','at_risk','protected','broken','recovery')`, `updated_at TIMESTAMPTZ`.
- Index `(child_id, streak_type)`.

## 15. Validation
- Exhaustive transition-table test suite is mandatory and must assert both: (a) every legal transition produces the documented result, and (b) no transition outside the documented table is reachable via the public API/service surface.

## 16. Authentication
Bearer JWT, child-mode or parent-mode session.

## 17. Authorization
Session must own the requested `child_id`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Streak Service unavailable | Return last-known cached streak display, no alarming error framing, never silently reset to zero |
| Impossible/unrecognized state in stored data | Log as a critical invariant-violation alert (cross-ref N-06 monitoring); do not crash the read path — surface last valid known state |

## 19. Offline First
N/A directly (backend); client mirrors last-synced state offline (K-04).

## 20. Local Data
N/A.

## 21. Localization
State labels (`active`, `at_risk`, etc.) are internal keys only — never surfaced as raw text to the client UI (enforced client-side in K-04); no localization needed at this layer.

## 22. RTL
N/A.

## 23. Analytics
`streak_state_changed` (with `from_state`, `to_state`, `streak_type`) emitted on every persisted transition; `streak_shield_applied` on `at_risk→protected`.

## 24. Performance
State evaluation is a lightweight in-memory pure function; persistence is a single-row upsert per child per evaluation.

## 25. Security
No monetization pathway may ever set `shield_available=true` from a purchase — this must be verified as a security-equivalent invariant, not just a product rule (FR-11).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2, pytest for exhaustive table-driven tests.

## 27. Testing
- Unit: exhaustive transition table (all legal + illegal-impossibility assertions).
- Integration: full check-in → streak recalculation → correct state persisted.
- Regression: staging "time-travel" utility (per PRD §10 DevOps) used to replay historical fixture data confirming no child's computed state regresses on deploy.

## 28. Documentation
Document the full transition table verbatim in code comments directly above `compute_next_state()`, referencing PRD §1.17 as the source of truth.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Pure State-Transition Function**
- Objective: `compute_next_state()` exactly encoding the PRD §1.17 diagram.
- Why Required: This is the feature's highest-priority correctness guarantee (PRD §5 backend prompt item 3).
- Existing Architecture to Follow: none directly reusable — this is genuinely new logic; keep it framework-free (pure Python) for maximal testability.
- Files to Create: `streak_state_machine.py`
- Business Rules: FR-7, FR-8.
- Tests: exhaustive 48-combination table test.
- Do Not Change: the transition table itself must not be altered without explicit product/architecture sign-off given its "most safety-critical" status.
- Definition of Done: function passes exhaustive test suite; no reachable illegal transition.

**Task 02 — Create Streak Model & Migration**
- Files to Create: `models.py` extension, `alembic/versions/<rev>_create_streak_table.py`
- Validation: CHECK constraint on `state` matching the six canonical values exactly.
- Definition of Done: table created, constraint enforced at DB layer.

**Task 03 — Implement StreakService Orchestration**
- Files to Create: `streak_service.py`
- Existing Files to Reuse: `HabitRepository` for activity lookups.
- Implementation Details: gather `has_meaningful_activity_today`, `day_has_closed`, `shield_available` signals; call pure function; persist.
- Business Rules: FR-8 meaningful-activity definition.
- Tests: unit tests mocking signal sources.
- Definition of Done: service correctly orchestrates the pure function against real data.

**Task 04 — Wire Streak Recalculation into Check-In Flow**
- Files to Modify: `src/noorheroes/modules/habits/service.py` (replace the `# TODO(B-03)` placeholder from B-02)
- Implementation Details: call `StreakService.evaluate_and_persist()` after successful check-in.
- Tests: integration test verifying streak updates after check-in.
- Definition of Done: check-in → streak update flow verified end-to-end.

**Task 05 — Implement GET Streak Endpoint**
- Files to Modify: `api.py`
- Authentication/Authorization: per §16/§17.
- Error Handling: cached-fallback behavior per §18.
- Tests: integration test.
- Definition of Done: endpoint live, documented, degraded-mode-safe.

**Task 06 — Add Illegal-Transition-Impossibility Test**
- Files to Create: `tests/modules/habits/test_streak_state_machine.py`
- Implementation Details: enumerate all input combinations; assert only documented outputs occur.
- Definition of Done: test suite exhaustive and passing.

**Task 07 — Add Monitoring Hook for Impossible Production States**
- Implementation Details: periodic canary/invariant check comparing stored `state` values against the legal state set (cross-ref N-06, PRD §10 DevOps alerting requirement).
- Definition of Done: alert wired for any impossible-state detection.

**Task 08 — Add Logging & Documentation**
- Documentation: transition table documented in-code; `FAST-API-INSTRUCTIONS.md` updated.
- Definition of Done: docs accurate.

**Task 09 — Final Code Review**
- Do Not Change: transition table, `StreakCalculator` (unrelated `learning`-context class).
- Expected Result: PR merge-ready with exhaustive tests green.

## 30. Definition of Done
- Pure state-transition function exactly matches PRD §1.17 with exhaustive test coverage.
- Streak recalculation correctly wired into the check-in flow.
- Degraded-mode behavior never silently resets state to zero.
- No confusion/coupling with the unrelated existing `StreakCalculator`.

## 31. Final Verification Checklist
- [x] All 9 documented transitions implemented exactly (Verified: `DOCUMENTED_TRANSITIONS` in `src/noorheroes/modules/habits/streak_state_machine.py`)
- [x] Exhaustive 48-combination test passes with illegal-transition-impossibility assertions (Verified: `test_exhaustive_48_combination_matrix` in `tests/modules/habits/test_streak_state_machine.py`)
- [x] `Streak` table CHECK constraint matches the six canonical states (Verified: `ck_streak_state` in `models.py` & `0055_create_streak_table.py`)
- [x] Check-in flow correctly triggers streak recalculation (Verified: `# TODO(B-03)` replaced with live call in `service.process_check_in()`)
- [x] Degraded-mode read returns cached state, never a silent zero-reset (Verified: 300s TTL Redis snapshot fallback in `StreakService.get_child_streak()`)
- [x] No monetization pathway can set `shield_available=true` (Verified: `TestStreakAntiMonetizationInvariants` asserts 0 monetization fields/methods)
- [x] Monitoring alert wired for impossible production states (Verified: `check_streak_state_invariants()` emits structured critical alerts)
- [x] `StreakCalculator` (unrelated existing class) left untouched (Verified: `src/noorheroes/core/security/streak.py` unmodified)

## 32. Implementation Artifacts & Verified Files
- **Pure State Machine Engine**:
  - `src/noorheroes/modules/habits/streak_state_machine.py`: `compute_next_state`, `check_streak_state_invariants`, `VALID_STATES`, `DOCUMENTED_TRANSITIONS`
- **Database Schema & Migration**:
  - `src/noorheroes/modules/habits/models.py`: `Streak` ORM model on table `streak` with `ck_streak_state` and `uq_streak_child_type`
  - `alembic/versions/0055_create_streak_table.py`: Reversible schema migration (current `head`)
- **Domain Services & Repositories**:
  - `src/noorheroes/modules/habits/repository.py`: `StreakRepository` (`get_by_child_and_type`, `upsert_streak`)
  - `src/noorheroes/modules/habits/streak_service.py`: `StreakService` (`evaluate_and_persist`, `recalculate`, `get_child_streak`)
  - `src/noorheroes/modules/habits/service.py`: Check-in flow wired with live streak recalculation and response population
- **API Gateway & Dependencies**:
  - `src/noorheroes/modules/habits/api.py`: `GET /v1/habits/streaks/{child_id}` with Thin Gateway architecture (0 `ast.If` nodes)
  - `src/noorheroes/modules/habits/deps.py`: `validate_streak_access`, `get_streak_repository`, `get_streak_service`, `get_current_parent_or_child`
  - `src/noorheroes/modules/habits/schemas.py`: `StreakResponse`, `StreakHistoryItem`, `STREAK_GET_RESPONSES`
- **Transactional Outbox Events**:
  - `src/noorheroes/modules/habits/events.py`: `StreakStateChanged`, `StreakShieldApplied`
  - `src/noorheroes/common/outbox_relay.py`: Registered in `DISPATCH_TABLE`
- **Testing & Verification**:
  - `tests/modules/habits/test_streak_state_machine.py`: 49 comprehensive tests (48 matrix permutations, 9 transitions, degraded mode, multi-day time-travel fixture replay, controller, TestClient HTTP, anti-monetization invariants)
  - Full habits test suite: 101/101 passed in 10.2s; habits + routing suite: 110/110 passed; architecture suite: 246/246 passed.
- **Documentation**:
  - `MASTER-README.md`: Section 11.51 updated
  - `FAST-API-INSTRUCTIONS.md`: Section 5.15, Section 6, and Section 9 (Scenario 32 & Scenario 33) updated
  - `walkthrough.md`: Comprehensive walkthrough and verification inventory updated
  - `NoorHeroes_Consolidated_Execution_Blueprint.md`: Row 233 and Section 0.5 summary updated
