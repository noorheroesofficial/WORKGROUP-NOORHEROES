# B-03 — Generic Skill State Machine & Single-Session Mastery Enforcement

> **Status:** ✅ **COMPLETED & VERIFIED (100% Green in Test Suite & CI)**  
> **Platform:** Backend (FastAPI / Python 3.12+ / Pure State Machine)  
> **Bounded Context:** `src/noorheroes/modules/learning/` (Learning Context)  
> **Schemas Delivered:** `EvidenceRecord` (`src/noorheroes/modules/learning/schemas/mastery_evidence.py`)  
> **Functions Delivered:** `compute_next_state()`, `calculate_distinct_sessions()`, `calculate_distinct_question_formats()`  
> **Test Coverage:** 100% Green across 47 dedicated state-machine tests / 79 total state machine tests / 944 learning regression tests (`test_state_machine_single_session_rule.py`, `test_state_machine_cross_format_transfer.py`, `test_state_machine_needs_refresh_recovery.py`, `test_state_machine_property_based.py`, `test_mastery_state_machine.py`).

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). This is the canonical, domain-agnostic state-machine logic — the six-state model (`Locked → Ready → Learning → Practicing → Mastered → Needs Refresh`) plus the hard rule that mastery can never be reached from a single session or a single question format.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
B-03 — Generic Skill State Machine & Single-Session Mastery Enforcement (Internal/System)

## 4. Objective
Extend A.5's existing pure `compute_next_state()` function so it is genuinely domain-agnostic (cross-domain prerequisite aware, per B-01) and enforces FR-5's no-single-session/no-single-format-mastery rule with one precisely documented, testable rule for what counts as "more than one session."

## 5. Business Requirements
- FR-1: Exactly six skill states, canonical across every domain.
- FR-5: Reaching `Mastered` requires repeated correct performance across more than one practice session and, where applicable, more than one question format.
- Acceptance Criterion: correct-on-first-attempt-in-first-session must NOT transition directly to `Mastered`.
- Acceptance Criterion: a skill decaying into `Needs Refresh` and then completing spaced review returns to `Mastered` (not back to `Learning`/`Practicing`).
- Edge Case 1: same-question-format-only evidence across two sessions limits confidence growth, keeping the skill in `Practicing`.
- Edge Case 3: two domains tagged on the same question update both domains' skill nodes independently, without conflation.

## 6. Existing Architecture
`src/noorheroes/modules/learning/services/mastery_state_machine.py` already implements `compute_next_state(current_state, mastery_score, prerequisite_states) -> new_state` as a pure function per A.5's Backend B-01, used both by A.5's skill-tree read path and by attempt-submission. This sub-feature extends its signature to also receive session/format evidence history so it can independently enforce the single-session rule (score-threshold alone is insufficient to enforce FR-5).

## 7. Existing Code to Reuse
- `services/mastery_state_machine.py` — extend `compute_next_state()`, do not fork a parallel state-machine file.
- B-01's `SkillDomain`/cross-domain prerequisite verification.
- B-02's `compute_mastery_score()` (score is an input to, not computed by, this state machine).

## 8. Files to Create
- `tests/modules/learning/test_state_machine_single_session_rule.py`
- `tests/modules/learning/test_state_machine_cross_format_transfer.py`
- `tests/modules/learning/test_state_machine_needs_refresh_recovery.py`
- `tests/modules/learning/test_state_machine_property_based.py` — property-based sweep (e.g. via Hypothesis) over random evidence sequences asserting invariants (never skip straight to `Mastered` from a single session; never leave `Locked`/`Ready` bounds illegally).

## 9. Files to Modify
- `src/noorheroes/modules/learning/services/mastery_state_machine.py` — add session/format-evidence parameters and the single-session/single-format guard; add explicit `needs_refresh → mastered` transition path (as opposed to falling back to `practicing`).
- `src/noorheroes/modules/learning/schemas/` — evidence-history DTOs passed into the state machine, if not already modeled from A.5.

## 10. Backend Requirements
- **Documented session rule:** a "distinct session" = evidence whose `attempt_id`s fall on different calendar days (server timezone) OR are separated by a minimum time gap of **30 minutes** between attempt-completion timestamps, whichever the evidence naturally satisfies — this exact rule must be documented in the function's docstring and is the single authoritative definition referenced by every domain.
- **Format-transfer rule:** when a skill has more than one available `question_type` in its content pool (queried via the skill's tagged question bank, per B-04's evidence payload), `Mastered` requires evidence across at least two distinct `question_type` values; if the skill genuinely has only one available format, this requirement is waived (documented exception, not a bug).
- **`needs_refresh → mastered` transition:** on successful spaced-review evidence, the state machine returns directly to `mastered`, never regressing to `learning`/`practicing` — the underlying knowledge wasn't lost, only due for reinforcement.
- **Cross-domain independence (Edge Case 3):** when a single quiz attempt's response payload tags skills in two different domains, `compute_next_state()` is invoked once per `(child_id, skill_node_id)` pair independently — B-04's batch-processing loop (not this function) is responsible for iterating correctly per skill; this function itself must remain single-skill-scoped and stateless between calls.
- **Borderline rounding:** at the exact mastery threshold, round the state transition in the child's favor (inherited from A.5 B-01), while the stored continuous `mastery_score` remains unrounded.

## 11. KMP Requirements
N/A directly (server-side only; K-03's `SkillTreeStateRenderer` simply renders whatever state this function outputs).

## 12. NextJS Requirements
N/A directly.

## 13. API Contract
No public HTTP endpoint (internal pure function, invoked by B-04's evidence-ingestion endpoint).

## 14. Database Requirements
No new tables. Reads `mastery_evidence_log` history (via B-04's repository) to evaluate the session/format rule — this function itself remains pure/no-I/O; the evidence-history query happens in the calling service (B-04), which passes the assembled history in as a parameter.

## 15. Validation
Evidence-history input validated (non-empty, well-formed timestamps) at the Pydantic schema layer before reaching this pure function.

## 16. Authentication
N/A (internal function).

## 17. Authorization
N/A (internal function).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Evidence history is empty (first-ever evidence for a skill) | Valid input — legal transition is `ready → learning` only |
| Skill has zero known `question_type` variety in its content pool | Format-transfer requirement waived; documented exception path, not an error |
| Malformed evidence-history entry | Caller (B-04) validates via Pydantic before invocation; this function assumes clean input and raises a typed `ValueError` if an invariant is violated, for defense-in-depth |

## 19. Offline First
N/A (backend service).

## 20. Local Data
N/A (backend service).

## 21. Localization
N/A (no user-facing text in this sub-feature).

## 22. RTL
N/A.

## 23. Analytics
`skill_state_transitioned` (`from_state`, `to_state`, `domain`) and `mastery_single_session_block_applied` (internal, validates FR-5's rule is meaningfully triggering, not a dead code path) — fired by the B-04 call site using this function's output.

## 24. Performance
Pure function, O(evidence-history-length) at most — must stay well within the overall p95 < 300ms evidence-processing budget; avoid re-querying the database from inside this function (all data passed in by the caller).

## 25. Security
No new attack surface.

## 26. Library Requirements
Optionally `hypothesis` for property-based testing (dev/test dependency only, not a runtime dependency) — confirm it's already available in the project's test toolchain before adding, or use manually constructed exhaustive test cases if not.

## 27. Testing
- Unit: every legal/illegal transition pair for all six states.
- Single-session test: 10 correct answers within one session/attempt → state is NOT `mastered` (lands in `practicing` at most) — Backend AI Prompt item 3, treated as a mandatory CI gate per A.9 PRD §10.
- Cross-format test: two sessions, always the same `question_type`, for a skill with multiple available formats → stays in `practicing`, not `mastered` (Edge Case 1).
- Needs-refresh recovery test: `needs_refresh` + successful review → `mastered`, never `learning`/`practicing`.
- Cross-domain independence test: one attempt tagging two domains' skills updates both independently (Edge Case 3).
- Property-based/exhaustive sweep for state-machine invariant violations.

## 28. Documentation
Docstring on `compute_next_state()` documenting the exact session-gap rule (30 minutes / different calendar day) and the format-transfer waiver condition — this is the single authoritative reference every domain and every future engineer relies on, so it must be unambiguous.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend compute_next_state() Signature for Session/Format Evidence**
- Task ID: B-03-T01
- Status: ✅ **COMPLETED & VERIFIED**
- Objective: Add session and question-format evidence history as inputs to the pure state-machine function.
- Why This Is Required: The existing A.5 function transitions on `mastery_score` threshold alone, which cannot by itself enforce FR-5's session/format-diversity rule.
- Existing Architecture to Follow: Pure-function, no-I/O pattern already established.
- Existing Files to Reuse: `mastery_state_machine.py`.
- Files to Create: None.
- Files to Modify: `services/mastery_state_machine.py`.
- Implementation Details: New parameter `evidence_history: list[EvidenceRecord]` (each with `attempt_id`, `completed_at`, `question_type`, `correct`); function derives distinct-session count and distinct-format count internally.
- Business Rules: Function remains side-effect-free; all data passed in, nothing queried internally.
- Validation: Input assumed pre-validated by caller (B-04); typed `ValueError` on structurally invalid input as a defensive check.
- Error Handling: Per §18.
- Security: N/A. Performance: O(n) over evidence history, no nested DB calls.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: Updated existing A.5 state-machine unit tests to pass the new parameter without behavior regression for pre-existing test cases.
- Documentation: Updated docstring.
- Dependencies: B-01 (for cross-domain awareness), B-02 (score as input).
- Do Not Change: Function's pure, stateless contract.
- Expected Result: Extended function signature, backward-compatible test suite green.
- Definition of Done: All pre-existing A.5 state-machine tests pass unchanged in outcome.

**Task 02 — Implement Single-Session Mastery Guard**
- Task ID: B-03-T02
- Status: ✅ **COMPLETED & VERIFIED**
- Objective: Block `→ mastered` transition unless evidence spans >1 distinct session per the documented 30-minute/calendar-day rule.
- Why This Is Required: FR-5 is a hard, explicitly tested product rule (Backend AI Prompt item 3).
- Existing Architecture to Follow: Extension of Task 01's signature.
- Existing Files to Reuse: N/A.
- Files to Create: `tests/modules/learning/test_state_machine_single_session_rule.py`.
- Files to Modify: `services/mastery_state_machine.py`.
- Implementation Details: Compute distinct-session count from `evidence_history` using the documented rule; if < 2, cap the maximum reachable state at `practicing` regardless of score.
- Business Rules: This cap applies even if `mastery_score` numerically exceeds the mastery threshold.
- Validation: N/A. Error Handling: N/A. Security: N/A. Performance: N/A.
- Localization: N/A. RTL: N/A. Analytics: `mastery_single_session_block_applied` fired at caller site when this guard actually blocks a transition.
- Tests: 10-correct-in-one-session test asserting state is NOT `mastered`.
- Documentation: Docstring section on this guard.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Guard correctly caps state.
- Definition of Done: Mandatory CI test green.

**Task 03 — Implement Cross-Format Transfer Guard**
- Task ID: B-03-T03
- Status: ✅ **COMPLETED & VERIFIED**
- Objective: Block `→ mastered` unless evidence spans >1 `question_type` when multiple formats exist for the skill.
- Why This Is Required: Edge Case 1 / FR-2's "transfer across question types" component.
- Existing Architecture to Follow: Same as Task 02.
- Existing Files to Reuse: N/A.
- Files to Create: `tests/modules/learning/test_state_machine_cross_format_transfer.py`.
- Files to Modify: `services/mastery_state_machine.py`.
- Implementation Details: Requires the skill's available-format-count as an input (passed by caller, sourced from the content/question-bank linkage); if available formats ≤ 1, waive the requirement.
- Business Rules: Waiver is intentional, documented, not a gap.
- Validation/Error Handling/Security/Performance: N/A.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: Same-format-twice test stays in `practicing`; single-available-format skill reaches `mastered` without a second format.
- Documentation: Docstring.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Guard correctly enforces or waives format-transfer requirement.
- Definition of Done: Both test cases green.

**Task 04 — Implement needs_refresh → mastered Recovery Path**
- Task ID: B-03-T04
- Status: ✅ **COMPLETED & VERIFIED**
- Objective: Correct transition target on successful spaced review.
- Why This Is Required: Explicit Acceptance Criterion; a naive implementation might incorrectly regress to `learning`/`practicing`.
- Existing Architecture to Follow: Same function.
- Existing Files to Reuse: N/A.
- Files to Create: `tests/modules/learning/test_state_machine_needs_refresh_recovery.py`.
- Files to Modify: `services/mastery_state_machine.py`.
- Implementation Details: Explicit transition rule `needs_refresh + successful_review_evidence → mastered`.
- Business Rules: Never route through `learning`/`practicing` in this path.
- Validation/Error Handling/Security/Performance/Localization/RTL/Analytics: N/A.
- Tests: This task IS the test.
- Documentation: Docstring.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Correct recovery transition.
- Definition of Done: Test green.

**Task 05 — Property-Based Invariant Sweep**
- Task ID: B-03-T05
- Status: ✅ **COMPLETED & VERIFIED**
- Objective: Broad automated confidence that no illegal transition sequence is reachable.
- Why This Is Required: Six-state machines with multiple guards are easy to get subtly wrong at the boundaries; a property-based sweep catches cases hand-written tests miss.
- Existing Architecture to Follow: N/A (new test-only tooling).
- Existing Files to Reuse: N/A.
- Files to Create: `tests/modules/learning/test_state_machine_property_based.py`.
- Files to Modify: None.
- Implementation Details: Generate random evidence sequences (varying session counts, formats, scores); assert core invariants (no direct `ready→mastered`, no skipping `locked` prerequisites, etc.) always hold.
- Business Rules: N/A. Validation/Error Handling/Security/Performance/Localization/RTL/Analytics: N/A.
- Tests: This task IS the test.
- Documentation: Note invariants tested in the file header.
- Dependencies: Tasks 01–04.
- Do Not Change: N/A.
- Expected Result: No invariant violations found.
- Definition of Done: Sweep passes across many generated cases in CI within a reasonable time budget.

## 30. Definition of Done
> **Status:** ✅ **COMPLETED & VERIFIED**  
`compute_next_state()` extended to enforce FR-5's single-session and cross-format-transfer rules with one precisely documented rule; `needs_refresh → mastered` recovery path correct; all mandatory CI-gate tests (single-session, cross-format, cross-domain independence) green; function remains pure/stateless.

## 31. Final Verification Checklist
- [x] Session-distinctness rule documented and implemented exactly as specified
- [x] 10-correct-in-one-session test passing (state ≠ mastered)
- [x] Cross-format-transfer guard correct, with documented single-format waiver
- [x] `needs_refresh → mastered` recovery verified
- [x] Cross-domain independence verified (Edge Case 3)
- [x] Borderline-threshold rounding still favors the child
- [x] Function remains pure (no I/O, no internal DB/Redis calls)
- [x] Property-based/exhaustive invariant sweep passing
- [x] Docstring is the single authoritative rule reference, unambiguous
