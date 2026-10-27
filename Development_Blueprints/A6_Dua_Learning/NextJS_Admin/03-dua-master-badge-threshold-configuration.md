# N-03 — Dua Master Badge Threshold Configuration (Coordination File)

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. As established in B-05/B-10, badge threshold configuration is already owned generically by `A11_Rewards_System/NextJS_Admin/02-badge-achievement-definition-manager.md`. Per user direction this file is kept as the dedicated Dua Master record, but implements no new admin page.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
N-03 — Dua Master Badge Threshold Configuration (owned by A11's existing admin UI)

## 4. Objective
Ensure the "Dua Master" badge is configured through A11's existing `badge-achievement-definition-manager.md` screen, and record the configuration for discoverability.

## 5. Business Requirements
FR-10; Admin Requirements §8.

## 6. Existing Architecture
`A11_Rewards_System/NextJS_Admin/02-badge-achievement-definition-manager.md` — existing generic `criteria_json`-driven badge CRUD UI, presumably built on the same `BaseResourceClient`/`DataTable`/`RequirePermission` stack as N-01.

## 7. Existing Code to Reuse
A11's entire existing badge-definition manager screen.

## 8. Files to Create
None new — see B-10 §8 for the shared `docs/dua/dua_master_badge_criteria.md` reference doc.

## 9. Files to Modify
None.

## 10. Backend Requirements
None new — see B-10.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
None new.

## 13. API Contract
None owned here — see A11's real contract.

## 14. Database Requirements
None new.

## 15. Validation
Inherited from A11's existing `criteria_json` schema validation, including its non-mutating simulate/dry-run tool.

## 16. Authentication / 17. Authorization
Whatever scope A11's real screen requires — confirm before restating as fact (same correction as B-10 §17).

## 18. Error Handling / 19. Offline First / 20. Local Data / 21. Localization / 22. RTL / 23. Analytics / 24. Performance / 25. Security
N/A — all inherited from A11's existing, already-hardened screen.

## 26. Library Requirements
None.

## 27. Testing
Confirm A11's simulate/dry-run tool correctly previews the configured Dua Master thresholds without writing real data — the one thing worth verifying from A.6's side.

## 28. Documentation
`docs/dua/dua_master_badge_criteria.md` (shared with B-05/B-10).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Configure via A11's Existing UI**
Task ID: N-03-T01. Objective: a scope-appropriate admin configures the Dua Master badge through A11's real screen. Definition of Done: badge visible in A11's list, simulate tool confirms expected behavior.

**Task 02 — Verify Simulate Tool**
Task ID: N-03-T02. Definition of Done: dry-run confirmed accurate per §27.

**Task 03 — Final Review**
Task ID: N-03-T03. Definition of Done: §31 checklist fully checked; confirm no duplicate admin page was built.

## 30. Definition of Done
Dua Master badge fully configured through A11's existing screen; no duplicate NextJS admin page built for A.6.

## 31. Final Verification Checklist
- [ ] No new NextJS admin page created for this concern
- [ ] Configuration done via A11's real `badge-achievement-definition-manager.md` screen
- [ ] Thresholds documented in the shared `docs/dua/dua_master_badge_criteria.md`
- [ ] Simulate/dry-run tool verified accurate

## 32. Addendum — What Changed From the Original Draft
The original draft built a bespoke `product_admin`-restricted ordered-list settings form. Per explicit user direction the file is kept, but its content now correctly points at A11's existing generic badge-definition admin screen, which already provides this capability with a dry-run simulator the original draft lacked.
