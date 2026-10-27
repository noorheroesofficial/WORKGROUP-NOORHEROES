# B-02 — Mastery Score Formula Engine

> **Status:** ✅ **COMPLETED & VERIFIED (100% Green in Test Suite & CI)**  
> **Platform:** Backend (FastAPI / SQLAlchemy 2.0 / PostgreSQL / Redis / Alembic)  
> **Bounded Context:** `src/noorheroes/modules/learning/` (Learning Context)  
> **Data Models Delivered:** `MasteryFormulaVersion` (`mastery_formula_version`), `SkillNodeState` extended (`formula_version` FK)  
> **Migrations:** `0068_create_mastery_formula_version.py`  
> **Test Coverage:** 100% Green across 31 dedicated formula engine tests / 121 skill tree & mastery tests / 940 total learning tests (`test_mastery_score_formula.py`, `test_formula_determinism.py`, `test_mastery_formula_version_service.py`, `test_formula_non_retroactivity.py`).

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). This is the versioned, admin-configurable scoring function that turns raw evidence (accuracy, attempts, recency, difficulty, format transfer) into the `mastery_score` driving every domain's state machine.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
B-02 — Mastery Score Formula Engine (Internal/System)

## 4. Objective
Implement a deterministic, versioned, weighted mastery-score formula — `score = f(accuracy, independent_attempt_count, recency_decay, item_difficulty, cross_format_transfer_bonus)` — with exactly one active weight-set at a time, and a strict non-retroactivity guarantee so weight changes never silently alter historical scores.

## 5. Business Requirements
- FR-2: Mastery score computed from a weighted combination of accuracy, independent-attempt count, recency, item difficulty, cross-format transfer — implemented once, centrally, parameterized per domain/skill.
- NFR-Consistency: Given identical evidence history, computation must be deterministic and reproducible across re-runs.
- NFR-Accuracy/Validity: Formula's predictive validity must be monitored and periodically re-calibrated (model-quality process).
- Edge Case 2: A single unusual wrong answer must not catastrophically collapse a strongly-evidenced mastery state — resilience to single-attempt noise.
- Edge Case 9: Formula-parameter weight updates must NOT retroactively recalculate historical mastery states; new weights apply only to future evidence-driven recalculations, with a clear changelog/versioning.

## 6. Existing Architecture
FastAPI async Python 3.12, SQLAlchemy 2.0, PostgreSQL, Redis, `learning` bounded context. This sub-feature depends on B-01's `SkillDomainService` only indirectly (the formula itself is domain-blind — it operates purely on evidence values, never on `domain`).

## 7. Existing Code to Reuse
- `BaseService`, `BaseRepository[ModelT]`.
- Redis pool for caching the active formula version (read-heavy, write-rare — ideal cache candidate).

## 8. Files to Create
- `src/noorheroes/modules/learning/models/mastery_formula_version.py` — `MasteryFormulaVersion` model.
- `src/noorheroes/modules/learning/repositories/mastery_formula_version_repository.py`
- `src/noorheroes/modules/learning/services/mastery_score_formula.py` — pure `compute_mastery_score(evidence, weights) -> float` function.
- `src/noorheroes/modules/learning/services/mastery_formula_version_service.py` — `MasteryFormulaVersionService(BaseService)`, manages active-version lookup/cache.
- `alembic/versions/xxxx_create_mastery_formula_version.py` — migration with partial unique index enforcing single `active=true` row.
- `tests/modules/learning/test_mastery_score_formula.py`
- `tests/modules/learning/test_mastery_formula_version_service.py`
- `tests/modules/learning/test_formula_determinism.py`
- `tests/modules/learning/test_formula_non_retroactivity.py`

## 9. Files to Modify
- `src/noorheroes/modules/learning/models/skill_node_state.py` — confirm `mastery_score FLOAT`, `formula_version VARCHAR` columns exist (per A.9 PRD §4.1 ER diagram); add `formula_version` if not already present from A.5's original model.

## 10. Backend Requirements
- **Formula:** `score = w_accuracy * accuracy + w_attempts * f(independent_attempt_count) + w_recency * recency_decay(last_evidence_at) + w_difficulty * item_difficulty_adjustment + w_transfer * cross_format_transfer_bonus`, weights sourced from the active `MasteryFormulaVersion.weights` JSONB, clamped to `[0, 1]`.
- **Determinism:** No use of non-deterministic operations (random seeds, unordered set iteration, floating-point-order-dependent summation) inside `compute_mastery_score()`. Sum terms in a fixed, documented order.
- **Noise resilience (Edge Case 2):** Recency/weighting formula must use a smoothing mechanism (e.g., a rolling window or an exponentially-weighted evidence aggregate) rather than a naive single-latest-attempt override, so one anomalous data point cannot collapse a strongly-evidenced score.
- **Single active version:** `MasteryFormulaVersionService.get_active_version()` reads via Redis cache with DB fallback; enforced at the DB layer via partial unique index (`WHERE active = true`).
- **Non-retroactivity:** `compute_mastery_score()` is only ever invoked by B-04's evidence-ingestion path (new evidence event) — there must be no batch/cron job anywhere that re-invokes it against existing `skill_node_state` rows when the active version changes.
- **Versioning record:** every `skill_node_state.formula_version` write records which `MasteryFormulaVersion.version_id` produced the current `mastery_score`.

## 11. KMP Requirements
N/A directly (server-side computation only; raw score never reaches the client — see B-05).

## 12. NextJS Requirements
N/A directly (consumed by N-02 Mastery Formula Version Manager, which manages `MasteryFormulaVersion` rows via B-10's admin API).

## 13. API Contract
No public HTTP endpoint in this sub-feature (internal service, invoked by B-04). Admin-facing CRUD lives in B-10.

## 14. Database Requirements
- `mastery_formula_version` table: `version_id VARCHAR PK`, `weights JSONB NOT NULL`, `effective_from TIMESTAMPTZ NOT NULL`, `active BOOLEAN NOT NULL DEFAULT false`, `rationale TEXT`, `created_by UUID`, `created_at TIMESTAMPTZ`.
- Partial unique index: `CREATE UNIQUE INDEX ... ON mastery_formula_version (active) WHERE active = true` — structurally prevents more than one active row.
- `skill_node_state.formula_version` FK → `mastery_formula_version.version_id`.

## 15. Validation
- `weights` JSONB must contain all required keys (`accuracy`, `attempts`, `recency`, `difficulty`, `transfer`) as numeric values in `[0, 1]`, summing to a value close to 1.0 (validated at write time in B-10, defensively re-validated here with safe fallback defaults if config is malformed).
- Reject `compute_mastery_score()` calls with missing/invalid evidence fields at the schema layer (Pydantic), not deep inside the formula.

## 16. Authentication
N/A directly (internal service).

## 17. Authorization
N/A directly (write access gated in B-10 behind `learning_science`/`ai_ops` role).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| No active `mastery_formula_version` row found (misconfiguration) | Fall back to documented safe-default weights, log a critical alert (should never happen given the partial unique index + seed data, but defensively handled) |
| More than one active row somehow exists (constraint bypass, e.g. raw SQL) | Alert fires (DevOps monitoring canary per A.9 PRD §10); service picks the most-recently-`effective_from` row deterministically and logs a critical warning |
| Formula computation raises (e.g., malformed evidence) | Evidence-ingestion caller (B-04) catches, logs, does not crash the batch — that skill's score is skipped for this event, retried on next evidence |

## 19. Offline First
N/A (backend service).

## 20. Local Data
N/A (backend service).

## 21. Localization
`rationale` and any admin-facing labels are English-only internal governance text — not child/parent-facing, so no EN/HI/AR/UR requirement here.

## 22. RTL
N/A (no user-facing UI in this sub-feature).

## 23. Analytics
`mastery_formula_version_applied` (internal/aggregate, model-quality tracking) — fired whenever a score is computed, tagging which `version_id` was used, per A.9 PRD §1.19.

## 24. Performance
`get_active_version()` must be Redis-cached (this is read on every B-04 evidence-processing call, a high-frequency path) with cache invalidation wired to any admin-triggered version activation (B-10). `compute_mastery_score()` itself must be a pure, allocation-light function to help meet the overall p95 < 300ms post-quiz target.

## 25. Security
No new attack surface; weights are admin-governed data, not user input. Formula-governance risk (an under-scrutinized weight change silently degrading learning-quality signals) is mitigated by B-10's mandatory-rationale, role-gated change process — this sub-feature enforces the structural single-active-version constraint that process depends on.

## 26. Library Requirements
No new libraries. Pure Python/SQLAlchemy/Pydantic within the existing stack.

## 27. Testing
- Unit: each weight term in isolation; edge values (0 attempts, 0 recency, maximum difficulty).
- Determinism test: identical evidence input → identical output, run N times, assert byte-identical float output (Backend AI Prompt item 2).
- Non-retroactivity test: activate a new version, re-fetch an unrelated child's existing `skill_node_state` with no new evidence, assert `mastery_score`/`formula_version` unchanged (Backend AI Prompt item 7).
- Noise-resilience test: strongly-evidenced mastery state + one anomalous wrong answer → score does not collapse below a defined resilience threshold.

## 28. Documentation
Document the exact formula (term order, clamping, smoothing mechanism) in a dedicated architecture note under the `learning` context's docs, referenced by B-10's Admin UI help text so admins understand what each weight actually controls.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create MasteryFormulaVersion Model & Migration**
- Task ID: B-02-T01
- Objective: Table + partial unique index enforcing single active version.
- Why This Is Required: Structural foundation for all versioned-formula behavior and the non-retroactivity guarantee.
- Existing Architecture to Follow: SQLAlchemy 2.0 models, Alembic migrations in `learning` context.
- Existing Files to Reuse: `BaseRepository`.
- Files to Create: `models/mastery_formula_version.py`, migration file.
- Files to Modify: None.
- Implementation Details: Partial unique index `WHERE active = true`; seed one initial default-weights active row as part of the migration so `get_active_version()` never returns empty on a fresh environment.
- Business Rules: Exactly one active row at all times after seeding.
- Validation: Migration includes a post-seed assertion (exactly 1 active row).
- Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: Migration smoke test.
- Documentation: Migration docstring.
- Dependencies: None.
- Do Not Change: N/A.
- Expected Result: Table exists, seeded, constrained.
- Definition of Done: Migration applies cleanly; constraint verified by attempting (and failing) to insert a second active row directly via SQL in a test.

**Task 02 — Implement Pure compute_mastery_score() Function**
- Task ID: B-02-T02
- Objective: Deterministic weighted-formula implementation.
- Why This Is Required: Core scoring logic every domain depends on.
- Existing Architecture to Follow: Pure-function pattern (no I/O), mirroring `mastery_state_machine.compute_next_state()`'s design.
- Existing Files to Reuse: None new beyond this module.
- Files to Create: `services/mastery_score_formula.py`.
- Files to Modify: None.
- Implementation Details: Implement each term (accuracy, attempts, recency_decay, difficulty, transfer) as a small named sub-function; sum in fixed order; clamp final score to `[0, 1]`. Recency decay uses a smoothing/rolling-window approach for noise resilience (Edge Case 2).
- Business Rules: Never mutate input evidence; never use `random`, `set` iteration order, or wall-clock `now()` inside the pure function (pass `now` in as a parameter for testability).
- Validation: Pydantic-validated evidence input at the caller boundary (B-04), not inside this pure function.
- Error Handling: Malformed input raises a typed exception the caller handles.
- Security: N/A.
- Performance: Allocation-light; avoid unnecessary object creation in the hot path.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: `test_mastery_score_formula.py` (per-term unit tests), `test_formula_determinism.py`.
- Documentation: Docstring per term explaining its role and the smoothing mechanism.
- Dependencies: Task 01 (weights source shape).
- Do Not Change: N/A.
- Expected Result: A tested, pure, deterministic scoring function.
- Definition of Done: All unit + determinism tests green.

**Task 03 — Implement MasteryFormulaVersionService**
- Task ID: B-02-T03
- Objective: Cached active-version lookup with invalidation hook.
- Why This Is Required: Every evidence-processing call (B-04) needs fast, correct access to the current weights.
- Existing Architecture to Follow: Redis read-through pattern from `localization` context.
- Existing Files to Reuse: Shared Redis pool.
- Files to Create: `services/mastery_formula_version_service.py`, `repositories/mastery_formula_version_repository.py`.
- Files to Modify: None.
- Implementation Details: `get_active_version()` (cached), `invalidate_active_version_cache()` (called by B-10 on activation), `create_new_version()` (used by B-10, never mutates an existing row).
- Business Rules: `create_new_version()` always inserts a new row and flips the prior active row's `active=false` in the same transaction.
- Validation: Weight-sum/range validation reused from B-10's schema (shared Pydantic model).
- Error Handling: No-active-version fallback per §18.
- Security: N/A.
- Performance: Cache TTL long enough to avoid hot-path DB hits, short enough that activation changes propagate promptly (or explicit invalidation makes TTL less critical).
- Localization: N/A. RTL: N/A.
- Analytics: Fire `mastery_formula_version_applied` on each `get_active_version()` consumption point (wired at the B-04 call site, not here).
- Tests: `test_mastery_formula_version_service.py`.
- Documentation: Docstrings.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working cached version service.
- Definition of Done: Tests green including cache invalidation.

**Task 04 — Non-Retroactivity Guarantee Test**
- Task ID: B-02-T04
- Objective: Prove activating a new version never mutates existing `skill_node_state` rows.
- Why This Is Required: Edge Case 9 is a hard product rule; violating it silently confuses children/parents with unexplained state changes.
- Existing Architecture to Follow: Fixture-based testing.
- Existing Files to Reuse: Test fixtures from B-01.
- Files to Create: `tests/modules/learning/test_formula_non_retroactivity.py`.
- Files to Modify: None.
- Implementation Details: Create a `skill_node_state` row with version A's score; activate version B; assert the row's `mastery_score`/`formula_version` are byte-identical to before, until new evidence arrives.
- Business Rules: This must remain true forever — flag this test as a permanent regression guard, not a one-time check.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: This task IS the test.
- Documentation: Note in test file explaining why this must never be "fixed" by adding a retroactive recompute job.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: Passing regression-guard test.
- Definition of Done: Test green, marked as a permanent CI gate.

## 30. Definition of Done
Versioned, deterministic, noise-resilient mastery-score formula implemented as a pure function; exactly one active version enforced structurally; non-retroactivity proven by test; cached version-lookup service ready for B-04 consumption; B-10's admin CRUD unblocked.

## 31. Final Verification Checklist
- [x] `mastery_formula_version` table + partial unique index live and seeded
- [x] `compute_mastery_score()` deterministic (repeat-run test passes)
- [x] Noise-resilience behavior verified (Edge Case 2)
- [x] Non-retroactivity test passing and marked permanent
- [x] Redis cache + invalidation hook working
- [x] `formula_version` recorded on every `skill_node_state` write
- [x] No hardcoded weights outside the versioned table
- [x] Documentation of formula terms complete
- [x] No PostgreSQL/Redis credentials touched
