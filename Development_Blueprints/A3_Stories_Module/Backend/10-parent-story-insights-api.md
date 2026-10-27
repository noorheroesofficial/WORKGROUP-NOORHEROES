# B-10 — Parent Story Insights API

## 1. Feature Context
Read-only aggregation surface for the in-app Parent Area (K-09): what stories a child watched, time spent, quiz scores, and morals learned. Strictly scoped to the requesting parent's own family — never exposed to the child's own view in an analytics-framed way.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
1.10 Parent Story Insights API (ID: **B-10**)

## 4. Objective
Implement `GET /v1/children/{id}/story-insights` spanning `learning` and `content` data, aggregating completions, quiz results, and accepted moral summaries per child, gated to the requesting parent's own family.

## 5. Business Requirements
- FR-20: Parent Story Insights shows stories watched, time spent, quiz scores, morals learned; accessible only from the Parent Area.
- §1.14 Offline States: shows last-synced data with a "may not reflect today's offline activity yet" note if relevant.
- §1.12 Empty States: "Once [Child] watches their first story, you'll see their progress here."

## 6. Existing Architecture
Extends the existing `learning` module pattern (`LearningService.get_child_learning_progress()`) with a Stories-specific aggregation, joining `content`'s `story_completion` (B-04) and `content_moral_version` (B-06) tables. Parent-facing, authorized via existing family-scoping checks used elsewhere (e.g., `identity`'s child-profile listing).

## 7. Existing Code to Reuse
- `modules/learning/service.py::LearningService` (extend with a Stories-specific aggregation method, do not fork)
- `modules/content/completion_repository.py::StoryCompletionRepository` (B-04)
- `modules/ai_safety/moral_summary_repository.py::ContentMoralVersionRepository` (B-06)
- `core/deps.py::get_current_parent`
- `modules/identity/repository.py::ChildRepository.get_child_by_id_and_family()` (family-scoping pattern to reuse)

## 8. Files to Create
- `src/noorheroes/modules/learning/story_insights_schemas.py` — `StoryInsightsResponse`, `StoryInsightItem`
- `src/noorheroes/modules/learning/story_insights_service.py` — `StoryInsightsService(BaseService)`
- `tests/modules/learning/test_story_insights_service.py`
- `tests/modules/learning/test_story_insights_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/learning/api.py::LearningRouter` — add `GET /v1/children/{id}/story-insights`

## 10. Backend Requirements
- `StoryInsightsService.get_insights(parent_id, child_id)`: first confirms `child_id` belongs to `parent_id`'s family via the existing `ChildRepository.get_child_by_id_and_family()` pattern — `403`/`404` if not, before any aggregation query runs.
- Aggregates: list of watched stories (title, watched date, time spent derived from `episode_progress`), quiz scores (joined from the shared A.8 quiz-attempt table), moral learned (from `content_moral_version` via the accepted `moral_version_id` recorded at completion time).
- Empty-state-safe: zero completions returns a valid `200` with an empty array, not an error.

## 11. API Contract

### `GET /v1/children/{id}/story-insights`
- Auth: Bearer (parent session, scoped to own family's child). Response 200: aggregated watched stories, time spent, quiz scores, morals learned. Errors: `403 FORBIDDEN` (child not in requesting parent's family), `404 CHILD_NOT_FOUND`.

## 12. Database Requirements
- No new tables — reads `story_completion` (B-04), `episode_progress` (B-02), `content_moral_version` (B-06), and the existing quiz-attempt table (`learning` module).

## 13. Validation
- `child_id` path param validated as an existing child belonging to the authenticated parent's family before any other processing.

## 14. Authentication
Bearer parent session via `get_current_parent`.

## 15. Authorization
Family-scoping check is the authorization mechanism — mirrors the existing pattern already used for child-profile access elsewhere in `identity`.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Child not in requesting parent's family | `403 FORBIDDEN` |
| Unknown child ID | `404 CHILD_NOT_FOUND` |
| Zero watched stories | `200` with empty array |
| Underlying data source (quiz table) temporarily unavailable | Return partial insights (stories/morals) with quiz scores omitted and a degraded-data flag, rather than failing the whole response |
| Database failure | `503`, logged |

## 17. Security
- Strict family-scoping check before any query — this is the primary defense against one parent viewing another family's child data.
- No child-facing exposure of this endpoint or its data shape (Parent Area only, enforced client-side per K-09 and conceptually reinforced here by requiring `get_current_parent`, never `get_current_child`).

## 18. Analytics
Emit via `OutboxWriter`: `parent_story_insights_viewed`.

## 19. Performance
- Aggregation query joins across three tables scoped by `child_id` with existing indexes (`story_completion(child_id, completed_at DESC)`, `episode_progress(child_id, updated_at DESC)`) — no full-table scans.

## 20. Library Requirements
No new libraries.

## 21. Testing
- Unit: family-scoping rejection (parent A requesting child of parent B → `403`), empty-state response shape.
- Integration: full aggregation correctness against a seeded multi-story, multi-quiz fixture; degraded-partial-response behavior when the quiz data source is mocked unavailable.

## 22. Documentation
Update OpenAPI schema.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Implement `StoryInsightsResponse`/`StoryInsightItem` Schemas**
Objective: Define the aggregated response shape. Follow: existing Pydantic v2 conventions. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement Family-Scoping Guard**
Objective: Reuse `ChildRepository.get_child_by_id_and_family()` pattern to reject cross-family access before any aggregation runs. Tests: cross-family rejection test (the primary security test for this endpoint). Definition of Done: test passes.

**Task 03 — Implement `StoryInsightsService.get_insights()` Aggregation**
Objective: Join `story_completion`, `episode_progress`, `content_moral_version`, and the quiz-attempt table into the response shape. Dependencies: Task 01–02, B-04, B-06. Business Rules: empty state returns valid empty array, not an error. Tests: full aggregation correctness, empty-state case. Definition of Done: tests pass.

**Task 04 — Implement Degraded-Partial-Response Handling**
Objective: If the quiz-attempt data source is unavailable, return stories/morals with quiz scores omitted and a flag, rather than failing entirely. Tests: mocked-unavailable quiz source test. Definition of Done: test passes.

**Task 05 — Add Router Endpoint**
Objective: Wire `GET /v1/children/{id}/story-insights` into `LearningRouter`. Tests: covered by Task 06. Definition of Done: endpoint live, documented.

**Task 06 — Add Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all green in CI.

**Task 07 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify. Definition of Done: non-breaking diff confirmed.

**Task 08 — Final Code Review**
Objective: Confirm the family-scoping check is the very first thing evaluated in the request path, before any data touches the response. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [x] Family-scoping check rejects cross-family access with `403` before any aggregation query runs
- [x] Unknown child ID returns `404`
- [x] Zero-activity child returns valid empty-array `200`, not an error
- [x] Quiz-data-source outage degrades gracefully (partial response), never a full failure
- [x] Endpoint requires `get_current_parent`, never accessible via a child session
- [x] `parent_story_insights_viewed` analytics event emitted
- [x] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
Parents can see an accurate, family-scoped, gracefully-degrading view of their child's story activity — feeding K-09's Parent Story Insights screens and the broader C.22 Per-Child Reports feature.
