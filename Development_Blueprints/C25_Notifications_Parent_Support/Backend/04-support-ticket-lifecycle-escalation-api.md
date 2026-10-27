# Blueprint: Support Ticket Lifecycle & Escalation API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI, Modular Monolith). Extends the `support` bounded context created in B-03 with the ticket half of the Support Center. This blueprint delivers the feature's second highest-stakes guarantee (alongside B-02's safety-critical enforcement): ticket creation must **never** itself execute a privileged action such as account-deletion cancellation.

## 2. Parent Feature
C.25 — Notifications (Parent) & Support.

## 3. Sub-feature
B-04 — Support Ticket Lifecycle & Escalation API.

## 4. Objective
Implement `POST /v1/support/tickets`, `GET /v1/support/tickets`, `GET /v1/support/tickets/{id}` with category-based expedited/standard queue routing, and structurally prove that ticket creation — including for `account_deletion_cancellation` — has zero side effects on a family's `deletion_pending` status.

## 5. Business Requirements
Source: PRD §1.7 FR-8, FR-9; §1.10 Edge Case 2, 3, 7, 8; §3.4; §3.5; §4.2; §5 Backend AI Code-Generation Prompt items 4–5.
- **FR-8:** "Parent Account Deletion cancellation during the 7-day grace period routes through Support, never self-service" — the ticket-submission flow is the mechanism a parent uses to *initiate* this, tagged `account_deletion_cancellation`, but the actual cancellation remains C.21's exclusive admin-only action.
- **FR-9:** Category taxonomy — `billing`, `technical`, `content_concern`, `safety_concern`, `account_deletion_cancellation`, `general` — each may route to a different queue/SLA; `safety_concern` and `account_deletion_cancellation` receive expedited priority.
- **§3.5 Ticket-to-admin-action separation:** "The Support Service creates and tracks tickets; it never itself performs the underlying privileged action... that remains exclusively a human-Support-agent action via the admin-only endpoint already specified in C.21."
- Edge Case 2: a second, related ticket on the same topic is never auto-merged — each exists independently; agents may manually link on the admin side.
- Edge Case 3: if the deletion grace period cascade completes while a cancellation ticket is still open, the ticket must be updated to reflect the outcome rather than remaining ambiguously "open" forever — cross-ref C.21's cascade-worker boundary logic.
- Edge Case 7: a ticket can be recategorized by a support agent without the parent needing to resubmit.
- Edge Case 8: two co-guardians submitting separately about the same issue are tracked as separate tickets by default.

**Amendment (post-generation, per `ARCHITECTURE_NOTE_support_ticket_vs_support_cases.md`):** E.32's `Feature_E32_User_Management_Child_Safety_View.md` independently defines a `support_cases` table (`id, parent_id, category, status, owner_id, created_at`) for "child-deletion and parent-deletion-cancellation cases" — the exact same real-world cases `support_ticket`'s `account_deletion_cancellation`/`safety_concern` categories cover. Per the reconciliation note, `support_ticket` is the single system of record; `support_cases` is not implemented as a second table. The one capability gap this creates — case ownership/assignment, which `support_cases.owner_id` provided — is closed by adding `assigned_admin_id` to `support_ticket` directly (§10, §14 below).

## 6. Existing Architecture
Builds directly on B-03's `support` context scaffold (`models.py`/`schemas.py`/`repository.py`/`service.py`/`api.py`, `SupportRouter`). Reuses `FAST-API-INSTRUCTIONS.md` §11 Layer Rules (no direct DB access in routers, no manual commits outside the session lifecycle, no naked exceptions) and §7's Router → Service → Repository → DB flow.

## 7. Existing Code to Reuse
- `SupportRouter` (from B-03) — add ticket routes to the same router rather than creating a second router for the same context.
- `BaseRepository[ModelT]` for standard CRUD/pagination.
- `BaseService`, `core/exceptions.py` `NotFoundError`/`ValidationError`/`AuthorizationError`.
- Parent-Session-Only Gate pattern (B-01/B-02, C.20's B-01).
- C.21's admin-only deletion-cancellation endpoint — **referenced only, never imported or called** from this module (the entire point of this blueprint's core guarantee).

## 8. Files to Create
- `tests/modules/support/test_ticket_lifecycle_api.py`
- `tests/modules/support/test_ticket_no_privileged_action_structural.py`
- `alembic/versions/xxxx_create_support_ticket_ticket_message.py`

## 9. Files to Modify
- `src/noorheroes/modules/support/models.py` — add `SupportTicket`, `TicketMessage` ORM models.
- `src/noorheroes/modules/support/schemas.py` — add `TicketCreateRequest`, `TicketResponse`, `TicketDetailResponse`, `TicketMessageRequest`.
- `src/noorheroes/modules/support/repository.py` — add `TicketRepository` methods (or extend the existing `FaqRepository` file into a shared `repository.py` with a distinct `TicketRepository` class — do not merge FAQ and ticket query logic into one class; keep them as separate classes within the module for clarity, per the platform's per-entity repository convention seen elsewhere, e.g. `UserRepository`/`ChildRepository` both living in `identity`'s `repository.py`).
- `src/noorheroes/modules/support/service.py` — add `TicketService(BaseService)`.
- `src/noorheroes/modules/support/api.py` — add ticket routes to `SupportRouter`.

## 10. Backend Requirements
- `SupportTicket`: `ticket_id` (PK), `parent_id` (FK), `category` (CHECK constraint per §4.2's exact enum), `status` (CHECK `submitted|in_progress|resolved`), `queue_priority`, `assigned_admin_id` (FK to the admin/operator identity, nullable — added per the E.32 reconciliation note, absent from the original PRD §4.2 schema), `created_at`, `resolved_at`.
- `assigned_admin_id` is admin-mutable only (via `B-06`'s assignment endpoint) — never parent-writable through this blueprint's own routes.
- `TicketMessage`: `message_id` (PK), `ticket_id` (FK), `sender_type` (CHECK `parent|support_agent`), `body`, `created_at` — append-only.
- `POST /v1/support/tickets`: validates `category` against the FR-9 enum; routes `account_deletion_cancellation`/`safety_concern` → `queue_priority='expedited'`, all others → `standard`; accepts optional `related_family_deletion_request_id`.
- **Hard boundary (this blueprint's core guarantee):** `TicketService.create_ticket()` must contain **zero** code path that calls C.21's `POST /v1/admin/parent-deletion/{family_id}/cancel` (or any equivalent cancellation logic, ORM mutation of `deletion_pending`, or event that triggers it) — ticket creation is a pure `INSERT`, full stop. A human Support agent's separate, audited admin action is the only path to actual cancellation.
- `GET /v1/support/tickets` / `GET /v1/support/tickets/{id}`: own-family-scoped; detail includes messages.
- No ticket auto-merge logic anywhere (Edge Case 2) — creation is always a fresh independent row.
- Status transitions (`submitted → in_progress → resolved`) and category recategorization (Edge Case 7) are **not** parent-writable via this API — they are admin-only mutations delivered through N-02's admin endpoints, not exposed here. This endpoint is read-only for status/category from the parent's perspective, plus follow-up-message append.

## 11. KMP Requirements
N/A for backend scope — consumed by K-04's `SupportRepository.submitTicket()/getTickets()`.

## 12. NextJS Requirements
N/A for backend scope — N-02 requires new admin-scoped mutation endpoints (`PATCH /v1/admin/support/tickets/{id}` for status/category changes, `POST .../messages` for agent responses) not specified in C.25's own §3.4 list; explicitly deferred to N-02's own blueprint, not assumed here.

## 13. API Contract
### `POST /v1/support/tickets`
- **Auth:** Bearer (Parent session)
- **Request:** `{ "category": "account_deletion_cancellation|billing|technical|content_concern|safety_concern|general", "message": "...", "related_family_deletion_request_id": null }`
- **Response 200:** `{ "ticket_id": "...", "status": "submitted", "queue_priority": "expedited|standard" }`

### `GET /v1/support/tickets`
- **Response 200:** `{ "tickets": [ { "ticket_id", "category", "status", "queue_priority", "created_at" } ] }` (own-family-scoped)

### `GET /v1/support/tickets/{id}`
- **Response 200:** Ticket detail + `messages: [ { "message_id", "sender_type", "body", "created_at" } ]`
- **Response 404:** Not found or not owned by requesting family.

### `POST /v1/support/tickets/{id}/messages`
- **Request:** `{ "body": "..." }` (parent follow-up)
- **Response 200:** Created `TicketMessage`.

## 14. Database Requirements
New tables per PRD §4.2: `support_ticket` (Index `(parent_id, created_at DESC)`, Index `(category, status)`, additionally `Index (assigned_admin_id, status)` to support B-06's "my assigned tickets" admin queue view), `ticket_message` (Index `(ticket_id, created_at)`). Both append-only in effect — no soft-delete rules apply (§4.4: "N/A for tickets/messages, append-only, permanent record"). `assigned_admin_id` is a plain nullable FK column addition, not a new table — no migration conflict with the original §4.2 schema, purely additive.

## 15. Validation
- `category` validated against the exact FR-9 enum — reject unknown values with `422`.
- `related_family_deletion_request_id`, if provided, should correspond to an actual pending deletion request for this family (soft validation — log a warning rather than hard-reject if it doesn't, since this is a cross-reference convenience field, not a security boundary).
- Follow-up `body` non-empty.

## 16. Authentication
Reuses `get_current_parent()`.

## 17. Authorization
Parent-Session-Only Gate; own-family-scoped row access on `GET` routes; parents may only append messages/create tickets, never mutate `status`/`category` (admin-only, N-02).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Unknown `category` value | `422` |
| Ticket not found / not owned by family | `404` |
| Follow-up on a resolved ticket | Allowed (reopens conversation; does not force a status change automatically — status remains agent-controlled) |
| Child-mode token | `403 CHILD_MODE_TOKEN_REJECTED` |
| Network failure on client submission | Client-side retry with local draft preservation (K-04); server-side idempotency key support recommended so a client retry doesn't create duplicate tickets |
| Deletion grace period expires while ticket open | Handled by C.21's cascade worker updating ticket status via the admin path (Edge Case 3) — not a direct concern of this endpoint's own logic, but its `status` field must be able to reflect this outcome once N-02/C.21 write it |

## 19. Offline First
N/A server-side; K-04 requires connectivity for submission per PRD §1.14, with local draft preservation on failure.

## 20. Local Data
N/A.

## 21. Localization
Ticket `category`/`status` are machine-readable codes; K-04 owns all display-string localization.

## 22. RTL
N/A (backend).

## 23. Analytics
No server-side emission required; `support_ticket_submitted` (with `category`), `support_ticket_status_viewed`, `support_ticket_follow_up_added`, `account_deletion_cancellation_ticket_submitted` (§1.19) are client-fired (K-04).

## 24. Performance
`(parent_id, created_at DESC)` and `(category, status)` indexes support both the parent-facing list view and the admin queue's (N-02) filtering needs.

## 25. Security
- **This blueprint's core guarantee**, alongside B-02's safety-critical enforcement, is the single highest-priority control in the entire C.25 feature: ticket creation never self-executes a privileged action.
- Own-family-scoped access prevents cross-family ticket disclosure.
- `sender_type` CHECK constraint prevents a parent-authored message from being mis-tagged as `support_agent` (which would misrepresent official responses).

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: `account_deletion_cancellation` and `safety_concern` categories route to `queue_priority='expedited'`.
2. Unit test: all other categories route to `standard`.
3. **Structural/behavioral test (mandatory, highest priority):** creating a ticket with `category='account_deletion_cancellation'` produces **zero** side effects on the family's `deletion_pending` status — assert the family record is byte-for-byte unchanged before/after ticket creation, and assert (via mock/spy) that no call is made to C.21's cancellation service/endpoint (§5 item 5).
4. Integration test: two tickets on the same topic from the same parent are stored as two independent rows (Edge Case 2, no auto-merge).
5. Integration test: a follow-up message appends correctly to an existing ticket regardless of its current status.
6. Integration test: `GET /v1/support/tickets/{id}` returns `404` for a ticket belonging to a different family.
7. Integration test: child-mode token rejected on all routes.
8. Test: unknown `category` value returns `422`.

## 28. Documentation
- OpenAPI descriptions for all four endpoints.
- Module-level docstring on `TicketService` explicitly stating: "This service creates and tracks tickets only. It must NEVER call C.21's admin-only deletion-cancellation endpoint or mutate `deletion_pending` — that is exclusively a human Support agent's separate, audited action" — as a standing constraint for future contributors, citing FR-8 and §3.5.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create Ticket Models and Migration**
- Task ID: B04-T01
- Objective: `SupportTicket`/`TicketMessage` schema.
- Why This Is Required: Core persistence for the ticket lifecycle.
- Existing Architecture to Follow: B-03's `support` module scaffold; `infrastructure/db/base.py` `Base`/`TimestampMixin`.
- Existing Files to Reuse: `modules/support/models.py` (extend the file B-03 created).
- Files to Create: Alembic migration.
- Files to Modify: `modules/support/models.py`.
- Implementation Details: Per §4.2, including both CHECK constraints and all indexes, plus the `assigned_admin_id` nullable FK column and its `(assigned_admin_id, status)` index per the E.32 reconciliation amendment (§5).
- Business Rules: FR-9, §4.2.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: Indexes as specified.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: Docstrings.
- Dependencies: B-03 (must be generated/implemented first — this blueprint extends its scaffold).
- Do Not Change: Do not modify `FaqArticle`/`FaqFeedback` from B-03.
- Expected Result: Tables exist with correct constraints.
- Definition of Done: Matches §4.2.

**Task 02 — Implement TicketRepository**
- Task ID: B04-T02
- Objective: Data-access layer for tickets/messages, family-scoped.
- Why This Is Required: Core query logic.
- Existing Architecture to Follow: `BaseRepository[ModelT]`.
- Existing Files to Reuse: `common/base_repository.py`.
- Files to Create: none.
- Files to Modify: `modules/support/repository.py` (add `TicketRepository` as a distinct class alongside B-03's `FaqRepository`).
- Implementation Details: `create_ticket(parent_id, category, message, related_id) -> SupportTicket`, `list_for_parent(parent_id) -> list[SupportTicket]`, `get_detail(ticket_id, parent_id) -> SupportTicket | None`, `add_message(ticket_id, sender_type, body) -> TicketMessage`.
- Business Rules: Family-scoping, append-only messages.
- Validation: N/A.
- Error Handling: Returns `None` for not-found/not-owned (service maps to 404).
- Security: Family-scoping is the core access control.
- Performance: Uses `(parent_id, created_at DESC)` index.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: Docstrings.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Repository correctly scoped and structured.
- Definition of Done: No method accepts a `family_id` other than the authenticated session's own.

**Task 03 — Implement TicketService with Queue Routing and the Privileged-Action Boundary**
- Task ID: B04-T03
- Objective: Business logic, including the category-routing rule and the hard non-negotiable separation from C.21's cancellation logic.
- Why This Is Required: This IS the feature's core guarantee.
- Existing Architecture to Follow: `BaseService`, `core/exceptions.py`.
- Existing Files to Reuse: `TicketRepository` (Task 02).
- Files to Create: none.
- Files to Modify: `modules/support/service.py`.
- Implementation Details: `create_ticket()` performs category validation → queue-priority derivation → a single `INSERT` via the repository → return response. **No import of C.21's module anywhere in this file.**
- Business Rules: FR-8, FR-9, §3.5 — treated as the top-priority guarantee of this entire blueprint.
- Validation: Category enum check.
- Error Handling: `422` on unknown category.
- Security: The core control — verified structurally in Task 06.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Tasks 05–06.
- Documentation: Module docstring per §28.
- Dependencies: Task 02.
- Do Not Change: N/A.
- Expected Result: Ticket creation is a pure data operation.
- Definition of Done: Zero coupling to C.21's cancellation code path, proven in Task 06.

**Task 04 — Add Ticket Routes to SupportRouter**
- Task ID: B04-T04
- Objective: Expose all four endpoints under the existing gate pattern.
- Why This Is Required: Core deliverable.
- Existing Architecture to Follow: B-03's `SupportRouter`; Parent-Session-Only Gate.
- Existing Files to Reuse: `modules/support/api.py`.
- Files to Create: none.
- Files to Modify: `modules/support/api.py`, `modules/support/schemas.py`.
- Implementation Details: Per §13 exactly.
- Business Rules: N/A.
- Validation: Pydantic schema validation.
- Error Handling: Per §18.
- Security: Router-level Parent-Session-Only Gate; family-scoped row checks in the service layer.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: OpenAPI.
- Dependencies: Task 03.
- Do Not Change: Do not alter B-03's FAQ routes on the same router.
- Expected Result: All 4 routes live.
- Definition of Done: Matches §13.

**Task 05 — Write Standard Test Suite**
- Task ID: B04-T05
- Objective: Cover §27 items 1–2, 4–8.
- Why This Is Required: Standard coverage.
- Existing Architecture to Follow: pytest conventions.
- Existing Files to Reuse: Existing auth fixtures.
- Files to Create: `tests/modules/support/test_ticket_lifecycle_api.py`.
- Files to Modify: none.
- Implementation Details: Cases 1–2, 4–8 from §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact status codes.
- Security: Family-scoping and child-mode-token tests are security-critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–04.
- Do Not Change: N/A.
- Expected Result: All pass.
- Definition of Done: Cases 1–2, 4–8 green.

**Task 06 — Write the Zero-Side-Effect Structural/Behavioral Test**
- Task ID: B04-T06
- Objective: Prove ticket creation for `account_deletion_cancellation` never mutates deletion status or calls C.21's endpoint.
- Why This Is Required: PRD §5 item 5 — the single highest-priority guarantee in this entire service.
- Existing Architecture to Follow: Test isolation via mocking/spying on any client/service object that could reach C.21's endpoint; direct DB-state comparison before/after.
- Existing Files to Reuse: C.21's family/deletion-request test fixtures if they exist (confirm before inventing new ones).
- Files to Create: `tests/modules/support/test_ticket_no_privileged_action_structural.py`.
- Files to Modify: none.
- Implementation Details: Set up a family with `deletion_pending=true`; create a ticket with `category='account_deletion_cancellation'`; assert the family's `deletion_pending` field and all other deletion-related fields are byte-for-byte unchanged; assert (via spy/mock) zero calls to any C.21 cancellation code path; additionally, a static import-check confirming `modules/support/service.py` has no import from C.21's module.
- Business Rules: FR-8, §3.5.
- Validation: N/A.
- Error Handling: N/A.
- Security: This is the top-priority test in the entire C.25 feature alongside B-02's Task 05.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the test.
- Documentation: Test docstring explicitly citing FR-8 and §3.5.
- Dependencies: Tasks 01–04.
- Do Not Change: N/A.
- Expected Result: Test passes now; will fail as a regression signal if anyone later wires direct cancellation logic into ticket creation.
- Definition of Done: Structural/behavioral test green, treated as CI-mandatory.

## 30. Definition of Done
`support_ticket`/`ticket_message` tables live; `POST/GET /v1/support/tickets`, `GET /v1/support/tickets/{id}`, `POST .../messages` functional with correct expedited/standard routing, structurally proven to never self-execute the deletion-cancellation action, all tests green.

## 31. Final Verification Checklist
- [ ] `account_deletion_cancellation`/`safety_concern` route to `queue_priority='expedited'` (tested)
- [ ] Ticket creation has zero measurable side effects on `deletion_pending` status (tested)
- [ ] No import of C.21's cancellation module anywhere in `modules/support/`
- [ ] No auto-merge of duplicate/related tickets (tested)
- [ ] Family-scoped access enforced on all `GET` routes
- [ ] Status/category are not parent-mutable via this API
- [ ] No PostgreSQL/Redis credential files touched
- [ ] B-03's FAQ routes/tables unaffected
- [ ] `assigned_admin_id` present on `support_ticket`, nullable, admin-mutable only (never exposed on parent-facing routes)
- [ ] No separate `support_cases` table introduced (superseded by this table per the reconciliation note)
