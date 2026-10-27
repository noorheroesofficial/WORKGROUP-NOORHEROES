# B-06 — Family Child Profile Management API

## 1. Feature Context
Creates and lists child profiles under a family account. This is the endpoint the existing `identity` module already partially implements (`IdentityService.create_child_profile()`, `IdentityRouter`'s `POST/GET /v1/identity/family/children`) — this sub-feature **extends** that existing implementation with the onboarding-specific fields (DOB-only age input, idempotency, avatar/interests) rather than replacing it.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
1.6 Family Child Profile Management API (ID: **B-06**)

## 4. Objective
Extend the existing child-creation endpoint with DOB-derived age banding, idempotency-key enforcement (DB-constraint-backed, not in-memory), duplicate-nickname disambiguation, and the full onboarding field set, while preserving the existing entitlement-cap check already wired to `SubscriptionService`.

## 5. Business Requirements
- FR-13: Add Child requires nickname, DOB, avatar, preferred language, learning level; must NOT expose a raw "age" field — age band always server-derived from DOB, recalculated automatically on the child's birthday.
- FR-14: Optional fields — interests, daily learning goal, AI/voice permission toggle (default OFF), accessibility preferences.
- FR-15: Duplicate nicknames within a family allowed only if distinguished by avatar/color, with explicit parent confirmation.
- FR-17: Child profile creation idempotent via client-generated idempotency key on `POST /v1/family/children`, preventing duplicates from retried requests.
- Edge Cases: DOB implying age >17 → block with explanatory copy (default policy); DOB implying age <3 → block with explanatory copy and support link; two children with identical nickname+DOB+avatar → second save blocked with clarification prompt.
- Negative Test: same Idempotency-Key + different body → server returns the *original* response (idempotency key wins over body diff).

## 6. Existing Architecture
Extends existing `IdentityService.create_child_profile()` / `ChildRepository` / `IdentityRouter`. Existing flow already checks `SubscriptionService.get_entitlement()` for family child-count caps and emits `ChildProfileCreated` via `OutboxWriter` — preserve this exactly, only adding the new fields/validations around it.

## 7. Existing Code to Reuse
- `modules/identity/service.py::IdentityService.create_child_profile()` (extend in place)
- `modules/identity/repository.py::ChildRepository.get_by_family_id()`, `get_child_by_id_and_family()`
- `modules/subscriptions/service.py::SubscriptionService.get_entitlement()` (existing entitlement-cap check — do not duplicate)
- `common/outbox.py::OutboxWriter` (existing `ChildProfileCreated` event — do not rename)
- `common/utils/age_band.py::AgeBand` enum — canonical 5 bands (`BAND_4_TO_6`, `BAND_6_TO_9`, `BAND_9_TO_12`, `BAND_12_TO_15`, `BAND_15_TO_18_PLUS`, with values `"4 to 6"`, `"6 to 9"`, `"9 to 12"`, `"12 to 15"`, `"15 to 18+"`) derived deterministically from child date of birth.

## 8. Files to Create
- `alembic/versions/xxxx_extend_child_profile_add_dob_avatar_interests.py` — extends existing `ChildProfile` table
- `src/noorheroes/common/utils/age_band_calculator.py` — pure function `calculate_age_band(dob, today) -> AgeBand`, using the existing `AgeBand` enum from `common/utils/age_band.py`
- `src/noorheroes/modules/identity/onboarding_progress_models.py` — `ChildLockOrm`, `OnboardingProgressOrm`
- `alembic/versions/xxxx_add_child_lock_onboarding_progress.py`
- `src/noorheroes/scripts/recalculate_age_bands_job.py` — nightly scheduled job (Celery beat or equivalent) to roll children into new age bands on birthdays
- `src/noorheroes/common/security/encrypted_column.py` — new `EncryptedString`/`EncryptedDate` SQLAlchemy `TypeDecorator` (AES-256-GCM), resolving the column-level-encryption gap per §19
- `tests/modules/identity/test_child_profile_extended.py`
- `tests/common/utils/test_age_band_calculator.py`
- `tests/common/security/test_encrypted_column.py`

## 9. Files to Modify
- `src/noorheroes/modules/identity/models.py::ChildProfile` — add `dob`, `age_band`, `avatar_id`, `preferred_language`, `learning_level`, `interests` (jsonb), `daily_goal_minutes`, `ai_voice_permission`, `accessibility_prefs` (jsonb), `idempotency_key` columns; add CHECK constraint `dob` between 3–18 years; add `UNIQUE(family_id, idempotency_key)`
- `src/noorheroes/modules/identity/service.py::create_child_profile()` — add DOB validation, age-band calculation, duplicate-nickname disambiguation logic, idempotency-key replay handling
- `src/noorheroes/modules/identity/schemas.py::ChildProfileCreateRequest`/`ChildProfileResponse` — extend with new fields
- `src/noorheroes/modules/identity/api.py::create_child` — require `Idempotency-Key` header

## 10. Backend Requirements
- Idempotency: `Idempotency-Key` header required; enforced via `UNIQUE(family_id, idempotency_key)` DB constraint, not in-memory dedup (per PRD backend AI-prompt requirement #3). On replay with the same key (regardless of body diff), return the original `201` response — look up the existing row by the constraint before attempting insert.
- Age band: computed via pure `calculate_age_band(dob, today)` function at creation time; a nightly scheduled job re-runs this for every active child and updates `age_band` if changed (birthday rollover) — not just computed once at creation.
- DOB CHECK constraint: `dob <= current_date - interval '3 years' AND dob >= current_date - interval '18 years'` at the database level, mirrored by a `422 INVALID_DOB` app-level check for a friendlier error message before hitting the DB constraint.
- Duplicate nickname: non-unique index on `(family_id, nickname)` (duplicates structurally allowed); service-layer check returns `409 DUPLICATE_NICKNAME` with the existing child's summary (name, avatar) for client-side disambiguation UI — client must re-submit with explicit confirmation (a `confirmed_duplicate: true` flag) to proceed.
- Preserve existing `SubscriptionService.get_entitlement()` cap check exactly as implemented — `403 CHILD_LIMIT_REACHED` on breach.

## 11. API Contract

### `POST /v1/identity/family/children` (extends existing endpoint)
- Auth: Bearer (parent). Headers: `Idempotency-Key` (required, new). Request: `{nickname, dob, avatar_id, preferred_language, learning_level, interests[], daily_goal_minutes, ai_voice_permission, accessibility, confirmed_duplicate?}`. Response 201: `{child_id, age_band}`. Errors: `422 INVALID_DOB`, `409 DUPLICATE_NICKNAME`, `403 CHILD_LIMIT_REACHED`. Rate limit: 10/min/family.

### `GET /v1/identity/family/children` (existing, unchanged)
- Auth: Bearer (parent). Response: family + children summary list for Profile Picker. Cache: 30s client-side, invalidated on mutation.

## 12. Database Requirements
Extends existing `ChildProfile`/`child` table per §4.2 with the columns in §9; new `child_lock` table (`lock_id` PK, `child_id` FK, `lock_type` CHECK IN `('pin','pattern','biometric_flag')`, `lock_value_hash`, `failed_attempts`, `locked_until`); new `onboarding_progress` table (`progress_id` PK, `family_id` FK UNIQUE, `last_completed_step`, `draft_data` jsonb, `updated_at`) — supports K-07's resume-after-kill requirement server-side as a durable backstop to the client-side DataStore draft.

## 13. Validation
- DOB required, age band always server-derived — schema must not accept a raw `age` field at all (physically absent from `ChildProfileCreateRequest`).
- `Idempotency-Key` header required — reject with `422` if absent (do not silently proceed without idempotency protection).

## 14. Authentication
Bearer token via existing `get_current_parent`.

## 15. Authorization
Parent-scope only; existing child-count-cap entitlement check preserved.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| DOB implies age <3 or >18 | `422 INVALID_DOB`, explanatory message, link to support for edge cases |
| Duplicate nickname, no `confirmed_duplicate` flag | `409 DUPLICATE_NICKNAME` + existing child summary |
| Same idempotency key, different body | Return the original `201` response verbatim — body diff is ignored |
| Family at child-count cap | `403 CHILD_LIMIT_REACHED` (existing `EntitlementLimitExceededError`) |
| Missing `Idempotency-Key` header | `422` |

## 17. Analytics
Emit `add_child_started`, `avatar_selected`, `interest_selected`, `learning_level_selected`, `add_child_submitted`, `add_child_succeeded` (with `age_band`, `latency_ms`), `add_child_failed` (with `error_code`), `add_another_child_prompted` via `OutboxWriter` — extends the existing `ChildProfileCreated` event, does not replace it.

## 18. Performance
- Rate limit: 10 req/min/family.
- Idempotency lookup must use the `UNIQUE(family_id, idempotency_key)` index — single indexed lookup before insert, not a full scan.
- Nightly age-band recalculation job must batch-process (not one query per child) to avoid a full-table N+1 on large datasets.

## 19. Security
- `accessibility_prefs`/`interests` stored as jsonb — validate shape server-side (Pydantic) before persisting, do not accept arbitrary unvalidated JSON blobs.
- **Resolved architecture decision — column-level encryption:** `FAST-API-INSTRUCTIONS.md` documents no existing column-level encryption utility anywhere in the codebase (the Infrastructure Layer and Master Reference Table list `R2StorageService`, `AIProviderFactory`, Redis, and telemetry, but no `EncryptedType`/pgcrypto/AES helper). PRD §12.6 explicitly requires column-level encryption for `child.nickname` and `child.dob` in addition to disk-level encryption — this is a real, currently-unmet requirement, not a false alarm. Resolution: this sub-feature adds a small, reusable `common/security/encrypted_column.py` providing a SQLAlchemy `TypeDecorator` (AES-256-GCM via `cryptography`'s `Fernet`/`AESGCM`, key sourced from a named env var through the existing `Settings` singleton — never hardcoded, never a new bespoke key-management system) and applies it to `ChildProfile.nickname` and `ChildProfile.dob` only. This utility is intentionally placed in `common/security/` (not `modules/identity/`) so other modules with sensitive PII columns can adopt the same decorator later — flag this in code review as a new cross-cutting primitive, not a one-off hack scoped only to children.

## 20. Library Requirements
No new dependencies — reuses existing SQLAlchemy/Alembic/Pydantic stack.

## 21. Testing
- Unit: `calculate_age_band()` boundary tests (exactly 3 years − 1 day → reject at schema/DB layer if tested there; exactly 18 years → boundary-inclusive per CHECK constraint wording — confirm inclusive/exclusive semantics match the PRD's CHECK constraint exactly).
- Integration: idempotency replay with identical key + different body → original response returned; duplicate-nickname flow with and without `confirmed_duplicate`; entitlement-cap breach still returns `403` (regression test against existing behavior); nightly age-band job correctly rolls a child from one band to the next on a simulated birthday.

## 22. Documentation
Update OpenAPI for the extended request/response schemas; note the idempotency-key requirement prominently since it's a breaking addition to an existing endpoint's contract (existing clients must be updated to send the header).

## 23. AI Coding Agent Implementation Steps

**Task 01 — Extend `ChildProfile` Model & Migration**
Objective: Add DOB/avatar/interests/idempotency columns to the existing table. Why: current model only supports basic child CRUD, not the full onboarding field set. Follow: existing `ChildProfile` model conventions in `modules/identity/models.py`. Files to Modify: `models.py`, new migration file. Business Rules: `UNIQUE(family_id, idempotency_key)`, DOB CHECK constraint. Do Not Change: do not rename or remove any existing `ChildProfile` column consumed elsewhere (check `LearningService`/`RewardService` for existing references before altering). Tests: migration smoke test on a DB seeded with existing child rows (backward-compatibility check). Definition of Done: existing child rows still readable after migration; new columns nullable-safe for legacy rows or backfilled with sensible defaults.

**Task 02 — Implement `calculate_age_band()` Pure Function**
Objective: DOB → `AgeBand` enum mapping. Why: FR-13 mandates server-only age derivation. Follow: `common/utils/` pure-function pattern (mirrors `common/utils/streak.py` style). Reuse: existing `AgeBand` enum — do not create a second age-band type. Tests: boundary values exactly matching the DOB CHECK constraint's 3–18 year window. Definition of Done: 100% branch coverage, enum values match existing `AgeBand` semantics.

**Task 03 — Implement Nightly Age-Band Recalculation Job**
Objective: Batch job rolling children into new bands on birthdays. Why: PRD explicitly requires recalculation "not just at creation time." Follow: existing Celery task pattern from `modules/localization/tasks.py` (e.g., `retry_failed_translations_task` as a periodic-task style reference). Files to Create: `scripts/recalculate_age_bands_job.py`. Business Rules: batch update, not per-child queries. Tests: simulated-birthday integration test. Dependencies: Task 02. Definition of Done: job correctly updates `age_band` for a batch of children with today's date as a birthday, in a single batched operation.

**Task 04 — Extend `IdentityService.create_child_profile()`**
Objective: Wire idempotency-key DB-constraint handling, DOB validation, duplicate-nickname disambiguation into the existing method — without disturbing the existing `SubscriptionService.get_entitlement()` call or `OutboxWriter.emit()` call. Follow: existing method structure, insert new validation steps around the existing core logic. Business Rules: idempotency-key replay returns original response (catch the unique-constraint violation, look up and return the existing row, do not treat it as an error). Tests: full matrix per §21. Dependencies: Tasks 01–02. Definition of Done: existing entitlement-cap test still passes unmodified (regression-safe), all new validation tests pass.

**Task 05 — Extend Request/Response Schemas & Router**
Objective: Add new fields to `ChildProfileCreateRequest`/`ChildProfileResponse`, require `Idempotency-Key` header in the router. Follow: existing schema/router conventions. Files to Modify: `schemas.py`, `api.py`. Tests: covered by Task 06. Definition of Done: schema physically excludes a raw `age` field.

**Task 06 — Create `child_lock` and `onboarding_progress` Tables**
Objective: Support K-08 (child lock) and K-07 (server-side onboarding-progress backstop). Follow: standard migration conventions. Business Rules: `onboarding_progress` is `UNIQUE(family_id)` — one draft row per family. Tests: migration smoke test. Definition of Done: both tables created, ready for their respective KMP sub-features to read/write.

**Task 07 — Implement `EncryptedString`/`EncryptedDate` Column Type and Apply to `nickname`/`dob`**
Objective: Resolve the column-level-encryption gap identified in §19 by building a small, reusable SQLAlchemy `TypeDecorator` and applying it to the two PII columns PRD §12.6 specifically calls out. Why: no existing encryption-at-rest utility exists anywhere in the documented architecture (confirmed by searching `FAST-API-INSTRUCTIONS.md`'s Infrastructure Layer and Master Reference Table). Follow: `cryptography` library's `AESGCM`, key sourced by name from the existing `Settings` singleton (e.g. `CHILD_PII_ENCRYPTION_KEY`), never hardcoded. Files to Create: `common/security/encrypted_column.py`, `tests/common/security/test_encrypted_column.py`. Business Rules: encryption/decryption is transparent to the ORM layer (application code reads/writes plain Python `str`/`date` values; the `TypeDecorator` handles ciphertext at the DB boundary) — no other module's code should need to know the column is encrypted. Security: key rotation is out of scope for this task but the key must be referenced by a named, documented env var so rotation is possible later without a schema change. Tests: round-trip encrypt/decrypt test; DB-level test confirming raw `SELECT` of the column returns ciphertext, not plaintext. Definition of Done: `nickname` and `dob` are unreadable as plaintext via a raw SQL query against the table, verified by a test connecting directly (bypassing the ORM) and asserting the stored value is not the plaintext value.

**Task 08 — Add Unit & Integration Tests**
Objective: Full coverage per §21, including the explicit idempotency-key-wins-over-body-diff negative test called out in the PRD's QA section. Definition of Done: all green in CI, including a regression run of pre-existing `create_child`/`list_children` tests.

**Task 09 — Update OpenAPI Documentation**
Objective: Regenerate; explicitly flag the new required `Idempotency-Key` header as a contract change for existing API consumers. Definition of Done: diff classifier run and reviewed (this change is *additive to the schema* but *behaviorally breaking* for any caller not yet sending the header — document this clearly even if the classifier marks it non-breaking at the schema level).

**Task 10 — Final Code Review**
Objective: Confirm no regression to existing entitlement-cap or `ChildProfileCreated` event behavior; confirm age-band-only (no raw age field) end-to-end; confirm `nickname`/`dob` are genuinely ciphertext at rest. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [x] `ChildProfile` extended without breaking existing rows/consumers
- [x] Idempotency enforced via DB unique constraint, not in-memory dedup
- [x] Idempotency replay with different body returns the *original* response
- [x] Age band always server-derived from DOB; no raw age field anywhere in the schema
- [x] Nightly recalculation job batches updates, doesn't iterate per-child
- [x] Duplicate-nickname flow requires explicit `confirmed_duplicate` before allowing a second save
- [x] Existing `SubscriptionService.get_entitlement()` cap check untouched and still passing its existing tests
- [x] `nickname`/`dob` are stored as ciphertext at rest (verified by a raw-SQL test), resolving the previously-open column-level-encryption question
- [x] `child_lock`/`onboarding_progress` tables created for K-07/K-08
- [x] No PostgreSQL credentials modified

## 25. Definition of Done
`POST/GET /v1/identity/family/children` now supports the full onboarding field set with DB-enforced idempotency, server-only age banding with nightly recalculation, and duplicate-nickname disambiguation — all built as a backward-compatible extension of the existing `IdentityService`, ready for K-06 (Add Child Profile flow) and K-08 (Profile Picker) to consume. Status: **Implemented & Verified**.
