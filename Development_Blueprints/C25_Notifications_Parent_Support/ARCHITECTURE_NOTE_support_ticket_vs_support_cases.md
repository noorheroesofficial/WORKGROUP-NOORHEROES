# Architecture Reconciliation Note: `support_ticket` (C.25) vs. `support_cases` (E.32)

## Existing Architecture
Two independent PRDs each introduce a support/case-tracking concept:
- **E.32** (`Feature_E32_User_Management_Child_Safety_View.md`, Admin & Scholar Portal) defines a **Support Case Service** over a `support_cases` table — "Case queue, including child-deletion and parent-deletion-cancellation cases" (§3.3), with `SupportCaseRepository.getQueue()/getDetail()` (§6.5), a search entry point `GET /v1/admin/users/search?query=&type=support_case` (§3.4), and Screen Inventory #19–20 ("Support Case Queue"/"Support Case Detail"). The platform's master table catalog (`NoorHeroes_Consolidated_Blueprint_v6.md` §9.5) lists its schema as `support_cases | id, parent_id (FK), category, status, owner_id, created_at` — a thin, general-purpose case-tracking table with no message thread, no FAQ integration, no queue-priority concept, predating C.25.
- **C.25** (this feature) defines `support_ticket`/`ticket_message` with a specific category taxonomy (`billing|technical|content_concern|safety_concern|account_deletion_cancellation|general`), `queue_priority` (expedited/standard), and a full append-only message thread — purpose-built for the parent-facing Support Center, including the exact `account_deletion_cancellation` and `safety_concern` cases E.32's `support_cases` also claims to cover.

## Problem
Both tables claim ownership of the same real-world case type (deletion-cancellation and safety-concern cases originating from a parent). If both ship independently, admins get two differently-shaped "support queue" screens, agents may not know which one is authoritative for a given case, and a parent-initiated `account_deletion_cancellation` ticket (C.25) would have no relationship to whatever `support_cases` row (if any) E.32's tooling expects to see — defeating the "route through Support" guarantee both features individually depend on (C.25 FR-8, cross-referenced by E.32's own `DELETIONSVC` dependency, §3.3).

## Proposed Improvement
Treat **`support_ticket`/`ticket_message` (C.25) as the single system of record** for all parent-initiated support requests, including deletion-cancellation and safety-concern cases. `support_cases` is **not** implemented as a second, parallel table. Instead:
1. E.32's `GET /v1/admin/users/search?query=&type=support_case` resolves against `support_ticket`, not a separate `support_cases` table.
2. E.32's Screen #19–20 ("Support Case Queue"/"Support Case Detail") and its `SupportCaseRepository.getQueue()/getDetail()` become an admin **view** scoped to `support_ticket` rows where `category IN ('account_deletion_cancellation', 'safety_concern')` — i.e., E.32's screens surface the safety/deletion-relevant subset of the same underlying data N-02 (this feature's Support Ticket Queue & Case Management) manages more generally. Whether E.32 ends up as a filtered variant of N-02's own console, or a thin cross-reference into it, is an E.32-side implementation decision to make when E.32's own blueprints are generated — it is out of scope for this note to redesign E.32's screens, but it must **not** stand up a second, divergent `support_cases` table to do so.
3. `support_cases.owner_id` (case-assignment) is the one genuinely useful capability C.25's original `support_ticket` schema lacked. This gap is closed by adding `assigned_admin_id` directly to `support_ticket` (see the accompanying edit to `B-04`), rather than carrying it on a separate table.

## Impact
- **C.25 (B-04, N-02):** `support_ticket` gains one new nullable column, `assigned_admin_id` (FK to the admin/operator identity, per E.28's Role Registry). No other change to B-04's already-generated contract. N-02's admin console gains an "Assign to me / Assign to agent" action, a natural admin-console capability that was implicitly expected via `support_cases.owner_id` but never surfaced in N-02's original scope.
- **E.32 (not yet generated as blueprints):** When E.32's own blueprints are written, its Support Case Queue/Detail sub-features must be scoped against `support_ticket`, not a new `support_cases` table. This note should be read alongside E.32's PRD before that generation happens — flag it to whoever runs `Generate:` on E.32's Support Case Queue sub-feature.
- **No impact** to B-01, B-02, B-03, K-01 through K-04, or N-01 — this reconciliation is scoped entirely to the ticket/case admin surface.

## Implementation
1. `B-04` (`Backend/04-support-ticket-lifecycle-escalation-api.md`) is amended in place to add `assigned_admin_id` to the `support_ticket` schema (see that file's updated §10/§14).
2. `B-06` (`Backend/06-admin-support-ticket-queue-case-management-api.md`, generated alongside this note) implements the admin-side assignment mutation (`PATCH .../assign`) and explicitly documents that it is the intended backing service for E.32's eventual Support Case Queue screens for the deletion/safety-concern subset of cases.
3. `N-02` (`NextJS_Admin/02-support-ticket-queue-case-management.md`) is amended to reference this note instead of leaving the overlap as an open flag, and to add the assignment control to its scope.

## Documentation Update
This note is the durable record of the decision. E.32's own PRD document is **not** edited by this note (out of scope — PRD documents are source-of-truth inputs, not blueprint outputs), but any future `Generate:` pass on E.32's Support Case Queue sub-feature must read this note first and scope its blueprint against `support_ticket`, not reintroduce `support_cases` as a separate table.
