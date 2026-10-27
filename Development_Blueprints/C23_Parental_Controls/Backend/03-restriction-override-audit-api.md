# B-03 — Restriction Override & Audit API

## 1. Feature Context
When a child hits a screen-time limit or bedtime block, a parent may grant a time extension or bedtime bypass. Every such override must require fresh Parent Gate verification and produce a permanent, attributed audit record (PRD C.23 FR-11, §5 item 5).

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
1.3 Restriction Override & Audit API (ID: **B-03**)

## 4. Objective
Implement `POST /v1/restriction-overrides`, requiring a fresh Parent Gate pass, writing an append-only `parent_overrides` row with no UPDATE/DELETE grant, and making the grant immediately visible to the child's next heartbeat/policy check without requiring app restart.

## 5. Business Requirements
- FR-11: override requires Parent Profile verification and creates an audited unlock entry — fully traceable, never invisible.
- FR-2 item 6: parent override requires Parent Profile verification and creates an audited unlock entry.
- Edge Case 3: granting an override while the child's session is already blocked unblocks that same session immediately, no re-entry required.
- NFR (Auditability): every override logged with who granted it, when, and how much additional time/access.
- Security Checklist: append-only `parent_overrides` table permission lockout verified pre-launch.

## 6. Existing Architecture
Lives in `modules/restrictions`. Reuses C.19's step-up gate (`require_elevated_session`, freshly re-verified — not a stale elevation) and the append-only-ledger pattern established for `RewardLedgerEntry` (A.11) as the architectural precedent for permission lockout on mutation.

## 7. Existing Code to Reuse
- `core/deps.py::require_elevated_session` (must require a **fresh** pass, not merely "currently elevated" — confirm/extend if the existing implementation doesn't distinguish freshness)
- `modules/rewards/repository.py` append-only pattern (reference implementation for permission lockout)
- `common/outbox.py::OutboxWriter`

## 8. Files to Create
- `src/noorheroes/modules/restrictions/override_models.py` — `ParentOverrideOrm`
- `src/noorheroes/modules/restrictions/override_schemas.py` — `RestrictionOverrideRequest`, `RestrictionOverrideResponse`
- `src/noorheroes/modules/restrictions/override_repository.py` — `ParentOverrideRepository` (insert-only)
- `src/noorheroes/modules/restrictions/override_service.py` — `RestrictionOverrideService(BaseService)`
- `alembic/versions/xxxx_create_parent_overrides.py` (includes explicit permission lockout: revoke UPDATE/DELETE grants)
- `tests/modules/restrictions/test_override_service.py`
- `tests/modules/restrictions/test_override_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/restrictions/api.py` — add `POST /v1/restriction-overrides`
- `src/noorheroes/modules/restrictions/deps.py` — add `get_override_service`

## 10. Backend Requirements
- `RestrictionOverrideService.grant_override(parent_ctx, payload)`:
  1. Require fresh `require_elevated_session` step-up (re-verify freshness, not a cached elevation from an earlier unrelated action).
  2. Verify family ownership of `payload.child_id`.
  3. Validate `type in ('screen_time', 'bedtime')` and `minutes_granted > 0`.
  4. Insert append-only `ParentOverrideOrm` row (`granted_by = parent_ctx.parent_sub`).
  5. If `type == 'screen_time'`: adjust the effective daily limit for today (e.g., write a Redis/PostgreSQL override marker consumed by B-02's next heartbeat evaluation) so the currently blocked session unblocks immediately.
  6. If `type == 'bedtime'`: write a bedtime-bypass marker with a bounded duration consumed identically by B-02.
  7. Emit `RestrictionOverrideGranted` outbox event.
  8. Write a `child_restriction_events` row is NOT created here (that table logs `limit_hit`/`bedtime_block` events, distinct from the override grant itself, per §4.2's `event_type` CHECK constraint).

## 11. API Contract

### `POST /v1/restriction-overrides`
- **Auth:** Bearer (parent) + step-up (fresh Parent Gate pass required, `require_elevated_session`)
- **Request:** `{ "child_id": "...", "type": "screen_time|bedtime", "minutes_granted": 15 }`
- **Response 200:** `{ "override_id": "...", "granted_by": "...", "granted_at": "..." }`
- **Error Responses:** `401 UNAUTHORIZED`, `403 FORBIDDEN` (no fresh step-up / not owned), `404 CHILD_NOT_FOUND`, `422 VALIDATION_ERROR`

## 12. Database Requirements
`parent_overrides`: `override_id UUID PK`, `child_id FK`, `type VARCHAR CHECK IN ('screen_time','bedtime')`, `minutes_granted INT`, `granted_by FK → users.id`, `created_at TIMESTAMPTZ`. Append-only — **no UPDATE/DELETE grant** on this table for the application's DB role (enforced at the migration/permission level, not just application code). Index `(child_id, created_at DESC)`.

## 13. Validation
- `type`: must be exactly `screen_time` or `bedtime`.
- `minutes_granted`: positive integer, capped at a sane maximum (e.g., 240) to prevent accidental/malicious extreme values.
- `child_id`: must exist and belong to caller's family.

## 14. Authentication
`Depends(get_current_parent)` + `Depends(require_elevated_session)` — the fresh-pass requirement is the defining security property of this endpoint.

## 15. Authorization
Family-ownership check on `child_id`.

## 16. Error Handling
| Scenario | Response |
|---|---|
| No fresh step-up pass | 403 FORBIDDEN |
| Child not found/not owned | 404 CHILD_NOT_FOUND |
| Invalid `type` value | 422 VALIDATION_ERROR |
| Attempt to UPDATE/DELETE a `parent_overrides` row (any path) | Rejected at DB permission layer, not just application layer |

## 17. Offline First
N/A — override grants require connectivity (parent-initiated, server-authoritative).

## 18. Local Data
N/A (backend); consumed by K-08's override-resume flow via B-02's next heartbeat response.

## 19. Localization
N/A — numeric/ID payload only.

## 20. RTL
N/A.

## 21. Analytics
Backing source for `restriction_override_requested`, `restriction_override_granted` (with `minutes_granted`, `granted_by` params).

## 22. Performance
Low-volume, parent-initiated only. Simple insert; no special optimization required beyond standard indexing.

## 23. Security
The append-only, no-UPDATE/DELETE-grant design is the core security guarantee: an override, once granted, is a permanent fact that cannot be retroactively hidden or altered — critical for dispute investigation and trust (PRD §12.9 pre-launch checklist item).

## 24. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Alembic (with explicit `REVOKE UPDATE, DELETE` SQL in the migration).

## 25. Testing
- Unit: override cannot be granted without a fresh step-up pass (stale elevation from an unrelated earlier action must not suffice).
- Unit: resulting row cannot be updated or deleted via direct repository call (permission-layer test, not just business-logic test).
- Unit: `minutes_granted` validation boundaries.
- Integration: full limit-reached → override-granted → next-heartbeat-reflects-unblock flow (coordinate with B-02).
- Negative: attempt direct DB `UPDATE`/`DELETE` on `parent_overrides` — confirm rejected at the permission layer.

## 26. Documentation
OpenAPI description must state explicitly that this table is append-only and why (audit integrity).

## 27. AI Coding Agent Implementation Steps

**Task 01 — Create `ParentOverrideOrm` Model**
- Files to Create: `src/noorheroes/modules/restrictions/override_models.py`

**Task 02 — Create Migration with Permission Lockout**
- Files to Create: `alembic/versions/xxxx_create_parent_overrides.py`
- Implementation Details: Standard `CREATE TABLE` plus explicit `REVOKE UPDATE, DELETE ON parent_overrides FROM <app_role>;` — do not rely on application-code-only enforcement.

**Task 03 — Create Request/Response Schemas**
- Files to Create: `src/noorheroes/modules/restrictions/override_schemas.py`

**Task 04 — Implement Insert-Only `ParentOverrideRepository`**
- Files to Create: `src/noorheroes/modules/restrictions/override_repository.py`
- Implementation Details: Expose only `add()`/`list_by_child()` — no `update`/`delete` methods defined at all, reinforcing the DB-level lockout in the code surface itself.

**Task 05 — Implement `RestrictionOverrideService.grant_override`**
- Dependencies: Task 04, B-02's usage/policy override-marker consumption mechanism (coordinate interface).
- Implementation Details: Per §10; the fresh-step-up check is the critical path — write and test this first.

**Task 06 — Implement Override-Marker Write for B-02 Consumption**
- Objective: Ensure a granted override is reflected on the child's very next heartbeat.
- Implementation Details: Write a lightweight marker (Redis key with TTL, or a PostgreSQL row B-02 already reads) — coordinate exact mechanism with B-02's `RestrictionEnforcementService`.

**Task 07 — Implement API Endpoint**
- Files to Modify: `src/noorheroes/modules/restrictions/api.py`, `deps.py`

**Task 08 — Add Fresh-Step-Up Test**
- Files to Create: `tests/modules/restrictions/test_override_service.py`

**Task 09 — Add Permission-Lockout Test**
- Objective: Confirm append-only guarantee at the DB permission layer, not just application logic.

**Task 10 — Add Integration Test**
- Files to Create: `tests/modules/restrictions/test_override_api.py`
- Coverage: full limit-reached → override → unblock flow.

**Task 11 — Add API Documentation**
- Objective: Document append-only guarantee and audit rationale.

**Task 12 — Final Code Review**
- Objective: Confirm no code path anywhere calls `UPDATE`/`DELETE` against this table; confirm outbox event emission.

## 28. Definition of Done
- Override cannot be granted without a fresh step-up pass (tested).
- `parent_overrides` rows are immutable post-creation at both application and DB permission layers (tested).
- Granted override reflects on child's next heartbeat without app restart (integration-tested with B-02).

## 29. Final Verification Checklist
- [ ] Fresh step-up (not stale elevation) required and tested
- [ ] `REVOKE UPDATE, DELETE` applied in migration
- [ ] No repository method exists for update/delete of override rows
- [ ] Override-marker consumption confirmed working end-to-end with B-02
- [ ] Outbox event emitted on grant
- [ ] OpenAPI documents append-only guarantee
