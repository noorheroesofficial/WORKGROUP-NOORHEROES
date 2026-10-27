# Blueprint: Support Ticket Queue & Case Management

## 1. Feature Context
Platform: NoorHeroes Admin Portal (Next.js 15 App Router, TypeScript, TanStack Query, Zod). This is the admin console over `support_ticket`/`ticket_message` (B-04) — schema-distinct from E.32's "Support Case Queue" over `support_cases`. This overlap was identified during research (not invented) and is flagged here for reconciliation rather than silently duplicated.

## 2. Parent Feature
C.25 — Notifications (Parent) & Support.

## 3. Sub-feature
N-02 — Support Ticket Queue & Case Management.

## 4. Objective
Build an admin console for viewing, triaging, recategorizing, and responding to `support_ticket` rows, with expedited-queue visual prioritization, while preserving the same hard structural separation B-04 enforces server-side: this console may change ticket status/category and append agent messages, but must **never** itself trigger C.21's deletion-cancellation action.

## 5. Business Requirements
Source: PRD §1.10 Edge Case 3, 7; §3.2 (Admin Support Queue - E-track); §3.5. Cross-referenced gap: E.32's `Feature_E32_User_Management_Child_Safety_View.md` Screen #19–20 "Support Case Queue"/"Support Case Detail" over a `support_cases` table (a different, more general case-management concept — "case queue, including child-deletion and parent-deletion-cancellation cases") does **not** implement C.25's `support_ticket`/`ticket_message` schema; no other document in the project owns this admin surface.
- Ticket recategorization without requiring parent resubmission (Edge Case 7) — an admin action, not exposed to the parent-facing API (B-04 deliberately excludes this from the parent's own surface).
- If the deletion-grace-period cascade completes while a cancellation ticket is open, the ticket must reflect that outcome rather than remaining ambiguously open (Edge Case 3) — this console (or a background process it triggers) is the mechanism that updates the ticket's status/messages to reflect this, though the actual cascade completion itself is C.21's own worker, not initiated here.
- Every mutating action here writes an immutable `audit_log` row, consistent with the platform's mutation-auditing convention already applied elsewhere (e.g., B.17's admin campaign actions).

## 6. Existing Architecture
Same as N-01: strict layering, `RequirePermission`, `DataTable`, standard shared components.

## 7. Existing Code to Reuse
- `BaseResourceClient` — extend for `SupportTicketResourceClient` (list, get, and a narrower `update` limited to status/category fields — never exposing a field that could mutate deletion status).
- `DataTable`, `FilterPanel`, `SearchBar`, `StatusBadge`, `EmptyState`, `ErrorView`, `LoadingState`, `QueryErrorState`, `ConfirmationDialog`.
- `RequirePermission`.
- Existing `audit_log` write pattern (confirm exact mechanism — e.g., a shared `useAuditLog()` hook or an implicit backend-side write triggered by the mutation endpoint itself; do not invent a client-side audit-log-writing mechanism if the backend already handles this transparently on every admin mutation, per the platform's general convention).

## 8. Files to Create
- `src/features/support-tickets/api/support-ticket.client.ts` (extends `BaseResourceClient`)
- `src/features/support-tickets/api/support-ticket.schema.ts`
- `src/features/support-tickets/hooks/use-support-tickets.ts`
- `src/features/support-tickets/hooks/use-support-ticket-detail.ts`
- `src/features/support-tickets/hooks/use-support-ticket-mutations.ts` (status change, recategorize, add agent message)
- `src/features/support-tickets/components/support-ticket-queue-table.tsx`
- `src/features/support-tickets/components/support-ticket-detail-panel.tsx`
- `src/features/support-tickets/components/ticket-category-recategorize-control.tsx`
- `src/app/(dashboard)/support-tickets/page.tsx`
- `src/app/(dashboard)/support-tickets/[id]/page.tsx`
- `src/features/support-tickets/__tests__/support-ticket-queue.test.tsx`
- `src/features/support-tickets/__tests__/support-ticket-no-privileged-action.test.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `SUPPORT.TICKETS` endpoint constant.
- `src/shared/components/dashboard-shell.tsx` — add "Support Tickets" nav entry, guarded by `RequirePermission`.
- `AdminPermission` type — add the relevant permission string(s) if not already present.

## 10. NextJS Requirements
- `SupportTicketResourceClient extends BaseResourceClient<SupportTicket, never, SupportTicketUpdateInput, SupportTicketQueryFilters>` — `create` unimplemented/disabled (admins don't create tickets on a parent's behalf in this console's scope; if that capability is later needed, it's a distinct, deliberate addition, not assumed here); `update` limited strictly to `{ status?, category? }` — **the type itself must not include any deletion-related field**, making the structural boundary visible at the TypeScript level, not just enforced by convention.
- `useSupportTickets(filters)` — list hook with `category`/`status`/`queue_priority` filters, expedited items visually prioritized (e.g., sorted first or highlighted via `StatusBadge` variant).
- `useSupportTicketDetail(id)` — detail hook including the message thread.
- `useSupportTicketMutations()` — `updateStatus(id, status)`, `recategorize(id, category)`, `addAgentMessage(id, body)`, `assign(id, adminId)` (per B-06's `.../assign` endpoint — closes the case-ownership gap flagged in the E.32 reconciliation note) — four narrow, explicit mutations rather than one generic "update ticket" catch-all, keeping the API surface auditable and intention-revealing.
- List page: `FilterPanel` (category, status, queue_priority filters) + `DataTable` (columns: category, status badge, queue_priority badge — expedited visually distinct — created_at) + pagination.
- Detail page: message thread (parent + agent messages, visually distinguished by `sender_type`), status-transition control (`ConfirmationDialog`-gated for `resolved` transitions, since this is a meaningful state change), recategorization control (Edge Case 7), agent follow-up message composer, an "Assign to me / Assign to agent" control (per B-06, closes the `support_cases.owner_id` capability gap).
- **Hard boundary, mirrored from B-04/K-04:** no component, hook, or API client in this feature folder may call, import, or reference C.21's deletion-cancellation endpoint or any deletion-status-mutating client method — recategorizing or resolving an `account_deletion_cancellation` ticket here is purely a ticket-lifecycle action; the actual cancellation (if warranted) remains a separate, deliberate action a Support agent takes in C.21's own admin console.
- Gate behind `RequirePermission` — exact permission string(s) TBD; flag for reconciliation against E.32's overlapping RBAC before finalizing (see §13 note).

## 11. KMP Requirements
N/A.

## 12. Files/Screens
Support Ticket Queue (list) and Support Ticket Detail (message thread + status/category controls) — two routes under `(dashboard)/support-tickets/`.

## 13. API Contract
**Resolved by `Backend/06-admin-support-ticket-queue-case-management-api.md` (B-06)** — both the original contract gap and the E.32 reconciliation flag are now closed (see `ARCHITECTURE_NOTE_support_ticket_vs_support_cases.md`).
- **List:** `GET /v1/admin/support/tickets?category=&status=&queue_priority=&assigned_admin_id=&page=&limit=` (supports `assigned_admin_id=me`)
- **Detail:** `GET /v1/admin/support/tickets/{id}` (cross-family, includes message thread)
- **Update status/category:** `PATCH /v1/admin/support/tickets/{id}` → `{ status?, category? }` only — schema uses `extra="forbid"`, structurally excludes any deletion-related field
- **Add agent message:** `POST /v1/admin/support/tickets/{id}/messages` → `{ body }` (`sender_type` forced server-side to `support_agent`)
- **Assign:** `PATCH /v1/admin/support/tickets/{id}/assign` → `{ admin_id }`
- **Auth:** Bearer admin session + scope (B-06 §17 — exact scope string TBD pending confirmation, same open item as before, now narrowed to just the scope-name question).
- **Admin API:** Yes.
- **Reconciliation resolved:** `support_ticket` (C.25) is the single system of record; no `support_cases` table is introduced. B-06 is the designated backing service for E.32's eventual Support Case Queue screens (scoped to `account_deletion_cancellation`/`safety_concern` categories) — see the architecture note for the full decision record.

## 14. Database Requirements
N/A (frontend only; backend owns `support_ticket`/`ticket_message` per B-04).

## 15. Validation
Zod schema validates ticket list/detail response shapes; recategorization control restricts `category` to B-04's exact FR-9 enum values (no free-text category entry).

## 16. Authentication
Standard Admin Portal session.

## 17. Authorization
`RequirePermission` guard; backend independently enforces RBAC on the (to-be-defined) admin ticket endpoints — coordinate exact scope naming with backend implementation.

## 18. Error Handling
- `QueryErrorState` on list/detail fetch failure with retry.
- `EmptyState` when the queue is empty ("No open support tickets").
- Status/category mutation failure → error toast, optimistic UI does not commit until confirmed by the server response.
- Agent message send failure → message not lost from the composer, retry offered.

## 19. Offline First
N/A — standard web app behavior.

## 20. Local Data
N/A.

## 21. Localization
All admin UI chrome via `useTranslation()`; ticket `message.body` content (parent-authored) rendered as-is, potentially in any of the platform's supported locales — no client-side translation applied to parent messages (agents read/respond in the language the parent used, consistent with how support consoles typically work; do not add machine translation here without explicit product direction).

## 22. RTL
N/A per Admin Portal's unconfirmed RTL scope (same caveat as N-01 §22) — flagged, not assumed.

## 23. Analytics
N/A — internal admin tool.

## 24. Performance
`(category, status)` and `(parent_id, created_at DESC)` indexes (B-04 §14) support this console's filtering; standard `DataTable` server-side pagination.

## 25. Security
- **This blueprint's core guarantee**, mirroring B-04/K-04: zero code path from this console to C.21's deletion-cancellation action. The TypeScript type for the ticket-update payload deliberately excludes any deletion-related field, making this boundary visible at compile time, not just a runtime convention.
- `RequirePermission` client-side guard is UX only; real boundary is backend RBAC.
- Agent messages are attributable (`sender_type`, and implicitly the authenticated admin's identity via the audit log) — no anonymous agent responses.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: `SupportTicketResourceClient.list()`/`.get()` correctly call endpoints and validate responses via Zod.
2. Unit test: expedited-priority tickets are visually distinguished/prioritized in the queue table.
3. Unit test: status-transition to `resolved` requires `ConfirmationDialog` confirmation.
4. Unit test: recategorization control only allows B-04's exact FR-9 enum values.
5. **Structural test (mandatory):** static-analysis or grep-based assertion confirming no file under `src/features/support-tickets/` imports or references any C.21 deletion-cancellation client method/endpoint constant.
6. Unit test: `RequirePermission` blocks access for unauthorized admins.
7. Unit test: empty state and error state render correctly.
8. Unit test: agent message composer preserves in-progress text on send failure.

## 28. Documentation
Component-level JSDoc noting: (a) this console's deliberate non-connection to C.21's cancellation action, citing B-04 §3.5/FR-8; (b) the flagged `support_cases`/E.32 reconciliation note from §13, so future contributors don't silently merge or diverge the two further without a deliberate decision.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement API Endpoint Constant and Zod Schema Against B-06's Confirmed Contract**
- Task ID: N02-T01
- Objective: Type-safe contract matching B-06 exactly, with the deletion-field exclusion built into the TypeScript type itself.
- Why This Is Required: B-06 (`Backend/06-admin-support-ticket-queue-case-management-api.md`) now defines the authoritative admin ticket contract, including the `extra="forbid"` schema restriction this frontend type must mirror.
- Existing Architecture to Follow: `API_ENDPOINTS` registry; existing Zod schema patterns.
- Existing Files to Reuse: `src/shared/constants/api-endpoints.ts`.
- Files to Create: `support-ticket.schema.ts`.
- Files to Modify: `api-endpoints.ts`.
- Implementation Details: `SupportTicketUpdateInput = { status?: TicketStatus; category?: TicketCategory }` — no other fields, matching B-06's `PATCH` schema exactly; add the `.../assign` endpoint and its `{ admin_id }` payload type per B-06 §13.
- Business Rules: FR-9's exact category enum.
- Validation: This IS the validation layer.
- Error Handling: N/A.
- Security: The narrow update-type IS a security-relevant design choice, now verified to match B-06's own `extra="forbid"` schema.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: JSDoc citing B-06 and the deliberate field exclusion.
- Dependencies: B-06 (implemented).
- Do Not Change: Do not modify unrelated endpoint constants.
- Expected Result: Schema/types available, narrow by construction.
- Definition of Done: `SupportTicketUpdateInput` type has no deletion-related field, matching B-06 exactly.

**Task 02 — Build SupportTicketResourceClient and React Query Hooks**
- Task ID: N02-T02
- Objective: Narrow, intention-revealing data-access layer.
- Why This Is Required: Platform's strict layering requirement; three explicit mutation methods rather than one generic update.
- Existing Architecture to Follow: `BaseResourceClient`, existing hook patterns.
- Existing Files to Reuse: `BaseResourceClient`, `apiClient`.
- Files to Create: `support-ticket.client.ts`, `use-support-tickets.ts`, `use-support-ticket-detail.ts`, `use-support-ticket-mutations.ts`.
- Files to Modify: none.
- Implementation Details: `updateStatus()`, `recategorize()`, `addAgentMessage()` as distinct methods per §10.
- Business Rules: Edge Case 7.
- Validation: Via Task 01's Zod schema.
- Error Handling: Standard `apiClient`/`parseApiError`.
- Security: No method on this client can reach a deletion-mutation endpoint (verified structurally in Task 05).
- Performance: React Query caching.
- Localization: N/A (data layer).
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: JSDoc.
- Dependencies: Task 01.
- Do Not Change: Do not modify `BaseResourceClient` itself.
- Expected Result: Hooks function correctly.
- Definition of Done: Matches §10.

**Task 03 — Build Queue List Page with Expedited Prioritization**
- Task ID: N02-T03
- Objective: Visual delivery of the ticket queue, RBAC-restricted.
- Why This Is Required: Core deliverable.
- Existing Architecture to Follow: `DataTable`, `FilterPanel`, `RequirePermission`, existing directory-page pattern.
- Existing Files to Reuse: `DataTable`, `FilterPanel`, `SearchBar`, `EmptyState`, `ErrorView`, `LoadingState`, `RequirePermission`, `usePaginationState`.
- Files to Create: `support-ticket-queue-table.tsx`, `page.tsx` (list).
- Files to Modify: `dashboard-shell.tsx`, `AdminPermission` type.
- Implementation Details: Expedited items visually distinct (e.g., a colored `StatusBadge` variant or sort-first ordering); filters per §10.
- Business Rules: FR-9 queue-priority visibility.
- Validation: N/A (handled upstream).
- Error Handling: Per §18.
- Security: `RequirePermission` guard.
- Performance: N/A.
- Localization: All copy via `useTranslation()`.
- RTL: Per §22 (flagged, not assumed).
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: Component comment.
- Dependencies: Task 02.
- Do Not Change: Do not modify unrelated pages/nav entries.
- Expected Result: Queue page renders correctly, expedited items prioritized visually.
- Definition of Done: Matches §10.

**Task 04 — Build Ticket Detail Page with Status/Recategorization Controls**
- Task ID: N02-T04
- Objective: Message thread, status transitions, recategorization, agent messaging — with the structural non-connection to C.21 preserved throughout.
- Why This Is Required: Core deliverable, and where the hard boundary must be most carefully honored (this is the screen where an agent handling an `account_deletion_cancellation` ticket might be tempted to add a "cancel now" shortcut — explicitly do not).
- Existing Architecture to Follow: `ConfirmationDialog` for the `resolved` transition; existing message-thread UI conventions if any exist elsewhere in the codebase (confirm before inventing a new thread-UI pattern).
- Existing Files to Reuse: `ConfirmationDialog`, `StatusBadge`.
- Files to Create: `support-ticket-detail-panel.tsx`, `ticket-category-recategorize-control.tsx`, `[id]/page.tsx`.
- Files to Modify: none beyond what Task 03 already touched.
- Implementation Details: Per §10; recategorization restricted to the FR-9 enum; status transitions to `resolved` confirmation-gated.
- Business Rules: Edge Case 3, 7; the B-04 §3.5 structural separation, restated at the UI layer.
- Validation: Category enum restriction.
- Error Handling: Per §18.
- Security: The core structural boundary of this entire blueprint.
- Performance: N/A.
- Localization: All copy via `useTranslation()`; parent messages rendered as-authored.
- RTL: Per §22.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: Component comment per §28.
- Dependencies: Task 02.
- Do Not Change: Do not add any control or action that references deletion-cancellation.
- Expected Result: Detail page functional, structurally clean of any deletion-mutation reference.
- Definition of Done: Matches §10, structural boundary intact.

**Task 05 — Write Test Suite Including the Structural No-Privileged-Action Test**
- Task ID: N02-T05
- Objective: Cover §27, with case 5 as the mandatory centerpiece.
- Why This Is Required: Mirrors B-04/K-04's top-priority guarantee at the admin layer — the third and final leg of this feature's core structural separation.
- Existing Architecture to Follow: Existing test conventions; grep/static-analysis-based structural test.
- Existing Files to Reuse: Existing test utilities/mocks.
- Files to Create: `support-ticket-queue.test.tsx`, `support-ticket-no-privileged-action.test.tsx`.
- Files to Modify: none.
- Implementation Details: All 8 cases from §27; the structural test scans `src/features/support-tickets/` source files for any import/reference to C.21's deletion-cancellation client/endpoint.
- Business Rules: FR-8 (restated at the admin layer).
- Validation: N/A.
- Error Handling: N/A.
- Security: Test 5 is the top-priority test in this blueprint.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings citing FR-8, B-04 §3.5.
- Dependencies: Tasks 01–04.
- Do Not Change: N/A.
- Expected Result: All pass.
- Definition of Done: 100% of §27 green, including the structural test.

## 30. Definition of Done
Support Ticket Queue and Detail pages live, RBAC-restricted, expedited tickets visually prioritized, recategorization and status-transition controls functional and confirmation-gated where appropriate, structurally proven to never reach C.21's deletion-cancellation action, all tests green — this completes C.25's full breakdown (B-01 through B-04, K-01 through K-04, N-01, N-02).

## 31. Final Verification Checklist
- [ ] Admin ticket API contract matches B-06's actual implementation exactly, including `.../assign`
- [ ] `SupportTicketUpdateInput` type structurally excludes any deletion-related field, matching B-06's `extra="forbid"` schema
- [ ] No file in this feature folder references C.21's deletion-cancellation action (tested)
- [ ] Expedited tickets visually prioritized in the queue
- [ ] Recategorization restricted to B-04/B-06's exact category enum
- [ ] `resolved` status transition requires confirmation
- [ ] Assignment control ("Assign to me / Assign to agent") functional per B-06
- [ ] E.32 `support_cases` overlap resolved per `ARCHITECTURE_NOTE_support_ticket_vs_support_cases.md` — no separate case-queue table or divergent screen built here
- [ ] Nav entry permission-guarded
