---
id: domain.delivery-adapter
kind: service
title: Delivery Adapter & Push Token Lifecycle Service
status: stable
owner_story: TASK-B17-05
version: 1
created: 2026-10-09
---

## Service Definition

```python
class DeliveryAdapter(BaseService):
    async def send_fcm(
        self,
        token: str,
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
        intent_id: Optional[str] = None,
        template_id: Optional[str] = None,
        recipient_ref: Optional[str] = None,
        deep_link_token: Optional[str] = None,
        max_retries: int = 3,
        base_delay_seconds: float = 0.05,
    ) -> DeliveryResult: ...

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        intent_id: Optional[str] = None,
        template_id: Optional[str] = None,
        recipient_ref: Optional[str] = None,
        max_retries: int = 3,
        base_delay_seconds: float = 0.05,
    ) -> DeliveryResult: ...

    async def send_batch_fcm(
        self,
        messages: List[Dict[str, Any]],
        max_concurrent: int = 50,
    ) -> List[DeliveryResult]: ...

    async def mark_opened(
        self,
        delivery_id: str,
        now: Optional[datetime] = None,
    ) -> Optional[NotificationDelivery]: ...


class PushTokenLifecycleManager(BaseService):
    async def get_token(self, token_id_or_fcm: str) -> Optional[PushToken]: ...

    async def is_token_deliverable(self, token_id_or_fcm: Union[str, PushToken]) -> bool: ...

    async def mark_invalid(
        self,
        token_id_or_fcm: str,
        reason: str = "UNREGISTERED",
    ) -> bool: ...

    async def refresh_rotated(
        self,
        old_token_id_or_fcm: str,
        new_fcm_token: str,
    ) -> Optional[PushToken]: ...

    async def handle_fcm_error(
        self,
        token_id_or_fcm: str,
        error_code_or_message: str,
        new_token: Optional[str] = None,
    ) -> str: ...
```

---

## 1. Domain Types & Transport Contracts

```python
class FCMResponse(BaseModel):
    success: bool
    message_id: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    new_token: Optional[str] = None


class EmailResponse(BaseModel):
    success: bool
    message_id: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None


class DeliveryResult(BaseModel):
    delivery_id: str
    status: str  # 'sent' | 'delivered' | 'failed'
    channel: str  # 'fcm' | 'email'
    recipient_ref: str
    retry_count: int = 0
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    sent_at: datetime
    latency_ms: float = 0.0
```

---

## 2. FCM Error Classification & Lifecycle Action Mappings

| FCM Error Code | Classification | Lifecycle Action / System Behavior |
|---|---|---|
| `UNREGISTERED` | `invalid` | Mark token `state='invalid'`, emit `PushTokenInvalidated`, permanently exclude from future sends. |
| `REGISTRATION_TOKEN_NOT_REGISTERED` | `invalid` | Mark token `state='invalid'`, emit `PushTokenInvalidated`. |
| `INVALID_ARGUMENT` (token format) | `invalid` | Mark token `state='invalid'`, emit `PushTokenInvalidated`. |
| `NOT_FOUND` | `invalid` | Mark token `state='invalid'`, emit `PushTokenInvalidated`. |
| `INVALID_REGISTRATION` | `invalid` | Mark token `state='invalid'`, emit `PushTokenInvalidated`. |
| `MISMATCH_SENDER_ID` | `invalid` | Mark token `state='invalid'`, emit `PushTokenInvalidated`. |
| `INVALID_TOKEN` | `invalid` | Mark token `state='invalid'`, emit `PushTokenInvalidated`. |
| `TOKEN_ROTATED` | `rotated` | Mark old `state='rotated'`, insert new active `PushToken`, emit `PushTokenRefreshed`. |
| `REFRESH_REQUIRED` | `rotated` | Mark old `state='rotated'`, insert new active `PushToken`, emit `PushTokenRefreshed`. |
| `TOKEN_REFRESH` | `rotated` | Mark old `state='rotated'`, insert new active `PushToken`, emit `PushTokenRefreshed`. |
| `QUOTA_EXCEEDED` | `transient` | Retry with bounded exponential backoff; alert on failure rate spike. |
| `UNAVAILABLE` | `transient` | Retry with bounded exponential backoff (`delay = base * 2^attempt`). |
| `INTERNAL` | `transient` | Retry with bounded exponential backoff. |
| `TIMEOUT` | `transient` | Retry with bounded exponential backoff. |
| `RESOURCE_EXHAUSTED` | `transient` | Retry with bounded exponential backoff. |
| `TOO_MANY_REQUESTS` | `transient` | Retry with bounded exponential backoff. |
| `SERVER_UNAVAILABLE` | `transient` | Retry with bounded exponential backoff. |

---

## 3. Core Architectural Invariants

1. **Pre-Send Deliverability Verification (PRD §5 Item 7, Blueprint B-05 §8/§10/§15)**:
   - Before attempting network transport via FCM, `DeliveryAdapter` calls `PushTokenLifecycleManager.is_token_deliverable(token)`.
   - Any token in `state='invalid'`, `state='rotated'`, or `expiry <= now()` is rejected immediately with `error_code='TOKEN_INVALID_PRECHECK'`.
   - **Zero network calls are made to dead tokens.**
2. **Terminal Invalid Token Eviction (PRD Edge Case 10, Blueprint B-05 §18)**:
   - Upon receiving an invalid/unregistered error from the FCM transport gateway, the token state transitions to `'invalid'`.
   - The token is never retried, and `PushTokenInvalidated` is emitted into the transactional outbox.
3. **Bounded Exponential Backoff for Transient Failures (Blueprint B-05 §10/§18)**:
   - Transient network/gateway errors retry up to `max_retries` (default 3) using `delay = base_delay_seconds * (2 ** attempt)`.
   - Infinite retry loops are strictly forbidden. Terminal failure persists a record with `status='failed'`.
4. **Concurrent High-Throughput Batch Fan-Out (Blueprint B-05 §10/§24)**:
   - `send_batch_fcm()` uses an `asyncio.Semaphore(max_concurrent)` pool to process large simultaneous notifications (e.g., daily reminder threshold hour) while strictly adhering to `latency p95 < 30s` (PRD §1.8 NFR).
5. **Open Receipt Traceability (Blueprint B-05 §14, PRD §1.17, Task B-06 Interaction)**:
   - Deep-link resolution service (`domain.deep-link-resolution` / TASK-B17-06) invokes `mark_opened(delivery_id)`.
   - Sets `opened_at` timestamp, transitions status to `'opened'`, and emits `NotificationOpened` for downstream conversion funnels and fatigue tracking.
   - **Conversion Funnel Integrity Gate**: `mark_opened` is strictly executed only upon valid resolution (`valid=True`). It is explicitly withheld on re-routes (`child_mismatch`, `requires_lock_gate`, `content_unavailable`, `session_expired`) to preserve pristine conversion analytics.
6. **Transactional Outbox Event Publication (Clean Architecture)**:
   - Domain events (`NotificationDelivered`, `NotificationOpened`, `PushTokenInvalidated`, `PushTokenRefreshed`) are committed atomically within the active database transaction to prevent dual-write drift.
