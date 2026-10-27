# Blueprint: Admin Support Ticket Queue & Case Management API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI, Modular Monolith). Extends the `support` bounded context (B-03, B-04) with the admin-side queue/case-management surface. Per `ARCHITECTURE_NOTE_support_ticket_vs_support_cases.md`, this blueprint is also the intended backing service for E.32's eventual Support Case Queue screens (for the `account_deletion_cancellation`/`safety_concern` subset of `support_ticket` rows) — no separate `support_cases` table is introduced anywhere in the platform.

## 2. Parent Feature
C.25 — Notifications (Parent) & Support.

## 3. Sub-feature
B-06 — Admin Support Ticket Queue & Case Management API.

## 4. Objective
Implement `GET /v1/admin/support/tickets`, `GET /v1/admin/support/tickets/{id}`, `PATCH /v1/admin/support/tickets/{id}` (status/category), `POST /v1/admin/support/tickets/{id}/messages`, and `PATCH /v1/admin/support/tickets/{id}/assign` — with the same hard structural boundary B-04 enforces on the parent-facing side: **none of these endpoints may call, trigger, or reference C.21's deletion-cancellation action.**

## 5. Business Requirements
Source: PRD §1.10 Edge Case 3, 7; §3.5; B-04's own §5/§10 (parent-facing ticket lifecycle, extended here to the admin side); `ARCHITECTURE_NOTE_support_ticket_vs_support_cases.md`.
- Recategorization without requiring parent resubmission (Edge Case 7) — admin-only mutation, not exposed on B-04's parent-facing routes.
- Status transitions (`submitted → in_progress → resolved`) are admin-only (B-04 explicitly excludes parent write access to `status`).
- If a family's deletion grace period cascade completes while a cancellation ticket is open, the ticket's status must be updated to reflect that outcome (Edge Case 3) — this endpoint provides the mutation surface an admin (or a coordinated background process reacting to C.21's cascade completion event) uses to reflect that; it does not itself initiate the cascade.
- **Ticket-to-privileged-action separation (this blueprint's core guarantee, mirroring B-04 §3.5):** an admin resolving or recategorizing an `account_deletion_cancellation` ticket through this API performs a pure ticket-lifecycle mutation. The actual deletion-cancellation remains exclusively reachable via C.21's own admin-only cancellation endpoint, invoked as a **separate, deliberate action** by the agent — never automatically triggered by a status change here.
- Assignment (`assigned_admin_id`, added to `support_ticket` in B-04's amendment) lets an agent claim ownership of a case, closing the capability gap E.32's `support_cases.owner_id` originally covered.

## 6. Existing Architecture
Extends B-04's `TicketRepository`/`TicketService`/`SupportRouter`. Per `FAST-API-INSTRUCTIONS.md` §5.2 `admin` context: `AdminAuditLog`, `AdminService.log_action()` — every mutating action here writes an audit entry, consistent with B.17's and E.32's own admin-mutation-auditing convention.

## 7. Existing Code to Reuse
- `TicketRepository`/`TicketService` (B-04) — extend with admin-scoped methods rather than forking.
- `get_current_admin()` / `require_admin_scope()` (`core/deps.py`).
- `AdminService.log_action()` audit pattern.
- C.21's admin-only deletion-cancellation endpoint — **referenced only in documentation/tests as the thing this module must never call**, never imported.

## 8. Files to Create
- `tests/modules/support/test_admin_ticket_queue_api.py`
- `tests/modules/support/test_admin_ticket_no_privileged_action_structural.py`

## 9. Files to Modify
- `src/noorheroes/modules/support/schemas.py` — add `AdminTicketListResponse`, `AdminTicketDetailResponse`, `TicketStatusUpdateRequest`, `TicketRecategorizeRequest`, `AdminTicketMessageRequest`, `TicketAssignRequest`.
- `src/noorheroes/modules/support/repository.py` — extend `TicketRepository` with `admin_list_tickets(category, status, queue_priority, assigned_admin_id, cursor, limit)`, `admin_get_detail(id)` (no family-scoping restriction — admin sees all families' tickets), `update_status(id, status)`, `update_category(id, category)`, `assign(id, admin_id)`, `add_agent_message(id, admin_id, body)`.
- `src/noorheroes/modules/support/service.py` — add `TicketService.admin_*` methods, each writing an audit log entry.
- `src/noorheroes/modules/support/api.py` — add admin routes.

## 10. Backend Requirements
- `GET /v1/admin/support/tickets?category=&status=&queue_priority=&assigned_admin_id=`: cross-family (admin sees all tickets, unlike B-04's family-scoped parent view); supports an `assigned_admin_id=me` convenience filter for "my assigned tickets."
- `GET /v1/admin/support/tickets/{id}`: full detail + message thread, cross-family.
- `PATCH /v1/admin/support/tickets/{id}`: `{ status?, category? }` only — **schema structurally excludes any deletion-mutation field**, mirroring N-02's client-side type-level exclusion.
- `POST /v1/admin/support/tickets/{id}/messages`: `{ body }`, `sender_type` forced to `support_agent` server-side (never client-suppliable, preventing message-origin spoofing).
- `PATCH /v1/admin/support/tickets/{id}/assign`: `{ admin_id }` — sets `assigned_admin_id`.
- Every mutating route (`PATCH .../{id}`, `.../messages`, `.../assign`) writes an `AdminAuditLog` entry recording the admin identity, action, and before/after values for status/category changes.
- **Core guarantee:** `TicketService`'s admin methods contain zero import of, or call to, C.21's cancellation service/endpoint — verified structurally in Task 05, mirroring B-04's own Task 06.
- Recategorizing or resolving a ticket never auto-triggers any downstream action beyond the `support_ticket` row's own state — no side effects on `deletion_pending` or any other family-level status field.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
Consumed directly by N-02's `SupportTicketResourceClient` — this blueprint is the authoritative resolution of N-02's originally-flagged API contract gap, and the intended backing service for any future E.32 Support Case Queue implementation per the reconciliation note.

## 13. API Contract
### `GET /v1/admin/support/tickets?category=&status=&queue_priority=&assigned_admin_id=&page=&limit=`
- **Auth:** Bearer admin session + support/case-management scope (confirm exact scope-string convention — do not invent `support_manager` as a literal string without checking existing scope naming)
- **Response 200:** `{ items: [ { ticket_id, parent_id, category, status, queue_priority, assigned_admin_id, created_at, resolved_at } ], total, page, limit, totalPages }`

### `GET /v1/admin/support/tickets/{id}`
- **Response 200:** Full detail + `messages: [ { message_id, sender_type, body, created_at } ]`

### `PATCH /v1/admin/support/tickets/{id}`
- **Request:** `{ status?: "submitted"|"in_progress"|"resolved", category?: "billing"|"technical"|"content_concern"|"safety_concern"|"account_deletion_cancellation"|"general" }` — no other fields accepted.
- **Response 200:** Updated ticket.

### `POST /v1/admin/support/tickets/{id}/messages`
- **Request:** `{ body: string }`
- **Response 201:** Created message, `sender_type: "support_agent"` forced.

### `PATCH /v1/admin/support/tickets/{id}/assign`
- **Request:** `{ admin_id: string }`
- **Response 200:** Updated ticket with `assigned_admin_id` set.

## 14. Database Requirements
No new tables — uses `support_ticket`/`ticket_message` (B-04), including the `assigned_admin_id` column added in B-04's reconciliation amendment. No `support_cases` table is created (per the reconciliation note).

## 15. Validation
`status`/`category` validated against their exact enums (no free-text); `admin_id` on assignment validated as an existing admin/operator identity (per E.28's Role Registry).

## 16. Authentication
`get_current_admin()`.

## 17. Authorization
`require_admin_scope(...)` — exact scope TBD pending confirmation against the platform's existing scope taxonomy (same open item N-02 flagged); recommend reusing whatever scope E.32's own Support Case Queue would have required, since this blueprint is designed to back that use case too.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Non-admin or wrong-scope token | `403` |
| Ticket not found | `404` |
| Unknown `status`/`category` value | `422` |
| Assign to a non-existent admin identity | `422` |
| `PATCH` payload containing an unrecognized field | `422` (schema rejects unknown fields — defense-in-depth against a future accidental deletion-field addition) |
| DB failure | `500` via standard `DomainError` handler |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
N/A (admin-facing, machine-readable codes; message `body` rendered as-authored).

## 22. RTL
N/A (backend).

## 23. Analytics
Every mutation writes an `AdminAuditLog` entry — this is the accountability trail, not a separate end-user analytics event.

## 24. Performance
Reuses B-04's `(category, status)` and the new `(assigned_admin_id, status)` index (added in B-04's amendment) for the "my assigned tickets" filter.

## 25. Security
- **This blueprint's core guarantee**, completing the three-layer structural separation established across B-04 (backend, parent-facing), K-04 (client), and N-02 (admin client): this admin backend surface also has zero code path to C.21's deletion-cancellation action.
- `PATCH .../{id}`'s schema-level field restriction is defense-in-depth beyond just "the service doesn't call it" — even a malformed/malicious request body cannot smuggle in a deletion-related field, since the schema doesn't define one.
- `sender_type` forced server-side prevents message-origin spoofing (an agent could not, even accidentally, post a message that renders as if it came from the parent).
- Cross-family read access is admin-appropriate here (unlike B-04's parent-facing family-scoping) but must remain behind the admin auth/RBAC boundary.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: `PATCH` correctly updates `status`/`category` independently and combined.
2. Unit test: `PATCH` with an unrecognized field (e.g., attempting to smuggle a deletion-related field) is rejected with `422` by schema validation before reaching any service logic.
3. Unit test: `POST .../messages` always forces `sender_type: "support_agent"` regardless of request payload content.
4. Unit test: `PATCH .../assign` correctly sets `assigned_admin_id`.
5. Unit test: every mutating route writes an `AdminAuditLog` entry with correct before/after values.
6. Unit test: non-admin or wrong-scope token rejected on all 5 routes.
7. **Structural/behavioral test (mandatory, mirrors B-04 Task 06):** resolving or recategorizing an `account_deletion_cancellation` ticket produces zero side effects on the associated family's `deletion_pending` status, and zero calls (via spy/mock) to C.21's cancellation service/endpoint; static import-check confirms `modules/support/service.py`'s admin methods have no import from C.21's module.
8. Integration test: `assigned_admin_id=me` filter correctly narrows results to the requesting admin's assigned tickets.

## 28. Documentation
OpenAPI descriptions for all 5 routes; module docstring explicitly stating the same standing constraint as B-04: "This service's admin methods must NEVER call C.21's deletion-cancellation endpoint or mutate `deletion_pending` — recategorization and resolution are pure ticket-lifecycle actions," citing this blueprint as the admin-side counterpart of B-04 §3.5 and noting it is the designated backing service for E.32's Support Case Queue per the reconciliation note.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend TicketRepository with Admin-Scoped, Cross-Family Methods**
- Task ID: B06-T01
- Objective: Data-access methods without family-scoping, supporting admin filters.
- Why This Is Required: Admins legitimately need cross-family visibility; B-04's parent-facing methods are family-scoped by design and must not be altered.
- Existing Architecture to Follow: B-04's `TicketRepository`.
- Existing Files to Reuse: `modules/support/repository.py`.
- Files to Create: none.
- Files to Modify: `modules/support/repository.py`.
- Implementation Details: Per §9/§10; `assigned_admin_id=me` resolves to the requesting admin's own ID at the service layer, not a literal DB value.
- Business Rules: §10.
- Validation: N/A.
- Error Handling: Returns `None` for not-found.
- Security: These methods must never be reachable from parent-facing routes.
- Performance: Uses `(category, status)`, `(assigned_admin_id, status)` indexes.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Docstrings.
- Dependencies: B-04 (including its `assigned_admin_id` amendment).
- Do Not Change: Do not alter B-04's parent-facing repository methods.
- Expected Result: Admin methods return cross-family data correctly.
- Definition of Done: No accidental family-scoping filter leaks into these methods (inverse concern from B-04's own guarantee).

**Task 02 — Implement Admin Service Methods with Audit Logging and the Privileged-Action Boundary**
- Task ID: B06-T02
- Objective: Business logic for status/category/assign/message mutations, each audited, none touching C.21.
- Why This Is Required: This IS the feature's core guarantee at the admin layer.
- Existing Architecture to Follow: `AdminService.log_action()` pattern; B-04's `TicketService`.
- Existing Files to Reuse: `modules/admin/service.py` (or equivalent), `TicketRepository` (Task 01).
- Files to Create: none.
- Files to Modify: `modules/support/service.py`.
- Implementation Details: `admin_update_status()`, `admin_recategorize()`, `admin_assign()`, `admin_add_message()` — each a single, narrow operation, each logging before/after values. **Zero import of C.21's module anywhere in these methods.**
- Business Rules: Edge Case 3, 7; §3.5 (restated for the admin layer).
- Validation: Enum checks for status/category.
- Error Handling: `422` on invalid values.
- Security: The core control — verified structurally in Task 05.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Tasks 04–05.
- Documentation: Module docstring per §28.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Each admin mutation is a pure, audited, narrowly-scoped operation.
- Definition of Done: Zero coupling to C.21, proven in Task 05.

**Task 03 — Add Admin Ticket Routes with RBAC Gate and Schema-Level Field Restriction**
- Task ID: B06-T03
- Objective: Expose all 5 endpoints, scope-gated, with `PATCH`'s schema deliberately excluding any deletion-related field.
- Why This Is Required: Core deliverable; the schema restriction is defense-in-depth for the core guarantee.
- Existing Architecture to Follow: `require_admin_scope()` pattern.
- Existing Files to Reuse: `modules/support/api.py`.
- Files to Create: none.
- Files to Modify: `modules/support/api.py`, `modules/support/schemas.py`.
- Implementation Details: Per §13; `TicketStatusUpdateRequest`/`TicketRecategorizeRequest` (or a combined narrow schema) with `extra="forbid"` (Pydantic v2) so unrecognized fields are rejected outright.
- Business Rules: N/A.
- Validation: Pydantic schema, `extra="forbid"`.
- Error Handling: Per §18.
- Security: Router-level scope gate + schema-level field restriction, two independent layers.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: OpenAPI.
- Dependencies: Task 02.
- Do Not Change: Do not alter B-04's parent-facing routes on the same router.
- Expected Result: All 5 routes live, schema-restricted.
- Definition of Done: Matches §13; `extra="forbid"` confirmed via Task 04's test 2.

**Task 04 — Write Standard Test Suite**
- Task ID: B06-T04
- Objective: Cover §27 items 1–6, 8.
- Why This Is Required: Standard coverage.
- Existing Architecture to Follow: pytest conventions.
- Existing Files to Reuse: Existing admin-auth test fixtures.
- Files to Create: `tests/modules/support/test_admin_ticket_queue_api.py`.
- Files to Modify: none.
- Implementation Details: Cases 1–6, 8 from §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact status codes.
- Security: Scope-rejection and message-spoofing-prevention tests are security-critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All pass.
- Definition of Done: Cases 1–6, 8 green.

**Task 05 — Write the Zero-Side-Effect Structural/Behavioral Test**
- Task ID: B06-T05
- Objective: Prove admin ticket mutations never reach C.21's deletion-cancellation action.
- Why This Is Required: The top-priority guarantee of this blueprint, mirroring B-04's Task 06 at the admin layer — completes the three-layer structural separation (B-04, B-06, N-02/K-04).
- Existing Architecture to Follow: Same mock/spy + DB-state-comparison approach as B-04 Task 06.
- Existing Files to Reuse: C.21's family/deletion-request test fixtures if they exist.
- Files to Create: `tests/modules/support/test_admin_ticket_no_privileged_action_structural.py`.
- Files to Modify: none.
- Implementation Details: Set up a family with `deletion_pending=true` and an open `account_deletion_cancellation` ticket; resolve and recategorize the ticket via this blueprint's admin endpoints; assert the family's `deletion_pending` field is byte-for-byte unchanged and zero calls occur to any C.21 cancellation code path; static import-check on `modules/support/service.py`'s admin methods.
- Business Rules: §3.5, mirrored from B-04.
- Validation: N/A.
- Error Handling: N/A.
- Security: This is a top-priority test, alongside B-04 Task 06 and K-04's/N-02's equivalents — the full guarantee only holds if all four layers pass their respective versions of this test.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the test.
- Documentation: Test docstring citing §3.5 and cross-referencing B-04 Task 06.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: Test passes now; fails as a regression signal if anyone later wires direct cancellation logic into admin ticket resolution.
- Definition of Done: Structural/behavioral test green, treated as CI-mandatory alongside B-04's equivalent suite.

## 30. Definition of Done
Admin ticket queue/case-management endpoints live, cross-family, RBAC-scoped, every mutation audited, `assigned_admin_id` assignment functional, structurally proven to never reach C.21's deletion-cancellation action — resolves N-02's originally-flagged API contract gap and serves as the designated backing service for any future E.32 Support Case Queue implementation, completing C.25's full backend scope (B-01 through B-06).

## 31. Final Verification Checklist
- [ ] `PATCH .../{id}` schema uses `extra="forbid"` and defines no deletion-related field
- [ ] Zero calls to C.21's cancellation code path from any admin ticket mutation (tested)
- [ ] Every mutation (status, category, assign, message) writes an audit log entry (tested)
- [ ] `sender_type` on admin-posted messages always forced to `support_agent`, never client-suppliable (tested)
- [ ] Cross-family read access correctly gated behind admin RBAC (not family-scoped like B-04's parent routes)
- [ ] No `support_cases` table introduced anywhere
- [ ] `assigned_admin_id=me` filter resolves correctly
- [ ] No PostgreSQL/Redis credential files touched
