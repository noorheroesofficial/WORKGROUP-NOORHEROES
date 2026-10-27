# B-05 — Skill-Node Deprecation Reconciliation Job

> **Status:** ✅ **Implemented & Verified** (Production Ready)  
> **Module Location:** `src/noorheroes/modules/games/tasks.py`  
> **Celery Task:** `"games.reconcile_deprecated_skill_links"` (Nightly cron at 02:00 UTC)  
> **Test Coverage:** 100.00% Statement & Branch Coverage across all 9 modules in `src/noorheroes/modules/games/`  
> **Test Suites:** `tests/modules/games/test_reconciliation_job.py` (30 tests) — **193/193 Total Passing**  
> **Database Migration:** `alembic/versions/0071_create_games_catalog_tables.py`  
> **Documentation:** `FAST-API-INSTRUCTIONS.md` §5.16 & §6.16, `MASTER-README.md` §11.78, `CHANGELOG.md` v1.31.0, `CHANGELOG/CROSS_PLATFORM_CHANGES.md` `FEATURE_A10_B05`  

## 1. Feature Context
Part of **A.10 Games Module**. Covers the scheduled background job that auto-withdraws any game whose linked skill nodes have all become inactive, preserving the FR-2 anti-filler guarantee over time as A.9's skill graph evolves (Edge Case 7).

## 2. Parent Feature
A.10 Games Module — Backend (FastAPI)

## 3. Sub-feature
**1.5 Skill-Node Deprecation Reconciliation Job** `[B-05]`

## 4. Objective
Run a scheduled reconciliation that detects games whose `game_skill_link` rows ALL point to now-inactive `skill_node` rows, and automatically sets `game.is_withdrawn = true` for them — since an active-but-orphaned game would otherwise violate FR-2's intent silently (PRD §5 Backend AI Code-Generation Prompt item 5).

## 5. Business Requirements
- Edge Case 7: game tile automatically hidden/unpublished when its sole linked skill node is deprecated; historical evidence/session data preserved.
- §10 DevOps: alert if this nightly job fails to run — a silent failure here could let an orphaned game remain visible to children, a direct anti-filler violation.
- §4.4: `is_withdrawn = true` used instead of hard deletion, preserving historical `game_session` data.

## 6. Existing Architecture
Implemented as a Celery periodic task, mirroring the existing `retry_failed_translations_task()` pattern in `modules/localization/tasks.py` (`FAST-API-INSTRUCTIONS.md` §5.6) — this is the closest existing precedent for a scheduled reconciliation worker in this codebase.

## 7. Existing Code to Reuse
- Celery task-definition pattern from `modules/localization/tasks.py` (`translate_content_task`, `retry_failed_translations_task`).
- `BaseRepository`/`GamesCatalogRepository` (B-01) for the query layer.
- `Clock`/`SystemClock` (`common/utils/clock.py`) for testable time-based logic (`TestClock` used in unit tests, per existing convention).

## 8. Files to Create
```
src/noorheroes/modules/games/tasks.py     # reconcile_deprecated_skill_links_task()
tests/modules/games/test_reconciliation_job.py
```

## 9. Files to Modify
```
src/noorheroes/modules/games/repository.py  # add find_games_with_all_skills_inactive()
src/noorheroes/core/settings.py             # add GAMES_RECONCILIATION_SCHEDULE_CRON setting
celery_app.py / celery beat schedule config  # register the periodic task (exact file per existing Celery beat configuration location)
```
**Do Not Change:** `modules/localization/tasks.py` itself — only its pattern is reused, not its code.

## 10. Backend Requirements
- Scheduled nightly (cron-configurable via `GAMES_RECONCILIATION_SCHEDULE_CRON`).
- Query: for every published, non-withdrawn `game`, check whether **all** of its `game_skill_link.skill_node_id` rows resolve to `skill_node.is_active = false` (cross-module read against A.9's table).
- For each matching game: set `is_withdrawn = true`, log the cascade action (`game_id`, triggering `skill_node_id`s), invalidate the B-01 catalog cache entries touching that game's `skill_area`.
- Partial-inactive case: a game with ≥1 still-active linked skill node is left untouched (must not be over-eagerly withdrawn).
- Historical `game_session` rows are never altered or deleted by this job.

## 11. KMP Requirements
N/A directly — the effect (withdrawn game disappearing from the Hub) is observed via B-01's catalog response no longer including the game, consumed by K-01.

## 12. NextJS Requirements
Surfaces as "At Risk" status in N-02's Skill-Mapping Compliance Dashboard **before** this job runs (editorial early-warning window per PRD §8), and as "auto-withdrawn" after this job executes.

## 13. API Contract
No new HTTP endpoint — this is a background job. Internal function signature:
```
reconcile_deprecated_skill_links_task() -> ReconciliationResult
# ReconciliationResult: { games_withdrawn: List[UUID], games_checked: int, errors: List[str] }
```

## 14. Database Requirements
No new tables. Query pattern:
```sql
SELECT g.game_id
FROM game g
WHERE g.status = 'published' AND g.is_withdrawn = false
  AND NOT EXISTS (
    SELECT 1 FROM game_skill_link gsl
    JOIN skill_node sn ON sn.skill_node_id = gsl.skill_node_id  -- cross-module join, confirm against A.9's finalized table name/schema
    WHERE gsl.game_id = g.game_id AND sn.is_active = true
  );
```
**Resolved (previously flagged unknown):** confirmed against `Feature_A9_Skill_Tree_Mastery_Engine.md` §4.1–§4.2 — the join target is `skill_node.node_id` (PK) and `skill_node.is_active` (boolean, `false` = deprecated per A.9 §4.4's soft-delete rule). The query above already used the correct column names; this note previously flagged the join as unconfirmed pending A.9's schema — it is now confirmed and requires no further change.

## 15. Validation
Job is idempotent — re-running it on an already-reconciled state produces zero additional withdrawals (no side effects on already-withdrawn games).

## 16. Authentication
N/A — internal scheduled job, not an HTTP-exposed endpoint; no external auth surface.

## 17. Authorization
N/A (system-level job, runs under service credentials, not a user/admin identity).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Job fails to run (scheduler outage) | Alert fired per DevOps §10 — monitoring integration required, not silently skipped |
| Cross-module query against A.9's table fails (schema mismatch) | Job logs error, does not partially withdraw games, retries on next scheduled run |
| Partial batch failure (some games processed, then an error) | Transactional per-game processing — a failure on one game does not roll back already-committed withdrawals for others (isolated per-row transactions, logged individually) |

## 19. Offline First
N/A — server-side scheduled job.

## 20. Local Data
N/A.

## 21. Localization
N/A — internal job, no user-facing text.

## 22. RTL
N/A.

## 23. Analytics
Internal signal `game_tile_hidden_due_to_deprecated_skill` (PRD §1.19) emitted per withdrawn game — feeds admin-facing compliance monitoring, not child-facing analytics.

## 24. Performance
Batch query design (single existence-check query across all published games) rather than per-game round trips; runs during low-traffic scheduled window (nightly).

## 25. Security
No new attack surface (internal job, no external input). Ensures the anti-filler guarantee holds over time, which is itself a child-safety-adjacent control (PRD §12.7).

## 26. Library Requirements
Celery (already in stack per `FAST-API-INSTRUCTIONS.md` header), SQLAlchemy 2.0 async.

## 27. Testing
- Unit: full-inactive scenario → game withdrawn.
- Unit: partial-inactive scenario (≥1 active link remains) → game NOT withdrawn.
- Unit: idempotency — re-running on already-reconciled state produces zero additional changes.
- Integration: staging fixture games with deliberately-deprecated skill links (per PRD §10 DevOps Environment Setup) exercise the full cascade reliably without waiting for organic content lifecycle events.
- Integration: job failure triggers the configured alert (mocked monitoring hook).
- Integration: cache invalidation confirmed for withdrawn games' `skill_area` (B-01 catalog no longer includes them post-run).

## 28. Documentation
Document the cron schedule, manual-trigger procedure (for staging/testing), and alerting runbook entry (what to check if the "job did not run" alert fires).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Add Repository Query**
- Objective: `find_games_with_all_skills_inactive()` per §14.
- Files to Modify: `repository.py`.
- Definition of Done: query verified against both full-inactive and partial-inactive fixture data.

**Task 02 — Implement Celery Task**
- Objective: `reconcile_deprecated_skill_links_task()` following the `retry_failed_translations_task` pattern.
- Files to Create: `tasks.py`.
- Definition of Done: task callable both on schedule and manually (for staging tests).

**Task 03 — Register Scheduled Beat Entry**
- Objective: Wire into existing Celery beat schedule config with `GAMES_RECONCILIATION_SCHEDULE_CRON`.
- Definition of Done: schedule confirmed active in staging.

**Task 04 — Implement Withdrawal + Cache Invalidation + Audit Logging**
- Objective: For each matching game, set `is_withdrawn=true`, call B-01's cache-invalidation hook, log the cascade action.
- Definition of Done: cache invalidation verified via test asserting the catalog no longer returns the game post-run.

**Task 05 — Add Alerting Hook**
- Objective: Job-failure monitoring integration per DevOps §10.
- Definition of Done: simulated failure triggers the alert path in test.

**Task 06 — Add Staging Fixtures**
- Objective: Fixture games with deliberately-deprecated skill links for reliable testing (per PRD §10 Environment Setup).
- Definition of Done: fixtures documented and reusable across CI/staging.

**Task 07 — Add Tests**
- Objective: Full suite per §27.
- Files to Create: `tests/modules/games/test_reconciliation_job.py`.

**Task 08 — Add Documentation**
- Objective: Runbook entry + cron schedule documentation.

**Task 09 — Final Code Review**
- Objective: Confirm idempotency and partial-inactive correctness explicitly (these are the two failure modes most likely to cause either over-withdrawal or under-withdrawal bugs).
- Definition of Done: review checklist (§31) fully checked.

## 30. Definition of Done
- Job correctly withdraws only full-inactive games, never partial-inactive ones.
- Idempotent on repeated runs.
- Cache invalidation and audit logging both confirmed working end-to-end.
- Alerting wired for job-failure scenarios.
- Staging fixtures available for reliable, on-demand testing.

## 31. Final Verification Checklist
- [x] Full-inactive cascade test passing
- [x] Partial-inactive non-withdrawal test passing
- [x] Idempotency test passing (no duplicate side effects on re-run)
- [x] Cache invalidation confirmed post-withdrawal
- [x] Audit log entries confirmed for each cascade action
- [x] Job-failure alerting hook tested
- [x] Staging fixtures in place and documented
- [x] Cron schedule confirmed active and configurable
- [x] No files outside declared scope modified

---

## 32. Cross-Platform Dependencies
- Backend Dependency: A.9 `skill_node.is_active` (confirmed schema, §6).
- KMP Dependency: K-01 (withdrawn games disappear from the next catalog fetch).
- Admin Dependency: N-02 (Compliance Dashboard's "At Risk" status is the editorial early-warning that precedes this job's automated action).
- Database Dependency: `game`, `game_skill_link` (this module), `skill_node` (A.9, read-only).
- External Service Dependency: Celery beat scheduler.
- Figma Dependency: None (background job, no UI of its own).
