# B-06 — License & Entitlement Periodic Refresh Job

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). The scheduled job that keeps offline access time-bounded — the mechanism enforcing FR-5's guarantee that withdrawn/de-entitled content becomes unavailable after the next refresh, without ever deleting the child's download record outright.

## 2. Parent Feature
B.15 — Offline Downloads & Sync

## 3. Sub-feature
B-06 — License & Entitlement Periodic Refresh Job

## 4. Objective
Implement a Celery periodic task that re-validates entitlement for every `status='complete'` `download_record`, transitioning to `status='license_expired'` when no longer valid, and flags (without deleting) records referencing withdrawn content — never leaving offline access indefinitely valid past a revocation.

## 5. Business Requirements
- FR-2 item 6: refresh entitlement periodically — offline access is time-bounded, not indefinite.
- FR-5: withdrawn content becomes unavailable after the next policy/entitlement refresh, while safe progress history is preserved.
- FR-7: license-expired downloads show a clear re-download prompt instead of silently failing — this job is what sets the state K-04 reacts to.
- §5 Backend AI Prompt item 6: scheduled job re-validates entitlement for every `complete` record, setting `license_expired` if no longer valid; simulated revocation test confirms correct transition without deletion.
- §12.7 Child Safety: withdrawn-content-becomes-unavailable-on-refresh ensures offline access can't become a permanent loophole around a safety-driven withdrawal.

## 6. Existing Architecture
Celery periodic task within the `downloads` bounded context (`src/noorheroes/modules/downloads/tasks.py`, alongside B-05's pruning task), following the exact pattern already established by `localization/tasks.py`'s `retry_failed_translations_task()` — no new job-scheduling infrastructure introduced.

## 7. Existing Code to Reuse
- Existing Celery infrastructure and beat-schedule configuration (`localization` module's established precedent).
- `subscriptions` module's `SubscriptionService.get_entitlement()` for the actual revalidation check.
- `content` module's withdrawal-status lookup for the withdrawn-content flagging path.
- `common/utils/clock.py` → `Clock` for consistent `license_expires_at` comparison.
- B-05's `SyncEventLogRepository`-adjacent pattern (batched processing) applied here as batched `download_record` scanning.

## 8. Files to Create
- `tests/modules/downloads/test_license_refresh_job.py`.
- `tests/modules/downloads/test_withdrawn_content_flagging.py`.

## 9. Files to Modify
- `modules/downloads/tasks.py` (B-05) — add `refresh_download_entitlements_task()`.
- `modules/downloads/repository.py` — add `list_complete_downloads_batch(cursor, limit)`, `mark_license_expired()`, `flag_withdrawn()`.
- Celery beat schedule config — register the new task (e.g., every 6–24 hours, per DevOps staging-injection requirement).

## 10. Backend Requirements
- Batched scan of all `status='complete'` `download_record` rows (keyset-paginated, never a single unbounded `SELECT *`).
- For each row, call `SubscriptionService.get_entitlement()`/`ContentService` to re-check entitlement validity for `(child_id, content_id)`.
- If no longer entitled or past `license_expires_at`: `UPDATE status = 'license_expired'` — never `DELETE`.
- If content is withdrawn (per `content` module's flag): set a `withdrawn` flag on the record (additive column, not a status-enum value, so it composes with `complete`/`license_expired`) — record remains visible in the child's list per FR-5, but excluded from any "recommend re-download" surfacing.
- Job is idempotent — re-running it mid-run or immediately after completion produces no additional side effects beyond the correct terminal state.
- Job failure on one row (e.g., transient entitlement-service timeout) does not abort the whole batch — logged and retried on the next scheduled run.

## 11. KMP Requirements
No direct KMP consumer — the resulting `status='license_expired'` is surfaced to K-04 via B-02's `GET /v1/children/{id}/downloads` on next fetch.

## 12. NextJS Requirements
No direct NextJS consumer — job run success/failure/duration feeds B-07's operational metrics.

## 13. API Contract
No public HTTP endpoint — scheduled Celery task only:
```python
@celery_app.task
async def refresh_download_entitlements_task() -> None: ...
```

## 14. Database Requirements
Reads/writes `download_record` (B-01) — `UPDATE` only (`status`, `withdrawn` flag), never `DELETE`. Reads `subscriptions`/`content` modules' entitlement/withdrawal data (read-only, cross-module service calls, not direct cross-module table joins).

## 15. Validation
N/A — internal scheduled job, no external input to validate.

## 16. Authentication
N/A — system-scheduled task, runs with service-level DB access, not a user session.

## 17. Authorization
N/A — no user-facing authorization surface; the job itself is restricted to run only via the Celery worker's own deployment-level access control (no public trigger endpoint).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Entitlement-service timeout for one row | That row logged, skipped, retried next scheduled run; batch continues for remaining rows |
| Job crashes mid-batch | Keyset pagination allows a safe resume/re-run without reprocessing already-updated rows incorrectly (idempotent `UPDATE`) |
| No longer entitled | `status → 'license_expired'`, row preserved |
| Content withdrawn | `withdrawn` flag set, row preserved, visible with appropriate messaging |

## 19. Offline First
N/A (backend scheduled job).

## 20. Local Data
N/A (backend).

## 21. Localization
N/A.

## 22. RTL
N/A.

## 23. Analytics
No direct client event; job run metrics (rows scanned, transitioned, failed) feed B-07's operational monitoring, surfaced in N-01.

## 24. Performance
- Keyset pagination (not `OFFSET`-based) for the batch scan to remain performant as `download_record` grows.
- Entitlement checks batched per-family where the `subscriptions`/`content` services support batch lookup, to avoid one round-trip per row on large children-with-many-downloads fixtures.
- Scheduled at a cadence (e.g., every 6–24 hours) that balances staleness-window risk against system load, per DevOps requirements.

## 25. Security
This job is the mechanism that closes the "offline access as a permanent bypass of a safety-driven content withdrawal" loophole (§12.7) — its correctness is a child-safety-relevant guarantee, not merely an operational one, and is treated with the same rigor as B-04's dedup guarantee in code review.

## 26. Library Requirements
Celery (existing infra), SQLAlchemy 2.0 (async). No new libraries.

## 27. Testing
- Unit: entitlement-revoked row transitions to `license_expired`, row not deleted.
- Unit: withdrawn-content row gets `withdrawn` flag set, `status` unaffected if otherwise still `complete`.
- Integration: simulated entitlement revocation via a fixture family/subscription state, job run, assert correct transition (§5 item 6's explicit test requirement).
- Integration: job idempotency — run twice in succession, assert no duplicate side effects or errors on the second run.
- Integration: partial-row-failure resilience — one row's entitlement-check fails, batch completes for all other rows.

## 28. Documentation
Docstring on the task explaining the non-deletion guarantee and its child-safety rationale; runbook note on the scheduled cadence and how to manually trigger an out-of-cycle run if a safety-critical withdrawal needs faster propagation.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Extend Repository for Batch Scanning**
Objective: `list_complete_downloads_batch(cursor, limit)`, `mark_license_expired()`, `flag_withdrawn()`.
Files to modify: `modules/downloads/repository.py`.

**Task 02 — Implement refresh_download_entitlements_task()**
Objective: keyset-paginated scan → per-row entitlement/withdrawal check → status/flag update.
Files to modify: `modules/downloads/tasks.py`.

**Task 03 — Register Celery Beat Schedule**
Files to modify: Celery beat schedule config.

**Task 04 — Add Revocation Transition Test (highest priority)**
Tests: `test_license_refresh_job.py`.

**Task 05 — Add Withdrawn-Content Flagging Test**
Tests: `test_withdrawn_content_flagging.py`.

**Task 06 — Add Idempotency & Partial-Failure Tests**

**Task 07 — Final Code Review**
Objective: confirm no `DELETE` statement anywhere in this task's code path.

## 30. Definition of Done
- Scheduled task live, correctly transitioning revoked/withdrawn records without deletion.
- Idempotent re-run verified.
- Partial-row-failure resilience verified.
- Runbook documentation complete.

## 31. Final Verification Checklist
- [ ] No `DELETE` statement anywhere in this job's code.
- [ ] Revoked entitlement → `license_expired`, row preserved.
- [ ] Withdrawn content → flagged, row preserved and still visible.
- [ ] Job safely idempotent and resumable on crash/partial run.
- [ ] Keyset pagination used, no unbounded full-table scan.
- [ ] No PostgreSQL/Redis credentials modified.
