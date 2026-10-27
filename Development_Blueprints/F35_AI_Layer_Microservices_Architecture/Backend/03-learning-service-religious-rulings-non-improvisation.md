# B-03 — Learning Service (Structural Religious-Rulings Non-Improvisation)

## 1. Feature Context
The service adapting Quran/Arabic/dua/quiz difficulty to a child's mastery level — whose most theologically sensitive guarantee is that any question touching rulings, aqeedah, halal/haram, prayer, or fiqh can never receive an improvised free-text answer, because the response schema for that category structurally has no field capable of carrying one.

## 2. Parent Feature
F.35 — AI Layer & Microservices Architecture

## 3. Sub-feature
1.3 Learning Service (ID: **B-03**)

## 4. Objective
Build `POST /v1/ai/learning/adapt-difficulty`, with a response schema that, for `is_religious_ruling_category=true` skill domains, structurally supports only an `approved_answer_id` reference or a `scholar_handoff` flag — no free-text answer field reachable for this category at all.

## 5. Business Requirements
- FR-1: separates educational hints from religious rulings.
- FR-3/FR-5: religious answers must map to approved knowledge cards; rulings/aqeedah/halal-haram/prayer/fiqh questions receive stricter confidence thresholds and review paths; legitimate scholarly-difference-of-opinion rulings are never improvised — route to an approved-answer set or scholar handoff; every response cites its approved source in parent/admin-visible history.
- §5 Backend AI prompt item 3 (highest-priority guarantee): the response schema must structurally only support `approved_answer_id`/`scholar_handoff`, with NO free-text answer field reachable for this category — schema-introspection test mandatory.
- Edge Case 2: a religious-rulings-category evaluation-suite failure is release-blocking regardless of strong aggregate metrics.

## 6. Existing Architecture
`ai` module, `app/ai/services/learning_service.py`, consulting E.29's approved knowledge-card corpus (scholar-approved content only) for the `approved_answer_id` reference.

## 7. Existing Code to Reuse
- E.29's approved-corpus/knowledge-card schema (read-only)
- A.9's mastery-tracking data (consumed, not duplicated)
- E.30's six-stage safety pipeline

## 8. Files to Create
- `app/ai/routers/learning_router.py`
- `app/ai/services/learning_service.py`
- `app/ai/repositories/skill_domain_repository.py`
- `app/ai/schemas/learning_schema.py` — two structurally distinct response schema variants (general vs. religious-ruling-category)

## 9. Files to Modify
- `app/ai/routers/__init__.py` — register router

## 10. Backend Requirements
- `LearningSchema` design: a discriminated-union or two-distinct-response-model approach where `GeneralDifficultyResponse` includes `recommended_difficulty` and MAY include a free-text `hint` field, while `ReligiousRulingResponse` (returned whenever `is_religious_ruling_category=true`) contains ONLY `approved_answer_id: UUID | None` and `scholar_handoff: bool` — there is no `hint`/`answer_text`/any free-text field defined anywhere on this second model, making an improvised answer for this category a type-level impossibility, not merely an unused field.
- `LearningService.adapt_difficulty()`: for religious-ruling-category skill domains, queries the approved knowledge-card corpus for a matching entry above the elevated confidence threshold; if found, returns its ID; if not, sets `scholar_handoff=true` — never generates or returns free text in either branch.
- Every `ReligiousRulingResponse` with a populated `approved_answer_id` carries the citation forward into parent/admin-visible history (via E.29's existing citation-attachment mechanism, not reimplemented).

## 11. Required API / API Contract
`POST /v1/ai/learning/adapt-difficulty` `{child_id, skill_id, mastery_state}` → `200 { "recommended_difficulty", "is_religious_ruling_category" }` for general domains, or `200 { "approved_answer_id", "scholar_handoff", "is_religious_ruling_category": true }` for ruling-category domains — two distinct response shapes, never merged into one model with optional free-text.

## 12. Database Requirements
No new tables — reads E.29's approved knowledge-card corpus and A.9's mastery data.

## 13. Validation
`skill_id` must map to a known skill-domain classification (general vs. religious-ruling-category), sourced from a maintained domain registry, not inferred ad-hoc per request.

## 14. Authentication
Internal service-to-service auth (called by A.5/A.8).

## 15. Authorization
Internal call scope only.

## 16. Error Handling
No matching approved answer above the confidence threshold: `scholar_handoff=true`, never an error and never a fallback to improvisation.

## 17. Security
This is one of the two highest-priority guarantees in the entire F.35 deliverable. Mandatory schema-introspection test: for the `ReligiousRulingResponse` model, enumerate its fields programmatically and assert none is a free-text/string-content field capable of carrying an improvised answer — only `approved_answer_id` (a UUID reference) and `scholar_handoff` (a boolean) exist. This test must fail loudly if any future code change adds such a field.

## 18. Analytics
`ai_learning_difficulty_adapted`, `ai_religious_question_routed_to_approved_answer`, `ai_religious_question_routed_to_scholar_handoff` per §1.19.

## 19. Performance
Indexed knowledge-card lookup by skill domain.

## 20. Library Requirements
FastAPI, Pydantic v2 (discriminated union / distinct models), SQLAlchemy 2.0 async. No new libraries.

## 21. Testing
Unit: skill-domain classification lookup. Integration: **mandatory** — schema-introspection test confirming `ReligiousRulingResponse` has zero free-text field; **mandatory** — a religious-ruling-category request with no matching approved answer above threshold returns `scholar_handoff=true`, never a generated answer; general-domain requests correctly return `recommended_difficulty` with the general schema shape; citation correctly attached for approved-answer responses.

## 22. Documentation
OpenAPI docstring explicitly documenting the two distinct response shapes and stating why the religious-ruling variant has no free-text field.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Define the Two Structurally Distinct Response Schemas**
Objective: `GeneralDifficultyResponse` and `ReligiousRulingResponse`, the latter with zero free-text fields. Files: `schemas/learning_schema.py`. Tests: **mandatory** — schema-introspection test. Definition of Done: test passes.

**Task 02 — Implement `SkillDomainRepository`**
Objective: Skill-domain classification lookup (general vs. religious-ruling-category) plus approved knowledge-card query. Files: `repositories/skill_domain_repository.py`. Dependencies: Task 01. Tests: classification tests. Definition of Done: tests pass.

**Task 03 — Implement `LearningService`**
Objective: Branch logic returning the correct schema variant per domain classification, elevated-confidence-threshold approved-answer lookup, scholar-handoff fallback. Files: `services/learning_service.py`. Dependencies: Task 02. Tests: **mandatory** — no-match-triggers-handoff-never-improvisation test. Definition of Done: test passes.

**Task 04 — Implement the Router Endpoint**
Objective: `POST /v1/ai/learning/adapt-difficulty`. Files: `routers/learning_router.py`. Dependencies: Task 03. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 05 — Wire Citation Attachment**
Objective: Approved-answer responses carry citation into parent/admin-visible history via E.29's mechanism. Dependencies: Task 04. Tests: citation-attachment test. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §21, both mandatory tests included. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm the schema-introspection test genuinely fails if a free-text field is added to `ReligiousRulingResponse` (verify by temporarily adding one locally and confirming the test catches it, then reverting). Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] `ReligiousRulingResponse` has zero free-text/string-content fields — mandatory schema-introspection test passing, proven to actually catch a violation
- [ ] No-matching-approved-answer scenario routes to `scholar_handoff=true`, never improvisation
- [ ] Citation correctly attached to parent/admin-visible history for approved-answer responses
- [ ] General and religious-ruling-category domains return distinct, non-mergeable response shapes

## 25. Definition of Done
Religious-rulings-category questions are structurally, type-level incapable of receiving an improvised answer — this platform's single most theologically-sensitive engineering guarantee, enforced by schema design rather than convention.
