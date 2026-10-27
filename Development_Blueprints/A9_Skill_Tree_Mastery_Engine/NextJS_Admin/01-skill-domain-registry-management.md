# N-01 — Skill Domain Registry Management

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). The Admin Portal CRUD page for the `skill_domain` registry (B-01/B-09) — the gating list that makes FR-9's "add a domain via data alone" promise usable by a real admin, and the required replacement for A.5's Curriculum Builder's hardcoded domain dropdown.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
N-01 — Skill Domain Registry Management (Admin Page)

## 4. Objective
Build a simple CRUD table page (`domain_key`, `display_name`, `active`) backed by B-09's `GET/POST/PUT /admin/v1/mastery/domains`, and update A.5's existing Curriculum Builder domain-selector dropdown to fetch from this same endpoint instead of a static enum.

## 5. Business Requirements
- Admin AI Code-Generation Prompt (A.9 PRD §9) item 1: "a simple CRUD table... This is the gating list that the Skill Tree / Curriculum Builder's domain selector dropdown (from A.5) should read from dynamically, rather than a hardcoded list of options — update that existing dropdown component to fetch from `GET /admin/v1/mastery/domains` instead of a static enum."
- CRUD permissions: full CRUD behind `product_admin` role.

## 6. Existing Architecture
React + TypeScript Admin Portal (NextJS). Reference `NEXT-JS-INSTRUCTIONS.md` for app structure, routing, component conventions, API-client layer, auth/RBAC context, form/table/pagination patterns already established. A.5's existing Curriculum Builder (`01-skill-tree-curriculum-builder.md`) already has a domain-selector dropdown component this sub-feature must locate and modify.

## 7. Existing Code to Reuse
- Existing Admin Portal CRUD table pattern (reuse whatever generic/reusable table+form component the platform already has for simple lookup-table management — do not build a bespoke table component for this).
- Existing RBAC context/role-guard components (`product_admin` gating).
- Existing API-client layer conventions (typed fetch wrapper, error handling, loading states).
- A.5's Curriculum Builder's domain-selector dropdown component — locate and modify, don't duplicate.

## 8. Files to Create
- `app/admin/mastery/domains/page.tsx` — the Skill Domain Registry page.
- `app/admin/mastery/domains/components/SkillDomainTable.tsx`
- `app/admin/mastery/domains/components/SkillDomainFormDialog.tsx` — create/edit form.
- `lib/api/masteryDomains.ts` — typed API-client functions (`listDomains`, `createDomain`, `updateDomain`).
- `lib/types/masteryDomain.ts` — TypeScript types matching B-09's schema.
- `__tests__/admin/mastery/domains/SkillDomainTable.test.tsx`

## 9. Files to Modify
- A.5's Curriculum Builder domain-selector dropdown component — replace its hardcoded enum/options list with a call to `lib/api/masteryDomains.ts`'s `listDomains()` (filtered to `active: true`).

## 10. Backend Requirements
N/A (consumes B-09).

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Page:** `/admin/mastery/domains` — table listing all domains (active + inactive), with create/edit actions.
- **Table columns:** `domain_key`, `display_name`, `active` (toggle or badge), last-modified metadata if available.
- **Create form:** `domain_key` (immutable once created — read-only on edit), `display_name`, `active` toggle.
- **Deactivation confirmation:** if B-09 returns a `409` (domain has active `skill_node` rows), show a clear confirmation dialog explaining the impact before allowing a forced deactivation (if the API supports a `force` flag) — never silently retry with force without explicit admin confirmation.
- **RBAC:** page and all mutating actions gated behind `product_admin` role; non-admins see an access-denied state, not a broken/empty page.
- **Loading/empty/error states:** standard patterns — skeleton/spinner on load, "no domains registered yet" empty state (unlikely given seed data, but handled), error state with retry on fetch failure.

## 13. API Contract
Consumes B-09's `GET/POST/PUT /admin/v1/mastery/domains[/{domain_key}]` exactly as specified there — no invented fields.

## 14. Database Requirements
N/A (frontend only).

## 15. Validation
Client-side form validation mirrors B-09's server-side rules: `domain_key` lowercase snake_case format, non-empty `display_name`, before submission — server remains the source of truth, but client-side validation improves UX by catching errors before a round-trip.

## 16. Authentication
Reuses existing Admin Portal auth/session context.

## 17. Authorization
`product_admin` role required for create/update actions; read access per B-09's confirmed scope (§13 note in B-09 — may be broader than `product_admin` for read).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate `domain_key` on create | Form-level error shown inline, submission not silently retried |
| Deactivation blocked by active content (409) | Confirmation dialog explaining impact, with an explicit force-confirm action if supported |
| Fetch failure | Error state with retry, not a blank table |
| Non-`product_admin` user reaches the page | Access-denied state, not a broken/empty table |

## 19. Offline First
N/A (admin web app, always-online context).

## 20. Local Data
N/A.

## 21. Localization
Admin Portal UI localization scope per existing platform convention — if Admin Portal is English-only for internal tooling, document that as the deliberate scope; if it supports EN/HI/AR/UR like the child/parent-facing surfaces, apply the same localization pattern here.

## 22. RTL
If Admin Portal supports RTL locales, verify table/form layout mirrors correctly; otherwise document as out of scope consistent with §21's determination.

## 23. Analytics
N/A (internal admin tooling; audit logging, not product analytics, is the relevant tracking mechanism here — per B-09's audit-log requirement).

## 24. Performance
Small dataset (handful of domains) — no pagination/virtualization required; standard React Query/SWR-style caching (whichever the platform's existing API-client pattern uses) for the domain list, invalidated on mutation.

## 25. Security
`product_admin` RBAC enforced both client-side (UI gating) and relies on B-09's server-side enforcement as the actual security boundary (client-side gating is UX, not the security control).

## 26. Library Requirements
No new libraries beyond the existing Admin Portal stack (React, TypeScript, existing table/form/dialog component library).

## 27. Testing
- Unit: form validation logic.
- Component test: `SkillDomainTable` renders correctly for various data states (empty, populated, loading, error).
- Integration/E2E: create → list reflects new domain → A.5's Curriculum Builder dropdown reflects the new domain dynamically (this is the key cross-feature verification for this sub-feature).
- RBAC test: non-admin access denied.

## 28. Documentation
Note in the page's code comments (or Admin Portal internal docs) that this page's `GET` endpoint is the required data source for A.5's Curriculum Builder dropdown — cross-reference for future maintainers.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Build API Client & Types**
- Task ID: N-01-T01
- Objective: Typed client layer for B-09.
- Why This Is Required: Foundation for the page and for the Curriculum Builder dropdown migration.
- Existing Architecture to Follow: Existing Admin Portal API-client conventions.
- Existing Files to Reuse: Existing typed-fetch wrapper.
- Files to Create: `lib/api/masteryDomains.ts`, `lib/types/masteryDomain.ts`.
- Files to Modify: None.
- Implementation Details: `listDomains()`, `createDomain()`, `updateDomain()` matching B-09's contract exactly.
- Business Rules: N/A. Validation: Type-safe request/response shapes.
- Error Handling: Standard typed error propagation.
- Security: Reuses existing auth-header attachment. Performance: N/A.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: N/A (thin client layer, covered by integration tests).
- Documentation: TSDoc.
- Dependencies: B-09.
- Do Not Change: N/A.
- Expected Result: Working typed client.
- Definition of Done: Types match B-09's schema exactly.

**Task 02 — Build SkillDomainTable & SkillDomainFormDialog**
- Task ID: N-01-T02
- Objective: The CRUD page UI.
- Why This Is Required: Core deliverable.
- Existing Architecture to Follow: Existing generic table/dialog component patterns.
- Existing Files to Reuse: Platform's reusable table/form/dialog components.
- Files to Create: `page.tsx`, `SkillDomainTable.tsx`, `SkillDomainFormDialog.tsx`.
- Files to Modify: None.
- Implementation Details: Standard list+create+edit CRUD flow, deactivation-confirmation dialog per §12.
- Business Rules: `domain_key` immutable on edit.
- Validation: Client-side per §15.
- Error Handling: Per §18.
- Security: `product_admin` RBAC gate.
- Performance: Small dataset, no pagination needed.
- Localization: Per §21 decision. RTL: Per §22.
- Analytics: N/A.
- Tests: `SkillDomainTable.test.tsx`.
- Documentation: N/A.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working CRUD page.
- Definition of Done: Component tests green; manual RBAC verification.

**Task 03 — Migrate A.5's Curriculum Builder Dropdown to Dynamic Source**
- Task ID: N-01-T03
- Objective: Replace the hardcoded domain enum with a live fetch from this sub-feature's data source.
- Why This Is Required: Explicit, named requirement in the top-level Admin AI Prompt — this is the actual point of building the registry.
- Existing Architecture to Follow: A.5's existing Curriculum Builder component structure.
- Existing Files to Reuse: A.5's domain-selector dropdown component — locate and modify in place.
- Files to Create: None.
- Files to Modify: A.5's Curriculum Builder dropdown component.
- Implementation Details: Replace static options array with `listDomains({ active: true })` call, cached/invalidated consistently with the rest of the Curriculum Builder's data-fetching pattern.
- Business Rules: Only `active: true` domains appear as selectable options for new `skill_node` creation.
- Validation/Error Handling: Fallback/loading state while the dropdown's own fetch is in flight.
- Security: N/A beyond existing Curriculum Builder RBAC. Performance: Small, cacheable dataset.
- Localization: N/A (delegated to Task 02's decision). RTL: N/A. Analytics: N/A.
- Tests: E2E test confirming a newly-created domain (via N-01's UI) appears in the Curriculum Builder's dropdown without a code deploy.
- Documentation: N/A (migration task).
- Dependencies: Task 01, Task 02.
- Do Not Change: A.5's Curriculum Builder's other functionality (only the dropdown's data source changes).
- Expected Result: Dropdown is now fully data-driven.
- Definition of Done: E2E test proving zero-code-change domain addition end-to-end (Admin registers domain → Curriculum Builder dropdown shows it immediately) passes — this is the tangible proof of FR-9's extensibility promise at the tooling layer.

## 30. Definition of Done
Skill Domain Registry Management page live, `product_admin`-gated, full CRUD with a deactivation-confirmation safeguard; A.5's Curriculum Builder dropdown fully migrated off its hardcoded enum to read dynamically from this registry.

## 31. Final Verification Checklist
- [ ] CRUD page working (create/read/update; deactivate with confirmation, not hard-delete)
- [ ] `product_admin` RBAC enforced
- [ ] Deactivation-with-active-content confirmation flow working
- [ ] A.5's Curriculum Builder dropdown now reads dynamically from this registry (E2E-verified, zero code change for a new domain)
- [ ] Loading/empty/error states all handled
- [ ] `domain_key` immutability enforced in the edit form
