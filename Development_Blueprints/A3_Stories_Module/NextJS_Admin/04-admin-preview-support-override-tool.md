# N-04 — Admin Preview & Support Override Tool

## 1. Feature Context
Support/content-review staff's tool to preview locked content for troubleshooting, with a persistent, non-dismissible banner stating the reward-isolation guarantee B-13/B-04 enforce server-side, plus a read-only audit log of every preview session ever issued.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
3.4 Admin Preview & Support Override Tool (ID: **N-04**)

## 4. Objective
Build a search-by-content-id form issuing a preview session against B-13, with a persistent non-dismissible reassurance banner and a read-only audit-log table beneath it.

## 5. Business Requirements
- §8: issues the `is_preview=true` token; every use audited; cannot be used to grant rewards (enforced server-side, surfaced here as a read-only confirmation banner).
- §9: persistent, non-dismissible banner: "Preview sessions never grant XP, Noor Heroes Points, or badges to the real child account — this is enforced server-side." Below the banner, read-only audit log (admin_id, content_id, timestamp).

## 6. Existing Architecture
`src/features/preview-tool/` module.

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/data-table.tsx::DataTable` (for the audit log)
- `src/shared/api/base-resource-client.ts::BaseResourceClient`

## 8. Files to Create
- `src/app/(dashboard)/stories/preview-tool/page.tsx`
- `src/features/preview-tool/api/preview-tool-repository.ts`
- `src/features/preview-tool/hooks/use-issue-preview-session.ts`, `use-preview-audit-log.ts`
- `src/features/preview-tool/components/reward-isolation-banner.tsx` — persistent, non-dismissible
- `src/features/preview-tool/components/preview-audit-log-table.tsx`
- `src/features/preview-tool/types/preview-session.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `PREVIEW_TOOL.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item gated by `support` or `content_review`

## 10. NextJS Requirements
- `RewardIsolationBanner`: renders at the top of the page with zero dismiss/close affordance in its component API at all (no `onDismiss` prop exists — this is a structural, not just a default-props, guarantee).
- Search-by-content-id form calls `POST /admin/v1/preview-session` on submit; on success, surfaces the returned preview token/session details (not the raw token value itself if it's sensitive — display only non-sensitive session metadata, confirm exact response shape against B-13 before finalizing what's shown).
- `PreviewAuditLogTable`: read-only `DataTable` of all preview sessions (admin_id, content_id, timestamp) — no row-level actions, no mutation columns.

## 11. Required API
**Admin API** — B-13: `POST /v1/admin/preview-session` (issuance also serves as the audit-log write; if a separate audit-log read endpoint doesn't exist yet, confirm with backend whether B-13's audit log is queryable via `AdminRouter`'s existing `GET /v1/admin/audit-logs` filtered by action type, rather than assuming a bespoke endpoint — reuse the existing admin audit-log read path if it already covers this).

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="support"` OR `permission="content_review"` gating the page.

## 13. Loading / Empty / Error States
Form-submission loading state; audit-log loading skeleton and empty state ("No preview sessions issued yet"); error state distinct for issuance failure vs. audit-log load failure.

## 14. Responsive UI / Accessibility
Banner text remains fully legible/readable by screen readers as page-level content (not an easily-dismissed toast pattern); audit log table responsive per existing `DataTable` conventions.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
- The banner's non-dismissible, always-visible nature is itself a security/trust communication requirement from the PRD — the final code review must confirm no dismiss mechanism was accidentally introduced (e.g., via a generic reusable "Banner" component that happens to support dismissal by default).
- `support`/`content_review` RBAC enforced via `RequirePermission`.

## 17. Testing
Unit: banner has no dismiss affordance (component-API-level assertion, not just "not rendered by default"); form disabled during submission (prevent double-issuance). Integration: issuance flow populates the audit log table with the new session immediately (refetch or optimistic insert).

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `preview-session.ts` schema for request/response and audit-log rows. Files: `types/preview-session.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `PreviewToolRepositoryImpl`**
Objective: Repository for issuance + audit-log read (confirming and reusing the existing `admin/v1/audit-logs` path if applicable per §11). Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `RewardIsolationBanner`**
Objective: Persistent banner with no dismiss prop in its component API. Tests: **mandatory structural test** asserting the component's prop interface has no `onDismiss`/`onClose`-shaped prop. Definition of Done: test passes.

**Task 04 — Implement `useIssuePreviewSession`/`usePreviewAuditLog` Hooks**
Objective: React Query hooks for issuance (mutation) and audit-log (query). Dependencies: Task 02. Tests: covered by Task 06. Definition of Done: hooks wired correctly.

**Task 05 — Implement `PreviewAuditLogTable`**
Objective: Read-only `DataTable` of audit rows, zero row-level actions. Dependencies: Task 04. Tests: no-row-actions assertion. Definition of Done: test passes.

**Task 06 — Implement the Page**
Objective: Compose `RequirePermission` + banner + search form + audit log table + states. Dependencies: Tasks 03–05. Tests: full-page smoke test, issuance-populates-log integration test. Definition of Done: tests pass.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm the banner genuinely cannot be dismissed under any prop configuration; confirm the audit log has zero mutation affordances. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Banner is persistently visible with no dismiss/close mechanism anywhere in its component API
- [ ] Banner text matches the PRD's exact reassurance copy
- [ ] Preview-session issuance form disabled during submission (no double-issuance)
- [ ] Audit log table is strictly read-only, zero row-level mutation actions
- [ ] Issuing a session correctly and promptly populates the audit log view
- [ ] `support`/`content_review` RBAC enforced via `RequirePermission`

## 20. Definition of Done
Support/content-review staff can issue audited preview sessions through a tool that structurally cannot hide or dismiss the reward-isolation guarantee, with a fully read-only audit trail mirroring B-13's backend guarantees.
