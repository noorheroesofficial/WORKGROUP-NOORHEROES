# B-07 — AI Safety Intelligence Registries API

## 1. Feature Context
Parent PRD: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
Depends on: B-01 (queue data + `resolution_action` filter amendment), B-05 (`evaluation_run_result.model_version_candidate`)
Feeds into: N-06 (AI Safety Intelligence Registries screens)

**Origin note:** This blueprint fills a gap the original E.30 breakdown left explicitly open — §1.18 Screens 13–15 (False-Positive Feedback Log, Model Version / Blocked Topics Registry, Model Version Detail) have no endpoint contracted anywhere in the E.30 PRD's §3.4 API List. `Feature_F35_AI_Layer_Microservices_Architecture.md` was checked directly as the natural place such a registry might be owned — it defines no model-version-metadata store or blocked-topics table either (its own §4 lists only `voice_consent_record`/`ai_recommendation_log` as net-new tables). Rather than invent a dependency on a system that doesn't exist in either PRD, this blueprint builds both registries as **read-only aggregations over data E.30 already captures** (`ai_safety_event.model_version`, `ai_moderation_queue_item.stage_flagged`/`filters_triggered`-equivalent data, and B-05's `evaluation_run_result.model_version_candidate`) — no new external dependency, no new write path, no guessed schema.

## 2. Parent Feature
E.30 — AI Moderation Console & Safety Evaluation Harness

## 3. Sub-feature
**AI Safety Intelligence Registries API** (ID: B-07) — three read-only endpoints: the False-Positive Feedback Log (a filtered view of B-01's queue), the Model Version Registry (aggregated from already-captured `model_version` values), and the Blocked Topics Registry (aggregated from already-captured filter/category values).

## 4. Objective
Give Trust & Safety and AI/ML engineering a read-only, always-consistent view of which model versions have produced flagged interactions and what topics/filters are actually triggering — sourced entirely from data this console already writes, so there is no second system to keep in sync.

## 5. Business Requirements
- §1.18 Screen 13: False-Positive Feedback Log, Read-only, model-quality signal.
- §1.18 Screens 14–15: Model Version / Blocked Topics Registry, Model Version Detail.
- §11.5: false-positive and content-gap signals from this console directly inform model/corpus quality improvements.
- Parent PRD's "Do not guess" rule (§30): rather than inventing an endpoint against an unconfirmed F.35 contract, this blueprint grounds both registries in E.30's own already-specified tables.

## 6. Existing Architecture
Extends the `ai_moderation` context (B-01/B-03/B-05). No new tables — purely aggregation queries over `ai_safety_event` (read-only, existing), `ai_moderation_queue_item` (B-01), and `evaluation_run_result` (B-05).

## 7. Existing Code to Reuse
- B-01's `AiModerationRepository` and its (now amended) `resolution_action` filter for the False-Positive Feedback Log
- B-05's `EvaluationRepository.get_latest_run_for_version()`-style query patterns, extended to list distinct `model_version_candidate` values
- `noorheroes/modules/ai_safety/models.py::AiSafetyEvent.model_version` — the same field B-01 already reads

## 8. Files to Create
- `src/noorheroes/modules/ai_moderation/registry_schemas.py` → `FalsePositiveLogItemResponse`, `ModelVersionSummaryResponse`, `ModelVersionDetailResponse`, `BlockedTopicSummaryResponse`
- `src/noorheroes/modules/ai_moderation/registry_repository.py` → `AiSafetyRegistryRepository`
- `src/noorheroes/modules/ai_moderation/registry_service.py` → `AiSafetyRegistryService(BaseService)`
- `src/noorheroes/modules/ai_moderation/registry_api.py` → `AiSafetyRegistryRouter`
- `tests/modules/ai_moderation/test_registries.py`

## 9. Files to Modify
- `main.py` → mount `AiSafetyRegistryRouter` under `/v1/admin/ai-moderation` (false-positives is an alias of B-01's existing endpoint, documented but not separately routed) and `/v1/admin/ai-model-versions`

## 10. Backend Requirements

### 10.1 False-Positive Feedback Log — Alias, Not a New Endpoint
No new route. `N-06` calls B-01's existing `GET /v1/admin/ai-moderation?status=resolved&resolution_action=mark_false_positive` directly (per B-01's amendment). This blueprint documents that usage as the canonical way to serve Screen 13, rather than duplicating a query B-01 already supports.

### 10.2 Model Version Registry
```python
class AiSafetyRegistryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_model_versions(self) -> list[dict]:
        """Aggregates DISTINCT model_version values already captured on
        ai_safety_event, joined with evaluation run history from B-05 —
        no new table, no external F.35 dependency."""
        stmt = (
            select(
                AiSafetyEvent.model_version,
                func.count(AiSafetyEvent.event_id).label("flagged_interaction_count"),
                func.max(AiSafetyEvent.occurred_at).label("last_seen_at"),
            )
            .where(AiSafetyEvent.model_version.is_not(None))
            .group_by(AiSafetyEvent.model_version)
            .order_by(func.max(AiSafetyEvent.occurred_at).desc())
        )
        result = await self.session.execute(stmt)
        rows = result.all()
        return [
            {"model_version": r.model_version, "flagged_interaction_count": r.flagged_interaction_count, "last_seen_at": r.last_seen_at}
            for r in rows
        ]

    async def get_model_version_detail(self, model_version: str) -> dict:
        """Joins flagged-interaction stats (this table) with B-05's
        evaluation_run_result history for the same model_version string —
        the two tables share the identical model_version_candidate/model_version
        string space by construction (both originate from the same F.35
        model-deployment identifier), so this join requires no translation layer."""
        interaction_stats = await self._interaction_stats_for_version(model_version)
        eval_runs = await self._evaluation_runs_for_version(model_version)  # delegates to B-05's EvaluationRepository
        return {"model_version": model_version, **interaction_stats, "evaluation_runs": eval_runs}
```

### 10.3 Blocked Topics Registry
```python
    async def list_blocked_topics(self) -> list[dict]:
        """Aggregates DISTINCT `category` values (the same field B-01's
        detail response labels `policy_category`) across AiSafetyEvent rows
        where the interaction was blocked/redirected — this IS the platform's
        actual, currently-enforced blocked-topics taxonomy, derived from real
        enforcement data rather than a separately-maintained static list that
        could drift out of sync with what the pipeline actually blocks."""
        stmt = (
            select(AiSafetyEvent.category, func.count(AiSafetyEvent.event_id).label("occurrence_count"))
            .where(AiSafetyEvent.category.in_(("topic_blocked", "question_redirected")))
            .group_by(AiSafetyEvent.category)
        )
        result = await self.session.execute(stmt)
        return [{"category": r.category, "occurrence_count": r.occurrence_count} for r in result.all()]
```
> Note: `AiSafetyEvent.category` (per `ai_safety/models.py`) is currently a coarse three-value enum (`topic_blocked|question_redirected|question_approved`), not a fine-grained topic taxonomy (e.g., individual blocked keywords/phrases). If a finer-grained "blocked topics" list is genuinely required by Trust & Safety beyond this coarse category breakdown, that finer taxonomy would need to be introduced upstream in F.35's Prompt Filter stage output — this registry surfaces exactly what's currently captured, and does not invent additional granularity that isn't actually recorded anywhere yet. Flag this distinction to the user/product owner rather than silently presenting coarse data as if it were the detailed registry the PRD's screen name implies.

### 10.4 Endpoints
| Method | Path | Auth | Purpose |
|---|---|---|---|
| GET | `/v1/admin/ai-moderation?status=resolved&resolution_action=mark_false_positive` | `ai-moderation:read` | False-Positive Feedback Log (B-01 alias, §10.1) |
| GET | `/v1/admin/ai-model-versions` | `ai-moderation:read` | Model Version Registry |
| GET | `/v1/admin/ai-model-versions/{model_version}` | `ai-moderation:read` | Model Version Detail |
| GET | `/v1/admin/ai-blocked-topics` | `ai-moderation:read` | Blocked Topics Registry (coarse-category breakdown, see §10.3 caveat) |

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
Consumed by N-06, replacing its previously-blocked/speculative state with these three concrete endpoints.

## 13. API Contract

### `GET /v1/admin/ai-model-versions`
- **Response 200:** `{ "items": [ { "model_version", "flagged_interaction_count", "last_seen_at" } ] }`

### `GET /v1/admin/ai-model-versions/{model_version}`
- **Response 200:** `{ "model_version", "flagged_interaction_count", "last_seen_at", "evaluation_runs": [ { "run_id", "critical_findings_count", "non_critical_findings_count", "run_at" } ] }`
- **Errors:** `404 NOT_FOUND` if `model_version` has zero flagged interactions **and** zero evaluation runs on record.

### `GET /v1/admin/ai-blocked-topics`
- **Response 200:** `{ "items": [ { "category", "occurrence_count" } ] }` — the three-value coarse category breakdown per §10.3.

## 14. Database Requirements
None new — purely aggregation queries over existing tables (`ai_safety_event`, `ai_moderation_queue_item`, `evaluation_run_result`).

## 15. Validation
`{model_version}` path param — no format constraint beyond matching an existing recorded value; unknown values return `404`, not an empty `200`, since a registry detail page for a truly nonexistent version is a genuine not-found case (unlike the queue's empty-filter convention).

## 16. Authentication
`Depends(get_current_admin)`.

## 17. Authorization
`require_admin_scope("ai-moderation:read")` — same scope as B-01/B-03; no elevated permission needed since this is aggregated, already-redacted metadata, never transcript content.

## 18. Error Handling
| Scenario | Response |
|---|---|
| Unknown `model_version` in detail lookup | `404 NOT_FOUND` |
| Zero model versions recorded yet | `200`, `items: []` |
| Zero blocked-topic categories recorded yet | `200`, `items: []` |

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
`category` values (`topic_blocked`/`question_redirected`) are stable enum strings, translated client-side, consistent with B-01's convention.

## 22. RTL
Not applicable to backend.

## 23. Analytics
No new events beyond the general queue-view pattern; these are read-only registry views without their own dedicated events in the PRD's §1.19 list.

## 24. Performance
Aggregation queries are `GROUP BY` over indexed columns (`model_version`, `category`) — acceptable at current data volumes; revisit with a materialized view or scheduled rollup table only if `ai_safety_event` volume grows large enough to make live aggregation slow (not needed at launch).

## 25. Security
No new security surface — same scope, same already-redacted data sources as the rest of the console. The Blocked Topics Registry's coarse-category caveat (§10.3) is a data-completeness honesty concern, not a security one.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Alembic (none needed — no schema change), Pydantic v2, pytest-asyncio.

## 27. Testing
- Unit: `list_model_versions()` correctly aggregates distinct versions with counts and last-seen timestamps.
- Unit: `get_model_version_detail()` correctly joins interaction stats with B-05's evaluation-run history for the same version string.
- Unit: `list_blocked_topics()` correctly aggregates the three-category breakdown.
- Unit: unknown `model_version` detail lookup returns `404`.
- Integration: seed fixture `AiSafetyEvent` rows across two model versions and confirm the registry correctly distinguishes them.

## 28. Documentation
Export OpenAPI; explicitly document in the Blocked Topics Registry endpoint's description that it reflects the current coarse three-category enforcement taxonomy, not a fine-grained keyword/topic list — so registry consumers don't misread its granularity.

## 29. AI Coding Agent Implementation Steps
- **Task 01 — Schemas**: registry response DTOs per §13.
- **Task 02 — Repository**: `AiSafetyRegistryRepository` per §10.2/§10.3.
- **Task 03 — Service**: `AiSafetyRegistryService`, delegating to B-05's `EvaluationRepository` for the join in `get_model_version_detail()`.
- **Task 04 — Router**: three new endpoints (False-Positive Log remains B-01's existing route, documented not re-implemented).
- **Task 05 — Tests** per §27.
- **Task 06 — Documentation**: OpenAPI with the coarse-taxonomy caveat explicit.
- **Task 07 — Final Code Review**: confirm zero new tables were introduced and zero speculative F.35 dependency was added.

## 30. Definition of Done
All three registry surfaces implemented as read-only aggregations over already-captured E.30 data; zero new external dependency; coarse-taxonomy limitation explicitly documented rather than silently overstated.

## 31. Final Verification Checklist
- [ ] False-Positive Feedback Log served via B-01's amended filter, no duplicate endpoint
- [ ] Model Version Registry aggregates correctly, joins cleanly with B-05's evaluation-run data
- [ ] Blocked Topics Registry aggregates correctly, coarse-taxonomy caveat documented in OpenAPI
- [ ] Unknown `model_version` detail lookup returns `404`
- [ ] Zero new tables, zero new external dependencies
- [ ] Tests green in CI
