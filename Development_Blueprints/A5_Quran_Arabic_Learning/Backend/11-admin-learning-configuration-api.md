# B-11 — Admin Learning Configuration API

> **Status:** ✅ **COMPLETED & VERIFIED**  
> **Target Framework:** FastAPI (Python 3.12+) / SQLAlchemy 2.0 (Async) / Pydantic v2 / Redis 7  
> **Architecture Pattern:** Clean Architecture, Modular Monolith, Strict RBAC (product_admin/ai_ops vs ai_ops-only), Server-Side Typed Confirmation Friction ("I understand"), Dialect-Aware JSONType Singleton Storage, Downstream Dynamic Injection (B-04 & B-06), Short-TTL Caching with Failover Resilience, Dual-Route Parity  
> **Test Coverage:** 63 Dedicated Tests Passing (+ 4 Downstream Integration Tests, 671 Total Learning Module Tests Passing, 100% Green in CI)

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Exposes admin-tunable configuration for the Spaced Repetition Scheduler (B-06) and the AI Pronunciation confidence threshold (B-04) without requiring a code deploy.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
B-11 — Admin Learning Configuration API (Admin API)

## 4. Objective
Provide update-only configuration endpoints for spaced-repetition decay weights/daily cap and the pronunciation confidence threshold, with extra friction (typed confirmation) on the threshold given its sensitivity.

## 5. Business Requirements
- Admin Requirements §8: Spaced Repetition Configuration (decay weights, daily cap) admin-tunable without code deploy; Pronunciation Confidence Threshold admin-tunable with a clear warning that lowering it increases AI-generated (vs. fallback) feedback — a deliberate friction point.
- CRUD permissions: both configs are Update-only behind `product_admin` or `ai_ops` role (confidence threshold specifically restricted to `ai_ops`, with a typed confirmation phrase required before save, per §9 Admin AI Code-Generation Prompt).

## 6. Existing Architecture
Modular monolith `admin` context handles cross-cutting admin auth/RBAC/audit-logging; this blueprint's config table lives in the `learning` context (config it governs) but is gated by the same RBAC pattern as B-09/B-10.

## 7. Existing Code to Reuse
- `get_current_admin`, admin `audit_log` mechanism (same pattern as B-09/B-10).

## 8. Files Created
- `src/noorheroes/modules/learning/learning_config_models.py` (`LearningConfig` ORM model mapped to `learning_config` table with singleton-per-key pattern, cross-dialect `JSONType`, and `updated_by_admin_id`)
- `src/noorheroes/modules/learning/learning_config_repository.py` (`LearningConfigRepository` with atomic upserts, cache invalidation hooks, and safe defaults)
- `src/noorheroes/modules/learning/learning_config_schemas.py` (Pydantic v2 schemas: `SpacedRepetitionConfigUpdateRequest`, `SpacedRepetitionConfigResponse`, `ConfidenceThresholdConfigRequest`, `ConfidenceThresholdConfigResponse`, `LearningConfigEnvelopeResponse`, and OpenAPI dicts)
- `src/noorheroes/modules/learning/admin_learning_config_service.py` (`AdminLearningConfigService` orchestrating RBAC enforcement, exact-match typed confirmation phrase validation, bounds checks, atomic `AdminAuditRecord` logging with diffs, and Redis cache invalidation)
- `alembic/versions/0050_add_learning_config.py` (Alembic migration creating `learning_config` table and seeding default configurations)
- `tests/modules/learning/test_admin_learning_config_api.py` (63 dedicated tests covering bounds, exact phrase friction, role isolation, audit diffs, cache resilience, and wire contracts)

## 9. Files Modified
- `src/noorheroes/modules/learning/admin_api.py` (mounted `/learning/config/spaced-repetition` and `/learning/config/confidence-threshold` routes with canonical and direct aliases)
- `src/noorheroes/modules/learning/pronunciation_coaching_service.py` (wired dynamic confidence threshold resolution via `get_effective_confidence_threshold()` with safe fallback `0.70`)
- `src/noorheroes/modules/learning/spaced_repetition_scheduler.py` (wired dynamic decay weights and daily prompt cap resolution via `get_effective_config()` with safe fallbacks `{recency: 0.4, mastery_strength: 0.6}` and cap `2`)
- `src/noorheroes/core/exceptions.py` (registered `ConfirmationPhraseMismatchError` and `LearningConfigNotFoundError`)
- `src/noorheroes/core/i18n.py` (added 4-language localized translations for `CONFIRMATION_PHRASE_MISMATCH` and `LEARNING_CONFIG_NOT_FOUND` in `en`, `hi`, `ur`, `ar`)
- `FAST-API-INSTRUCTIONS.md` (updated Sections 5.2, 5.5, 6, 8, 9, 10, 11, 12, 15)
- `MASTER-README.md` (added Section 11.44 and Scenarios S-203 to S-225)
- `docs/NoorHeroes_Consolidated_Execution_Blueprint.md` (updated Phase 6 Overview, Item 180 row, and next active item pointer)
- `src/noorheroes/modules/learning/README.md` (added Section 2.19, Scenarios S-203 to S-225, and 716 test suite matrix)

## 10. Backend Requirements
- **Spaced Repetition Configuration**: `PUT /v1/admin/learning/config/spaced-repetition` — updates decay-function weights and `daily_review_prompt_cap` (default 2); restricted to `product_admin`/`ai_ops`.
- **Confidence Threshold Configuration**: `PUT /v1/admin/learning/config/confidence-threshold` — updates the 0.0–1.0 threshold used by B-04's confidence gate; restricted to `ai_ops`; requires a server-side-validated typed confirmation phrase (e.g., `"confirmation_phrase": "I understand"`) in the request body — reject the save if the phrase doesn't match exactly, as extra friction for this sensitive lever.
- **Single active config row**: both configs are singleton settings (one active row per config type, not a history table) — updates overwrite in place, with the audit_log preserving the historical before/after diff for traceability.
- **Downstream consumption**: B-06 and B-04 must read from this config at runtime (or via a short-TTL cache) rather than using hardcoded defaults, with safe fallback defaults if the config row is somehow missing.

## 11. KMP Requirements
N/A (admin-only).

## 12. NextJS Requirements
Consumed by `N-04 Learning Configuration Panel`.

## 13. API Contract

**`PUT /v1/admin/learning/config/spaced-repetition`**
- **Auth:** `get_current_admin`, requires `product_admin` or `ai_ops` role
- **Request:** `{ "decay_weights": { "recency": 0.4, "mastery_strength": 0.6 }, "daily_review_prompt_cap": 2 }`
- **Response 200:** updated config
- **Error Responses:** `401`, `403`, `422` (invalid weights/cap out of bounds)

**`PUT /v1/admin/learning/config/confidence-threshold`**
- **Auth:** `get_current_admin`, requires `ai_ops` role
- **Request:** `{ "threshold": 0.7, "confirmation_phrase": "I understand" }`
- **Response 200:** updated config
- **Error Responses:** `401`, `403`, `422` (threshold out of 0.0–1.0 range, or confirmation phrase mismatch)

## 14. Database Requirements
`learning_config` table: `config_key PK` (e.g., `"spaced_repetition"`, `"confidence_threshold"`), `config_value JSONB`, `updated_at`, `updated_by_admin_id`. Singleton-per-key pattern.

## 15. Validation
- `daily_review_prompt_cap` ≥ 1.
- `decay_weights` non-negative.
- `threshold` strictly within `[0.0, 1.0]`.
- `confirmation_phrase` must match exactly (server-side validated, not just a client-side UI gate).

## 16. Authentication
Bearer JWT, `get_current_admin`.

## 17. Authorization
`product_admin`/`ai_ops` for spaced-repetition config; `ai_ops` only for confidence threshold — stricter role for the more safety-sensitive lever.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Confirmation phrase mismatch | `422`, save rejected |
| Wrong role | `403` |
| Out-of-bounds values | `422` |
| Missing config row at runtime (B-04/B-06 read) | Fall back to safe hardcoded defaults, log warning |

## 19. Offline First
N/A (admin backend).

## 20. Local Data
N/A (admin backend).

## 21. Localization
N/A (numeric/technical config, no user-facing text).

## 22. RTL
N/A.

## 23. Analytics
N/A (admin audit logging only — every config change is a P1 auditable event given downstream child-safety impact of the confidence threshold specifically).

## 24. Performance
Config reads by B-04/B-06 should be cached with a short TTL (config changes infrequently) to avoid a DB round-trip on every recitation request.

## 25. Security
Confidence-threshold changes are treated as a sensitive, deliberate-friction action: `ai_ops`-only role plus mandatory typed confirmation, both enforced server-side (never trust a client-only confirmation gate). Every change is audit-logged with before/after diff given the downstream safety implications.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0, Pydantic v2. No new dependencies.

## 27. Testing
- Unit: validation bounds (cap ≥1, weights non-negative, threshold in range).
- Unit: confirmation-phrase exact-match enforcement.
- Integration: wrong role rejected for each config route (`product_admin`/`ai_ops` vs `ai_ops`-only distinction verified).
- Integration: successful update reflected immediately in B-04's/B-06's next config read (cache invalidation or short-TTL expiry verified).
- Integration: audit_log entry created with correct before/after diff on every successful update.

## 28. Documentation
OpenAPI docstring for the confidence-threshold route explicitly documents the friction requirement and why (downstream child-safety impact).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `learning_config` Model & Migration**
- Task ID: B-11-T01
- Status: Completed ✅
- Files Created: `src/noorheroes/modules/learning/learning_config_models.py`, `alembic/versions/0050_add_learning_config.py`.
- Implementation Details: `LearningConfig` ORM model mapped to `learning_config` table with singleton-per-key pattern, cross-dialect `JSONType`, and `updated_by_admin_id`. Migration auto-seeds safe defaults for `"spaced_repetition"` (`decay_weights: {recency: 0.4, mastery_strength: 0.6}`, `daily_review_prompt_cap: 2`) and `"confidence_threshold"` (`threshold: 0.70`).
- Dependencies: None.
- Definition of Done: Migration applies cleanly with seeded defaults present.

**Task 02 — Implement `LearningConfigRepository`**
- Task ID: B-11-T02
- Status: Completed ✅
- Files Created: `src/noorheroes/modules/learning/learning_config_repository.py`.
- Implementation Details: Async repository with atomic PostgreSQL `ON CONFLICT (config_key) DO UPDATE` and SQLite fallback, short-TTL (300s) Redis caching with immediate cache invalidation on updates, and corrupt cache resilience.
- Dependencies: B-11-T01.
- Definition of Done: Repository unit and integration tests pass.

**Task 03 — Implement `AdminLearningConfigService`**
- Task ID: B-11-T03
- Status: Completed ✅
- Files Created: `src/noorheroes/modules/learning/admin_learning_config_service.py`, `src/noorheroes/modules/learning/learning_config_schemas.py`.
- Implementation Details: Validation (cap $\in [1, 50]$, non-negative weights, threshold $\in [0.0, 1.0]$, typed confirmation phrase exact match `"I understand"` with `str_strip_whitespace=False`) + atomic `AdminAuditRecord` logging with before/after state diffs.
- Dependencies: B-11-T02.
- Definition of Done: Unit and service tests pass.

**Task 04 — Wire Admin Router with Role-Specific RBAC**
- Task ID: B-11-T04
- Status: Completed ✅
- Files Created/Modified: `src/noorheroes/modules/learning/admin_api.py`, `src/noorheroes/api/v1/router.py`, `main.py`.
- Implementation Details: Distinct role checks per route (`product_admin`/`ai_ops` for spaced repetition vs strictly `ai_ops`-only for confidence threshold); triple-route wire parity (`/v1/admin/learning/config/...`, `/v1/admin/config/...`, `/admin/v1/config/...`).
- Dependencies: B-11-T03.
- Definition of Done: Endpoints reachable, RBAC verified per route.

**Task 05 — Wire Downstream Consumption in B-04/B-06**
- Task ID: B-11-T05
- Status: Completed ✅
- Files Modified: `src/noorheroes/modules/learning/pronunciation_coaching_service.py`, `src/noorheroes/modules/learning/spaced_repetition_scheduler.py`.
- Implementation Details: Dynamic configuration resolution via `get_effective_confidence_threshold()` and `get_effective_config()` with safe fallback defaults (`0.70`, `{recency: 0.4, mastery_strength: 0.6}`, cap `2`).
- Dependencies: B-11-T02, B-04-T05, B-06-T03.
- Definition of Done: Integration tests confirm config updates dynamically govern B-04 recitation feedback gating and B-06 review interval calculations.

**Task 06 — Tests**
- Task ID: B-11-T06
- Status: Completed ✅
- Objective: Full coverage per §27.
- Files Created: `tests/modules/learning/test_admin_learning_config_api.py` (63 tests) + 4 downstream integration tests in `test_pronunciation_coaching_service.py` and `test_spaced_repetition_scheduler.py`.
- Dependencies: B-11-T01–T05.
- Definition of Done: All green in CI (671 total learning module tests passing, 100% green).

**Task 07 — API Documentation**
- Task ID: B-11-T07
- Status: Completed ✅
- Dependencies: B-11-T04.
- Definition of Done: OpenAPI 3.1.0 specifications complete across 8 status codes (200, 400, 401, 403, 404, 422, 429, 500), friction rationale documented across `FAST-API-INSTRUCTIONS.md`, `MASTER-README.md`, and `learning/README.md`.

## 30. Definition of Done
✅ **FULLY ACHIEVED**: Both configuration endpoints live with strict role-specific RBAC, server-side typed confirmation phrase `"I understand"` enforced as a non-bypassable friction gate, live downstream consumption across B-04 and B-06 with safe fallbacks and Redis cache invalidation, atomic `AdminAuditRecord` logging with before/after diffs, fully tested (63 dedicated tests, 671 total learning module tests) and documented across `FAST-API-INSTRUCTIONS.md`, `MASTER-README.md`, and `learning/README.md`.

## 31. Final Verification Checklist
- [x] `product_admin`/`ai_ops` roles correctly distinguished per route
- [x] Confirmation phrase server-side validated (not just a UI-layer gate) for confidence-threshold changes
- [x] Bounds validation enforced (cap ≥1, weights non-negative, threshold in [0.0, 1.0])
- [x] B-04 and B-06 read live config values (not hardcoded), with safe fallback defaults
- [x] Every config change produces an audit_log entry with before/after diff
- [x] Full test suite green in CI
