# K-06 — Architecture Consolidation: Migrate A.5/K-11 Fact Detail into `:feature:facts`

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). Resolves the conflict identified during B.18's breakdown: A.5's existing "K-11" (Islamic Fact Detail & Mastery Celebration) already built a Fact Detail screen inside `feature-learn`, bundled with an unrelated Mastery Celebration modal.

## 2. Parent Feature
B.18 — Islamic Facts Module (cross-cutting with A.5 — Quran & Arabic Learning)

## 3. Sub-feature
2.6 Architecture Consolidation — Migrate A.5/K-11 Fact Detail (ID: K-06)

## 4. Existing Architecture → Problem → Proposed Improvement → Impact → Implementation → Documentation Update

**Existing Architecture:** A.5's K-11 renders Islamic Fact Detail inside `feature-learn`, sourced from "the `content` context's existing content-detail fetch pattern" (per its own blueprint, written before B.18's canonical `FactDetailScreen`/B-03 contract existed) — and bundles an unrelated Mastery Celebration modal in the same file.

**Problem:** Two Fact Detail screens would exist in the codebase (`feature-learn`'s and `:feature:facts`'s K-01) if both are built independently, violating Rule 23 and B.18's own ownership claim (FR-5). `feature-learn`'s version predates B.18's approval-gated, versioned contract and would silently diverge.

**Proposed Improvement:** `:feature:facts`'s K-01 becomes the sole Fact Detail implementation. A.5's `feature-learn` entry points that currently launch K-11's fact detail are repointed to deep-link into `:feature:facts` (K-05) instead. A.5/K-11's Mastery Celebration modal — a genuinely distinct, unrelated concern — is explicitly retained in place, not touched.

**Impact:** Lesson/quiz content in `feature-learn` that links to an Islamic Fact continues to work identically for the child, now backed by B.18's richer, approval-gated data model. A.5's blueprint documentation requires a follow-up annotation.

**Implementation:** See Tasks below.

**Documentation Update:** `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/11-islamic-fact-detail-mastery-celebration.md` annotated to reflect that its fact-detail responsibility has moved to B.18/K-01, retaining only the Mastery Celebration modal — file renamed or content updated per team convention (recommend renaming to `11-mastery-celebration.md` in a follow-up, out of scope for this blueprint's file-write step to avoid breaking existing cross-references without coordination).

## 5. Business Requirements
Rule 23 (remove genuinely redundant code, protect unrelated future-ready code). Rule 24 (explicit architecture-improvement identification). B.18 FR-5 (canonical fact-content/detail ownership).

## 6. Existing Architecture
A.5's `feature-learn` module: `IslamicFactDetailScreen.kt` + ViewModel, `GetIslamicFactUseCase.kt`, `MasteryCelebrationModal.kt` — per A.5/K-11's own Files to Create list.

## 7. Existing Code to Reuse
B.18's K-01 (`FactDetailScreen`, `FactDetailViewModel`) — the consolidation target, already built by this point in the execution sequence. K-05's deep-link routing.

## 8. Files to Create
- `tests/integration/test_learn_tab_fact_link_regression.md` equivalent test file: `feature-learn/src/commonTest/kotlin/.../LearnFactLinkRegressionTest.kt` — confirms lesson/quiz content linking to a fact still resolves correctly post-migration.

## 9. Files to Modify
- A.5's `feature-learn` — wherever lesson/quiz content currently navigates to `IslamicFactDetailScreen` (A.5/K-11), repoint to deep-link `noorheroes://facts/{fact_id}` (K-05) instead.
- `LearnRoute` (per A.5/K-11's own "Files to Modify" list) — remove the `IslamicFactDetail` destination registration if it duplicates `:feature:facts`'s route, retaining only the celebration-trigger wiring.

## 10. Files to Deprecate/Remove (after verification)
- `feature-learn/.../facts/IslamicFactDetailScreen.kt` + its ViewModel.
- `feature-learn-domain/.../GetIslamicFactUseCase.kt`.
- **Retain unchanged:** `feature-learn/.../celebration/MasteryCelebrationModal.kt` and K-01's own `SkillTreeViewModel` mastery-transition-detection logic (A.5/K-11 §11) — this is a distinct concern (skill-node mastery events), not fact content, and remains fully in scope for A.5.

## 11. KMP Requirements
- Confirm no other A.5 screen depends on `IslamicFactDetailScreen`'s specific ViewModel state shape before removal (grep-verify across `feature-learn`).
- `SkillTreeViewModel`'s mastery-transition-detection → `MasteryCelebrationModal` trigger logic is entirely independent of fact content and requires zero changes.
- Regression-test lesson/quiz content that links to an Islamic Fact still resolves correctly, now via `:feature:facts`'s K-01/K-05.

## 12. NextJS Requirements
N/A directly — coordinates conceptually with N-06 (which performs the equivalent consolidation on the backend/admin side) but this is a client-only migration.

## 13. API Contract
No new contract — A.5's `feature-learn` now consumes B.18's B-03 contract (via K-01) instead of whatever content-detail endpoint A.5/K-11 originally assumed.

## 14. Database Requirements
None — client-side only; no local Room schema change beyond what K-03 already introduces.

## 15. Validation
Grep-verify (Task 01 below) that no other A.5 code references `IslamicFactDetailScreen`/`GetIslamicFactUseCase` before deletion — an automated safety check, not a manual assumption.

## 16. Authentication / 17. Authorization
Unchanged — inherits `:feature:facts`'s existing child-session auth once migration completes.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| A.5 code still references the old screen after removal | Compile failure surfaces immediately (intentional — safer than a silent runtime gap) |
| Deep-link repoint fails to resolve a fact reachable from a lesson | Regression test (Task 03) catches this before merge |

## 19-22. Offline/Local Data/Localization/RTL
Inherits `:feature:facts`'s K-01/K-03 handling entirely once migrated — no separate offline/localization/RTL work needed here.

## 23. Analytics
Confirm `fact_detail_viewed`-equivalent events previously fired by A.5/K-11 (if any existed) are not double-counted or lost after migration — `:feature:facts`'s K-01 analytics become the sole source.

## 24. Performance
No new performance concern; removes a duplicate screen implementation, net reduction in app size/maintenance surface.

## 25. Security
No new attack surface; reduces duplicate code paths, lowering overall risk of divergent security handling (e.g., one screen enforcing the approval gate correctly, another not).

## 26. Library Requirements
None new.

## 27. Testing
- Automated reference check: no remaining imports of `IslamicFactDetailScreen`/`GetIslamicFactUseCase` anywhere in `feature-learn` after removal.
- Regression test: lesson/quiz content linking to an Islamic Fact resolves correctly via the new deep-link path.
- Confirm `MasteryCelebrationModal` and `SkillTreeViewModel`'s mastery-detection logic are entirely unaffected (still function, no accidental removal).

## 28. Documentation
Annotate `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/11-islamic-fact-detail-mastery-celebration.md` to reflect the fact-detail portion has moved to B.18/K-01; the file's celebration-modal content remains accurate as-is.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Reference Audit**
Objective: Grep the full `feature-learn` module (and any consumer) for references to `IslamicFactDetailScreen`, its ViewModel, and `GetIslamicFactUseCase`.
Why Required: Rule 30 — do not guess at blast radius; confirm before removing.
Dependencies: None (first task, research-only).
Definition of Done: Complete list of every reference site produced.

**Task 02 — Repoint Lesson/Quiz Fact Links**
Objective: Update every reference site found in Task 01 to deep-link into `:feature:facts` (K-05) instead of A.5/K-11's screen.
Files to Modify: Each reference site identified.
Dependencies: Task 01, K-01, K-05 complete.
Definition of Done: All reference sites navigate correctly to `:feature:facts`'s Fact Detail.

**Task 03 — Regression Test**
Objective: Confirm lesson/quiz-linked fact navigation works identically post-repoint.
Files to Create: `LearnFactLinkRegressionTest.kt`.
Dependencies: Task 02.
Definition of Done: Test green.

**Task 04 — Remove Duplicate Screen Code**
Objective: Delete `IslamicFactDetailScreen.kt`, its ViewModel, `GetIslamicFactUseCase.kt`.
Do Not Change: `MasteryCelebrationModal.kt`, `SkillTreeViewModel`'s mastery-detection logic.
Dependencies: Task 03 passing (no remaining references, regression verified).
Definition of Done: Code compiles cleanly with zero references remaining; celebration modal still functions.

**Task 05 — Documentation Annotation**
Objective: Update A.5/K-11's blueprint file.
Dependencies: Task 04.
Definition of Done: Blueprint accurately reflects final ownership split.

## 30. Definition of Done
- Single Fact Detail implementation across the app (`:feature:facts`'s K-01).
- All A.5 lesson/quiz fact links verified working via the consolidated screen.
- Mastery Celebration modal and skill-tree mastery-detection logic fully preserved, untouched.
- Zero dangling references to the removed screen.
- Documentation on the A.5 side annotated.

## 31. Final Verification Checklist
- [ ] Reference audit completed before any deletion
- [ ] All lesson/quiz fact-detail entry points repointed and regression-tested
- [ ] `IslamicFactDetailScreen`/`GetIslamicFactUseCase` removed with zero remaining references
- [ ] `MasteryCelebrationModal` and mastery-detection logic fully unaffected
- [ ] A.5's blueprint documentation annotated to reflect final ownership
- [ ] No duplicate Fact Detail implementation remains anywhere in the codebase
