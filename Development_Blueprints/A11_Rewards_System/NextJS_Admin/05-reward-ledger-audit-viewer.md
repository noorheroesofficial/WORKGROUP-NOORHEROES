# N-05 — Reward Ledger Audit Viewer (Read-Only)

> **⚠ DEPRECATED — superseded by `E31_Engagement_Tools_Admin_Suite/NextJS_Admin/04-reward-ledger-manual-grant-ui.md`.** Backend counterpart's ledger-audit portion is likewise deprecated in favor of E.31 B-04 (see `13-admin-reward-ledger-audit-reconciliation-viewer-api.md`'s deprecation note, and its extracted replacement `14-admin-reconciliation-incident-log-api.md` for the surviving reconciliation-log surface). Do not implement this file — implement E.31's Reward Ledger & Manual Grant UI instead. Retained for historical/design-rationale reference only.

## 1. Feature Context
Part of Feature A.11 — Rewards System. Strictly read-only support/dispute-resolution surface over the append-only reward ledger.

## 2. Parent Feature
A.11 Rewards System — NextJS Admin

## 3. Sub-feature
N-05 Reward Ledger Audit Viewer (Read-Only)

## 4. Objective
Build the read-only Ledger Audit Viewer page consuming B-13, restricted to `support`/`trust_safety`, per PRD §8/§9/§12.5.

## 5. Business Requirements
- Search-by-masked-identifier table of `reward_ledger` entries for support/dispute investigation.
- No edit or delete controls exist anywhere on this page, matching the backend's database-level permission lockout.
- Restricted to `support`/`trust_safety` role.

## 6. Existing Architecture
Existing Admin Portal shell; reuses `DataTable`, `FilterPanel`, `SearchBar`, `RequirePermission`.

## 7. Existing Code to Reuse
- `DataTable`, `FilterPanel`, `SearchBar`, `RequirePermission`, `LoadingState`, `EmptyState`, `ErrorView`.
- `BaseResourceClient` (read-only subset — this client implements only `list()`/`get()`, no mutating methods at all).

## 8. Files to Create
- `src/features/rewards/ledger-audit/LedgerAuditResourceClient.ts` (read-only client, no create/update/delete methods defined)
- `src/features/rewards/ledger-audit/LedgerAuditViewerPage.tsx`
- `src/features/rewards/ledger-audit/__tests__/LedgerAuditViewerPage.test.tsx`

## 9. Files to Modify
- Admin route registry — `/rewards/ledger-audit`.
- Admin nav/sidebar config.

## 10. Backend Requirements
Consumes B-13 (`GET /v1/admin/rewards/ledger`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- `LedgerAuditResourceClient` is implemented with **only** `list()` — the class/module contains no `create`/`update`/`delete` method definitions at all, not merely unused UI buttons for them.
- Filter by date range, `reason_type`, masked identifier via `FilterPanel`/`SearchBar`.
- No row-level action menu exists on this page.

## 13. API Contract
`GET /v1/admin/rewards/ledger` (B-13).

## 14. Database Requirements
N/A (admin frontend).

## 15. Validation
UI test scanning the rendered page for any edit/delete/save control — assert zero exist, for any role, including high-privilege ones (mirrors B-13's backend no-write-route guarantee).

## 16. Authentication
Reuses existing Admin session/auth flow.

## 17. Authorization
`RequirePermission` gate for `support`/`trust_safety`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| No matching results | `EmptyState` with "no entries match your filters" |
| Fetch failure | `ErrorView` with retry |
| Insufficient permission | Permission-denied state |

## 19. Offline First
Not applicable (admin web).

## 20. Local Data
Not applicable.

## 21. Localization
Admin UI localized (labels, filter controls); ledger entry `reason_type`/`reason_id` values displayed as their stable keys or resolved to an admin-facing label via a lookup table, not translated as if child-facing.

## 22. RTL
Table/filter layout mirrors correctly for Arabic admin locale.

## 23. Analytics
N/A directly; viewing full (unmasked) detail is itself logged server-side per B-13 §10.

## 24. Performance
`DataTable` pagination against B-13's indexed query paths.

## 25. Security
Read-only-by-design at the client layer (no mutating methods exist in the resource client at all) mirrors the backend's read-only route design — a defense-in-depth pairing.

## 26. Library Requirements
Existing Admin Portal stack.

## 27. Testing
- Unit: filter/search param construction.
- Integration: search/list flow, permission-gated rendering, no-write-control UI test (mandatory).

## 28. Documentation
Component README stating this page is read-only by design, with no corresponding write capability anywhere in the backend for this resource, cross-referenced against B-13.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Read-Only `LedgerAuditResourceClient`**
- Files to Create: `LedgerAuditResourceClient.ts`
- Do Not Change: never add a create/update/delete method to this client.
- Definition of Done: only `list()` exists.

**Task 02 — Build `LedgerAuditViewerPage`**
- Files to Create: `LedgerAuditViewerPage.tsx`
- Existing Files to Reuse: `DataTable`, `FilterPanel`, `SearchBar`, `RequirePermission`.
- Tests: no-write-control UI test (mandatory).
- Definition of Done: test passing.

**Task 03 — Wire Route, Nav, and Permission Gate**
- Files to Modify: route registry, nav config.
- Definition of Done: `/rewards/ledger-audit` reachable only to `support`/`trust_safety`.

**Task 04 — Documentation & Final Review**
- Documentation: README per §28.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Ledger Audit Viewer live, verifiably read-only at both client and backend layers, RBAC-gated.

## 31. Final Verification Checklist
- [ ] No write/edit/delete control exists anywhere on this page
- [ ] `LedgerAuditResourceClient` contains no mutating method definitions
- [ ] Search/filter by masked identifier, date range, `reason_type` functional
- [ ] `RequirePermission` restricts to `support`/`trust_safety`
- [ ] Localization and RTL verified
