# B-06 — Admin AI Interaction Retention Configuration API

## 1. Feature Context
Part of Feature C.26's Admin Requirements (§8). Lets Trust & Safety/AI Ops tune the retention window for AI interaction history, extending the same `ai_safety_event` table B-02 extends (per B-02's cross-feature resolution with C.22 B-03).

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**B-06 — Admin AI Interaction Retention Configuration API**

## 4. Objective
Implement an admin-tunable default retention window for AI interaction history entries, update-only, restricted to `trust_safety`/`ai_ops` roles, driving the `expires_at` value applied to `ai_safety_event` rows at ingestion time.

## 5. Business Requirements
- §8: "AI Interaction History Retention Configuration: Admin-tunable `expires_at` default window for `ai_interactions`, behind an elevated (`trust_safety`/`ai_ops`) role."
- CRUD permissions: Update-only.
- Cross-ref B-02: this configuration governs the `expires_at` boundary applied by the ingestion consumer B-02 extends (`ai_safety_event_consumer.py`, owned by C.22 B-03).

## 6. Existing Architecture
**Depends on B-02's resolution being adopted (extending C.22's `ai_safety_event` table rather than a new `ai_interactions` table).** If B-02's cross-feature sign-off has not yet happened, this sub-feature is also blocked, since it configures the same table's retention field — do not implement independently of B-02's Task 00 outcome.

Lives in `modules/admin/` as a small settings resource, reading/writing a single config value consumed by `modules/ai_safety`'s ingestion consumer — reuses the platform's existing settings/config pattern (`Settings`, per C.21 B-06's precedent of reading a Legal/Compliance-configured retention duration from `Settings` rather than hardcoding it).

## 7. Existing Code to Reuse
- `modules/admin/api.py` — existing `AdminRouter` RBAC pattern.
- `common/config/settings.py::Settings` (or equivalent) — precedent from C.21 B-06 for reading an admin-configured retention duration.
- `modules/ai_safety/ai_safety_event_consumer.py` (C.22 B-03, extended by B-02) — the consumer that must read this value when stamping `expires_at` on ingestion.

## 8. Files to Create
- `src/noorheroes/modules/admin/ai_retention_config_schemas.py`
- `tests/modules/admin/test_ai_retention_config.py`

## 9. Files to Modify
- `src/noorheroes/modules/admin/api.py` — add `GET /v1/admin/ai-interaction-retention-config`, `PATCH /v1/admin/ai-interaction-retention-config`
- A config table or existing platform-wide settings store — add `ai_interaction_retention_days` (confirm exact existing mechanism, e.g. a `platform_config` table if one exists, before adding a new one-off table for a single value)
- `modules/ai_safety/ai_safety_event_consumer.py` — read this value when stamping `expires_at` on each ingested row (coordinate as a shared task with B-02, do not duplicate the read logic)

## 10. Backend Requirements
- `GET` returns current default retention window (in days).
- `PATCH` validates the new value against sane data-minimization bounds (reject unbounded/absurdly large values, e.g. cap at a documented maximum — confirm the actual maximum with Trust & Safety rather than inventing an arbitrary number); persists; writes an immutable audit log row.
- Changing this value does **not** retroactively alter `expires_at` on already-ingested rows — only new ingestions after the change apply the new window (state this explicitly, since silently reinterpreting historical rows would be a data-integrity surprise).

## 11. API Contract

### `GET /v1/admin/ai-interaction-retention-config`
- **Response 200:** `{ "retention_days": 90 }`

### `PATCH /v1/admin/ai-interaction-retention-config`
- **Auth:** `trust_safety`/`ai_ops` role required
- **Request:** `{ "retention_days": 60 }`
- **Response 200:** `{ "updated": true, "retention_days": 60 }`
- **Errors:** `403` (wrong role), `422` (out of bounds)

## 12. Database Requirements
Single config value — store in the platform's existing config/settings table if one exists (confirm before creating a new one); if none exists, a minimal `platform_config(key TEXT PK, value TEXT, updated_at, updated_by)` table, generically reusable by future single-value admin settings rather than a table dedicated only to this one field.

## 13. Validation
`retention_days` positive integer, within a Trust & Safety-confirmed maximum bound.

## 14. Authentication
Existing admin session mechanism.

## 15. Authorization
`trust_safety`/`ai_ops` role strictly required — reject all other roles including `product_admin`.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Non-`trust_safety`/`ai_ops` role attempts update | `403` |
| Value outside confirmed bounds | `422` |
| Config store read failure | `500`, cached last-known value served if available (read-path resilience) |

## 17. Offline First
N/A.

## 18. Local Data
N/A.

## 19. Localization
N/A.

## 20. RTL
N/A.

## 21. Analytics
Standard admin audit logging.

## 22. Performance
Trivial single-value read/write, cacheable (short TTL) given the ingestion consumer reads it on every message.

## 23. Security
Elevated-role restriction is the primary control, given the data-minimization significance of this setting; audit trail on every change.

## 24. Library Requirements
No new libraries.

## 25. Testing
- Unit: non-`trust_safety`/`ai_ops` roles rejected.
- Unit: out-of-bounds values rejected.
- Integration: updated value is read by a fixture ingestion event and correctly stamps the new `expires_at` window, while a pre-existing row's `expires_at` is confirmed unchanged.
- Integration: audit log row written on update.

## 26. Documentation
OpenAPI must state explicitly that changes are forward-only (no retroactive reinterpretation of existing rows' `expires_at`).

## 27. AI Coding Agent Implementation Steps

**Task 00 — Confirm Dependency on B-02's Sign-Off**
- **Objective:** Verify B-02's cross-feature resolution (extending `ai_safety_event`) has been adopted before proceeding.
- **Definition of Done:** Confirmed, or this task explicitly deferred until B-02 unblocks.

**Task 01 — Confirm/Create Config Store**
- **Objective:** Locate existing platform-wide settings table or create a minimal reusable one.
- **Definition of Done:** Storage mechanism confirmed, not duplicated.

**Task 02 — Implement Read/Update Endpoints with RBAC**
- **Files to Modify:** `admin/api.py`.
- **Definition of Done:** Role restriction verified by test.

**Task 03 — Wire Consumer to Read Configured Value**
- **Files to Modify:** `ai_safety_event_consumer.py` (coordinate with B-02).
- **Definition of Done:** New ingestions use the current configured value; historical rows unaffected.

**Task 04 — Full Test Suite & Documentation**

## 28. Definition of Done
Retention window is admin-configurable behind the correct elevated role, forward-only in effect, fully audited, and correctly consumed by the (B-02-extended) ingestion consumer.

## 29. Final Verification Checklist
- [ ] Confirmed dependency on B-02's resolution before implementation
- [ ] `trust_safety`/`ai_ops` role strictly enforced
- [ ] Bounds validated against a confirmed maximum, not an invented number
- [ ] Change is forward-only; historical `expires_at` values unaffected
- [ ] Audit log row written on every change
- [ ] No PostgreSQL/Redis credential changes
