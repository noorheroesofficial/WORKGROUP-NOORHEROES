# B-07 — Cross-Domain Spaced Repetition Scheduler

> **Status:** ✅ **COMPLETED & VERIFIED (100% Green in Test Suite & CI)**  
> **Platform:** Backend (FastAPI / SQLAlchemy 2.0 / PostgreSQL / Redis / Celery)  
> **Bounded Context:** `src/noorheroes/modules/learning/` (Learning Context)  
> **Endpoints Delivered:** `POST /v1/mastery/review-due`, `POST /v1/learning/mastery/review-due` (Canonical & Module Alias)  
> **Schemas Delivered:** `DueSkillItem`, `DueSkillResponse` in `src/noorheroes/modules/learning/schemas/spaced_review.py`  
> **Service Layer:** `SpacedRepetitionScheduler.run_scheduler()`, `get_due_reviews_for_child()`, `purge_expired_schedules()` with cross-domain global capping, outage recovery, and per-child savepoint isolation  
> **Background Job / Celery Task:** `learning.run_spaced_repetition_scheduler` registered in `src/noorheroes/modules/learning/tasks.py` with periodic Celery Beat schedule (`run_spaced_repetition_scheduler_nightly`)  
> **Child-Safety Invariant (FR-3):** Strict structural continuous score/confidence omission enforced via mandatory CI reflection gate (`test_no_raw_score_schema_introspection.py`)  
> **Test Coverage:** 100% Green across 84 dedicated spaced repetition tests (`test_cross_domain_daily_cap.py` [10], `test_scheduler_outage_recovery.py` [7], `test_no_raw_score_schema_introspection.py` [5], `test_spaced_repetition_scheduler.py` [22], `test_spaced_repetition_task.py` [14], `test_spaced_repetition_api.py` [26]), and 1,036 total learning context tests.

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). Generalizes A.5's existing per-domain nightly Celery scheduler (`06-spaced-repetition-scheduler-service.md`, `run_spaced_repetition_scheduler_task`) into a cross-domain service with a single globally-coordinated daily review-prompt cap.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
B-07 — Cross-Domain Spaced Repetition Scheduler (Internal/System — Background Job + User API)

## 4. Objective
Extend the existing decay-based `due_date` computation and Celery nightly job so the daily review-prompt cap (default 2) applies across ALL domains combined for a child, not per-domain, while preserving A.5's existing decay function and retention-purge behavior unchanged.

## 5. Business Requirements
- FR-8: `next_review_at` computed per `(child_id, skill_id)` via decay over time-since-`last_evidence_at`, weighted by mastery strength, with the same daily-prompt cap (default 2) generalized to cross-domain.
- Edge Case 4: multiple skills due simultaneously across different domains on the same day → the platform-wide cap applies globally, not per-domain (a child should not see 2 Quran + 2 Arabic on the same day if the cap is meant to be a total daily limit).
- Edge Case 12: a `next_review_at` that has already passed by the time the scheduler runs (e.g., outage) must still be correctly queued on the next successful run, not skipped.
- Retention Rule: `spaced_review_schedule` rows purged 30 days after `due_date` once no longer needed.

## 6. Existing Architecture
Modular monolith; background jobs use Celery workers, mirroring the `localization` context's periodic-task pattern (`translate_content_task`, `batch_translate_task`, `retry_failed_translations_task`). A.5's Backend B-06 already built `services/spaced_repetition_scheduler.py`, `models/spaced_review_schedule.py`, `repositories/spaced_review_schedule_repository.py`, and `tasks.py` registering `run_spaced_repetition_scheduler_task`, all currently scoped implicitly to Quran/Arabic/Tajweed via `skill_node.track` (pre-B-01-generalization).

## 7. Existing Code to Reuse
- A.5's `services/spaced_repetition_scheduler.py` — extend the cap-enforcement logic, do not fork a parallel scheduler.
- A.5's `models/spaced_review_schedule.py`, `repositories/spaced_review_schedule_repository.py` — schema unchanged, already cross-domain-capable (table has no `domain` column of its own, joins to `skill_node.domain` via `node_id`).
- A.5's `tasks.py` Celery registration pattern.
- B-03's `compute_next_state()` for the `mastered → needs_refresh` transition.
- B-01's `SkillDomainService` (to confirm the cap query genuinely spans all registered domains, not a hardcoded list).

## 8. Files to Create
- `tests/modules/learning/test_cross_domain_daily_cap.py`
- `tests/modules/learning/test_scheduler_outage_recovery.py`
- `src/noorheroes/modules/learning/schemas/spaced_review.py` — `DueSkillResponse` for the `POST /v1/mastery/review-due` endpoint.

## 9. Files to Modify
- `src/noorheroes/modules/learning/services/spaced_repetition_scheduler.py` — change the daily-cap query from per-domain to a single cross-domain query against `spaced_review_schedule` joined to `skill_node` (any domain), ordered/capped globally.
- `src/noorheroes/modules/learning/tasks.py` — confirm `run_spaced_repetition_scheduler_task` iterates `mastered` `skill_node_state` rows across ALL domains (post B-01 generalization, this should already be true structurally since the query no longer filters by `track`; verify and add a regression test).
- `src/noorheroes/modules/learning/api.py` — add `POST /v1/mastery/review-due?child_id=` route.

## 10. Backend Requirements
- **Decay function (unchanged from A.5):** `compute_due_date(last_practiced_at, mastery_score) -> date`, admin-tunable weights sourced from B-11's configuration, safe defaults if unset.
- **Nightly Celery task (generalized):** iterates all `mastered` `skill_node_state` rows across children AND across every registered domain (via B-01's registry, not a hardcoded enum), computes due-dates, upserts `spaced_review_schedule`, transitions `state → needs_refresh` via B-03's `compute_next_state()` for any row whose `due_date <= today`.
- **Global cross-domain cap enforcement:** per child, mark at most `daily_review_prompt_cap` (default 2, from B-11) rows as `shown_today=true` **across the combined set of due rows spanning all domains** — remaining due rows stay queued (`shown_today=false`) for subsequent days without losing due status. This is the single highest-priority behavioral change in this sub-feature.
- **Outage recovery (Edge Case 12):** overdue reviews (`due_date` in the past when the job finally runs) are still correctly queued/capped on the next successful run, never silently dropped.
- **Retention purge:** secondary nightly step deletes `spaced_review_schedule` rows where `due_date < today - 30 days`.
- **Cache invalidation:** any transition to `needs_refresh` invalidates B-05's skill-tree cache for the affected child.
- **`POST /v1/mastery/review-due?child_id=`:** returns the capped `due_skills` list for immediate client consumption (distinct from the nightly batch job — this is the synchronous read the client calls, e.g., on app open).

## 11. KMP Requirements
Consumed by A.5's `K-01` (renders `needs_refresh` state via K-03's renderer) and `K-09 Spaced Review & Needs-Refresh Prompt`; this sub-feature's cross-domain cap directly determines how many refresh prompts a child sees per day across the entire app, not per learning tab.

## 12. NextJS Requirements
Decay weights and the global daily cap are admin-tunable via N-03 (Cross-Domain Spaced Repetition Configuration), replacing any per-domain config surface A.5 may have exposed.

## 13. API Contract

**`POST /v1/mastery/review-due?child_id={uuid}`**
- **Auth:** Bearer (child-mode)
- **Response 200:**
```json
{
  "due_skills": [
    { "skill_node_id": "uuid", "domain": "quran" }
  ]
}
```
- **Business Logic:** Capped at the global daily limit (default 2) **across all domains combined**, computed centrally.
- **Error Responses:** `401`/`403` per standard child-session pattern, `500` on DB failure.

No public HTTP contract for the nightly Celery task itself (internal, no external parameters, reads config from B-11).

## 14. Database Requirements
`spaced_review_schedule` per A.9 PRD §4.2: `schedule_id PK`, `child_id FK`, `node_id FK`, `due_date`, `shown_today BOOLEAN`. `UNIQUE(child_id, node_id, due_date)`. Index `(child_id, due_date)`. Schema unchanged from A.5 — **the daily-cap query spans this single table regardless of `node_id`'s domain**, which is the entire point: no per-domain partitioning of this table.

## 15. Validation
Decay-function weights and daily cap validated as sane bounds (cap ≥ 1, weights non-negative) at B-11's config-write time; defensively re-checked here with safe defaults if config is missing/corrupt.

## 16. Authentication
`POST /v1/mastery/review-due` uses Bearer (child-mode) via `get_current_child`. The nightly Celery task has no external auth surface (internal job).

## 17. Authorization
`child_id` in the review-due request must match/be scoped to the authenticated session's family.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Spaced Repetition Scheduler batch job failure | No reviews lost — overdue reviews queue correctly on next successful run (Edge Case 12), capped per the standing daily limit |
| Cap computed per-domain by mistake (regression) | Caught by the mandatory cross-domain cap test (§27); this is the single highest-priority regression risk in this sub-feature |
| Missing/corrupt B-11 config | Falls back to documented safe defaults (cap=2, standard decay weights), logs a warning |
| `child_id` not in caller's family | `403` |

## 19. Offline First
N/A (backend). Client-side `needs_refresh` display uses cached last-synced state per K-01/K-03.

## 20. Local Data
N/A (backend).

## 21. Localization
N/A (backend; refresh-prompt copy owned client-side, localized there — "let's review this together" framing per FR-8, never a failure/regression tone).

## 22. RTL
N/A (backend).

## 23. Analytics
`spaced_review_due_cross_domain_capped` (internal, Edge Case 4 signal) — fired whenever the global cap actually truncates the due-skills list, distinguishing "cap engaged" from "nothing was due beyond the cap anyway."

## 24. Performance
Nightly batch job must complete within its scheduled window even as the child base and domain count grow — cross-domain query must be properly indexed (`(child_id, due_date)` already covers this); the cap-enforcement step should be a single ranked/limited query per child, not N per-domain queries merged in application code (which would reintroduce the per-domain-cap bug this sub-feature exists to fix).

## 25. Security
No new attack surface. `POST /v1/mastery/review-due` is child-session-scoped like other mastery read endpoints.

## 26. Library Requirements
No new libraries; existing Celery/Celery-beat stack.

## 27. Testing
- **Mandatory CI gate (highest priority, per A.9 PRD §10):** 3 due Quran skills + 2 due Arabic skills simultaneously → exactly 2 TOTAL returned as due today, not 4, with the remainder correctly queued for subsequent days regardless of domain (Backend AI Prompt item 5).
- Outage-recovery test: simulate a missed scheduler run, confirm overdue reviews are queued (not skipped) on the next successful run, still respecting the cap.
- Unit: decay function, retention-purge logic.
- Integration: full nightly-task run against a multi-domain, multi-child fixture dataset.

## 28. Documentation
Update the scheduler's docstring/runbook to explicitly state the cap is GLOBAL/cross-domain, replacing any prior per-domain-cap documentation inherited from A.5.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Refactor Cap-Enforcement Query to Cross-Domain** — ✅ **COMPLETED & VERIFIED**
- Task ID: B-07-T01
- Objective: Change the daily-cap computation from (implicitly) per-domain to explicitly cross-domain.
- Why This Is Required: This is the core generalization this sub-feature exists to deliver; Edge Case 4 is explicit about the risk of a naive per-domain implementation.
- Existing Architecture to Follow: A.5's existing `spaced_repetition_scheduler.py` structure.
- Existing Files to Reuse: Same file, extended.
- Files to Create: None.
- Files to Modify: `services/spaced_repetition_scheduler.py`.
- Implementation Details: Single query per child selecting due `spaced_review_schedule` rows (joined to `skill_node` for domain metadata only, not for filtering/partitioning), ordered by priority (e.g., due-date recency or mastery-decay severity), `LIMIT daily_review_prompt_cap`, marking those `shown_today=true`.
- Business Rules: Cap is a single number applied once per child per day, full stop.
- Validation: N/A. Error Handling: Per §18.
- Security: N/A. Performance: Single ranked query, not N per-domain queries merged app-side.
- Localization: N/A. RTL: N/A.
- Analytics: `spaced_review_due_cross_domain_capped` fired when truncation occurs.
- Tests: `test_cross_domain_daily_cap.py` — the 3-Quran + 2-Arabic → 2-total scenario.
- Documentation: Docstring updated.
- Dependencies: B-01 (domain-agnostic `skill_node`), B-03.
- Do Not Change: Decay function itself (`compute_due_date`), retention-purge logic.
- Expected Result: Cap correctly spans all domains.
- Definition of Done: Mandatory CI gate test green.

**Task 02 — Outage-Recovery Verification** — ✅ **COMPLETED & VERIFIED**
- Task ID: B-07-T02
- Objective: Confirm overdue reviews aren't lost across a missed scheduler run.
- Why This Is Required: Edge Case 12.
- Existing Architecture to Follow: Existing task-idempotency assumptions from A.5.
- Existing Files to Reuse: `tasks.py`.
- Files to Create: `tests/modules/learning/test_scheduler_outage_recovery.py`.
- Files to Modify: `tasks.py` only if a gap is found (e.g., if the task currently only looks at "due today" rather than "due on or before today").
- Implementation Details: Simulate a `due_date` in the past relative to "now" at job-run time; assert it's still correctly included in the next run's due-set and subject to the cap.
- Business Rules: Never silently drop overdue reviews.
- Validation/Error Handling/Security/Performance/Localization/RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the test.
- Documentation: Note in task docstring.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Verified outage-safe behavior.
- Definition of Done: Test green.

**Task 03 — Implement POST /v1/mastery/review-due Endpoint** — ✅ **COMPLETED & VERIFIED**
- Task ID: B-07-T03
- Objective: Synchronous client-facing read of the capped due-skills list.
- Why This Is Required: Client (K-09 in A.5) needs an on-demand read, not just the nightly batch job's side effects.
- Existing Architecture to Follow: Router → Service → Repository.
- Existing Files to Reuse: `get_current_child`.
- Files to Create: `schemas/spaced_review.py`.
- Files to Modify: `api.py`.
- Implementation Details: Reads the already-capped `spaced_review_schedule` rows for the child (does not recompute the cap on every call — reads the nightly job's `shown_today` output).
- Business Rules: Reflects the same cap already enforced nightly; does not double-apply or bypass it.
- Validation: `child_id` ownership. Error Handling: Per §18.
- Security: Child-session scoped. Performance: Simple indexed read.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: Part of `test_cross_domain_daily_cap.py` integration coverage.
- Documentation: OpenAPI schema.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working endpoint.
- Definition of Done: Integration test green.

## 30. Definition of Done
Cross-domain daily review-prompt cap correctly enforced as a single global limit per child; outage-recovery verified; `POST /v1/mastery/review-due` live; A.5's existing decay function and retention-purge behavior unchanged.

## 31. Final Verification Checklist
- [x] Cross-domain cap test passing (2 total, not 4, across mixed-domain due skills) — mandatory CI gate
- [x] Outage-recovery test passing
- [x] Retention purge unchanged/still functioning
- [x] Cache invalidation on `needs_refresh` transition verified
- [x] `POST /v1/mastery/review-due` returns correctly capped results
- [x] Nightly task iterates all registered domains via B-01's registry, no hardcoded domain list
- [x] Documentation updated to state the cap is explicitly global/cross-domain

## 32. Verification Evidence & Test Results
- **Dedicated B-07 Suite (`test_cross_domain_daily_cap.py`, `test_scheduler_outage_recovery.py`, `test_spaced_repetition_scheduler.py`, `test_spaced_repetition_task.py`, `test_spaced_repetition_api.py`)**: 79 passed in 5.8s (100% green).
- **Mandatory FR-3 CI Gate (`test_no_raw_score_schema_introspection.py`)**: 5 passed in 2.7s (verifying Pydantic model fields, camelCase/snake_case wire contracts, and OpenAPI specification components contain zero raw score or confidence disclosures).
- **Sub-feature B-07 Test Total**: 84 passed in 8.50s (100% green).
- **Full Learning Bounded Context Suite (`tests/modules/learning/`)**: 1,036 passed in 53.40s (100% green, 0 regressions across B-01 through B-07).
- **Backend Test Suite Total**: 4,930 passed across 342 test files with zero failures and zero regressions.

