---
id: api.admin-notification-templates
kind: api
title: Admin Notification Copy Template Governance API (CRUD, Blocklist Validation, Archive & Multi-Locale Listing)
status: stable
owner_story: TASK-B17-04
version: 1
created: 2026-10-09
---

## Endpoints

```http
POST   /v1/admin/notifications/templates
GET    /v1/admin/notifications/templates
GET    /v1/admin/notifications/templates/{template_id}
PATCH  /v1/admin/notifications/templates/{template_id}
POST   /v1/admin/notifications/templates/{template_id}/archive
DELETE /v1/admin/notifications/templates/{template_id}
```

## Auth & Security

- **Auth**: Bearer admin session token via `Depends(get_current_admin)`.
- **RBAC**:
  - `POST /templates`, `PATCH /templates/{id}`, `POST /templates/{id}/archive`, `DELETE /templates/{id}`: Requires `content_editor`, `product_admin`, `superadmin`, `super_admin`, or `*` (`Depends(require_any_scope(...))`).
  - `GET /templates`, `GET /templates/{id}`: Requires `content_editor`, `product_admin`, `admin:read`, `superadmin`, `super_admin`, or `*`.
  - Child and parent session tokens: Strictly rejected with `401/403`.
- **Content Safety Non-Bypassable Invariant (PRD FR-6, §12.1, §12.5, Blueprint B-04 §10, §25)**:
  - Every child-facing template (`template_class='child_facing'`) has its title and body scanned against the `ChildSafetyBlocklistValidator` for prohibited commercial, billing, pricing, trial, and sensitive analytics terms.
  - **Zero Bypass**: No administrative role (including `superadmin`), query parameter (`override`, `force`, `bypass`), header, or request body flag can bypass the validator.
  - Matches reject immediately with HTTP `422 Unprocessable Entity` (`BLOCKLIST_VIOLATION`), returning the exact offending term in the error envelope.
  - Parent-facing templates (`template_class='parent_facing'`) are exempt from commercial term blocking, allowing legitimate parent subscription and billing notices.
- **Single Active Template Mutex**:
  - Exactly one template with `status='active'` can exist per `(type, template_class, locale)`. Duplicate active creation or reactivation returns HTTP `409 Conflict` (`DUPLICATE_ACTIVE_TEMPLATE`).
- **Anti-Caching Headers**:
  - `Cache-Control: no-store, no-cache, must-revalidate, private`
  - `Pragma: no-cache`

---

## 1. POST /v1/admin/notifications/templates — Create Notification Template (201 Created)

### Request Payload

```ts
export interface TemplateCreateRequest {
  type: string;                           // Notification trigger type (e.g. "streak_risk", "bedtime_story", "milestone_badge")
  template_class: "child_facing" | "parent_facing"; // Audience isolation class (Default: "child_facing")
  locale: string;                         // Canonical language locale ("en", "ar", "ur", "hi")
  body: string;                           // Governed template body text with {{placeholder}} syntax
  title?: string | null;                  // Optional governed notification title
}
```

### Response Payload (201 Created)

```ts
export interface TemplateResponse {
  template_id: string;                    // UUIDv7 unique identifier
  type: string;                           // Notification trigger type
  template_class: "child_facing" | "parent_facing";
  locale: string;                         // Locale code (e.g. "en", "ar")
  title: string | null;                   // Template title or null
  body: string;                           // Governed template body
  status: "active" | "archived";          // Lifecycle status
  created_by: string | null;              // Admin UUID creator
  created_at: string;                     // ISO 8601 UTC timestamp
  updated_at: string;                     // ISO 8601 UTC timestamp
}
```

### Error Responses

- **401 Unauthorized**: Missing or expired admin token (`UNAUTHORIZED`).
- **403 Forbidden**: Caller lacks `content_editor` or equivalent scope (`INSUFFICIENT_SCOPE`).
- **409 Conflict**: Active template already exists for `(type, template_class, locale)`:
  ```json
  {
    "error": "DUPLICATE_ACTIVE_TEMPLATE",
    "message": "An active template already exists for type 'streak_risk', class 'child_facing', and locale 'en'.",
    "status_code": 409
  }
  ```
- **422 Unprocessable Entity — Blocklist Violation**:
  ```json
  {
    "error": "BLOCKLIST_VIOLATION",
    "message": "Child-facing notification copy violates safety blocklist: contains prohibited term 'trial'.",
    "status_code": 422,
    "details": {
      "matched_term": "trial",
      "template_class": "child_facing"
    }
  }
  ```
- **422 Unprocessable Entity — Placeholder Syntax Error**:
  ```json
  {
    "error": "TEMPLATE_PLACEHOLDER_ERROR",
    "message": "Required placeholder 'streak_count' is missing from template body for type 'streak_risk'.",
    "status_code": 422,
    "details": {
      "notification_type": "streak_risk",
      "missing_placeholders": ["streak_count"]
    }
  }
  ```

---

## 2. GET /v1/admin/notifications/templates — List Notification Templates (200 OK)

### Query Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `type` | string | No | null | Filter by trigger type (e.g. `streak_risk`) |
| `class` | string | No | null | Filter by audience class (`child_facing`, `parent_facing`) |
| `locale` | string | No | null | Filter by locale code (`en`, `ar`, `ur`, `hi`) |
| `status` | string | No | null | Filter by lifecycle status (`active`, `archived`) |
| `limit` | integer | No | 50 | Maximum records per page (1-100) |
| `offset` | integer | No | 0 | Pagination offset |

### Response Payload (200 OK)

```ts
export interface TemplateListResponse {
  items: TemplateResponse[];
  total: number;
  limit: number;
  offset: number;
}
```

---

## 3. GET /v1/admin/notifications/templates/{template_id} — Get Template Details (200 OK)

### Path Parameters

- `template_id`: UUIDv7 template primary identifier string.

### Response Payload (200 OK)

Returns `TemplateResponse` representing the requested record.

### Error Responses

- **404 Not Found**: Template does not exist:
  ```json
  {
    "error": "TEMPLATE_NOT_FOUND",
    "message": "Notification template with ID '0191c0e3-9824-7ef2-9e8a-0242ac120002' was not found.",
    "status_code": 404
  }
  ```

---

## 4. PATCH /v1/admin/notifications/templates/{template_id} — Update Template (200 OK)

### Request Payload

```ts
export interface TemplateUpdateRequest {
  title?: string | null;                  // Optional new title
  body?: string | null;                   // Optional new body copy (scanned for blocklist terms)
  status?: "active" | "archived" | null;  // Optional status transition
}
```

### Validation & Behavior

1. If `body` or `title` is modified and existing template is `child_facing`, the updated copy is evaluated against `ChildSafetyBlocklistValidator`. Violations return `422 BLOCKLIST_VIOLATION`.
2. Placeholders in updated copy are re-validated for syntax and required tokens.
3. If `status` transitions from `archived` to `active`, checks that no other active template exists for that `(type, template_class, locale)` tuple (`409 Conflict`).
4. On successful update, Redis template cache is automatically invalidated.

---

## 5. POST /v1/admin/notifications/templates/{template_id}/archive — Archive Template (200 OK)

### Path Parameters

- `template_id`: UUIDv7 template primary identifier.

### Behavior

Transitions template `status` to `'archived'`, invalidates Redis cache, and permits a new template to be activated for that `(type, template_class, locale)` slot. Returns updated `TemplateResponse`.

---

## 6. DELETE /v1/admin/notifications/templates/{template_id} — Soft Delete / Archive Template (200 OK)

### Path Parameters

- `template_id`: UUIDv7 template primary identifier.

### Behavior

Synonymous with archive endpoint. Soft-deletes the template by setting `status='archived'` and invalidating Redis cache. Returns updated `TemplateResponse`.
