# B-06 — Permanent Child Deletion & Audit Trail Service

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management. This is the feature's single most legally and emotionally sensitive control: genuine, irreversible, self-service deletion — deliberately engineered to require zero Support intervention while remaining fully auditable.

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**B-06 — Permanent Child Deletion & Audit Trail Service** (`POST /v1/children/{id}/delete`)

## 4. Objective
Execute a genuinely irreversible child-profile deletion — gated by step-up authentication **and** an explicit, non-implicit warning acknowledgment — while automatically creating a complete audit trail with zero Support-ticket involvement, subject to a legally configured retention window.

## 5. Business Requirements
- FR-5: full five-step deletion flow — navigate → step-up → warning shown → confirm → execute + auto-audit.
- Acceptance Criteria: "Given a parent successfully deletes a child, then no Support ticket was required, an audited deletion record was automatically created, and the deletion is irreversible subject only to the legal-retention window."
- Edge Case #3: back out before final confirmation → no deletion occurs, profile unaffected.
- Edge Case #6: unusual per-child entitlement tied to deletion → deletion proceeds per standard flow; entitlement cascade handled by C.24's own logic (this service does not implement entitlement cascade).
- Edge Case #9: deleting the only remaining active child → allowed, with a gentle informational note, not a hard block.
- NFR: "Irreversibility Integrity: Permanent deletion must be genuinely irreversible after its legal-retention window."

## 6. Existing Architecture
New `Deletion Service` component within the `identity` context (per PRD §3.3), reusing B-04's `session_revocation.py` module for the same immediate-cutoff guarantee deletion also requires.

## 7. Existing Code to Reuse
- `session_revocation.revoke_all_sessions_for_child()` (built in B-04, Task 01) — a deleted child must also be immediately cut off from all sessions.
- `OutboxWriter.emit()` — emit a `ChildDeletionInitiated`/`ChildDeletionCompleted` domain event for downstream consumers (e.g., C.24's entitlement cascade, C.22's report archival).
- `AdminAuditRepository`-equivalent pattern for `audit_logs` — reuse the existing audit-log table/writer, do not create a parallel logging mechanism.
- `require_elevated_session`.

## 8. Files to Create
- `modules/identity/models.py` additions: `ChildDeletionCase` ORM model (if not already present).
- `modules/identity/deletion_service.py` — dedicated service class for the deletion workflow, kept separate from the general `IdentityService` given its compliance sensitivity.
- `alembic/versions/xxxx_create_child_deletion_case.py` — migration for `child_deletion_case` table.
- `scripts/purge_expired_child_deletions.py` — scheduled job (Celery periodic task, following the `retry_failed_translations_task()` pattern in `localization/tasks.py`) that purges/anonymizes data at `retention_expires_at`.

## 9. Files to Modify
- `modules/identity/api.py` — add `POST /v1/children/{id}/delete`.
- `modules/identity/schemas.py` — add `ChildDeletionRequest { acknowledgedWarning: bool }`.
- `tests/modules/identity/test_children_deletion.py` — new test module.

## 10. Backend Requirements
- Require **both** step-up **and** `acknowledged_warning: true` in the request body — reject (`422`) if either is absent, even with a valid step-up token.
- On confirmed deletion: set `child.status = 'deletion_pending'`, revoke all sessions (reuse B-04's module), deactivate bindings, create `child_deletion_case` row, create `audit_logs` row — **all in one transaction**.
- Genuinely purge/anonymize underlying data at `retention_expires_at` via the scheduled job — the exact retention duration is Legal/Compliance-configured (§4.5), not hardcoded arbitrarily in this service; read it from `Settings`.
- Permit deletion of the only remaining active child (informational note is a client-side UX concern, not a server-side block).
- Permit deletion of an already-disabled child directly (no re-enable-first requirement).
- Do NOT implement entitlement-cascade logic here — emit the domain event and let C.24 react to it independently (Edge Case #6).

## 11. KMP Requirements
K-05's two-step warning flow calls this only after the user taps "Permanently Delete" on the sober warning screen; `acknowledged_warning: true` must never be sent from any other code path.

## 12. NextJS Requirements
B-09 (Admin Deletion Case Audit API) is the sole read surface over `child_deletion_case` created here.

## 13. API Contract

**`POST /v1/children/{id}/delete`**
- **Auth:** Bearer + step-up.
- **Request:**
```json
{ "acknowledgedWarning": true }
```
- **Response 200:**
```json
{
  "childId": "uuid",
  "status": "deletion_pending",
  "deletionCaseId": "uuid",
  "retentionExpiresAt": "timestamp"
}
```
- **Error Responses:**
  - `422` — `acknowledgedWarning` missing or `false`, even with valid step-up.
  - `404` — not found/not owned.
  - `401` — missing session/step-up.

## 14. Database Requirements
Per §4.1/§4.2:
```sql
CREATE TABLE child_deletion_case (
    case_id UUID PRIMARY KEY,
    child_id UUID NOT NULL REFERENCES child(child_id),
    initiated_by_parent_id UUID NOT NULL,
    requested_at TIMESTAMPTZ NOT NULL,
    retention_expires_at TIMESTAMPTZ NOT NULL,
    purged_at TIMESTAMPTZ,
    status TEXT NOT NULL
);
CREATE INDEX ON child_deletion_case (child_id);
```
Append-only table — no UPDATE grants beyond the purge job setting `purged_at`/`status`.

## 15. Validation
`acknowledgedWarning` must be a literal boolean `true`; any other value (missing, `false`, string `"true"`) is rejected.

## 16. Authentication
Bearer parent session.

## 17. Authorization
Step-up required, plus the explicit acknowledgment field — a double gate, intentionally.

## 18. Error Handling
| Scenario | Response |
|---|---|
| `acknowledgedWarning` false/missing | `422`, even with valid step-up |
| Not found/not owned | `404` |
| Step-up missing | `401` |
| Already deletion_pending | `200` idempotent no-op (do not create a second case row) |
| Session-revocation failure | `500`, transaction rolls back — same atomicity guarantee as B-04 |

## 19. Offline First
N/A — mutating action, requires connectivity.

## 20. Local Data
N/A backend; K-09 removes the child from local cache on success.

## 21. Localization
N/A — no localized fields on this endpoint itself (warning text is client-rendered).

## 22. RTL
N/A backend.

## 23. Analytics
None server-side; the full `child_delete_initiated → _warning_shown → (_confirmed → _completed) / _canceled` funnel is client-side (K-05).

## 24. Performance
Single transaction, bounded work (status update, session revocation, two inserts); not on a latency-critical path — correctness matters far more than speed here.

## 25. Security
- Double-gated (step-up + explicit acknowledgment) specifically to prevent both unauthorized *and* accidental/coerced deletion (§12.1).
- Audit trail is fully automatic and non-optional — there is no code path that deletes without creating the corresponding `child_deletion_case`/`audit_logs` rows (enforced by the single-transaction requirement).

## 26. Library Requirements
Celery (existing, already used by `localization/tasks.py`) for the scheduled purge job — no new library.

## 27. Testing
- **Highest-priority test (per PRD §5 backend AI prompt item 4):** confirm rejection when `acknowledgedWarning` is missing/false even with valid step-up.
- Unit: `deletion_service` creates `child_deletion_case` + `audit_logs` atomically — test a simulated failure after the case-row insert and confirm the audit-log insert (and the whole transaction) rolls back too.
- Integration: full deletion flow, verify session revocation (reuse B-04's live-session test pattern).
- Integration: deleting the only remaining active child succeeds (no server-side block).
- Integration: deleting an already-disabled child succeeds directly.
- Integration: purge job correctly anonymizes/purges data at `retention_expires_at` in a time-mocked test (`TestClock`).

## 28. Documentation
Document the two-gate requirement prominently in the OpenAPI description; document that entitlement cascade is deliberately out of scope here (cross-reference C.24).

## 29. AI Coding Agent Implementation Steps

**Task 01 — `child_deletion_case` Model & Migration**
- **Objective:** Create the append-only audit table.
- **Files to Create:** ORM model in `modules/identity/models.py`, Alembic migration.
- **Implementation Details:** Per §14 schema exactly; no additional columns beyond what's specified without a documented reason.
- **Definition of Done:** Migration applies cleanly; table matches §4.1 ER diagram.

**Task 02 — Deletion Service with Double-Gate Enforcement**
- **Objective:** Implement `DeletionService.delete_child()` requiring both step-up and `acknowledgedWarning: true`.
- **Files to Create:** `modules/identity/deletion_service.py`.
- **Why Required:** This is the PRD's highest-stakes guarantee — a genuinely irreversible action must never be reachable by accident or by a compromised session token alone.
- **Implementation Details:** Reject before any side effect if `acknowledgedWarning is not True`; then, in one transaction: set `status='deletion_pending'`, call `session_revocation.revoke_all_sessions_for_child()`, deactivate bindings, insert `child_deletion_case`, insert `audit_logs` row, emit `ChildDeletionInitiated` via `OutboxWriter`.
- **Tests:** The highest-priority acknowledgment-gating test; atomicity-under-failure test.
- **Definition of Done:** No code path deletes without both gates passing and without the audit row being created in the same transaction.

**Task 03 — Retention-Then-Purge Scheduled Job**
- **Objective:** Automatically purge/anonymize data at `retention_expires_at`.
- **Files to Create:** `scripts/purge_expired_child_deletions.py` (Celery periodic task).
- **Implementation Details:** Query `child_deletion_case WHERE retention_expires_at <= now() AND purged_at IS NULL`; anonymize/hard-delete the underlying `child` row and dependent data per Legal/Compliance's configured scope; set `purged_at` and `status='purged'`.
- **Monitoring:** Add alerting on job failure (P0 per §10 DevOps Requirements).
- **Tests:** Time-mocked test using `TestClock` confirming purge only fires post-expiry, not before.
- **Definition of Done:** Purge job is idempotent, alerts on failure, and never fires early.

**Task 04 — Router Wiring**
- **Objective:** Attach step-up and route the endpoint with idempotent-replay handling.
- **Files to Modify:** `modules/identity/api.py`.
- **Definition of Done:** End-to-end test covering happy path, both-gates-required rejection, and idempotent replay.

## 30. Definition of Done
Deletion is genuinely double-gated, fully auditable in one atomic transaction, session-revoking, and retention-then-purge is correctly time-gated and monitored — with zero Support-ticket dependency.

## 31. Final Verification Checklist
- [ ] `acknowledgedWarning` both-gates test passes (highest priority)
- [ ] `child_deletion_case` + `audit_logs` created atomically with the status change
- [ ] Session revocation reused correctly from B-04
- [ ] Deletion of only-remaining-active-child allowed
- [ ] Deletion of already-disabled child allowed without re-enable
- [ ] Purge job time-gated correctly and alerts on failure
- [ ] Entitlement cascade deliberately deferred to C.24 (event emitted, not handled here)
- [ ] No PostgreSQL/Redis credential changes
