---
id: domain.admin-notification-campaigns
kind: service
title: Notification Campaign & Segment Management Domain Service
status: stable
owner_story: TASK-B17-07
version: 1
created: 2026-10-09
---

## Service Definition

```python
class CampaignService(BaseService):
    async def create_campaign(
        self,
        arg1: Any = None,
        arg2: Any = None,
        *,
        template_id: Optional[str] = None,
        title: Optional[str] = None,
        segment_filters: Optional[Dict[str, Any]] = None,
        scheduled_at: Optional[datetime] = None,
        created_by: Optional[str] = None,
        admin_id: Optional[str] = None,
    ) -> NotificationCampaign: ...

    async def get_campaign(self, campaign_id: str) -> NotificationCampaign: ...

    async def list_campaigns(
        self,
        status: Optional[str] = None,
        template_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[NotificationCampaign], int]: ...

    async def update_campaign(
        self,
        campaign_id: str,
        request: Optional[CampaignUpdateRequest] = None,
        *,
        title: Optional[str] = None,
        template_id: Optional[str] = None,
        segment_filters: Optional[Dict[str, Any]] = None,
        scheduled_at: Optional[datetime] = None,
        admin_id: Optional[str] = None,
    ) -> NotificationCampaign: ...

    async def preview_campaign(
        self,
        campaign_id: str,
        locale: str = "en",
        sample_params: Optional[Dict[str, Any]] = None,
    ) -> CampaignPreviewResponse: ...

    async def test_send(
        self,
        campaign_id: str,
        test_recipients: List[str],
        locale: str = "en",
        admin_id: Optional[str] = None,
    ) -> NotificationCampaign: ...

    async def schedule(
        self,
        campaign_id: str,
        scheduled_at: Optional[datetime] = None,
        session: Optional[AsyncSession] = None,
        admin_id: Optional[str] = None,
    ) -> NotificationCampaign: ...

    async def cancel(
        self,
        campaign_id: str,
        reason: Optional[str] = "admin_canceled",
        admin_id: Optional[str] = None,
    ) -> NotificationCampaign: ...

    async def kill_switch(
        self,
        campaign_id: str,
        reason: Optional[str] = "emergency_kill_switch",
        admin_id: Optional[str] = None,
    ) -> NotificationCampaign: ...

    async def estimate_segment(
        self,
        arg1: Any = None,
        arg2: Any = None,
        *,
        filters: Optional[Dict[str, Any]] = None,
        session: Optional[AsyncSession] = None,
    ) -> SegmentEstimateResponse: ...


class SegmentBuilder:
    async def estimate(
        self,
        session: Optional[AsyncSession] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> SegmentEstimateResponse: ...

    async def resolve_recipients(
        self,
        session: Optional[AsyncSession] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[ResolvedRecipient]: ...
```

---

## 1. Domain Entities & Value Objects

```python
class ResolvedRecipient(BaseModel):
    parent_id: str
    target_child_id: Optional[str] = None
    target_type: str  # 'parent' | 'child'
    locale: str = "en"
    timezone: str = "UTC"


class NotificationCampaign(Base, TimestampMixin):
    __tablename__ = "notification_campaigns"

    campaign_id: str  # UUIDv7 PK
    template_id: str  # FK notification_templates.template_id
    title: str
    segment_filters: Optional[Dict[str, Any]]
    status: str  # 'draft' | 'scheduled' | 'sending' | 'sent' | 'canceled' | 'killed'
    scheduled_at: Optional[datetime]
    sent_at: Optional[datetime]
    total_recipients: int
    sent_count: int
    suppressed_count: int
    failed_count: int
    created_by: Optional[str]
```

---

## 2. Core Architectural Invariants

1. **Child Safety Blocklist Gate (PRD FR-6, Blueprint B-07 §10)**:
   - Any campaign targeting `child_facing` templates or audience `child`/`family` is strictly validated through `ChildSafetyBlocklistValidator`.
   - Prohibited marketing, subscription, and commercial terms reject campaign creation with `422 BlocklistViolationError`.
2. **Privacy-Preserving Segment Estimation (Blueprint B-07 §5/§10/§13)**:
   - `SegmentBuilder.estimate()` strictly returns aggregate counts (`estimated_families`, `estimated_children`, `estimated_devices`, `total_estimated_recipients`, `confidence`).
   - Zero child profile IDs, parent IDs, or individual records are ever leaked.
3. **Edge Case 9 Family-Wide Expansion (Blueprint B-07 §10/§27)**:
   - When `target_audience == "family"`, scheduling generates 1 parent intent (`target_binding="parent"`) plus 1 distinct intent for each active, non-archived child profile (`target_binding="child"`).
4. **No-Bypass Policy Engine Flow (Blueprint B-07 §25, PRD §12.5)**:
   - Campaign intents flow strictly through `NotificationIntentService` and downstream `PolicyEngine`.
   - Campaign notifications are policed identically to automated triggers (respecting quiet hours, bedtime windows, consent, and frequency budgets). There is NO unpoliced direct delivery bypass.
5. **Emergency Kill-Switch Immediacy (Blueprint B-07 §10/§18)**:
   - Triggers instantaneous revocation of both `pending` and `processing` intents via `cancel_by_campaign_id(include_processing=True)`.
   - Halts delivery worker pickups and moves campaign status to `'killed'`.
6. **Immutable Administrative Audit Records**:
   - Every mutating campaign operation (`create`, `update`, `schedule`, `test_send`, `cancel`, `kill_switch`) writes an immutable record to `admin_audit_records`.
7. **Draft Updating & State Machine Guard (Blueprint B-07 §8, §13, §18)**:
   - Campaign updates (`update_campaign`) are restricted exclusively to `draft` campaigns. Attempting updates on `scheduled`, `sending`, `sent`, `canceled`, or `killed` campaigns strictly raises `409 Conflict`.
8. **Transactional Savepoint Rollback on Schedule Failure (Blueprint B-07 §18)**:
   - Batch intent generation during `schedule()` is isolated within transactional savepoints (`async with session.begin_nested():`). Any database or dispatch failure rolls back partial intents completely, ensuring zero partial intent sets and leaving the campaign safely in `draft` state.
