# B-04 — AI Feature Kill Switch Service

## 1. Feature Context
Parent PRD: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
Depends on: E.28 (RBAC, shared audit log), `infrastructure/redis_client.py` (nearest existing fast-propagation primitive)
Feeds into: N-04 (Kill Switch Console); A.5's existing graceful-degradation fallback (consumer, out of this document's scope)

## 2. Parent Feature
E.30 — AI Moderation Console & Safety Evaluation Harness

## 3. Sub-feature
**AI Feature Kill Switch Service** (ID: B-04) — remote, platform-wide, sub-60-second AI feature suspension/reinstatement, restricted to safety roles only. Alongside B-02's audited transcript gate, this is one of the two highest-priority guarantees in the entire E.30 service (backend AI code-gen prompt, item 4).

## 4. Objective
Let a safety-role admin suspend a specific AI capability platform-wide within 60 seconds, and reinstate it, with every action rejected at the service layer for non-safety roles (never merely hidden in the UI) and fully audited.

## 5. Business Requirements
- FR-9: a kill switch exists at the feature level, remote-activatable; activation must take effect platform-wide within the §1.4 latency target, not merely flip a flag that propagates on its own schedule.
- §1.4: kill-switch activation-to-effect latency ≤ 60 seconds — **hard requirement**, not best-effort.
- Edge Case 3: a kill switch activated mid-session for an actively-using child → graceful fallback to non-AI/listen-only mode on the next app-state check (A.5's own pattern; this service's job ends at "the flag is observably suspended within 60s," not the client-side fallback UI itself).
- Edge Case 8: `suspend_feature` attempted by a non-safety role → rejected at the service layer, actually rejected via direct API call, not merely hidden in the UI.
- §10 DevOps: any kill-switch activation is itself a P0 incident-severity event, alert regardless of root cause; alert if measured propagation latency exceeds 60s in production.

## 6. Existing Architecture
New standalone service within the `ai_moderation` context (or a dedicated `kill_switch` submodule if propagation logic grows large enough to warrant isolation — start co-located, per FAST-API-INSTRUCTIONS.md §14's incremental-feature guide, and extract only if it later needs independent scaling). Builds directly on `infrastructure/redis_client.py`'s existing Redis-shaped interface.

## 7. Existing Code to Reuse
- `infrastructure/redis_client.py::get_redis_pool()` / `InMemoryRedisLike` — extended per §10.2 with `publish`/`subscribe`/`smembers`/`sadd`/`srem` alongside the existing `setex`/`exists`/`delete`; note its own docstring: "No Redis instance is configured in this sandbox environment... Swap `InMemoryRedisLike` for a real Redis client in production without changing call sites" — this service is built against that same interface contract so swapping in `redis.asyncio.Redis` requires no call-site changes, only a real shared Redis instance to point at.
- `require_admin_scope()` (`core/deps.py`)
- `OutboxWriter` for audit-adjacent domain events
- `AdminService.log_action()` pattern (E.28/E.29 precedent) for the dual-write to the shared audit log

## 8. Files to Create
- `src/noorheroes/modules/ai_moderation/kill_switch_models.py` → `KillSwitchEvent` ORM model
- `src/noorheroes/modules/ai_moderation/kill_switch_schemas.py` → `KillSwitchActionResponse`, `ActiveSuspensionsResponse`
- `src/noorheroes/modules/ai_moderation/kill_switch_service.py` → `KillSwitchService(BaseService)`
- `src/noorheroes/modules/ai_moderation/suspension_cache.py` → `AiFeatureSuspensionCache` per §10.2 (pub/sub + reconciliation-poll)
- `src/noorheroes/modules/ai_moderation/kill_switch_api.py` → `KillSwitchRouter`
- `alembic/versions/xxxx_add_kill_switch_event.py`
- `tests/modules/ai_moderation/test_kill_switch_latency.py`
- `tests/modules/ai_moderation/test_kill_switch_role_restriction.py`
- `tests/modules/ai_moderation/test_suspension_cache_reconciliation.py` → proves a dropped pub/sub message still self-corrects within `RECONCILIATION_POLL_SECONDS`

## 9. Files to Modify
- `main.py` → mount `KillSwitchRouter` under `/v1/admin/ai-features`, and register `AiFeatureSuspensionCache.start()`/`.stop()` in the app `lifespan` per §10.2
- `src/noorheroes/infrastructure/redis_client.py` → add a `publish`/`subscribe` pair to the Redis-shaped interface (see §10.2's `AiFeatureSuspensionCache` design) — `InMemoryRedisLike` gets an in-process pub/sub stand-in for local dev/test; production swaps in `redis.asyncio.Redis`'s real pub/sub, same call sites

## 10. Backend Requirements

### 10.1 Model
```python
class KillSwitchEvent(Base):
    __tablename__ = "kill_switch_event"
    __table_args__ = (
        CheckConstraint("action IN ('suspend','reinstate')", name="ck_kill_switch_action"),
        Index("ix_kill_switch_feature_time", "ai_feature", "occurred_at"),
    )
    # append-only

    event_id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_ulid)
    ai_feature: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)
    actor_admin_id: Mapped[str] = mapped_column(String, ForeignKey("admin_account.admin_id"))
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
```

### 10.2 Propagation Mechanism — the Latency-Critical Path (resolved design)

`infrastructure/redis_client.py`'s current `InMemoryRedisLike` is a **single-process** in-memory dict — it cannot itself provide multi-instance propagation, per its own docstring ("no Redis instance is configured in this sandbox environment"). The design below is grounded in two things the PRD suite already states rather than an invented mechanism: E.30 PRD §10 DevOps's own suggestion of "a fast pub/sub or distributed-cache invalidation mechanism," and F.35's Edge Case 7, which explicitly places this kill switch in "the platform's general feature-flag-based kill-switch philosophy." A **pub/sub broadcast backing a per-instance in-memory cache, with a bounded reconciliation poll as a fallback against a missed message**, is the standard implementation of exactly that philosophy — this section commits to that design rather than leaving it open.

```python
SUSPENSION_KEY_PREFIX = "ai_feature:suspended:"
SUSPENSION_CHANNEL = "ai_feature_suspension_events"
RECONCILIATION_POLL_SECONDS = 15  # << 60s SLA, catches any instance that missed the pub/sub message

class AiFeatureSuspensionCache:
    """Runs once per service instance (started in the app `lifespan`). Holds
    the authoritative-for-this-instance in-memory suspension set, kept in
    sync two ways: (1) an active Redis pub/sub subscription for near-
    instant updates, and (2) a bounded reconciliation poll against the
    Redis key set, so a single dropped pub/sub message can never leave an
    instance permanently stale beyond RECONCILIATION_POLL_SECONDS."""

    def __init__(self, redis):
        self.redis = redis
        self._suspended: set[str] = set()

    def is_suspended(self, feature: str) -> bool:
        return feature in self._suspended  # in-process read, zero latency — this is what F.35's
                                            # consuming services actually check per request (§10.4)

    async def start(self) -> None:
        self._suspended = set(await self.redis.smembers(f"{SUSPENSION_KEY_PREFIX}active"))
        asyncio.create_task(self._subscribe_loop())
        asyncio.create_task(self._reconciliation_loop())

    async def _subscribe_loop(self) -> None:
        async for message in self.redis.subscribe(SUSPENSION_CHANNEL):
            feature, action = message["feature"], message["action"]
            if action == "suspend":
                self._suspended.add(feature)
            elif action == "reinstate":
                self._suspended.discard(feature)

    async def _reconciliation_loop(self) -> None:
        while True:
            await asyncio.sleep(RECONCILIATION_POLL_SECONDS)
            self._suspended = set(await self.redis.smembers(f"{SUSPENSION_KEY_PREFIX}active"))


class KillSwitchService(BaseService):
    def __init__(self, redis, event_repo: "KillSwitchEventRepository"):
        self.redis = redis  # get_redis_pool() — same interface InMemoryRedisLike exposes, extended with publish/smembers/sadd/srem
        self.event_repo = event_repo

    async def suspend(self, feature: str, admin_ctx: AdminSessionContext) -> dict:
        self._require_safety_role(admin_ctx)
        await self.redis.sadd(f"{SUSPENSION_KEY_PREFIX}active", feature)          # source of truth for reconciliation
        await self.redis.publish(SUSPENSION_CHANNEL, {"feature": feature, "action": "suspend"})  # fast path
        await self.event_repo.add(KillSwitchEvent(ai_feature=feature, action="suspend", actor_admin_id=admin_ctx.admin_id))
        return {"ai_feature": feature, "status": "suspended"}

    async def reinstate(self, feature: str, admin_ctx: AdminSessionContext) -> dict:
        self._require_safety_role(admin_ctx)
        await self.redis.srem(f"{SUSPENSION_KEY_PREFIX}active", feature)
        await self.redis.publish(SUSPENSION_CHANNEL, {"feature": feature, "action": "reinstate"})
        await self.event_repo.add(KillSwitchEvent(ai_feature=feature, action="reinstate", actor_admin_id=admin_ctx.admin_id))
        return {"ai_feature": feature, "status": "active"}

    def _require_safety_role(self, admin_ctx: AdminSessionContext) -> None:
        SAFETY_SCOPES = {"child_safety_reviewer", "super_admin"}
        if not SAFETY_SCOPES.intersection(admin_ctx.scopes):
            raise AuthorizationError(
                "Only safety roles may suspend or reinstate an AI feature.",
                ai_feature="",
            )
```

**Why both paths, not just pub/sub alone:** pub/sub delivers near-instant propagation but Redis pub/sub messages are fire-and-forget — an instance that is mid-restart or briefly disconnected at the moment of publish will simply never receive that message. The `_reconciliation_loop`'s `RECONCILIATION_POLL_SECONDS = 15` bound guarantees every instance self-corrects well inside the 60-second SLA even in that worst case, without requiring Redis Streams/consumer-group delivery guarantees the project doesn't otherwise use.

**Remaining infrastructure dependency (genuinely external, not invented):** this design still requires a **real, shared Redis instance** in every non-sandbox environment — `InMemoryRedisLike`'s in-process dict cannot back a `publish`/`subscribe` channel across separate OS processes/containers no matter how the call sites are written. Provisioning that shared Redis instance is an infrastructure/DevOps task tracked in §10 DevOps below, not a code-design gap; the `publish`/`subscribe`/`smembers`/`sadd`/`srem` interface this service is written against is what makes swapping the sandbox stand-in for a real Redis client a non-call-site-changing operation once that instance exists.

### 10.3 Endpoints
| Method | Path | Auth | Purpose |
|---|---|---|---|
| POST | `/v1/admin/ai-features/{feature}/suspend` | Safety roles only | Suspend an AI feature platform-wide |
| POST | `/v1/admin/ai-features/{feature}/reinstate` | Safety roles only | Reinstate a suspended feature |
| GET | `/v1/admin/ai-features/active-suspensions` | `ai-moderation:read` | List currently-suspended features (Screen 6) |

### 10.4 Consuming-Side Check (contract, not built here)
Every AI-touching service instance (F.35's pipeline services) must call `AiFeatureSuspensionCache.is_suspended(feature)` — the in-process, zero-latency read backed by §10.2's pub/sub-plus-reconciliation cache — **before** serving that feature to a child. B-04 owns and ships the `AiFeatureSuspensionCache` class itself (since it's the same propagation mechanism this module's own suspend/reinstate endpoints publish to); F.35's pipeline services are the consumers that instantiate and query it, not reimplement it.

## 11. KMP Requirements
Not applicable to this backend service directly — A.5's own KMP blueprint owns the client-side graceful-degradation response to an observed suspension (Edge Case 3), not duplicated here.

## 12. NextJS Requirements
Consumed by N-04 (AI Feature Kill Switch Console) for suspend/reinstate/active-list.

## 13. API Contract

### `POST /v1/admin/ai-features/{feature}/suspend`
- **Auth:** Safety roles only (`child_safety_reviewer`, `super_admin`)
- **Response 200:** `{ "ai_feature": "pronunciation_coaching", "status": "suspended" }`
- **Response 403:** rejected for any other role, even one with general `ai-moderation:read` access

### `POST /v1/admin/ai-features/{feature}/reinstate`
- Same auth; `{ "status": "active" }`

### `GET /v1/admin/ai-features/active-suspensions`
- **Response 200:** `{ "items": [ { "ai_feature", "suspended_at", "suspended_by" } ] }`

## 14. Database Requirements
- `kill_switch_event`: append-only; FK `actor_admin_id`; CHECK `action IN ('suspend','reinstate')`; index `(ai_feature, occurred_at DESC)` per §4.2.
- Retained at the platform's highest safety-audit durability tier (§10 DevOps).

## 15. Validation
`feature` path param validated against a known AI-feature registry (do not accept arbitrary strings that don't correspond to a real F.35-registered capability — confirm the registry source rather than inventing one).

## 16. Authentication
`Depends(get_current_admin)`.

## 17. Authorization
Hard-coded safety-role check (`child_safety_reviewer`, `super_admin`) per §10.2's `_require_safety_role` — **not** a generic `require_admin_scope()` call, since this restriction is narrower and more severity-class-specific than a normal scope check; keep it as an explicit, readable, separately-tested guard given its P0 severity.

## 18. Error Handling
| Scenario | Response |
|---|---|
| Non-safety role attempts suspend/reinstate | `403 FORBIDDEN`, rejected even for roles with general `ai-moderation:read` |
| Suspend-of-already-suspended | Idempotent no-op, `200` |
| Reinstate-of-already-active | Idempotent no-op, `200` |
| Unknown `feature` value | `404 NOT_FOUND` or `422`, per the confirmed feature registry |
| Redis unavailable | Fail **loudly** (5xx) — never silently succeed with an unpropagated suspension, since a false "suspended" success while propagation actually failed is a worse safety failure than a visible error |

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
Not applicable server-side.

## 22. RTL
Not applicable to backend.

## 23. Analytics
`ai_moderation_kill_switch_activated`, `ai_moderation_kill_switch_reinstated` (§1.19). DevOps-side (not analytics): P0 alert on every activation; alert on propagation latency exceeding 60s.

## 24. Performance
The entire point of this sub-feature **is** its latency guarantee — see §27's signature test. No other performance concern is more important here.

## 25. Security
- Role-restriction is enforced at the service layer, verified by direct API call in tests, not just UI absence (N-04 handles the UI-absence layer separately).
- Fail-loud-on-Redis-unavailable (§18) is itself a security/safety design choice: a silent false-positive "suspended" state is unacceptable.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Alembic, Pydantic v2, `redis.asyncio` (production; `InMemoryRedisLike` extended with an in-process pub/sub stand-in for local dev/test, per existing convention), pytest-asyncio, `fakeredis`'s async pub/sub support (or an equivalent lightweight multi-instance test harness) for the latency test — chosen specifically because it can simulate two independent "instances" subscribing to the same channel without standing up a real Redis container in CI; use a real `redis.asyncio.Redis` against a CI-provisioned Redis service container instead if the project's existing test infra already runs one for other suites (check before introducing `fakeredis` as a new test dependency).

## 27. Testing
- **Signature test 1 (CI-blocking, backend AI code-gen prompt item 4a):** two simulated instances, each running its own `AiFeatureSuspensionCache`, subscribed to the same channel; suspend via one instance's `KillSwitchService`, assert the *other* instance's `is_suspended()` flips to `True` well under the 60-second SLA via the pub/sub fast path.
- **Signature test 1b (CI-blocking companion — the reconciliation fallback):** simulate a dropped pub/sub message (subscribe callback intentionally skipped for one instance), assert that instance's `is_suspended()` still flips to `True` within `RECONCILIATION_POLL_SECONDS` via the poll loop alone — this is what actually proves the 60-second SLA holds even in the pub/sub-message-lost case, not just the happy path.
- **Signature test 2 (CI-blocking, item 4b):** confirm this endpoint is rejected for any role other than the designated safety roles, even a role with general AI-moderation queue access.
- Unit: idempotent double-suspend / double-reinstate (both the Redis `SADD`/`SREM` set operations and the in-memory cache are naturally idempotent — assert this explicitly rather than assuming it).
- Unit: dual-write to `kill_switch_event` and E.28's shared audit log.
- Integration: suspend → verify flag observable from a second simulated instance within SLA (both via pub/sub and, separately, via reconciliation-only) → reinstate → verify cleared on both paths.

## 28. Documentation
Export OpenAPI; explicitly document the 60-second SLA, the safety-role restriction, and the fail-loud-on-infrastructure-failure behavior.

## 29. AI Coding Agent Implementation Steps
- **Task 01 — Confirm AI-feature registry source** (F.35 defines 5 coarse services, not finer-grained toggles like "pronunciation_coaching" that the PRD's own mockup names — this granularity mismatch is a genuinely open question, still not resolved by this pass; confirm with Product/F.35 owners before hardcoding valid `feature` values, per §15).
- **Task 02 — Model & Migration**: `KillSwitchEvent`, append-only, per §14.
- **Task 03 — Extend the Redis-shaped interface**: add `publish`/`subscribe`/`smembers`/`sadd`/`srem` to `infrastructure/redis_client.py`, with an in-process pub/sub stand-in on `InMemoryRedisLike` for local dev/test.
- **Task 04 — `AiFeatureSuspensionCache`**: pub/sub subscriber + reconciliation-poll loop per §10.2, started in the app `lifespan`.
- **Task 05 — Service**: `KillSwitchService.suspend()`/`.reinstate()` with hard-coded safety-role guard, publishing to `AiFeatureSuspensionCache`'s channel.
- **Task 06 — Router**: suspend/reinstate/active-list endpoints.
- **Task 07 — Provision a real shared Redis instance** in every non-sandbox environment (infrastructure/DevOps task, tracked in §10 — the code-level design in §10.2 is complete, but it has nothing to propagate across without this).
- **Task 08 — Latency signature tests**: both the pub/sub-fast-path test and the dropped-message/reconciliation-fallback test per §27.
- **Task 09 — Role-restriction signature test**.
- **Task 10 — Idempotency and dual-audit tests**.
- **Task 11 — DevOps wiring**: P0 alert hook on activation; latency-exceeded alert.
- **Task 12 — Documentation**.
- **Task 13 — Final Code Review**: confirm the fail-loud-on-Redis-failure behavior is actually exercised in a test (kill the Redis connection mid-test, confirm 5xx not silent success), and confirm the reconciliation loop's poll interval is genuinely well inside the 60-second SLA with margin for the poll's own execution time.

## 30. Definition of Done
Suspend/reinstate implemented with hard safety-role restriction; propagation mechanism is a concrete pub/sub-plus-reconciliation design (not an open question) verified by two CI-blocking tests (fast-path and dropped-message fallback); a real shared Redis instance provisioned in every non-sandbox environment; P0 alerting wired. The AI-feature registry granularity question (Task 01) remains a genuinely separate open item pending Product/F.35 confirmation.

## 31. Final Verification Checklist
- [ ] `kill_switch_event` table created, append-only, correctly indexed
- [ ] Safety-role-only restriction enforced and tested via direct API call (not just UI)
- [ ] `AiFeatureSuspensionCache` pub/sub fast-path verified under 60s in a genuine multi-instance test
- [ ] Reconciliation-poll fallback verified to self-correct within `RECONCILIATION_POLL_SECONDS` when a pub/sub message is dropped
- [ ] Real shared Redis instance provisioned in staging/production (infrastructure task, not just code)
- [ ] Idempotent double-suspend/reinstate handled gracefully
- [ ] Redis-unavailable path fails loudly, never silently succeeds
- [ ] Dual-write to shared E.28 audit log verified
- [ ] P0 alert wired on every activation
- [ ] AI-feature registry granularity (coarse F.35 service vs. fine-grained toggle) confirmed with Product before launch — tracked separately, not blocking this blueprint's own completion
- [ ] Tests green in CI, both signature tests non-bypassable
