# B-01 — AI Moderation Queue & Detail API

## 1. Feature Context
Parent PRD: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
Depends on: E.28 (Admin Auth/RBAC — role scopes, shared audit log), `ai_safety` module (existing `AiSafetyEvent`/`ai_interactions` store — read-only join target), F.35 (six-stage AI Safety Pipeline — the actual write path into the queue)
Feeds into: B-02 (Transcript Access Gate), B-03 (Moderator Resolution), N-01/N-02 (Queue Dashboard/Detail screens)

## 2. Parent Feature
E.30 — AI Moderation Console & Safety Evaluation Harness

## 3. Sub-feature
**AI Moderation Queue & Detail API** (ID: B-01) — the read surface of the AI Moderation Workflow Service: a filterable queue listing and a redacted-by-default detail endpoint, structurally guaranteed to never leak raw prompt/output content.

## 4. Objective
Give moderators a fast, filterable queue of flagged AI interactions and a detail view carrying full pipeline context (policy category, model version, retrieval sources, confidence score, filters triggered) — while the response schema itself makes it structurally impossible to return the raw, unredacted prompt/output by default.

## 5. Business Requirements
- FR-4: Console contents — prompt/output display with redacted child identifiers; policy category; model version; retrieval sources; confidence score; filters triggered.
- §3.4 `GET /v1/admin/ai-moderation/{id}` response: **never the raw, unredacted prompt/output** in this default response (hard structural rule, not a UI convention).
- Acceptance (§1.9): given a moderator opens a flagged interaction, when it renders, child identifiers are redacted and full pipeline context is shown.
- Empty state (§1.12): zero items in queue → calm "Nothing flagged right now" state (data contract: an empty `items` array is a normal, first-class response, not an error).

## 6. Existing Architecture
New `ai_moderation` bounded context, following the same layered pattern (`Router → Service → Repository → PostgreSQL`) as every other context in FAST-API-INSTRUCTIONS.md §5 — mirroring `review/` (E.29) exactly, since both are moderator-workflow queues. This context does **not** duplicate `ai_safety`'s `AiSafetyEvent` table (which already **is** the `ai_interactions` store, redacted at write time, shared with C.26) — it reads that table via FK join and adds its own queue-state table on top.

## 7. Existing Code to Reuse
- `BaseService`, `BaseRepository[ModelT]` (`common/base_repository.py`, `common/base_service.py`)
- `AdminSessionContext`, `get_current_admin`, `require_admin_scope` (`core/deps.py`)
- `noorheroes/modules/ai_safety/models.py::AiSafetyEvent` — **read-only**, do not modify or duplicate; `model_version`, `input_redacted`, `output_redacted` columns already exist and are already bounded/redacted at write time
- `review/repository.py`'s queue-assembly join pattern (`ReviewRepository.get_queue()`) as the direct structural precedent for this endpoint's query shape
- `OutboxWriter` (not used for reads, but the same module will need it in B-03)

## 8. Files to Create
- `src/noorheroes/modules/ai_moderation/__init__.py`
- `src/noorheroes/modules/ai_moderation/models.py` → `AiModerationQueueItem` ORM model
- `src/noorheroes/modules/ai_moderation/schemas.py` → `AiModerationQueueItemResponse`, `AiModerationDetailResponse`
- `src/noorheroes/modules/ai_moderation/repository.py` → `AiModerationRepository`
- `src/noorheroes/modules/ai_moderation/service.py` → `AiModerationQueueService(BaseService)`
- `src/noorheroes/modules/ai_moderation/deps.py` → `get_ai_moderation_service()`
- `src/noorheroes/modules/ai_moderation/api.py` → `AiModerationRouter`
- `alembic/versions/xxxx_add_ai_moderation_queue_item.py`
- `tests/modules/ai_moderation/test_queue_detail_redaction.py`

## 9. Files to Modify
- `main.py` (or `api/v1/router.py`) → mount `AiModerationRouter` under `/v1/admin/ai-moderation`

## 10. Backend Requirements

### 10.1 Model
```python
class AiModerationQueueItem(Base):
    __tablename__ = "ai_moderation_queue_item"
    __table_args__ = (
        CheckConstraint("status IN ('pending','resolved')", name="ck_ai_moderation_queue_status"),
        Index("ix_ai_moderation_queue_status_flagged", "status", "flagged_at"),
    )

    queue_item_id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_ulid)
    interaction_id: Mapped[str] = mapped_column(String, ForeignKey("ai_safety_event.event_id"), nullable=False)
    stage_flagged: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="pending")
    resolution_action: Mapped[str | None] = mapped_column(String, nullable=True)
    resolved_by: Mapped[str | None] = mapped_column(String, ForeignKey("admin_account.admin_id"), nullable=True)
    flagged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
```
> `interaction_id` FKs to the **existing** `ai_safety_event` table — confirm the actual production table/column name against `ai_safety/models.py::AiSafetyEvent.__tablename__` (`ai_safety_event`) before writing the migration; do not assume a table literally named `ai_interactions` exists as a separate physical table.

### 10.2 Endpoints
| Method | Path | Auth | Purpose |
|---|---|---|---|
| GET | `/v1/admin/ai-moderation` | `ai-moderation:read` (`child_safety_reviewer`+) | Filterable, paginated queue |
| GET | `/v1/admin/ai-moderation/{id}` | `ai-moderation:read` | Redacted detail |

> **Amendment (added to support B-07's False-Positive Feedback Log):** `GET /v1/admin/ai-moderation` accepts an additional optional `resolution_action` query param (`approve_refusal|mark_false_positive|escalate_content_gap|create_evaluation_case`), filtering resolved items by their recorded action. This reuses the existing endpoint/index rather than introducing a parallel query surface — B-07's False-Positive Feedback Log is simply `GET /v1/admin/ai-moderation?status=resolved&resolution_action=mark_false_positive`.

### 10.3 Service Logic
```python
class AiModerationQueueService(BaseService):
    def __init__(self, repo: AiModerationRepository):
        self.repo = repo

    async def get_queue(
        self, status: str | None, policy_category: str | None, resolution_action: str | None = None
    ) -> list[dict]:
        return await self.repo.get_queue(status=status, policy_category=policy_category, resolution_action=resolution_action)

    async def get_detail(self, queue_item_id: str) -> dict:
        row = await self.repo.get_detail_joined(queue_item_id)
        if row is None:
            raise NotFoundError(f"AI moderation queue item {queue_item_id} not found")
        # Structural guarantee: only redacted fields are read off AiSafetyEvent here —
        # raw_prompt/raw_output are never selected in this code path (see B-02 for the
        # ONLY code path permitted to read them).
        return row
```

### 10.4 Redaction Boundary — Structural, Not Conventional
`AiModerationDetailResponse` must be typed such that it has **no field capable of holding raw content** — mirror `ai_safety/models.py`'s own comment style: "no column here is named or shaped to hold raw prompt/response transcripts." The repository method backing this endpoint must `select()` only `input_redacted`, `output_redacted`, `model_version`, `category`, and the queue-item columns — never the (nonexistent, by design) raw columns.

## 11. KMP Requirements
Not applicable — internal operator tool only (PRD §6.7/§12.4).

## 12. NextJS Requirements
Consumed by N-01 (AI Moderation Queue Dashboard) and N-02 (AI Moderation Detail & Redacted Transcript View).

## 13. API Contract

### `GET /v1/admin/ai-moderation?status=&policy_category=&resolution_action=`
- **Auth:** `child_safety_reviewer`+ role
- **Response 200:** `{ "items": [ { "queue_item_id", "stage_flagged", "status", "policy_category", "flagged_at", "resolution_action", "resolved_by", "resolved_at" } ], "total": n }`
- **Empty case:** `{ "items": [], "total": 0 }` — a normal 200, never a 404.
- **`resolution_action` filter:** added to serve B-07's False-Positive Feedback Log without a parallel endpoint; only meaningful combined with `status=resolved`.

### `GET /v1/admin/ai-moderation/{id}`
- **Response 200:** `{ "redacted_prompt": "...", "redacted_output": "...", "policy_category": "...", "model_version": "...", "retrieval_sources": [...], "confidence_score": 0.61, "filters_triggered": [...], "stage_flagged": "confidence_score" }` (§3.4, verbatim)
- **Errors:** `404 NOT_FOUND` (unknown id), `403 FORBIDDEN` (missing `ai-moderation:read` scope)

## 14. Database Requirements
- `ai_moderation_queue_item`: FK `interaction_id` → `ai_safety_event.event_id`; CHECK `status IN ('pending','resolved')`; index `(status, flagged_at DESC)` per PRD §4.2.
- No new columns added to `ai_safety_event` — this feature reads it as-is.

## 15. Validation
- `status` query param, if present, must be one of `pending|resolved`.
- `policy_category` filters exact-match; unknown category values simply return an empty set, never an error (avoids leaking the internal category enum via error messages).
- `resolution_action`, if present, must be one of B-03's `RESOLUTION_ACTIONS` (`approve_refusal|mark_false_positive|escalate_content_gap|create_evaluation_case`); combined with `status != resolved` it simply returns an empty set (a pending item has no `resolution_action` yet), never an error.

## 16. Authentication
`Depends(get_current_admin)`.

## 17. Authorization
`require_admin_scope("ai-moderation:read")` — a new scope distinct from the elevated `ai-moderation:transcript-access` scope introduced in B-02; reconcile the exact scope string against E.28's RBAC matrix once it exists, per the parent blueprints' "do not guess" instruction (same caveat `core/deps.py`'s `require_admin_scope` docstring already carries for E.29's scopes).

## 18. Error Handling
| Scenario | Response |
|---|---|
| Unknown `{id}` | `404 NOT_FOUND` |
| Missing/insufficient scope | `403 FORBIDDEN` |
| Invalid `status` filter value | `422 VALIDATION_ERROR` |
| Empty queue | `200` with `items: []` (not an error) |
| Database failure | Propagated through the existing `DomainError` handler, no raw SQL leakage |

## 19. Offline First
Not applicable (§1.14 — internal operator tool, connectivity assumed).

## 20. Local Data
Not applicable.

## 21. Localization
Response payload is data-only; all label/copy localization is a NextJS concern (N-01/N-02). `policy_category`/`stage_flagged` values are stable enum strings, translated client-side.

## 22. RTL
Not applicable to backend.

## 23. Analytics
This endpoint's calls are the source of `ai_moderation_queue_viewed` and `ai_moderation_detail_viewed` (§1.19) — fired client-side on successful fetch, not server-side, consistent with the rest of the Admin Portal's analytics pattern.

## 24. Performance
- Queue query must be index-backed on `(status, flagged_at DESC)` — no full table scan as queue volume grows.
- Detail query is a single joined read (`AiModerationQueueItem` + `AiSafetyEvent`), no N+1.
- Pagination required once queue volume exceeds a single page (cursor or offset, consistent with `BaseRepository.list_paginated` convention).

## 25. Security
- **The redaction boundary in §10.4 is this sub-feature's defining guarantee** — verified structurally, not just by convention, per the backend AI code-gen prompt's item 1.
- No transcript-level content is reachable through this endpoint under any query parameter combination.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Alembic, Pydantic v2, pytest-asyncio, `httpx` for integration tests.

## 27. Testing
- **Signature test (CI-blocking):** assert `AiModerationDetailResponse`'s schema/fields structurally cannot include a raw/unredacted field — a static schema-introspection test, not just a runtime-value check, mirroring C.26's own write-time-redaction guarantee test style.
- Unit: queue filter by `status`, filter by `policy_category`, combined filters.
- Unit: empty-queue response shape.
- Unit: 404 on unknown `{id}`.
- Unit: 403 on missing scope.
- Integration: seed a flagged `AiSafetyEvent` + `AiModerationQueueItem` pair, confirm both queue and detail responses surface it correctly with only redacted fields.

## 28. Documentation
Export OpenAPI; explicitly document in the `GET /v1/admin/ai-moderation/{id}` description that this endpoint **never** returns raw transcript content and that `POST .../transcript-access-request` (B-02) is the sole sanctioned exception — this is the feature's core trust claim and should be discoverable directly from the API docs, mirroring E.29's segregation-of-duties documentation practice.

## 29. AI Coding Agent Implementation Steps
- **Task 01 — Model & Migration**: `AiModerationQueueItem` table, FK to existing `ai_safety_event`, CHECK/index per §14.
- **Task 02 — Schemas**: `AiModerationQueueItemResponse`, `AiModerationDetailResponse` — confirm no raw-content field exists on either.
- **Task 03 — Repository**: `AiModerationRepository.get_queue()`, `.get_detail_joined()`, selecting only redacted columns from `AiSafetyEvent`.
- **Task 04 — Service**: `AiModerationQueueService` per §10.3.
- **Task 05 — Router**: `GET` endpoints with scope enforcement.
- **Task 06 — Redaction-boundary signature test**: schema-introspection test per §27.
- **Task 07 — Filter/empty-state/404/403 unit tests**.
- **Task 08 — Integration test**: seed-and-fetch happy path.
- **Task 09 — Documentation**: OpenAPI export with the redaction-boundary claim documented.
- **Task 10 — Final Code Review**: confirm zero code path in this module selects `AiSafetyEvent`'s columns beyond `model_version`/`input_redacted`/`output_redacted`/`category`/`occurred_at`/`event_id`.

## 30. Definition of Done
Queue and detail endpoints implemented, redaction boundary verified by a structural schema test (not just a runtime assertion), all filter/error/empty-state paths covered, OpenAPI documented.

## 31. Final Verification Checklist
- [ ] `ai_moderation_queue_item` table created, FK'd to existing `ai_safety_event` (no parallel raw-content table)
- [ ] Detail response schema structurally cannot contain a raw/unredacted field (tested)
- [ ] Queue filters by `status` and `policy_category` correctly
- [ ] Empty queue returns `200`/`items: []`, never an error
- [ ] 404/403 paths tested
- [ ] Index-backed queue query confirmed (no full scan)
- [ ] OpenAPI documents the redaction guarantee explicitly
- [ ] Tests green in CI
