# Blueprint: Platform-Wide Entitlement Check Service

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/subscriptions/`. Delivers `GET /v1/entitlements/check`, the single shared entitlement-decision endpoint every other feature (A.2/A.3/A.5/A.6/A.10/A.11/B.15/C.21/C.22) calls rather than independently re-deriving entitlement logic.

## 2. Parent Feature
C.24 — Subscription & Billing.

## 3. Sub-feature
B-06 — Platform-Wide Entitlement Check Service.

## 4. Objective
Provide a single, high-volume, low-latency internal endpoint resolving entitlement for a given feature+child, honoring last-verified entitlement plus a grace window when webhook delivery is delayed, and serving as the sole entitlement-decision authority platform-wide.

## 5. Business Requirements
Source: PRD §1.7 FR-5, FR-6, §3.4 (`GET /v1/entitlements/check`), §5 AI Code-Gen Prompt item 5.
- Consumed at exactly 7 checkpoints: catalog/home feed, search, content detail, playback start, download manifest, AI features, child-profile activation/creation.
- No other service independently re-derives entitlement logic — an architectural convention this endpoint's existence and adoption enforces.
- Webhook-delay handling: use last-verified entitlement plus a grace window rather than failing closed immediately; the Reconciliation Job (B-04) resolves any lingering ambiguity.
- High-volume, sampled analytics (`entitlement_check_performed`) given call frequency.

## 6. Existing Architecture
Per `FAST-API-INSTRUCTIONS.md` §5.10: `SubscriptionService.get_entitlement()` already exists as a named method in the inventory — this blueprint implements/extends that exact method rather than inventing a parallel one. Redis caching per `infrastructure/redis.py`, same pattern as B-01.

## 7. Existing Code to Reuse
- `SubscriptionService.get_entitlement()` (existing named method per inventory — extend to the full 7-checkpoint contract).
- `SubscriptionRepository.get_active_family_subscription()`.
- Redis pool singleton for entitlement-state caching (short TTL, given entitlement can change via webhook at any time).
- `ChildRepository` (`modules/identity/`) — resolve `child_id` to family/plan context.

## 8. Files to Create
- `tests/modules/subscriptions/test_platform_entitlement_check_service.py`
- `docs/architecture/entitlement-check-contract.md` (or equivalent) — documents the sole-consumer convention for other feature teams

## 9. Files to Modify
- `src/noorheroes/modules/subscriptions/schemas.py` — add `EntitlementCheckResponse`
- `src/noorheroes/modules/subscriptions/service.py` — extend `get_entitlement()` to cover all 7 checkpoint contexts
- `src/noorheroes/modules/subscriptions/api.py` — add `GET /v1/entitlements/check`

## 10. Backend Requirements
- Route: `GET /v1/entitlements/check?feature=&child_id=`, requires authenticated session (parent or child, per the calling feature's own auth context — this endpoint itself does not restrict by session type beyond requiring a valid authenticated caller).
- `SubscriptionService.get_entitlement(context, feature, child_id)`:
  1. Resolve `child_id`'s family and current `subscription.state`/`plan` (cache-first, Redis short TTL keyed `entitlement:{family_id}`).
  2. Map `feature` (one of: `catalog`, `search`, `content_detail`, `playback`, `download_manifest`, `ai_features`, `child_profile_activation`) to the plan's included-features list.
  3. If cached entitlement is within the signed grace window of the last webhook-verified state (even if a webhook update might be pending), honor it rather than failing closed.
  4. Return `{ "entitled": bool, "reason": str }` — `reason` values e.g. `plan_includes_feature`, `plan_excludes_feature`, `child_capacity_exceeded`, `grace_window_active`.
  5. Emit sampled `entitlement_check_performed` analytics event (not on every call, per high-volume NFR).

## 11. KMP Requirements
Consumed exclusively via `EntitlementRepository.check(feature, childId)` (K-07) — the shared client-side wrapper every other feature module calls.

## 12. NextJS Requirements
N/A — admin surface does not perform per-feature entitlement checks (it manages plan definitions themselves, not runtime entitlement decisions).

## 13. API Contract
- **HTTP Method:** GET
- **Endpoint:** `/v1/entitlements/check?feature=&child_id=`
- **Auth:** Authenticated session (parent or child, internal/high-volume, called by every consuming feature)
- **Request:** query params `feature: str` (enum of 7 checkpoint values), `child_id: str`
- **Response 200:** `{ "entitled": true, "reason": "plan_includes_feature" }`
- **Authentication:** Bearer (parent or child session, per calling context)
- **Authorization:** `child_id` must belong to the caller's family
- **Validation:** `feature` must be one of the 7 known checkpoint values; unknown value → `422`
- **Error Responses:** `401` invalid session; `422` unknown `feature` value; `404` `child_id` not found/not owned

## 14. Database Requirements
Read-only against `subscription` table; no new tables. Heavy read-path — this is where Redis caching matters most given call volume.

## 15. Validation
- `feature` enum-validated against the exact 7 checkpoint values from FR-5 — no open-ended string accepted.
- `child_id` family-ownership validated.

## 16. Authentication
Bearer session — parent or child, depending on which feature is calling (e.g., playback-start checks may originate from a child-mode session, catalog checks from either).

## 17. Authorization
`child_id` must resolve to the caller's own family.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Unknown `feature` value | `422`, explicit list of valid values in error detail |
| `child_id` not owned by caller's family | `404` (uniform, avoid existence leakage) |
| Webhook delayed, entitlement within grace window | `200`, `entitled` per last-verified state, `reason: grace_window_active` if relevant |
| Redis unavailable | Fall back to direct DB read, log warning, still return correct result |

## 19. Offline First
N/A server-side; KMP's `EntitlementRepository` caches last-verified entitlement for offline feature-gating (K-07's responsibility).

## 20. Local Data
N/A (backend).

## 21. Localization
`reason` values are machine-readable codes, localized client-side into user-facing upsell copy where applicable.

## 22. RTL
N/A (backend).

## 23. Analytics
`entitlement_check_performed` — internal, high-volume, **sampled** (not fired on every call, per §1.19 explicit note) to avoid overwhelming the Analytics Event Bus.

## 24. Performance
- **This is the platform's highest-call-volume billing-related endpoint** — Redis cache-first is mandatory, short TTL balancing freshness against load.
- p95 latency target must be low given synchronous gating use at playback-start and content-detail load (blocking UX paths).
- No N+1 queries; single cached lookup per `family_id`.

## 25. Security
- Sole-authority convention: write an architectural test/lint rule (or documented convention, per PRD §5 item 5) confirming no other backend service independently re-derives entitlement logic rather than calling this endpoint.
- No new PII surface.

## 26. Library Requirements
No new dependencies; existing Redis client, SQLAlchemy async session.

## 27. Testing
1. Unit test: entitled feature under current plan → `entitled: true`.
2. Unit test: excluded feature under current plan → `entitled: false, reason: plan_excludes_feature`.
3. Unit test: each of the 7 checkpoint contexts resolves correctly (catalog, search, content_detail, playback, download_manifest, ai_features, child_profile_activation) — PRD §5 item 5 explicit requirement.
4. Unit test: unknown `feature` value → `422`.
5. Unit test: cross-family `child_id` → `404`.
6. Unit test: webhook-delayed scenario honors last-verified entitlement within grace window.
7. Integration test: cache-hit vs. cache-miss latency/behavior.
8. Architectural/documented-convention test: confirm (via code search or lint rule) no other module independently calls the store/receipt logic or re-derives entitlement outside this service.

## 28. Documentation
OpenAPI docstring listing all 7 valid `feature` enum values; a dedicated architecture note (`docs/architecture/entitlement-check-contract.md`) instructing all feature teams to consume this endpoint exclusively — referenced from each consuming feature's own blueprint (A.2/A.3/A.5/A.6/A.10/A.11/B.15/C.21/C.22).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Entitlement Check Schema & Feature Enum**
- Task ID: B06-T01
- Objective: `EntitlementCheckResponse`, `EntitlementFeature` enum (7 values).
- Why This Is Required: Type-safe, exhaustive contract per FR-5.
- Existing Architecture to Follow: `NoorHeroesBaseModel`, Python `Enum`.
- Existing Files to Reuse: `common/schemas.py`.
- Files to Create: none.
- Files to Modify: `modules/subscriptions/schemas.py`.
- Implementation Details: Enum values exactly: `catalog`, `search`, `content_detail`, `playback`, `download_manifest`, `ai_features`, `child_profile_activation`.
- Business Rules: FR-5.
- Validation: Enum-constrained.
- Error Handling/Security/Performance/Localization/RTL/Analytics: N/A (definitions).
- Tests: Covered in Task 04.
- Documentation: Docstring per enum value explaining its checkpoint.
- Dependencies: none.
- Do Not Change: N/A.
- Expected Result: Schema importable.
- Definition of Done: Exactly 7 enum values, matching FR-5.

**Task 02 — Implement/Extend get_entitlement() with Redis Caching**
- Task ID: B06-T02
- Objective: Full resolution logic per §10, cache-first.
- Why This Is Required: Core business logic, highest-call-volume path.
- Existing Architecture to Follow: Existing `SubscriptionService.get_entitlement()` named method; Redis pool pattern.
- Existing Files to Reuse: `SubscriptionRepository`, Redis pool.
- Files to Create: none.
- Files to Modify: `service.py`.
- Implementation Details: Per §10 steps 1–5.
- Business Rules: FR-5, FR-6.
- Validation: Per §15.
- Error Handling: Per §18 (Redis fallback).
- Security: N/A beyond family-ownership.
- Performance: This IS the performance-critical path — cache-first mandatory.
- Localization: `reason` as machine-readable code.
- RTL: N/A.
- Analytics: Sampled `entitlement_check_performed` emission.
- Tests: Covered in Task 04.
- Documentation: Docstring.
- Dependencies: Task 01.
- Do Not Change: Do not modify Redis credentials/config.
- Expected Result: Correct entitlement resolution for all 7 checkpoints.
- Definition of Done: All Task 04 tests pass.

**Task 03 — Implement Route**
- Task ID: B06-T03
- Objective: Expose `GET /v1/entitlements/check`.
- Why This Is Required: Public internal contract delivery.
- Existing Architecture to Follow: Existing router pattern, flexible parent/child session dependency.
- Existing Files to Reuse: `api.py`.
- Files to Create: none.
- Files to Modify: `api.py`.
- Implementation Details: `@router.get(...)` accepting either `ParentSessionContext` or `ChildSessionContext` (confirm exact combined-auth dependency pattern against existing code rather than guessing — Do Not Guess).
- Business Rules: FR-5.
- Validation: Pydantic query param validation.
- Error Handling: Per §18.
- Security: Family-ownership check on `child_id`.
- Performance: N/A.
- Localization/RTL: N/A.
- Analytics: N/A (handled in service).
- Tests: Covered in Task 04.
- Documentation: OpenAPI listing all 7 feature values.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: Endpoint live.
- Definition of Done: Matches §13 exactly.

**Task 04 — Write Test Suite & Architectural Convention Check**
- Task ID: B06-T04
- Objective: Cover all 8 scenarios in §27, including the sole-authority architectural test.
- Why This Is Required: PRD §5 item 5's explicit dual requirement (functional correctness + architectural convention enforcement).
- Existing Architecture to Follow: pytest, async test client, optional lint/static-analysis check.
- Existing Files to Reuse: Fixture factories for family/child/subscription state.
- Files to Create: `tests/modules/subscriptions/test_platform_entitlement_check_service.py`.
- Files to Modify: none.
- Implementation Details: 8 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact status codes.
- Security: Cross-family rejection test.
- Performance: Cache-hit/miss timing assertions.
- Localization/RTL: N/A.
- Analytics: Assert sampled (not 100%) emission behavior.
- Tests: This task IS the tests.
- Documentation: Test docstrings, architecture note.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 covered and green.

## 30. Definition of Done
`GET /v1/entitlements/check` live, resolves correctly for all 7 checkpoint contexts, Redis-cached for high-volume performance, honors grace-window logic during webhook delay, documented as the sole entitlement-decision authority, all tests green.

## 31. Final Verification Checklist
- [ ] All 7 checkpoint contexts resolve correctly (test-verified)
- [ ] Grace-window behavior verified during simulated webhook delay
- [ ] Cache-first performance path verified
- [ ] Cross-family `child_id` rejected
- [ ] Architectural sole-authority convention documented and referenced from every consuming feature's blueprint
- [ ] Sampled (not full-volume) analytics emission confirmed
- [ ] OpenAPI docs list all 7 valid feature values
