# N-06 — Quran Content Proposal Editor & Elevated Scholar Review

## 1. Feature Context
The deliberately distinct, stricter authoring/review path for Quran-adjacent content — visually and structurally separate from the general Story Editor, so the elevated rigor this content category requires is never diluted by shared general-purpose tooling.

## 2. Parent Feature
E.29 — Content CMS & Scholar Review Workflow

## 3. Sub-feature
2.6 Quran Content Proposal Editor & Elevated Scholar Review (ID: **N-06**)

## 4. Objective
Build the Quran Content Proposal Editor (translation/tafseer/recitation, linked to an immutable ayah) and the Quran Scholar Review screen (surfacing the elevated confidence threshold) against B-08.

## 5. Business Requirements
- FR-10: ayah text immutable; only translations/tafseer/recitations version; proposed changes link to an existing immutable ayah record; scholar review at an elevated confidence threshold; approval publishes with locale + age tags.
- §1.18 screens 25–26: Quran Content Proposal Editor, Quran Scholar Review (elevated confidence threshold).

## 6. Existing Architecture
`src/features/quran-proposals/` module, deliberately separate navigation/route from the general Content CMS (N-01), consuming A.5's existing ayah reference data read-only.

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`
- A.5's existing ayah-selector/reference component if one already exists in the Admin Portal (reuse, do not rebuild a parallel ayah browser)

## 8. Files to Create
- `src/app/(dashboard)/quran-proposals/page.tsx`
- `src/app/(dashboard)/quran-proposals/new/page.tsx` — Proposal Editor
- `src/app/(dashboard)/quran-proposals/[id]/review/page.tsx` — Elevated Scholar Review
- `src/features/quran-proposals/api/quran-proposal-repository.ts`
- `src/features/quran-proposals/hooks/use-quran-proposals.ts`, `use-ayah-lookup.ts`, `use-submit-quran-decision.ts`
- `src/features/quran-proposals/components/ayah-reference-selector.tsx`
- `src/features/quran-proposals/components/proposal-type-form.tsx` — translation/tafseer/recitation-specific fields
- `src/features/quran-proposals/components/elevated-threshold-banner.tsx`
- `src/features/quran-proposals/types/quran-proposal.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `QURAN_PROPOSALS.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item under "Content" group, distinct from the general Content List entry

## 10. NextJS Requirements
- `AyahReferenceSelector`: read-only lookup against A.5's ayah reference data — no create/edit capability for the ayah itself anywhere in this module's component tree (structurally: no form field binds to ayah text).
- `ProposalTypeForm`: renders translation/tafseer/recitation-specific fields based on `proposal_type`.
- `ElevatedThresholdBanner`: displays the actual `QURAN_REVIEW_CONFIDENCE_THRESHOLD` value fetched from the server (never hardcoded), visibly distinct from the general Scholar Review screen's threshold framing, reinforcing to the reviewer that this is the stricter path.
- Approval publishes with locale + age tags attached to the new version.

## 11. Required API
**Admin API** — B-08: `POST /v1/admin/quran-proposals`, `PATCH /v1/admin/quran-proposals/{id}`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="content_editor"` for proposal creation, `permission="scholar_reviewer"` for the elevated review screen.

## 13. Loading / Empty / Error States
Ayah lookup loading/empty (no matching ayah) states; proposal-submission error state; invalid-ayah-reference error distinct from a general submission failure.

## 14. Responsive UI / Accessibility
Ayah reference text rendered with correct Arabic typography/RTL support (this content is inherently Arabic-script, regardless of the Admin Portal's own general localization scope); proposal form fully keyboard-navigable.

## 15. Localization / RTL
Ayah text and Arabic-script content render RTL correctly regardless of the admin's own UI locale — this is a content-rendering requirement, not an admin-UI-localization one.

## 16. Security
No form field or component in this module can write to ayah text — the `AyahReferenceSelector` is read-only by construction, mirroring B-08's read-only FK relationship at the UI layer.

## 17. Testing
Unit: `proposal_type`-driven form field rendering, threshold-value-fetched-not-hardcoded logic. UI: ayah reference selector has no editable text field for the ayah itself (structural absence test). Integration: full propose → elevated review → approve → publish-with-tags flow.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `quran-proposal.ts` schema. Files: `types/quran-proposal.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `QuranProposalRepositoryImpl`**
Objective: Repository for B-08's two endpoints. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `AyahReferenceSelector` (Read-Only)**
Objective: Ayah lookup with zero write capability. Dependencies: Task 02. Tests: **mandatory** — structural test confirming no editable ayah-text field exists in this component. Definition of Done: test passes.

**Task 04 — Implement `ProposalTypeForm`**
Objective: Type-specific fields for translation/tafseer/recitation. Dependencies: Task 02. Tests: per-type field rendering. Definition of Done: test passes.

**Task 05 — Implement `ElevatedThresholdBanner`**
Objective: Server-fetched threshold display, never hardcoded. Dependencies: Task 02. Tests: threshold-value-sourced-from-server test. Definition of Done: test passes.

**Task 06 — Implement the Proposal Editor and Review Pages**
Objective: Compose selector + form + submit; review page with threshold banner + decision actions. Dependencies: Tasks 03–05. Tests: full-flow smoke tests. Definition of Done: tests pass.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm zero write path to ayah text exists anywhere in this module, confirm this path is visually and structurally distinct from the general Content Editor. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Ayah reference selector is read-only — no editable ayah-text field exists anywhere in the module
- [ ] Proposal type correctly drives translation/tafseer/recitation-specific form fields
- [ ] Elevated threshold value is fetched from the server, never hardcoded
- [ ] Approval publishes with locale + age tags
- [ ] This module is visually/structurally distinct from N-01's general Story Editor

## 20. Definition of Done
Quran-adjacent content proposals are authored and reviewed through a deliberately separate, elevated-rigor path with zero capability to mutate immutable ayah text — reinforcing B-08's backend guarantee at the UI layer.
