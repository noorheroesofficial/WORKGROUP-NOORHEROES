# B-04 — AI Permissions & Content Age Level Configuration API

## 1. Feature Context
Parents need fine-grained, per-child control over AI/voice features and content age-level eligibility — but these controls must be structurally restriction-only, never able to grant a child more capability than the platform's own age-band safety default (PRD C.23 FR-6, FR-7, FR-8).

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
1.4 AI Permissions & Content Age Level Configuration API (ID: **B-04**)

## 4. Objective
Extend `PATCH /v1/family/children/{id}/settings` (A.1's general child-settings contract) with AI-permission fields (`ai_enabled`, `voice_interaction_enabled`, `curated_only_mode`, `language_limit`) and a content fields (`content_age_level_override`), enforcing server-side that no combination of AI settings can grant capability beyond the platform-wide age-band default.

## 5. Business Requirements
- FR-6: parents can disable AI entirely, restrict voice interaction, set language limits, and choose "curated only" mode.
- FR-7 (hard ceiling principle): AI controls can only narrow capability, never expand it past platform-wide safety bounds, regardless of parent preference.
- FR-8: Content Age Level override adjusts the eligible band itself; downstream systems respect it exactly as the DOB-derived default, never bypassing hard age-band-exclusion guarantees elsewhere (cross-ref B.13, A.5).
- Edge Case 8: override below DOB-derived band fully supported, symmetric to above-band overrides.
- Acceptance Criteria: disabling AI entirely causes AI-touching features (e.g., A.5 pronunciation coaching) to fall back to listen-only/non-AI path.

## 6. Existing Architecture
Extends the existing child-settings contract established in A.1 (`PATCH /v1/family/children/{id}/settings`) rather than creating a parallel endpoint — reuses whatever `ChildProfile` settings model A.1 already defined, adding new fields to it. Lives conceptually in `modules/restrictions` for the AI-ceiling validation logic, but the endpoint itself is likely already routed through `modules/identity` (owner of `ChildProfile`) — **confirm the exact existing router location for this endpoint in A.1's implementation before adding fields**, per rule 30 (do not guess/duplicate an existing contract).

## 7. Existing Code to Reuse
- `modules/identity/models.py::ChildProfile` — extend with new nullable columns
- `modules/identity/schemas.py::ChildProfileUpdateRequest` — extend with new optional fields (confirm exact class name against actual A.1 implementation)
- `core/deps.py::get_current_parent`, `require_elevated_session`
- Platform-wide AI-safety age-band default table — confirm exact source (likely `modules/ai_safety` or a config table); **do not invent this table's location — verify against `ai_safety` module before implementing the ceiling check**

## 8. Files to Create
- `src/noorheroes/modules/restrictions/ai_ceiling.py` — `validate_ai_settings_within_ceiling(age_band, requested_settings, platform_default) -> None | raises ValidationError`
- `tests/modules/restrictions/test_ai_ceiling.py`
- `tests/modules/identity/test_settings_ai_permissions.py` (or equivalent location matching where the endpoint actually lives)

## 9. Files to Modify
- `modules/identity/models.py::ChildProfile` — add `ai_enabled BOOLEAN NULL`, `voice_interaction_enabled BOOLEAN NULL`, `curated_only_mode BOOLEAN NULL`, `language_limit VARCHAR NULL`, `content_age_level_override VARCHAR NULL`
- `modules/identity/schemas.py` — extend update/response DTOs with the above fields
- `modules/identity/service.py` (or wherever the settings PATCH handler lives) — add ceiling validation call before persisting AI fields
- `alembic/versions/xxxx_add_ai_permissions_content_age_level_to_child_profile.py`

## 10. Backend Requirements
- On PATCH, before persisting any AI field:
  1. Resolve `age_band` for the child (existing `AgeBand` enum from `common/utils/age_band.py`).
  2. Resolve platform-wide AI-permission default for that age band (source: confirm against `ai_safety` module / admin config table established by B-07's admin console).
  3. Validate that the requested settings combination is a **subset** of (or equal to, never a superset of) the platform default's allowed capability — since every field here is boolean-restrict-only or an enum-narrowing value, the validation is structurally "each requested value must be `<= default`" (e.g., `ai_enabled=true` requested when platform default for that age band is `ai_enabled=false` → reject/clamp to `false`).
  4. `content_age_level_override`: no ceiling check (any band, above or below DOB-derived, is valid per FR-8) — but validate against the supported age-band enum.
  5. Persist and emit `AiPermissionsConfigured`/`ContentAgeLevelOverridden` outbox events.
- This ceiling validation function must be pure and independently unit-testable (`ai_ceiling.py`), since it is the platform's core AI-safety-boundary enforcement point.

## 11. API Contract

### `PATCH /v1/family/children/{id}/settings`
- **Auth:** Bearer (parent) + step-up
- **Request (AI fields):** `{ "ai_enabled"?: true, "voice_interaction_enabled"?: false, "curated_only_mode"?: false, "language_limit"?: null }`
- **Request (content fields):** `{ "content_age_level_override"?: "6 to 9" }`
- **Response 200:** full updated child settings object (confirm exact shape against A.1's existing response schema)
- **Error Responses:** `401 UNAUTHORIZED`, `403 FORBIDDEN`, `404 CHILD_NOT_FOUND`, `422 VALIDATION_ERROR` (includes ceiling-violation rejection)

## 12. Database Requirements
Extends existing `child_profiles` table (owned by `modules/identity`, established in A.1) with the five new nullable columns listed in §9. No new table.

## 13. Validation
- `ai_enabled`, `voice_interaction_enabled`, `curated_only_mode`: booleans, validated against the ceiling per §10.
- `language_limit`: nullable string, validated against supported language codes (reuse `modules/localization`'s language registry).
- `content_age_level_override`: nullable string, validated against the platform's defined age-band enum values.

## 14. Authentication
`Depends(get_current_parent)` + `Depends(require_elevated_session)`.

## 15. Authorization
Family-ownership check on `child_id`.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Requested AI setting exceeds age-band ceiling | 422 VALIDATION_ERROR (or clamp-and-warn, per team preference — reject is safer and more auditable, recommended) |
| Invalid `content_age_level_override` value | 422 VALIDATION_ERROR |
| Child not found/not owned | 404 CHILD_NOT_FOUND |
| Missing step-up | 403 FORBIDDEN |

## 17. Offline First
N/A — configuration write requires connectivity.

## 18. Local Data
N/A (backend); consumed downstream by A.5 (AI/voice gating) and B.13 (age-band content filter) as read-only settings.

## 19. Localization
`language_limit` values are language codes, not display strings — client localizes for display.

## 20. RTL
N/A (backend).

## 21. Analytics
Backing source for `ai_permissions_configured` (with `setting` param) and `content_age_level_overridden`.

## 22. Performance
Low-volume, parent-initiated only.

## 23. Security
The AI-ceiling validation is a defining child-safety guarantee: this function must be reviewed with the same rigor as A.5's pronunciation-confidence-threshold config. No code path should allow a request body to bypass `ai_ceiling.py`.

## 24. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2. Reuses existing `AgeBand` enum and language registry.

## 25. Testing
- Unit: enumerate all AI-setting combinations; confirm none can request more capability than the age-band default and succeed.
- Unit: `content_age_level_override` accepted both above and below DOB-derived band.
- Integration: AI disabled for a child → confirm A.5's pronunciation flow reads this flag and falls back to listen-only (coordinate cross-feature test with A.5).
- Negative: attempt to PATCH `ai_enabled: true` for a child whose age-band default is `false` → rejected.

## 26. Documentation
OpenAPI description must state the ceiling principle explicitly: "these settings can only restrict, never expand, AI capability beyond the platform default for the child's age band."

## 27. AI Coding Agent Implementation Steps

**Task 01 — Confirm Existing Settings Endpoint Location**
- Objective: Locate A.1's actual `PATCH /v1/family/children/{id}/settings` implementation before adding fields (do not assume `modules/identity` without confirming file path against real codebase).
- Why This Is Required: Rule 30 — never guess existing architecture.

**Task 02 — Add New Columns to `ChildProfile`**
- Files to Modify: `modules/identity/models.py`
- Files to Create: `alembic/versions/xxxx_add_ai_permissions_content_age_level_to_child_profile.py`

**Task 03 — Extend Update/Response Schemas**
- Files to Modify: `modules/identity/schemas.py` (or actual confirmed location)

**Task 04 — Confirm/Locate Platform AI-Ceiling Default Source**
- Objective: Find where age-band AI defaults are stored (likely `ai_safety` module or a new admin-config table from B-07) before writing `ai_ceiling.py` against a guessed source.

**Task 05 — Implement `ai_ceiling.py`**
- Files to Create: `src/noorheroes/modules/restrictions/ai_ceiling.py`
- Implementation Details: Pure function, `validate_ai_settings_within_ceiling(age_band, requested, platform_default)`.
- Dependencies: Task 04.

**Task 06 — Wire Ceiling Validation into Settings Update Handler**
- Files to Modify: the confirmed settings service/handler from Task 01.
- Implementation Details: Call `ai_ceiling.py` before persisting any AI field; reject on violation.

**Task 07 — Add `content_age_level_override` Validation**
- Implementation Details: Validate against age-band enum; no ceiling check needed (symmetric override).

**Task 08 — Add Step-Up Enforcement**
- Confirm existing settings endpoint already enforces `require_elevated_session`; add if missing.

**Task 09 — Add Unit Tests for Ceiling Enforcement**
- Files to Create: `tests/modules/restrictions/test_ai_ceiling.py`

**Task 10 — Add Cross-Feature Integration Test with A.5**
- Objective: Confirm AI-disabled setting is correctly consumed by A.5's pronunciation flow.

**Task 11 — Add API Documentation**
- Objective: Document the ceiling principle explicitly.

**Task 12 — Final Code Review**
- Objective: Confirm no bypass path exists; confirm no duplicate settings endpoint was accidentally created instead of extending the existing A.1 contract.

## 28. Definition of Done
- AI-ceiling enforcement verified by exhaustive combination test.
- Content Age Level override verified in both directions.
- Cross-feature consumption by A.5 verified.
- Existing A.1 settings contract extended, not duplicated.

## 29. Final Verification Checklist
- [ ] Confirmed exact existing settings endpoint location before implementation (not guessed)
- [ ] No settings combination in tests exceeds age-band default
- [ ] `content_age_level_override` works both above and below DOB band
- [ ] Step-up required and tested
- [ ] A.5 integration test passes
- [ ] OpenAPI documents the ceiling principle
