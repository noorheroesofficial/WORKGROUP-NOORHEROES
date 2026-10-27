# Feature A.1 — Architecture Decisions Log

This log records every open question the first generation pass of the B/K/N blueprints deliberately flagged rather than guessed, and the resolution applied on the follow-up pass after re-checking `FAST-API-INSTRUCTIONS.md`, `NEXT-JS-INSTRUCTIONS.md`, and the KMP `Core setup manuals` against each flag. Kept here so a future blueprint (for A.1 or any other feature) doesn't re-litigate the same questions from scratch.

---

### 1. B-02 — Does `auth_identifier` replace or complement the existing `User.email` login?
**Finding:** `FAST-API-INSTRUCTIONS.md` §5.1 documents the `identity` context as having only `User.email` + password login today, with no phone field and no multi-identifier table.
**Decision:** `auth_identifier` is permanently additive. The existing password-login endpoint (`POST /v1/identity/auth/login/json`) is untouched; a `User` gains a linked `auth_identifier` row only when they register/login via phone-OTP, email-OTP, or Google.
**File updated:** `Backend/02-parent-registration-otp-authentication-api.md`

### 2. B-06 — Does an existing column-level encryption pattern exist for child PII?
**Finding:** No encryption-at-rest utility (pgcrypto/AES/`EncryptedType`) appears anywhere in the documented Infrastructure Layer or Master Reference Table — PRD §12.6's requirement for encrypted `nickname`/`dob` is real and currently unmet.
**Decision:** Build a new, reusable `common/security/encrypted_column.py` (SQLAlchemy `TypeDecorator`, AES-256-GCM, key from a named `Settings` var) and apply it to `ChildProfile.nickname`/`.dob` only, deliberately placed for other modules to adopt later rather than scoped as a one-off child-data hack.
**File updated:** `Backend/06-family-child-profile-management-api.md` (new Task 07, new files, updated checklist)

### 3. B-07 — Does an analytics warehouse / rollup layer exist for funnel and OTP-health reporting?
**Finding:** No warehouse, OLAP store, or rollup/materialized-view infrastructure is documented anywhere — only Postgres, Redis, R2, Celery, and `outbox_events` + `OutboxRelay`. The PRD's "Analytics Event Bus" is aspirational language, not an existing component.
**Decision:** Build the rollup **inside the existing Postgres instance**: two new tables (`onboarding_funnel_rollup`, `otp_health_rollup`) populated by a new periodic Celery task (`compute_onboarding_rollups_task`), modeled directly on the already-existing `retry_failed_translations_task` periodic-task pattern. Both admin endpoints read only from these tables.
**Side effect:** Added `remote_config.otp_health_threshold_pct` (default 95.0) so the alert threshold is admin-tunable via B-09 instead of hardcoded, resolving B-07 §20's secondary open question in the same pass.
**Files updated:** `Backend/07-admin-onboarding-funnel-otp-health-monitoring-api.md` (rewritten §6–§10, §12, error table, Task list, checklist), `Backend/01-bootstrap-remote-configuration-api.md` (new column), `Backend/09-admin-remote-configuration-release-management-api.md` (new field in `PUT` contract)

### 4. B-08 — Does an admin-side step-up MFA dependency already exist for the 15-minute Consent Audit freshness check?
**Finding:** `require_elevated_session(parent, redis)` exists but is typed to `ParentSessionContext` specifically (mobile-app PIN/biometric step-up) — there is no `AdminSessionContext` equivalent.
**Decision:** Add `require_elevated_admin_session(admin, redis)` to `core/deps.py`, mirroring the existing function's Redis-marker structure exactly, keyed on `admin_id` instead of `parent_id`. Not a discovery task — a build task.
**File updated:** `Backend/08-admin-consent-audit-risk-review-api.md` (§7, §9, §10, Task 01, new test file)

### 5. K-03 — Does `NoorPinInput` already support OTP-specific behaviors (auto-advance, paste-distribution, auto-submit)?
**Finding:** `CORE_UI_INSTRUCTIONS.md` describes the component only as "secure PIN/OTP entry with automatic masking" — none of the three OTP-specific UX behaviors are in its documented capability list.
**Decision:** Treat as confirmed-absent. Extend `NoorPinInput` with new **opt-in** constructor parameters (`autoAdvance`, `onComplete`) so existing non-OTP callers (e.g., K-05's PIN pad, which must *not* auto-submit) are unaffected by default.
**File updated:** `KMP/03-registration-consent-otp-verification-flow.md` (§6, §7, Task 03)

### 6. K-05 — Does an existing local (on-device) parent-PIN verification store exist?
**Finding:** `core-data`'s `ChildLockRepository.verifyChildLock()` is documented specifically for *child*-lock entry (a different credential/table). `core-security` documents `AuthState.Parent.elevatedUntil` (freshness tracking) and `CredentialHasher` (the hash primitive) but no repository that persists the *parent's own* PIN hash locally.
**Decision:** Build a new `ParentPinLocalStore` in `core-security`, co-located with `CredentialHasher`/`TokenStore`, using `TokenStore`'s existing secure-platform-storage pattern (EncryptedSharedPreferences/Keychain). A successful local verify updates `AuthState.Parent.elevatedUntil` via the existing `MutableAuthStateHolder` — the new store only owns the hash, not elevation state.
**File updated:** `KMP/05-parent-pin-biometric-enrollment-flow.md` (§7, §8, Task 02)

### 7. K-06 — Should idempotency keys use `UUID.randomUUID()` (per the PRD's own AI-prompt) or an existing project utility?
**Finding:** `core-common`'s `id` package is explicitly documented as covering "sortable unique ID generation (ULID) **and idempotency keys**," with `Ulid.randomULID(clock)` as the standardized call.
**Decision:** Use `Ulid.randomULID(clock)`, deliberately overriding the PRD's own generic prompt wording, per this project's stated rule that existing architecture takes precedence over PRD boilerplate when the two conflict.
**File updated:** `KMP/06-add-child-profile-flow.md` (§7)

### 8. K-07 — Should the onboarding draft persist via `core-datastore` (DataStore) or `core-database` (Room)?
**Finding:** `CORE_DATASTORE_INSTRUCTIONS.md` explicitly rules out its own use for this shape of data: "❌ Complex Data... ❌ Heavy Data: Do not store JSON blobs or large lists. Use `core-database`." The onboarding draft (multiple children × many fields, each with its own idempotency key) is exactly that shape.
**Decision:** Room, via a new `OnboardingDraftEntity`/`OnboardingDraftDao`, written through the existing `SafeDatabaseHelper.withTransaction()` pattern every other `core-database` write path already uses.
**File updated:** `KMP/07-onboarding-draft-persistence-resume-offline-sync.md` (§6–§8, Task 01–02, checklist)

### 9. K-08 — Does `ChildLockRepository.verifyChildLock()` actually exist, and with what signature?
**Finding:** Its *existence and behavior* are already confirmed by `CORE_DATA_INSTRUCTIONS.md`'s own "Handling 'Child Mode' Entry" usage scenario — this was never really in doubt. What the docs don't give is the *exact Kotlin signature*.
**Decision:** Narrowed Task 01 from "confirm it exists" to "read the source to pin down the exact signature" — a much smaller, correctly-scoped task.
**File updated:** `KMP/08-profile-picker-child-lock-first-mission-flow.md` (Task 01)

### 10. N-01/N-02 — What `AdminPermission` string should gate the two reporting dashboards?
**Finding:** `NEXT-JS-INSTRUCTIONS.md` doesn't enumerate the full `AdminPermission` union, but its one worked example (`RequirePermission permission="users:read"`) establishes a clear `resource:action` naming convention, consistent with the backend's own `admin:read`/`admin:write` scope style.
**Decision:** Add `"analytics:read"` to `AdminPermission` and gate both N-01 and N-02 behind it — a new, specific frontend permission backed by the same broad `admin:read` capability server-side (B-07).
**Files updated:** `NextJS_Admin/01-onboarding-funnel-dashboard.md`, `NextJS_Admin/02-otp-delivery-health-monitor.md`

### 11. N-05 — Does an endpoint exist for the Remote Config panel's change-history list?
**Finding:** `FAST-API-INSTRUCTIONS.md` §6 confirms `GET /v1/admin/audit-logs` already exists (`admin:read`, paginated audit logs) — this was resolvable, not actually blocked.
**Decision:** `ConfigChangeHistory` reuses this existing endpoint. If it doesn't yet accept a `resource_type` filter param, add one as a small backward-compatible extension; otherwise filter client-side on the existing `action`/`resource_type` fields already present on each `AdminAuditLog` row (confirmed reused by B-08 too).
**File updated:** `NextJS_Admin/05-remote-configuration-release-management-panel.md` (§10, Task 06, checklist)

---

## Net new backend surface introduced by this resolution pass
- `common/security/encrypted_column.py` — new shared PII-encryption primitive (item 2)
- `onboarding_funnel_rollup`, `otp_health_rollup` tables + `compute_onboarding_rollups_task` (item 3)
- `remote_config.otp_health_threshold_pct` column (item 3)
- `core/deps.py::require_elevated_admin_session` (item 4)
- Possible small `GET /v1/admin/audit-logs?resource_type=` filter param (item 11, only if not already present)

## Net new KMP surface introduced by this resolution pass
- `NoorPinInput` opt-in `autoAdvance`/`onComplete` parameters (item 5)
- `core-security/ParentPinLocalStore.kt` (item 6)
- `core-database/entity/OnboardingDraftEntity.kt` + `OnboardingDraftDao.kt` (item 8)

## Net new NextJS Admin surface introduced by this resolution pass
- `AdminPermission` value `"analytics:read"` (item 10)

None of these require re-opening B-01, B-03, B-04, B-05, B-09, K-01, K-02, K-04, N-03, or N-04 — those blueprints had no flagged open questions in the first pass.
