# B-05 — Consent Ledger & Privacy Preference API

> **Status:** ✅ **COMPLETED** (100% Implemented & Verified — 20 Dedicated Tests Passing, Alembic Migration 0007, Append-Only Repository & DB Grants Revoked, Outbox Events Registered)
> **Implementation Date:** 2026-09-01
> **Verification Suite:** `tests/modules/identity/test_consent_service.py`, `tests/modules/identity/test_consent_api.py`, `tests/modules/identity/test_consent_immutability.py`

## 1. Feature Context

The legal backbone of onboarding: an append-only, tamper-evident record of every consent decision a parent makes, before any child data is collected. This is the compliance proof for COPPA/GDPR-K and must survive account deletion (anonymized) as evidence of historical compliance.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
1.5 Consent Ledger & Privacy Preference API (ID: **B-05**)

## 4. Objective
Implement an append-only `consent_record` write path (called internally by B-02's registration flow) plus a parent-facing `POST /v1/identity/family/consent` endpoint for revoking/granting optional consents post-onboarding, with database-role-enforced immutability.

## 5. Business Requirements
- FR-5: 3 required + 3 optional consent flags at registration; required flags cannot be revoked without triggering account deletion.
- FR-19: Every consent decision recorded with consent text version, timestamp, IP-derived region (not raw IP retained long-term), source platform, and specific toggles granted/denied.
- FR-20: Each optional consent (personalization, voice, marketing) independently revocable later from Settings → Privacy & Support, without requiring re-onboarding.
- §4.4/§4.5: `consent_record` is never deleted, soft or hard — superseded by new rows only; retained indefinitely (or per regulation minimum) even post-deletion, anonymized.
- §12.1: Consent record tampering mitigated by append-only ledger with no UPDATE/DELETE database grant for the application role — defense in depth beyond app-layer checks.

## 6. Existing Architecture
New `ConsentLedgerService`/`ConsentRepository` inside `modules/identity/`, called synchronously from B-02's `register()` flow (same transaction) and independently from the new `/family/consent` endpoint for optional-consent updates.

## 7. Existing Code to Reuse
- `common/base_service.py::BaseService`, `common/base_repository.py::BaseRepository` (note: repository here deliberately does **not** expose update/delete methods, breaking from the typical `BaseRepository` CRUD surface — see Task 03)
- `core/deps.py::get_current_parent`
- `common/outbox.py::OutboxWriter`

## 8. Files to Create
- `src/noorheroes/modules/identity/consent_models.py` — `ConsentRecordOrm`
- `alembic/versions/xxxx_add_consent_record_table.py` (includes the DB-role grant restriction — see §12)
- `src/noorheroes/modules/identity/consent_schemas.py` — `ConsentUpdateRequest`, `ConsentUpdateResponse`
- `src/noorheroes/modules/identity/consent_repository.py` — `ConsentRepository` (append-only: `add_record()` only, no `update`/`delete`)
- `src/noorheroes/modules/identity/consent_service.py` — `ConsentLedgerService(BaseService)`
- `tests/modules/identity/test_consent_service.py`
- `tests/modules/identity/test_consent_api.py`
- `tests/modules/identity/test_consent_immutability.py` — dedicated DB-role-permission test

## 9. Files to Modify
- `src/noorheroes/modules/identity/api.py` — add `POST /v1/identity/family/consent`
- `src/noorheroes/modules/identity/service.py::register()` (B-02) — call `ConsentLedgerService.record_initial_consent()` inside the same transaction

## 10. Backend Requirements
- `ConsentLedgerService.record_initial_consent(family_id, parent_id, consent_payload, region, source_platform)`: called during registration; writes one `consent_record` row capturing all 6 flags + versions.
- `ConsentLedgerService.update_optional_consent(parent_ctx, payload)`: writes a **new** row (never mutates the prior row) reflecting the updated optional-consent state; required-consent fields are carried forward unchanged from the most recent row (cannot be altered via this path).
- Region derivation: resolve from request IP at write time, store the derived region string — do not persist the raw IP long-term (mirrors B-02's IP-hashing-after-30-days pattern, but here region is derived once and the source IP is discarded immediately, never stored).
- Reject any attempt to set a required consent field to `false` via `/family/consent` — that field is simply not accepted by this endpoint's schema (schema-level enforcement, not just a runtime check).

## 11. API Contract

### `POST /v1/identity/family/consent`
- Auth: Bearer (parent). Request: `{personalization, voice, marketing}` (optional consents only — required consents are not accepted fields on this schema at all). Response 200: `{updated: true, effective_at}`. Audit: every call appends a new ledger row.

## 12. Database Requirements
New table `consent_record` per §4.2: `consent_id` PK, `family_id` FK, `parent_id` FK, `terms_version`, `privacy_version`, `child_data_version`, `personalization_consent`, `voice_consent`, `marketing_consent`, `region`, `source_platform`, `recorded_at`. Index `(family_id, recorded_at DESC)`.
- **Critical migration requirement:** the Alembic migration must explicitly `REVOKE UPDATE, DELETE ON consent_record FROM <app_db_role>` (or equivalent `GRANT` statement omitting those privileges) — this must be enforced at the PostgreSQL role level, not merely absent from the ORM/repository code. This is the single most safety-critical line in this entire sub-feature.

## 13. Validation
- Registration-time write requires all 3 required flags `true` (enforced by B-02, not duplicated here — B-05 trusts the payload it receives from the same-transaction caller).
- `/family/consent` schema physically excludes required-consent fields — a client cannot even attempt to send them.

## 14. Authentication
Bearer token via existing `get_current_parent`.

## 15. Authorization
Parent-scope only for `/family/consent`. Read-only admin access to consent history is a separate concern (B-08).

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Attempted UPDATE/DELETE on `consent_record` (e.g., a bug elsewhere) | Rejected at the PostgreSQL role level — surfaces as a DB permission error, must be caught and mapped to a generic `500` with alerting, never silently swallowed |
| Missing/malformed optional-consent payload | `422` |
| Consent text/version fails to load at registration time (CDN/localization failure, client-side concern) | Not this endpoint's responsibility — registration blocks client-side per PRD §1.11; this API simply records whatever version string it's given |

## 17. Security
- Append-only enforcement is the primary security control here — verified by an explicit test (Task 04) that attempts an UPDATE and asserts DB-level rejection, per PRD backend AI-prompt requirement #10.
- No PII beyond what's already in `parent`/`family` — `region` is derived/generalized, not raw geolocation.

## 18. Analytics
Emit `consent_toggle_changed` (per-toggle) and `consent_full_text_opened` (client-driven, logged when the client reports opening a full document) via `OutboxWriter`.

## 19. Performance
Single-row append, indexed by `(family_id, recorded_at DESC)` for fast "most recent consent state" reads (used by Settings → Privacy screen and by B-08's audit viewer).

## 20. Compliance
- COPPA-aligned verifiable parental consent before child-data collection.
- GDPR-K equivalent data-subject rights honored via the separate account-deletion flow (out of scope here — this sub-feature only ensures the ledger itself is retained/anonymized correctly on deletion, coordinating with whatever deletion-flow feature owns that job).

## 21. Testing
- Unit: required-consent fields physically absent from `/family/consent` schema (schema introspection test, not just a runtime check).
- Integration: full registration → consent-record-written flow; optional-consent update → new row appended, old row untouched; **dedicated DB-permission test** — connect as the application role and attempt a raw `UPDATE`/`DELETE` on `consent_record`, assert it is rejected by Postgres itself.

## 22. Documentation
Document the DB-role grant restriction explicitly in the migration file's comments and in the module README, flagged as security-critical and not to be "fixed" by a future well-meaning developer who notices the missing UPDATE grant.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `consent_record` Table with Restricted Grants**
Objective: Append-only table, DB-role-enforced. Why: PRD's single most explicit "defense in depth" requirement in this whole feature. Follow: Alembic migration conventions, extended with raw `GRANT`/`REVOKE` SQL. Implementation: create table per §12 schema; in the same migration, explicitly revoke UPDATE/DELETE from the app's runtime DB role (identify the correct role name from existing `infrastructure/db/session.py` connection config — do not guess a role name, inspect the actual configured connection string/role). Security: this is the core control of the entire sub-feature. Tests: migration-level test connecting as the app role and confirming UPDATE fails. Do Not Change: do not grant these privileges "temporarily for testing" and forget to revoke — tests must run against the same restricted role, not a superuser. Definition of Done: UPDATE/DELETE both fail with a Postgres permission error when attempted as the app role.

**Task 02 — Implement `ConsentRecordOrm` and Repository (Append-Only)**
Objective: ORM model + repository exposing only `add_record()` and `get_latest_for_family()` — deliberately no `update`/`delete` methods, even though `BaseRepository` would normally provide them (do not inherit the mutation methods; either don't extend `BaseRepository` or override-and-raise on `update`/`soft_delete`/etc.). Why: app-layer mirror of the DB-layer restriction — defense in depth means both layers refuse mutation. Tests: attempting to call an update-style method (if inherited) raises immediately, before ever reaching the DB. Definition of Done: repository's public surface has zero mutation methods.

**Task 03 — Implement `ConsentLedgerService.record_initial_consent()`**
Objective: Registration-time consent write, called from within B-02's transaction. Follow: `BaseService`, region-derivation-then-discard-raw-IP pattern. Business Rules: called once per registration, captures all 6 flags. Security: raw IP never persisted — derive region, discard IP immediately. Tests: region derivation, all-flags-captured assertion. Dependencies: Task 02. Definition of Done: called correctly from B-02's flow without altering B-02's existing transaction boundaries.

**Task 04 — Implement `ConsentLedgerService.update_optional_consent()` + DB Immutability Test**
Objective: Post-onboarding optional-consent updates as new-row-appends; the dedicated immutability test from §21. Business Rules: required-consent fields carried forward unchanged, never accepted as input. Tests: new-row-appended-not-mutated assertion; the raw-SQL UPDATE/DELETE rejection test against the actual app DB role (this is the most important single test in this sub-feature). Dependencies: Tasks 01–03. Definition of Done: immutability test passes against the real restricted role, not a mocked permission check.

**Task 05 — Add Router Endpoint**
Objective: Wire `POST /v1/identity/family/consent`. Follow: existing router conventions. Tests: covered by Task 06. Definition of Done: endpoint live, schema physically excludes required-consent fields.

**Task 06 — Add Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all green in CI, including the DB-role permission test running in the actual CI Postgres instance (not skipped/mocked).

**Task 07 — Update OpenAPI Documentation**
Objective: Regenerate, confirm non-breaking diff. Definition of Done: diff classifier passes.

**Task 08 — Final Code Review**
Objective: Confirm append-only enforcement exists at both the app-code layer and the DB-role layer, confirm B-02's registration flow correctly calls this service inside its existing transaction (no dual-write/orphan-record risk). Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [x] `consent_record` table created with UPDATE/DELETE revoked from the app DB role (verified by `tests/modules/identity/test_consent_immutability.py`)
- [x] `ConsentRepository` exposes no mutation methods (`update`, `delete`, `soft_delete` raise `PermissionError`)
- [x] Registration-time write happens inside B-02's existing transaction (`OtpAuthService.verify_otp()` synchronous invocation)
- [x] Optional-consent updates always append a new row, never touch prior rows
- [x] Required-consent fields are schema-excluded from `/family/consent` (`extra="forbid"`), not just runtime-rejected
- [x] Raw IP never persisted — only derived region (`ConsentLedgerService.derive_region()`)
- [x] `consent_toggle_changed` analytics event emitted on every optional-consent change
- [x] No PostgreSQL credentials modified


## 25. Definition of Done
The consent ledger is genuinely append-only at both the application and database-role levels, verified by a real permission test, correctly wired into B-02's registration transaction, and exposes a schema-safe optional-consent update path — the compliance backbone the entire onboarding feature depends on is in place.
