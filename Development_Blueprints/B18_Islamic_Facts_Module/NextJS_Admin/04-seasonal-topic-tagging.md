# N-04 — Seasonal Topic Tagging

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). A small addition to the Fact Editor form (N-01) enabling admins to tag facts as seasonally relevant, feeding B-02's seasonal-weighting selection logic.

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
3.4 Seasonal Topic Tagging (ID: N-04)

## 4. Objective
Add a multi-select seasonal-relevance field (Ramadan, Eid al-Fitr, Eid al-Adha, etc.) to the Fact Editor form, persisted as part of the fact/version payload and consumed by B-02's seasonal-weighting logic.

## 5. Business Requirements
- FR-10: facts surfaced during an active seasonal mode are weighted toward seasonally-relevant topics where available, without hard-excluding non-seasonal facts.
- §8: Seasonal Topic Tagging — part of the Fact Editor's form, `content_editor` role.

## 6. Existing Architecture
A field within N-01's `FactForm.tsx`, not a standalone page — per the PRD's own framing ("part of the Fact Editor form").

## 7. Existing Code to Reuse
- N-01's existing form infrastructure and multi-select component pattern (reuse the platform's existing multi-select UI component, do not build a new one).
- Existing seasonal-mode enum/registry, if the platform already defines Ramadan/Eid values elsewhere (A.2's occasion calendar, A.36 Ramadan Mode) — reuse that exact enum rather than defining a parallel one.

## 8. Files to Create
None standalone — this is additive to N-01's existing files.

## 9. Files to Modify
- `components/islamic-facts/FactForm.tsx` (N-01) — add the seasonal multi-select field.
- `types/islamicFacts.ts` (N-01) — add `seasonalTags: SeasonalTag[]` to the fact/version type.
- `lib/validation/factSchema.ts` (N-01) — add validation for the new field.

## 10. Backend Requirements
Consumes B-06's fact create/update endpoints, extended to accept `seasonal_tags` as part of the version payload (confirm this field is included in B-06's request schema; coordinate a B-06 addition if not yet present).

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Component:** multi-select field on `FactForm.tsx`, options sourced from the platform's existing seasonal-mode enum (Ramadan, Eid al-Fitr, Eid al-Adha, and any others already defined — confirm exact list, do not invent additional values).
- **Form/Validation:** no hard validation forcing a selection — a fact may have zero seasonal tags (general/evergreen fact), consistent with FR-10's "without hard-excluding non-seasonal facts" principle; values restricted to the platform's registered seasonal-mode enum, arbitrary free-text tags not permitted (prevents typos/fragmentation in the weighting logic's lookup).
- **Loading/Empty/Error States:** inherits N-01's form-level handling entirely — no distinct states for this single field.

## 13. API Contract
Field addition to B-06's existing `POST/PUT /v1/admin/facts...` request/response payloads: `"seasonal_tags": ["ramadan", "eid_al_fitr"]`. No new endpoint.

## 14. Database Requirements
Adds to a dedicated `seasonal_tags` jsonb/array column on `fact_version` (B-01) — confirm exact column decision with B-01's implementation before this field can be wired end-to-end; if B-01 didn't include this column, flag as a required B-01 schema addition (coordination dependency, not a silent assumption).

## 15. Validation
Values restricted to the platform's registered seasonal-mode enum; arbitrary free-text tags not permitted.

## 16. Authentication
Inherits N-01's standard Admin Portal auth.

## 17. Authorization
Inherits N-01's `content_editor` role gating entirely — no separate permission for this field.

## 18. Error Handling
Standard form-field validation error if an invalid/unregistered tag value is somehow submitted (shouldn't be reachable via the multi-select UI itself, but validated as a backstop).

## 19. Offline First
N/A — online-only admin surface.

## 20. Local Data
N/A.

## 21. Localization
Seasonal tag labels ("Ramadan," "Eid al-Fitr") localized per the Admin Portal's supported locale for the admin UI chrome itself.

## 22. RTL
N/A beyond standard admin chrome handling — tag labels are short enum-backed strings, not user-authored RTL content.

## 23. Analytics
N/A.

## 24. Performance
Negligible — a small enum-backed multi-select, no additional API calls beyond the existing fact save.

## 25. Security
N/A beyond N-01's existing role gating.

## 26. Library Requirements
N-01's existing multi-select component — no new libraries.

## 27. Testing
- Unit: multi-select correctly persists selected tags into the form payload.
- Unit: zero-selection (no seasonal tags) is a valid, non-blocking state.
- Integration: saved seasonal tags correctly round-trip through B-06 and are visible in B-02's seasonal-weighting behavior (cross-reference B-02's own seasonal-fallback test).

## 28. Documentation
Note in N-01's component documentation that `FactForm.tsx` includes this field, sourced from the platform's single seasonal-mode enum.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm B-01 Schema Support**
Objective: Verify `fact_version` has a column for seasonal tags; if absent, flag as a coordination dependency back to B-01 rather than silently working around it.
Dependencies: B-01 implementation status.
Definition of Done: Confirmed column exists or a tracked follow-up is created.

**Task 02 — Confirm Seasonal-Mode Enum Source**
Objective: Identify the platform's existing seasonal-mode enum (A.2/A.36) rather than defining a new one.
Dependencies: None (research task).
Definition of Done: Single source of truth confirmed.

**Task 03 — Add Field to Fact Editor**
Objective: Multi-select field in `FactForm.tsx`.
Files to Modify: `FactForm.tsx`, `types/islamicFacts.ts`, `factSchema.ts`.
Dependencies: Task 01, Task 02, N-01 complete.
Definition of Done: Field functions correctly, persists via existing save flow.

**Task 04 — Tests**
Dependencies: Task 03.
Definition of Done: All green.

## 30. Definition of Done
- Seasonal tagging field integrated into N-01's existing form, no standalone page.
- Reuses the platform's single existing seasonal-mode enum.
- Correctly round-trips through B-06/B-01 and feeds B-02's weighting logic.

## 31. Final Verification Checklist
- [ ] Field reuses existing platform seasonal-mode enum, no duplicate definition
- [ ] Zero-selection is valid (non-seasonal facts not excluded)
- [ ] B-01 schema support confirmed (or flagged as a coordination dependency)
- [ ] Saved tags verified to correctly influence B-02's seasonal-weighting behavior end-to-end
