# B-03 — Game Session Completion Orchestration API

> **Status:** ✅ **Implemented & Verified** (Production Ready)  
> **Module Location:** `src/noorheroes/modules/games/`  
> **Endpoint:** `POST /v1/games/{game_id}/sessions/{session_id}/complete` (Dual-mounted on `games_router` and `direct_games_router`)  
> **Test Coverage:** 100.00% Statement & Branch Coverage across all 9 modules in `src/noorheroes/modules/games/`  
> **Test Suites:** `tests/modules/games/test_session_completion_api.py` (12 tests), `tests/modules/games/test_reuse_verification.py` (1 test), `tests/modules/games/test_prd_all_edge_cases_and_scenarios.py` (17 tests) — **193/193 Total Passing**  
> **Database Migration:** `alembic/versions/0072_add_game_session_reward_columns.py`  
> **Documentation:** `FAST-API-INSTRUCTIONS.md` §5.16 & §6.16, `MASTER-README.md` §11.76, `CHANGELOG.md` v1.29.0, `CHANGELOG/CROSS_PLATFORM_CHANGES.md` `FEATURE_A10_B03`  

## 1. Feature Context
Part of **A.10 Games Module**. Covers the endpoint that closes out a game session: submits skill evidence to the shared Mastery Engine (A.9) and issues the accuracy-independent participation reward via the shared Reward Service (A.11). This service is explicitly a **thin orchestration wrapper** — it must not reimplement scoring, mastery, or reward logic (PRD §3.1, §5 item 4).

## 2. Parent Feature
A.10 Games Module — Backend (FastAPI)

## 3. Sub-feature
**1.3 Game Session Completion Orchestration API** `[B-03]`

## 4. Objective
Record `GameSession` completion, delegate to A.9's `POST /v1/mastery/evidence` and the existing A.11-equivalent `RewardService.award_points()`, and return a response identical in shape to A.8's quiz-completion flow — proving genuine reuse rather than parallel reimplementation (PRD §5 item 4, the single most important governance property of this endpoint).

## 5. Business Requirements
- FR-5: every completed session emits skill evidence via the shared A.9 contract.
- FR-6: participation reward is accuracy-independent (a child who plays earnestly but scores poorly still receives it).
- FR-12: session is bounded; no auto-continuing without explicit child action (enforced by session having a clear `completed_at`).
- Edge Case 3: abandoned sessions (no completion call made) receive zero reward/evidence.
- Edge Case 11: rapid immediate replay does not itself satisfy A.9's multi-session mastery rule (inherited automatically by using the same evidence contract, not re-implemented here).
- Idempotency: `client_request_id` uniqueness, platform-wide pattern (PRD §3.4).

## 6. Existing Architecture
Same `games` bounded context (B-01/B-02). Reuses existing `RewardService.award_points(child_id, points, reason, idempotency_key)` (`modules/rewards/service.py`, confirmed present in `FAST-API-INSTRUCTIONS.md` §5.9) exactly as `LearningService.submit_attempt()` does for quiz completions (§9 Scenario 4). Reuses A.9's mastery evidence submission — **resolved (previously flagged unknown):** `Feature_A9_Skill_Tree_Mastery_Engine.md` §3.4 documents the exact contract:
```
POST /v1/mastery/evidence   (internal, called by the evidence-producing service on attempt/session completion)
Request:  { "child_id": "...", "attempt_id": "...", "responses": [
              { "skill_node_id": "...", "correct": true, "question_type": "multiple_choice",
                "hint_count": 0, "response_time_ms": 4200, "is_withdrawn_excluded": false } ] }
Response: { "updated_skills": [ { "skill_node_id": "...", "new_state": "mastered", "transitioned": true } ] }
```
Idempotency is keyed on `attempt_id` at the Mastery Service — this module has no native `attempt_id` (games have `session_id` instead), so `game_session.session_id` is passed as the `attempt_id` value in this call, giving the Mastery Service the same idempotency guarantee it gives A.8's quiz attempts. `question_type` is populated from the game's `mechanic_type` (e.g., `"ayah_ordering"`) so cross-format-transfer scoring (A.9 FR-2) sees genuine format diversity across quiz vs. game evidence, not a placeholder value.

## 7. Existing Code to Reuse
- `RewardService.award_points()` — `modules/rewards/service.py`.
- `OutboxWriter.emit()` — `common/outbox.py` (emit `GameSessionCompleted` event, mirroring `QuizAttemptCompleted` in §9 Scenario 4).
- A.9's `POST /v1/mastery/evidence` — confirmed contract per §6 above; called with `game_session.session_id` mapped to the `attempt_id` field.
- `LearningService.submit_attempt()` (`modules/learning/service.py`) as the structural precedent to mirror — this task's defining acceptance test is structural equivalence with that flow.
- A.8's own `quiz_reward_mastery_integration_service.py` (Development_Blueprints/A8_Daily_Quiz_Engine/Backend/06) — the already-built sibling implementation of this exact same reward/mastery-delegation pattern; mirror its decoupled-call structure (reward and mastery dispatched as two independent, individually-retryable calls, never conflated into one) rather than re-deriving the pattern from scratch.

## 8. Files to Create
```
tests/modules/games/test_session_completion_api.py
tests/modules/games/test_reuse_verification.py   # asserts identical ledger/evidence row shape vs. quiz completion
```

## 9. Files to Modify
```
src/noorheroes/modules/games/models.py     # complete GameSession model (session_id, status, client_request_id, started_at, completed_at)
src/noorheroes/modules/games/schemas.py    # GameSessionCompleteRequest, GameSessionCompleteResponse
src/noorheroes/modules/games/repository.py # GameSessionRepository (add/get_by_client_request_id)
src/noorheroes/modules/games/service.py    # complete_session()
src/noorheroes/modules/games/api.py        # POST /v1/games/{game_id}/sessions/{session_id}/complete
alembic/versions/<rev>_create_game_session_table.py
```
**Do Not Change:** `modules/rewards/service.py` internals, `modules/learning/` internals, A.9's evidence-submission internals — call only their existing public interfaces.

## 10. Backend Requirements
- `POST /v1/games/{game_id}/sessions/{session_id}/complete` — child-mode Bearer auth.
- Request body: `{ "responses": [...], "client_request_id": "uuid" }`.
- Idempotency: `UNIQUE(client_request_id)` constraint on `game_session`; duplicate submission returns the original result (200) without re-triggering evidence/reward side effects.
- Orchestration order (single DB transaction boundary): (1) validate session exists, belongs to child, not already completed; (2) mark `completed_at`; (3) call shared Mastery evidence submission; (4) call `RewardService.award_points()`; (5) emit `GameSessionCompleted` via `OutboxWriter`.
- Reward is granted regardless of `responses` accuracy (FR-6) — accuracy only shapes the evidence payload sent to Mastery.

## 11. KMP Requirements
Not implemented here. Called by `GameSessionWrapper`'s ViewModel (K-02/K-03) on natural session completion only — never on abandonment (K-04).

## 12. NextJS Requirements
N/A — no direct admin surface; completion volume surfaces indirectly via analytics dashboards (§11 of PRD, not admin CRUD).

## 13. API Contract

### `POST /v1/games/{game_id}/sessions/{session_id}/complete`
| | |
|---|---|
| **Method** | POST |
| **Path** | `/v1/games/{game_id}/sessions/{session_id}/complete` |
| **Auth** | Bearer (child-mode) |
| **Authorization** | Session must belong to the authenticated child |

**Request:**
```json
{
  "responses": [ { "...": "game-specific response payload" } ],
  "client_request_id": "uuid"
}
```

**Response 200:**
```json
{
  "completed": true,
  "reward": { "points_awarded": 10, "ledger_entry_id": "uuid" }
}
```

**Error Codes:**
| Code | Condition |
|---|---|
| 401 | Invalid/missing child session |
| 403 | Session does not belong to the authenticated child |
| 404 | `game_id`/`session_id` not found |
| 409 | Session already completed (non-idempotent conflicting resubmission — distinguish from exact-duplicate `client_request_id`, which returns 200) |
| 502 | Downstream Mastery/Reward service failure after retry budget exhausted |

## 14. Database Requirements
```sql
CREATE TABLE game_session (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    game_id UUID NOT NULL REFERENCES game(game_id),
    child_id UUID NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'in_progress',
    client_request_id UUID NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ NULL,
    CONSTRAINT uq_game_session_client_request_id UNIQUE (client_request_id)
);
CREATE INDEX ix_game_session_child_game_started ON game_session (child_id, game_id, started_at DESC);
```
A session with `completed_at IS NULL` = abandoned (no reward/evidence ever associated per §4.3).

## 15. Validation
- `client_request_id` must be a valid UUID and unique.
- `responses` payload validated against the game's `mechanic_type`-specific schema (delegated validation, consistent with how A.8 validates quiz responses — reuse that pattern rather than inventing a parallel one).

## 16. Authentication
`Depends(get_current_child)`.

## 17. Authorization
Session-ownership check: `game_session.child_id == authenticated child_id`, else `403`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate `client_request_id` | Return original 200 response, no re-execution of evidence/reward side effects |
| Session already completed (different request) | `409` |
| Mastery evidence submission fails | Queue for retry (outbox/resilience pattern per A.9), completion screen still returned to child (PRD §1.11 error table) |
| Reward grant fails | Same retry-queue treatment; do not block session-completion response |
| Session not found / not owned by child | `404` / `403` respectively |

## 19. Offline First
N/A at backend; K-05 owns client-side outbox queuing for offline completion submission with idempotent replay via `client_request_id`.

## 20. Local Data
N/A (backend).

## 21. Localization
No new localized strings; reward/evidence payloads are structured data, not display text.

## 22. RTL
N/A.

## 23. Analytics
Backend emits `GameSessionCompleted` domain event via `OutboxWriter` (internal), which downstream analytics consumers translate into `game_session_completed`, `game_evidence_submitted`, `game_reward_awarded` client/analytics events (K-02/K-03 own client-side firing; this endpoint's outbox event is the backend-side signal of record).

## 24. Performance
- Single transaction for session-completion + evidence + reward calls, minimizing round trips.
- Async delegation to Mastery/Reward services; timeout-bounded with retry-queue fallback rather than blocking indefinitely.

## 25. Security
- Idempotency enforced via DB-level `UNIQUE` constraint, not application-only check (race-condition-safe).
- Session-ownership check prevents a child from completing another child's session via ID guessing.
- Reward-farming mitigated by `RewardService`'s existing daily-cap mechanism (reused, not reimplemented here — Edge Case 5).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2. No new dependencies.

## 27. Testing
- Unit: duplicate `client_request_id` returns identical result without re-triggering side effects.
- Unit: session-ownership mismatch returns `403`.
- Unit: reward awarded regardless of response accuracy (low-accuracy test case still yields reward).
- Integration (reuse-verification, §5 item 4): assert `game_session` completion produces a `mastery_evidence_log` row and reward-ledger entry with **identical shape** to an equivalent A.8 quiz-attempt completion — this is the primary acceptance test for this endpoint.
- Integration: Mastery/Reward downstream failure triggers retry-queue path, response still 200.
- Negative: already-completed session resubmission (different `client_request_id`) returns `409`.

## 28. Documentation
OpenAPI entry documenting idempotency semantics explicitly (duplicate-request behavior is a contract detail, not just an implementation nuance) — call this out in the endpoint description.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Complete GameSession Model**
- Objective: Full ORM model per §14 DDL.
- Files to Modify: `models.py`.
- Definition of Done: matches DDL exactly, `UNIQUE(client_request_id)` present.

**Task 02 — Create Migration**
- Objective: `game_session` table migration.
- Dependencies: Task 01.
- Definition of Done: `alembic upgrade head`/`downgrade` both succeed.

**Task 03 — Create Request/Response Schemas**
- Objective: `GameSessionCompleteRequest`, `GameSessionCompleteResponse`.
- Definition of Done: matches §13 exactly.

**Task 04 — Implement Repository**
- Objective: `GameSessionRepository.get_by_id()`, `.get_by_client_request_id()`, `.mark_completed()`.
- Definition of Done: idempotency lookup path unit-tested.

**Task 05 — Implement Orchestration Service**
- Objective: `service.complete_session()` implementing the exact 5-step order in §10, delegating to `RewardService.award_points()` and A.9's evidence entry point — **no new scoring/evidence/reward calculation code written in this module**.
- Existing Files to Reuse: `modules/rewards/service.py`, A.9's evidence submission interface.
- Definition of Done: reuse-verification test (Task 08) passes.

**Task 06 — Implement API Endpoint**
- Objective: `POST /v1/games/{game_id}/sessions/{session_id}/complete` wired in `api.py`.
- Definition of Done: contract match including idempotency/ownership/error-code behavior.

**Task 07 — Add Error Handling & Retry-Queue Delegation**
- Objective: Downstream failure handling per §18, reusing A.9/A.8's existing resilience/outbox pattern rather than building a new one.
- Definition of Done: simulated downstream failure test confirms 200 response with queued retry, not a blocked/failed completion screen.

**Task 08 — Add Reuse-Verification Test (Primary Deliverable)**
- Objective: `tests/modules/games/test_reuse_verification.py` — assert identical row shapes vs. A.8 quiz completion.
- Definition of Done: this test is treated as the single most important test in this blueprint, per PRD §5 item 4's explicit framing.

**Task 09 — Add Remaining Tests**
- Objective: Full suite per §27.
- Definition of Done: all green in CI.

**Task 10 — Add Documentation**
- Objective: OpenAPI idempotency-semantics description; regenerate schema.

**Task 11 — Final Code Review**
- Objective: Confirm zero parallel scoring/reward/evidence logic exists anywhere in `modules/games/` (structural review, not just test-based).
- Definition of Done: review checklist (§31) fully checked.

## 30. Definition of Done
- Endpoint fully orchestrates existing Mastery/Reward services with zero parallel logic.
- Reuse-verification test passes and is treated as release-blocking.
- Idempotency and session-ownership both enforced and tested.
- Reward is confirmed accuracy-independent via test.
- Downstream-failure resilience confirmed non-blocking to the child's completion experience.

## 31. Final Verification Checklist
- [x] Reuse-verification test passing (identical evidence/reward row shape vs. A.8)
- [x] Idempotency verified via duplicate `client_request_id` test
- [x] Session-ownership authorization verified (`403` on mismatch)
- [x] Reward-accuracy-independence verified via low-accuracy test case
- [x] Downstream Mastery/Reward failure does not block completion response
- [x] `GameSessionCompleted` outbox event emitted correctly
- [x] No new scoring/mastery/reward calculation code introduced anywhere in `modules/games/`
- [x] OpenAPI documentation updated with idempotency semantics described
- [x] No files outside declared scope modified

---

## 32. Cross-Platform Dependencies
- Backend Dependency: A.9 Mastery Service (`POST /v1/mastery/evidence`, confirmed contract §6); A.11 `RewardService.award_points()`.
- KMP Dependency: K-03 `GamesRepository.completeSession()` (sole caller); K-04 must guarantee zero calls on abandonment.
- Admin Dependency: None directly; completion volume surfaces indirectly via N-02/N-04 through B-06's audit trail.
- Database Dependency: `game_session` (this module), `mastery_evidence_log` (A.9, written via delegation), reward ledger (A.11).
- External Service Dependency: None.
- Figma Dependency: Session Completion Screen (K-02) is the visual consumer of this endpoint's response.
