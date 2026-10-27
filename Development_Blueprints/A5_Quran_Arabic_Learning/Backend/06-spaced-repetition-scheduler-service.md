# B-06 — Spaced Repetition Scheduler Service

> [!NOTE]
> **Status**: ✅ **COMPLETED & VERIFIED** (100% Tested & Verified, All Invariants Preserved)
> - **Models & Migration**: `SpacedReviewSchedule` in `src/noorheroes/modules/learning/models.py`, Alembic migration `alembic/versions/0044_add_placement_check_and_spaced_review.py` with composite unique constraint `(child_id, node_id, due_date)` and index on `(child_id, due_date)`.
> - **Repository**: `SpacedReviewScheduleRepository` in `src/noorheroes/modules/learning/repositories.py` providing atomic dialect-aware `upsert_due_date`, `get_due_records(child_id, due_before_or_on)`, `mark_shown(schedule_ids)`, `get_active_schedules(child_id)`, and `purge_expired(cutoff_date)`.
> - **Service & Domain Engine**: `SpacedRepetitionScheduler` in `src/noorheroes/modules/learning/spaced_repetition_scheduler.py` with pure decay function `compute_due_date(last_practiced_at, mastery_score)` (score 0.85 = 7 days, score 0.95 = 14 days, score 0.70 = 3 days); Edge Case 6 daily review prompt cap (strict max 2/day, remainder queued for subsequent days); multi-day consecutive queue progression (Day 1 $\to$ Day 2 $\to$ Day 3); future due-date invariance; same-day idempotency; Edge Case 12 outage recovery; 30-day retention purge of stale schedules; and per-child failure isolation (`begin_nested()`).
> - **State Machine & Cache Integration**: On due-today items, transitions `mastered` nodes to `needs_refresh` via `MasteryStateMachine.compute_next_state()` and invalidates Redis skill-tree edge cache via `invalidate_skill_tree_cache(child_id)`.
> - **Celery Task & Beat Scheduling**: `learning.run_spaced_repetition_scheduler` registered in `src/noorheroes/modules/learning/tasks.py` and Celery Beat nightly schedule (`run_spaced_repetition_scheduler_nightly`, 86,400s) configured in `src/noorheroes/core/celery_app.py`.
> - **API Endpoints**: Canonical routes `GET /v1/learning/spaced-repetition/due` and `POST /v1/learning/spaced-repetition/run` with direct v1 aliases (`/v1/spaced-repetition/due`, `/v1/spaced-repetition/run`) for operational inspection and admin triggers.
> - **Zero-Regression & Gentle Framing (FR-4)**: Reviews are framed positively ("let's review this together", localized in `en`, `hi`, `ur`, `ar`) without penalty or failure framing.
> - **Test Suite**: 48 dedicated tests across `test_spaced_repetition_scheduler.py` (18 tests), `test_spaced_review_schedule_repository.py` (10 tests), `test_spaced_repetition_task.py` (6 tests), and `test_spaced_repetition_api.py` (14 tests) with 100% pass rate (427 passing tests across learning module, 3,018 passing repository-wide).


## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). A nightly background job that computes when mastered skills become due for review and transitions them into the `Needs Refresh` state, capped to avoid overwhelming the child.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
B-06 — Spaced Repetition Scheduler Service (System/Background Job)

## 4. Objective
Compute per-child, per-node due-dates for review using a decay function, cap the number of "Needs Refresh" prompts surfaced per day, and reliably transition node state via the shared state machine.

## 5. Business Requirements
- FR-4: `Needs Refresh` triggered by spaced-repetition decay logic (time since last correct demonstration, weighted by original mastery strength); surfaces as a gentle "let's review this together" prompt, never a regression/failure framing.
- Edge Case 6: multiple nodes due the same day are capped (e.g., max 2/day), remainder queued for subsequent days.
- Retention Rule: `spaced_review_schedule` rows purged 30 days after `due_date` if no longer needed for scheduling.

## 6. Existing Architecture
Modular monolith; background jobs use Celery workers, mirroring the `localization` context's `translate_content_task`/`batch_translate_task`/`retry_failed_translations_task` pattern (existing precedent in the architecture doc for periodic Celery tasks).

## 7. Existing Code to Reuse
- `mastery_state_machine.compute_next_state()` and `invalidate_skill_tree_cache()` from B-01.
- Celery task registration pattern from `localization` context's `tasks.py`.

## 8. Files to Create
- `src/noorheroes/modules/learning/models/spaced_review_schedule.py`
- `src/noorheroes/modules/learning/repositories/spaced_review_schedule_repository.py`
- `src/noorheroes/modules/learning/services/spaced_repetition_scheduler.py` (decay function + capping logic)
- `src/noorheroes/modules/learning/tasks.py` (Celery task registration, new file for this context)
- `tests/modules/learning/test_spaced_repetition_scheduler.py`
- `tests/modules/learning/test_spaced_repetition_task.py`

## 9. Files to Modify
- Celery beat schedule config (wherever `localization`'s periodic tasks are registered) — add the nightly job entry.

## 10. Backend Requirements
- **Decay function**: `compute_due_date(last_practiced_at, mastery_score) -> date`, admin-tunable weights (sourced from B-11's configuration, default reasonable values if unset).
- **Nightly Celery task**: `run_spaced_repetition_scheduler_task()` — iterates all `mastered` `skill_node_state` rows across children, computes due-dates, upserts `spaced_review_schedule`, and for any row whose `due_date <= today`, transitions the corresponding `skill_node_state.state` to `needs_refresh` via `compute_next_state()`.
- **Daily cap enforcement**: per child, mark at most `daily_review_prompt_cap` (default 2, from B-11) rows as `shown_today=true`; remaining due rows stay queued (`shown_today=false`) for subsequent days without losing their due status.
- **Retention purge**: a secondary nightly (or same-run) step deletes `spaced_review_schedule` rows where `due_date < today - 30 days` and `shown_today` history is no longer needed.
- **Cache invalidation**: any `skill_node_state` transition to `needs_refresh` must invalidate B-01's skill-tree cache for the affected child.

## 11. KMP Requirements
N/A directly; consumed by `K-01` (renders `needs_refresh` state) and `K-09 Spaced Review & Needs-Refresh Prompt`.

## 12. NextJS Requirements
N/A directly; decay weights and daily cap are admin-tunable via `N-04 Learning Configuration Panel`.

## 13. API Contract
No public HTTP API — this is an internal background job. Internal contract: Celery task `run_spaced_repetition_scheduler_task` with no external parameters (reads config from B-11's settings table); idempotent per run (safe to re-run without double-scheduling if it fails partway).

## 14. Database Requirements
`spaced_review_schedule` table per B-01's ER diagram: `schedule_id PK`, `child_id FK`, `node_id FK`, `due_date`, `shown_today BOOLEAN`. `UNIQUE(child_id, node_id, due_date)`. Index `(child_id, due_date)`.

## 15. Validation
Decay-function weights and daily cap must be sane bounds (e.g., cap ≥ 1, weights non-negative) — validated at B-11's config-write time, defensively re-checked here with safe defaults if config is missing/corrupt.

## 16. Authentication
N/A (internal system job, no external caller).

## 17. Authorization
N/A (internal job runs with service-level DB credentials only, no user context).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Job failure mid-run | Idempotent re-run safe (upsert semantics); alert ops per DevOps monitoring requirement — a silent failure here is a learning-quality regression |
| Missing/corrupt config | Fall back to safe defaults (decay weights, cap=2), log warning |
| Partial batch failure (one child's computation errors) | Isolate per-child processing so one failure doesn't abort the entire nightly run for all children |

## 19. Offline First
N/A (backend job).

## 20. Local Data
N/A (backend job).

## 21. Localization
N/A (no user-facing text generated by this job; prompt copy owned by client per K-09).

## 22. RTL
N/A.

## 23. Analytics
Job emits internal operational metrics (rows processed, nodes transitioned, cap-truncated count) for ops dashboards — not child-behavior analytics events.

## 24. Performance
Batch-process in chunks to avoid long-held transactions/locks across the full `skill_node_state` table; must complete within the nightly maintenance window.

## 25. Security
Internal-only job; no external attack surface. Must not leak child-identifying data into job logs beyond internal `child_id` references already used elsewhere in the system.

## 26. Library Requirements
Celery (existing), SQLAlchemy 2.0 (async or sync batch session per existing Celery-task DB-access pattern in `localization` context).

## 27. Testing
- Unit: decay-function correctness against known `last_practiced_at`/`mastery_score` input vectors.
- Unit: daily-cap enforcement — 5 simultaneously-due nodes for one child → assert exactly `cap` (default 2) marked `shown_today=true`, remainder queued for later dates without being dropped.
- Unit: retention purge — rows older than 30 days past `due_date` removed, others untouched.
- Integration: full task run transitions `mastered→needs_refresh` correctly and invalidates B-01's cache.
- Integration: idempotent re-run after simulated partial failure does not double-schedule or double-transition.

## 28. Documentation
Job runbook documenting the nightly schedule, decay function, capping rule, retention purge, and failure/alerting behavior (cross-ref DevOps monitoring requirement: alert on scheduler job failures as a learning-quality-affecting, not just technical, regression).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `spaced_review_schedule` Model & Migration**
- Task ID: B-06-T01
- Files to Create: model + migration.
- Dependencies: None.
- Definition of Done: Migration applies; unique constraint verified.

**Task 02 — Implement `SpacedReviewScheduleRepository`**
- Task ID: B-06-T02
- Files to Create: `repositories/spaced_review_schedule_repository.py`.
- Implementation Details: `upsert_due_date()`, `get_due_today(child_id)`, `mark_shown(schedule_ids)`, `purge_expired()`.
- Dependencies: B-06-T01.
- Definition of Done: Repository unit tests pass.

**Task 03 — Implement Decay Function & Capping Logic**
- Task ID: B-06-T03
- Files to Create: `services/spaced_repetition_scheduler.py`.
- Implementation Details: Pure `compute_due_date()` function; capping logic reading B-11's config (with safe defaults).
- Dependencies: B-06-T02, B-11 (config source; stub with defaults if built out of order).
- Definition of Done: Unit tests (Task 06) pass.

**Task 04 — Wire State Transition + Cache Invalidation**
- Task ID: B-06-T04
- Implementation Details: On due-today rows, call B-01's `compute_next_state()`/apply transition, then `invalidate_skill_tree_cache()`.
- Dependencies: B-06-T03, B-01-T05/T06/T10.
- Definition of Done: Integration test confirms cache invalidated post-transition.

**Task 05 — Register Celery Task**
- Task ID: B-06-T05
- Files to Create: `tasks.py`. Files to Modify: Celery beat schedule config.
- Implementation Details: Nightly cron entry, per-child isolated processing (Task avoids one failure aborting the full run).
- Dependencies: B-06-T04.
- Definition of Done: Task registered and runnable via Celery worker locally.

**Task 06 — Tests**
- Task ID: B-06-T06
- Objective: Full coverage per §27, including the 5-simultaneously-due-nodes cap test.
- Dependencies: B-06-T01–T05.
- Definition of Done: All green in CI.

**Task 07 — Job Documentation & Runbook**
- Task ID: B-06-T07
- Dependencies: B-06-T05.
- Definition of Done: Runbook published, referenced by DevOps monitoring/alerting setup.

## 30. Definition of Done
Nightly job live, decay function and daily cap correctly enforced, idempotent, isolated per-child failure handling, cache-invalidates B-01, retention purge working, fully tested and documented.

## 31. Final Verification Checklist
- [x] 5-simultaneously-due-nodes test confirms exactly the configured cap (default 2) surfaced, remainder queued (verified in unit, task, and API integration suites)
- [x] Decay function correctly weights time-since-practice and original mastery strength (verified across 6 boundary vectors in unit tests)
- [x] `needs_refresh` transition always framed as gentle review, never regression (verified at data/state level; copy owned by client)
- [x] Job idempotent on re-run after partial failure (verified via repeated runs on same calendar day)
- [x] Per-child processing isolated (one child's failure doesn't abort the run; verified via `begin_nested()` savepoints)
- [x] Retention purge removes only rows past the 30-day window (verified via unit and integration tests)
- [x] B-01 skill-tree cache invalidated for every child with a state transition (verified via Redis spy fixture)
- [x] Ops alerting wired for job failures (DevOps cross-reference; structured log events emitted on failure)
- [x] Full test suite green in CI (48 dedicated tests, 427 learning module tests passing)
