# B-03 — Entitlement & Download Policy Enforcement Service

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). The internal policy-decision service that B-01 (manifest issuance) and B-06 (periodic refresh) both call — the single source of truth for "is this child allowed to download this content right now," combining the parent's custom cap/policy (owned by C.23) with the admin-configured plan default (owned by N-03/B-08).

## 2. Parent Feature
B.15 — Offline Downloads & Sync

## 3. Sub-feature
B-03 — Entitlement & Download Policy Enforcement Service

## 4. Objective
Implement `EntitlementPolicyService` as an internal service (no public router of its own) providing `check_download_allowed(child_id, content_id) -> PolicyDecision` and `resolve_effective_cap(child_id) -> int`, combining parent-set cap/disabled-flag (C.23) with admin plan defaults (B-08), enforcing the non-destructive cap-decrease rule.

## 5. Business Requirements
- FR-3: per-child download cap set by parent; exceeding it blocks new downloads with a clear message.
- FR-5: withdrawn content becomes unavailable after the next policy/entitlement refresh while safe progress history is preserved.
- Edge Case 4: parent reduces cap below current usage → existing downloads are not forcibly deleted; no new downloads permitted until usage drops under the new cap.
- Edge Case 11: parental controls disable downloads entirely for a child while existing downloads exist → existing downloads remain playable (two distinct controls: disable-new vs. revoke-existing), only new attempts blocked.
- §9 Admin AI Prompt item 3: admin default-cap changes affect only future defaults, never retroactively overriding a parent's already-configured custom cap.

## 6. Existing Architecture
Internal service module within the new `downloads` bounded context — `src/noorheroes/modules/downloads/policy.py` — deliberately **not** its own router/bounded-context, since it has no independent public API surface; it is a pure decision service consumed by B-01 and B-06. Reads the parent-cap table owned by C.23's Parental Controls context and the plan-default table owned by B-08, without duplicating either as its own source of truth.

## 7. Existing Code to Reuse
- `infrastructure/redis.py` → `get_redis_pool()` for short-TTL policy-decision caching.
- `common/base_service.py` → `BaseService` pattern for consistency, even though this service has no router.
- C.23's parent-cap repository (read-only reference, not duplicated).
- B-08's plan-default-cap repository (read-only reference).
- `subscriptions` module's `SubscriptionService.get_entitlement()` — for plan-tier resolution when no custom parent cap is set.

## 8. Files to Create
- `src/noorheroes/modules/downloads/policy.py` — `EntitlementPolicyService`, `PolicyDecision` (dataclass: `allowed: bool`, `reason: Optional[str]`, `usage_bytes: int`, `limit_bytes: int`).
- `tests/modules/downloads/test_policy_enforcement.py`.
- `tests/modules/downloads/test_cap_decrease_non_destructive.py`.

## 9. Files to Modify
- `modules/downloads/service.py` (B-01) — inject `EntitlementPolicyService`, call `check_download_allowed()` before manifest issuance.
- `modules/downloads/repository.py` (B-01) — add `sum_storage_used()` reuse for cap comparison (shared with B-02).

## 10. Backend Requirements
- `resolve_effective_cap(child_id)`: parent-custom cap (C.23) if explicitly set, else the admin plan default (B-08) for the family's current subscription tier.
- `check_download_allowed(child_id, content_id)`: returns `allowed=False, reason='DOWNLOAD_CAP_REACHED'` if `sum_storage_used(child_id) >= effective_cap` **and** this is a genuinely new download (not a re-request for already-`complete` content, which B-01 handles before ever calling this).
- Returns `allowed=False, reason='DOWNLOADS_DISABLED_BY_PARENT'` if C.23's `downloads_disabled` flag is set for the child — checked independently of, and before, the cap check.
- Returns `allowed=False, reason='ENTITLEMENT_REQUIRED'` if the content isn't within the family's active entitlement (delegates to `SubscriptionService`/`ContentService` for the actual entitlement lookup).
- Cap-decrease handling: this service never deletes or invalidates `download_record` rows — it only ever affects the outcome of a **new** `check_download_allowed()` call, never touches existing rows.
- Withdrawn-content flagging: exposes `is_content_withdrawn(content_id)` (delegates to `content` module) so B-06's refresh job can flag rather than delete affected `download_record` rows.
- Policy decision cached in Redis with a short TTL (e.g., 30s), keyed `(child_id,)`, invalidated on any parent-cap or admin-default-cap write (via an outbox-consumed cache-bust, or a direct cache-clear call from C.23/B-08's write paths).

## 11. KMP Requirements
No direct KMP consumer — this service is only reachable via B-01/B-06's public contracts.

## 12. NextJS Requirements
No direct NextJS consumer — B-08 writes the plan-default table this service reads; N-01/N-02 read aggregate outcomes, not this service directly.

## 13. API Contract
No public HTTP endpoint — internal service interface only:
```python
async def check_download_allowed(child_id: str, content_id: str) -> PolicyDecision: ...
async def resolve_effective_cap(child_id: str) -> int: ...
async def is_content_withdrawn(content_id: str) -> bool: ...
```

## 14. Database Requirements
Reads (does not own): C.23's parent-cap/disabled-flag table, B-08's `downloads_default_cap_config` table, `content` module's withdrawal flag, `download_record` (B-01, for usage sum). Owns no table of its own.

## 15. Validation
`child_id`/`content_id` validated as UUIDs by the callers (B-01/B-06); this internal service assumes caller-validated input, consistent with the platform's layer-boundary convention (validation lives at the API/schema layer, not re-validated in internal services).

## 16. Authentication
N/A — internal service, not directly exposed; inherits the auth context of its caller (B-01/B-06).

## 17. Authorization
N/A directly — authorization is enforced by callers' `Depends(get_current_child)`/scheduled-job context; this service trusts the `child_id` it's given by an already-authorized caller.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Redis cache failure | Fall through to direct DB read for cap/disabled-flag — never fail-open on enforcement |
| C.23 parent-cap table read failure | Propagate as a service-level error; B-01 surfaces `500`, never silently allows the download |
| No custom parent cap set | Falls back to admin plan default from B-08, never an unlimited/unbounded default |
| Content already withdrawn | `check_download_allowed` still evaluates cap/entitlement normally; withdrawal-flagging is B-06's separate concern |

## 19. Offline First
N/A (backend internal service).

## 20. Local Data
N/A (backend).

## 21. Localization
N/A — `reason` codes are machine-readable enums; user-facing copy is rendered client-side (K-01) from localized strings keyed by the reason code.

## 22. RTL
N/A.

## 23. Analytics
No direct analytics emission — B-01's outbox events carry the `reason` for B-07's cap-rejection-rate metric.

## 24. Performance
- Redis-cached policy decision keeps B-01's manifest-issuance p95 low, since this check runs on every manifest request.
- `sum_storage_used()` query indexed on `(child_id, status)`.
- Cache invalidation is targeted (single `child_id` key), never a full-cache flush, to avoid a thundering-herd re-computation.

## 25. Security
- This is the sole enforcement point for the cap/disabled-flag/entitlement decision — B-01 has no independent cap-checking logic, preventing enforcement drift between two code paths.
- Cache-invalidation-on-write is mandatory for any C.23/B-08 mutation path — a stale cached "allowed" decision past a parent's cap-decrease or downloads-disabled toggle is a security-relevant staleness bug, tested explicitly (§27).

## 26. Library Requirements
FastAPI (internal, no router), SQLAlchemy 2.0 (async), Redis. No new libraries.

## 27. Testing
- Unit: under-cap allowed, at-cap rejected with correct `usage_bytes`/`limit_bytes`.
- Unit: `downloads_disabled` flag rejects independently of cap state (distinct `reason` code).
- Unit: cap-decrease scenario — existing `download_record` rows untouched; only new `check_download_allowed()` calls affected (Edge Case 4, dedicated test file).
- Unit: no custom parent cap → falls back to admin plan default correctly.
- Integration: Redis cache invalidation on a C.23 cap-write and a B-08 default-cap-write both correctly bust the cached decision within the TTL window.

## 28. Documentation
Docstrings on `PolicyDecision` explaining each `reason` code's exact meaning and which client-facing message it maps to (documented for K-01's consumption, even though this service has no public API doc surface).

## 29. AI Coding Agent Implementation Steps
**Task 01 — Define PolicyDecision & Service Skeleton**
Objective: `PolicyDecision` dataclass, `EntitlementPolicyService` class shell.
Files to create: `modules/downloads/policy.py`.

**Task 02 — Implement resolve_effective_cap()**
Objective: parent-custom-cap-or-admin-default resolution.
Existing code to reuse: C.23 parent-cap repository, B-08 plan-default repository.

**Task 03 — Implement check_download_allowed()**
Objective: disabled-flag check → entitlement check → cap check, in that order, each with a distinct `reason` code.
Business rules: cap-decrease never mutates existing rows.

**Task 04 — Implement Redis Caching & Invalidation**
Objective: short-TTL cache on the policy decision; invalidation hooks callable from C.23/B-08 write paths.
Files to modify: C.23's cap-write path, B-08's default-cap-write path (add cache-bust call).

**Task 05 — Wire into B-01 and B-06**
Files to modify: `modules/downloads/service.py`.

**Task 06 — Add Cap-Decrease Non-Destructive Test (highest priority)**
Tests: `test_cap_decrease_non_destructive.py`.
Definition of done: CI-blocking gate.

**Task 07 — Add Full Test Suite**

**Task 08 — Final Code Review**
Objective: confirm B-01 has zero independent cap-checking logic (single enforcement point verified by code inspection).

## 30. Definition of Done
- `EntitlementPolicyService` fully implemented and wired into B-01/B-06.
- Cap-decrease non-destructive guarantee verified by test.
- Downloads-disabled vs. cap-reached correctly distinguished.
- Cache invalidation verified on both C.23 and B-08 write paths.

## 31. Final Verification Checklist
- [ ] Single enforcement point — no duplicate cap logic in B-01.
- [ ] Cap-decrease never deletes/invalidates existing `download_record` rows.
- [ ] `downloads_disabled` and `cap_reached` are distinct, independently-testable reason codes.
- [ ] Redis failure falls through to direct DB read, never fail-open.
- [ ] Cache invalidated correctly on parent-cap and admin-default-cap writes.
- [ ] No PostgreSQL/Redis credentials modified.
