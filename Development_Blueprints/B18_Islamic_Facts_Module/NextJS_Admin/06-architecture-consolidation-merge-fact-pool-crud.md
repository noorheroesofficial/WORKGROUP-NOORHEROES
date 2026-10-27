# N-06 — Architecture Consolidation: Merge A.2/N-04 Fact Pool CRUD into Fact Editor

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). Resolves the conflict identified during B.18's breakdown: A.2's existing "N-04" (Islamic Fact & Occasion Calendar Manager) already built full CRUD for a flat, unversioned fact pool, predating B.18's richer versioned/approval-gated schema.

**Existing Architecture → Problem → Proposed Improvement → Impact → Implementation → Documentation Update:**

- **Existing Architecture:** A.2's N-04 built CRUD for both the fact pool (text per locale/age-band, source citation, scholar-approval status) and calendar-occasion mappings (Hijri date ranges → greeting phrase keys) in a single admin surface, per its own blueprint's assumption of A.2/B-07's flat schema.
- **Problem:** B.18's N-01 now owns the canonical, versioned Fact Editor (B-06-backed). Two admin CRUD surfaces for facts would exist, and B-08's backend migration means A.2/N-04's fact-pool CRUD would be writing against a data model the child-facing API no longer reads from — a silent, high-risk content-governance gap.
- **Proposed Improvement:** N-01 (Fact Editor) becomes the sole fact-pool CRUD surface. A.2/N-04's fact-pool CRUD components/pages are removed; its navigation entry is repointed to N-01. A.2/N-04's Occasion Calendar Mapping CRUD is explicitly retained — a genuinely distinct concern.
- **Impact:** Admins get a single, correct place to manage fact content, backed by B.18's approval-gate rigor. Must land in the same release as B-08's backend cutover.
- **Implementation:** See §29 Tasks.
- **Documentation Update:** `Development_Blueprints/A2_Home_Dashboard_AI_Personalization/NextJS_Admin/04-islamic-fact-occasion-calendar-manager.md` annotated to reflect that its fact-pool CRUD responsibility has moved to B.18/N-01, retaining only Occasion Calendar Mapping.

## 2. Parent Feature
B.18 — Islamic Facts Module (cross-cutting with A.2 — Child Home Dashboard & AI Personalization)

## 3. Sub-feature
3.6 Architecture Consolidation — Merge A.2/N-04 Fact Pool CRUD (ID: N-06)

## 4. Objective
Reconcile A.2/N-04's fact-pool CRUD with B.18/N-01's canonical Fact Editor into a single implementation, retaining A.2/N-04's Occasion Calendar Mapping CRUD unchanged, and confirm the two features converge on identical file paths rather than silently competing.

## 5. Business Requirements
Rule 23 (remove genuinely redundant code, protect unrelated future-ready code). Rule 24 (explicit architecture-improvement identification). B.18 FR-5 and FR-11 (canonical, versioned fact-content ownership).

## 6. Existing Architecture
A.2's N-04: `app/(admin)/islamic-facts/page.tsx`, `app/(admin)/islamic-facts/occasions/page.tsx`, `components/islamic-facts/FactTable.tsx`, `components/islamic-facts/FactForm.tsx`, `components/islamic-facts/OccasionMappingTable.tsx`, `components/islamic-facts/OccasionMappingForm.tsx`, `lib/api/islamicFacts.ts`, `types/islamicFacts.ts`, `lib/validation/factSchema.ts`.

**Naming collision note:** A.2/N-04's file paths are **identical** to the paths B.18's own N-01/N-04/N-05 blueprints specify. This confirms these two features were always meant to converge on one implementation — the consolidation task is to ensure exactly one, canonical, B-06-backed version of each file exists, not two competing implementations at the same path.

## 7. Existing Code to Reuse
B.18's N-01 (canonical Fact Editor, backed by B-06) — the consolidation target.

## 8. Files to Create
- `tests/integration/occasion-calendar-independence.test.ts` — confirms Occasion Calendar Mapping CRUD functions correctly after the fact-pool CRUD merge, with no shared-code breakage.

## 9. Files to Modify
- Admin navigation config — ensure the "Islamic Facts" entry points to N-01's canonical pages; remove any duplicate/legacy entry if A.2/N-04 registered its own separately.
- `app/(admin)/islamic-facts/occasions/page.tsx` (A.2/N-04) — confirm this page's imports do not depend on any fact-pool-CRUD-specific code being removed; extract shared dependencies before any removal if coupling exists.
- `lib/api/islamicFacts.ts`, `types/islamicFacts.ts`, `lib/validation/factSchema.ts` — reconcile into ONE file each, containing B.18/N-01's B-06-backed implementation plus whatever occasion-mapping-specific types/functions A.2/N-04 needs preserved (e.g., `OccasionMapping` type, `getOccasionMappings()` client function) — a genuine merge, not a pick-one-and-discard operation.
- `components/islamic-facts/FactTable.tsx`, `FactForm.tsx` — B.18/N-01's versions are canonical (richer schema); A.2/N-04's versions are superseded and removed.

## 10. Backend Requirements
Fact CRUD: B-06 (canonical, per N-01). Occasion Mapping CRUD: whatever admin endpoint A.2/B-07 originally defined for calendar-occasion mappings (unchanged, confirm exact endpoint before assuming; if it doesn't exist yet, that's a gap in A.2's own blueprint to flag back to that feature, not silently invented here).

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- After reconciliation, exactly one `FactForm.tsx`/`FactTable.tsx` (B.18/N-01's, B-06-backed) and exactly one `OccasionMappingTable.tsx`/`OccasionMappingForm.tsx` (A.2/N-04's, unchanged) coexist in `components/islamic-facts/`.
- `lib/api/islamicFacts.ts` exposes both B-06's fact CRUD functions and A.2/N-04's occasion-mapping functions from a single, non-duplicated client file.
- Admin navigation shows both "Fact Editor" and "Occasion Calendar" as distinct entries (or tabs within one "Islamic Facts" section), each backed by its correct, single implementation.
- **Error State:** if an admin navigates to a stale bookmarked URL for A.2/N-04's old fact-pool page (if the path changed), redirect to N-01's canonical page, not a 404.

## 13. API Contract
Fact CRUD: B-06 (canonical, per N-01). Occasion Mapping CRUD: unchanged from A.2/B-07's original definition (confirm exact endpoint before assuming).

## 14. Database Requirements
Fact content: B-01's tables (via B-06). Occasion mappings: whatever table A.2/B-07 originally defined (unchanged; confirm exact table name — none should be needed since this is a NextJS-only consolidation).

## 15. Validation
Reconciled `factSchema.ts` must validate against B-06's actual request schema (B.18's richer version-aware fields), not A.2/N-04's original flat-schema assumptions.

## 16. Authentication
Fact CRUD and Occasion Mapping CRUD both inherit standard Admin Portal auth, unchanged.

## 17. Authorization
Fact CRUD: `content_editor` (per N-01/B-06). Occasion Mapping CRUD: whatever role A.2/N-04 originally specified (unchanged).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Reconciled API client accidentally drops an occasion-mapping function during merge | Task 03's regression test catches this before merge |
| Stale bookmarked URL for old fact-pool page | Redirect to N-01's canonical page, not a 404 |

## 19. Offline First
N/A — online-only admin surface.

## 20. Local Data
N/A.

## 21. Localization
Fact CRUD inherits N-01's handling. Occasion Mapping unchanged from A.2/N-04.

## 22. RTL
Fact CRUD inherits N-01's handling. Occasion Mapping unchanged from A.2/N-04.

## 23. Analytics
N/A.

## 24. Performance
Net reduction in duplicate code/bundle size after consolidation (one `FactForm` instead of two).

## 25. Security
Eliminates the risk of an admin unknowingly editing a fact via a code path that no longer affects what children see (the exact silent-gap risk this consolidation prevents) — this is itself a security/content-governance improvement, not merely a cleanliness one.

## 26. Library Requirements
None new — pure consolidation of existing code.

## 27. Testing
- Regression: Occasion Calendar Mapping CRUD functions correctly after the merge, with zero behavior change.
- Regression: Fact CRUD via the reconciled surface produces identical outcomes to N-01's standalone implementation.
- Integration: reconciled `lib/api/islamicFacts.ts` exposes both fact and occasion-mapping functions correctly, no function lost in the merge.
- Manual verification: no stale/duplicate `FactForm`/`FactTable` component exists anywhere in the codebase post-merge.

## 28. Documentation
Annotate `Development_Blueprints/A2_Home_Dashboard_AI_Personalization/NextJS_Admin/04-islamic-fact-occasion-calendar-manager.md` to reflect the fact-pool CRUD move; update B.18's own docs to confirm sole ownership.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Inventory Both Implementations**
Objective: Full diff of A.2/N-04's files against B.18/N-01's files at the colliding paths (§6/§9).
Why Required: Rule 30 — confirm exact overlap/divergence before merging, do not guess.
Dependencies: N-01 complete.
Definition of Done: Complete diff produced, listing every function/component that must be preserved from each side.

**Task 02 — Reconcile Shared Files**
Objective: Merge `lib/api/islamicFacts.ts`, `types/islamicFacts.ts`, `lib/validation/factSchema.ts` into single canonical versions containing B-06-backed fact functions plus preserved occasion-mapping functions.
Files to Modify: the three shared files.
Dependencies: Task 01.
Definition of Done: Single file each, no duplicate exports, both feature sets' functions present and correctly typed.

**Task 03 — Remove Superseded Fact Components, Retain Occasion Components**
Objective: Delete A.2/N-04's `FactTable.tsx`/`FactForm.tsx` if divergent from N-01's; retain `OccasionMappingTable.tsx`/`OccasionMappingForm.tsx` unchanged.
Dependencies: Task 02.
Definition of Done: Exactly one Fact CRUD implementation, occasion-mapping CRUD untouched and verified functioning.

**Task 04 — Regression Tests**
Objective: Coverage per §27.
Files to Create: `occasion-calendar-independence.test.ts`.
Dependencies: Task 03.
Definition of Done: All green.

**Task 05 — Navigation Cleanup**
Objective: Single "Islamic Facts" navigation section with correct sub-entries (Fact Editor, Occasion Calendar, Engagement Monitor), no duplicate/dead links.
Dependencies: Task 03.
Definition of Done: Navigation verified manually, no broken/duplicate entries.

**Task 06 — Documentation Update**
Objective: Annotate A.2's N-04 blueprint file to reflect the fact-pool CRUD move.
Dependencies: Task 05.
Definition of Done: Both A.2 and B.18 documentation accurately reflect final ownership.

**Task 07 — Coordinate Release Timing with B-08**
Objective: Confirm this consolidation ships in the same release as B-08's backend cutover, not before or after.
Dependencies: B-08 status.
Definition of Done: Release plan explicitly sequences N-06 and B-08 together.

## 30. Definition of Done
- Single, canonical Fact CRUD surface (N-01, B-06-backed); occasion-mapping CRUD retained unchanged.
- No duplicate/dead code at the colliding file paths.
- Regression tests confirm zero behavior change for occasion-mapping functionality.
- Coordinated release timing with B-08 to avoid a data-source-mismatch window.
- Documentation on both A.2 and B.18 sides updated.

## 31. Final Verification Checklist
- [ ] Full diff of both implementations completed before any merge decision
- [ ] Reconciled shared files contain zero duplicate exports, all functions from both sides preserved appropriately
- [ ] Exactly one Fact CRUD implementation remains (N-01's, B-06-backed)
- [ ] Occasion Calendar Mapping CRUD verified functioning, unchanged
- [ ] Navigation shows no duplicate/dead entries
- [ ] Release sequenced together with B-08 (backend cutover)
- [ ] A.2/N-04 blueprint documentation annotated
