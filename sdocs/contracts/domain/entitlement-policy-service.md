---
id: domain.entitlement-policy-service
kind: service
title: Entitlement & Download Policy Enforcement Service
status: stable
owner_story: TASK-B03
version: 1
created: 2026-09-29
---

## Service Definition

```python
class EntitlementPolicyService(BaseService):
    async def check_download_allowed(
        self,
        child_id: str,
        content_id: str,
        incoming_bytes: int = 0,
    ) -> PolicyDecision: ...

    async def resolve_effective_cap(
        self,
        child_id: str,
        plan_code: Optional[str] = None,
    ) -> int: ...

    async def is_content_withdrawn(
        self,
        content_id: str,
    ) -> bool: ...

    async def invalidate_policy_cache(
        self,
        child_id: Optional[str] = None,
    ) -> None: ...
```

---

## 1. Domain Types

```python
@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: Optional[str] = None
    effective_cap_bytes: int = 0
    current_usage_bytes: int = 0
    remaining_bytes: int = 0

    @property
    def usage_bytes(self) -> int:
        return self.current_usage_bytes

    @property
    def limit_bytes(self) -> int:
        return self.effective_cap_bytes
```

---

## 2. Decision Codes & Reason Mappings

| Reason Code | HTTP Status | Description |
|---|---|---|
| `None` (allowed=True) | 200 | All policy gates passed; download manifest can be issued. |
| `DOWNLOADS_DISABLED_BY_PARENT` | 403 | Gate 1 failure: Parental control policy revoked offline downloads for child. |
| `ENTITLEMENT_REQUIRED` | 403 | Gate 2 failure: Content requires an active subscription tier not possessed by family. |
| `DOWNLOAD_CAP_REACHED` | 403 | Gate 3 failure: `current_usage_bytes + incoming_bytes > effective_cap_bytes`. |

---

## 3. Core Architectural Invariants

1. **Deterministic 3-Tier Precedence Evaluation (Blueprint B-03 §10)**:
   - **Gate 1 (Parental Lockout Gate)**: If parent controls have disabled downloads for child, reject immediately with `DOWNLOADS_DISABLED_BY_PARENT`.
   - **Gate 2 (Subscription Entitlement Gate)**: If content tier exceeds family subscription entitlement, reject with `ENTITLEMENT_REQUIRED`.
   - **Gate 3 (Storage Cap Gate)**: If storage usage plus incoming media size exceeds effective cap, reject with `DOWNLOAD_CAP_REACHED`.
2. **Authoritative Cap Resolution Precedence (Blueprint B-03 §10, B-08 §10)**:
   - 1st: Parent-configured custom cap (`C.23`).
   - 2nd: Admin subscription tier default cap (`downloads_default_cap_config`).
   - 3rd: Global admin default cap (`plan_code = 'default'`).
   - 4th: System hardcoded fallback (1 GiB = 1,073,741,824 bytes).
3. **Strict Non-Destructive Cap Decrease Invariant (PRD §1.10 Edge Case 4, Blueprint B-03 §5 / §10)**:
   - If a parent lowers the download cap below current usage, existing completed downloads are **never deleted or invalidated**.
   - Existing downloads remain fully playable offline. Only new download attempts are rejected until usage drops below the new cap.
4. **Strict Non-Retroactive Admin Default Cap Invariant (PRD §12.5, Blueprint B-08 §10 / §27)**:
   - Modifications to admin plan defaults NEVER alter or overwrite parent-configured custom caps.
5. **Short-TTL Redis Fast-Path Caching (Blueprint B-03 §10 / §24)**:
   - Decisions cached in Redis with a 30-second TTL (`downloads:policy:{child_id}`).
   - Direct cache invalidation hooks (`invalidate_policy_cache`) executed on parent cap writes or admin default updates.
   - Redis connectivity outages fall through gracefully to direct database queries without failing.
