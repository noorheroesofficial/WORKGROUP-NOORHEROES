# N-05 — Withdrawn Content Manager

## 1. Feature Context
The final admin surface: a searchable content table with a "Withdraw" action (never "Delete") requiring a reason field, and a future-ready "Restore" action on already-withdrawn rows — mirroring B-14's soft-only, reason-required, always-visible backend guarantee.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
3.5 Withdrawn Content Manager (ID: **N-05**)

## 4. Objective
Build a searchable content table against B-14, with a required-reason "Withdraw" action and a "Restore" action, status pills, and zero delete-shaped affordance anywhere in the module.

## 5. Business Requirements
- §8: mark `is_withdrawn=true` (never hard-delete), required reason field, immediate cache/CDN invalidation trigger (server-side, this UI just triggers it via the API call).
- §9: searchable table, "Withdraw" action (not "Delete") requiring a reason field; `PATCH /admin/v1/content/{id}` with `{ is_withdrawn: true, reason }`; withdrawn items show a status pill and remain visible for future "Restore" actions.
- CRUD permissions: Update-only (the `is_withdrawn` flag), behind `content_editor` or `trust_safety` role.

## 6. Existing Architecture
`src/features/withdrawn-content/` module, following the existing `DataTable`/`SearchBar`/`RequirePermission` pattern.

## 7. Existing Code to Reuse
- `src/shared/components/data-table.tsx::DataTable`
- `src/shared/components/search-bar.tsx::SearchBar`
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/status-badge.tsx::StatusBadge` (for the withdrawn/published status pill)
- `src/shared/components/confirmation-dialog.tsx::ConfirmationDialog`

## 8. Files to Create
- `src/app/(dashboard)/stories/withdrawn-content/page.tsx`
- `src/features/withdrawn-content/api/withdrawn-content-repository.ts`
- `src/features/withdrawn-content/hooks/use-content-search.ts`, `use-withdraw-content.ts`, `use-restore-content.ts`
- `src/features/withdrawn-content/components/withdraw-dialog.tsx` — reason field required before submission
- `src/features/withdrawn-content/components/content-status-table.tsx`
- `src/features/withdrawn-content/types/withdrawal.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `WITHDRAWN_CONTENT.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item gated by `content_editor` or `trust_safety`

## 10. NextJS Requirements
- `WithdrawDialog`: submit button disabled until `reason` is non-empty (Zod `.min(1)` on the field, enforced before the `PATCH` call fires at all).
- `ContentStatusTable`: every row shows a `StatusBadge` (published/withdrawn); withdrawn rows never disappear from this table — they remain searchable/visible with a "Restore" action available in place of "Withdraw".
- No `DELETE`-verb call exists anywhere in `withdrawn-content-repository.ts` — the module is architecturally incapable of hard-deleting content, mirroring B-14.

## 11. Required API
**Admin API** — B-14: `PATCH /admin/v1/content/{id}` (`{ is_withdrawn, reason }`), `POST /admin/v1/content/{id}/restore` (or equivalent — confirm exact restore endpoint shape against B-14's blueprint, which specifies `POST /admin/v1/content/{id}/restore` explicitly).

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="content_editor"` OR `permission="trust_safety"` gating the page.

## 13. Loading / Empty / Error States
Table-loading skeleton; empty state for a search with zero matches; withdrawal-submission error state (e.g., reason-required validation surfaced inline, not just disabled-button — an explicit error message if somehow submitted without a reason).

## 14. Responsive UI / Accessibility
Table responsive per existing `DataTable` conventions; status pill conveyed with text label, not color alone; `WithdrawDialog`'s reason field has a clear, programmatically-associated label for screen readers.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
- `content_editor`/`trust_safety` RBAC enforced via `RequirePermission`.
- No delete capability exists anywhere in this module's UI or repository — architecturally mirrors B-14's backend guarantee, verified by an explicit negative test.

## 17. Testing
Unit: reason-required validation blocks submission (both UI-disabled-state and a defensive repository-level check); withdrawn rows remain visible/searchable, never filtered out of the table. Integration: withdraw → row shows withdrawn status pill immediately (optimistic or refetch) → restore → row reverts to published status pill.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `withdrawal.ts` with `reason: z.string().min(1)`. Files: `types/withdrawal.ts`, `api-endpoints.ts`. Tests: schema rejects empty reason. Definition of Done: test passes.

**Task 02 — Implement `WithdrawnContentRepositoryImpl`**
Objective: Repository for search, withdraw, restore — zero `delete()` method defined. Follow: existing repository conventions. Tests: mocked-fetch tests, reason-required defensive test. Dependencies: Task 01. Definition of Done: repository has zero delete-shaped method.

**Task 03 — Implement `useContentSearch`/`useWithdrawContent`/`useRestoreContent` Hooks**
Objective: React Query hooks (search query + two mutations). Dependencies: Task 02. Tests: covered by Task 06. Definition of Done: hooks wired correctly.

**Task 04 — Implement `WithdrawDialog` with Required Reason**
Objective: Submit disabled until reason is non-empty. Dependencies: Task 03. Tests: **mandatory validation test** — submit blocked with empty reason, enabled once populated. Definition of Done: test passes.

**Task 05 — Implement `ContentStatusTable`**
Objective: Search + status pill + Withdraw/Restore action per row, withdrawn rows always visible. Dependencies: Task 03–04. Tests: withdrawn-row-visibility test. Definition of Done: test passes.

**Task 06 — Implement the Page**
Objective: Compose `RequirePermission` + `SearchBar` + `ContentStatusTable` + `WithdrawDialog` + states. Dependencies: Task 05. Tests: full withdraw-then-restore integration test. Definition of Done: test passes.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm zero delete-shaped code path exists anywhere in the module; confirm withdrawn rows are provably never filtered out of the visible table. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Withdraw submission blocked until a non-empty reason is provided
- [ ] Withdrawn rows remain visible and searchable in the table, never disappear
- [ ] Status pill correctly reflects published/withdrawn state with a text label
- [ ] Restore action available on withdrawn rows, correctly reverts status
- [ ] Zero delete-shaped UI affordance or API call exists anywhere in this module
- [ ] `content_editor`/`trust_safety` RBAC enforced via `RequirePermission`

## 20. Definition of Done
Content editors and Trust & Safety can withdraw and restore content through a reason-required, always-visible, delete-free workflow that exactly mirrors B-14's backend guarantees — completing the full Stories Module admin surface (N-01 through N-05).
