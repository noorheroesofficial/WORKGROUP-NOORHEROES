# N-02 — Dua Recall Question Authoring (Coordination File)

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. Mirrors B-09's backend-side finding: `A8_Daily_Quiz_Engine/NextJS_Admin/01-quiz-question-bank-management.md` likely already provides generic admin question CRUD. This file's scope is downstream of B-09's ownership decision.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
N-02 — Dua Recall Question Authoring (likely owned by A8's admin UI, consumed/configured by A.6)

## 4. Objective
If B-09 confirms A8's generic question-bank admin UI is reused, this file's scope shrinks to: adding a `dua_recall`-scoped filter/view into that existing screen (per its own `NextJS_Admin/01` design) and, if not already generic, a soft (non-blocking) >3-questions warning specific to dua's brevity guidance. If B-09 instead concludes a dua-scoped table is genuinely needed, this file reverts to a dedicated builder UI.

## 5. Business Requirements
FR-6 (soft 1–3 question guideline).

## 6. Existing Architecture
Pending B-09's resolution. `A8_Daily_Quiz_Engine/NextJS_Admin/01-quiz-question-bank-management.md` and `02-pre-publish-preview-version-history.md` are the likely real, existing screens this integrates with.

## 7. Existing Code to Reuse
Pending B-09 — likely A8's existing `QuestionResourceClient`/`useQuestionList` (or real equivalent names, confirm against A8's actual NextJS_Admin files) rather than a new `DuaResourceClient` question sub-resource.

## 8. Files to Create
Pending B-09's resolution — see that file for the decision point.

## 9. Files to Modify
If reusing A8: coordinate a `source_type=dua_recall` filter option into A8's existing admin screen. If dua-scoped: extend N-01's `DuaEditorPage` with a nested question-builder tab.

## 10. Backend Requirements
Per B-09.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
Soft warning banner (reusing whatever generic warning/alert component the admin portal already has, not inventing one) when a dua exceeds 3 questions — a UI-layer concern once the underlying count (wherever it lives) is accurate.

## 13. API Contract
Per B-09 §13.

## 14. Database Requirements
N/A (frontend).

## 15. Validation
Inherits A8's existing question-authoring validation if the bank is shared.

## 16. Authentication / 17. Authorization
Whatever scope/permission A8's real admin question CRUD requires.

## 18. Error Handling / 19. Offline First / 20. Local Data / 21. Localization / 22. RTL
Inherited from A8's existing screen if reused.

## 23. Analytics / 24. Performance / 25. Security
N/A directly.

## 26. Library Requirements
None new.

## 27. Testing
- Integration: create a `dua_recall`-scoped question via whichever screen B-09 resolves to own → confirm it correctly appears in B-03's `total_available` count

## 28. Documentation
Record B-09's ownership decision here too.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Apply B-09's Ownership Decision**
Task ID: N-02-T01. Objective: implement this file's scope per B-09's finalized decision. Definition of Done: this file's §8/§9/§13 updated to match, not left as placeholder branches.

**Task 02 — Implement Per Task 01's Branch**
Task ID: N-02-T02. Definition of Done: question authoring functional end-to-end for dua content.

**Task 03 — Add Tests**
Task ID: N-02-T03. Definition of Done: integration test per §27 green.

**Task 04 — Final Code Review**
Task ID: N-02-T04. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
Question authoring for duas functional, correctly attributed to whichever system B-09 determined owns it, no duplicate implementation.

## 31. Final Verification Checklist
- [ ] B-09's ownership decision applied consistently here
- [ ] No duplicate question-authoring UI if A8's is reused
- [ ] Soft warning banner reuses an existing generic component, not invented
- [ ] Count correctly reflected in B-03's `total_available`

## 32. Addendum — What Changed From the Original Draft
The original draft built a bespoke nested question-builder UI. This file is now explicitly downstream of B-09's ownership decision (A8's likely-existing generic question-bank admin screen vs. a genuinely dua-scoped one), avoiding a second, slightly-different authoring UI alongside a possibly-existing one.
