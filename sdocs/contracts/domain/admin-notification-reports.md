---
id: domain.admin-notification-reports
kind: service
title: Notification Reporting & Binding Health Monitoring Domain Service
status: stable
owner_story: TASK-B17-08
version: 1
created: 2026-10-09
---

## Service Definition

```python
class NotificationReportingService(BaseService):
    def __init__(
        self,
        session: AsyncSession,
        redis: Optional[Redis] = None,
        cache_ttl: int = CACHE_TTL_SECONDS,  # 300 seconds
    ) -> None: ...

    @staticmethod
    def validate_date_range(
        from_date: datetime,
        to_date: datetime,
    ) -> Tuple[datetime, datetime]: ...

    async def record_switch_latency(
        self,
        latency_ms: float,
        recorded_at: Optional[datetime] = None,
    ) -> None: ...

    async def get_delivery_engagement_report(
        self,
        from_date: datetime,
        to_date: datetime,
        category: Optional[str] = None,
        locale: Optional[str] = None,
    ) -> DeliveryEngagementReportResponse: ...

    async def get_binding_health_report(
        self,
        from_date: datetime,
        to_date: datetime,
    ) -> BindingHealthReportResponse: ...
```

---

## Domain Models & DTO Interfaces

```python
class DeliveryEngagementFunnel(NoorHeroesBaseModel):
    created: int
    sent: int
    delivered: int
    opened: int
    deep_link_resolved: int


class DeliveryEngagementRates(NoorHeroesBaseModel):
    delivery_rate: float
    open_rate: float
    deep_link_resolution_rate: float


class DeliveryEngagementReportResponse(NoorHeroesBaseModel):
    from_date: Optional[datetime]
    to_date: Optional[datetime]
    category: Optional[str]
    locale: Optional[str]
    funnel: DeliveryEngagementFunnel
    suppression_breakdown: Dict[str, int]
    fatigue_backoff_count: int
    rates: Optional[DeliveryEngagementRates]
    sent_rate: float
    delivered_rate: float
    open_rate: float


class BindingHealthReportResponse(NoorHeroesBaseModel):
    from_date: Optional[datetime]
    to_date: Optional[datetime]
    switch_latency_p50_ms: float
    switch_latency_p95_ms: float
    misdelivery_risk_events_prevented: int
```

---

## Core Domain Invariants

1. **Pure Read-Only Analytics:**
   - The reporting service queries `notification_intents`, `notification_deliveries`, `notification_templates`, and transactional outbox events.
   - It performs zero mutation or write operations to operational notification persistence tables.

2. **Date Range Validation & Query Cost Bounding:**
   - Enforces chronological validity: `to >= from`.
   - Bounded window constraint: `(to - from) <= 366 days` (1 year).
   - Timezone conversion: All non-UTC datetimes are normalized to UTC via `astimezone(timezone.utc)`.
   - Invalid or excessive date ranges raise `InvalidDateRangeError` (HTTP 422).

3. **Short-TTL Caching with Fail-Safe Degradation:**
   - Repeat aggregate dashboard queries are cached in Redis with a 300-second (5-minute) TTL.
   - Cache keys:
     - `admin:reports:delivery_engagement:{from}:{to}:{category}:{locale}`
     - `admin:reports:binding_health:{from}:{to}`
   - Any Redis connection failure or serialization exception gracefully degrades to direct PostgreSQL query execution without raising an error to the caller (200 OK).

4. **Zero-PII Child Safety Invariant (Blueprint B-08 §25 / PRD §12.6):**
   - The service returns strictly numeric counts, aggregated breakdowns, conversion ratios, and latency percentiles.
   - Under no circumstances are individual child profiles, parent account identifiers, device tokens, or personal identifiers included in reporting responses.

5. **Positive Framing for Misdelivery Prevention (PRD §8 / Blueprint B-08 §10):**
   - Counts notifications safely suppressed at send-time because the active profile switched away (`cancellation_reason='binding_inactive'`).
   - Framed positively as `misdelivery_risk_events_prevented` (an integrity monitor signal mirroring B.15 duplicate prevention).
