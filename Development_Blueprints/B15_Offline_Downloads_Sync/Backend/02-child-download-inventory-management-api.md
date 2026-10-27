# B-02 — Child Download Inventory & Removal API

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). Powers the Downloads Tab's list view and the remove-one/clear-all actions — the read/delete counterpart to B-01's write path.

## 2. Parent Feature
B.15 — Offline Downloads & Sync

## 3. Sub-feature
B-02 — Child Download Inventory & Removal API

## 4. Objective
Implement `GET /v1/children/{id}/downloads`, `DELETE /v1/children/{id}/downloads/{content_id}`, and `DELETE /v1/children/{id}/downloads` (clear all), returning accurate near-real-time storage-used/limit figures and performing hard deletes on `download_record` without touching Favorites (B.14) or server-side progress history.

## 5. Business Requirements
- FR-1: Downloads tab shows download list, storage used vs. limit, remove, retry, clear-all.
- FR-10: Clear All removes all downloaded media for the child, freeing storage, without affecting Favorites or server-side progress history — downloading and favoriting are independent, decoupled actions on the same content item.
- Acceptance Criteria §1.9: Clear All removes all downloads, frees storage, favorites/progress history unaffected.
- Edge Case 10: removing a single download while a different download is actively in progress affects only the targeted item.
- §4.4 Database Design: `download_record` rows are hard-deleted (not soft-deleted) on explicit removal/clear-all — current-state inventory, not history.

## 6. Existing Architecture
Same `downloads` bounded context as B-01 (`src/noorheroes/modules/downloads/`), extending `DownloadRecordRepository`/`DownloadService` rather than introducing a parallel module.

## 7. Existing Code to Reuse
- `core/deps.py` → `get_current_child`, `ChildSessionContext` (family-ownership check on `{id}` path param).
- `common/base_repository.py` → `BaseRepository[ModelT]` — note: this endpoint deliberately does **not** use `soft_delete()`; it performs a real `DELETE`, an intentional, PRD-mandated deviation from the base repository's default soft-delete convention (§4.4 of the parent PRD).
- `common/outbox.py` → `OutboxWriter.emit()` for `DownloadRemoved`/`DownloadsClearedAll` events (feeds B-07).
- `common/base_service.py` → `BaseService` on `DownloadService` (shared with B-01).

## 8. Files to Create
- `tests/modules/downloads/test_inventory_and_removal_api.py`.
- `tests/modules/downloads/test_clear_all_decoupled_from_favorites.py`.

## 9. Files to Modify
- `modules/downloads/schemas.py` — add `DownloadInventoryResponse`, `DownloadItemResponse`, `ClearAllResponse`.
- `modules/downloads/repository.py` — add `list_by_child()`, `delete_one()`, `delete_all_for_child()`, `sum_storage_used()`.
- `modules/downloads/service.py` — add `get_inventory()`, `remove_download()`, `clear_all_downloads()`.
- `modules/downloads/api.py` — add the three new routes.

## 10. Backend Requirements
- `GET /v1/children/{id}/downloads`: family-ownership-checked, returns `downloads[]` + `storage_used_bytes` (live `SUM(size_bytes)` over the child's `download_record` rows, not a stale cached counter) + `storage_limit_bytes` (from B-03).
- `DELETE /v1/children/{id}/downloads/{content_id}`: hard-deletes the single row; idempotent — deleting an already-removed/non-existent item returns `200 { "removed": true }`, not a `404`, since the end state (item absent) is identical either way.
- `DELETE /v1/children/{id}/downloads`: hard-deletes all rows for the child in one transaction, returns `{ "cleared": true, "count": N }`; emits `DownloadsClearedAll` with the count for audit/analytics.
- Neither delete route touches `favorite` (B.14) tables or any owning domain's progress/reward tables — enforced by module-boundary (no cross-module writes in `DownloadService`).

## 11. KMP Requirements
Consumed by K-03 (Downloads Tab) via `DownloadRepository.getDownloads()`, `.removeDownload()`, `.clearAllDownloads()`.

## 12. NextJS Requirements
N/A directly — removal/clear-all volume feeds B-07's health metrics, surfaced in N-01/N-02 only as aggregate counts, never per-child detail (no admin visibility into a specific child's download list, consistent with child-data privacy posture).

## 13. API Contract
**Endpoint 1:** `GET /v1/children/{id}/downloads`
**Response 200:**
```json
{ "downloads": [ { "content_id": "...", "status": "complete", "size_bytes": 12345, "license_expires_at": "..." } ], "storage_used_bytes": 1234567, "storage_limit_bytes": 3221225472 }
```
**Endpoint 2:** `DELETE /v1/children/{id}/downloads/{content_id}` → `{ "removed": true }`
**Endpoint 3:** `DELETE /v1/children/{id}/downloads` → `{ "cleared": true, "count": 12 }`
**Auth (all three):** Bearer, child-mode, `Depends(get_current_child)` + family-ownership check on `{id}`.

## 14. Database Requirements
Reuses `download_record` (B-01). No new tables. Deletes are physical `DELETE` statements, never `deleted_at` soft-delete flags, per §4.4.

## 15. Validation
- `{id}` path param must resolve to a child belonging to the authenticated session's family — otherwise `403`, never a `404` that would leak child-ID existence across families.
- `content_id` in the single-delete route validated as a UUID.

## 16. Authentication
`Depends(get_current_child)` on all three routes.

## 17. Authorization
Family-ownership check on `{id}`: the authenticated child session's family must match the target child's family — a parent-mode or sibling-child token targeting a different child's `{id}` is rejected with `403`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| List with zero downloads | `200`, empty `downloads[]`, `storage_used_bytes: 0` |
| Remove non-existent item | `200 { "removed": true }` (idempotent no-op) |
| Clear-all with zero downloads | `200 { "cleared": true, "count": 0 }` |
| Cross-family `{id}` access | `403`, no data leaked |
| DB failure | `500`, logged with request ID |

## 19. Offline First
N/A at backend layer — the Downloads Tab itself is fully usable offline on the client (K-03) using locally cached inventory; this API is the online-refresh/mutation path.

## 20. Local Data
N/A (backend).

## 21. Localization
N/A — response is data-only.

## 22. RTL
N/A at API layer.

## 23. Analytics
No server-emitted event directly; `download_removed`, `downloads_cleared_all` are client-fired (K-03) on successful response. `DownloadsClearedAll` outbox event feeds B-07's aggregate health metrics only.

## 24. Performance
- `storage_used_bytes` computed via an indexed `SUM(size_bytes)` query on `(child_id)`, not a per-row application-level aggregation.
- Clear-all uses a single `DELETE ... WHERE child_id = :id` statement, not N individual deletes.

## 25. Security
- Family-ownership check is mandatory on every route — no endpoint here trusts `{id}` at face value.
- Clear-all is logged via outbox event (traceable, even though the row itself is hard-deleted) for support/dispute-resolution purposes.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), asyncpg. No new libraries.

## 27. Testing
- Unit: `storage_used_bytes` matches `SUM(size_bytes)` for a fixture set of downloads.
- Unit: remove-non-existent returns `200`/`removed: true`, not `404`.
- Integration: clear-all removes all `download_record` rows for the child, verifies `favorite` table (B.14) and progress/reward tables are completely untouched (Edge Case/FR-10's core guarantee).
- Integration: cross-family `{id}` access returns `403` with zero data returned.
- Integration: remove-one-while-another-in-progress only affects the targeted item (Edge Case 10).

## 28. Documentation
OpenAPI summaries for all three routes; explicit doc note that hard-delete (not soft-delete) is intentional for this table.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Extend Schemas**
Objective: `DownloadInventoryResponse`, `DownloadItemResponse`, `ClearAllResponse`.
Files to modify: `modules/downloads/schemas.py`.

**Task 02 — Extend Repository**
Objective: `list_by_child()`, `delete_one()`, `delete_all_for_child()`, `sum_storage_used()`.
Files to modify: `modules/downloads/repository.py`.

**Task 03 — Extend Service**
Objective: `get_inventory()`, `remove_download()`, `clear_all_downloads()`, each emitting the appropriate outbox event.
Files to modify: `modules/downloads/service.py`.

**Task 04 — Add Routes**
Objective: wire the three new endpoints with family-ownership checks.
Files to modify: `modules/downloads/api.py`.

**Task 05 — Add Decoupling Test (highest priority)**
Tests: `test_clear_all_decoupled_from_favorites.py` — asserts `favorite`/progress/reward tables untouched after clear-all.

**Task 06 — Add Full Test Suite & OpenAPI Docs**

**Task 07 — Final Code Review**
Objective: confirm hard-delete (not soft-delete) is used; confirm no cross-module writes in `DownloadService`.

## 30. Definition of Done
- All three routes live, matching §13 contracts.
- Clear-all verified to never touch Favorites or progress/reward history.
- Storage-used figure verified accurate against a fixture dataset.
- Full test suite green.

## 31. Final Verification Checklist
- [ ] `storage_used_bytes` is a live, accurate `SUM`, not a stale counter.
- [ ] Remove-non-existent is idempotent (`200`, not `404`).
- [ ] Clear-all never mutates `favorite` or progress/reward tables — verified by test.
- [ ] Family-ownership check enforced on all three routes.
- [ ] Deletes are hard deletes, not soft-delete flags.
- [ ] No PostgreSQL/Redis credentials modified.
