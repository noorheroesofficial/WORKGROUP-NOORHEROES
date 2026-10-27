# B-04 — Maker-Checker Change Proposal Workflow

## 1. Feature Context
Part of E.28. Implements the shared `change_proposals` primitive that every high-risk Admin Portal mutation (role changes, safety/AI feature flags, production config) routes through. This is, alongside B-01's auth isolation, one of the two highest-priority guarantees in the entire E.28 service (PRD §5 Backend AI prompt).

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
B-04 — Maker-Checker Change Proposal Workflow

## 4. Objective
Implement proposal creation, distinct-approver enforcement (both application-layer and database-layer), and idempotent approval resolution, such that no admin can ever be the sole approver of a change to their own role, and no change can ever be self-approved regardless of session/device (FR-3, Edge Cases 1–2, 7).

## 5. Business Requirements
- FR-3: role changes require a second admin's approval (maker-checker); an admin cannot self-elevate their own role.
- FR-9: safety/AI feature flags require two-person approval.
- FR-13: production config changes require maker-checker.
- Edge Case 1: cross-session/cross-device self-approval attempts rejected by underlying admin identity, not session.
- Edge Case 2: concurrent approvals on the same proposal — first wins, second is a no-op, not an error.
- Edge Case 7: no auto-approval timeout — proposals remain pending indefinitely.
- Acceptance Criteria: proposing admin's own approval is never sufficient; self-elevation always rejected regardless of target role.

## 6. Existing Architecture
- No existing maker-checker mechanism exists in the codebase — this is genuinely new infrastructure, though it must follow the platform's standard layered pattern (Router → Service → Repository) and use `OutboxWriter` for any downstream event emission (e.g., notifying the approver, if notification integration is added later via `notifications` context — out of scope for B-04 itself, but the emission point should exist per `common/outbox.py::OutboxWriter.emit()` convention).
- Depends on B-01 (`admin_id` identity) and B-03 (role/permission data it will mutate upon approval).
- `BaseRepository`/`BaseService` patterns reused throughout.

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `BaseService`, `BaseRepository[ModelT]` | `common/base_service.py`, `common/base_repository.py` | Service/repository scaffolding |
| `OutboxWriter.emit()` | `common/outbox.py` | Emitting `ProposalCreated`/`ProposalApproved` domain events |
| `generate_ulid()` | `common/utils/ids.py` | `proposal_id`, `approval_id` |
| `Clock` | `common/utils/clock.py` | `created_at`/`resolved_at`/`decided_at` timestamps |
| `ConflictError` | `core/exceptions.py` | Redundant-approval no-op signaling (return 200 with existing state, not a hard conflict — see Task 05) |
| `RoleRepository`/`RolePermissionRepository` | B-03 | Applying the approved role-permission change |

## 8. Files to Create
- `src/noorheroes/modules/admin/maker_checker/models.py` — `ChangeProposalOrm`, `ChangeProposalApprovalOrm`
- `src/noorheroes/modules/admin/maker_checker/schemas.py` — `ChangeProposalResponse`, `ChangeProposalListResponse`, `ApprovalRequest`, `ApprovalResponse`
- `src/noorheroes/modules/admin/maker_checker/repository.py` — `ChangeProposalRepository`
- `src/noorheroes/modules/admin/maker_checker/service.py` — `MakerCheckerService`
- `src/noorheroes/modules/admin/maker_checker/api.py` — `GET /v1/admin/change-proposals`, `GET /v1/admin/change-proposals/{id}`, `POST /v1/admin/change-proposals/{id}/approve`
- `alembic/versions/xxxx_create_change_proposal_tables.py` (includes the DB-level CHECK constraint)
- `tests/modules/admin/maker_checker/test_maker_checker_workflow.py`
- `tests/modules/admin/maker_checker/test_self_approval_db_constraint.py`
- `tests/modules/admin/maker_checker/test_approval_idempotency.py`

## 9. Files to Modify
- `src/noorheroes/modules/admin/rbac/service.py` (B-03) — `PATCH /v1/admin/roles/{id}/permissions` handler routes into `MakerCheckerService.create_proposal()` instead of applying directly; rejects outright with `403 SELF_ELEVATION_BLOCKED` if the proposing admin's own role is the target

## 10. Backend Requirements
- **Models (§4.1/§4.2 of PRD):**
  - `change_proposal(proposal_id PK, proposal_type, proposed_by FK, proposed_change jsonb, status CHECK IN ('pending','approved','rejected'), created_at, resolved_at)`, index `(status, created_at DESC)`
  - `change_proposal_approval(approval_id PK, proposal_id FK, approved_by FK, decision, decided_at)`, index `(proposal_id)`, **DB-level `CHECK approved_by != (SELECT proposed_by FROM change_proposal WHERE proposal_id = change_proposal_approval.proposal_id)`**
- **`create_proposal(proposal_type, proposed_by, proposed_change)`:** self-elevation guard — if `proposal_type == "role_permission_change"` and the target role equals `proposed_by`'s own current role, reject outright with `403 SELF_ELEVATION_BLOCKED` (do not even create a pending proposal — PRD §3.4 specifies this as an outright rejection, not a proposal that later fails approval).
- **`approve_proposal(proposal_id, approved_by)`:**
  - Reject `403 SAME_ADMIN_CANNOT_APPROVE_OWN_PROPOSAL` if `approved_by == proposal.proposed_by`, compared by underlying `admin_id` regardless of session/device (Edge Case 1).
  - On approval: apply the underlying change atomically (single DB transaction spanning the approval-record insert and the target mutation — e.g., calling B-03's `RolePermissionRepository` update), mark proposal `approved`, set `resolved_at`.
  - On a second approval attempt against an already-resolved proposal: return the existing resolved state as a no-op (200, not an error) — Edge Case 2.
  - No auto-approval timeout logic anywhere — proposals remain `pending` indefinitely absent human action (Edge Case 7).
- **Reusable primitive:** any future Admin module (E.29–E.34) wanting maker-checker behavior calls `MakerCheckerService.create_proposal()` rather than building its own proposal mechanism (PRD §3.5 cross-cutting concern).
- **`GET /v1/admin/change-proposals?status=&proposal_type=&cursor=&limit=`:** paginated, filterable list of proposals (defaults to `status=pending` for the Approval Queue's primary view per §2.2). This endpoint was implied but not enumerated in PRD §3.4's API list — it is required by the Maker-Checker Approval Queue screen (§1.18 screen #15) and is added here as the correct owning module, since `ChangeProposalRepository.list_pending()` (Task 02) already provides the underlying query.
- **`GET /v1/admin/change-proposals/{id}`:** single-proposal detail including its full `proposed_change` diff payload and any recorded `change_proposal_approval` row — required by the Proposal Detail screen (§1.18 screen #16).

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
Consumed by `N-04` (role-change proposal creation), `N-05` (approval queue/detail), `N-07` (feature-flag proposal routing), `N-08` (config proposal routing).

## 13. API Contract
### `GET /v1/admin/change-proposals?status=&proposal_type=&cursor=&limit=`
- **Auth:** `super_admin` (or the appropriate approver role per proposal type)
- **Response 200:**
```json
{ "items": [ { "proposal_id": "...", "proposal_type": "role_permission_change", "proposed_by": "admin_01H...", "status": "pending", "created_at": "..." } ], "next_cursor": "...", "has_more": false }
```
- **Error Responses:** `401`, `403`, `422` (invalid filter params)

### `GET /v1/admin/change-proposals/{id}`
- **Auth:** `super_admin` (or the appropriate approver role per proposal type)
- **Response 200:** `{ "proposal_id": "...", "proposal_type": "...", "proposed_by": "...", "proposed_change": {}, "status": "pending", "created_at": "...", "resolved_at": null, "approvals": [] }`
- **Error Responses:** `401`, `403`, `404 PROPOSAL_NOT_FOUND`

### `POST /v1/admin/change-proposals/{id}/approve`
- **Auth:** `super_admin` (or the appropriate approver role for the proposal type, resolved via B-03's permission matrix)
- **Request:** `{ "decision": "approve" | "reject" }`
- **Response 200 (new approval):** `{ "proposal_id": "...", "status": "approved", "resolved_at": "..." }`
- **Response 200 (redundant/no-op):** identical shape reflecting the existing resolved state, not a new mutation
- **Error Responses:**
  | Status | Code | Condition |
  |---|---|---|
  | 403 | `SAME_ADMIN_CANNOT_APPROVE_OWN_PROPOSAL` | `approved_by == proposed_by` (identity, not session) |
  | 404 | `PROPOSAL_NOT_FOUND` | Unknown `proposal_id` |
  | 401/403 | standard auth/authz | Missing/insufficient role |

### `PATCH /v1/admin/roles/{id}/permissions` (B-03 endpoint, routing logic owned here)
- **Business Logic:** Creates a `change_proposal` row rather than applying immediately; rejects outright (`403 SELF_ELEVATION_BLOCKED`) if the proposing admin's own role is the target.

## 14. Database Requirements
- `change_proposal_approval` DB-level `CHECK` constraint comparing `approved_by` against the proposal's `proposed_by` — this is defense-in-depth **independent** of the application-layer check; must reject even a direct SQL `INSERT` that bypasses the service layer entirely.
- `change_proposal.status` CHECK constrained to `('pending','approved','rejected')`.
- Index `(status, created_at DESC)` supports the Approval Queue's default sort (pending, oldest first, or as UI specifies).

## 15. Validation
- `proposal_type` must be one of a known allow-listed set (`role_permission_change`, `feature_flag_change`, `app_config_change`, extensible for future E.29–E.34 use).
- `proposed_change` jsonb structurally validated per `proposal_type` (e.g., a role-permission proposal must reference a valid `role_id`).
- `decision` must be `"approve"` or `"reject"`.

## 16. Authentication
Delegated to B-01/B-02.

## 17. Authorization
`super_admin` (or type-appropriate approver role per B-03) required to approve; proposal creation authorization is owned by the calling module (e.g., B-03's PATCH handler already requires `super_admin` to reach the proposal-creation call).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Self-elevation attempt (any form) | Rejected outright at proposal-creation time, `403 SELF_ELEVATION_BLOCKED` |
| Self-approval attempt, same session | Rejected, `403 SAME_ADMIN_CANNOT_APPROVE_OWN_PROPOSAL` |
| Self-approval attempt, different session/device | Identically rejected — identity compared, not session (Edge Case 1) |
| Two admins approve simultaneously | First completes; second returns existing resolved state as no-op (Edge Case 2) |
| Proposal pending indefinitely | No auto-approval; remains pending (Edge Case 7) — optionally surfaced as a staleness alert by B-08's dashboard, not auto-resolved here |
| DB-level self-approval INSERT attempt | Rejected by the `CHECK` constraint independent of application code |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Proposal `proposal_type`/`decision` are stable enum values; display-label translation is a client concern (N-04/N-05).

## 22. RTL
N/A at backend layer.

## 23. Analytics
Backend response supports client-fired events: `role_change_proposed`, `maker_checker_proposal_created`, `maker_checker_proposal_approved`, `maker_checker_proposal_rejected`, `maker_checker_redundant_approval_noop` (internal), `role_change_self_elevation_attempt_blocked` (internal/security signal) per PRD §1.19.

## 24. Performance
- Approval application (proposal-resolve + target-mutation) executes in a single DB transaction — no dual-write risk between "proposal marked approved" and "underlying change applied."
- Concurrent-approval race handled via DB-level row locking / optimistic check on `status`, not application-level mutex, to remain correct under concurrent requests across multiple app instances.

## 25. Security
- **Dual-layer self-elevation/self-approval prevention (primary guarantee, alongside B-01's auth isolation, the two highest-priority guarantees in the whole service):** application-layer check in `MakerCheckerService.approve_proposal()` AND database-layer `CHECK` constraint, independently enforcing the same rule.
- Identity comparison uses `admin_id`, never session token or device fingerprint — defeats any session-switching circumvention attempt.
- No auto-approval timeout — a stale pending proposal is a UX/ops concern (surfaced via alerting per PRD §10 DevOps), never resolved by silently approving.
- P0 production alert (per PRD §10) on any successful self-elevation/self-approval attempt detected — should be structurally impossible; monitored as a defense-in-depth canary. This alerting hook is a `TODO`-tagged integration point for the platform's existing alerting infrastructure, wired in Task 07.

## 26. Library Requirements
No new libraries — SQLAlchemy 2.0 async (including raw `CHECK` constraint DDL via Alembic `op.create_check_constraint`).

## 27. Testing
- Unit: `create_proposal()` self-elevation rejection; `approve_proposal()` self-approval rejection, successful approval, redundant-approval no-op.
- **Signature test A:** direct database `INSERT` into `change_proposal_approval` violating the `CHECK` constraint is rejected by the database itself, independent of any application-layer check (§5 Backend AI prompt item 3).
- **Signature test B:** two different admins both attempting to approve the same proposal in quick succession — exactly one approval recorded, second receives the same resolved-state response (§5 item 4).
- Integration: full role-change-proposal → second-admin-approval → applied-change flow using two distinct fixture admins.
- Integration: `GET /v1/admin/change-proposals` filtering (status/proposal_type) and pagination; `GET /v1/admin/change-proposals/{id}` detail including nested approvals.

## 28. Documentation
OpenAPI schema for the approve endpoint; internal doc explaining the reusable `change_proposals` primitive for future E.29–E.34 module authors, and the two-layer defense pattern for self-approval prevention.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `ChangeProposal`/`ChangeProposalApproval` Models + DB CHECK Constraint**
- Task ID: B-04-T01
- Objective: Persist proposals and approvals with database-level self-approval prevention.
- Why Required: This is the feature's single defining risk-mitigation mechanism (PRD §12.1).
- Files to Create: `modules/admin/maker_checker/models.py`, migration file.
- Implementation Details: `CHECK approved_by != (SELECT proposed_by FROM change_proposal WHERE proposal_id = change_proposal_approval.proposal_id)`, `CHECK status IN ('pending','approved','rejected')`.
- Security: This constraint is the true defense-in-depth layer — must be verified via direct-INSERT test, not just application logic.
- Tests: Migration test; direct-INSERT constraint-violation test (Task 04).
- Dependencies: B-01 (admin_id FK target).
- Definition of Done: Constraint present and provably enforced at the DB layer.

**Task 02 — Implement `ChangeProposalRepository`**
- Task ID: B-04-T02
- Files to Create: `modules/admin/maker_checker/repository.py`.
- Implementation Details: `create()`, `get_by_id()`, `list_pending()`, `mark_resolved()`, `add_approval()`.
- Tests: Repository unit tests.
- Dependencies: Task 01.
- Definition of Done: CRUD operations tested against fixture DB.

**Task 03 — Implement `MakerCheckerService.create_proposal()`**
- Task ID: B-04-T03
- Objective: Proposal creation with outright self-elevation rejection.
- Files to Create: `modules/admin/maker_checker/service.py`.
- Implementation Details: Validate `proposal_type`; if `role_permission_change` targeting the proposer's own role, raise `403 SELF_ELEVATION_BLOCKED` immediately (no proposal row created); otherwise persist `pending` proposal.
- Business Rules: FR-3(b) — structurally impossible to be the change that also approves itself.
- Tests: Self-elevation rejection unit test; valid proposal creation.
- Dependencies: Task 02.
- Definition of Done: Self-elevation blocked before any proposal row exists.

**Task 04 — Implement `MakerCheckerService.approve_proposal()` + Signature Tests**
- Task ID: B-04-T04
- Objective: Approval logic with application-layer self-approval check, atomic apply, and idempotent no-op handling.
- Files to Create: `modules/admin/maker_checker/service.py` (extend), `tests/modules/admin/maker_checker/test_self_approval_db_constraint.py`, `tests/modules/admin/maker_checker/test_approval_idempotency.py`.
- Implementation Details: Compare `approved_by` to `proposal.proposed_by` by `admin_id`; on match raise `403`; on resolved-already proposal return existing state; on valid approval, open a transaction applying the underlying change (e.g., delegate to B-03's permission-update method) + insert approval row + update proposal status atomically.
- Business Rules: Edge Cases 1, 2, 7 all apply here.
- Error Handling: Concurrent-approval race must not raise a hard error to the "losing" request — it must return the resolved state.
- Security: This is the application-layer half of the dual-layer guarantee.
- Tests: Signature Test A (DB constraint direct-INSERT rejection) and Signature Test B (concurrent double-approval, exactly one recorded) — both explicitly required by PRD §5 items 3–4.
- Dependencies: Task 01, Task 03.
- Definition of Done: Both signature tests pass; concurrent-approval integration test confirms exactly one approval persists.

**Task 05 — Implement `POST /v1/admin/change-proposals/{id}/approve` Router**
- Task ID: B-04-T05
- Files to Create: `modules/admin/maker_checker/api.py`.
- Implementation Details: Per §13 API contract; gated by `require_admin_permission` (B-03) for the approver role appropriate to `proposal_type`.
- Dependencies: Task 04, B-03 Task 05.
- Definition of Done: Integration tests pass for approve/reject/self-approval-rejected/redundant-noop/not-found.

**Task 06 — Wire B-03's PATCH Endpoint Through the Proposal Workflow**
- Task ID: B-04-T06
- Objective: `PATCH /v1/admin/roles/{id}/permissions` creates a proposal instead of applying directly.
- Files to Modify: `modules/admin/rbac/service.py` (B-03).
- Implementation Details: Replace any direct-write path with a call to `MakerCheckerService.create_proposal(proposal_type="role_permission_change", ...)`.
- Dependencies: Task 03.
- Definition of Done: PATCH request results in a pending proposal, never an immediate change.

**Task 07 — Wire P0 Self-Elevation/Self-Approval Alerting Hook**
- Task ID: B-04-T07
- Objective: Per PRD §10 DevOps requirement, alert (P0) on any successful self-elevation/self-approval attempt detected in production — a defense-in-depth canary since this should be structurally impossible.
- Implementation Details: Emit a distinct log-level/metric event any time the self-elevation or self-approval rejection branch is hit (the *attempt* itself, even though rejected, is the security-relevant signal worth alerting on if it occurs in production at any non-trivial frequency).
- Dependencies: Task 03, Task 04.
- Definition of Done: Metric/log event emitted and documented for ops team to wire into alerting.

**Task 08 — Implement `GET /v1/admin/change-proposals` List & `GET /v1/admin/change-proposals/{id}` Detail Endpoints**
- Task ID: B-04-T08
- Objective: Expose the read surface the Maker-Checker Approval Queue and Proposal Detail screens (§1.18 screens #15–16) depend on — identified as missing from the original PRD §3.4 API enumeration and added here as this module's correct owning endpoint.
- Why Required: N-05 (Approval Queue & Proposal Detail) cannot function without a way to list pending proposals and fetch a single proposal's full detail/diff; PRD §3.4 only specified the approve action, not the read path, even though the screen inventory clearly requires it.
- Existing Architecture to Follow: Standard FastAPI router pattern; cursor-based pagination consistent with `BaseRepository.list_paginated()`.
- Existing Files to Reuse: `ChangeProposalRepository.list_pending()` (Task 02) — extend to a general `list_paginated(status=, proposal_type=, cursor=, limit=)` rather than a pending-only method, since the Queue may also want to filter by resolved status for historical review.
- Files to Modify: `modules/admin/maker_checker/repository.py`, `modules/admin/maker_checker/service.py`, `modules/admin/maker_checker/schemas.py`, `modules/admin/maker_checker/api.py`.
- Implementation Details: Per §13 API contract; `GET` list defaults to `status=pending` when no filter supplied; detail endpoint eager-loads associated `change_proposal_approval` rows.
- Business Rules: Read-only, no state mutation; authorization mirrors the approve endpoint's approver-role gating (a role that can approve a proposal type should be able to view its queue).
- Validation: `status`/`proposal_type` filter values validated against known enums; `cursor`/`limit` bounds validated.
- Error Handling: `404 PROPOSAL_NOT_FOUND` for unknown `id` on the detail endpoint; `422` for invalid filters.
- Security: Same permission gating as the approve endpoint — no broader read access than the corresponding write access.
- Performance: Cursor-based pagination; index `(status, created_at DESC)` (already defined in §14) directly supports this query pattern.
- Localization: N/A server-side.
- RTL: N/A.
- Analytics: N/A server-side (supports client-fired `operations_dashboard_viewed`-adjacent queue-view events, if any, from N-05).
- Tests: List filtering/pagination test; detail-with-nested-approvals test; 404-on-unknown-id test.
- Documentation: OpenAPI schema for both new routes.
- Dependencies: Task 02 (repository), Task 03/04 (proposal/approval data to list), B-03 Task 05 (`require_admin_permission`).
- Do Not Change: The approve endpoint's own contract (Task 05) — this task is additive only.
- Expected Result: N-05's Approval Queue and Proposal Detail screens have a working data source.
- Definition of Done: Both endpoints integration-tested; N-05's blueprint dependency note resolved.

**Task 09 — Full Test Suite + Documentation**
- Task ID: B-04-T09
- Files to Create: `tests/modules/admin/maker_checker/test_maker_checker_workflow.py`.
- Dependencies: Tasks 01–08.
- Definition of Done: All §27 scenarios green; OpenAPI updated; internal reusable-primitive doc written.

## 30. Definition of Done
- `change_proposal`/`change_proposal_approval` tables live with DB-level self-approval CHECK constraint.
- Self-elevation rejected outright at proposal creation; self-approval rejected at approval time, both by identity not session.
- Approval idempotent under concurrent double-approval.
- No auto-approval timeout exists anywhere in the code.
- B-03's PATCH endpoint routes through this workflow.
- Both signature tests (DB constraint, concurrent approval) pass.

## 31. Final Verification Checklist
- [ ] DB `CHECK` constraint present and verified via direct-INSERT test
- [ ] Self-elevation rejected outright, no proposal row created for that attempt
- [ ] Self-approval rejected by `admin_id` comparison, not session/device
- [ ] Concurrent double-approval test: exactly one approval persists, second is a no-op response
- [ ] No auto-approval timeout code path exists anywhere
- [ ] B-03's `PATCH /v1/admin/roles/{id}/permissions` creates a proposal, never applies directly
- [ ] Feature-flag/config maker-checker routing (owned by B-06/B-07) has a clean integration point here
- [ ] P0 alerting hook emits on any self-elevation/self-approval attempt
- [ ] `GET /v1/admin/change-proposals` (list) and `GET /v1/admin/change-proposals/{id}` (detail) implemented, tested, and permission-gated identically to the approve endpoint
- [ ] OpenAPI docs updated
