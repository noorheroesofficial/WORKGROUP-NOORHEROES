# B-04 — Bedtime Ritual Status Tracking API

> **Status:** Implemented & Verified (100% Green, 125 Bedtime Tests + 39 Parity Tests Passing, 0 Regressions)  
> **Parent Feature:** Feature A.4 — Audio Bedtime Player & Bedtime Mode  
> **Sub-feature ID:** B-04 (1.4 Bedtime Ritual Status Tracking API)  
> **Authoritative Specification:** `FAST-API-INSTRUCTIONS.md` §5.13 & `MASTER-README.md` §11.30  
> **Last Verified:** 2026-09-07  

## 1. Feature Context
Powers the lightweight, non-invasive "Bedtime Ritual ✓" indicator on the Parent Dashboard (FR-12) without the parent needing to query full Story Insights for a simple yes/no. Deliberately stores only a boolean and a date per child per day — detailed listening data stays exclusively in A.3's more thoroughly-governed Story Insights schema.

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
1.4 Bedtime Ritual Status Tracking API (ID: **B-04**)

## 4. Objective
Build a `bedtime_session_log` upsert triggered whenever a `silent_completion=true` completion (B-03) is processed for a child, and a read-only `GET /v1/children/{id}/bedtime-ritual-status?date=` endpoint for the Parent Dashboard widget — both within the `bedtime` module established in B-01.

## 5. Business Requirements
- FR-12: parent sees a lightweight "bedtime ritual happened" indicator, non-invasive (completion fact only, not full listening transcript/analytics).
- §5 (Backend AI prompt item 5): upsert `(child_id, session_date, ritual_completed=true)` via `ON CONFLICT (child_id, session_date) DO UPDATE`; endpoint returns ONLY a boolean and date.
- §4.5 Retention: retained for the same window as general progress history; no special shorter retention since it stores only a boolean + date.
- §12.6: minimal data surface by design — no detailed nightly listening transcripts in this table.

## 6. Existing Architecture
Extends the `bedtime` module created in B-01 (`modules/bedtime/`) with a second table and a second router surface — same layering, same module, no new bounded context.

## 7. Existing Code to Reuse
- `modules/bedtime/models.py`, `repository.py`, `service.py`, `api.py` (B-01's `BedtimeRouter` — add endpoint here, not a new router file)
- B-03's completion-processing call site — this is where the upsert trigger hooks in (an internal service call, not a new HTTP-facing integration)
- `common/base_repository.py`

## 8. Files to Create
- `alembic/versions/xxxx_add_bedtime_session_log.py`
- `tests/modules/bedtime/test_bedtime_session_log_service.py`
- `tests/modules/bedtime/test_bedtime_ritual_status_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/bedtime/models.py` — add `BedtimeSessionLogOrm` (`log_id: UUID PK`, `child_id: UUID FK`, `session_date: Date`, `ritual_completed: bool`, `created_at`; `UNIQUE(child_id, session_date)`)
- `src/noorheroes/modules/bedtime/repository.py` — add `BedtimeSessionLogRepository.upsert(child_id, session_date, ritual_completed=True)`
- `src/noorheroes/modules/bedtime/service.py` — add `BedtimeSessionLogService.record_ritual(child_id, session_date)`, `get_ritual_status(child_id, date, requester_ctx)`
- `src/noorheroes/modules/bedtime/api.py` — add `GET /v1/children/{id}/bedtime-ritual-status?date=`
- A.3's completion-processing call site (B-03's service method) — after a successful `silent_completion=true` write, call `BedtimeSessionLogService.record_ritual(child_id, today)`

## 10. Backend Requirements
- Upsert uses `ON CONFLICT (child_id, session_date) DO UPDATE SET ritual_completed = true` — multiple silent completions on the same day for the same child collapse to one row, never duplicated.
- `session_date` derived from server time at the moment the completion is processed (not client-supplied), to prevent client-side date manipulation.
- `get_ritual_status()`: returns `{ "child_id": ..., "date": ..., "ritual_completed": bool }` — for a date with no row, `ritual_completed: false`, not an error.
- The upsert call from B-03's completion path must be non-blocking to the completion response — if the upsert fails, log the error but do not fail the parent completion call (the reward/ledger write is the source of truth; the ritual-log row is a best-effort derived indicator).

## 11. API Contract

### `GET /v1/children/{id}/bedtime-ritual-status?date=YYYY-MM-DD`
- Auth: Bearer (parent-session; family-membership check on `child_id`).
- Response 200: `{ "child_id": "...", "date": "2026-08-16", "ritual_completed": true }`.
- Errors: `401 UNAUTHORIZED`, `403 FORBIDDEN` (parent outside family), `422 INVALID_DATE` (malformed date param).

## 12. Database Requirements
- `bedtime_session_log`: FK `child_id`; `UNIQUE(child_id, session_date)`; index `(child_id, session_date DESC)` for efficient recent-status/trend queries.
- No independent deletion lifecycle beyond the global account-deletion cascade (mirror B-01's cascade convention).
- Retention: same window as general progress history — confirm the existing retention job/policy that governs progress-history tables and register this table under the same policy rather than writing a new retention job.

## 13. Validation
- `date` query param must be a valid `YYYY-MM-DD` date; reject malformed input with `422 INVALID_DATE`.
- No future-dated queries beyond server "today" are meaningful, but are not rejected outright (simply return `ritual_completed: false` for a future date with no row) — avoids brittle server/client clock-skew edge cases.

## 14. Authentication
Bearer, parent-session only for the read endpoint (this is intentionally more restrictive than B-01's `GET`, since ritual status is Parent Dashboard-facing, not child-facing).

## 15. Authorization
Parent session scoped to children within their own family — reuse the same family-membership check used in B-01.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| No row for the requested date | `200` with `ritual_completed: false` |
| Malformed `date` param | `422 INVALID_DATE` |
| Parent requests a child outside their family | `403 FORBIDDEN` |
| Upsert fails during completion processing | Logged, does not fail the parent `POST /complete` call (B-03) |
| Database read failure | `503`, structured error, logged with correlation ID |

## 17. Security
- Response is strictly boolean + date — no detailed content/duration data is ever included, enforced by the response schema itself having no fields beyond `child_id`, `date`, `ritual_completed` (defense against future accidental field creep).
- Parent-session-only read access, scoped to own family.

## 18. Analytics
Emit via `OutboxWriter`: `parent_bedtime_ritual_status_viewed` when the Parent Dashboard widget calls this endpoint.

## 19. Performance
- Single upsert per completion event (not per heartbeat) — negligible write load.
- Read path is a single indexed lookup by `(child_id, session_date)`.

## 20. Library Requirements
No new third-party libraries.

## 21. Testing
- Unit: upsert idempotency — multiple silent completions same day/child produce exactly one row with `ritual_completed=true`.
- Unit: `get_ritual_status()` returns `false` (not an error) for a date with no row.
- Integration: upsert triggered correctly from B-03's completion path; upsert failure does not fail the parent completion response.
- Integration: `403` for parent requesting a child outside their family; `422` for malformed date.

## 22. Documentation
Update OpenAPI schema for the new endpoint; run `classify_openapi_diff.py`.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `BedtimeSessionLogOrm` Model & Migration**
Objective: New table with `UNIQUE(child_id, session_date)` and the recency index. Follow: B-01's model conventions in the same `bedtime` module. Files to create: migration file. Files to modify: `models.py`. Tests: migration up/down smoke test; unique-constraint-violation test (raw insert). Definition of Done: constraint verified at the DB layer.

**Task 02 — Implement `BedtimeSessionLogRepository.upsert()`**
Objective: `ON CONFLICT (child_id, session_date) DO UPDATE` upsert. Follow: `BaseRepository`. Dependencies: Task 01. Tests: upsert idempotency test. Definition of Done: test passes.

**Task 03 — Implement `BedtimeSessionLogService`**
Objective: `record_ritual()` (server-time-derived date, non-blocking failure handling) and `get_ritual_status()` (safe-default for missing rows). Dependencies: Task 02. Tests: server-time-derivation test, missing-row-returns-false test. Definition of Done: tests pass.

**Task 04 — Hook `record_ritual()` into B-03's Completion Path**
Objective: After a successful `silent_completion=true` ledger write, call `record_ritual(child_id, today)` — failure here must not fail the parent completion response. Files to modify: B-03's completion service method. Dependencies: Task 03, B-03. Tests: upsert-failure-does-not-fail-completion test (mocked upsert exception). Definition of Done: test passes.

**Task 05 — Add `GET /v1/children/{id}/bedtime-ritual-status` Endpoint**
Objective: Parent-session-only read, family-scoped. Files to modify: `api.py`. Dependencies: Task 03. Tests: `403`/`422` cases per §16. Definition of Done: tests pass.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §21. Definition of Done: all green in CI.

**Task 07 — Register Table Under Existing Retention Policy**
Objective: Confirm and apply the existing progress-history retention job to `bedtime_session_log` rather than writing a new retention mechanism. Definition of Done: table confirmed under the correct policy (documented, not a new cron job).

**Task 08 — Update OpenAPI Documentation**
Objective: Regenerate and diff-classify. Definition of Done: additive/non-breaking diff confirmed.

**Task 09 — Final Code Review**
Objective: Confirm the response payload can never expose more than boolean+date; confirm upsert failures are fully isolated from the completion response path. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [x] `bedtime_session_log` upsert collapses multiple same-day completions to one row
- [x] `session_date` derived from server time, never client-supplied
- [x] Read endpoint returns strictly `{ child_id, date, ritual_completed }` — no detailed data
- [x] Missing row returns `ritual_completed: false` with `200`, not an error
- [x] Upsert failure during completion processing does not fail the parent's `POST /complete` response
- [x] Parent-session-only read access, family-scoped
- [x] Table registered under the existing progress-history retention policy
- [x] Analytics event emitted on Parent Dashboard widget view

## 25. Definition of Done
The Parent Dashboard can reliably display a non-invasive "Bedtime Ritual ✓" indicator backed by a minimal, privacy-conscious `bedtime_session_log` table, upserted automatically from B-03's silent-completion path without ever risking the parent-facing completion flow.
