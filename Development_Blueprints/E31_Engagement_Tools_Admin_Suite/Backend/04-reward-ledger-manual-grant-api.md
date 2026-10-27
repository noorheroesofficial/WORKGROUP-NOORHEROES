# B-04 — Reward Ledger & Manual Grant API

> **Reconciliation note (2026-08-18):** A.11 Rewards System's own blueprint originally specified an equivalent read-only ledger viewer at `A11_Rewards_System/Backend/13-admin-reward-ledger-audit-reconciliation-viewer-api.md` (B-13). That file's ledger-audit portion is now marked deprecated in favor of this one — this file (E.31 B-04) is authoritative for both the read-only ledger view and the manual-grant tool. Note: B-13's *other* portion (Reconciliation Incident Log — wallet-balance-drift corrections made by A.11's standing reconciliation job) is **not** covered here and was extracted into `A11_Rewards_System/Backend/14-admin-reconciliation-incident-log-api.md`, which remains A.11-owned; do not fold that surface into this file without an explicit scope decision.

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the read-only, append-only reward ledger surface and the audited manual reward-grant tool, split out from XP rule authoring (see **B-03 XP Rule Management API**) because the PRD treats the Ledger Viewer (Screen #9) and Manual Reward Grant Tool (Screen #10) as a distinct read/append-only surface from the XP Rule Table/Editor (#7/#8). Source: PRD §1.7 FR-3 (ledger portion), §1.18 Screens 9–10, §3.4, §5 item 1 (shared no-retroactivity spirit).

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
1.4 Reward Ledger & Manual Grant API (Backend ID: **B-04**)

## 4. Objective
Give admins/support agents a structurally read-only view of the reward ledger and a fully audited, idempotent, reason-coded manual reward-grant tool — with no edit or delete path anywhere in this API surface, reusing A.11's exact append-only-permission-lockout pattern.

## 5. Business Requirements
- FR-3 (PRD §1.7, ledger portion): reward ledger viewer (read-only, append-only), manual reward grant tool (support use, fully audited).
- **Hard rule:** ledger entries are never edited or deleted, only appended.
- **Hard rule:** manual grants require a reason code and create their own audited ledger row with an idempotency key.
- Edge Case 5 (PRD §1.10): an erroneous manual grant is corrected via an equal-and-opposite adjustment entry, never an edit or deletion of the original.

## 6. Existing Architecture
Extends A.11's Reward Service. Reuses A.11's existing append-only-permission-lockout pattern for the `reward_ledger` table (PRD §2.1, §3.4) — a DB-permission-level guarantee, not merely an API-surface omission.

## 7. Existing Code to Reuse
- A.11's existing `reward_ledger` table and its DB-role permission lockout (no UPDATE/DELETE grants for the application's DB role on this table).
- E.28's audit log client, RBAC dependency (`support`/`billing_ops` role check).

## 8. Files to Create
- `app/routers/admin/reward_ledger_router.py`
- `app/schemas/admin/reward_ledger_schemas.py`
- `app/services/admin/reward_ledger_admin_service.py`
- `app/repositories/admin/reward_ledger_admin_repository.py`
- `tests/admin/test_reward_ledger_admin_api.py`

## 9. Files to Modify
- `app/routers/admin/__init__.py`
- `app/core/audit.py` (`manual_reward_grant.issued`)
- `app/core/rbac.py` (ensure `support`/`billing_ops` roles defined per A.11's established pattern)

## 10. Backend Requirements
- **Database:** `reward_ledger` (existing, A.11, append-only via DB role permissions — this sub-feature must NOT grant UPDATE/DELETE to the application role on this table).
- **Migration:** none destructive; confirm/enforce existing permission lockout if not already applied.
- **Model:** `RewardLedgerEntry` (read model only from this layer).
- **Schema/DTO:** `ManualGrantRequest` (`child_id`, `amount`, `currency`, `reason_code`, `idempotency_key`), `RewardLedgerEntryRead`.
- **Repository:** `list_ledger_entries(child_id)`, `insert_manual_grant()` (INSERT only, no update path exists in this repository at all).
- **Service:** `RewardLedgerAdminService` — validates reason_code presence, checks idempotency key for replay-safety, writes ledger row tagged `reason_type='manual_grant'`, audit-logs.
- **Router:** `GET /v1/admin/reward-ledger`, `POST /v1/admin/reward-ledger/manual-grant`.
- **Dependency Injection:** `require_role_any(["support", "billing_ops"])` for manual grants; broader read access for the ledger GET.
- **Authentication/Authorization:** admin JWT; manual-grant endpoint restricted specifically to `support`/`billing_ops`.
- **Validation:** `reason_code` required and must be a registered code; `idempotency_key` required and unique-checked before insert (return the original result on replay rather than double-granting).
- **Business Rules:** no PATCH/DELETE route exists for `reward_ledger` anywhere in this router — this is a structural, not just behavioral, guarantee.
- **Exception Handling:** duplicate `idempotency_key` treated as a safe replay (return the original grant result, not an error).
- **Logging:** every manual grant logged with `reason_code`, `admin_id`, `child_id`.
- **Caching:** N/A (ledger reads are not cached, to avoid staleness in support workflows).
- **Transaction:** manual grant insert + audit log write in a single transaction.
- **Pagination/Filtering/Sorting:** ledger list paginated, filterable by `child_id`, `reason_type`, date range.

## 11. KMP Requirements
N/A — admin-only. Child-facing reward issuance remains entirely within A.11's existing engine; this layer only adds support tooling in front of it.

## 12. NextJS Requirements
Consumed by **N-04 Reward Ledger & Manual Grant UI**, which must render the Ledger Viewer with zero edit/delete affordances anywhere, mirroring this backend's structural read-only guarantee.

## 13. API Contract

### `GET /v1/admin/reward-ledger?child_id=`
- **Authorization:** any admin role with Engagement/Support visibility
- **Response (200):** paginated, read-only ledger entries — no mutating verb exists on this route at all

### `POST /v1/admin/reward-ledger/manual-grant`
- **Authorization:** `support` or `billing_ops` role only
- **Request:**
```json
{
  "child_id": "uuid",
  "amount": 50,
  "currency": "noor_points",
  "reason_code": "missing_reward_ticket_1234",
  "idempotency_key": "support-ticket-1234-grant-1"
}
```
- **Response (201):** new ledger row, `reason_type: "manual_grant"`
- **Error Responses:** `401`, `403`, `422 REASON_CODE_REQUIRED`, safe replay on duplicate `idempotency_key`, `404 CHILD_NOT_FOUND`

## 14. Database Requirements
- `reward_ledger`: existing A.11 table; confirm application DB role has INSERT-only (no UPDATE/DELETE) grants — this sub-feature's implementation must not introduce any code path or DB permission that could bypass that lockout.
- Unique index on `reward_ledger(idempotency_key)` where `idempotency_key IS NOT NULL`.

## 15. Validation
`reason_code` required and registered; `idempotency_key` required for manual grants; `amount` positive; `currency` valid enum.

## 16. Authentication
Admin JWT (E.28).

## 17. Authorization
`support`/`billing_ops` exclusively for manual grants, per A.11's established pattern (PRD §1.15); broader read access for the ledger view.

## 18. Error Handling
| Scenario | Response |
|---|---|
| Missing `reason_code` on manual grant | `422 REASON_CODE_REQUIRED` |
| Duplicate `idempotency_key` | Safe replay of original result |
| Attempt to PATCH/DELETE a ledger entry | No such route exists — `404`/`405` at the routing level |
| Insufficient role for manual grant | `403 FORBIDDEN` |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
`reason_code` maps to a localized display label in the UI layer; backend stores the code only.

## 22. RTL
N/A at API layer.

## 23. Analytics
`manual_reward_grant_issued` (with `reason_code`) per PRD §1.19.

## 24. Performance
Ledger list queries indexed by `(child_id, created_at)`; manual-grant idempotency check uses a unique index for O(log n) lookup, not a table scan.

## 25. Security
Append-only integrity enforced at the DB permission layer (defense-in-depth beyond just API-surface omission) — per PRD §1.8 "reuses A.11's exact append-only-permission-lockout pattern, never a parallel writable log." Manual-grant role restriction strictly enforced.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2, pytest-asyncio.

## 27. Testing
- Unit: reason-code validation, idempotency-key handling.
- Integration: manual grant creates a new audited row; duplicate idempotency key returns safe replay, not a double grant.
- Edge cases: Edge Case 5 — corrective adjustment entry pattern (confirm no update/delete endpoint exists for ledger entries, only a new adjustment-entry creation path if implemented as a distinct grant type).
- Negative cases: missing reason_code, unauthorized role attempting manual grant.

## 28. Documentation
OpenAPI docs explicitly stating the ledger's structural read-only/append-only guarantee and the idempotency-key replay semantics.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm/Enforce DB Permission Lockout**
- Task ID: B-04-T01
- Objective: Verify (or apply, if missing) the DB-role permission lockout on `reward_ledger` preventing UPDATE/DELETE.
- Why Required: PRD §1.8 requires this be a structural guarantee, not just an API-surface omission.
- Files to Create: migration granting/revoking DB privileges accordingly (if not already applied by A.11).
- Tests: attempt a raw UPDATE/DELETE against `reward_ledger` using the application's DB role in a test and confirm it is rejected by PostgreSQL itself.
- Dependencies: none.
- Do Not Change: PostgreSQL credentials.
- Definition of Done: permission-lockout test passes.

**Task 02 — Reward Ledger Read Endpoint**
- Task ID: B-04-T02
- Files to Create: `app/routers/admin/reward_ledger_router.py` (GET only), `app/repositories/admin/reward_ledger_admin_repository.py`.
- Implementation Details: no mutating route defined anywhere in this router file.
- Tests: confirm router exposes only `GET`.
- Dependencies: Task 01.
- Definition of Done: test green.

**Task 03 — Manual Reward Grant Endpoint**
- Task ID: B-04-T03
- Objective: Implement the audited, idempotent, reason-coded manual grant tool.
- Files to Create: `app/services/admin/reward_ledger_admin_service.py`.
- Implementation Details: role check `support`/`billing_ops`; idempotency-key unique-constraint-based replay safety; ledger row tagged `reason_type='manual_grant'`.
- Tests: `test_manual_grant_requires_reason_code`, `test_manual_grant_idempotent_replay`, `test_manual_grant_forbidden_for_content_editor_role`.
- Dependencies: Tasks 01–02.
- Definition of Done: all tests green.

**Task 04 — Documentation & Final Review**
- Task ID: B-04-T04
- Dependencies: Tasks 01–03.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
Ledger proven structurally append-only at both API and DB-permission layers; manual-grant tool fully audited, reason-coded, and idempotent; role restrictions enforced; full test suite green.

## 31. Final Verification Checklist
- [ ] No PATCH/DELETE route exists anywhere for `reward_ledger`
- [ ] DB-role permission lockout on `reward_ledger` verified via direct-SQL test
- [ ] Manual grant requires `reason_code` (rejected without it)
- [ ] Manual grant requires `idempotency_key`; duplicate key replays safely, never double-grants
- [ ] Manual grant restricted to `support`/`billing_ops` role
- [ ] Every mutation audit-logged
- [ ] Negative/unauthorized paths tested
- [ ] No school/madrasa/institutional-tier logic introduced
- [ ] PostgreSQL/Redis credentials untouched
