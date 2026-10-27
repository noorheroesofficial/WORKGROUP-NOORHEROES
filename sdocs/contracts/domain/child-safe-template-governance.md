---
id: domain.child-safe-template-governance
kind: service
title: Child-Safe Notification Template Governance & Rendering Domain Service
status: stable
owner_story: TASK-B17-04
version: 1
created: 2026-10-09
---

## Service Definition

```python
class TemplateService(BaseService):
    """
    Service coordinating notification template lifecycle, safety governance, and rendering.
    (Feature B.17 / Blueprint B-04 Tasks 03 & 06)
    """

    def __init__(
        self,
        repository: TemplateRepository,
        validator: ChildSafetyBlocklistValidator,
        renderer: TemplateRenderer,
        redis: Optional[Redis] = None,
    ) -> None: ...

    async def create_template(
        self,
        notification_type: str,
        template_class: str,
        locale: str,
        body: str,
        title: Optional[str] = None,
        created_by: Optional[str] = None,
        **kwargs: Any,
    ) -> NotificationTemplate: ...

    async def get_template_by_id(self, template_id: str) -> NotificationTemplate: ...

    async def update_template(
        self,
        template_id: str,
        body: Optional[str] = None,
        title: Optional[str] = None,
        status: Optional[str] = None,
        **kwargs: Any,
    ) -> NotificationTemplate: ...

    async def archive_template(self, template_id: str) -> NotificationTemplate: ...

    async def delete_template(self, template_id: str) -> NotificationTemplate: ...

    async def list_templates(
        self,
        notification_type: Optional[str] = None,
        template_class: Optional[str] = None,
        locale: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[NotificationTemplate], int]: ...

    async def get_active_template_for_render(
        self,
        notification_type: Optional[str] = None,
        template_class: str = "child_facing",
        locale: str = "en",
        type: Optional[str] = None,
    ) -> Optional[NotificationTemplate]: ...

    async def render_copy(
        self,
        notification_type: Optional[str] = None,
        template_class: str = "child_facing",
        locale: str = "en",
        context: Optional[Dict[str, Any]] = None,
        type: Optional[str] = None,
    ) -> RenderResult: ...
```

---

## Content Safety Blocklist Validator (`ChildSafetyBlocklistValidator`)

```python
class ChildSafetyBlocklistValidator:
    """
    Enforces non-bypassable content governance rules on child-facing templates.
    (PRD FR-6, §12.1, §12.5, Blueprint B-04 Tasks 02 & §28)
    """

    def validate(
        self,
        body: str,
        template_class: str = "child_facing",
        title: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Validates body and title text against the prohibited terms blocklist.
        Raises BlocklistViolationError if template_class is 'child_facing' and any prohibited term is detected.
        Zero bypass for any admin role.
        """
        ...
```

### Prohibited Terms Catalog (49 Terms)

1. **Commercial, Billing, Pricing & Transactional (32 Terms)**:
   `subscribe`, `subscription`, `subscribing`, `price`, `pricing`, `billing`, `bill`, `renew`, `renewal`, `renewing`, `trial`, `free trial`, `payment`, `pay`, `charge`, `invoice`, `credit card`, `purchase`, `in-app purchase`, `iap`, `buy`, `upgrade`, `promo`, `discount`, `deal`, `cost`, `dollar`, `paywall`, `checkout`, `upsell`, `downsell`, `revenue`.

2. **Telemetry, Analytics & Engagement Metrics (17 Terms)**:
   `engagement score`, `engagement`, `retention rate`, `retention`, `churn`, `conversion rate`, `conversion`, `funnel dropoff`, `funnel`, `ltv`, `cohort`, `analytics`, `metrics`, `telemetry`, `monetization`, `monetise`, `monetize`, `arpu`.

---

## Template Renderer (`TemplateRenderer`)

```python
class RenderResult(BaseModel):
    title: Optional[str]
    body: str
    locale: str
    is_rtl: bool


class TemplateRenderer:
    """
    Placeholder substitution and multi-locale rendering engine.
    (Blueprint B-04 Task 04 & §21, §22)
    """

    def extract_placeholders(self, text: Optional[str]) -> List[str]: ...

    def validate_placeholders(
        self,
        notification_type: str,
        body: str,
        title: Optional[str] = None,
    ) -> List[str]: ...

    def render(
        self,
        body_template: str,
        context: Dict[str, Any],
        title_template: Optional[str] = None,
        locale: str = "en",
    ) -> RenderResult: ...

    def log_fallback(
        self,
        requested_locale: str,
        fallback_locale: str = "en",
        notification_type: str = "unknown",
    ) -> None: ...
```

---

## Template Repository (`TemplateRepository`)

```python
class TemplateRepository(BaseRepository[NotificationTemplate]):
    """
    Data access layer for notification copy templates with partial active index enforcement.
    """

    async def create_template(self, template: NotificationTemplate) -> NotificationTemplate: ...

    async def get_by_id(self, template_id: str) -> Optional[NotificationTemplate]: ...

    async def get_active_template(
        self,
        notification_type: str,
        template_class: str,
        locale: str,
    ) -> Optional[NotificationTemplate]: ...

    async def update_template(
        self,
        template_id: str,
        body: Optional[str] = None,
        title: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Optional[NotificationTemplate]: ...

    async def archive_template(self, template_id: str) -> Optional[NotificationTemplate]: ...

    async def list_templates(
        self,
        notification_type: Optional[str] = None,
        template_class: Optional[str] = None,
        locale: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[NotificationTemplate], int]: ...
```

---

## Domain Invariants & Rules

1. **Non-Bypassable Child Safety Gate (PRD FR-6, §12.1, §12.5)**:
   - Evaluated unconditionally on every creation and update of child-facing templates (`template_class='child_facing'`).
   - No parameter (`force`, `bypass`, `skip_validation`) can override the blocklist check under any admin role, including `superadmin`.
   - Parent-facing templates (`template_class='parent_facing'`) are exempt from commercial term filtering.

2. **Single Active Template Mutex (Blueprint B-04 §14, §18)**:
   - Exactly one active template per `(type, template_class, locale)`.
   - Enforced by database constraint `uq_notification_templates_active` and service-level pre-checks.
   - Collisions raise `DuplicateActiveTemplateError` (mapped to HTTP 409 Conflict).

3. **Placeholder Grammar & Required Variable Enforcement (Blueprint B-04 §13, §15)**:
   - Enforces `{{placeholder}}` syntax. Unbalanced or single braces raise `TemplatePlaceholderError` (HTTP 422).
   - Trigger-specific required placeholders (e.g. `streak_count` for `streak_risk` / `streak_at_risk`) must be present in the body.

4. **Multi-Locale Direction-Aware Rendering (Blueprint B-04 §21, §22)**:
   - Supports Canonical Locales: `en`, `ar`, `ur`, `hi`.
   - RTL indicator flag: Sets `is_rtl=True` when rendering `ar` (Arabic) or `ur` (Urdu) copy.
   - Graceful English Fallback: If a requested non-English localized active template is missing, automatically falls back to `locale='en'` while recording a structured warning log (`template_locale_fallback`).

5. **Redis Template Cache Layer (Blueprint B-04 §24)**:
   - Cached under key `notif:template:{notification_type}:{template_class}:{locale}` with a 1-hour TTL (`CACHE_TTL_SECONDS = 3600`).
   - Mutating operations (`create_template`, `update_template`, `archive_template`, `delete_template`) immediately invalidate the corresponding Redis key.
