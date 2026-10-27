---
id: api.admin-notification-reports
kind: api
title: Admin Notification Delivery, Engagement & Binding Health Reporting API
status: stable
owner_story: TASK-B17-08
version: 1
created: 2026-10-09
---

## Endpoints

```http
GET /v1/admin/notifications/reports/delivery-engagement?from={from}&to={to}&category={category}&locale={locale}
GET /v1/admin/notifications/reports/binding-health?from={from}&to={to}
```

## Auth & Security

- **Auth**: Bearer admin session token via `Depends(get_current_admin)`.
- **RBAC**:
  - `GET /delivery-engagement`: Requires `product_admin` or `content_editor` (plus `superadmin`, `super_admin`, `*`).
  - `GET /binding-health`: Requires `product_admin` or `trust_safety` (plus `superadmin`, `super_admin`, `*`).
  - Child and parent session tokens: Strictly rejected with `401 Unauthorized` / `403 Forbidden`.
- **Privacy & Child Safety Invariant**:
  - Aggregate statistics only. Under no circumstances are individual child profiles, parent IDs, tokens, or personal identifiers included.
  - Zero PII exposure across all reporting models.
- **Cache Strategy**:
  - Redis cache with 300s (5-minute) TTL (`reports:delivery_engagement:*`, `reports:binding_health:*`).
  - Fail-safe fallback to direct PostgreSQL queries on cache failure.

---

## 1. GET /v1/admin/notifications/reports/delivery-engagement — Delivery & Engagement Report (200 OK)

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `from` | string (ISO 8601 UTC) | Yes | Start timestamp of reporting window |
| `to` | string (ISO 8601 UTC) | Yes | End timestamp of reporting window |
| `category` | string | No | Optional notification trigger type (e.g. `daily_reminder`, `streak_risk`) |
| `locale` | string | No | Optional target template locale (e.g. `en`, `ar`, `ur`) |

### Validation Rules

- `to >= from`: Must be valid chronological range.
- `to - from <= 366 days`: Maximum 1-year window limit.
- Violation returns HTTP `422 Unprocessable Entity` with error code `INVALID_DATE_RANGE`.

### Response Payload (200 OK)

```ts
export interface DeliveryEngagementReportResponse {
  from: string; // ISO 8601 UTC
  to: string;   // ISO 8601 UTC
  category?: string | null;
  locale?: string | null;
  funnel: {
    created: number;
    sent: number;
    delivered: number;
    opened: number;
    deepLinkResolved: number;
  };
  suppressionBreakdown: {
    quietHours: number;
    frequencyCap: number;
    bindingInactive: number;
    staleCondition: number;
    consentWithdrawn: number;
  };
  fatigueBackoffCount: number;
  rates: {
    deliveryRate: number; // delivered / sent
    openRate: number;     // opened / delivered
    deepLinkResolutionRate: number; // deepLinkResolved / opened
  };
  sentRate?: number;      // sent / created
  deliveredRate?: number; // delivered / sent
  openRate?: number;      // opened / delivered
}
```

---

## 2. GET /v1/admin/notifications/reports/binding-health — Device Profile Binding Health Report (200 OK)

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `from` | string (ISO 8601 UTC) | Yes | Start timestamp of reporting window |
| `to` | string (ISO 8601 UTC) | Yes | End timestamp of reporting window |

### Response Payload (200 OK)

```ts
export interface BindingHealthReportResponse {
  from: string; // ISO 8601 UTC
  to: string;   // ISO 8601 UTC
  switchLatencyP50Ms: number; // 50th percentile (median) switch duration in milliseconds
  switchLatencyP95Ms: number; // 95th percentile switch duration in milliseconds
  misdeliveryRiskEventsPrevented: number; // Suppression count where cancellation_reason = 'binding_inactive'
}
```

---

## Error Envelopes

### HTTP 401 Unauthorized
```json
{
  "error": {
    "code": "AUTHENTICATION_REQUIRED",
    "message": "Missing or malformed Authorization header"
  }
}
```

### HTTP 403 Forbidden
```json
{
  "error": {
    "code": "INSUFFICIENT_PERMISSIONS",
    "message": "Admin missing at least one required scope from: ['content_editor', 'product_admin']"
  }
}
```

### HTTP 422 Unprocessable Entity (Invalid Date Range)
```json
{
  "error": {
    "code": "INVALID_DATE_RANGE",
    "message": "Parameter 'from' must be before or equal to 'to'."
  }
}
```
