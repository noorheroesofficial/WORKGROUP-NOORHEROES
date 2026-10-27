# N-03 — Segment Builder

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). A filter-builder UI for age band, locale, plan tier, and engagement-state criteria, sourced from existing Analytics segment data — never displaying or exporting raw individual child identities, only aggregate segment size estimates (PRD §9 item 3).

## 2. Parent Feature
B.17 Notifications (Child-Facing) — NextJS Admin

## 3. Sub-feature
N-03 Segment Builder

## 4. Objective
Build the Segment Builder component (embedded within N-02's Campaign Scheduler) allowing an admin to filter a target audience by age band, locale, plan tier, and engagement state, showing only an aggregate size estimate.

## 5. Business Requirements
- Filter by age band, locale, plan tier, engagement state, sourced from existing Analytics segment data (PRD §9 item 3).
- Never display or export raw individual child identities — only aggregate segment size estimates (PRD §9 item 3, §12.6 data-exposure mitigation).
- Same role as Campaign Scheduler's tooling (`notification_manager`/`content_editor`) since it is part of that flow (PRD §8).

## 6. Existing Architecture
- Embedded as a sub-component within N-02's campaign creation wizard, not a standalone top-level page (PRD §9 item 3 frames it as "part of Campaign Scheduler's tooling").
- Sourced from B-07's `POST /v1/admin/notifications/segments/estimate` endpoint.
- Follows `NEXT-JS-INSTRUCTIONS.md` form-component conventions.

## 7. Existing Code to Reuse
- Existing Admin Portal filter-builder UI patterns, if any exist elsewhere (e.g., in analytics/reporting sections) — reuse rather than build a bespoke filter UI from scratch.

## 8. Files to Create
- `components/notifications/SegmentFilterBuilder.tsx`.
- `components/notifications/SegmentEstimateDisplay.tsx`.
- `lib/api/notifications/segments.ts` — API client.
- `lib/types/notifications.ts` — extend with `SegmentFilters`, `SegmentEstimate`.
- `tests/notifications/SegmentFilterBuilder.test.tsx`.

## 9. Files to Modify
- N-02's `campaigns/new/page.tsx` — embed `SegmentFilterBuilder` in the segment-configuration step.

## 10. Backend Requirements
Consumes B-07's `POST /v1/admin/notifications/segments/estimate` exactly as documented.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Component: filter builder for age band, locale, plan tier, engagement state (multi-select/range controls as appropriate per criterion).
- Component: aggregate estimate display (count only, never a list).
- API Client: typed wrapper over B-07's segment-estimate endpoint.
- Type Definition: `SegmentFilters`, `SegmentEstimate`.
- Form/Validation: at least one filter criterion recommended (not strictly required — an unfiltered "all families" segment may be a valid, intentional choice, subject to server-side confirmation/warning).
- Authentication/Authorization: same as N-02 (`notification_manager`/`content_editor`).
- Loading/Empty/Error States: loading spinner while estimate recalculates on filter change; "0 recipients match" empty state; error state on API failure.
- Testing: filter-combination → correct estimate-request → correct display flow.

## 13. API Contract
Consumes B-07 §13's segment-estimate contract: `POST /v1/admin/notifications/segments/estimate` with filter payload, returning an aggregate count only.

## 14. Database Requirements
N/A (frontend only).

## 15. Validation
Filter criteria combine with AND logic; the UI must never construct a request that could return individual-level data — only the documented aggregate-estimate contract is called.

## 16. Authentication
Admin session via existing Admin Portal auth context.

## 17. Authorization
Same role gate as N-02 (`notification_manager`/`content_editor`).

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| Segment resolves to zero matches | "0 recipients match these filters" state, non-blocking |
| API failure fetching estimate | Error state with retry, does not block filter editing |
| Filter combination changes rapidly (debounced) | Debounce re-estimate calls to avoid excessive API traffic |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Locale is itself one of the filter criteria (a data value being filtered on), distinct from the admin's own UI locale.

## 22. RTL
Standard portal RTL support if the admin's own UI locale is AR/UR.

## 23. Analytics
Not applicable directly.

## 24. Performance
Debounce estimate recalculation on filter change (e.g., 300–500ms) to avoid excessive API calls while an admin is actively adjusting filters.

## 25. Security
This component must never render or fetch raw child-identity data under any circumstance — verified via a contract test asserting the API client only ever calls the aggregate-estimate endpoint, never any child-listing endpoint (PRD §12.6).

## 26. Library Requirements
Next.js (App Router), TypeScript, React, existing Admin Portal component library.

## 27. Testing
- Unit: filter-state → correct API request payload construction.
- Integration: filter change → debounced estimate call → correct display update.
- Security: **mandatory** — assert the component never calls or renders any endpoint/data shape containing individual child identities.
- Edge case: zero-match segment renders the correct empty state.

## 28. Documentation
Document the "aggregate-only, never individual identities" constraint prominently in `SegmentFilterBuilder.tsx`'s comments.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Types & API Client**
- Files to Create: `lib/types/notifications.ts` extension, `lib/api/notifications/segments.ts`.

**Task 02 — Implement SegmentFilterBuilder Component**
- Files to Create: `SegmentFilterBuilder.tsx`.
- Implementation Details: multi-select/range controls per criterion (age band, locale, plan tier, engagement state).
- Tests: filter-state test.

**Task 03 — Implement Debounced Estimate Fetching**
- Files to Modify: `SegmentFilterBuilder.tsx`.
- Performance: debounce per §24.
- Tests: debounce-behavior test.

**Task 04 — Implement SegmentEstimateDisplay**
- Files to Create: `SegmentEstimateDisplay.tsx`.
- Implementation Details: aggregate count display, zero-match empty state.
- Tests: display-state tests.

**Task 05 — Embed into N-02's Campaign Wizard**
- Files to Modify: N-02's `campaigns/new/page.tsx`.
- Definition of Done: filter selections correctly flow into the campaign creation payload.

**Task 06 — Add Security Contract Test**
- Objective: Prove no individual-identity data path exists.
- Why Required: PRD §12.6, non-negotiable privacy guarantee.
- Tests: mandatory contract test.

**Task 07 — Write Full Test Suite & Documentation**
- Tests: per §27.
- Documentation: per §28.

## 30. Definition of Done
- Filter builder correctly constructs and combines all four criteria.
- Estimate display shows aggregate counts only, verified by the mandatory security contract test.
- Correctly embedded within N-02's campaign creation flow.

## 31. Final Verification Checklist
- [ ] All four filter criteria (age band, locale, plan tier, engagement state) function correctly and combine with AND logic
- [ ] Estimate display shows an aggregate count only — no individual child identity ever rendered or fetched
- [ ] Zero-match segment shows a clear, non-blocking empty state
- [ ] Estimate recalculation is debounced to avoid excessive API traffic
- [ ] Correctly embedded within N-02's campaign creation wizard
- [ ] Full test suite passes, including the mandatory no-individual-identity security test
