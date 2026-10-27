# N-01 — Consent Type Registry Management

## 1. Feature Context
Part of Feature C.26's Admin Requirements (§8). Full CRUD (with a review-gate) over consent type definitions, consuming B-05.

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**N-01 — Consent Type Registry Management**

## 4. Objective
Build a `legal_compliance`/`content_editor`-gated page for creating and updating consent type definitions, with the create/update-then-approve two-step workflow B-05 requires visibly represented (never a single-step "save and it's live" UI).

## 5. Business Requirements
- §8/§9: full CRUD for consent type definitions, changes route through legal/scholar review before becoming active.
- CRUD permissions: `legal_compliance`/`content_editor`.

## 6. Existing Architecture
Follows the NextJS Admin layered architecture (`NEXT-JS-INSTRUCTIONS.md`): Page → Custom Hook → Repository/`BaseResourceClient` → `apiClient` → Backend REST API, wrapped in `RequirePermission` — the same pattern C.21 N-01 and C.19 N-01 already use.

## 7. Existing Code to Reuse
- `BaseResourceClient<TEntity, TCreate, TUpdate, TFilters>` — extend for `ConsentTypeResourceClient`, exposing `list`/`create`/`update`/a distinct `approve` action (not part of the generic base — add as a custom method, following the precedent of feature-specific actions beyond plain CRUD elsewhere in the admin codebase).
- `DataTable`, `SearchBar`, `RequirePermission`, `StatusBadge` (for `pending_review`/`active`/`superseded` status).
- Existing form-building pattern for admin create/edit forms (per `NEXT-JS-INSTRUCTIONS.md`'s documented forms convention).

## 8. Files to Create
- `src/features/consent-type-registry/api/consent-type-resource-client.ts`
- `src/features/consent-type-registry/api/schemas.ts` (Zod schemas)
- `src/features/consent-type-registry/hooks/use-consent-types.ts`
- `src/features/consent-type-registry/hooks/use-approve-consent-type.ts`
- `src/features/consent-type-registry/components/ConsentTypeForm.tsx`
- `src/features/consent-type-registry/index.ts`
- `src/app/(dashboard)/legal/consent-types/page.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `API_ENDPOINTS.CONSENT_TYPES.BASE`, `.APPROVE(id)`.
- Sidebar navigation config — add entry under Legal/Compliance, gated by `RequirePermission`.

## 10. Backend Requirements
Consumes B-05 exclusively (`GET/POST/PATCH /v1/admin/consent-types`, `POST /v1/admin/consent-types/{id}/approve`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- `ConsentTypeResourceClient extends BaseResourceClient<ConsentTypeDefinition, ConsentTypeCreate, ConsentTypeUpdate, ConsentTypeFilters>`, plus a non-CRUD `approve(id)` method.
- Table renders `type_code`, `required` badge, `review_status` (`StatusBadge`: pending_review/active/superseded), `activated_at`.
- Create/Edit form always results in a `pending_review` row — the UI must never present a "Save & Publish" single-step action; "Save Draft" and a separate, clearly distinct "Approve" action (visible only to a reviewer, ideally requiring the reviewer differ from the author per B-05's flagged four-eyes constraint) are the only two mutation paths.
- `RequirePermission permission="consent-types:manage"` gating the page; confirm/add this permission string to the frontend's `AdminPermission` catalog, mapped to the backend's `legal_compliance`/`content_editor` roles.

## 13. API Contract
Consumes B-05's contract as documented in that blueprint.

## 14. Database Requirements
Not applicable — Admin Portal has no direct DB access.

## 15. Validation
`type_code` required, unique (server-validated, surfaced inline); `display_text_version_ref` required, validated against the legal-content versioning system (B-05 §6, location to be confirmed).

## 16. Authentication
`useAdminSession()` standard guard.

## 17. Authorization
`RequirePermission` wraps the page and the Approve action separately — a `legal_compliance`/`content_editor` user without reviewer standing (if the four-eyes rule is confirmed) sees the Approve button disabled with an explanatory tooltip, not hidden without explanation.

## 18. Error Handling
- `QueryErrorState` for list/detail failures.
- Inline form validation errors (duplicate `type_code`, invalid version ref).
- `403` on approve attempted by the original author (if four-eyes is confirmed) → clear, specific message, not a generic error.

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
All labels, status badges, form fields via `useTranslation()`.

## 22. RTL
Full RTL layout for the table and form.

## 23. Analytics
Not specified in PRD; standard admin audit trail suffices (server-side, per B-05).

## 24. Performance
Server-side pagination if the registry grows large (unlikely given it's a small, curated list — confirm pagination is actually needed before adding it, per the "don't build what isn't required" principle).

## 25. Security
- Approve action structurally distinct from create/update in the resource client (separate method, not a flag on `update`), mirroring the review-gate's backend enforcement.
- No path in the UI allows a create/update call to simultaneously activate a version.

## 26. Library Requirements
No new libraries — TanStack Query, Zod, existing shared component library, existing form library.

## 27. Testing
- Unit: `ConsentTypeResourceClient` Zod validation on both valid and malformed responses.
- Integration/UI: create flow results in `pending_review` status, never `active`, immediately after save.
- Integration/UI: Approve action is a distinct, separately-permissioned control from Save.
- Integration/UI: `RequirePermission` correctly hides the page/nav-entry for unauthorized roles.
- Negative test: no UI path exists that activates a version without a separate Approve action.

## 28. Documentation
Document the two-step draft/approve workflow prominently in the feature's README, cross-referencing B-05.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Zod Schemas & Resource Client with Distinct Approve Method**
- **Files to Create:** `schemas.ts`, `consent-type-resource-client.ts`.
- **Definition of Done:** `approve()` is structurally separate from `update()`.

**Task 02 — `useConsentTypes` and `useApproveConsentType` Hooks**
- **Files to Create:** both hooks.

**Task 03 — `ConsentTypeForm` (Draft-Only) and Table Page**
- **Files to Create:** `ConsentTypeForm.tsx`, `page.tsx`.
- **Tests:** negative test confirming no single-step publish path exists.

**Task 04 — Approve Action UI with Four-Eyes Consideration**
- **Implementation Details:** disable with tooltip if the current admin authored the pending version and four-eyes is confirmed required.

**Task 05 — Permission Wiring, Localization, RTL**

**Task 06 — Full Test Suite & Documentation**

## 30. Definition of Done
Consent type CRUD is fully functional with a genuinely two-step draft/approve workflow, correctly permission-gated, and provably free of any single-step publish path.

## 31. Final Verification Checklist
- [ ] `approve()` structurally distinct from `update()` in the resource client
- [ ] No UI path publishes a version without a separate Approve action
- [ ] Four-eyes consideration implemented (or explicitly deferred if not confirmed required)
- [ ] `RequirePermission` correctly gates page and nav entry
- [ ] Full localization and RTL verified
