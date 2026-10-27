# B-03 — Data Export Request & Status API

## 1. Feature Context
Part of Feature C.26 — Privacy, Consent, Account Security & Data Rights (Settings). The platform's data-portability implementation — genuinely async, idempotent, and identically visible from both the mobile app and the NoorHeroes Web Account Portal (D.27).

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**B-03 — Data Export Request & Status API** (`POST /v1/data-requests/exports`, `GET /v1/data-requests/{id}`)

## 4. Objective
Implement a net-new async export pipeline: request creation with idempotent deduplication, a Celery worker that assembles a strictly family-scoped export, and a status endpoint returning byte-identical responses regardless of calling surface (mobile vs. web portal).

## 5. Business Requirements
- FR-5: async, cross-surface-consistent status.
- FR-12: export includes consent history, child progress summaries, AI interaction history, billing history; never another family's data; excludes raw biometric data (never exists in exportable form).
- Edge Case 2: duplicate export request while one is `preparing` — dedup or queue, never two conflicting "ready" states.
- Edge Case 7: large-family export handled via the existing async "preparing" state, no special-casing.
- NFR: Cross-Surface Consistency — single source of truth, never two diverging status views.

## 6. Existing Architecture
Net-new `Data Export Service` — no prior feature owns this. Lives in a new `modules/data_rights/` bounded context (sibling to `identity`/`ai_safety`, per `FAST-API-INSTRUCTIONS.md`'s modular-monolith pattern) since it spans multiple contexts' data (identity's consent/children, ai_safety's history, subscriptions' billing) and belongs to none of them individually — confirm this new-context decision against the platform's actual module registry before creating it, per rule 30, since adding an 11th bounded context is itself an architectural change worth a second pair of eyes.

## 7. Existing Code to Reuse
- `core/deps.py::get_current_parent`, `require_elevated_session`.
- Celery infrastructure already in use by `localization/tasks.py` (`retry_failed_translations_task()`) and C.21 B-06's `purge_expired_child_deletions.py` — same periodic/async-task framework, not a new job runner.
- `modules/identity/consent_repository.py::ConsentRepository.get_latest_for_family()` (A.1 B-05) — one of the export's data sources.
- `modules/ai_safety` read path (B-02, once extended) — another data source.
- `modules/subscriptions` billing-history read path — another data source.
- `common/outbox.py::OutboxWriter`.

## 8. Files to Create
- `src/noorheroes/modules/data_rights/__init__.py`
- `src/noorheroes/modules/data_rights/models.py` — `DataRequestOrm`
- `src/noorheroes/modules/data_rights/schemas.py` — `DataExportRequestResponse`, `DataRequestStatusResponse`
- `src/noorheroes/modules/data_rights/repository.py` — `DataRequestRepository` (`add()`, `get_in_progress_export_for_family()`, `get_by_id()`, `update_status()`)
- `src/noorheroes/modules/data_rights/service.py` — `DataExportService(BaseService)`
- `src/noorheroes/modules/data_rights/export_job.py` — Celery task `run_data_export_job(request_id: str)`
- `src/noorheroes/modules/data_rights/api.py` — `DataRequestsRouter`
- `alembic/versions/xxxx_create_data_request.py`
- `tests/modules/data_rights/test_data_export_service.py`
- `tests/modules/data_rights/test_data_export_idempotency.py`
- `tests/modules/data_rights/test_data_export_job.py`
- `tests/modules/data_rights/test_data_export_api.py`

## 9. Files to Modify
- Router registry (wherever `IdentityRouter`/`AISafetyRouter` etc. are mounted onto the FastAPI app) — mount `DataRequestsRouter`.
- Celery task registry/startup wiring — register `run_data_export_job`.

## 10. Backend Requirements
- `DataExportService.request_export(parent_ctx)`:
  1. Query `DataRequestRepository.get_in_progress_export_for_family(family_id)` — if a row exists with `type='export', status='preparing'`, return its `request_id` unchanged (Edge Case 2), do not enqueue a new job.
  2. Else, insert a new `data_request` row (`status='preparing'`), enqueue `run_data_export_job.delay(request_id)`, return the new `request_id`.
  3. This check-then-insert must be done under a row-level lock or a unique partial index (`WHERE status='preparing' AND type='export'` per `family_id`) to avoid a race between two near-simultaneous requests — do not rely on the read-then-write check alone under concurrency.
- `run_data_export_job(request_id)` (Celery task):
  1. Load the `data_request` row; strictly scope every downstream query by the row's `family_id` — never accept a family id from any other source.
  2. Gather: consent history (A.1's `ConsentRepository`), per-child progress summaries (owning module TBD — confirm against C.20/C.22's aggregation service rather than re-querying raw tables), AI interaction history (B-02's extended endpoint/service), billing history (`modules/subscriptions`).
  3. Assemble a structured export document (JSON or a generated file, per the platform's existing media/export convention — confirm against `modules/media`'s upload/asset pattern rather than inventing a new file-storage mechanism); exclude any biometric-shaped field entirely (there is none to exclude, per A.1/C.19's zero-biometric-storage guarantee — but assert this explicitly in code as a defensive check).
  4. On success: `status='ready'`, `completed_at=now()`, store `download_url` (signed, time-limited, via the same R2 pre-signed-URL mechanism `modules/media` already uses).
  5. On failure: `status='failed'`, alert, retry per Celery's standard retry policy (bounded, not infinite).
- `DataExportService.get_status(request_id, parent_ctx)`: family-ownership check, return current row state verbatim — **no surface-specific branching of any kind** (this is the cross-surface-consistency guarantee).

## 11. API Contract

### `POST /v1/data-requests/exports`
- **Auth:** Bearer + step-up
- **Response 200 (existing in-progress request):** `{ "request_id": "...", "status": "preparing" }`
- **Response 201 (new request created):** same shape — client does not need to distinguish 200 vs 201 semantically, though the status code itself signals new-vs-existing (confirm against PRD's stated `222` — likely a documentation typo for `201`/`200`, verify with API-contract owner before finalizing, do not implement a nonstandard `222` status code without explicit confirmation).

### `GET /v1/data-requests/{id}`
- **Auth:** Bearer + step-up
- **Response 200:** `{ "status": "preparing|ready|failed", "download_url": "..." }` — identical whether called from mobile or D.27's web portal, since both hit this same endpoint.
- **Error Responses:** `403`/`404` on cross-family access.

## 12. Database Requirements
```sql
CREATE TABLE data_request (
    request_id UUID PRIMARY KEY,
    family_id UUID NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('export','delete')),
    scope TEXT,
    status TEXT NOT NULL CHECK (status IN ('preparing','ready','failed')),
    download_url TEXT,
    requested_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ
);
CREATE UNIQUE INDEX data_request_one_in_progress_export_per_family
  ON data_request (family_id) WHERE type='export' AND status='preparing';
CREATE INDEX ON data_request (family_id, requested_at DESC);
```
The partial unique index is the concurrency-safe enforcement of the idempotent-dedup requirement — do not rely on application-level locking alone.

## 13. Validation
No request body required beyond auth; `id` path param on the status endpoint must be a valid UUID owned by the requesting family.

## 14. Authentication
`Depends(get_current_parent)` + `Depends(require_elevated_session)` on both endpoints (§FR-3: export requires step-up).

## 15. Authorization
Family-ownership check on every `data_request` row access.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Export job fails to start (queue unavailable) | `500` with clear retry messaging, never silent |
| Duplicate request while `preparing` | Returns existing `request_id`, no new job (enforced by the partial unique index + repository check) |
| Status query for a request not owned by the family | `403`/`404` |
| Job failure mid-processing | `status='failed'` visible via status endpoint, bounded Celery retries, alert on final failure |

## 17. Offline First
N/A — mutating actions require connectivity; status polling degrades gracefully offline (client shows last-known cached state, K-06).

## 18. Local Data
N/A (backend).

## 19. Localization
N/A — export document content localization (if any) is out of scope for this API contract; the export reflects data as stored.

## 20. RTL
N/A (backend).

## 21. Analytics
Backing source for `data_export_requested`, `data_export_status_viewed`, `data_export_completed` (K-06).

## 22. Performance
Export job runs async off the request path; large families accommodated by the existing "preparing" state with no additional handling (Edge Case 7); signed URL generation is O(1), not proportional to export size.

## 23. Security
- Strict family-scoping on every downstream query the export job issues — the single most important control preventing cross-family data leakage.
- Defensive assertion that no biometric-shaped field is ever included, even though none should exist upstream.
- Signed, time-limited download URLs — never a permanently public export file.

## 24. Library Requirements
Celery (existing), R2 pre-signed URL mechanism (existing, via `modules/media`'s pattern) — no new libraries.

## 25. Testing
- Unit: idempotent dedup — two rapid requests from the same family return the same `request_id`, only one Celery job enqueued.
- Integration: concurrency test — two near-simultaneous requests under load do not both create `preparing` rows (exercises the partial unique index).
- Integration: `get_status()` response is byte-identical regardless of a simulated "mobile" vs. "web portal" caller (no branching logic exists to diverge).
- Integration: export job strictly excludes another family's fixture data (cross-family leakage test — the highest-priority test for this sub-feature).
- Integration: export job failure sets `status='failed'` and is visible via the status endpoint.
- Unit: no biometric-shaped field appears in the assembled export document (defensive assertion test).

## 26. Documentation
OpenAPI must state the idempotency contract explicitly and that this endpoint's response is the single source of truth consumed identically by D.27's web portal — cross-reference D.27's blueprint once it exists.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Confirm New Bounded Context Placement**
- **Objective:** Verify `modules/data_rights/` as a new context is the correct home (per §6) rather than nesting this under an existing module.
- **Definition of Done:** Placement confirmed against the platform's actual module registry.

**Task 02 — `data_request` Model, Migration, Partial Unique Index**
- **Files to Create:** `models.py`, migration.
- **Definition of Done:** Migration applies; partial unique index present and verified via a concurrency test.

**Task 03 — `DataRequestRepository`**
- **Files to Create:** `repository.py`.
- **Definition of Done:** `get_in_progress_export_for_family()` correctly returns only `preparing`/`export` rows.

**Task 04 — `DataExportService.request_export()` with Idempotent Dedup**
- **Files to Create:** `service.py`.
- **Tests:** Task 25's idempotency and concurrency tests.
- **Definition of Done:** No duplicate `preparing` export rows possible even under concurrent requests.

**Task 05 — `run_data_export_job` Celery Task**
- **Files to Create:** `export_job.py`.
- **Implementation Details:** Strictly family-scoped gathering across identity/ai_safety/subscriptions read paths; signed URL on completion.
- **Tests:** Cross-family leakage test (highest priority), success and failure paths.
- **Definition of Done:** Job idempotent-safe on retry (does not duplicate output on redelivery).

**Task 06 — `GET /v1/data-requests/{id}` Status Endpoint**
- **Files to Modify:** `api.py`.
- **Tests:** Cross-surface-identical-response test.
- **Definition of Done:** Zero surface-specific branching exists in the implementation (verifiable by code inspection).

**Task 07 — Router Wiring & Step-Up Enforcement**
- **Definition of Done:** Both endpoints live, step-up enforced.

**Task 08 — Full Test Suite & Documentation**
- **Definition of Done:** All §25 tests green; OpenAPI updated.

## 28. Definition of Done
Data export requests are genuinely idempotent under concurrency, strictly family-scoped end to end, async via the platform's existing Celery infrastructure, and the status endpoint is provably surface-agnostic — ready to be consumed identically by D.27's web portal once built.

## 29. Final Verification Checklist
- [ ] `data_request` partial unique index enforces one in-progress export per family at the DB level, not just app-level
- [ ] Concurrency test confirms no duplicate `preparing` rows under simultaneous requests
- [ ] Export job cross-family leakage test passes
- [ ] No biometric-shaped field present in assembled export
- [ ] `GET /v1/data-requests/{id}` response verified surface-agnostic
- [ ] `222` status code in the source PRD confirmed/corrected before implementation (flagged, not silently implemented)
- [ ] No PostgreSQL/Redis credential changes
