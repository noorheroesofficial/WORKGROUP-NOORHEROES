---
id: api.admin-default-download-caps
kind: api
title: Admin Default Download Cap Configuration API (GET & PUT /v1/admin/downloads/default-caps)
status: stable
owner_story: TASK-B08
version: 1
created: 2026-09-30
---

## Endpoints

```http
GET /v1/admin/downloads/default-caps
PUT /v1/admin/downloads/default-caps
```

## Auth & Security

- **Auth**: Bearer admin session token via `Depends(get_current_admin)`.
- **RBAC**:
  - `GET`: Requires `admin:read`, `admin:write`, `product_admin`, `super_admin`, or `*` (`Depends(require_any_scope(...))`).
  - `PUT`: Requires `admin:write`, `product_admin`, `super_admin`, or `*` (`Depends(require_any_scope(...))`). `admin:read` alone returns `403 Forbidden`.
  - Child/Parent tokens: Rejected with `401/403`.
- **Anti-Caching Headers**:
  - `Cache-Control: no-store, no-cache, must-revalidate, private`
  - `Pragma: no-cache`
- **Method Guards**:
  - Mutating HTTP methods other than `PUT` (`POST`, `DELETE`, `PATCH`) return `405 Method Not Allowed`.

---

## 1. GET Response — 200 OK

```ts
export interface PlanDefaultCapItem {
  plan_code: string; // Identifier: "free" | "premium" | "family" | "default"
  cap_bytes: number; // Storage ceiling in bytes (e.g. 1073741824)
  version: number;   // Revision counter for optimistic locking
}

export interface DefaultCapConfigResponse {
  caps: PlanDefaultCapItem[];
}
```

*Note: Dual-wire compatibility supports both camelCase (`planCode`, `capBytes`) and snake_case (`plan_code`, `cap_bytes`).*

---

## 2. PUT Request & Response

### Request Payload

```ts
export interface PlanDefaultCapUpdateItem {
  plan_code: string; // "free" | "premium" | "family" | "default" (case-insensitive)
  cap_bytes: number; // 0 <= cap_bytes <= 100 GiB (107374182400)
  version: number;   // Expected current version (ge=1)
}

export interface DefaultCapConfigUpdateRequest {
  updates: PlanDefaultCapUpdateItem[]; // Non-empty array (min_length=1)
}
```

### Response — 200 OK

Returns updated `DefaultCapConfigResponse` matching the `GET` contract shape.

---

## Errors

- `401 UNAUTHENTICATED`: Missing, invalid, or expired admin token (or child/parent session provided).
- `403 FORBIDDEN`: Admin token lacking required scope (`admin:write` for PUT, `admin:read` for GET).
- `405 METHOD NOT ALLOWED`: `POST`, `DELETE`, or `PATCH` on endpoint.
- `409 OPTIMISTIC_LOCK_CONFLICT`: Concurrent edit conflict (stale `version` submitted). No partial writes committed.
- `422 VALIDATION_ERROR`:
  - `cap_bytes < 0` or `cap_bytes > 100 GiB`
  - Missing `version` field
  - Unknown `plan_code`
  - Empty `updates: []` array
  - Extra unrecognized fields (`extra="forbid"`)

---

## Core Invariants & Guarantees

1. **Non-Retroactive Parent Cap Preservation (Blueprint B-08 §10 / §25 / §27, PRD §12.5)**:
   - Changes to plan default caps never retroactively alter or override parent-set custom caps (`C.23`).
   - If a parent clears their custom cap, child profile seamlessly defaults to the active admin tier default.
2. **Optimistic Concurrency Control (Blueprint B-08 §10 / §18)**:
   - Each row carries an integer `version`. Mutations require exact version match and increment `version = version + 1`.
   - Stale versions abort with HTTP 409 Conflict.
3. **Atomic Savepoint Demarcation (Blueprint B-08 §10 / §18)**:
   - Batch updates execute within transactional savepoints (`begin_nested`), ensuring all-or-nothing rollback on conflict.
4. **Immutable Audit Trail (Blueprint B-08 §10 / §23, PRD §8)**:
   - Every mutation produces an immutable `AdminAuditRecord` with `admin_id`, old/new byte caps, version, and UTC timestamp.
