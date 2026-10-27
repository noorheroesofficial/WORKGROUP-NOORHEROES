---
id: api.download-inventory
kind: api
title: Child Download Inventory & Removal API (GET & DELETE /v1/children/{id}/downloads)
status: stable
owner_story: TASK-B02
version: 1
created: 2026-09-29
---

## Endpoints

```http
GET    /v1/children/{id}/downloads
DELETE /v1/children/{id}/downloads/{content_id}
DELETE /v1/children/{id}/downloads
```

## Auth & Security

- **Auth**: Bearer child session token (`Depends(get_current_child)`).
- **Scope**: Rejects parent-mode tokens (`SessionMode.PARENT`) with HTTP `403 Forbidden`.
- **Family-Ownership Gate (`verify_child_download_scope`)**:
  - Validates that path parameter `{id}` matches the authenticated child profile's `child_id`. Cross-child or cross-family access is rejected with HTTP `403 Forbidden`.
- **Anti-Caching Headers**:
  - `Cache-Control: private, no-store, no-cache, must-revalidate`
  - `Pragma: no-cache`

---

## 1. GET /v1/children/{id}/downloads — 200 OK

```ts
export interface DownloadItemResponse {
  content_id: string;
  content_type: string;
  status: "complete" | "in_progress" | "failed" | "license_expired";
  size_bytes: number;
  license_expires_at?: string | null;
  withdrawn: boolean;
  created_at: string;
}

export interface DownloadInventoryResponse {
  downloads: DownloadItemResponse[];
  storage_used_bytes: number;  // Live SUM(size_bytes)
  storage_limit_bytes: number; // Effective cap from policy engine
}
```

---

## 2. DELETE /v1/children/{id}/downloads/{content_id} — 200 OK

```ts
export interface DownloadRemovedResponse {
  removed: boolean; // Always true (idempotent)
}
```

*Note: Removing a non-existent or already-deleted content item returns HTTP `200 { "removed": true }` idempotently.*

---

## 3. DELETE /v1/children/{id}/downloads — 200 OK (Clear All)

```ts
export interface ClearAllResponse {
  cleared: boolean; // Always true
  count: number;    // Number of purged records
}
```

---

## 4. Error Responses

| Code | HTTP Status | Description | Details Envelope |
|---|---|---|---|
| `UNAUTHENTICATED` | 401 | Missing or malformed child Bearer token | `{ "code": "UNAUTHENTICATED", "message": "..." }` |
| `FORBIDDEN` | 403 | Parent-mode token or scope violation | `{ "code": "FORBIDDEN", "message": "..." }` |
| `CHILD_SCOPE_VIOLATION` | 403 | Accessing/mutating another child profile's downloads | `{ "code": "CHILD_SCOPE_VIOLATION" }` |
| `VALIDATION_ERROR` | 422 | Invalid UUID format for `{id}` or `{content_id}` | `{ "code": "VALIDATION_ERROR", "details": [...] }` |

---

## 5. Core Invariants & Guarantees

1. **Physical Hard-Delete Convention (PRD §4.4, Blueprint B-02 §5 / §14)**:
   - Records are permanently removed (`DELETE FROM download_record WHERE ...`) rather than soft-deleted with timestamps, reflecting current-state inventory.
2. **Strict Decoupling from Favorites & Progress (PRD FR-10, Blueprint B-02 §5 / §10)**:
   - Removing single items or issuing Clear All NEVER mutates or deletes rows from `favorite` (B.14), story playback progress, habit check-ins, or reward ledgers.
3. **Live Aggregate Accuracy (Blueprint B-02 §10 / §24)**:
   - `storage_used_bytes` is computed via live database query `SUM(size_bytes) WHERE child_id = :id AND status = 'complete'`, eliminating counter drift.
4. **Targeted Removal Isolation (PRD Edge Case 10)**:
   - Removing a single completed download while another download is actively in progress affects only the targeted item without canceling or corrupting the in-progress download.
5. **Outbox Auditing**:
   - Deletions emit `DownloadRemoved` and `DownloadsClearedAll` outbox domain events.
