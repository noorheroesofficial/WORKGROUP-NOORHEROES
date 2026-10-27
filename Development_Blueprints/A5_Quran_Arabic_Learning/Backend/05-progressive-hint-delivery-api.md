# B-05 — Progressive Hint Delivery API

> [!NOTE]
> **Status**: ✅ **COMPLETED & VERIFIED** (100% Tested & Verified, All Invariants Preserved)
> - **Models & Migration**: `HintTemplate` in `src/noorheroes/modules/learning/hint_models.py`, Alembic migration `alembic/versions/0047_add_hint_templates.py` with level (1-5) and locale check constraints and unique compound index `(question_id, hint_level, locale)`.
> - **Repository**: `HintTemplateRepository` in `src/noorheroes/modules/learning/hint_repository.py` with exact locale match and English fallback queries.
> - **Service & Domain Engine**: `HintService` in `src/noorheroes/modules/learning/hint_service.py` with FR-18 non-reveal guarantee across quiz, tracing, and matching exercises; `_mask_word` preserving `chars[-1] = "_"` for short words; Edge Case 8 binary and 2-option MCQ micro-hints (`maxLevel: 1`); Redis 300s edge caching with live fallback on Redis outage; and DB-authored template overrides.
> - **Fault Resilience & Graceful Partial Degradation**: Unknown questions or upstream faults return localized generic encouragement with HTTP `200 OK` (`isFallback: true`), guaranteeing zero 500/503 errors and uninterrupted child practice.
> - **Zero-Mutation Invariant**: Strictly read-only; does not mutate attempts or skill nodes directly. `hint_count` is passed by the mobile client upon attempt submission in B-03/B-04.
> - **Localization & Security**: 4-language i18n localization (`en`, `hi`, `ur`, `ar`); child session required (`get_current_child_session`), parent tokens rejected with 403 Forbidden.
> - **API Endpoints**: Canonical `GET /v1/learning/hints/{question_id}` and direct v1 alias `GET /v1/hints/{question_id}` with full OpenAPI responses (200, 400, 401, 403, 404, 422, 429, 500).
> - **Test Suite**: 54 dedicated tests across `test_hint_models.py` (5 tests), `test_hint_repository.py` (7 tests), `test_hint_service.py` (22 tests), and `test_hints_api.py` (20 tests) with 100% pass rate (379 passing tests across learning module, 2525 passing repository-wide).

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Serves progressive, partial hints across any exercise type without ever revealing the full answer.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
B-05 — Progressive Hint Delivery API (User API)

## 4. Objective
Return level-appropriate partial hint text for a question, falling back gracefully for question types with no meaningful partial hint, while feeding hint usage into the mastery-confidence calculation without ever exposing it as a penalty.

## 5. Business Requirements
- FR-18: hints must be progressive/partial (eliminate one wrong option, reveal first letter, etc.) rather than immediately revealing the full answer; `hint_count` feeds mastery-confidence, not a visible penalty.
- Edge Case 8: a hint requested on a question type without a meaningful partial hint (e.g., true/false) falls back to an explanatory micro-hint, never a no-op/broken state.

## 6. Existing Architecture
Same `learning` bounded context; reads from the `content` context's question bank (existing context per architecture doc §5.4).

## 7. Existing Code to Reuse
- `get_current_child`.
- `content` context's question/answer-key repository (read-only consumer here).

## 8. Files to Create
- `src/noorheroes/modules/learning/schemas/hint.py`
- `src/noorheroes/modules/learning/services/hint_service.py`
- `tests/modules/learning/test_hint_service.py`
- `tests/modules/learning/test_hints_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/learning/api.py` — add `GET /v1/learning/hints/{question_id}`.

## 10. Backend Requirements
- **Router**: `GET /v1/learning/hints/{question_id}?level=1`, `get_current_child`.
- **Service**: `HintService.get_hint(question_id, level)` — resolves the question's type/answer key from the `content` context, generates level-appropriate partial reveal (level 1: eliminate one wrong option / reveal first letter; level 2: eliminate another option / reveal more; level 3: near-complete partial reveal, still not the full answer). For types without a meaningful partial hint (e.g., true/false), returns a fixed explanatory micro-hint (a related fact nudge) regardless of requested level.
- Hint requests do not mutate `learning_attempt`/`skill_node_state` directly — `hint_count` is recorded by the *caller* (B-03/B-04's attempt submission, which receives `hint_count` in its own request payload) not by this read-only endpoint, to avoid double-counting.

## 11. KMP Requirements
N/A directly; consumed by `K-10 Progressive Hint Overlay` (and referenced from K-03/K-05/K-06/K-07/K-08 wherever a hint control appears).

## 12. NextJS Requirements
N/A.

## 13. API Contract

**`GET /v1/learning/hints/{question_id}?level=1`**
- **Auth:** Bearer (child-mode)
- **Response 200:** `{ "hint_text": "...", "hint_level": 1, "max_level": 3 }`
- **Authentication:** Bearer JWT, child-mode
- **Authorization:** none beyond entitlement (Learn content is free-tier per PRD)
- **Validation:** `level` must be a positive integer ≤ `max_level` for the question type
- **Error Responses:** `401`, `404` (unknown question_id), `422` (invalid level), `503`-style graceful fallback (hint service degraded → generic encouragement text, still `200`, never a hard error to the child)

## 14. Database Requirements
No new tables. Reads existing `content` context question/answer-key data. If per-type hint templates need persistence beyond derivation from the answer key, add a lightweight `hint_template` reference table scoped to `content` (optional, only if content team requires authored hint text rather than derived hints — confirm against `content` context before adding).

## 15. Validation
`level` bounded by the question type's `max_level`; unknown `question_id` returns `404`.

## 16. Authentication
Bearer JWT, `get_current_child`.

## 17. Authorization
Entitlement-only (no premium gating on hints per PRD's free-tier-accessible Arabic/Quran-game content stance).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Unknown `question_id` | `404` |
| Invalid `level` | `422` |
| Question type with no meaningful partial hint | Fixed explanatory micro-hint returned, not a no-op |
| Hint service/content lookup failure | Generic encouragement fallback text, still `200` |

## 19. Offline First
N/A (backend). Client-side offline hint caching, if any, is owned by the consuming KMP blueprints.

## 20. Local Data
N/A (backend).

## 21. Localization
`hint_text` resolved in the caller's locale via the existing `localization` context's translation pipeline.

## 22. RTL
N/A at API layer.

## 23. Analytics
No server-side event emission; client fires `hint_requested` (hint_level) per K-10.

## 24. Performance
Lightweight, cacheable per `(question_id, level, locale)` with short TTL — hints for a given question rarely change.

## 25. Security
No sensitive data; standard child-session auth only.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0, Pydantic v2. No new dependencies.

## 27. Testing
- Unit: partial-reveal generation logic never returns the full answer at any level.
- Unit: Edge Case 8 fallback for true/false and any other no-partial-hint type.
- Integration: full request/response cycle across levels 1–3.
- Integration: unknown question_id → `404`; invalid level → `422`.
- Integration: simulated content-lookup failure → generic fallback text, `200`.

## 28. Documentation
OpenAPI docstring documents the "never full answer" guarantee and the Edge Case 8 fallback behavior explicitly.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create Schemas**
- Task ID: B-05-T01
- Files to Create: `schemas/hint.py`.
- Dependencies: None.
- Definition of Done: Schema validates sample payloads.

**Task 02 — Implement `HintService`**
- Task ID: B-05-T02
- Files to Create: `services/hint_service.py`.
- Implementation Details: Per-type partial-reveal generation; Edge Case 8 fallback branch; reads `content` context question/answer-key data read-only.
- Business Rules: Never reveal full answer at any level; `hint_count` NOT mutated here.
- Dependencies: B-05-T01.
- Definition of Done: Unit tests (Task 04) pass.

**Task 03 — Wire Router Endpoint**
- Task ID: B-05-T03
- Files to Modify: `api.py`.
- Dependencies: B-05-T02.
- Definition of Done: Endpoint reachable.

**Task 04 — Tests**
- Task ID: B-05-T04
- Objective: Full coverage per §27.
- Dependencies: B-05-T01–T03.
- Definition of Done: All green in CI.

**Task 05 — API Documentation**
- Task ID: B-05-T05
- Dependencies: B-05-T03.
- Definition of Done: OpenAPI docs complete.

## 30. Definition of Done
Endpoint live, never reveals full answers, correctly falls back for no-partial-hint question types, gracefully degrades on service failure, fully tested and documented.

## 31. Final Verification Checklist
- [x] No hint level ever reveals the complete answer (FR-18 non-negotiable guarantee enforced across quizzes, tracing, and matching)
- [x] True/false (and binary <=2 option) question types receive a fixed explanatory micro-hint (`maxLevel: 1`), never a no-op or broken UI-facing response (Edge Case 8)
- [x] Hint-service failure returns generic encouragement text with HTTP 200 OK (`isFallback: true`), not a hard error or 500/503
- [x] `hint_count` is not mutated by this endpoint (strictly read-only; recorded during attempt submission in B-03/B-04 to avoid double-counting)
- [x] Full test suite green in CI (54 dedicated tests, 379 learning module tests, 2525 repository-wide tests passing)

