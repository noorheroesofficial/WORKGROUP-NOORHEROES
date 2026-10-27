# B-05 — Skill State Query API

> **Status:** ✅ **COMPLETED & VERIFIED (100% Green in Test Suite & CI)**  
> **Platform:** Backend (FastAPI / SQLAlchemy 2.0 / PostgreSQL / Redis)  
> **Bounded Context:** `src/noorheroes/modules/learning/` (Learning Context)  
> **Endpoints Delivered:** `GET /v1/mastery/skills`, `GET /v1/learning/mastery/skills` (Canonical & Module Alias)  
> **Schemas Delivered:** `SkillStateResponse`, `SkillStateListResponse` in `src/noorheroes/modules/learning/schemas/mastery_skill_state.py`  
> **Service Layer:** `SkillTreeService.get_skill_states()` with Redis 120s edge caching & multi-domain support  
> **Child-Safety Invariant (FR-3):** Strict structural continuous score/confidence omission enforced via mandatory CI reflection gate  
> **Test Coverage:** 100% Green across 15 dedicated B-05 tests (`test_skill_state_query_api.py` [10], `test_no_raw_score_schema_introspection.py` [5]), 60 Feature A.9 mastery tests, and 981 total learning context tests.

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). This is the child-facing read endpoint that every domain's skill-tree UI (A.5's `K-01 Quran Skill Tree Map`, and any future domain UI) calls to render current skill states — with a hard, structurally-enforced guarantee that no raw mastery score ever reaches the client.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
B-05 — Skill State Query API (User API)

## 4. Objective
Implement `GET /v1/mastery/skills?child_id=&domain=`, returning per-skill state for a domain (or, per future extension, potentially all domains) with a response schema that structurally omits any raw numeric mastery/confidence field.

## 5. Business Requirements
- FR-3: Child-facing UI must show progress without ever revealing the raw numeric mastery/confidence score — enforced by the engine's API contract, never including a raw score field in any child-facing response.
- Acceptance Criterion: viewing any skill's progress never renders a raw numeric score — only a state label and/or progress-ring visualization.
- Cross-Cutting API Concern (A.9 PRD §3.5): covered by a dedicated schema-introspection test.

## 6. Existing Architecture
FastAPI async Python 3.12, SQLAlchemy 2.0, PostgreSQL, Redis. `learning` bounded context. This endpoint is functionally the generalized successor to A.5's existing `GET /v1/learning/paths` (which already excludes raw score in its child-facing shape per A.5 B-01) — confirm whether this is a genuinely new route or whether A.5's existing endpoint is being renamed/aliased to `/v1/mastery/skills` as part of the A.9 generalization; if the latter, this sub-feature is a rename+re-scope of that existing route rather than a parallel new one (avoid the "two endpoints doing the same thing" anti-pattern FR-9 warns against).

## 7. Existing Code to Reuse
- `get_current_child` dependency, `ChildSessionContext` DTO from `src/noorheroes/core/deps.py`.
- A.5 B-01's existing `SkillTreeService`/`skill_node_repository`/`skill_node_state_repository` — extend for domain-agnostic querying (post B-01's generalization) rather than duplicating.
- Redis read-through caching pattern already used for A.5's skill-tree reads.

## 8. Files to Create
- `src/noorheroes/modules/learning/schemas/mastery_skill_state.py` — `SkillStateResponse` (list item: `skill_node_id`, `state`, `domain` — no score field declared, structurally).
- `tests/modules/learning/test_skill_state_query_api.py`
- `tests/modules/learning/test_no_raw_score_schema_introspection.py` — reflection-based test enumerating every response model in the `learning` context's mastery-facing routes, asserting none contains a numeric field matching `/score|confidence/i`.

## 9. Files to Modify
- `src/noorheroes/modules/learning/api.py` — add (or re-scope A.5's existing) `GET /v1/mastery/skills` route.
- `src/noorheroes/modules/learning/services/skill_tree_service.py` — extend `get_skill_tree()`/add `get_skill_states()` to operate against B-01's generalized `domain` field.

## 10. Backend Requirements
- **Router:** `GET /v1/mastery/skills?child_id=&domain=`, guarded by `get_current_child`; `child_id` must match/be scoped to the authenticated session's family — `403` on mismatch.
- **Optional domain filter:** omitting `domain` is a documented extension point (not required for A.5's initial consumer, which always passes a domain) — if implemented, returns states across all domains; if deferred, document it as a known future extension in the API contract rather than silently unsupported.
- **Response shape:** `{ skill_node_id, state, domain }` per item — `mastery_score` and `formula_version` (both present in the DB row) are never serialized into this response; enforced structurally by the Pydantic response model simply not declaring those fields (not by a runtime filter that could be bypassed).
- **Cache:** Redis read-through, short TTL, invalidated on any `skill_node_state` write (B-04's evidence processing, B-07's spaced-repetition transitions).

## 11. KMP Requirements
Consumed by `MasteryRepository.getSkillStates(domain)` (K-01); domain skill-tree screens (A.5's `K-01 Quran Skill Tree Map`, generalized via K-03's `SkillTreeStateRenderer`) render this response directly with zero client-side mastery computation.

## 12. NextJS Requirements
N/A directly (admin-side skill definitions managed via A.5's Curriculum Builder / N-01's domain registry, not this read endpoint).

## 13. API Contract

**`GET /v1/mastery/skills?child_id={uuid}&domain={domain_key}`**
- **Auth:** Bearer (child-mode), `get_current_child`
- **Response 200:**
```json
{
  "domain": "quran",
  "skills": [
    { "skill_node_id": "uuid", "state": "practicing" }
  ]
}
```
- **Authentication:** Bearer JWT, child-session scope.
- **Authorization:** `child_id` must belong to the authenticated session's `family_id`.
- **Validation:** `domain` must be a registered, active domain (per B-01's `SkillDomainService`); `child_id` valid UUID belonging to the family.
- **Error Responses:** `401` (invalid/missing token), `403` (child_id not in caller's family), `422` (invalid/unregistered domain), `500` (db failure), degrade to cached response on Redis failure.

## 14. Database Requirements
Reads `skill_node_state` joined with `skill_node` (for domain filtering, post B-01 generalization). No schema changes beyond what B-01/B-04 already introduced.

## 15. Validation
- `domain` validated against `SkillDomainService.list_active_domains()`.
- `child_id` must resolve to an active child profile in the caller's family.
- Zero skills for a domain returns an empty `skills` array, not an error (consistent with A.5's empty-state precedent).

## 16. Authentication
Bearer JWT via `get_current_child`; no admin/parent token accepted on this route.

## 17. Authorization
`child_id` must match the authenticated session's family; cross-family access rejected as `403` without leaking existence of another family's child via a different error code (mirrors A.5 B-01's existing pattern).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Redis cache failure | Serve DB-fresh read, log warning, no error |
| DB failure | `500`, generic error body, correlation-ID logged |
| Unknown/cross-family `child_id` | `403` |
| Invalid/unregistered `domain` | `422` |
| Zero skills for domain | `200` with empty `skills` array |

## 19. Offline First
N/A (backend). Client-side offline/cache-fallback owned by K-01 (Room-cached `skill_node_state`).

## 20. Local Data
N/A (backend).

## 21. Localization
N/A (raw state enums only; human-readable label mapping owned client-side by K-03's `SkillTreeStateRenderer`, localized there).

## 22. RTL
N/A (backend).

## 23. Analytics
No dedicated event for this read endpoint beyond standard API-latency monitoring; state-transition events are fired at the write path (B-04/B-07), not here.

## 24. Performance
Redis-cached, short TTL; must support frequent polling from the Learn Tab entry point (A.5's high-traffic screen) without DB load — index on `(child_id, state)` already present per A.9 PRD §4.2 table.

## 25. Security
Schema-level exclusion of raw score fields is the primary security/child-UX control here — verified by the mandatory schema-introspection test (Backend AI Prompt item 8), treated as one of the two highest-priority tests for this feature per the top-level Backend AI Code-Generation Prompt.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: response serialization confirming absence of score fields.
- Schema introspection test: enumerate all mastery-facing response models, assert none exposes a numeric score/confidence field (Backend AI Prompt item 8 — highest priority alongside B-07's cross-domain cap test).
- Integration: full request→response cycle including cache-hit and cache-miss paths, cross-family rejection, unregistered-domain rejection.

## 28. Documentation
OpenAPI schema explicitly documents the intentional absence of a score field (a design decision, not an oversight) so future engineers don't "helpfully" add one back.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define SkillStateResponse Schema (No Score Field)**
- Task ID: B-05-T01
- Objective: Pydantic response model that structurally cannot carry a raw score.
- Why This Is Required: FR-3 is a hard rule; structural enforcement (field doesn't exist) is stronger than convention (field exists but isn't populated).
- Existing Architecture to Follow: Existing Pydantic schema conventions in `learning/schemas/`.
- Existing Files to Reuse: N/A.
- Files to Create: `schemas/mastery_skill_state.py`.
- Files to Modify: None.
- Implementation Details: `SkillStateResponse(skill_node_id: UUID, state: str)`, `SkillStateListResponse(domain: str, skills: list[SkillStateResponse])` — no `mastery_score`/`confidence` field anywhere.
- Business Rules: N/A. Validation: `state` constrained to the 6-value enum.
- Error Handling/Security/Performance: N/A.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: Covered by Task 03's introspection test.
- Documentation: Inline comment explaining the intentional omission.
- Dependencies: B-01, B-03.
- Do Not Change: N/A.
- Expected Result: Score-free schema ready.
- Definition of Done: Schema reviewed against introspection test criteria.

**Task 02 — Implement GET /v1/mastery/skills Router + Service Method**
- Task ID: B-05-T02
- Objective: Working, cached, authorized endpoint.
- Why This Is Required: Primary read path for every domain's skill-tree UI.
- Existing Architecture to Follow: Router → Service → Repository; `get_current_child` guard pattern.
- Existing Files to Reuse: `SkillTreeService`, `get_current_child`.
- Files to Create: None beyond Task 01.
- Files to Modify: `api.py`, `services/skill_tree_service.py`.
- Implementation Details: `get_skill_states(child_id, domain)` queries `skill_node_state` joined to `skill_node` filtered by `domain`; Redis-cached with invalidation hooks wired to B-04/B-07's write paths.
- Business Rules: `403` on cross-family access; `422` on unregistered domain.
- Validation: Per §15.
- Error Handling: Per §18.
- Security: Auth/authz enforced via `get_current_child`.
- Performance: Cache hit path avoids DB round-trip.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: `test_skill_state_query_api.py`.
- Documentation: OpenAPI schema.
- Dependencies: Task 01, B-01.
- Do Not Change: N/A.
- Expected Result: Working endpoint.
- Definition of Done: Integration test green including cache-hit/miss and error paths.

**Task 03 — Schema Introspection Test (No Raw Score Anywhere)**
- Task ID: B-05-T03
- Objective: Automated, structural proof that no mastery-facing response model exposes a raw score.
- Why This Is Required: This is the single highest-priority test for FR-3's child-safety guarantee (Backend AI Prompt item 8).
- Existing Architecture to Follow: Reflection over Pydantic models, mirroring A.8/A.5's existing schema-introspection test pattern (if one exists in that codebase, reuse its approach rather than inventing a new introspection mechanism).
- Existing Files to Reuse: A.8/A.5's schema-introspection test pattern, if present.
- Files to Create: `tests/modules/learning/test_no_raw_score_schema_introspection.py`.
- Files to Modify: None.
- Implementation Details: Enumerate every response model registered on mastery-facing routes (`/v1/mastery/*`); for each, walk its fields recursively; assert no numeric field name matches `/score|confidence/i` at any nesting level.
- Business Rules: This test must cover every current AND future mastery-facing response model automatically (via route/model registry introspection, not a hardcoded list that could go stale).
- Validation/Error Handling/Security: This IS the security control being tested.
- Performance: N/A. Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: This task IS the test.
- Documentation: Test docstring explaining why this is a permanent, mandatory CI gate.
- Dependencies: Task 01, Task 02.
- Do Not Change: N/A.
- Expected Result: Passing structural guarantee.
- Definition of Done: Test green, marked mandatory/non-bypassable in CI per A.9 PRD §10.

## 30. Definition of Done
`GET /v1/mastery/skills` live, cached, authorized, returning per-domain skill states with a response schema that structurally and verifiably never exposes a raw mastery/confidence score.

## 31. Final Verification Checklist
- [x] Endpoint returns correct per-domain skill states
- [x] Response schema contains no score/confidence field (introspection test green)
- [x] Cross-family access rejected (403)
- [x] Unregistered domain rejected (422)
- [x] Empty-domain case returns empty array, not error
- [x] Redis cache + invalidation wired to B-04/B-07 writes
- [x] OpenAPI docs explicitly note the intentional score-field omission

## 32. Verification Evidence & Test Results
- **Dedicated B-05 Suite (`test_skill_state_query_api.py`, `test_no_raw_score_schema_introspection.py`)**: 15 passed in 3.05s (100% green).
- **Mandatory FR-3 CI Gate (`test_no_raw_score_schema_introspection.py`)**: 5 passed in 2.73s (verifying Pydantic model fields, camelCase/snake_case serialized keys, dynamic router models, and OpenAPI specification components contain zero `/score|confidence/i` fields).
- **Thin Controller Router Verification (`test_routing.py`)**: 9 passed (0 `ast.If` router violations across all controllers).
- **Core Suite & Translation Integrity (`tests/core/`)**: 262 passed, 0 failures (100% green across all error classes, __all__ exports, and 4-locale error translation catalog).
- **Full Learning Bounded Context Suite (`tests/modules/learning/`)**: 981 passed in 29.05s (100% green, 0 regressions across B-01 through B-05).

