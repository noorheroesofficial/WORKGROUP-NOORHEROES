# K-07 — Shared Entitlement Repository (Cross-Feature Gating Contract)

## 1. Feature Context
The single client-side entitlement-check mechanism every other feature module (A.2/A.3/A.5/A.6/A.10/A.11/B.15) must consume — a shared `EntitlementRepository` rather than each module independently calling the backend or deriving its own gating logic.

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
2.7 Shared Entitlement Repository (Cross-Feature Gating Contract) (ID: **K-07**)

## 4. Objective
Implement `EntitlementRepository.check(feature, childId)` in `:core:network` or a dedicated `:core:entitlement` module as the sole client-side entitlement mechanism, with a structural test/lint rule confirming no other feature module makes an independent entitlement-related network call.

## 5. Business Requirements
- §6.5: `EntitlementRepository.check(feature, childId)` is the shared client-side wrapper around `GET /v1/entitlements/check`, consumed by every other feature module rather than each implementing its own call.
- §5 AI Code-Gen Prompt item 2 (Android): structural test/enforced lint rule confirming exclusivity.

## 6. Existing Architecture
New shared module `:core:entitlement` (or extension of `:core:network`, per architecture team preference — confirm placement before implementation, consistent with C.20's precedent of placing genuinely shared cross-feature contracts in `:core:*` rather than a feature module).

## 7. Existing Code to Reuse
- `:core:network` Retrofit/OkHttp scaffolding, Hilt DI conventions.
- `:core:auth` session context for parent/child token resolution (this endpoint is callable by either session type per B-06).

## 8. Files to Create
- `core/entitlement/EntitlementRepository.kt` (interface + impl)
- `core/entitlement/EntitlementCache.kt` — local short-TTL cache for offline/latency resilience
- `test/core/entitlement/EntitlementRepositoryTest.kt`
- `test/architecture/NoIndependentEntitlementCallsTest.kt` — structural test scanning feature modules

## 9. Files to Modify
- Each consuming feature module (A.2/A.3/A.5/A.6/A.10/A.11/B.15) — replace any ad hoc entitlement logic with `EntitlementRepository.check()` calls (cross-feature migration; coordinate with each feature's own blueprint rather than modifying their internals unilaterally here — this blueprint defines the contract, adoption is tracked per consuming feature).

## 10. KMP Requirements
- `EntitlementRepository.check(feature: EntitlementFeature, childId: String): EntitlementResult` wraps `GET /v1/entitlements/check`.
- Local short-TTL cache: on network failure, fall back to the last-known entitlement result rather than failing closed immediately (mirrors backend's own grace-window philosophy, client-side).
- `EntitlementFeature` enum mirrors B-06's exact 7 values: `CATALOG`, `SEARCH`, `CONTENT_DETAIL`, `PLAYBACK`, `DOWNLOAD_MANIFEST`, `AI_FEATURES`, `CHILD_PROFILE_ACTIVATION`.
- No feature module may instantiate its own Retrofit service for entitlement checks — this is the sole path.

## 11. Required API
`GET /v1/entitlements/check?feature=&child_id=` (B-06). **User/internal API**, called by every consuming feature via this shared repository.

## 12. Offline First
Last-cached entitlement result serves feature-gating decisions offline; each consuming feature's own offline UX (e.g., "content available offline but requires connection to verify access") is that feature's responsibility, informed by this repository's cached result.

## 13. Local Data
Short-TTL local cache keyed `(feature, childId)`, invalidated on any subscription-state-changing action (cancel, upgrade, downgrade) via a shared event/callback mechanism.

## 14. Localization
N/A directly (this is a data-layer contract); `reason` codes are consumed and localized by each calling feature's own UI layer.

## 15. RTL
N/A (data layer).

## 16. Analytics
None directly fired here (entitlement_check_performed is server-side/sampled per B-06); this repository is a pure data-access layer.

## 17. Performance
Cache-first with short TTL to avoid redundant network calls across features checking entitlement for the same child in quick succession (e.g., catalog load triggering multiple per-item checks).

## 18. Security
This is the platform's structural enforcement point preventing entitlement-logic drift/duplication across feature modules — a lint rule or CI-enforced structural test is mandatory, not optional, per PRD §5 item 2.

## 19. Testing
- Unit: `EntitlementRepository.check()` correctly wraps the backend call for each of the 7 feature enum values.
- Unit: cache fallback on network failure returns the last-known result rather than failing closed.
- Structural/architectural test: confirm no other feature module makes an independent entitlement-related network call outside this repository (PRD §7 item 2 — critical test, implement as a static-analysis/lint check or a test scanning module dependency graphs for direct entitlement-endpoint Retrofit service usage).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `:core:entitlement` Module**
Objective: create/extend the shared module housing this contract. Files to Create: module scaffolding. Dependencies: none.

**Task 02 — Implement `EntitlementRepository` & `EntitlementFeature` Enum**
Objective: wrap `GET /v1/entitlements/check` for all 7 feature values. Files to Create: `EntitlementRepository.kt`. Dependencies: Task 01, B-06 live.

**Task 03 — Implement Local Short-TTL Cache**
Objective: fallback-on-failure caching layer. Files to Create: `EntitlementCache.kt`. Dependencies: Task 02.

**Task 04 — Implement Structural No-Independent-Calls Test**
Objective: enforce sole-consumer convention across feature modules. Files to Create: `NoIndependentEntitlementCallsTest.kt`. Dependencies: Task 02.

**Task 05 — Publish Adoption Contract & Coordinate Migration**
Objective: document the contract for A.2/A.3/A.5/A.6/A.10/A.11/B.15 to adopt (cross-referenced from each feature's own blueprint, not modified here directly). Dependencies: Tasks 02–04.

**Task 06 — Add Full Test Suite**
Objective: coverage per §19. Dependencies: Tasks 01–05.

## 21. Final Verification Checklist
- [ ] `EntitlementRepository.check()` correctly resolves all 7 feature contexts
- [ ] Cache fallback verified on simulated network failure
- [ ] Structural test confirms zero independent entitlement network calls elsewhere in the codebase
- [ ] Contract documented and cross-referenced from every consuming feature's blueprint

## 22. Definition of Done
`EntitlementRepository` live as the sole client-side entitlement-check mechanism, with cache-resilient offline behavior and a structural test enforcing exclusive adoption across all consuming feature modules.
