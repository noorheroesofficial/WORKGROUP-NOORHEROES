# N-03 — Per-Plan Default Download Cap Configuration

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). The write-enabled admin settings form for configuring the fallback per-plan default download cap consumed by B-03 whenever a parent hasn't set a custom cap.

## 2. Parent Feature
B.15 — Offline Downloads & Sync

## 3. Sub-feature
N-03 — Per-Plan Default Download Cap Configuration

## 4. Objective
Build a settings form mapping subscription plan codes to default per-child download caps, restricted to `product_admin`, with clear UI messaging that changes affect only future defaults and never retroactively override a parent's already-configured custom cap, plus optimistic-lock conflict handling.

## 5. Business Requirements
- §8 Admin Requirements: Per-Plan Default Download Cap Configuration — admin-tunable default caps per subscription tier, Update-only behind `product_admin`.
- §9 Admin AI Prompt item 3: changes affect only future defaults, never retroactively altering a parent's already-configured custom cap.
- §12.5 Admin Security: cap-default changes don't retroactively override parent settings.

## 6. Existing Architecture
New settings page under `src/features/downloads/`, reusing the platform's existing Admin Settings form pattern (`SettingsRepositoryImpl`, `useUpdateSettings()` precedent per `NEXT-JS-INSTRUCTIONS.md` §5/§9) rather than a bespoke form implementation.

## 7. Existing Code to Reuse
- `RequirePermission`, `ConfirmationDialog`, `DataTable` (for the editable plan-cap list), `LoadingState`/`EmptyState`/`ErrorView`.
- `apiClient.get()`/`apiClient.patch()` (or `.put()`) pattern per `NEXT-JS-INSTRUCTIONS.md` §6.
- `hasPermission(admin, permission)` for `product_admin`-only gating.
- Existing form/validation conventions (whatever form library the platform's other admin settings forms already use, per §5's `SettingsRepositoryImpl` precedent).
- Existing `AdminAuditLog` viewer pattern (if one exists in the admin portal) for linking to the change history after a save.

## 8. Files to Create
- `src/features/downloads/api/download-cap-config-repository.ts`.
- `src/features/downloads/hooks/use-default-cap-config.ts`, `use-update-default-cap-config.ts`.
- `src/features/downloads/types/default-cap-config.types.ts` (Zod schema matching B-08 §13's request/response shapes, including `version` for optimistic locking).
- `src/features/downloads/components/default-cap-config-form.tsx`.
- `src/features/downloads/components/default-cap-config-table.tsx`.
- `src/app/(dashboard)/downloads/default-cap-config/page.tsx`.
- `src/features/downloads/__tests__/use-update-default-cap-config.test.ts`.

## 9. Files to Modify
- Sidebar navigation config — add "Default Download Caps" entry under the Downloads section, gated by `RequirePermission` for `product_admin`.

## 10. Backend Requirements
Consumes B-08: `GET`/`PUT /v1/admin/downloads/default-caps`.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- `useDefaultCapConfig()` fetches current plan-code → cap mappings (`admin:read`-gated read).
- `DefaultCapConfigTable` (`DataTable`) lists each plan code with its current cap (formatted human-readably, e.g., "3 GB"), an inline edit affordance.
- `DefaultCapConfigForm`: per-row edit with validation (non-negative, sane bounds); submits via `useUpdateDefaultCapConfig()` → `PUT`, including the row's current `version` for optimistic-lock enforcement.
- Explicit, persistent UI copy near the form: "Changes here set the default for new/unconfigured families on this plan only — they never override a parent's existing custom download limit."
- `ConfirmationDialog` before a save, given this is a state-mutating action affecting (at minimum) future default resolution platform-wide for the plan.
- On `409` (stale `version` — a concurrent admin edit occurred), surface a clear "this value was changed by someone else, please refresh and retry" error — never silently overwrite.
- Success toast confirming the new default, with a link to the relevant `AdminAuditLog` entry if the platform's existing audit-log viewer supports deep-linking to a specific entry.
- RBAC: form fields/save action disabled (or the whole page inaccessible) for any role without `product_admin`; a `product_admin`-only role check, not the broader `content_editor`/`trust_safety` scopes used by N-01/N-02.

## 13. API Contract
`GET /v1/admin/downloads/default-caps` → `{ caps: [{ plan_code, cap_bytes, version }] }`.
`PUT /v1/admin/downloads/default-caps` → request `{ updates: [{ plan_code, cap_bytes, version }] }`, response same shape as `GET`, per B-08 §13.
**Error Responses:** `409` (stale version), `422` (invalid `cap_bytes`/unknown `plan_code`), `403` (missing `admin:write`).

## 14. Database Requirements
N/A (frontend consumes API only).

## 15. Validation
`cap_bytes` input validated client-side as non-negative and within a sane bound (mirroring B-08's server-side validation) before submission — a UX guard; the server remains authoritative.

## 16. Authentication
Standard admin session via `apiClient`.

## 17. Authorization
`RequirePermission` for `product_admin` specifically (stricter than N-01/N-02's `product_admin`/`trust_safety` either-or gating) on the mutating action; read access may use the broader `admin:read` scope consistent with B-08's own read/write scope split.

## 18. Error Handling
- `409` stale-version conflict: clear, actionable "refresh and retry" messaging, never a silent overwrite or a generic error toast.
- `422` validation failure: inline field-level error, not a full-page error state.
- Network/server failure: standard `QueryErrorState` with retry.

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Form labels, validation messages, the non-retroactive-override explanatory copy, and success/error toasts all localized via `useTranslation`; cap values formatted via `useFormatters` (e.g., locale-appropriate byte/GB formatting).

## 22. RTL
Standard RTL support for the form and table via existing layout conventions.

## 23. Analytics
No dedicated client event beyond standard admin-page-view tracking, if the platform has one; the authoritative change record is the backend's `AdminAuditLog` entry (B-08), not a client-side analytics event.

## 24. Performance
Small, low-cardinality dataset (one row per subscription plan) — no special performance considerations; standard React Query caching on the read hook.

## 25. Security
- `product_admin`-only gating on the mutating action, stricter than the two read-only monitors.
- Optimistic-lock (`version`) enforcement surfaced clearly in the UI, preventing accidental silent overwrites by two admins editing concurrently.
- The non-retroactive-override guarantee is a backend-structural fact (B-03's read-order); this UI's role is to communicate it clearly, not to enforce it — enforcement lives in B-03/B-08.

## 26. Library Requirements
Existing stack: Next.js, TanStack Query, Zod, existing form library per the platform's other admin settings forms.

## 27. Testing
- Hook test: correct parsing of the cap-config response, including `version`.
- Component test: form validation rejects negative/out-of-bound `cap_bytes` values inline.
- Component test: `409` response renders the stale-version-conflict messaging, not a generic error or a silent overwrite.
- RBAC test: save action disabled/hidden for a role without `product_admin`.
- Component test: the non-retroactive-override explanatory copy is present and visible near the form.

## 28. Documentation
TSDoc noting the `version` field is mandatory on every update entry and why (optimistic-lock enforcement), cross-referenced to B-08 §5.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Define Types**
Files to create: `default-cap-config.types.ts`.

**Task 02 — Implement Repository & Hooks**
Files to create: `download-cap-config-repository.ts`, `use-default-cap-config.ts`, `use-update-default-cap-config.ts`.

**Task 03 — Build DefaultCapConfigTable**
Files to create: `default-cap-config-table.tsx`.

**Task 04 — Build DefaultCapConfigForm with Validation**
Files to create: `default-cap-config-form.tsx`.

**Task 05 — Implement Optimistic-Lock Conflict Handling**
Objective: clear `409` messaging, no silent overwrite.

**Task 06 — Assemble Page, Wire RBAC (product_admin-only) + Navigation**
Files to create: `page.tsx`; files to modify: sidebar config.

**Task 07 — Add Tests**

**Task 08 — Final Review**
Objective: confirm the non-retroactive-override explanatory copy is present and RBAC is `product_admin`-only on the mutating action (stricter than the two read-only dashboards).

## 30. Definition of Done
- Form live, `product_admin`-gated, correctly reading and updating plan-cap defaults.
- Optimistic-lock conflicts surfaced clearly, never silently overwritten.
- Non-retroactive-override guarantee clearly communicated in the UI.

## 31. Final Verification Checklist
- [ ] Save action restricted to `product_admin` specifically.
- [ ] Stale-version conflicts (`409`) surfaced clearly, never silently overwritten.
- [ ] Client-side validation mirrors server-side bounds on `cap_bytes`.
- [ ] Non-retroactive-override explanatory copy visible near the form.
- [ ] Success confirmation links to the audit-log entry where supported.
- [ ] Localization and RTL verified.
