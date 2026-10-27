# B-01 — Download Manifest Issuance API

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). This is the entry-point service every offline-capable feature (A.3/A.4/A.5/A.7/A.8/A.9/A.11) funnels through to obtain a signed, resumable download manifest — the single canonical place entitlement and the parent-configured download cap are checked before any byte leaves the CDN.

## 2. Parent Feature
B.15 — Offline Downloads & Sync

## 3. Sub-feature
B-01 — Download Manifest Issuance API

## 4. Objective
Implement `POST /v1/downloads/manifest` in a new `downloads` bounded context, issuing a short-TTL signed chunk manifest only after entitlement and cap/policy verification, with `UNIQUE(child_id, content_id)` semantics so a re-request for already-downloaded content resolves the existing record instead of duplicating it.

## 5. Business Requirements
- FR-2: canonical download flow — verify entitlement/policy → request signed manifest → resumable chunked download → local encryption/sandboxing → store version/locale/expiry/license → periodic entitlement refresh.
- FR-3: per-child download cap enforced before issuance; cap-exceeded shows a clear "cap reached" message, no download begins.
- FR-6: interrupted/failed downloads resume with exponential backoff rather than restarting (client-side, enabled by this endpoint's stable `manifest_id`/chunk addressing).
- Edge Case 3: re-download request for already-complete content is a no-op/"already downloaded" confirmation, not a duplicate manifest.
- Edge Case 5: signed manifest URL expiring mid-download is transparently re-issued via a fresh call to this same endpoint.
- Edge Case 9: device-storage-exhaustion is a client-side failure mode, not something this endpoint prevents — this endpoint's job stops at issuing a valid manifest.
- Acceptance Criteria §1.9: entitlement + cap verified before any download begins; cap-reached shows a clear message with no download starting.
- NFR: signed chunk URLs are short-TTL, consistent with A.3's media-security pattern (§12.3, §12.4).

## 6. Existing Architecture
New `downloads` bounded context at `src/noorheroes/modules/downloads/`, following the identical Router → Service → Repository → `BaseRepository[ModelT]` layering used by all 10 existing contexts (`FAST-API-INSTRUCTIONS.md` §1, §5) — this is the 11th context, flagged as an architecture addition in the B.15 breakdown's architecture note (not a bespoke pattern). Signed URLs are minted via the existing `CDNService`/`R2StorageService` (`infrastructure/`), not a new CDN integration. No Kafka is introduced for manifest issuance — this is a synchronous request/response path.

## 7. Existing Code to Reuse
- `core/deps.py` → `get_current_child`, `ChildSessionContext`.
- `common/base_repository.py` → `BaseRepository[ModelT]` for `DownloadRecordRepository`.
- `common/base_service.py` → `BaseService` for `DownloadService`.
- `common/outbox.py` → `OutboxWriter.emit()` to publish `DownloadManifestIssued` for B-07's health monitoring.
- `common/utils/ids.py` → `generate_ulid()` for `manifest_id`.
- `infrastructure/R2StorageService` / `CDNService` → signed, short-TTL chunk URL generation (same pattern as A.3's Signed Media Manifest Delivery API).
- `infrastructure/redis.py` → `get_redis_pool()` for the cap-usage read cache consumed from B-03.
- `common/schemas.py` → `NoorHeroesBaseModel` Pydantic v2 base.

## 8. Files to Create
- `src/noorheroes/modules/downloads/models.py` — `DownloadRecordOrm` (maps to `download_record`).
- `src/noorheroes/modules/downloads/schemas.py` — `DownloadManifestRequest`, `DownloadManifestResponse`, `ManifestChunk`.
- `src/noorheroes/modules/downloads/repository.py` — `DownloadRecordRepository(BaseRepository[DownloadRecordOrm])` with `get_by_child_and_content()`, `create_pending()`, `mark_complete()`.
- `src/noorheroes/modules/downloads/service.py` — `DownloadService(BaseService)` with `issue_manifest(child_ctx, payload) -> DownloadManifestResponse`.
- `src/noorheroes/modules/downloads/api.py` — `DownloadsRouter`, `POST /v1/downloads/manifest`.
- `src/noorheroes/modules/downloads/deps.py` — `get_download_service` factory.
- `tests/modules/downloads/test_manifest_issuance_api.py`.
- `tests/modules/downloads/test_manifest_dedup_and_cap.py`.
- Alembic migration: `create_download_record_table.py`.

## 9. Files to Modify
- `src/noorheroes/api/router.py` (v1 aggregator) — register `DownloadsRouter`.

## 10. Backend Requirements
- `POST /v1/downloads/manifest`, `Depends(get_current_child)`.
- Calls B-03's `EntitlementPolicyService.check_download_allowed(child_id, content_id)` before touching `download_record` — a `403` from that check short-circuits with **no row written**.
- Lookup existing `download_record` by `(child_id, content_id)` first: if `status == 'complete'`, return the existing manifest metadata (regenerating fresh signed URLs if the underlying chunks still exist) rather than creating a duplicate row (Edge Case 3).
- If `status in ('in_progress', 'failed')`, resume: reuse the existing `download_id`, reissue signed URLs for outstanding/all chunks.
- On a genuinely new request, insert a `download_record` row with `status='in_progress'` inside the same transaction the manifest is computed in.
- Response includes `manifest_id`, `chunks[]` (`chunk_id`, `url`, `checksum`), `expires_at`, `license_expires_at`.
- Emit `DownloadManifestIssued` outbox event (success or cap-rejected, for B-07's rejection-rate metric).

## 11. KMP Requirements
Consumed by K-01 (Download Initiation Gate) and K-02 (Resumable Chunked Download Engine) via `DownloadRepository.requestManifest()`. No KMP code produced by this backend blueprint; interface contract only (§13).

## 12. NextJS Requirements
N/A directly — issuance events feed B-07's read model, surfaced in N-01.

## 13. API Contract
**Endpoint:** `POST /v1/downloads/manifest`
**Auth:** Bearer, child-mode (`Depends(get_current_child)`)
**Request:**
```json
{ "content_id": "...", "content_type": "story", "quality": "standard" }
```
**Response 200:**
```json
{ "manifest_id": "...", "chunks": [ { "chunk_id": "...", "url": "...", "checksum": "sha256:..." } ], "expires_at": "...", "license_expires_at": "..." }
```
**Error Responses:** `403 DOWNLOAD_CAP_REACHED` (body includes `usage_bytes`/`limit_bytes`), `403 DOWNLOADS_DISABLED_BY_PARENT`, `403 ENTITLEMENT_REQUIRED`, `422` (invalid `content_type`).

## 14. Database Requirements
- New table `download_record`: `download_id UUID PK`, `child_id UUID FK`, `content_id UUID`, `content_type VARCHAR`, `status VARCHAR CHECK IN ('in_progress','complete','failed','license_expired')`, `size_bytes BIGINT`, `license_expires_at TIMESTAMPTZ`, `created_at TIMESTAMPTZ`.
- Constraints: `UNIQUE(child_id, content_id)` — the dedup backbone for this endpoint.
- Index: `(child_id, status)`.
- No PostgreSQL/Redis credential changes.

## 15. Validation
- `content_id` required, valid UUID.
- `content_type` restricted to known enum values (`story|surah|dua|quiz|audio`).
- `quality` optional, defaults to `standard`; invalid value → `422`.

## 16. Authentication
`Depends(get_current_child)` — rejects non-child-mode tokens with `401`.

## 17. Authorization
Implicit family/child scoping via `ChildSessionContext`; a child can never request a manifest for another family's content-entitlement context.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Cap exceeded | `403 DOWNLOAD_CAP_REACHED`, no `download_record` row created |
| Downloads disabled by parent | `403 DOWNLOADS_DISABLED_BY_PARENT` |
| Entitlement missing | `403 ENTITLEMENT_REQUIRED` |
| Already complete | `200`, existing record's manifest metadata returned (no duplicate) |
| In-progress/failed | `200`, resumed manifest for the same `download_id` |
| DB failure | `500`, logged with request ID, no partial row left in an ambiguous state (single transaction) |
| Redis cap-cache failure | Falls through to direct DB cap read in B-03 (never fail-open on the cap check) |

## 19. Offline First
N/A at backend layer — this is the online precondition to offline use; offline behavior is a KMP concern (K-02).

## 20. Local Data
N/A (backend).

## 21. Localization
N/A — response is data-only; user-facing cap/entitlement messaging is rendered client-side (K-01) from localized strings, not from this API's error body text.

## 22. RTL
N/A at API layer.

## 23. Analytics
No server-emitted analytics event directly; `download_initiated`, `download_cap_reached_shown` are client-fired (K-01) based on this endpoint's response/error.

## 24. Performance
- Cap-check delegated to B-03's Redis-cached read to keep p95 issuance latency low.
- Signed URL generation batched per chunk in a single `CDNService` call where the CDN SDK supports batch signing.
- Single DB transaction for the lookup-or-create path to avoid a race between two rapid manifest requests for the same content.

## 25. Security
- Cap/entitlement enforcement is server-side only — no client-suppliable override field exists in `DownloadManifestRequest`.
- Signed chunk URLs are short-TTL; no long-lived or unsigned CDN URL is ever returned.
- Concurrent double-request race on `(child_id, content_id)` handled via the `UNIQUE` constraint + retry-on-conflict, not an application-level lock.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), asyncpg, Redis, existing R2/CDN SDK. No new third-party media library.

## 27. Testing
- Unit: cap under-limit issues manifest; cap at-limit rejects with `403` and zero rows created.
- Unit: re-request for `complete` content returns existing record, no duplicate row (`UNIQUE` constraint never triggers an integrity error in the happy path).
- Integration: concurrent double-request race resolves to a single `download_record` row.
- Integration: expired signed URL scenario — client re-requests, receives fresh URLs for the same `download_id`.

## 28. Documentation
OpenAPI summary/description on the route; documented example for the cap-reached error body shape (`usage_bytes`, `limit_bytes`).

## 29. AI Coding Agent Implementation Steps
**Task 01 — Create Download Record Model & Migration**
Objective: `DownloadRecordOrm` and its Alembic migration with the `UNIQUE(child_id, content_id)` constraint.
Files to create: `modules/downloads/models.py`, migration file.
Expected result: table exists; migration applies/rolls back cleanly.

**Task 02 — Define Request/Response Schemas**
Objective: `DownloadManifestRequest`, `DownloadManifestResponse`, `ManifestChunk`.
Files to create: `modules/downloads/schemas.py`.

**Task 03 — Implement DownloadRecordRepository**
Objective: `get_by_child_and_content()`, `create_pending()`, `mark_complete()` on top of `BaseRepository`.
Files to create: `modules/downloads/repository.py`.

**Task 04 — Implement DownloadService.issue_manifest()**
Objective: orchestrate B-03 policy check → lookup-or-create → signed URL generation → outbox emit.
Business rules: no row written on cap/entitlement rejection; existing `complete` record returned as-is, not duplicated.
Files to create: `modules/downloads/service.py`.

**Task 05 — Implement API Endpoint**
Objective: `POST /v1/downloads/manifest` wired to `Depends(get_current_child)` and `Depends(get_download_service)`.
Files to create: `modules/downloads/api.py`, `modules/downloads/deps.py`.

**Task 06 — Add Cap/Dedup Test Suite (highest priority)**
Tests: `test_manifest_dedup_and_cap.py` — under-cap, at-cap, re-request-for-complete, concurrent-race.
Definition of done: CI-blocking gate per DevOps §10 of the parent PRD.

**Task 07 — Add Full Test Suite & OpenAPI Docs**
Objective: complete unit + integration coverage per §27, OpenAPI descriptions per §28.

**Task 08 — Final Code Review**
Objective: confirm no direct DB access in router, single-transaction lookup-or-create, no client-suppliable cap override field exists.

## 30. Definition of Done
- `POST /v1/downloads/manifest` live, matches §13 contract exactly.
- Cap/entitlement enforcement verified server-side-only via test.
- Re-request-for-complete-content dedup verified.
- Full unit + integration test suite green.
- OpenAPI documentation complete.

## 31. Final Verification Checklist
- [ ] Cap check runs before any `download_record` row is written.
- [ ] `403 DOWNLOAD_CAP_REACHED` includes usage/limit in body.
- [ ] Re-request for complete content never creates a duplicate row.
- [ ] Concurrent double-request race resolves to one row.
- [ ] Signed URLs are short-TTL, never unsigned/long-lived.
- [ ] No PostgreSQL/Redis credentials modified.
