# B-05 — Evaluation Harness & Release Gate API

## 1. Feature Context
Parent PRD: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E30_AI_Moderation_Console.md`
Depends on: B-03 (`create_evaluation_case` resolve action), E.28 (RBAC)
Feeds into: N-05 (Evaluation Harness Dashboard); the platform CI/CD pipeline (external consumer of the release-gate check)

## 2. Parent Feature
E.30 — AI Moderation Console & Safety Evaluation Harness

## 3. Sub-feature
**Evaluation Harness & Release Gate API** (ID: B-05) — maintains the persistent evaluation-case test corpus, records evaluation-run results, and exposes the CI/CD-consumed release-gate check that blocks any AI-layer deploy with unresolved critical findings.

## 4. Objective
Ensure no AI-layer change can ever reach production while `critical_findings_count > 0` for its candidate model version — a literal, non-bypassable release blocker (§1.8), never overridden by schedule pressure.

## 5. Business Requirements
- FR-7: AI safety evaluation gates must pass with zero unresolved critical findings before any AI-layer change reaches production — a hard release-gating requirement, not a recommended practice.
- FR-11: evaluation-case creation produces a structured record used by the Evaluation Harness to test future model/policy changes against real flagged scenarios.
- Edge Case 5: zero *critical* findings but several *non-critical* findings → release may proceed; non-critical findings tracked, not ignored.
- Edge Case 7: an evaluation case referencing since-withdrawn E.29 content remains valid as a behavior test; the stale reference is clearly annotated, not silently broken.
- §10 DevOps: this release-gate check is a **mandatory CI/CD pipeline gate**, not optional, not bypassable by any role.

## 6. Existing Architecture
New submodule within `ai_moderation` (or standalone `evaluation_harness` submodule — start co-located per FAST-API-INSTRUCTIONS.md §14, split out only if scale warrants). No existing precedent in the codebase for a CI/CD-consumed gate endpoint; this is a genuinely new pattern, built with the same layered discipline as every other context.

## 7. Existing Code to Reuse
- `BaseRepository`, `BaseService`
- `core/exceptions.py::NotFoundError`, `ValidationError`
- B-03's `AiModerationQueueItem` (nullable FK source for evaluation cases)

## 8. Files to Create
- `src/noorheroes/modules/ai_moderation/evaluation_models.py` → `EvaluationCase`, `EvaluationRunResult`
- `src/noorheroes/modules/ai_moderation/evaluation_schemas.py` → `EvaluationCaseCreateRequest`, `EvaluationCaseResponse`, `EvaluationRunResultResponse`, `ReleaseGateResponse`
- `src/noorheroes/modules/ai_moderation/evaluation_repository.py` → `EvaluationRepository`
- `src/noorheroes/modules/ai_moderation/evaluation_service.py` → `EvaluationHarnessService(BaseService)`
- `src/noorheroes/modules/ai_moderation/evaluation_api.py` → `EvaluationHarnessRouter`
- `alembic/versions/xxxx_add_evaluation_case_and_run_result.py`
- `tests/modules/ai_moderation/test_release_gate.py`
- `tests/modules/ai_moderation/test_evaluation_case_creation.py`

## 9. Files to Modify
- `main.py` → mount `EvaluationHarnessRouter` under `/v1/admin/ai-evaluations`
- `src/noorheroes/modules/ai_moderation/resolution_service.py` (B-03) → call `EvaluationHarnessService.create_case_from_queue_item()` in the `create_evaluation_case` branch

## 10. Backend Requirements

### 10.1 Models
```python
class EvaluationCase(Base):
    __tablename__ = "evaluation_case"
    __table_args__ = (Index("ix_evaluation_case_created", "created_at"),)

    case_id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_ulid)
    source_queue_item_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("ai_moderation_queue_item.queue_item_id"), nullable=True
    )
    scenario: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class EvaluationRunResult(Base):
    __tablename__ = "evaluation_run_result"
    __table_args__ = (
        CheckConstraint("critical_findings_count >= 0", name="ck_eval_run_critical_nonneg"),
        Index("ix_evaluation_run_model_time", "model_version_candidate", "run_at"),
    )

    run_id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_ulid)
    model_version_candidate: Mapped[str] = mapped_column(String, nullable=False)
    critical_findings_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    non_critical_findings_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    run_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
```

### 10.2 Endpoints
| Method | Path | Auth | Purpose |
|---|---|---|---|
| POST | `/v1/admin/ai-evaluations` | `ai-moderation:read` | Add a case to the persistent test corpus |
| GET | `/v1/admin/ai-evaluations/runs/{id}` | `ai-moderation:read` | Fetch a run's findings breakdown |
| GET | `/v1/admin/ai-evaluations/release-gate?model_version=` | CI/CD service credential (machine-to-machine auth, distinct from interactive admin scopes — confirm the exact mechanism against E.28's service-account pattern before implementation) | Release-gate pass/block decision |

### 10.3 Service Logic
```python
class EvaluationHarnessService(BaseService):
    def __init__(self, repo: EvaluationRepository):
        self.repo = repo

    async def create_case_from_queue_item(self, queue_item_id: str) -> EvaluationCase:
        item = await self.repo.get_queue_item(queue_item_id)
        if item is None:
            raise NotFoundError(f"Queue item {queue_item_id} not found")
        scenario = await self.repo.build_scenario_snapshot(item)  # captures redacted prompt/output, category, filters
        case = EvaluationCase(source_queue_item_id=queue_item_id, scenario=scenario)
        return await self.repo.add(case)

    async def create_standalone_case(self, scenario: dict) -> EvaluationCase:
        return await self.repo.add(EvaluationCase(source_queue_item_id=None, scenario=scenario))

    async def get_release_gate_decision(self, model_version: str) -> dict:
        latest_run = await self.repo.get_latest_run_for_version(model_version)
        if latest_run is None:
            # No run yet recorded for this candidate — fail CLOSED (blocked), never open-by-default,
            # consistent with the fail-closed pattern established in media/safety_pipeline.py.
            return {"model_version_candidate": model_version, "gate_passed": False, "reason": "NO_EVALUATION_RUN_FOUND"}
        gate_passed = latest_run.critical_findings_count == 0
        return {
            "model_version_candidate": model_version,
            "gate_passed": gate_passed,
            "critical_findings_count": latest_run.critical_findings_count,
            "non_critical_findings_count": latest_run.non_critical_findings_count,
        }
```
> The fail-closed default (no run found ⇒ blocked) directly mirrors `media/safety_pipeline.py`'s established codebase convention: "Any stage failure, timeout, or ambiguous result => quarantined, NEVER pass." Applying that same discipline here means an AI-layer change with **no evaluation run at all** must never be treated as an implicit pass.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
Consumed by N-05 (Evaluation Harness Dashboard, Evaluation Run Detail, Release Gate Decision, Evaluation Case Detail).

## 13. API Contract

### `POST /v1/admin/ai-evaluations`
- **Request:** `{ "source_queue_item_id": "...|null", "scenario": {...} }`
- **Response 201:** `EvaluationCaseResponse`

### `GET /v1/admin/ai-evaluations/runs/{id}`
- **Response 200:** `{ "run_id", "model_version_candidate", "critical_findings_count", "non_critical_findings_count", "run_at" }`

### `GET /v1/admin/ai-evaluations/release-gate?model_version=`
- **Response 200:** `{ "model_version_candidate", "gate_passed": bool, "critical_findings_count", "non_critical_findings_count" }`
- **Response 200 (no run found):** `{ "gate_passed": false, "reason": "NO_EVALUATION_RUN_FOUND" }` — fail-closed, not a 404/error, so CI/CD tooling can treat it as a normal "blocked" decision without special-casing an error response

## 14. Database Requirements
- `evaluation_case`: FK `source_queue_item_id` nullable; index `(created_at DESC)`.
- `evaluation_run_result`: CHECK `critical_findings_count >= 0`; index `(model_version_candidate, run_at DESC)`.
- Both retained indefinitely as the platform's AI-safety-process evidentiary record (§4.5).

## 15. Validation
- `scenario` must be a non-empty JSON object.
- `model_version` query param required on the release-gate endpoint.

## 16. Authentication
Interactive endpoints: `Depends(get_current_admin)`. Release-gate endpoint: a **separate, non-interactive service-credential auth path** for CI/CD — do not reuse interactive admin JWTs for a machine-to-machine pipeline call; confirm the exact mechanism (service account, signed CI token, mTLS, etc.) against E.28's existing patterns rather than inventing one here.

## 17. Authorization
`require_admin_scope("ai-moderation:read")` for the interactive endpoints; the release-gate endpoint's authorization is CI/CD-infrastructure-scoped, not an admin RBAC scope.

## 18. Error Handling
| Scenario | Response |
|---|---|
| `create_case_from_queue_item` with unknown queue item | `404 NOT_FOUND` |
| Empty/invalid `scenario` | `422 VALIDATION_ERROR` |
| Release-gate query with no run on record | `200`, `gate_passed: false` (fail-closed, not an error) |
| Release-gate query, nonzero critical findings | `200`, `gate_passed: false` |
| Release-gate query, zero critical findings | `200`, `gate_passed: true` |

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
Not applicable server-side; `scenario` content may itself contain redacted-prompt text in whatever language it originated in — no translation performed here.

## 22. RTL
Not applicable to backend.

## 23. Analytics
`ai_evaluation_harness_run_completed` (with `critical_findings_count`, `non_critical_findings_count`), `ai_evaluation_release_gate_passed`, `ai_evaluation_release_gate_blocked` (§1.19).

## 24. Performance
Release-gate query is a single indexed lookup (`model_version_candidate`, latest `run_at`) — must be fast enough to sit inline in a CI/CD pipeline step without materially slowing deploys.

## 25. Security
- The release-gate endpoint is a **security-relevant CI/CD trust boundary** — a forged or spoofed "gate passed" response would defeat the entire zero-critical-findings guarantee; the service-credential auth mechanism (§16) must be robust against this.
- Fail-closed-on-no-run (§10.3) prevents a "just don't run the evaluation" bypass strategy.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Alembic, Pydantic v2, pytest-asyncio.

## 27. Testing
- **Signature test (CI-blocking, backend AI code-gen prompt item 6):** both the zero-critical-findings (gate passes) and nonzero-critical-findings (gate blocks) cases.
- Unit: fail-closed behavior when no evaluation run exists for a candidate version.
- Unit: `create_case_from_queue_item` correctly references the source queue item (backend AI code-gen prompt item 7) and is queryable afterward as part of the persistent corpus.
- Unit: since-withdrawn-content annotation surfaces correctly in a case's scenario snapshot (Edge Case 7) — this is primarily a data-shape/annotation concern; confirm exactly how "withdrawn" status is signaled from E.29 before implementing the annotation logic, rather than guessing the field name.
- Integration: full evaluation-case-creation → evaluation-run → release-gate flow.

## 28. Documentation
Export OpenAPI; explicitly document the fail-closed default and that this endpoint is the platform's mandatory, non-bypassable CI/CD release gate for AI-layer changes.

## 29. AI Coding Agent Implementation Steps
- **Task 01 — Models & Migration**: `EvaluationCase`, `EvaluationRunResult` per §14.
- **Task 02 — Confirm CI/CD service-credential auth mechanism** against E.28 before building the release-gate endpoint's auth dependency.
- **Task 03 — Schemas**.
- **Task 04 — Repository**: `get_queue_item()`, `build_scenario_snapshot()`, `get_latest_run_for_version()`.
- **Task 05 — Service**: `EvaluationHarnessService` per §10.3, including the fail-closed release-gate decision.
- **Task 06 — Router**: three endpoints per §10.2.
- **Task 07 — Wire B-03's `create_evaluation_case` branch** to call `create_case_from_queue_item()`.
- **Task 08 — Release-gate signature test** (both pass/block cases, CI-blocking).
- **Task 09 — Fail-closed and case-creation unit tests**.
- **Task 10 — Integration test**: full corpus-to-gate flow.
- **Task 11 — Documentation**.
- **Task 12 — Final Code Review**: confirm the release-gate endpoint cannot be spoofed/bypassed and that "no run" genuinely fails closed in every code path.

## 30. Definition of Done
Evaluation-case corpus and run-result recording implemented; release-gate endpoint verified fail-closed and correctly gating on `critical_findings_count`, with a CI-blocking test for both pass and block outcomes.

## 31. Final Verification Checklist
- [ ] `evaluation_case`/`evaluation_run_result` tables created per §14
- [ ] Release-gate endpoint blocks on `critical_findings_count > 0` (tested)
- [ ] Release-gate endpoint passes on zero critical findings (tested)
- [ ] Fail-closed behavior confirmed when no run exists for a candidate version
- [ ] `create_evaluation_case` correctly references source queue item and is corpus-queryable
- [ ] Since-withdrawn-content annotation confirmed against actual E.29 data shape, not guessed
- [ ] CI/CD service-credential auth mechanism confirmed against E.28, not invented
- [ ] Tests green in CI, signature test non-bypassable
