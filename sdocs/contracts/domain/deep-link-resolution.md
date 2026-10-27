---
id: domain.deep-link-resolution
kind: service
title: Deep Link Resolution Domain Service Interface
status: stable
owner_story: TASK-B17-06
version: 1
created: 2026-10-09
---

## Service Definition

```python
class DeepLinkResolutionService(BaseService):
    def __init__(
        self,
        delivery_repository: NotificationDeliveryRepository,
        intent_repository: NotificationIntentRepository,
        delivery_adapter: Optional[DeliveryAdapter] = None,
        outbox: Optional[OutboxWriter] = None,
        content_availability_checker: Optional[Callable[[str], Awaitable[bool]]] = None,
        clock: Optional[Clock] = None,
    ) -> None: ...

    async def resolve(
        self,
        deep_link_token: str,
        caller_context: Optional[DeviceCallerContext] = None,
        session_valid: bool = True,
    ) -> DeepLinkResolveResponse: ...
```

---

## 1. Domain Types & Schemas

```python
class DeepLinkResolveResponse(BaseSchema):
    valid: bool
    destination: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    reason: Optional[str] = None  # 'child_mismatch' | 'content_unavailable' | 'requires_lock_gate' | 'session_expired'
    fallback_destination: Optional[str] = None  # 'who_is_learning' | 'home' | 'parent_gate' | 'login'
    delivery_id: Optional[str] = None
```

---

## 2. Default Destination Routes by Canonical Class (PRD FR-1, FR-12, FR-13)

| Notification Trigger Type | Default Navigation Destination | Target Bounded Context |
|---|---|---|
| `streak_risk` / `streak_at_risk` | `habit_builder` | A.7 Habit Tracker |
| `daily_reminder` / `daily_reminder_due` | `home` | A.2 Home Hub |
| `bedtime_story` / `bedtime_story_due` | `bedtime_player` | A.4 Bedtime Mode |
| `content_published` / `new_content` | `story_player` | A.3/A.6 Story Player |
| `reward_posted` / `reward_milestone` | `rewards_wallet` | A.11 Rewards & Achievements |
| `seasonal_event` | `ramadan_hub` | Seasonal Campaign Hub |
| `in_app_banner` | `home` | A.2 Home Hub |

---

## 3. Parent-Gated Destinations Catalog

Destinations strictly requiring Parent Gate / PIN lock verification before child entry:
- `parent_dashboard`
- `parent_settings`
- `billing`
- `subscriptions`
- `parent_area`
- `parent_support`
- `account_settings`

---

## 4. Domain Events Published

```python
class NotificationDeepLinkResolved(DomainEvent):
    deep_link_token: str
    delivery_id: Optional[str] = None
    valid: bool
    destination: Optional[str] = None
    reason: Optional[str] = None
    fallback_destination: Optional[str] = None
    intended_child_id: Optional[str] = None
    caller_child_id: Optional[str] = None
```

---

## 5. Domain Dependencies & Integration Invariants

1. **Downstream Service Integration (`domain.delivery-adapter`)**:
   - Depends on `DeliveryAdapter.mark_opened(delivery_id)` to mutate `notification_deliveries.opened_at` upon valid resolution (`valid=True`).
   - If `delivery_adapter` is not injected, falls back directly to `NotificationDeliveryRepository.mark_opened(delivery_id)`.
2. **P0 Sibling Access Isolation (PRD §5 Item 5, Edge Case 2)**:
   - When `caller_context.mode == 'child'` and `caller_context.child_id != intended_child_id`, resolution strictly returns `valid=False, reason='child_mismatch', fallback_destination='who_is_learning'`.
   - Never leaks private child progress or content, and explicitly suppresses updating `opened_at` to avoid false conversion counts.
3. **Withdrawn Content Graceful Degradation (PRD Edge Case 4)**:
   - Integrates with destination service availability hooks (`content_availability_checker`).
   - If content is withdrawn/archived, returns `valid=False, reason='content_unavailable', fallback_destination='home'` with zero client crashes.
4. **Clean Architecture Layer Isolation**:
   - Outbox events (`NotificationDeepLinkResolved`, `NotificationOpened`) are emitted through `OutboxWriter` within the transactional unit of work.
