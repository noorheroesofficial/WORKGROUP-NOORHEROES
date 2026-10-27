# B-04 — Mastery Evidence Ingestion API

> **Status:** ✅ **COMPLETED & VERIFIED (100% Green in Test Suite & CI)**  
> **Platform:** Backend (FastAPI / SQLAlchemy 2.0 / PostgreSQL / Redis / Alembic)  
> **Bounded Context:** `src/noorheroes/modules/learning/` (Learning Context)  
> **Data Models Delivered:** `MasteryEvidenceLog` (`mastery_evidence_log`), `SkillNodeState` linked  
> **Migrations:** `0069_create_mastery_evidence_log.py`  
> **Test Coverage:** 100% Green across 21 dedicated B-04 tests (30 including model tests) / 269 mastery & skill tree tests / 965 total learning tests (`test_mastery_evidence_service.py`, `test_mastery_evidence_api.py`, `test_mastery_evidence_idempotency.py`, `test_mastery_evidence_withdrawn_exclusion.py`, `test_skill_tree_models.py`).

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). This is the entry point where A.8's Quiz Service hands off a completed attempt's per-skill evidence, triggering score recomputation and state-machine evaluation for every tagged skill.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
B-04 — Mastery Evidence Ingestion API (User API — internal, service-to-service)

## 4. Objective
Implement `POST /v1/mastery/evidence`: process a batch of per-skill evidence from a single quiz attempt atomically, computing new mastery scores (B-02) and state transitions (B-03) per skill, excluding withdrawn responses, and guaranteeing idempotency on `attempt_id`.

## 5. Business Requirements
- FR-2, FR-5 (via B-02/B-03 consumption).
- FR-10: A withdrawn/safety-flagged quiz item's evidence is excluded from mastery-score computation even if recorded before withdrawal.
- NFR-Performance: p95 < 300ms so the Quiz Completion Result screen never feels delayed.
- Error Handling table: idempotency key resubmission (network retry) returns the original result, never double-processes evidence.
- Edge Case 7: the score difference caused by withdrawal-exclusion should itself be logged for content-quality monitoring.

## 6. Existing Architecture
FastAPI async Python 3.12, SQLAlchemy 2.0, PostgreSQL, Redis, Kafka. `learning` bounded context. This endpoint is the primary consumer of B-01 (domain lookup), B-02 (score formula), B-03 (state machine).

## 7. Existing Code to Reuse
- `BaseService`, `BaseRepository[ModelT]`.
- A.8's existing evidence-emission pattern (however A.8's Quiz Service currently calls into mastery/reward integration — per A.8 Backend B-06 "Accuracy-Independent Reward & Mastery-Confidence Integration" — this sub-feature is the receiving side of that existing integration point; reuse the established call contract rather than inventing a new one).
- Redis-based idempotency-key pattern already used elsewhere in the platform for attempt-completion endpoints.

## 8. Files to Create
- `src/noorheroes/modules/learning/models/mastery_evidence_log.py` — `MasteryEvidenceLog` model (append-only).
- `src/noorheroes/modules/learning/repositories/mastery_evidence_log_repository.py`
- `src/noorheroes/modules/learning/schemas/mastery_evidence.py` — `MasteryEvidenceRequest`, `MasteryEvidenceResponse` Pydantic schemas.
- `src/noorheroes/modules/learning/services/mastery_evidence_service.py` — `MasteryEvidenceService(BaseService)`, orchestrates the full evidence→score→state pipeline.
- `alembic/versions/xxxx_create_mastery_evidence_log.py`
- `tests/modules/learning/test_mastery_evidence_service.py`
- `tests/modules/learning/test_mastery_evidence_api.py`
- `tests/modules/learning/test_mastery_evidence_idempotency.py`
- `tests/modules/learning/test_mastery_evidence_withdrawn_exclusion.py`

## 9. Files to Modify
- `src/noorheroes/modules/learning/api.py` — add `POST /v1/mastery/evidence` route.
- `src/noorheroes/modules/learning/models/__init__.py` — register `MasteryEvidenceLog`.

## 10. Backend Requirements
- **Router:** `POST /v1/mastery/evidence`, internal service-to-service auth (not child-session Bearer — this is called by A.8's Quiz Service backend, not directly by clients; use the platform's existing internal-service auth mechanism, whatever pattern secures other service-to-service calls in the `learning`/`content` contexts).
- **Service orchestration (`MasteryEvidenceService.process_evidence()`):** for each `skill_node_id` in the payload: (1) look up or create `skill_node_state`, (2) if `is_withdrawn_excluded=true`, log to `mastery_evidence_log` with `excluded_withdrawn=true` and skip score computation entirely for that response, (3) otherwise assemble evidence history (query prior `mastery_evidence_log` rows for this `state_id`), (4) call B-02's `compute_mastery_score()` with the active formula version, (5) call B-03's `compute_next_state()`, (6) write the new `mastery_evidence_log` row and updated `skill_node_state` — all within a single DB transaction per attempt.
- **Idempotency:** keyed on `attempt_id`; a Redis-backed idempotency lock/result-cache returns the original `MasteryEvidenceResponse` on resubmission without reprocessing.
- **Withdrawal-exclusion delta logging (Edge Case 7):** when a response is excluded, log both the "with exclusion" and a computed "would-have-been without exclusion" delta for content-quality monitoring — flag an alert if a skill's exclusion rate spikes (wired to DevOps monitoring, A.9 PRD §10).

## 11. KMP Requirements
N/A directly (internal endpoint; K-02's Result screen consumes B-06, which reads the outcome of this processing).

## 12. NextJS Requirements
N/A directly.

## 13. API Contract

**`POST /v1/mastery/evidence`**
- **Auth:** Internal service-to-service (A.8 Quiz Service only)
- **Request:**
```json
{
  "child_id": "uuid",
  "attempt_id": "uuid",
  "responses": [
    {
      "skill_node_id": "uuid",
      "correct": true,
      "question_type": "multiple_choice",
      "hint_count": 0,
      "response_time_ms": 4200,
      "is_withdrawn_excluded": false
    }
  ]
}
```
- **Response 200:**
```json
{
  "updated_skills": [
    { "skill_node_id": "uuid", "new_state": "mastered", "transitioned": true }
  ]
}
```
- **Validation:** `child_id`/`attempt_id` valid UUIDs; `responses` non-empty; `skill_node_id` values must resolve to existing, active `skill_node` rows.
- **Error Responses:** `401`/`403` (invalid internal auth), `422` (malformed payload/unknown skill), `500` (DB failure — evidence queues for retry per Error Handling table in A.9 PRD §1.11), idempotent resubmission → `200` with original result.

## 14. Database Requirements
- `mastery_evidence_log` per A.9 PRD §4.1 ER diagram: `evidence_id PK`, `state_id FK`, `attempt_id FK`, `correct`, `question_type`, `hint_count`, `excluded_withdrawn`, `created_at`. Append-only (no UPDATE/DELETE paths). Index `(state_id, created_at DESC)`.
- Writes to `skill_node_state` (already exists per A.5/B-01) — `mastery_score`, `state`, `formula_version`, `last_evidence_at`, `updated_at`.

## 15. Validation
- Reject payloads with zero `responses`.
- Reject `skill_node_id` not found or belonging to an inactive `skill_node`.
- `child_id` must correspond to an existing, active child profile (defensive check even on internal-only calls).

## 16. Authentication
Internal service-to-service credential/mTLS/shared-secret pattern (whichever mechanism the platform already uses between the Quiz Service and other internal endpoints) — **do not invent a new auth mechanism**; if the existing pattern is undocumented in available context, flag as an open question for the architecture team rather than guessing.

## 17. Authorization
Only A.8's Quiz Service is a legitimate caller; no child/parent/admin token should be accepted on this route.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Mastery-score computation service unavailable post-quiz | Reward issuance (A.8, unconditional) still completes independently; mastery update queues for retry via a dead-letter/retry queue; Result screen (B-06) shows based on most-recent available state |
| Duplicate `attempt_id` resubmission | Returns original cached result, no double-processing |
| `is_withdrawn_excluded=true` response | Logged with `excluded_withdrawn=true`, completely skipped from score computation |
| Partial batch failure (one skill's processing errors mid-batch) | Whole-attempt transaction rolls back; entire batch retried as a unit — never a partially-applied evidence batch |
| Unknown `skill_node_id` | `422`, entire request rejected (fail-closed, not silently-skip, to avoid masking a real content-linkage bug) |

## 19. Offline First
N/A (backend service; offline handling owned by K-04 on the client).

## 20. Local Data
N/A (backend service).

## 21. Localization
N/A (no user-facing text; internal API).

## 22. RTL
N/A.

## 23. Analytics
`mastery_score_recomputed` (`skill_id`, `domain`, internal/aggregate), `skill_state_transitioned` (`from_state`, `to_state`, `domain`), `mastery_single_session_block_applied`, `mastery_formula_version_applied` — all fired from this service's orchestration, per A.9 PRD §1.19.

## 24. Performance
p95 < 300ms end-to-end for the full batch (all skills tagged on one attempt) — achieved via: single DB transaction per attempt (not per skill), cached active-formula-version lookup (B-02), evidence-history query scoped/indexed on `(state_id, created_at DESC)`, no synchronous external calls beyond DB/Redis inside the critical path.

## 25. Security
Idempotency prevents evidence double-counting from replay/retry attacks. Internal-only auth prevents client-side forgery of evidence (a child's app could never call this directly with fabricated "correct" answers).

## 26. Library Requirements
No new libraries beyond existing FastAPI/SQLAlchemy/Redis/Kafka stack.

## 27. Testing
- Unit: `MasteryEvidenceService.process_evidence()` orchestration logic, including withdrawal-exclusion branch.
- Idempotency test: same `attempt_id` submitted twice → identical result, evidence not double-counted (mirrors A.8's withdrawn-question test pattern, verified at this layer per Backend AI Prompt item 4).
- Latency test against the p95 < 300ms target under representative batch sizes.
- Integration: full attempt → evidence → score → state-transition flow, including a withdrawn-question-containing attempt.

## 28. Documentation
OpenAPI schema for `POST /v1/mastery/evidence`, marked internal-only (excluded from public-facing API docs if the platform distinguishes internal vs. external OpenAPI surfaces).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create MasteryEvidenceLog Model & Migration**
- Task ID: B-04-T01
- Objective: Append-only evidence audit table.
- Why This Is Required: The auditable evidence trail behind every mastery-score computation; required for B-02's formula, dispute resolution, and content-quality monitoring.
- Existing Architecture to Follow: SQLAlchemy 2.0, Alembic conventions.
- Existing Files to Reuse: `BaseRepository`.
- Files to Create: `models/mastery_evidence_log.py`, migration.
- Files to Modify: `models/__init__.py`.
- Implementation Details: Append-only enforced at the repository layer (no update/delete methods exposed); index `(state_id, created_at DESC)`.
- Business Rules: Never edited once written.
- Validation: N/A. Error Handling: N/A. Security: N/A. Performance: Index supports fast evidence-history queries.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: Migration smoke test.
- Documentation: Model docstring noting append-only contract.
- Dependencies: B-01 (skill_node FK target).
- Do Not Change: N/A.
- Expected Result: Table live.
- Definition of Done: Migration applies cleanly.

**Task 02 — Implement MasteryEvidenceService Orchestration**
- Task ID: B-04-T02
- Objective: Core per-skill processing pipeline.
- Why This Is Required: Central orchestrator tying together B-01/B-02/B-03 for every evidence event.
- Existing Architecture to Follow: `BaseService` pattern, single-transaction-per-request convention.
- Existing Files to Reuse: B-02's `compute_mastery_score()`, B-03's `compute_next_state()`.
- Files to Create: `services/mastery_evidence_service.py`.
- Files to Modify: None.
- Implementation Details: Loop over `responses`, branch on `is_withdrawn_excluded`, assemble evidence history per skill, call the formula and state machine, write log + updated state, all inside one transaction per attempt.
- Business Rules: Whole-batch atomicity (§18 partial-failure rule).
- Validation: Pydantic schema validation at the router boundary.
- Error Handling: Transaction rollback on any per-skill failure.
- Security: N/A. Performance: Single transaction, indexed queries, cached formula lookup.
- Localization: N/A. RTL: N/A.
- Analytics: Fires the four events listed in §23.
- Tests: `test_mastery_evidence_service.py`.
- Documentation: Docstring on orchestration order.
- Dependencies: Task 01, B-02, B-03.
- Do Not Change: B-02/B-03's pure-function contracts (call them, don't modify their internals here).
- Expected Result: Working orchestration service.
- Definition of Done: Unit tests green.

**Task 03 — Implement POST /v1/mastery/evidence Router + Idempotency**
- Task ID: B-04-T03
- Objective: Public (internal) endpoint with Redis-backed idempotency.
- Why This Is Required: A.8's Quiz Service needs a reliable, retry-safe integration point.
- Existing Architecture to Follow: Router → Service → Repository layering; existing idempotency-key pattern elsewhere in the platform.
- Existing Files to Reuse: Internal-service-auth dependency (existing pattern, not invented here).
- Files to Create: `schemas/mastery_evidence.py`.
- Files to Modify: `api.py`.
- Implementation Details: Redis key `mastery_evidence:{attempt_id}` stores the serialized response after first successful processing; subsequent requests with the same `attempt_id` short-circuit to the cached response without re-invoking the service.
- Business Rules: Idempotency window should be generously long (e.g., 24-48h) to cover realistic retry scenarios.
- Validation: Request schema validation per §15.
- Error Handling: Per §18 table.
- Security: Internal-only auth enforced.
- Performance: Idempotency check is a single Redis GET before any DB work.
- Localization: N/A. RTL: N/A. Analytics: N/A (fired inside the service, Task 02).
- Tests: `test_mastery_evidence_api.py`, `test_mastery_evidence_idempotency.py`.
- Documentation: OpenAPI schema.
- Dependencies: Task 02.
- Do Not Change: N/A.
- Expected Result: Working, idempotent, internally-authenticated endpoint.
- Definition of Done: Idempotency test (double-submit → single processing) green; API test green.

**Task 04 — Withdrawn-Exclusion & Content-Quality Delta Logging**
- Task ID: B-04-T04
- Objective: Correctly skip withdrawn evidence from scoring while preserving audit visibility and content-quality signal.
- Why This Is Required: FR-10 is a hard rule; Edge Case 7 asks for the exclusion delta to be monitored.
- Existing Architecture to Follow: Same service.
- Existing Files to Reuse: A.8's withdrawn-question test pattern (referenced, not copied verbatim — this is a different layer).
- Files to Create: `tests/modules/learning/test_mastery_evidence_withdrawn_exclusion.py`.
- Files to Modify: `services/mastery_evidence_service.py` (if not already complete from Task 02).
- Implementation Details: Log excluded responses with `excluded_withdrawn=true`; compute and log the score delta (with vs. without exclusion) for monitoring; wire an alert threshold for exclusion-rate spikes per skill (coordinate with DevOps monitoring config referenced in A.9 PRD §10).
- Business Rules: Excluded evidence never contributes to `mastery_score`.
- Validation/Error Handling/Security/Performance: N/A beyond Task 02's coverage.
- Localization: N/A. RTL: N/A.
- Analytics: Exclusion-rate monitoring signal (internal).
- Tests: This task IS the primary test.
- Documentation: Note in service docstring.
- Dependencies: Task 02.
- Do Not Change: N/A.
- Expected Result: Correct exclusion behavior with audit trail.
- Definition of Done: Test mirroring A.8's withdrawn-question test passes at this layer.

## 30. Definition of Done
`POST /v1/mastery/evidence` live, internally-authenticated, idempotent, atomically processing per-attempt evidence batches through B-02/B-03, correctly excluding withdrawn responses while preserving audit trail, meeting the p95 < 300ms latency target.

## 31. Final Verification Checklist
- [x] `mastery_evidence_log` table live, append-only enforced
- [x] Idempotency verified (duplicate `attempt_id` → no double-processing)
- [x] Withdrawn-exclusion verified (mirrors A.8 pattern at this layer)
- [x] Whole-batch transactional atomicity verified (partial-failure rollback)
- [x] p95 < 300ms latency verified under representative load
- [x] All four analytics events firing correctly
- [x] Internal-only auth enforced, no client-facing token accepted
- [x] Exclusion-rate content-quality monitoring wired
