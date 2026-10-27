# Blueprint: Plan Catalog & Pricing API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/subscriptions/`. This blueprint delivers the public, cached plan-catalog read endpoint that powers the Plan Comparison screen and every other surface that needs current plan/pricing/capacity data: `GET /api/v1/billing/plans`.

## 2. Parent Feature
C.24 — Subscription & Billing.

## 3. Sub-feature
B-01 — Plan Catalog & Pricing API.

## 4. Objective
Serve the three canonical plans (Free Family Starter, Mobile Family, Premium Family) — pricing (monthly/annual), child capacity, and included-feature lists — as a public, Redis-cached response, sourced from admin-managed plan records (E.33 Plan Catalog Manager writes these; this endpoint only reads).

## 5. Business Requirements
Source: PRD §1.7 FR-1, §3.4 (`GET /api/v1/billing/plans`), §2.2 Plan Comparison screen requirements.
- Three plans: Free Family Starter ($0, 1 child), Mobile Family ($3/mo or $30/yr, 4 children), Premium Family ($5.99/mo or $59/yr, 8 children).
- Response cached in Redis; public, unauthenticated, high-traffic endpoint (hit on every Subscription/Plan Comparison screen load).
- Plan/pricing changes made via E.33's Plan Catalog Manager must never retroactively alter already-existing subscribers' entitlements — only this catalog read and new-subscriber activation are affected.
- Deactivated plans are excluded from this response but existing subscribers on them keep their entitlements (enforced elsewhere, not by this endpoint).

## 6. Existing Architecture
Per `FAST-API-INSTRUCTIONS.md` §5.10 (`subscriptions` context): Router → Service → Repository layering; existing `SubscriptionPlan` model, `SubscriptionRepository` (`get_plan_by_id()`), `SubscriptionService(BaseService)`, `SubscriptionsRouter`. This blueprint extends the existing `subscriptions` module rather than creating a new one. Redis access via `infrastructure/redis.py`. `BaseService`/`BaseRepository[ModelT]` generic patterns apply.

## 7. Existing Code to Reuse
- `SubscriptionRepository` (`modules/subscriptions/repository.py`) — extend with `list_active_plans()`.
- `SubscriptionService(BaseService)` (`modules/subscriptions/service.py`) — extend with `get_plan_catalog()`.
- `SubscriptionsRouter` (`modules/subscriptions/api.py`) — existing router to mount the new route on.
- Redis pool singleton (`infrastructure/redis.py`, `get_redis_pool()`), same pattern used by C.20's dashboard cache.
- `common/schemas.py` → `NoorHeroesBaseModel` base for new Pydantic schemas.

## 8. Files to Create
- `src/noorheroes/modules/subscriptions/schemas.py` (if not already present) — `PlanResponse`, `PlanCatalogResponse`
- `tests/modules/subscriptions/test_plan_catalog_pricing_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/subscriptions/repository.py` — add `list_active_plans()`
- `src/noorheroes/modules/subscriptions/service.py` — add `get_plan_catalog()`
- `src/noorheroes/modules/subscriptions/api.py` — add `GET /api/v1/billing/plans` route
- `src/noorheroes/modules/subscriptions/deps.py` — expose `get_subscription_service()` if not already present

## 10. Backend Requirements
- Route: `GET /api/v1/billing/plans`, no auth dependency (public).
- `SubscriptionService.get_plan_catalog()`:
  1. Attempt Redis cache read (`billing:plans:catalog`).
  2. On cache miss, query `SubscriptionRepository.list_active_plans()` (only `is_active = true` plans, ordered by tier).
  3. Serialize to `PlanCatalogResponse`, write through to Redis with a medium TTL (plan data changes rarely).
  4. Return.
- Cache invalidation: E.33's Plan Catalog Manager mutation endpoints must explicitly bust `billing:plans:catalog` on any create/update/deactivate (cross-ref N-01).

## 11. KMP Requirements
Consumed by `SubscriptionRepository.getPlans()` (K-01, K-02) to render Plan Comparison. Response shape must map directly to plan-card UI fields (no client-side reshaping of pricing math beyond currency/locale formatting).

## 12. NextJS Requirements
Indirectly consumed: N-01 Plan Catalog Manager writes the records this endpoint reads and is responsible for cache invalidation on mutation.

## 13. API Contract
- **HTTP Method:** GET
- **Endpoint:** `/api/v1/billing/plans`
- **Auth:** Public
- **Request:** none
- **Response 200:**
```json
{
  "plans": [
    {
      "plan_code": "free_family_starter",
      "display_name": "Free Family Starter",
      "monthly_price": 0.00,
      "annual_price": 0.00,
      "annual_savings_pct": 0,
      "currency": "USD",
      "child_capacity": 1,
      "included_features": ["basic_stories", "basic_duas", "habit_tracking", "basic_reports"],
      "is_current_default": true
    },
    {
      "plan_code": "mobile_family",
      "display_name": "Mobile Family",
      "monthly_price": 3.00,
      "annual_price": 30.00,
      "annual_savings_pct": 16.7,
      "currency": "USD",
      "child_capacity": 4,
      "included_features": ["expanded_content", "offline_downloads_10", "monthly_family_report", "limited_ai_insights"]
    },
    {
      "plan_code": "premium_family",
      "display_name": "Premium Family",
      "monthly_price": 5.99,
      "annual_price": 59.00,
      "annual_savings_pct": 17.9,
      "currency": "USD",
      "child_capacity": 8,
      "included_features": ["full_story_library", "premium_animated_stories", "full_offline_mode", "weekly_ai_parent_reports", "advanced_dashboard"]
    }
  ]
}
```
- **Authentication:** None (public)
- **Authorization:** None
- **Validation:** N/A (no request body/params)
- **Error Responses:** `500` on Redis+DB simultaneous failure (rare, logged as P1)

## 14. Database Requirements
Reuses existing `subscription_plan` table (owned by `SubscriptionPlan` model, admin-managed via E.33). No new tables for this sub-feature. Add `is_active` boolean column and `included_features` (JSON/array) column if not already present — confirm against actual model before assuming absence (Do Not Guess).

## 15. Validation
N/A — no request input to validate.

## 16. Authentication
None (public endpoint).

## 17. Authorization
None (public endpoint) — but the endpoint MUST NOT expose any admin-only or PII field (e.g., internal cost basis, provider product IDs beyond what's needed client-side).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Redis unavailable | Fall back to direct DB read, log cache-unavailable warning, still return 200 |
| Empty/misconfigured plan catalog | Return `{"plans": []}` with 200, never a 500 — client renders an empty/error state gracefully rather than crashing on a malformed catalog |
| DB unavailable | `503`, alertable |

## 19. Offline First
N/A server-side; KMP client caches last-fetched catalog for offline Plan Comparison rendering (K-02's responsibility).

## 20. Local Data
N/A (backend).

## 21. Localization
`display_name` and feature labels should resolve through the platform's localization service where the client requests a locale-aware response, or be returned as stable keys that the KMP/NextJS layers resolve to localized strings — never hardcoded English-only display copy baked into the DB record consumed directly as-is.

## 22. RTL
N/A (backend; RTL is a KMP/NextJS presentation concern).

## 23. Analytics
`plan_comparison_viewed` fires client-side (K-02), not server-side; this endpoint's role is solely to serve catalog data.

## 24. Performance
- Redis cache-first, medium TTL, given plan data changes infrequently but this endpoint is hit on nearly every Subscription screen load.
- No N+1 queries — single `list_active_plans()` query.
- Rate-limit at the API Gateway level given public/unauthenticated exposure.

## 25. Security
- No PII surface.
- No mutation capability on this route (read-only, GET only).
- Public exposure is intentional and by design (PRD FR-12); do not add an auth dependency.

## 26. Library Requirements
No new dependencies; existing Redis client, SQLAlchemy async session, Pydantic v2.

## 27. Testing
1. Unit test: cache-hit path returns cached payload without hitting DB.
2. Unit test: cache-miss path queries DB, writes through to cache.
3. Unit test: inactive/deactivated plans excluded from response.
4. Unit test: empty catalog returns `{"plans": []}` with 200, not an error.
5. Integration test: Redis unavailable → graceful DB fallback, still 200.
6. Integration test: full request against seeded three-plan fixture data matches §13 contract shape exactly.

## 28. Documentation
OpenAPI docstring on the route documenting all fields and the public/cached nature of the endpoint; update `subscriptions` module docstring noting this is the sole source for plan/pricing data platform-wide.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Plan Catalog Schemas**
- Task ID: B01-T01
- Objective: Create Pydantic schemas for plan and catalog response.
- Why This Is Required: Type-safe, validated public API contract.
- Existing Architecture to Follow: `NoorHeroesBaseModel` pattern (`common/schemas.py`).
- Existing Files to Reuse: `common/schemas.py`.
- Files to Create: `src/noorheroes/modules/subscriptions/schemas.py` (extend if exists).
- Files to Modify: none.
- Implementation Details: `PlanResponse` (plan_code, display_name, monthly_price, annual_price, annual_savings_pct, currency, child_capacity, included_features), `PlanCatalogResponse` (plans: list[PlanResponse]).
- Business Rules: FR-1 plan definitions exactly (three tiers, exact pricing/capacity).
- Validation: Field types match §13.
- Error Handling: N/A.
- Security: No admin-only fields included.
- Performance: N/A.
- Localization: `display_name`/feature labels as locale-resolvable.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Docstrings per field.
- Dependencies: none.
- Do Not Change: Existing schemas in other modules.
- Expected Result: Schemas importable.
- Definition of Done: Matches §13 contract exactly.

**Task 02 — Implement Repository & Service Methods**
- Task ID: B01-T02
- Objective: Build `list_active_plans()` (repository) and `get_plan_catalog()` (service, cache-then-DB).
- Why This Is Required: Core read logic with caching.
- Existing Architecture to Follow: `BaseRepository[ModelT]`, `BaseService`, Redis pool singleton.
- Existing Files to Reuse: `SubscriptionRepository`, `SubscriptionService`, `infrastructure/redis.py`.
- Files to Create: none.
- Files to Modify: `modules/subscriptions/repository.py`, `modules/subscriptions/service.py`.
- Implementation Details: Per §10 steps 1–4; cache key `billing:plans:catalog`; medium TTL (e.g. 1 hour).
- Business Rules: FR-1.
- Validation: N/A.
- Error Handling: Per §18 (Redis fallback to DB).
- Security: No admin-only field leakage.
- Performance: Cache-first read pattern is the primary optimization.
- Localization: Pass through locale-resolvable fields.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Docstring citing FR-1.
- Dependencies: Task 01.
- Do Not Change: Do not modify Redis connection credentials/config.
- Expected Result: Service returns `PlanCatalogResponse` from cache or DB.
- Definition of Done: Cache-hit and cache-miss paths both verified correct.

**Task 03 — Implement Route**
- Task ID: B01-T03
- Objective: Expose `GET /api/v1/billing/plans`.
- Why This Is Required: Public contract delivery.
- Existing Architecture to Follow: Existing `SubscriptionsRouter` pattern, no-auth route declaration.
- Existing Files to Reuse: `modules/subscriptions/api.py`, `deps.py`.
- Files to Create: none.
- Files to Modify: `api.py`, `deps.py` (expose `get_subscription_service()` if absent).
- Implementation Details: `@router.get("/api/v1/billing/plans", response_model=PlanCatalogResponse)` with no `Depends()` auth.
- Business Rules: FR-12 (public, cached).
- Validation: N/A.
- Error Handling: Per §18.
- Security: Confirm no auth dependency accidentally inherited from router-level middleware; explicitly public.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: OpenAPI summary/description noting public+cached nature.
- Dependencies: Tasks 01–02.
- Do Not Change: Do not add authentication to this route.
- Expected Result: Endpoint live and publicly reachable.
- Definition of Done: Matches §13 contract exactly.

**Task 04 — Write Test Suite**
- Task ID: B01-T04
- Objective: Cover all scenarios in §27.
- Why This Is Required: QA coverage for a high-traffic public endpoint.
- Existing Architecture to Follow: pytest + existing async test client fixtures.
- Existing Files to Reuse: Existing fixture factories for plan seed data.
- Files to Create: `tests/modules/subscriptions/test_plan_catalog_pricing_api.py`.
- Files to Modify: none.
- Implementation Details: 6 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert graceful fallback behavior.
- Security: Assert no admin-only fields present in response.
- Performance: Assert cache-hit path skips DB query (mock/spy).
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 scenarios covered and green.

## 30. Definition of Done
`GET /api/v1/billing/plans` live, public, Redis-cached with DB fallback, returns exactly the three canonical plans with correct pricing/capacity/feature data, all tests green.

## 31. Final Verification Checklist
- [ ] Cache-hit and cache-miss paths both verified
- [ ] Inactive plans excluded from response
- [ ] Empty catalog returns 200 with empty array, never a 500
- [ ] No admin-only/PII fields exposed
- [ ] No auth dependency present (confirmed intentionally public)
- [ ] Response shape matches §13 exactly, consumable by both KMP and admin cache-invalidation logic
- [ ] OpenAPI docs reflect full contract
