# B-06 — AI Moral Summary Generation & Safety Gating Service

## 1. Feature Context
The feature's signature child-safety control: every AI-generated moral summary must pass an Islamic-accuracy and child-safety validator before a child ever sees it, with a human-reviewed fallback always available and a hard latency budget so AI never delays the completion flow. A validator-gate failure allowing an unreviewed/unsafe moral to display is a zero-tolerance P0 per the PRD's rollback plan.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
1.6 AI Moral Summary Generation & Safety Gating Service (ID: **B-06**)

## 4. Objective
Implement an internal `ai_safety` service (`MoralSummaryService`) that generates or selects a moral summary through a strict chain — generate → validate (accuracy + child-safety) → confidence-gate → fallback — bounded by a hard 600ms end-to-end timeout, fail-closed to the human-reviewed version at every failure point, called synchronously (in-process) by B-04's completion flow.

## 5. Business Requirements
- FR-10: moral generated only from the approved story version/sources; vocabulary adapted to age band; Islamic-accuracy + child-safety validated; below-threshold confidence → human-reviewed fallback; accepted moral stored as a versioned artifact.
- Edge Case 5: AI service times out entirely (not just low-confidence) → falls back immediately, same as the low-confidence path — never blocks completion.
- §12.1 Threat Analysis: AI moral-summary content-safety failure mitigated by mandatory validator gate plus human-fallback, fail-closed on any timeout/uncertainty.
- §12.9 Pre-launch checklist: chaos test — kill validator service, confirm human fallback always used.
- Rollback trigger: any unreviewed/unsafe moral reaching a child is P0, zero tolerance, immediate `stories_ai_moral_summary_enabled` flag-off.

## 6. Existing Architecture
Lives in the existing `ai_safety` bounded context alongside `AISafetyService.evaluate_content()` and `SafetyAuditRepository`. No new router — this is an internal service called by B-04, mirroring the existing `AISafetyRouter`'s `POST /v1/ai-safety/evaluate` validator pattern but invoked in-process rather than over HTTP for the completion-flow hot path.

## 7. Existing Code to Reuse
- `modules/ai_safety/service.py::AISafetyService.evaluate_content()` (the accuracy/child-safety validator — reuse, do not reimplement)
- `modules/ai_safety/models.py::SafetyAuditLog`
- `infrastructure/ai/` AI provider infrastructure
- `common/base_service.py`

## 8. Files to Create
- `src/noorheroes/modules/content/story_models.py` — extend with `ContentMoralVersionOrm` (or add to `ai_safety` models if that ownership boundary fits better — coding agent should place it alongside `content_moral_version`'s natural owner per the PRD ER diagram, which ties it to `story_episode`)
- `alembic/versions/xxxx_add_content_moral_version.py`
- `src/noorheroes/modules/ai_safety/moral_summary_service.py` — `MoralSummaryService(BaseService)`
- `src/noorheroes/modules/ai_safety/moral_summary_repository.py` — `ContentMoralVersionRepository`
- `src/noorheroes/infrastructure/ai/moral_summary_provider.py` — thin wrapper around the AI provider infrastructure for the generation call
- `tests/modules/ai_safety/test_moral_summary_service.py`
- `tests/modules/ai_safety/test_moral_summary_chaos.py`

## 9. Files to Modify
- None outside this sub-feature's files; B-04 wires the call site into its own completion orchestration (documented in B-04, not here).

## 10. Backend Requirements
- `MoralSummaryService.get_moral_summary(episode_id, locale, age_band) -> MoralSummaryResult`: orchestrates generate → `AISafetyService.evaluate_content()` → confidence check → fallback lookup, all within a single 600ms budget enforced via `asyncio.wait_for` (or equivalent) at the outermost call.
- Generation step must only consume the approved story version's sources (query `story_episode`/associated approved content, never free-form/unlicensed input).
- Confidence gate: use AI version only if `ai_confidence_score >= threshold` (threshold read from config, not hardcoded) AND validator passes; otherwise query `ContentMoralVersionRepository.get_human_reviewed(episode_id, locale)`.
- On ANY step exceeding its slice of the 600ms budget (generation, validation, or DB lookup), immediately return the human-reviewed fallback — never partially block waiting.
- Persist the accepted moral (AI or fallback) as a new row in `content_moral_version` (versioned artifact) for editorial traceability and B-10's Parent Insights surfacing.
- Low-confidence AI results are still persisted (flagged, not shown to the child) so B-12's review queue can surface them.

## 11. API Contract
No public HTTP endpoint. Internal service contract:
```
MoralSummaryService.get_moral_summary(episode_id: UUID, locale: str, age_band: str) -> MoralSummaryResult
  # MoralSummaryResult: { source: "ai"|"human_fallback", text: str, moral_version_id: UUID }
```
Called exclusively from B-04's `CompletionService` within its 600ms sub-budget.

## 12. Database Requirements
- `content_moral_version`: FK `episode_id`; `CHECK (ai_confidence_score BETWEEN 0 AND 1) WHEN ai_generated = true`; index `(episode_id, locale)`; `human_reviewed` boolean gated by B-12's scholar approval workflow (read here, written there).

## 13. Validation
- `ai_confidence_score` constrained to `[0,1]` at the database CHECK-constraint layer, not just application validation.
- Generation input strictly scoped to the approved story version — no external/free-text prompt injection surface exposed to any caller.

## 14. Authentication
N/A — internal service; the calling endpoint (B-04) is already authenticated.

## 15. Authorization
N/A — internal service.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| AI generation call times out | Immediate fallback to human-reviewed moral |
| Validator (Islamic-accuracy/child-safety) fails | Immediate fallback, low-confidence/failed event logged for B-12 review |
| Confidence below threshold | Immediate fallback, logged for B-12 review |
| No human-reviewed fallback exists yet for this episode+locale | Fail-safe generic calm fallback text (configured platform default) — never block completion on a missing fallback; flagged urgently for editorial backfill |
| Validator service entirely unavailable | Fail-closed to human-reviewed fallback (chaos-tested) |
| 600ms budget exceeded at any step | Immediate fallback, regardless of which step was in progress |

## 17. Security
- Fail-closed design: any uncertainty (timeout, low confidence, validator failure, validator unavailability) resolves to the safest known-good content, never to raw/unvalidated AI output.
- AI generation scoped strictly to approved, licensed story content — no arbitrary prompt surface.
- All low-confidence/failed AI attempts logged to `SafetyAuditLog` for editorial/security review, never silently discarded.

## 18. Analytics
Emit via `OutboxWriter`: `moral_summary_shown` (with `source: ai|human_fallback`), `moral_summary_ai_confidence_score` (internal/aggregate, not child-facing).

## 19. Performance
- Hard 600ms end-to-end timeout is a correctness requirement, not just a performance target — verified by the mandatory chaos test.
- Fallback lookup path (`ContentMoralVersionRepository.get_human_reviewed()`) must itself be fast (indexed on `episode_id, locale`) since it is the safety net every failure path routes through.

## 20. Library Requirements
- Existing `infrastructure/ai/` provider abstraction (no new AI SDK beyond what is already integrated).
- `asyncio` timeout primitives already standard in the async FastAPI stack.

## 21. Testing
- Unit: confidence-threshold boundary logic, fallback-selection correctness, budget-config read (never hardcoded threshold).
- Integration: full generate→validate→fallback chain against a seeded approved-content fixture.
- **Mandatory chaos test**: kill/mock the validator service to raise/hang, confirm the human-reviewed fallback is used every time and the 600ms budget is never exceeded (per PRD §12.9 pre-launch checklist).
- Integration: missing-fallback-content edge case (generic platform default served, urgent-flag event logged).

## 22. Documentation
Module README documents the confidence-threshold config key (name only), the fail-closed matrix in §16, and the chaos-test requirement as a permanent CI gate — this is the feature's core child-safety guarantee and must be discoverable by any future maintainer.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `ContentMoralVersionOrm` Model & Migration**
Objective: Add the versioned-artifact table per the PRD ER diagram, including the CHECK constraint. Follow: existing SQLAlchemy/Alembic conventions. Business Rules: `CHECK (ai_confidence_score BETWEEN 0 AND 1) WHEN ai_generated = true` enforced at the DB layer. Do Not Change: `story_episode` schema beyond the FK relationship. Tests: migration smoke test, constraint-violation test (out-of-range score rejected). Definition of Done: clean migration, constraint verified.

**Task 02 — Implement `ContentMoralVersionRepository`**
Objective: Data access for versioned morals, including `get_human_reviewed(episode_id, locale)` and `insert_version()`. Follow: `BaseRepository`. Tests: fallback lookup correctness, versioned insert. Definition of Done: repository methods covered.

**Task 03 — Implement AI Generation Provider Wrapper**
Objective: `moral_summary_provider.py` scoping generation strictly to approved story sources, age-band-adapted vocabulary. Follow: existing `infrastructure/ai/` abstraction pattern. Security: no free-text/unlicensed input surface. Tests: generation scoped correctly, age-band adaptation. Definition of Done: unit tests pass.

**Task 04 — Implement `MoralSummaryService.get_moral_summary()` Orchestration**
Objective: generate → validate (reuse `AISafetyService.evaluate_content()`) → confidence-gate → fallback chain, wrapped in a hard 600ms timeout. Dependencies: Task 01–03, existing `AISafetyService`. Business Rules: fail-closed at every step per §16. Tests: confidence-boundary unit tests, full-chain integration test. Definition of Done: tests pass.

**Task 05 — Implement Mandatory Chaos Test**
Objective: Kill/mock the validator dependency, confirm fallback always used within budget (PRD §12.9 requirement). Files: `test_moral_summary_chaos.py`. Definition of Done: test passes reliably and is registered as a required CI check.

**Task 06 — Implement Missing-Fallback Safety Net**
Objective: Generic platform-default calm fallback text when no `human_reviewed` row exists yet for an episode+locale, plus an urgent editorial-backfill flag/log. Tests: missing-fallback edge case. Definition of Done: test passes, urgent flag verified in logs/audit table.

**Task 07 — Wire Low-Confidence Logging for B-12's Review Queue**
Objective: Persist low-confidence/failed AI attempts (flagged, not shown) so B-12 can surface them for scholar review. Dependencies: Task 01–02. Tests: low-confidence row correctly queryable by the shape B-12 expects. Definition of Done: test passes.

**Task 08 — Add Remaining Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm fail-closed behavior at every single failure point in §16 with no exceptions, confirm the 600ms budget is enforced at the outermost boundary (not just per-step), confirm no path exists for unvalidated AI text to reach a child. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] AI moral summary used only when confidence ≥ threshold AND validator passes
- [ ] Every failure mode (timeout, low confidence, validator failure, validator unavailable) falls back to human-reviewed moral
- [ ] Chaos test confirms fallback always used when validator service is killed
- [ ] Hard 600ms end-to-end budget enforced and never exceeded under any failure mode
- [ ] Generation strictly scoped to approved story sources — no free-text/unlicensed input surface
- [ ] `ai_confidence_score` constrained to `[0,1]` at the database layer
- [ ] Missing-fallback-content case served a safe generic default, never blocks completion
- [ ] Low-confidence attempts logged and queryable by B-12's review queue
- [ ] No unvalidated AI-generated text can reach a child under any code path
- [ ] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
The Moral Summary Service reliably delivers a scholar-safe moral to every completed story within a strict latency budget, fails closed under every failure condition including validator outage, and produces the versioned audit trail B-10 (Parent Insights) and B-12 (Scholar Review Queue) depend on.
