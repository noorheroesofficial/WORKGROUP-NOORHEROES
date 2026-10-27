# N-03 — RTL Preview

## 1. Feature Context
The tool that lets a localization manager actually see mirrored layout fidelity for Arabic/Urdu before anything ships — a genuine side-by-side rendering comparison, not a cosmetic direction toggle on a single panel that could hide real layout defects.

## 2. Parent Feature
E.34 — Localization Management

## 3. Sub-feature
2.3 RTL Preview (ID: **N-03**)

## 4. Objective
Build the RTL Preview screen against B-04, rendering an actual side-by-side LTR-reference / RTL-rendering comparison with both panels rendered simultaneously.

## 5. Business Requirements
- §1.18 screen 4: RTL Preview (Arabic/Urdu).
- §2.1/§2.2: a genuine side-by-side LTR/RTL rendering comparison, not merely a text-direction toggle — letting the manager see actual mirrored layout fidelity, with a screen-selector to preview different child/parent-facing screens.
- §7 Frontend AI prompt item 3: both panels render simultaneously for a fixture screen/string set — tested explicitly.
- FR-7: full RTL mirroring for Arabic and Urdu.

## 6. Existing Architecture
`src/features/rtl-preview/` module.

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`

## 8. Files to Create
- `src/app/(dashboard)/platform/locales/[code]/rtl-preview/page.tsx`
- `src/features/rtl-preview/api/rtl-preview-repository.ts`
- `src/features/rtl-preview/hooks/use-rtl-preview.ts`
- `src/features/rtl-preview/components/rtl-preview-comparison.tsx` — dual simultaneous panels
- `src/features/rtl-preview/components/screen-selector.tsx`
- `src/features/rtl-preview/types/rtl-preview.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `RTL_PREVIEW.*` endpoints

## 10. NextJS Requirements
- `RtlPreviewComparison`: renders two genuinely separate, simultaneously-mounted preview panels — an LTR-reference panel (fixed `dir="ltr"`) and an RTL-rendering panel (fixed `dir="rtl"`) — both populated from the same fetched preview data, never a single panel whose `dir` attribute is toggled by a control (which would only demonstrate text-direction, not actual mirrored component/icon/navigation layout).
- `ScreenSelector`: lets the manager choose which child/parent-facing screen's string set to preview, re-fetching preview data on change.

## 11. Required API
**Admin API** — B-04: `GET /v1/admin/locales/{code}/rtl-preview?screen=`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="localization_manager"`.

## 13. Loading / Empty / Error States
Preview loading skeleton per panel; screen-selector-changed re-fetch loading state; error state if preview data fails to load for either panel.

## 14. Responsive UI / Accessibility
Both panels labeled with clear headings ("LTR Reference (English)" / "RTL Preview (Arabic)") for screen-reader users navigating between them.

## 15. Localization / RTL
This screen's entire purpose is RTL correctness verification — the RTL panel's `dir="rtl"` is fixed and independent of the Admin Portal's own chrome locale.

## 16. Security
N/A — a read-only preview tool with no mutation path.

## 17. Testing
Unit: screen-selector re-fetch trigger logic. UI: **mandatory** — both LTR and RTL panels render simultaneously (not sequentially/exclusively) for a fixture screen/string set, confirmed by asserting both are present in the DOM at once, not merely that a toggle switches between them. Integration: full screen-selection → both-panels-update flow.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `rtl-preview.ts` schema. Files: `types/rtl-preview.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `RtlPreviewRepositoryImpl`**
Objective: Repository for B-04's preview endpoint. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `RtlPreviewComparison` with Simultaneous Dual Panels**
Objective: Two fixed-`dir` panels, both mounted at once. Dependencies: Task 02. Tests: **mandatory** — both-panels-present-simultaneously DOM test. Definition of Done: test passes.

**Task 04 — Implement `ScreenSelector`**
Objective: Screen-set selection with re-fetch on change. Dependencies: Task 02. Tests: re-fetch-on-change test. Definition of Done: test passes.

**Task 05 — Implement the RTL Preview Page**
Objective: Compose comparison + selector with loading/error states. Dependencies: Tasks 03–04. Tests: full-page smoke test. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §17, including the mandatory dual-panel test. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm no single-panel-with-toggle implementation was substituted for the required dual-panel comparison. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Both LTR and RTL panels render simultaneously, not via a toggle — mandatory DOM test passing
- [ ] Screen selector correctly re-fetches preview data for the chosen screen
- [ ] Both panels clearly labeled for accessibility
- [ ] `localization_manager` scope enforced

## 20. Definition of Done
Localization managers can genuinely verify mirrored RTL layout fidelity for Arabic/Urdu through a true side-by-side comparison before any locale-affecting change ships.
