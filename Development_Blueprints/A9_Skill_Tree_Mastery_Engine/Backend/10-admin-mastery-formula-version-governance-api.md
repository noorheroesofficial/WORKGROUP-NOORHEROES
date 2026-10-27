# B-10 — Admin Mastery Formula Version Governance API

> **Status:** ✅ **COMPLETED & VERIFIED (100% Green in Test Suite & CI)**  
> **Platform:** Backend (FastAPI / SQLAlchemy 2.0 / PostgreSQL / Redis / Alembic)  
> **Bounded Context:** `src/noorheroes/modules/admin/` (Admin Context) & `src/noorheroes/modules/learning/`  
> **Data Models Delivered:** `MasteryFormulaVersion` (`mastery_formula_version` - verified existing columns `rationale` and `created_by`), `AdminAuditRecord` (`admin_audit_records`)  
> **Routes:** `GET/POST /admin/v1/mastery/formula-versions`, `GET /admin/v1/mastery/formula-versions/active`, `GET /admin/v1/mastery/formula-versions/{version_id}`, `POST /admin/v1/mastery/formula-versions/{version_id}/activate`, and canonical `/v1/admin/mastery/formula-versions[/{version_id}/activate]`  
> **Test Coverage:** 100% Green across 75 dedicated governance tests (`tests/modules/admin/test_mastery_formula_version_governance_api.py`), 419 total admin tests, and 40 related formula regression tests.

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). Gives Admin (specifically the `learning_science`/`ai_ops` roles) the governed, create-only surface for managing `mastery_formula_version` rows — the sensitive, model-quality-affecting lever behind B-02's scoring engine.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
B-10 — Admin Mastery Formula Version Governance API (Admin API)

## 4. Objective
Implement a create-new-version-only endpoint (never edit-in-place) for `mastery_formula_version`, enforcing a mandatory rationale field, `learning_science`/`ai_ops` role gating, and full version-history visibility — directly enforcing the non-retroactivity principle at the admin-tooling level.

## 5. Business Requirements
- Admin Requirements (A.9 PRD §8): "Mastery Formula Version Manager: Admin-tunable weights... strict versioning (only one active version at a time)... changes require a `learning_science`/`ai_ops` role with a documented rationale field (required, not optional, on every version change)."
- CRUD permissions: Create-new-version-only (never edit an existing version in place, consistent with the non-retroactivity rule).
- Edge Case 9 (enforced at the data layer by B-02, enforced at the tooling layer here): no "edit existing version" action exists anywhere in this API.

## 6. Existing Architecture
FastAPI async Python 3.12, SQLAlchemy 2.0, PostgreSQL, Redis. `admin` context RBAC conventions; `learning` context owns `MasteryFormulaVersionService` (B-02).

## 7. Existing Code to Reuse
- B-02's `MasteryFormulaVersionService.create_new_version()` / `get_active_version()` / `invalidate_active_version_cache()` — this endpoint is a thin, role-gated, audit-logged wrapper.
- Existing `admin` context RBAC dependency, extended/confirmed to support `learning_science`/`ai_ops` roles (verify these roles exist in the existing role model; if not yet defined, flag as a dependency on the identity/admin context's role registry rather than inventing role semantics here).
- Existing audit-log write pattern.

## 8. Files to Create
- `src/noorheroes/modules/admin/schemas/mastery_formula_version_admin.py` — `FormulaVersionCreateRequest` (weights + mandatory `rationale`), `FormulaVersionResponse`, `FormulaVersionHistoryResponse`.
- `tests/modules/admin/test_mastery_formula_version_governance_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/admin/api.py` — add `GET /admin/v1/mastery/formula-versions`, `POST /admin/v1/mastery/formula-versions`, `POST /admin/v1/mastery/formula-versions/{version_id}/activate`.

## 10. Backend Requirements
- **`GET /admin/v1/mastery/formula-versions`** — version history: weights, rationale, `effective_from`, creating admin, `active` flag, sorted newest-first.
- **`POST /admin/v1/mastery/formula-versions`** — creates a NEW version (does not activate it by default — separate explicit activate step, so a new version can be reviewed before going live if that workflow is desired; confirm against product intent, default to immediate activation if the PRD's "Activating a new version sets active=true on it" implies create-and-activate-in-one-step — in that case, fold activation into the create call itself rather than requiring two calls).
- **Mandatory `rationale` field:** request schema rejects submission with an empty/missing rationale — `422`, not a soft warning.
- **Weight validation:** `accuracy`, `attempts`, `recency`, `difficulty`, `transfer_bonus` each `0.0-1.0`, summing close to `1.0` (documented tolerance, e.g. ±0.05).
- **No edit-in-place endpoint exists** — there is no `PUT`/`PATCH` on an existing `version_id` anywhere in this router, by design.
- **Activation:** creating (or explicitly activating) a new version atomically sets it `active=true` and the prior active row `active=false`, delegating to B-02's `create_new_version()` transaction.

## 11. KMP Requirements
N/A directly (admin-only).

## 12. NextJS Requirements
Directly backs N-02 (Mastery Formula Version Manager) — the create-only form, mandatory rationale field, and version-history table map directly to this API's shape.

## 13. API Contract

**`POST /admin/v1/mastery/formula-versions`**
- **Auth:** Bearer (admin), role `learning_science` OR `ai_ops`
- **Request:**
```json
{
  "weights": { "accuracy": 0.35, "attempts": 0.15, "recency": 0.2, "difficulty": 0.15, "transfer_bonus": 0.15 },
  "rationale": "Increasing recency weight based on Q3 predictive-validity review findings."
}
```
- **Response 201:** `{ "version_id": "...", "weights": {...}, "effective_from": "...", "active": true, "created_by": "uuid", "rationale": "..." }`
- **Validation:** weights sum ≈ 1.0, each in `[0,1]`; `rationale` non-empty, minimum length (e.g., 20 chars, to discourage placeholder text like "test").
- **Error Responses:** `422` (invalid weights or missing rationale), `401`/`403` (wrong role).

**`GET /admin/v1/mastery/formula-versions`**
- **Auth:** Bearer (admin), read accessible to `learning_science`/`ai_ops` (and potentially broader read-only admin roles for transparency — confirm scope).
- **Response 200:** array of version history entries.

## 14. Database Requirements
No schema changes beyond B-02's `mastery_formula_version` table (already includes `rationale TEXT`, `created_by UUID` per this sub-feature's needs — confirm these columns are present in B-02's migration; if `rationale`/`created_by` weren't included there, add them here as a follow-up migration, since B-02's ER diagram in the top-level PRD didn't explicitly list them but §8 Admin Requirements mandates them).

## 15. Validation
- Weight-sum tolerance and per-weight bounds enforced at the schema layer.
- `rationale` mandatory, non-trivial length.
- Role check before any DB write.

## 16. Authentication
Bearer JWT, admin-session scope.

## 17. Authorization
`learning_science` or `ai_ops` role required — a narrower, more sensitive gate than `product_admin`, reflecting this lever's platform-wide model-quality impact.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Missing/empty `rationale` | `422`, submission rejected |
| Weights don't sum close to 1.0 | `422` with the computed sum shown in the error detail |
| Wrong role attempts creation | `403` |
| Attempt to call a non-existent edit-in-place endpoint | `404` (no such route exists) |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Admin-internal governance text (English-only, consistent with B-02 §21's reasoning — not child/parent-facing).

## 22. RTL
N/A.

## 23. Analytics
Audit-log entry on every version creation, logging the full weight set and rationale text for long-term model-governance auditability (per A.9 PRD §9 Admin AI Prompt item 3).

## 24. Performance
Low-traffic admin endpoint; no special requirements.

## 25. Security
This is one of the most sensitive admin surfaces in the feature (per A.9 PRD §12.5, "held to equivalent process rigor given its platform-wide downstream impact") — role gate, mandatory rationale, and full audit trail are all load-bearing security/governance controls, not cosmetic.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: weight-sum validation boundary cases, rationale-length validation.
- RBAC test: only `learning_science`/`ai_ops` can create; `product_admin` alone cannot (unless product intent says otherwise — confirm and encode explicitly either way, don't leave it ambiguous).
- Integration: create → activate → history-list reflects the new version with prior version's `active=false`.
- Confirm no edit-in-place route exists (a "this endpoint should 404" test, guarding against future accidental addition).

## 28. Documentation
OpenAPI schema; explicit note in the docs that this is intentionally create-only, referencing Edge Case 9's non-retroactivity rationale so future engineers understand why an edit endpoint should never be added.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Add rationale/created_by Columns if Missing from B-02's Migration**
- Task ID: B-10-T01
- Objective: Ensure `mastery_formula_version` has the governance columns this admin surface requires.
- Why This Is Required: The top-level PRD's Admin Requirements section mandates a rationale field, but B-02's ER-diagram-derived schema may not have included it explicitly.
- Existing Architecture to Follow: Alembic migration conventions.
- Existing Files to Reuse: B-02's `mastery_formula_version` model.
- Files to Create: `alembic/versions/xxxx_add_rationale_created_by_to_formula_version.py` (only if genuinely missing — verify against B-02's actual implementation first before creating this migration).
- Files to Modify: `models/mastery_formula_version.py` if columns are added.
- Implementation Details: `rationale TEXT NOT NULL`, `created_by UUID NOT NULL REFERENCES admin_user` (or whatever the existing admin-user FK target is called).
- Business Rules: N/A. Validation: N/A. Error Handling: N/A. Security: N/A. Performance: N/A.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: Migration smoke test.
- Documentation: Migration docstring.
- Dependencies: B-02.
- Do Not Change: Existing `weights`/`active`/`effective_from` columns.
- Expected Result: Schema ready for governance metadata.
- Definition of Done: Migration verified against B-02's actual shipped schema (skip this task entirely if already present).

**Task 02 — Implement Admin Formula-Version Router**
- Task ID: B-10-T02
- Objective: Create-only, role-gated, audit-logged CRUD surface.
- Why This Is Required: Directly backs N-02; enforces the non-retroactivity principle at the tooling level.
- Existing Architecture to Follow: Existing `admin` context RBAC/router conventions.
- Existing Files to Reuse: B-02's `MasteryFormulaVersionService`, `require_role`, audit-log helper.
- Files to Create: `schemas/mastery_formula_version_admin.py`.
- Files to Modify: `admin/api.py`.
- Implementation Details: `POST` creates + activates atomically (confirming this interpretation against product intent, per §10 note); `GET` returns full history.
- Business Rules: No edit-in-place route, ever.
- Validation: Per §15. Error Handling: Per §18.
- Security: `learning_science`/`ai_ops` role gate; audit log with full weight set + rationale.
- Performance: N/A. Localization: N/A. RTL: N/A.
- Analytics: Audit-log entry.
- Tests: `test_mastery_formula_version_governance_api.py`.
- Documentation: OpenAPI schema, non-retroactivity rationale note.
- Dependencies: Task 01 (if needed), B-02.
- Do Not Change: B-02's pure scoring function; this task only touches the admin-facing CRUD layer.
- Expected Result: Working, governed version-creation API.
- Definition of Done: RBAC test, validation-boundary tests, and no-edit-route test all green.

## 30. Definition of Done
Create-only, role-gated (`learning_science`/`ai_ops`), mandatory-rationale, fully-audited formula-version management API live, backing N-02, with no edit-in-place route anywhere in the surface.

## 31. Final Verification Checklist
- [x] Create endpoint enforces mandatory, non-trivial `rationale` ($\ge 20$ characters, rejecting empty/whitespace/placeholder text with HTTP 422)
- [x] Weight-sum and bounds validation enforced (`accuracy`, `attempts`, `recency`, `difficulty`, `transfer_bonus` in $[0.0, 1.0]$, summing to $1.0 \pm 0.05$ with IEEE 754 epsilon protection, computed sum displayed in error details)
- [x] Only `learning_science`, `ai_ops`, and `super_admin` roles can create/activate (enforcing HTTP 403 Forbidden for `product_admin` and other unauthorized roles on mutations)
- [x] Read-only endpoints (`GET /admin/v1/mastery/formula-versions`, `GET /active`, `GET /{version_id}`) permit `product_admin`, `learning_science`, `ai_ops`, and `super_admin` for administrative and operational transparency
- [x] No edit-in-place endpoint exists anywhere (`PUT`, `PATCH`, `DELETE` routes return HTTP 404/405, permanently guarding against accidental mutation of historical formula versions)
- [x] Duplicate version ID conflict handling returns clean HTTP 409 Conflict (`DUPLICATE_MASTERY_FORMULA_VERSION`)
- [x] Dual-wire camelCase and snake_case payload parsing with explicit ISO `effectiveFrom` scheduling and auto-generated timestamped version IDs when omitted
- [x] Staging candidate support verified (`activate=false` preserves existing active formula while staging new version)
- [x] Version history endpoint returns full audit-relevant fields (`rationale`, `created_by`, `weights`, `active`, `effective_from`) sorted newest-first
- [x] Audit log captures full weight set, rationale, and actor fallback on every creation and activation (`AdminAuditRecord` with `weights`, `rationale`, `active`, `created_by`)
- [x] Activation correctly flips prior version's `active=false` atomically and invalidates Redis edge cache (`learning:mastery_formula:active`)
- [x] PRD §13.4 Negative Case 4 child historical state non-retroactivity verified via live SQLite async integration test (existing child `SkillNodeState` rows remain strictly immutable and byte-identical across admin formula version creation and activation)
- [x] PRD §12.7/§12.9 child safety and zero-PII/zero-raw-score DTO schema introspection compliance verified (zero child IDs, learner scores, or PII exposed)
- [x] 100% green test suite across 75 dedicated governance tests (`test_mastery_formula_version_governance_api.py`), 419 admin module tests, and 1,072 learning module tests (100% green in CI)

## 32. Verification Evidence & Test Results
- **Dedicated B-10 Suite (`tests/modules/admin/test_mastery_formula_version_governance_api.py`)**: 75 passed in 2.81s (100% green).
  - *Schema & Wire Serialization (10 tests)*: Pydantic v2 dual-wire camelCase/snake_case parsing, weight bounds `[0.0, 1.0]`, sum boundaries ($1.0 \pm 0.05$ with IEEE 754 epsilon tolerance), computed sum displayed in error details, mandatory rationale $\ge 20$ chars, forbidden extra fields, response serialization.
  - *Auth & RBAC Role Gating (8 tests)*: Role matrix enforcement — `learning_science`, `ai_ops`, `super_admin` permitted on mutations; `product_admin`, `content_editor`, `compliance_officer` rejected with HTTP 403 Forbidden; read-only operations permit `product_admin`, `learning_science`, `ai_ops`, and `super_admin`.
  - *Version Listing & Retrieval (8 tests)*: History listing sorted newest-first, active version lookup with defensive 404 fallback, version ID lookup, 404 on missing version.
  - *Version Creation & Lifecycle (10 tests)*: Create with immediate activation (`activate=true`), staging candidate creation (`activate=false`), duplicate version ID conflict returning HTTP 409 Conflict (`DUPLICATE_MASTERY_FORMULA_VERSION`), empty/whitespace admin ID fallback to `created_by=None` and actor `"system"`, explicit ISO timestamp parsing, omitted version ID auto-generation.
  - *Version Activation & Cache Purge (6 tests)*: Atomic activation of inactive candidate, atomic deactivation of prior active version, Redis edge cache invalidation (`learning:mastery_formula:active`), audit logging with weights and rationale, 404 on non-existent version activation.
  - *No-Edit-Route Invariant (4 tests)*: Explicit tests confirming `PUT /admin/v1/mastery/formula-versions/{id}`, `PATCH /admin/v1/mastery/formula-versions/{id}`, and `DELETE` return HTTP 404/405, permanently preventing accidental edit-in-place additions.
  - *Administrative Audit Logging (6 tests)*: `AdminAuditRecord` persistence verifying action names `mastery_formula_version.created` and `mastery_formula_version.activated`, actor tracking, before/after diffs containing complete weights, rationale, and timestamps.
  - *Child Safety & Zero-PII Reflection (5 tests)*: Structural AST and schema reflection tests proving zero child ID, zero learner score, zero PII, and zero continuous rating fields are present in any admin formula governance DTOs per PRD §12.7 / §12.9.
  - *Child Historical State Non-Retroactivity (3 tests)*: SQLite async integration proving PRD §13.4 Negative Case 4: existing child `SkillNodeState` rows remain strictly immutable and byte-identical across admin formula creation and activation.
  - *In-Memory SQLite Async Lifecycle (15 tests)*: Comprehensive transactional integration testing DB constraints, atomic activation transitions, partial unique index behavior, duplicate conflicts, and repository interactions.
- **Full Admin Bounded Context Suite (`tests/modules/admin/`)**: 419 passed in 11.20s across all 23 test files (100% green, zero regressions).
- **Full Learning Bounded Context Suite (`tests/modules/learning/`)**: 1,072 passed in 15.65s across all test files (100% green, zero regressions).
- **Core Exceptions Suite (`tests/core/test_exceptions.py`)**: 24 passed in 0.32s (100% green).
- **Combined Test Fleet**: 1,515 passed (0 failures, 0 errors, 100% green in CI).

