# N-01 — Restriction Engine Configuration Defaults

## 1. Feature Context
Internal admins tune platform-wide default screen-time/bedtime suggestions (never enforced) and the AI-permission-default-by-age-band ceiling table that B-04 enforces against (PRD C.23 §8, §9).

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
3.1 Restriction Engine Configuration Defaults (ID: **N-01**)

## 4. Objective
Build a settings page for default screen-time/bedtime suggestions and the AI-permission ceiling table, requiring elevated (`ai_ops`-equivalent) session confirmation before ceiling-table changes commit, per the existing Admin Portal's `useElevatedSession()` high-risk-action pattern.

## 5. Business Requirements
- §8: Configuration Defaults = update-only behind `product_admin` role.
- §12.5: ceiling-table changes require `ai_ops` sign-off given platform-wide safety implications, mirroring the rigor applied to A.5's pronunciation-confidence-threshold configuration.
- Configuration Default changes write an immutable audit_log row.

## 6. Existing Architecture
Follows the Admin Portal's layered pattern: Component → Custom Hook → Repository (`BaseResourceClient` or custom) → `apiClient` → Backend REST API (B-07). High-risk ceiling-table changes reuse `useElevatedSession()` exactly as `DeleteFamilyButton` does for family deletion (per NEXT-JS-INSTRUCTIONS.md §15 example).

## 7. Existing Code to Reuse
- `RequirePermission` (RBAC guard component)
- `useElevatedSession()` (elevation for high-risk ceiling-table changes)
- `ConfirmationDialog` (danger-styled confirmation before ceiling-table submit)
- `apiClient`, `BaseResourceClient` pattern (or a custom repository if the shape doesn't fit standard CRUD)
- `useTranslation()`, `useFormatters()`
- `MoneyField`/form input patterns (for numeric minute inputs, adapted — not literally `MoneyField`, but the same controlled-input pattern)

## 8. Files to Create
- `src/features/restriction-engine/api/restriction-defaults.repository.ts`
- `src/features/restriction-engine/api/schemas.ts` (Zod schemas for defaults + ceiling table)
- `src/features/restriction-engine/hooks/use-restriction-defaults.ts`
- `src/features/restriction-engine/hooks/use-update-restriction-defaults.ts`
- `src/features/restriction-engine/hooks/use-ai-ceiling-table.ts`
- `src/features/restriction-engine/hooks/use-update-ai-ceiling-table.ts`
- `src/features/restriction-engine/components/restriction-defaults-form.tsx`
- `src/features/restriction-engine/components/ai-ceiling-table-editor.tsx`
- `src/app/(dashboard)/restriction-engine/defaults/page.tsx`
- `src/features/restriction-engine/__tests__/restriction-defaults-form.test.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `RESTRICTION_ENGINE.DEFAULTS`, `RESTRICTION_ENGINE.AI_CEILING`
- Sidebar navigation config — add "Restriction Engine" entry under Controls/Trust & Safety section, gated by `RequirePermission`

## 10. NextJS Requirements
- `restriction-defaults.repository.ts`: `getDefaults(signal)`, `updateDefaults(input)`, `getAiCeilingTable(signal)`, `updateAiCeilingTable(input, elevatedToken)` — the ceiling-update method requires an `elevatedToken` parameter, consistent with `useDeleteFamily`'s pattern.
- `RestrictionDefaultsForm`: standard form (React Hook Form + Zod), simple numeric/time inputs for suggested daily limit/bedtime, protected by `RequirePermission permission="restriction_engine:defaults:write"` (confirm exact permission string against the platform's actual `AdminPermission` enum before inventing one).
- `AiCeilingTableEditor`: a per-age-band row editor (table or repeated form section) for `ai_enabled_default`, `voice_interaction_default`, `curated_only_default`; submit flow requires `requestElevation(otp)` first (via `useElevatedSession()`), then calls `updateAiCeilingTable(input, elevatedToken)`, wrapped in a `ConfirmationDialog isDanger` given its platform-wide safety implications.
- Loading/saving/error states for both forms via `LoadingState`/`QueryErrorState`.

## 11. API Contract
### Required API (consumed)
- **HTTP Method:** GET/PATCH — **Endpoint:** `/v1/admin/restrictions/defaults` (B-07)
- **HTTP Method:** GET/PATCH — **Endpoint:** `/v1/admin/restrictions/ai-ceiling` (B-07, PATCH requires dual `product_admin`+`ai_ops` scope)
- **Authentication:** Bearer (admin), elevated token on ceiling PATCH

## 12. Database Requirements
N/A (frontend; backed by B-07's tables).

## 13. Validation
- Zod schemas mirror B-07's server-side validation (non-negative minutes, valid time strings, boolean fields for ceiling table) — client validation is a UX affordance, server remains authoritative.

## 14. Authentication
Standard admin session (`useAdminSession()`) for read; elevated session (`useElevatedSession()`) required specifically for the ceiling-table write.

## 15. Authorization
`RequirePermission` guards on both the page and the ceiling-table edit action specifically (distinct, more restrictive permission than the general defaults-write permission, reflecting the dual-scope backend requirement).

## 16. Error Handling
| Scenario | UI Behavior |
|---|---|
| Ceiling update without valid elevation | `requestElevation` fails, error shown before mutation ever fires |
| Server rejects due to missing `ai_ops` scope | `QueryErrorState` with clear message |
| Load failure | `QueryErrorState` with retry |
| Validation failure | Inline form field errors |

## 17. Offline First
N/A (admin web app, always-online assumption).

## 18. Local Data
N/A.

## 19. Localization
All labels/help text via `useTranslation()`; numeric formatting via `useFormatters()`.

## 20. RTL
Form and table layouts must support RTL admin locales if the Admin Portal supports them (confirm against NEXT-JS-INSTRUCTIONS.md's localization scope — the doc shows `updateLanguagePreference` supporting `hi`/`ar`/`en`, implying RTL support is expected).

## 21. Analytics
N/A explicitly required by PRD for this admin surface beyond the audit log (§8/§9); no client-side analytics events specified.

## 22. Performance
Trivial low-traffic admin page; standard React Query caching (`useSettings`-equivalent stale-time pattern).

## 23. Security
The ceiling-table editor is the platform's most safety-sensitive admin surface in this feature — dual-scope enforcement must be visibly reflected in the UI (e.g., disable submit until elevation succeeds), not just relied upon server-side.

## 24. Library Requirements
Next.js 15, TanStack Query v5, Zod, React Hook Form (confirm exact form library against existing Admin Portal conventions before introducing a new one).

## 25. Testing
- Component test: ceiling-table submit button disabled until elevation obtained.
- Component test: form validation errors render correctly.
- Integration test (mocked API): full defaults-update flow.
- Integration test (mocked API): ceiling-table update flow including elevation request.

## 26. Documentation
Inline comment on `AiCeilingTableEditor` explaining the platform-wide safety implications and why elevation is required, mirroring A.5's admin-console rigor.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Confirm Exact `AdminPermission` Strings**
- Objective: Verify the exact permission constants to use with `RequirePermission` against the platform's actual `AdminPermission` type before inventing new ones.

**Task 02 — Add API Endpoint Constants**
- Files to Modify: `src/shared/constants/api-endpoints.ts`

**Task 03 — Define Zod Schemas**
- Files to Create: `src/features/restriction-engine/api/schemas.ts`

**Task 04 — Implement Repository**
- Files to Create: `restriction-defaults.repository.ts`

**Task 05 — Implement Query/Mutation Hooks**
- Files to Create: the four hooks listed in §8.

**Task 06 — Implement `RestrictionDefaultsForm`**
- Files to Create: `components/restriction-defaults-form.tsx`

**Task 07 — Implement `AiCeilingTableEditor` with Elevation Flow**
- Files to Create: `components/ai-ceiling-table-editor.tsx`
- Implementation Details: Mirror `DeleteFamilyButton`'s elevation pattern exactly.

**Task 08 — Implement Page Route**
- Files to Create: `src/app/(dashboard)/restriction-engine/defaults/page.tsx`

**Task 09 — Add Sidebar Navigation Entry**

**Task 10 — Add Component/Integration Tests**

**Task 11 — Final Code Review**
- Objective: Confirm elevation is genuinely required (not bypassable) and confirm permission strings match the real `AdminPermission` enum.

## 28. Definition of Done
- Defaults form and ceiling-table editor both functional against B-07.
- Ceiling-table edits require and correctly use elevation.
- RBAC-gated per confirmed permission strings.

## 29. Final Verification Checklist
- [ ] Confirmed real `AdminPermission` strings used (not invented)
- [ ] Ceiling-table submit blocked until elevation succeeds
- [ ] Zod validation mirrors backend rules
- [ ] `ConfirmationDialog isDanger` shown before ceiling-table submit
- [ ] Tests cover both happy path and elevation-failure path
- [ ] Localization strings added
