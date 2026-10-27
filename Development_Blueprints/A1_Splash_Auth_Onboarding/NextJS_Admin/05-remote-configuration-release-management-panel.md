# N-05 — Remote Configuration & Release Management Panel

## 1. Feature Context
Admin-facing write surface for `min_supported_version`, `recommended_version`, `maintenance_mode`, and the two-admin-approval `consent_version` workflow — the UI counterpart to B-09.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
3.5 Remote Configuration & Release Management Panel (ID: **N-05**)

## 4. Objective
Build a form for direct config updates plus a distinct propose/approve workflow panel for `consent_version`, with the Approve action disabled/hidden when the current admin is the proposer, against B-09.

## 5. Business Requirements
- Remote Config panel: update `min_supported_version`, `recommended_version`, `maintenance_mode`; `consent_version` requires a second admin's approval via a two-step propose→pending→approve/reject workflow.
- CRUD permissions: Create/Update only, no delete.
- Every config change writes an immutable audit_log row — this page should surface recent change history for transparency, not just the current state.

## 6. Existing Architecture
`src/features/remote-config/` module; `SettingsRepositoryImpl`/`useSettings()`/`useUpdateSettings()` pattern (closest existing analog per the architecture doc's Quick Reference table) — model `RemoteConfigRepositoryImpl` directly on that existing pattern rather than inventing a new one.

## 7. Existing Code to Reuse
- Existing `SettingsRepositoryImpl.getSettings()`/`.updateSettings()` pattern (structural template, not the same resource)
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/confirmation-dialog.tsx::ConfirmationDialog` (for the Approve action, given its legal weight)
- `useAdminSession()` (to compare current admin_id against `proposed_by_admin_id`)

## 8. Files to Create
- `src/app/(dashboard)/remote-config/page.tsx`
- `src/features/remote-config/api/remote-config-repository.ts` — `RemoteConfigRepositoryImpl.get()/.update()/.proposeConsentVersion()/.approveConsentVersion()`
- `src/features/remote-config/hooks/use-remote-config.ts`, `use-update-remote-config.ts`, `use-consent-version-proposal.ts`
- `src/features/remote-config/components/version-gate-form.tsx` — min/recommended version + maintenance toggle form
- `src/features/remote-config/components/consent-version-approval-panel.tsx` — propose/pending/approve UI
- `src/features/remote-config/components/config-change-history.tsx` — recent audit-log-derived change list
- `src/features/remote-config/types/remote-config.ts` — Zod schemas

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `REMOTE_CONFIG.BASE`, `REMOTE_CONFIG.CONSENT_PROPOSE`, `REMOTE_CONFIG.CONSENT_APPROVE`
- `src/shared/components/dashboard-shell.tsx` — nav item gated by `admin:write`-equivalent permission

## 10. NextJS Requirements
- `VersionGateForm`: semver-validated text inputs (client-side validation mirroring B-09's server-side semver check, both required — server is the authority, client validation is UX), maintenance-mode toggle; submits via `useUpdateRemoteConfig()` mutation, direct effect (no approval needed for these fields).
- `ConsentVersionApprovalPanel`: shows the current active `consent_version`, any `pending` proposal (with proposer identity and timestamp), a "Propose New Version" form, and an "Approve"/"Reject" action pair.
- Approve action must be **disabled** (not just hidden — disabled-with-explanatory-tooltip is more informative for an admin who might wonder why) when `pendingProposal.proposedByAdminId === currentAdmin.adminId`, mirroring B-09's server-side self-approval rejection defensively on the client too.
- `ConfigChangeHistory`: **resolved architecture decision:** `FAST-API-INSTRUCTIONS.md` §6 confirms `GET /v1/admin/audit-logs` already exists (`admin:read` scope, "Queries paginated audit logs") — this component reuses that existing endpoint directly rather than needing a new B-09-specific one. The documented endpoint doesn't show a `resource_type`/`action`-filter query parameter, so this sub-feature's backend coordination point (not a blocker, a small additive extension) is: confirm whether `GET /v1/admin/audit-logs` already accepts a filter param; if not, add one (e.g., `?resource_type=remote_config`) as a minor, backward-compatible extension of that existing endpoint rather than building a parallel audit-read path. If filtering server-side isn't available in time, fall back to client-side filtering of the unfiltered recent-logs response by `action`/`resource_type` fields already present in each `AdminAuditLog` row (per B-08's confirmed usage of the same underlying table) — either approach is now unblocked.

## 11. Required API
- `GET /admin/v1/config/remote-config` (B-09)
- `PUT /admin/v1/config/remote-config` (B-09)
- `POST /admin/v1/config/consent-version/propose` (B-09)
- `POST /admin/v1/config/consent-version/{proposal_id}/approve` (B-09)

## 12. Validation
Client-side semver format validation on version fields (mirrors server-side, both layers required); Approve button disabled for self-proposals (mirrors server-side `409` rejection).

## 13. Authentication / Authorization
`RequirePermission` for the `admin:write`-equivalent scope; identity comparison for self-approval prevention uses `useAdminSession()`'s `admin.adminId`.

## 14. Loading / Empty / Error States
Loading on initial config fetch; no meaningful "empty" state (config always has exactly one active row per B-01/B-09's singleton design) but a "no pending proposal" state for the approval panel is a normal, expected state, not empty/error.

## 15. Responsive UI / Accessibility
Form fields properly labeled; disabled Approve button has an accessible explanation (`aria-describedby` or visible helper text), not just a silently-disabled control.

## 16. Localization / RTL
Standard `useTranslation()`/`useFormatters()`; version-history timestamps locale-formatted.

## 17. Security
This page controls production version-gating and the legally-significant consent-version pointer — the highest-consequence write surface in this entire admin feature set. Self-approval prevention is defense-in-depth (client convenience) atop the server's actual enforcement (B-09) — never treat the client-side check as sufficient on its own, and the code/tests must make this dependency explicit.

## 18. Testing
Unit: semver client-side validation; self-approval-disables-Approve-button assertion (tested both for the proposer and for a different admin); direct-update success/error handling; propose→approve full-flow integration test against a mocked API.

## 19. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schemas & Add API Endpoints**
Objective: Contracts for get/update/propose/approve. Files to Create/Modify: `types/remote-config.ts`, `api-endpoints.ts`. Tests: schema validation for all four shapes. Definition of Done: typed, validated contracts.

**Task 02 — Implement `RemoteConfigRepositoryImpl`**
Objective: All four repository methods. Follow: `SettingsRepositoryImpl`-equivalent structural pattern. Tests: mocked-fetch tests for each method. Dependencies: Task 01. Definition of Done: all four methods typed and tested.

**Task 03 — Implement Query/Mutation Hooks**
Objective: `useRemoteConfig()`, `useUpdateRemoteConfig()`, `useConsentVersionProposal()` (combining propose+approve mutations with appropriate query invalidation). Follow: `useSettings()`/`useUpdateSettings()`-equivalent pattern. Tests: invalidation-on-success tests. Dependencies: Task 02. Definition of Done: config view refreshes correctly after any successful mutation.

**Task 04 — Implement `VersionGateForm`**
Objective: Semver-validated direct-update form. Follow: existing form conventions, client-side semver validation. Tests: malformed-version-blocks-submit test. Dependencies: Task 03. Definition of Done: form never submits an invalid semver string.

**Task 05 — Implement `ConsentVersionApprovalPanel`**
Objective: Current version display, pending-proposal display, propose form, disabled-on-self-proposal Approve/Reject actions. Follow: `ConfirmationDialog` for Approve/Reject given legal weight. Tests: self-approval-disable test (both proposer and non-proposer admin scenarios), full propose→approve flow test. Dependencies: Task 03. Definition of Done: Approve button is provably unclickable (disabled, not just visually de-emphasized) for the proposing admin.

**Task 06 — Implement `ConfigChangeHistory` Against the Existing `GET /v1/admin/audit-logs` Endpoint**
Objective: Recent-changes list reusing the confirmed-existing admin audit-log endpoint (§10) rather than a new one. Follow: existing list/table conventions, `admin:read` scope (already covered by the page's broader `admin:write`-equivalent gate, so no separate permission check needed for reading). Implementation: request with a `resource_type=remote_config` filter param if the backend coordination in §10 confirms server-side filtering is available; otherwise fetch the general recent-logs page and filter client-side on `action`/`resource_type`. Definition of Done: history list renders real recent remote-config changes (direct updates, proposals, approvals, rejections) sourced from the existing audit-log table — no fabricated or placeholder endpoint.

**Task 07 — Implement the Page**
Objective: Compose `RequirePermission` + `VersionGateForm` + `ConsentVersionApprovalPanel` + `ConfigChangeHistory`. Files to Create: `page.tsx`. Dependencies: Tasks 04–06. Definition of Done: full page smoke test against a mocked API.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §18. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm self-approval prevention is explicitly documented as client-side-convenience-only (server is the real authority), confirm no version-gate field submits without valid semver, confirm the change-history dependency was resolved or explicitly flagged. Definition of Done: checklist in §20 checked.

## 20. Final Verification Checklist
- [ ] Version fields validated as semver client-side before submission (server remains the authority)
- [ ] Approve button disabled (not just hidden) for the proposing admin, verified for both the proposer and a different admin
- [ ] Maintenance-mode toggle and version updates apply immediately, without an approval step
- [ ] `consent_version` is never directly editable outside the propose/approve workflow
- [ ] Change-history reuses the confirmed-existing `GET /v1/admin/audit-logs` endpoint (no longer an open dependency)
- [ ] Page gated behind the correct write-level admin permission

## 21. Definition of Done
The Remote Configuration & Release Management Panel is live, reads/writes against B-09, enforces client-side self-approval prevention as a defense-in-depth layer atop the server's actual enforcement, and gives admins full visibility into current config and pending consent-version proposals — closing out the full A.1 sub-feature set (B-01 through N-05).
