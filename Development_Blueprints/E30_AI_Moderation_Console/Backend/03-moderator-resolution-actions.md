# B-03 — Moderator Resolution & Idempotent Queue Actions

## 1. Feature Context
Parent PRD: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
Depends on: B-01 (queue item), E.28 (RBAC), E.29 (content/scholar escalation routing target)
Feeds into: B-05 (`create_evaluation_case` action creates an `EvaluationCase`), N-03 (Resolution Action Bar)

## 2. Parent Feature
E.30 — AI Moderation Console & Safety Evaluation Harness

## 3. Sub-feature
**Moderator Resolution & Idempotent Queue Actions** (ID: B-03) — the five-action resolve endpoint (approve expected refusal / mark false positive / escalate content gap / suspend feature / create evaluation case), with idempotent resolution as its structural guarantee against double-processing under concurrent moderator access.

## 4. Objective
Let a moderator resolve a flagged item with exactly one of five canonical actions, correctly routing side effects (false-positive signal, content/scholar escalation, evaluation-case creation), while guaranteeing that two moderators racing to resolve the same item never double-process it.

## 5. Business Requirements
- FR-4: action set — approve expected refusal, mark false positive, escalate content gap, suspend feature, create an evaluation case.
- §3.4 `POST .../resolve`: **idempotent against an already-resolved item** — a second resolution attempt returns the existing resolved state as a no-op.
- Edge Case 4 (§1.10): two moderators simultaneously open the same item; first resolving action wins, second is a graceful no-op (mirrors E.28's maker-checker redundant-approval pattern).
- Edge Case 2: a religious-rulings item with a technically-passing-but-theologically-imprecise answer is escalated via `escalate_content_gap` with **Scholar Review Board-specific routing**, not treated as a false positive.
- Edge Case 8: `suspend_feature` attempted by a non-safety role is rejected at the service layer (full mechanics owned by B-04; this endpoint's `resolve` action set does **not** include `suspend_feature` as a resolve-body action — suspension is its own dedicated B-04 endpoint, referenced from the Detail screen alongside the four resolve actions per §2.2's five-button description).

## 6. Existing Architecture
Extends the `ai_moderation` context (B-01/B-02). Directly mirrors `review/service.py::submit_decision`'s idempotency-and-branching shape — the closest existing precedent in the codebase for "queue item + decision → branching side effects + outbox event."

## 7. Existing Code to Reuse
- `review/service.py::submit_decision` — structural precedent for decision validation + branching + outbox emission (adapt, do not copy verbatim: E.30's idempotency semantics return the existing state rather than raising, unlike E.29's segregation-of-duties which raises)
- `OutboxWriter.emit()` (`common/outbox.py`)
- `core/exceptions.py::ValidationError`, `NotFoundError`
- B-01's `AiModerationRepository`/`AiModerationQueueItem`

## 8. Files to Create
- `src/noorheroes/modules/ai_moderation/resolution_schemas.py` → `ResolveActionRequest`, `ResolveActionResponse`
- `src/noorheroes/modules/ai_moderation/resolution_service.py` → `ModerationResolutionService(BaseService)`
- `tests/modules/ai_moderation/test_idempotent_resolution.py`
- `tests/modules/ai_moderation/test_resolution_actions.py`

## 9. Files to Modify
- `src/noorheroes/modules/ai_moderation/api.py` → add `POST /{id}/resolve`
- `src/noorheroes/modules/ai_moderation/repository.py` → add `mark_resolved()`, `get_for_update()`

## 10. Backend Requirements

### 10.1 Allowed Actions
```python
RESOLUTION_ACTIONS = ("approve_refusal", "mark_false_positive", "escalate_content_gap", "create_evaluation_case")
```
> `suspend_feature` is intentionally excluded from this set — it is B-04's own dedicated, more-restrictively-scoped endpoint (`POST /v1/admin/ai-features/{feature}/suspend`), not a `resolve` action, since its role restriction (safety roles only) is strictly narrower than the general `child_safety_reviewer` scope that governs the other four actions.

### 10.2 Endpoint
| Method | Path | Auth | Purpose |
|---|---|---|---|
| POST | `/v1/admin/ai-moderation/{id}/resolve` | `ai-moderation:read` (`child_safety_reviewer`+) | Submit a resolution action |

### 10.3 Service Logic — Idempotency (the critical path)
```python
class ModerationResolutionService(BaseService):
    def __init__(self, repo: AiModerationRepository, outbox: OutboxWriter, eval_service: "EvaluationHarnessService"):
        self.repo = repo
        self.outbox = outbox
        self.eval_service = eval_service

    async def resolve(self, queue_item_id: str, action: str, admin_ctx: AdminSessionContext) -> dict:
        if action not in RESOLUTION_ACTIONS:
            raise ValidationError(f"Unknown resolution action: {action}")

        item = await self.repo.get_for_update(queue_item_id)  # row lock / SELECT ... FOR UPDATE
        if item is None:
            raise NotFoundError(f"AI moderation queue item {queue_item_id} not found")

        # --- IDEMPOTENCY: already-resolved is a no-op returning existing state, never an error ---
        if item.status == "resolved":
            return self._to_response(item, already_resolved=True)

        item.status = "resolved"
        item.resolution_action = action
        item.resolved_by = admin_ctx.admin_id
        item.resolved_at = datetime.now(timezone.utc)
        await self.repo.add(item)

        if action == "mark_false_positive":
            await self.outbox.emit({"queue_item_id": queue_item_id}, "ai_moderation_mark_false_positive", queue_item_id)
        elif action == "escalate_content_gap":
            is_religious = item.stage_flagged == "confidence_score" and await self.repo.is_religious_category(queue_item_id)
            event_name = "ai_moderation_escalate_scholar_board" if is_religious else "ai_moderation_escalate_content_gap"
            await self.outbox.emit({"queue_item_id": queue_item_id, "religious_routing": is_religious}, event_name, queue_item_id)
        elif action == "create_evaluation_case":
            await self.eval_service.create_case_from_queue_item(queue_item_id)
            await self.outbox.emit({"queue_item_id": queue_item_id}, "ai_moderation_evaluation_case_created", queue_item_id)
        elif action == "approve_refusal":
            await self.outbox.emit({"queue_item_id": queue_item_id}, "ai_moderation_approve_expected_refusal", queue_item_id)

        return self._to_response(item, already_resolved=False)
```
> **Concurrency note:** `get_for_update()` should use a `SELECT ... FOR UPDATE` (or the project's established optimistic-lock pattern via `BaseRepository.update_with_optimistic_lock`) so that two simultaneous `resolve` calls against the same `queue_item_id` serialize correctly at the database level — the idempotency check alone is not sufficient under true concurrency without a row-level lock or version check; confirm the exact mechanism against `common/base_repository.py`'s existing optimistic-lock convention before implementation.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
Consumed by N-03 (Moderator Resolution Action Bar) for all four actions, and cross-referenced by N-04 for the separate kill-switch action.

## 13. API Contract

### `POST /v1/admin/ai-moderation/{id}/resolve`
- **Auth:** `child_safety_reviewer`+ role
- **Request:** `{ "action": "approve_refusal|mark_false_positive|escalate_content_gap|create_evaluation_case" }`
- **Response 200:** `{ "queue_item_id", "status": "resolved", "resolution_action", "resolved_by", "resolved_at", "already_resolved": false }`
- **Response 200 (idempotent no-op):** same shape with `"already_resolved": true` and the **original** resolver's `resolved_by`/`resolved_at`/`resolution_action` — never the second caller's attempted action
- **Errors:** `422 VALIDATION_ERROR` (unknown action), `404 NOT_FOUND`, `403 FORBIDDEN`

## 14. Database Requirements
Uses B-01's `ai_moderation_queue_item` table; no new tables. Row-level locking or optimistic-lock versioning required on `UPDATE` per §10.3's concurrency note.

## 15. Validation
`action` must be one of the four `RESOLUTION_ACTIONS`; `suspend_feature` submitted here is rejected as an unknown action (not silently redirected to B-04).

## 16. Authentication
`Depends(get_current_admin)`.

## 17. Authorization
`require_admin_scope("ai-moderation:read")` — same general scope as B-01 (all four resolve actions are available to any `child_safety_reviewer`, unlike the elevated transcript-access scope in B-02 or the safety-role-only kill switch in B-04).

## 18. Error Handling
| Scenario | Response |
|---|---|
| Unknown action string | `422 VALIDATION_ERROR` |
| Unknown `{id}` | `404 NOT_FOUND` |
| Already-resolved item | `200`, no-op, `already_resolved: true` (never an error) |
| Two concurrent resolve calls | Exactly one resolution recorded; the loser receives the winner's resolved state |
| Missing scope | `403 FORBIDDEN` |

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
Not applicable server-side.

## 22. RTL
Not applicable to backend.

## 23. Analytics
Emits `ai_moderation_approve_expected_refusal`, `ai_moderation_mark_false_positive`, `ai_moderation_escalate_content_gap`, `ai_moderation_evaluation_case_created`, `ai_queue_redundant_action_noop` (internal — fired when `already_resolved: true` is returned), `ai_religious_category_strict_threshold_applied` (internal, fired via the religious-routing branch) per §1.19.

## 24. Performance
Single-row read-then-update per call; row lock held only for the duration of the transaction (short).

## 25. Security
Idempotent resolution is itself a defense against a race-condition-based double-processing exploit (e.g., two rapid-fire requests attempting to trigger two different outbox events for the same item) — the lock/idempotency check must be evaluated **before** any side-effect emission, not after.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Alembic, Pydantic v2, pytest-asyncio.

## 27. Testing
- **Signature test (CI-blocking, backend AI code-gen prompt item 3):** simulate two concurrent resolution attempts on the same queue item and confirm exactly one resolution is recorded, with the second receiving the same resolved-state response rather than erroring or double-processing.
- Unit: each of the four actions' branch logic and outbox event emission.
- Unit: religious-category-routing branch for `escalate_content_gap` (Edge Case 2).
- Unit: unknown action → `422`.
- Integration: full flagged-item → resolve flow for each of the four actions (§13.6 of the parent PRD).

## 28. Documentation
Export OpenAPI; explicitly document the idempotency guarantee and that `suspend_feature` is intentionally not part of this action set (routed to B-04 instead).

## 29. AI Coding Agent Implementation Steps
- **Task 01 — Schemas**: `ResolveActionRequest`/`ResolveActionResponse` including `already_resolved`.
- **Task 02 — Repository additions**: `get_for_update()` (locking), `mark_resolved()`, `is_religious_category()`.
- **Task 03 — Service**: `ModerationResolutionService.resolve()` per §10.3, wired to B-05's `EvaluationHarnessService` for the `create_evaluation_case` branch.
- **Task 04 — Router**: `POST /resolve` endpoint.
- **Task 05 — Concurrency signature test**: the CI-blocking idempotency test from §27.
- **Task 06 — Per-action unit tests**, including the religious-routing branch.
- **Task 07 — Integration test**: full lifecycle per action.
- **Task 08 — Documentation**.
- **Task 09 — Final Code Review**: confirm the row lock/version check genuinely prevents double side-effect emission under real concurrency (not just sequential-request idempotency).

## 30. Definition of Done
All four resolve actions implemented with correct branching and outbox emission; idempotent double-processing prevention verified under simulated concurrency by a CI-blocking test.

## 31. Final Verification Checklist
- [ ] `resolve` endpoint validates the four-action set, rejects `suspend_feature`
- [ ] Idempotent no-op path returns the original resolver's state, tested under concurrency
- [ ] Religious-category escalation routes distinctly from generic content-gap escalation
- [ ] `create_evaluation_case` correctly creates a B-05 `EvaluationCase` referencing this queue item
- [ ] All analytics events wired per §23
- [ ] Tests green in CI, concurrency signature test non-bypassable
