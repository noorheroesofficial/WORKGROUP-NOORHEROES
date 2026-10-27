---
id: api.admin-notification-campaigns
kind: api
title: Admin Notification Campaign & Segment API (CRUD, Preview, Test Send, Cancel, Kill-Switch & Segment Estimation)
status: stable
owner_story: TASK-B17-07
version: 1
created: 2026-10-09
---

## Endpoints

```http
POST  /v1/admin/notifications/campaigns
GET   /v1/admin/notifications/campaigns
GET   /v1/admin/notifications/campaigns/{campaign_id}
PATCH /v1/admin/notifications/campaigns/{campaign_id}
POST  /v1/admin/notifications/campaigns/{campaign_id}/schedule
POST  /v1/admin/notifications/campaigns/{campaign_id}/preview
POST  /v1/admin/notifications/campaigns/{campaign_id}/test-send
POST  /v1/admin/notifications/campaigns/{campaign_id}/cancel
POST  /v1/admin/notifications/campaigns/{campaign_id}/kill-switch
POST  /v1/admin/notifications/segments/estimate
```

## Auth & Security

- **Auth**: Bearer admin session token via `Depends(get_current_admin)`.
- **RBAC**:
  - `POST /campaigns`, `PATCH /campaigns/{id}`, `POST /campaigns/{id}/schedule`, `POST /test-send`, `POST /cancel`, `POST /kill-switch`: Requires `notification_manager`, `content_editor`, `product_admin`, `superadmin`, or `*` (`Depends(require_any_scope(...))`).
  - `GET /campaigns`, `GET /campaigns/{id}`, `POST /preview`, `POST /segments/estimate`: Requires `admin:read`, `notification_manager`, `content_editor`, `product_admin`, `superadmin`, or `*`.
  - Child and parent session tokens: Strictly rejected with `401/403`.
- **Anti-Caching Headers**:
  - `Cache-Control: no-store, no-cache, must-revalidate, private`
  - `Pragma: no-cache`
- **Method & Audit Guards**:
  - Every mutating action (`create`, `update`, `schedule`, `test_send`, `cancel`, `kill_switch`) writes an immutable audit record to `admin_audit_records`.

---

## 1. POST /v1/admin/notifications/campaigns — Create Campaign (201 Created)

### Request Payload

```ts
export interface CampaignCreateRequest {
  templateId: string; // UUIDv7 of active NotificationTemplate
  title: string;      // Campaign administrative label (1-255 chars)
  segmentFilters?: {
    targetAudience?: "child" | "parent" | "family"; // Default: "family"
    locales?: string[];                             // ["en", "ar", "ur", "hi"]
    ageBands?: string[];                            // ["early_childhood", "middle_childhood"]
    activityThresholdDays?: number;
    completedStoryIds?: string[];
    isTestSegment?: boolean;
  };
  scheduledAt?: string; // Optional future ISO 8601 UTC timestamp
}
```

### Response Payload — 201 Created

```ts
export interface CampaignResponse {
  campaignId: string;
  templateId: string;
  title: string;
  segmentFilters: Record<string, any>;
  status: "draft" | "scheduled" | "sending" | "sent" | "canceled" | "killed";
  scheduledAt: string | null;
  totalRecipients: number;
  sentCount: number;
  suppressedCount: number;
  failedCount: number;
  createdBy: string | null;
  createdAt: string;
  updatedAt: string;
}
```

---

## 2. GET /v1/admin/notifications/campaigns — List Campaigns (200 OK)

### Query Parameters
- `status`: Optional filter (`draft`, `scheduled`, `sending`, `sent`, `canceled`, `killed`)
- `templateId`: Optional template filter
- `limit`: Integer (default 50, max 100)
- `offset`: Integer (default 0)

### Response Payload

```ts
export interface CampaignListResponse {
  items: CampaignResponse[];
  total: number;
  limit: number;
  offset: number;
}
```

---

## 2.1 PATCH /v1/admin/notifications/campaigns/{campaign_id} — Update Draft Campaign (200 OK)

Updates mutable attributes of an existing draft campaign (`title`, `templateId`, `segmentFilters`, `scheduledAt`).
Only campaigns with status `draft` may be modified; any other state returns `409 Conflict`.
Enforces Child Safety Blocklist check if child-facing template or audience segment is specified.

### Request Payload
```ts
export interface CampaignUpdateRequest {
  title?: string;
  templateId?: string;
  segmentFilters?: Record<string, any>;
  scheduledAt?: string; // Optional future ISO 8601 UTC timestamp
}
```

### Response Payload
Returns updated `CampaignResponse`.

---

## 2.2 POST /v1/admin/notifications/campaigns/{campaign_id}/schedule — Schedule Campaign (200 OK)

Explicitly transitions a campaign to `scheduled` state, expanding the target audience (1 intent per parent + 1 per active child for family campaigns) and routing through the Policy Engine.

### Request Payload
```ts
export interface CampaignScheduleRequest {
  scheduledAt?: string; // Optional future ISO 8601 UTC override
}
```

### Response Payload
Returns updated `CampaignResponse` with `status: "scheduled"`.

---

## 3. POST /v1/admin/notifications/campaigns/{campaign_id}/preview — Preview Campaign (200 OK)

Renders template copy with sample parameters without writing any notification intents to the database.

### Request Payload
```ts
export interface CampaignPreviewRequest {
  locale?: string; // Default: "en"
  sampleParams?: Record<string, any>;
}
```

### Response Payload
```ts
export interface CampaignPreviewResponse {
  campaignId: string;
  templateId: string;
  title: string | null;
  body: string;
  locale: string;
  isRtl: boolean;
  sampleParams: Record<string, any>;
}
```

---

## 4. POST /v1/admin/notifications/campaigns/{campaign_id}/test-send — Test Send (200 OK)

Dispatches isolated sandbox intents strictly scoped to designated admin test recipients.

### Request Payload
```ts
export interface CampaignTestSendRequest {
  testRecipients: string[]; // List of push tokens or device identifiers
  locale?: string;          // Default: "en"
}
```

### Response Payload
Returns updated `CampaignResponse` reflecting the test dispatch count.

---

## 5. POST /v1/admin/notifications/campaigns/{campaign_id}/cancel — Cancel Campaign (200 OK)

Transitions campaign status from `draft` or `scheduled` to `canceled` and revokes all pending intents.

### Query Parameters
- `reason`: Optional cancellation explanation (default: `"admin_canceled"`)

### Response Payload
Returns updated `CampaignResponse` with `status: "canceled"`.

---

## 6. POST /v1/admin/notifications/campaigns/{campaign_id}/kill-switch — Emergency Kill-Switch (200 OK)

Immediately halts all in-flight delivery worker sends for an active campaign, aborting both `pending` and `processing` intents.

### Query Parameters
- `reason`: Optional justification string (default: `"emergency_kill_switch"`)

### Response Payload
Returns updated `CampaignResponse` with `status: "killed"`.

---

## 7. POST /v1/admin/notifications/segments/estimate — Aggregate Estimation (200 OK)

Returns privacy-preserving aggregate audience numbers. Guarantees zero individual PII exposure.

### Request Payload
```ts
export interface SegmentFilterRequest {
  targetAudience?: "child" | "parent" | "family";
  locales?: string[];
  ageBands?: string[];
  activityThresholdDays?: number;
  completedStoryIds?: string[];
  isTestSegment?: boolean;
}
```

### Response Payload
```ts
export interface SegmentEstimateResponse {
  estimatedFamilies: number;
  estimatedChildren: number;
  estimatedDevices: number;
  totalEstimatedRecipients: number;
  confidence: "high" | "medium" | "low";
  breakdownByLocale?: Record<string, number>;
  breakdownByAgeBand?: Record<string, number>;
}
```

---

## Errors & Status Codes

- `401 UNAUTHENTICATED`: Missing or invalid Bearer token.
- `403 FORBIDDEN`: Insufficient admin role/scope.
- `404 NOT_FOUND`: Campaign or template not found (`CAMPAIGN_NOT_FOUND`, `TEMPLATE_NOT_FOUND`).
- `409 CONFLICT`: Invalid state machine transition (`CAMPAIGN_INVALID_STATE`).
  - Attempting to update non-draft campaign.
  - Attempting to cancel an already-sent or terminal campaign.
  - Attempting to trigger kill-switch on a fully-sent campaign.
  - Attempting to schedule a terminal campaign.
- `422 UNPROCESSABLE_ENTITY`:
  - Child safety blocklist violation (`BLOCKLIST_VIOLATION`).
  - Past `scheduled_at` timestamp (`CAMPAIGN_SCHEDULE_TIME_ERROR`).
  - Unrecognized segment filters (`INVALID_SEGMENT_FILTER`).
