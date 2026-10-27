# N-04 — Islamic Fact & Occasion Calendar Manager

## 1. Feature Context
NoorHeroes Admin Portal (NextJS). Full CRUD interface for the Islamic Fact of the Day pool and the Islamic calendar occasion mappings used in Home greetings, scholar-approval-gated before publish.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
3.4 Islamic Fact & Occasion Calendar Manager (ID: N-04)

## 4. Objective
Build full CRUD for fact entries (text per locale/age-band, source citation, scholar-approval status) and calendar-occasion mappings (Hijri date ranges → greeting phrase keys), enforcing a hard validation rule that `scholar_status = 'approved'` is required before `active = true` — as a form-level hard block, not a warning.

## 5. Business Requirements
Per PRD §8, §9 item 4:
- Full CRUD for fact entries and occasion mappings.
- New/edited facts require `scholar_status = 'approved'` before `active = true` — hard validation rule in the form, not just a warning.
- Mirrors the Content CMS approval pattern from A.1's admin section (reuse that pattern, don't invent a new approval workflow).

## 6. Existing Architecture
Follow `NEXT-JS-INSTRUCTIONS.md` conventions and A.1's existing Content CMS scholar-approval workflow pattern (reuse the approval-state UI/logic if A.1 already implemented one, rather than building a parallel approval mechanism).

## 7. Existing Code to Reuse
A.1's scholar-approval workflow components/logic if available; existing Admin Portal CRUD-table/form patterns; existing audit-logging convention.

## 8. Files to Create
- `app/(admin)/islamic-facts/page.tsx`
- `app/(admin)/islamic-facts/occasions/page.tsx`
- `components/islamic-facts/FactTable.tsx`, `components/islamic-facts/FactForm.tsx`
- `components/islamic-facts/OccasionMappingTable.tsx`, `components/islamic-facts/OccasionMappingForm.tsx`
- `lib/api/islamicFacts.ts`
- `types/islamicFacts.ts`
- `lib/validation/factSchema.ts` (includes the hard approval-before-active rule)

## 9. Files to Modify
- Admin navigation/sidebar config (two entries: Facts, Occasion Calendar — or a tabbed single page, per existing admin-portal UX convention for related-but-distinct entities)

## 10. Backend Requirements
Consumes admin CRUD endpoints for the fact pool and occasion-mapping tables (owned/created by this sub-feature's backend counterpart — coordinate: B-07's blueprint assumes these tables already exist and are owned by N-04; confirm the corresponding backend admin CRUD API is implemented, either as part of B-07's scope extension or a dedicated admin-API addition, before finalizing this sub-feature's API client).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Fact CRUD: text per locale/age-band, source citation, `scholar_status` (draft/pending/approved/rejected), `active` toggle.
- Hard client-side AND server-side validation: form blocks setting `active = true` unless `scholar_status === 'approved'` (client validation is UX convenience; server validation, per B-07 §15, is the authoritative defense-in-depth check).
- Occasion mapping CRUD: Hijri date range → greeting phrase key.
- List/filter/sort by locale, age band, approval status; pagination for large catalogs.
- Every CRUD action writes an audit_log row.
- Localized form fields (EN/HI/AR/UR) with RTL-aware text inputs for Arabic/Urdu fact text.

## 13. API Contract
**Admin API:**
- `GET /admin/v1/facts` (paginated, filterable) — `POST /admin/v1/facts` — `PATCH /admin/v1/facts/{id}` — `DELETE /admin/v1/facts/{id}` (full CRUD per PRD §8, unlike N-02's soft-delete-only rule — confirm this distinction is intentional per the PRD's explicit "full CRUD" wording for this sub-feature)
- `GET /admin/v1/occasions`, `POST`, `PATCH`, `DELETE` — occasion-mapping CRUD

## 14. Database Requirements
Fact pool and occasion-mapping tables — schema ownership coordinated with B-07 (§10); this sub-feature is the primary CRUD owner even though B-07 reads from these tables at runtime.

## 15. Validation
`scholar_status = 'approved'` required before `active = true` — this is the sub-feature's signature hard-validation rule; must be enforced both client-side (immediate feedback) and server-side (authoritative), and covered by an explicit test attempting to bypass it via a direct API call with client validation skipped.

## 16. Authentication
Existing Admin Portal Bearer-session auth.

## 17. Authorization
Full CRUD behind the scholar-approval gate per PRD §8; confirm the specific admin role(s) permitted (likely a `content_editor`/`scholar_reviewer` role pairing similar to A.1's Content CMS pattern — reuse that role structure rather than inventing new roles).

## 18. Error Handling
Form blocks submission with a clear inline message when attempting `active=true` without approval; duplicate/conflict validation errors shown inline; API failure shown as a retry-capable banner.

## 19. Offline First
Not applicable (admin web portal).

## 20. Local Data
Not applicable.

## 21. Localization
Fact text entry must support all four locales (EN/HI/AR/UR) as separate localized fields per entry (not a single field with a locale selector that loses other-locale data) — confirm the exact multi-locale content-entry pattern against A.1's Content CMS convention rather than inventing a new one.

## 22. RTL
Arabic/Urdu text-entry fields must support RTL text direction input correctly (not just RTL page layout — actual RTL text-entry behavior in the textarea/input).

## 23. Analytics
Not specified as required; skip unless existing admin-tooling convention requires it.

## 24. Performance
Paginated fact/occasion tables (server-side pagination) for scalability as the catalog grows.

## 25. Security
Hard approval-gate validation is the primary security/quality-control concern; server-side enforcement (per B-07 §15) is non-negotiable even if this admin UI has a bug — defense in depth.

## 26. Library Requirements
Next.js, existing Admin Portal form/table/validation libraries, existing multi-locale content-entry component pattern from A.1 if available.

## 27. Testing
- Component test: fact form blocks `active=true` submission when `scholar_status !== 'approved'`, with clear inline error.
- Integration test: attempting to bypass the client-side gate via a direct API call (skipping the form) is still rejected by the server (mirrors B-07's server-side check) — this test proves defense-in-depth, not just UI correctness.
- Component test: occasion mapping CRUD table/form function correctly.
- Component test: multi-locale fact entry preserves all locale variants correctly (editing the Arabic field doesn't clear the English field).
- Integration test: audit-log entry created on every CRUD action.

## 28. Documentation
Documentation noting the hard approval-gate rule explicitly, and cross-referencing B-07's server-side enforcement of the same rule so future contributors understand both layers exist intentionally.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Types, API Client & Validation Schema (Including Hard Approval Gate)**
- Objective: Typed contract and the signature validation rule.
- Why Required: Foundation for both fact and occasion CRUD.
- Existing Architecture to Follow: Existing admin-portal API-client and validation conventions; A.1's Content CMS approval-schema pattern if reusable.
- Existing Files to Reuse: Existing typed-fetch wrapper, existing validation-library setup.
- Files to Create: `types/islamicFacts.ts`, `lib/api/islamicFacts.ts`, `lib/validation/factSchema.ts`
- Files to Modify: none
- Implementation Details: `FactEntry { id, textByLocale, sourceCitation, ageBand, scholarStatus, active }`; Zod (or existing) schema with a `.refine()` rule rejecting `active: true` when `scholarStatus !== 'approved'`.
- Business Rules: This IS the hard-gate rule at the schema level.
- Validation: Explicit refine/cross-field validation.
- Error Handling: Clear, field-attributable error message.
- Security: Client-side layer of the defense-in-depth approval gate.
- Performance: N/A.
- Localization: `textByLocale` typed as a record keyed by supported locale codes, all required (or explicitly optional per business rule — confirm against A.1's pattern; default to requiring at least English).
- RTL: N/A (type-level).
- Analytics: N/A.
- Tests: Schema unit test confirming the refine rule rejects the invalid combination and accepts the valid one.
- Documentation: TSDoc.
- Dependencies: Backend admin CRUD API for facts/occasions (coordinate before finalizing).
- Do Not Change: Do not weaken this validation rule.
- Expected Result: Typed foundation with hard-gate schema.
- Definition of Done: Schema unit test passes.

**Task 02 — Build Fact CRUD (Table + Form) with Multi-Locale Entry**
- Objective: Fact management UI.
- Why Required: Primary deliverable (fact pool side).
- Existing Architecture to Follow: A.1's multi-locale content-entry pattern if available; existing admin table/form conventions.
- Existing Files to Reuse: Task 01 schema/client.
- Files to Create: `components/islamic-facts/FactTable.tsx`, `components/islamic-facts/FactForm.tsx`, `app/(admin)/islamic-facts/page.tsx`
- Files to Modify: Admin navigation config
- Implementation Details: Table with filter/sort/pagination by locale/age-band/status; form with per-locale tabbed or stacked text fields, RTL-aware inputs for AR/UR, `scholarStatus` selector, `active` toggle disabled/blocked per Task 01's schema rule.
- Business Rules: Hard approval gate enforced in the form UI (toggle disabled or submission blocked with clear messaging).
- Validation: Task 01 schema.
- Error Handling: Inline + banner per §18.
- Security: Client-side gate layer.
- Performance: Server-side pagination.
- Localization: Full multi-locale entry support.
- RTL: Verified RTL text-entry for Arabic/Urdu fields specifically.
- Analytics: N/A.
- Tests: Component tests per §27 (gate-blocking, multi-locale preservation).
- Documentation: Page comment.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working fact CRUD.
- Definition of Done: Tests pass.

**Task 03 — Build Occasion Mapping CRUD**
- Objective: Hijri date-range → greeting-phrase-key management UI.
- Why Required: Second half of this sub-feature's scope.
- Existing Architecture to Follow: Existing admin table/form conventions.
- Existing Files to Reuse: Task 01 client patterns (extended for occasions).
- Files to Create: `components/islamic-facts/OccasionMappingTable.tsx`, `components/islamic-facts/OccasionMappingForm.tsx`, `app/(admin)/islamic-facts/occasions/page.tsx`
- Files to Modify: Admin navigation config
- Implementation Details: Table + form for Hijri date-range entries mapping to greeting phrase keys; standard full-CRUD (no special approval gate specified for occasions in the PRD, unlike facts — confirm this distinction is intentional rather than an oversight before finalizing).
- Business Rules: Per PRD, full CRUD, scholar-approval-gated "before publish" — clarify whether this gate applies to occasions too or facts only; PRD §9 item 4 groups both under "scholar approval status" for facts specifically, so apply the same hard-gate pattern here as a conservative default unless product guidance says otherwise.
- Validation: Date-range validity (start <= end, no unintended overlaps — confirm overlap-handling business rule before assuming silent overlap is acceptable).
- Error Handling: Per §18.
- Security: N/A beyond standard admin auth.
- Performance: N/A (small dataset expected).
- Localization: Greeting phrase keys reference locale-specific phrasing pools (owned by B-02); this UI manages the mapping, not the phrasing text itself.
- RTL: Per §22.
- Analytics: N/A.
- Tests: Component tests for CRUD operations and date-range validation.
- Documentation: Page comment noting the date-range overlap-handling decision made.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working occasion-mapping CRUD.
- Definition of Done: Tests pass; navigation entries added.

## 30. Definition of Done
Full CRUD for facts (with hard scholar-approval gate) and occasion mappings, multi-locale/RTL text entry working correctly, every action audit-logged; all tests green.

## 31. Final Verification Checklist
- [ ] `active=true` is blocked in the form unless `scholarStatus='approved'`, both client and server-side
- [ ] Direct API bypass of the client gate is still rejected server-side (defense-in-depth verified by test)
- [ ] Multi-locale fact text entry preserves all locale variants independently
- [ ] RTL text-entry verified for Arabic/Urdu fact fields
- [ ] Occasion mapping CRUD functions correctly with valid date-range validation
- [ ] Every CRUD action writes an audit_log row
- [ ] All tests pass
