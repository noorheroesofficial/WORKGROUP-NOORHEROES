# B-07 — Admin Search Operations Monitoring API

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). Read-only aggregate endpoints giving editorial/product/AI-ops staff visibility into search-system health: indexing sync lag, content rejected from indexing, zero-result query trends, and voice-search transcription quality — without ever exposing raw per-child data.

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
B-07 — Admin Search Operations Monitoring API

## 4. Objective
Expose four read-only, RBAC-scoped aggregate endpoints sourced from B-02 (indexing sync/rejections), B-03 (voice confidence), and B-04 (zero-result queries, content-safety-filtered before exposure).

## 5. Business Requirements
- Admin Requirements §8: Search Index Health Monitor (sync lag, rejected-indexing items), Zero-Result Query Report (aggregate, privacy-safe, no per-child attribution), Voice Search Confidence/Quality Monitor.
- DevOps §10: alert on sync-consumer lag, rejection-rate spikes, voice-search low-confidence-rate spikes.
- Edge Case 3 (carried forward from B-04): any aggregate "popular searches"/zero-result reporting must pass through a content-safety filter before persisting/displaying beyond the originating child's device.

## 6. Existing Architecture
Read-only aggregation endpoints inside the `search` module, following the existing `admin` module's read-only reporting pattern (e.g., `AdminAuditRepository.list_logs()`), RBAC-gated per-endpoint via `require_admin_scope`.

## 7. Existing Code to Reuse
- `core/deps.py` → `get_current_admin`, `require_admin_scope`.
- B-02's `search_index_rejection` data and `indexed_at` sync-freshness columns.
- B-03's per-request confidence scores (requires a lightweight aggregate table/log — see §14).
- B-04's `recent_search` data, read here only in aggregated, filtered form.
- `ai_safety` module's content-safety evaluation, applied to zero-result query text before aggregation exposure.

## 8. Files to Create
- `src/noorheroes/modules/search/monitoring_schemas.py` — `IndexHealthResponse`, `ZeroResultReportResponse`, `VoiceQualityResponse`.
- `src/noorheroes/modules/search/monitoring_service.py` — `SearchMonitoringService(BaseService)`.
- `src/noorheroes/modules/search/monitoring_repository.py` — aggregate queries.
- Extend `modules/search/api.py` — four new admin-scoped routes.
- New table/log for voice-confidence aggregation (see §14).
- `tests/modules/search/test_search_monitoring_api.py`.
- `tests/modules/search/test_zero_result_report_content_safety.py`.

## 9. Files to Modify
- `modules/search/voice_service.py` (B-03) — append a lightweight, PII-free confidence-score record per call (no transcript text stored, score + timestamp only) for N-04's trend chart.

## 10. Backend Requirements
- `GET /admin/v1/search/index-health` — sync lag (time since last successful sync event vs. now), list of rejected-from-indexing items with `content_id` + reason, each resolvable to a content-editor deep link.
- `GET /admin/v1/search/zero-result-report?from=&to=` — aggregated, **content-safety-filtered**, never-per-child-attributed top zero-result queries over a date range.
- `GET /admin/v1/search/voice-quality` — confidence-score distribution buckets and clarification-needed-rate trend over time, sourced from the PII-free confidence log (not from B-03's transcription text, which is never persisted at all per B-03's zero-retention guarantee).
- All four scoped per PRD §8: index-health → `content_editor`/`product_admin`; zero-result → `content_editor`; voice-quality → `ai_ops`/`product_admin`.

## 11. KMP Requirements
N/A — admin-only.

## 12. NextJS Requirements
Consumed by N-02 (Search Index Health Monitor), N-03 (Zero-Result Query Report), N-04 (Voice Search Quality Monitor).

## 13. API Contract
**Endpoint:** `GET /admin/v1/search/index-health` — Auth: admin + `content_editor`/`product_admin` scope — Response: `{ "sync_lag_seconds": 12, "rejected_items": [ { "content_id", "reason", "detected_at", "editor_url" } ] }`
**Endpoint:** `GET /admin/v1/search/zero-result-report?from=&to=` — Auth: admin + `content_editor` scope — Response: `{ "top_queries": [ { "query_text_filtered", "count" } ] }`
**Endpoint:** `GET /admin/v1/search/voice-quality` — Auth: admin + `ai_ops`/`product_admin` scope — Response: `{ "confidence_buckets": [...], "clarification_rate_trend": [...] }`

## 14. Database Requirements
- Reuse `search_index_rejection` (B-02) for index-health.
- New minimal table `voice_search_confidence_log`: `id`, `confidence_score`, `clarification_needed BOOLEAN`, `created_at` — explicitly **no `child_id`, no transcript text** column, by design, to keep this table structurally incapable of leaking per-child voice data even by accident.
- Zero-result aggregation reads `recent_search` (B-04) joined against a "resulted in zero matches" flag (add a `result_count` column to `recent_search` if not already present, or derive from a join at query time) — output is always a `GROUP BY query_text_filtered, COUNT(*)`, never a per-row/per-child listing.

## 15. Validation
Date-range params (`from`/`to`) validated as well-formed dates, bounded to a sane maximum range (e.g., 90 days) to bound aggregation query cost.

## 16. Authentication
`Depends(get_current_admin)` on all four endpoints.

## 17. Authorization
Distinct `require_admin_scope` per endpoint exactly as enumerated in §10 — not a single shared "admin" check, since the PRD requires different role tiers per monitor.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| No data in range | `200`, empty arrays |
| Invalid date range | `422` |
| Insufficient scope | `403` |
| Unauthenticated | `401` |

## 19. Offline First
N/A (admin web, always-online).

## 20. Local Data
N/A.

## 21. Localization
Admin-facing; localization handled at N-02/N-03/N-04's UI layer, not the API.

## 22. RTL
N/A (backend).

## 23. Analytics
These endpoints themselves are the analytics source for N-02/N-03/N-04's dashboards; no additional event emission needed here.

## 24. Performance
Zero-result and voice-quality aggregations are `GROUP BY`/bucketed queries over a bounded date range — add appropriate indexes on `created_at` for `recent_search` and `voice_search_confidence_log` to keep these performant at scale.

## 25. Security
- Zero-result report must never expose raw per-child query text or attribution — enforced by content-safety filtering applied before aggregation, and by the aggregation itself never selecting `child_id`.
- Voice-quality table is structurally incapable of holding transcript/audio data (no such column exists) — a defense-in-depth measure beyond B-03's own zero-retention guarantee.

## 26. Library Requirements
Existing stack only; optional lightweight scheduled aggregation if real-time `GROUP BY` proves too costly at scale (defer unless profiling shows a need — do not pre-build a materialized-view pipeline speculatively).

## 27. Testing
- Unit: date-range validation, scope-per-endpoint enforcement.
- Integration: index-health reflects a fixture set of rejected items with correct editor links.
- **Content-safety test:** assert the zero-result report never contains a raw, un-filtered query string that content-safety evaluation would have flagged.
- **Structural-privacy test:** assert `voice_search_confidence_log`'s schema has no column capable of holding transcript or `child_id` data (a schema-introspection test, not just a behavioral one).

## 28. Documentation
OpenAPI documents each endpoint's specific RBAC scope requirement distinctly; explicit note on `voice_search_confidence_log`'s intentionally minimal, PII-free schema.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Create Voice Confidence Log Table**
Objective: PII-free, transcript-free, child-id-free schema.
Files to create: migration, `monitoring_schemas.py` (partial).

**Task 02 — Wire Confidence Logging Into B-03**
Files to modify: `voice_service.py` — append `(confidence_score, clarification_needed, created_at)` only.

**Task 03 — Implement MonitoringRepository**
Objective: index-health, zero-result aggregation (with content-safety filter applied), voice-quality bucket queries.
Files to create: `monitoring_repository.py`.

**Task 04 — Implement MonitoringService & Endpoints**
Objective: per-endpoint RBAC scope wiring exactly per §17.
Files to create: `monitoring_service.py`; files to modify: `modules/search/api.py`.

**Task 05 — Add Content-Safety & Structural-Privacy Tests**
Files to create: `test_zero_result_report_content_safety.py`.

**Task 06 — Add Full Test Suite & Docs**

**Task 07 — Final Code Review**
Objective: confirm no endpoint here can be coerced into returning per-child-attributed data; confirm scope checks are per-endpoint, not shared.

## 30. Definition of Done
- All four endpoints live, correctly scoped per §17.
- Voice-confidence table schema verified free of PII/transcript columns.
- Zero-result report verified content-safety-filtered.

## 31. Final Verification Checklist
- [x] Index-health reflects real sync lag and rejected items with working editor links.
- [x] Zero-result report never exposes raw per-child query text or attribution.
- [x] Voice-quality table has no transcript/child_id column, verified by schema test.
- [x] Each endpoint enforces its own distinct RBAC scope.
- [x] Date-range params bounded and validated.

## 32. Implementation Summary & Verification Log

### Status: COMPLETED & VERIFIED (100% Tests Passing)
- **Feature Code:** B.13
- **Blueprint:** B-07 (Admin Search Operations Monitoring API)
- **Category:** Child App Supporting (13-18)

### Core Components Delivered:
1. **Alembic Migration (`0090_create_voice_search_confidence_log_and_add_result_count.py`):**
   - Created `voice_search_confidence_log` table with 4 columns: `id`, `confidence_score`, `clarification_needed`, `created_at`.
   - Added `result_count` integer column and composite index `ix_recent_search_result_created` to `recent_search`.
2. **Database Models (`src/noorheroes/modules/search/models.py` & `recent_search_models.py`):**
   - Added `VoiceSearchConfidenceLogOrm` entity with strict structural privacy (zero child_id, transcript, or audio columns).
   - Updated `RecentSearchOrm` with `result_count` column.
3. **Pydantic v2 Schemas (`src/noorheroes/modules/search/monitoring_schemas.py`):**
   - `IndexHealthResponse`, `RejectedIndexItem`, `ZeroResultReportResponse`, `ZeroResultQueryItem`, `VoiceQualityResponse`, `ConfidenceBucketItem`, `ClarificationTrendItem`.
   - Full dual-wire camelCase computed fields and OpenAPI descriptions.
4. **Data Access Repository (`src/noorheroes/modules/search/monitoring_repository.py`):**
   - `get_index_health`: Derives sync lag in seconds from latest `SearchIndexEntryOrm.indexed_at` and lists rejections from `SearchIndexRejectionOrm`.
   - `get_zero_result_query_frequencies`: Aggregates zero-result searches grouped by query text with counts, without selecting `child_id`.
   - `get_voice_quality_stats`: Computes 5 standard confidence distribution buckets and daily clarification trends.
   - `log_voice_confidence`: Appends PII-free confidence score and clarification needed flag.
5. **Domain Service (`src/noorheroes/modules/search/monitoring_service.py`):**
   - Date range validation (enforcing ISO-8601/YYYY-MM-DD, `from <= to`, max 90-day window).
   - Content safety filtering for zero-result queries (Edge Case 3) via heuristic sanitization and optional `AISafetyService`.
6. **API Routers (`src/noorheroes/modules/search/monitoring_api.py` & `admin_search_api.py`):**
   - Mounted at `/admin/v1/search/index-health`, `/admin/v1/search/rejected-items`, `/admin/v1/search/zero-result-report`, `/admin/v1/search/voice-quality`.
   - Canonical aliases mounted under `/v1/admin/search/*`.
   - Enforces distinct RBAC scopes per endpoint (`content_editor`, `product_admin`, `ai_ops`, `admin:read`, `*`).
7. **Test Suites Delivered:**
   - `tests/modules/search/test_search_monitoring_api.py` (15 tests: sync lag, rejected items, zero-result aggregation, date validation, voice quality buckets & trend, RBAC matrix, structural privacy schema reflection, dual-wire parity, 405 read-only contract, date filtering/validation, bucket boundaries, voice logging integration, query limit validation, clock drift resilience)
   - `tests/modules/search/test_zero_result_report_content_safety.py` (3 tests)
   - Total Search Module Tests: 227 passing (100% pass rate).
