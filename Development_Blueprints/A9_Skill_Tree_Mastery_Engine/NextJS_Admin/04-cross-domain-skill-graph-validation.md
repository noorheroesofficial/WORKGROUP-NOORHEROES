# N-04 — Cross-Domain Skill Graph Validation

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). Extends A.5's existing Curriculum Builder cycle-detection validator (frontend error-surfacing side) so a cross-domain prerequisite cycle rejected by B-11's backend validation is clearly communicated to the admin, with the specific cycle path shown, inside the existing save flow — no new page.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
N-04 — Cross-Domain Skill Graph Validation (Extension of Existing Curriculum Builder Save Flow)

## 4. Objective
Update A.5's existing Curriculum Builder save-flow error handling to correctly render B-11's cross-domain cycle-rejection response (including cross-domain node references in the cycle path, e.g., `quran:node_1 → arabic:node_7 → quran:node_1`), replacing any assumption that a cycle only ever involves nodes from the same domain.

## 5. Business Requirements
- Admin AI Code-Generation Prompt (A.9 PRD §9) item 2: "extend the existing cycle-detection validator... to run across ALL domains' combined prerequisite graph... No new page needed — this is a backend validation-logic extension surfaced through the existing Curriculum Builder save flow."
- Error Handling table: cross-domain prerequisite graph cycle rejected at admin-save time with the cycle path shown.

## 6. Existing Architecture
React + TypeScript Admin Portal. A.5's existing Curriculum Builder (`01-skill-tree-curriculum-builder.md`) already has a save flow with cycle-detection error handling for single-domain cycles — this sub-feature is a targeted extension of that existing error-display logic, not a new feature surface.

## 7. Existing Code to Reuse
- A.5's existing Curriculum Builder save-flow error-handling component/logic — locate and extend, do not duplicate.
- A.5's existing cycle-path visualization (if one exists — e.g., a breadcrumb-style path display) — extend it to render cross-domain node references clearly (e.g., prefixing each node with its domain when the path spans more than one domain).

## 8. Files to Create
- `__tests__/admin/curriculum-builder/CrossDomainCycleError.test.tsx`

## 9. Files to Modify
- A.5's Curriculum Builder save-flow error-handling component — extend cycle-path rendering to handle cross-domain node references clearly (e.g., show each node's domain alongside its label when the cycle spans multiple domains).
- A.5's Curriculum Builder's prerequisite-selection UI (if it currently only offers same-domain nodes as prerequisite options) — extend the prerequisite-node picker to allow selecting nodes from any registered domain (via N-01's domain registry as the source of selectable domains), consistent with B-01's cross-domain prerequisite support.

## 10. Backend Requirements
N/A (consumes B-11's extended cycle-detection validator via the existing curriculum-save endpoint).

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Cycle-path rendering:** when a cycle-rejection response includes nodes from more than one domain, the error display clearly shows each node's domain (e.g., "Quran: Ayah 3 → Arabic: Letter Alif → Quran: Ayah 3"), not just raw node IDs or domain-agnostic labels that could confuse an admin about where the cycle actually crosses domain boundaries.
- **Prerequisite picker cross-domain support:** if the existing prerequisite-selection UI in A.5's Curriculum Builder currently restricts the picker to the node's own domain, extend it to allow selecting prerequisite nodes from any active domain (sourced from N-01's registry) — this is what makes cross-domain prerequisites (Edge Case 11) actually usable by an admin, not just theoretically supported by the backend.
- **No new page:** this sub-feature modifies existing Curriculum Builder components in place.

## 13. API Contract
Consumes the existing Curriculum Builder save endpoint's error response, extended by B-11 to include a `cycle_path` array of `{ domain, node_id, label }` (or equivalent) when a cycle is detected.

## 14. Database Requirements
N/A (frontend only).

## 15. Validation
Client-side cannot fully replicate cross-domain cycle detection (that's inherently a server-side graph computation) — client-side validation here is limited to basic self-reference prevention (a node cannot list itself as its own prerequisite), with the authoritative cycle check always happening server-side via B-11.

## 16. Authentication
Reuses existing Curriculum Builder auth/session context.

## 17. Authorization
Part of the existing `curriculum_editor` role's tooling — no new role/permission introduced.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Cross-domain cycle detected on save | Save rejected, cycle path rendered clearly with domain labels per §12 |
| Large combined graph causes a validation timeout (per B-11 §18) | Error message surfaced clearly ("graph too large to validate, contact engineering"), not a generic/confusing failure |
| Prerequisite picker shows a cross-domain node the admin then removes/changes | Standard form-state handling, no special case needed |

## 19. Offline First
N/A (admin web app).

## 20. Local Data
N/A.

## 21. Localization
Per N-01 §21's platform-wide Admin Portal localization scope decision.

## 22. RTL
Per N-01 §22's decision.

## 23. Analytics
N/A.

## 24. Performance
No new performance concerns beyond what A.5's existing Curriculum Builder already handles; cross-domain prerequisite picker's node list may be larger (spanning multiple domains) — ensure the picker remains searchable/filterable rather than becoming an unwieldy flat list.

## 25. Security
No new attack surface; extends existing `curriculum_editor`-gated tooling.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Component test: cycle-path error display correctly renders a cross-domain path with clear domain labeling.
- Component test: prerequisite picker allows selecting nodes from a domain other than the node's own.
- Regression test: existing A.5 single-domain cycle-detection error display still renders correctly (unchanged for the single-domain case).

## 28. Documentation
Update A.5's Curriculum Builder documentation to note the prerequisite picker and cycle-error display are now cross-domain-aware.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend Cycle-Path Error Rendering for Cross-Domain Paths**
- Task ID: N-04-T01
- Objective: Clear, domain-labeled cycle-path display.
- Why This Is Required: An admin cannot fix a cross-domain cycle they can't understand; raw node IDs or domain-agnostic labels would be confusing/unusable.
- Existing Architecture to Follow: A.5's existing cycle-error display component.
- Existing Files to Reuse: That component, extended in place.
- Files to Create: `CrossDomainCycleError.test.tsx`.
- Files to Modify: A.5's cycle-error display component.
- Implementation Details: Render each cycle-path entry with its domain label alongside the node label; visually distinguish domain transitions in the path if helpful (e.g., a small domain badge per step).
- Business Rules: N/A. Validation: N/A. Error Handling: This IS the error-handling improvement.
- Security: N/A. Performance: N/A.
- Localization: Per decision. RTL: Per decision. Analytics: N/A.
- Tests: This task IS the primary test target.
- Documentation: Component comment.
- Dependencies: B-11.
- Do Not Change: The underlying cycle-detection algorithm (backend concern, B-11).
- Expected Result: Clear cross-domain cycle error display.
- Definition of Done: Test passes for both single-domain (regression) and cross-domain cycle paths.

**Task 02 — Extend Prerequisite Picker to Cross-Domain Node Selection**
- Task ID: N-04-T02
- Objective: Let admins actually select cross-domain prerequisites, not just receive errors about them.
- Why This Is Required: Without this, cross-domain prerequisite support (B-01/B-11) is backend-only and unreachable from the actual admin workflow — a half-finished feature.
- Existing Architecture to Follow: A.5's existing prerequisite-selection UI.
- Existing Files to Reuse: That component, extended; N-01's domain registry as the source of available domains.
- Files to Create: None (extend existing test suite).
- Files to Modify: A.5's prerequisite-picker component.
- Implementation Details: Remove any same-domain-only filter on the picker's node list; add domain grouping/filtering in the picker UI to keep a larger cross-domain node list navigable (search/filter by domain).
- Business Rules: N/A. Validation: Basic self-reference prevention client-side.
- Error Handling: Server-side cycle check remains authoritative (Task 01).
- Security: N/A. Performance: Searchable/filterable list for larger combined node sets.
- Localization: Per decision. RTL: Per decision. Analytics: N/A.
- Tests: Component test confirming cross-domain nodes are selectable.
- Documentation: Component comment.
- Dependencies: N-01, B-01.
- Do Not Change: N/A.
- Expected Result: Fully usable cross-domain prerequisite selection.
- Definition of Done: Test passes; manual verification that a Quran node can select an Arabic node as a prerequisite through the actual UI.

## 30. Definition of Done
A.5's existing Curriculum Builder correctly surfaces cross-domain cycle-rejection errors with clear, domain-labeled paths, and its prerequisite picker allows genuinely selecting cross-domain prerequisite nodes — completing the admin-usable half of B-01/B-11's cross-domain prerequisite support, with zero new page and zero regression to existing single-domain behavior.

## 31. Final Verification Checklist
- [ ] Cross-domain cycle-path error clearly shows domain labels per step
- [ ] Existing single-domain cycle-error display unregressed
- [ ] Prerequisite picker allows selecting nodes from any active domain, not just the node's own
- [ ] Picker remains navigable/searchable with a larger cross-domain node list
- [ ] No new page created (extension of existing Curriculum Builder save flow only)
- [ ] `curriculum_editor` role scope unchanged (no new role introduced)
