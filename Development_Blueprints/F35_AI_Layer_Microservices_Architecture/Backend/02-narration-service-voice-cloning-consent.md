# B-02 — Narration Service (Distinct Voice-Cloning Consent)

## 1. Feature Context
The service generating tone-aware narration and subtitle variants — whose single defining guarantee is that a child's own voice is never used as a cloning reference without a separate, explicit consent record, never inferred from general voice-feature consent.

## 2. Parent Feature
F.35 — AI Layer & Microservices Architecture

## 3. Sub-feature
1.2 Narration Service (ID: **B-02**)

## 4. Objective
Build `POST /v1/ai/narration/generate`, rejecting any `is_cloned_voice=true` request unless a distinct `voice_cloning` consent record exists, separately from general `voice_feature_general` consent.

## 5. Business Requirements
- FR-1: approved voices, bedtime limits, no child voice cloning without explicit consent.
- FR-7: push-to-talk-derived voice data handled per the platform's voice-data-minimization contract (raw audio deleted after response/scoring by default).
- §5 Backend AI prompt item 2 (highest-priority guarantee): `is_cloned_voice=true` requires a distinct `voice_cloning` consent record — general consent alone is insufficient.
- Edge Case 3: general voice-feature consent does NOT imply voice-cloning consent — the two are never bundled into a single permission.

## 6. Existing Architecture
`ai` module, `app/ai/services/narration_service.py`, consulting the new `voice_consent_record` table.

## 7. Existing Code to Reuse
- E.30's six-stage safety pipeline (narration output passes through it)
- A.5's existing voice-consent-tracking pattern where applicable (extended here with the distinct `voice_cloning` type, not duplicated)

## 8. Files to Create
- `app/ai/routers/narration_router.py`
- `app/ai/services/narration_service.py`
- `app/ai/repositories/voice_consent_repository.py`
- `app/ai/schemas/narration_schema.py`
- `alembic/versions/xxxx_create_voice_consent_record_table.py`

## 9. Files to Modify
- `app/ai/routers/__init__.py` — register router

## 10. Backend Requirements
- `VoiceConsentRepository.has_consent(child_id, consent_type)`: queries `voice_consent_record` for an active, granted record of the exact `consent_type` requested — `voice_feature_general` and `voice_cloning` are checked as two entirely independent lookups, never a single combined flag or an OR condition between them.
- `NarrationService.generate()`: when `is_cloned_voice=true`, calls `has_consent(child_id, 'voice_cloning')` specifically — if this returns `False` (including when only `voice_feature_general` is granted), rejects with `403 VOICE_CLONING_CONSENT_REQUIRED` before any generation attempt, never falling through to a "best effort" non-cloned generation as a silent substitute.
- Approved-voice-only selection for non-cloned variants; bedtime-hours limits enforced (cross-ref A.4's bedtime-mode contract).

## 11. Required API / API Contract
`POST /v1/ai/narration/generate` `{content_id, voice_profile_id, is_cloned_voice}` → `200` narration variant, or `403 VOICE_CLONING_CONSENT_REQUIRED`.

## 12. Database Requirements
`voice_consent_record(record_id PK, child_id FK, consent_type, granted, granted_at)`, `CHECK consent_type IN ('voice_feature_general','voice_cloning')`. Index `(child_id, consent_type)`.

## 13. Validation
`consent_type` restricted to the two enum values; `is_cloned_voice` boolean, defaults `false`.

## 14. Authentication
Internal service-to-service auth (called by A.3/A.5).

## 15. Authorization
Internal call scope only.

## 16. Error Handling
`403 VOICE_CLONING_CONSENT_REQUIRED` for the specific missing-cloning-consent case, distinguishable from a generic auth failure.

## 17. Security
Distinct, structurally separate consent-type checking is this sub-feature's single highest-priority guarantee — mandatory test confirms a fixture child with ONLY `voice_feature_general` consent granted (no `voice_cloning` record at all) is rejected with `403 VOICE_CLONING_CONSENT_REQUIRED` when `is_cloned_voice=true` is requested, proving the two consent types are never conflated anywhere in the check logic.

## 18. Analytics
`ai_narration_variant_generated`, `ai_voice_cloning_attempt_blocked_no_consent` (internal/security signal) per §1.19.

## 19. Performance
Indexed consent lookup on `(child_id, consent_type)`.

## 20. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Alembic. No new libraries.

## 21. Testing
Unit: consent-type-exact-match lookup logic. Integration: **mandatory** — child with only general consent rejected for cloned-voice request with `403 VOICE_CLONING_CONSENT_REQUIRED`; child with both consent types granted succeeds; child with neither consent type granted is rejected for BOTH general narration and cloned-voice requests as appropriate; bedtime-limit enforcement test.

## 22. Documentation
OpenAPI docstring explicitly stating the two consent types are checked independently and never inferred from one another.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Write Migration for `voice_consent_record`**
Objective: Table with `CHECK` on the two-value enum. Files: `alembic/versions/xxxx_create_voice_consent_record_table.py`. Tests: migration test. Definition of Done: schema created.

**Task 02 — Define Schemas**
Objective: `NarrationGenerateRequest`, `NarrationVariant`. Files: `schemas/narration_schema.py`. Dependencies: Task 01. Tests: schema validation. Definition of Done: tests pass.

**Task 03 — Implement `VoiceConsentRepository` with Exact-Type Lookup**
Objective: Independent, non-conflated consent-type queries. Files: `repositories/voice_consent_repository.py`. Dependencies: Task 01. Tests: **mandatory** — exact-type-match-only lookup test. Definition of Done: test passes.

**Task 04 — Implement `NarrationService` with Mandatory Consent Gating**
Objective: `is_cloned_voice=true` requires `voice_cloning` consent specifically, checked before any generation call. Files: `services/narration_service.py`. Dependencies: Task 03. Tests: **mandatory** — general-consent-only-rejected-for-cloning test. Definition of Done: test passes.

**Task 05 — Implement the Router Endpoint**
Objective: `POST /v1/ai/narration/generate` with `403` mapping. Files: `routers/narration_router.py`. Dependencies: Task 04. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 06 — Wire Bedtime-Limit Enforcement**
Objective: Reuse A.4's bedtime-mode contract. Dependencies: Task 05. Tests: bedtime-limit test. Definition of Done: test passes.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §21, mandatory test included. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm zero code path treats `voice_feature_general` consent as sufficient for a cloning request. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] `voice_cloning` and `voice_feature_general` checked as two entirely independent consent types — mandatory test passing
- [ ] General-consent-only child rejected with `403 VOICE_CLONING_CONSENT_REQUIRED` for cloned requests
- [ ] Approved-voice-only selection enforced for non-cloned variants
- [ ] Bedtime-hours limits enforced

## 25. Definition of Done
Voice cloning is provably gated by its own distinct, explicit consent record — never satisfied by, or confused with, general voice-feature consent — the platform's single highest-priority guarantee in this sub-feature.
