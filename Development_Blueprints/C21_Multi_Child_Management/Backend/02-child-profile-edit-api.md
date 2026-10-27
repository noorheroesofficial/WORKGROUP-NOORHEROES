# B-02 — Child Profile Edit API

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management. Powers the "Edit" action from the Child Management List, reusing the A.1 Add/Edit Child form fields but adding the DOB-immutability rule that distinguishes ongoing management from first-time onboarding.

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**B-02 — Child Profile Edit API** (`PATCH /v1/family/children/{id}`)

## 4. Objective
Allow a parent to update any editable field of an existing child profile, while enforcing that Date of Birth becomes permanently locked after the first save (FR-7), and that duplicate nicknames within the same family are rejected (FR-9) — all behind step-up authentication (FR-11).

## 5. Business Requirements
- FR-6: reuses A.1 field set (nickname, DOB picker, avatar grid, language/level selectors, interest chips, daily-goal slider, AI permission toggle).
- FR-7: DOB immutable after first save except via Support (B-10).
- FR-9: duplicate nicknames within a family rejected inline at save time.
- FR-11: every mutating action requires step-up authentication.
- Edge Case #1: DOB edit attempt post-lock → field locked with explanation, not a hard error the user can't recover from.
- Edge Case #7: step-up expires mid-form → fresh step-up prompt on retry, not silent failure/save.
- Edge Case #8: concurrent edits from two devices → last-write-wins at DB layer, each UI must re-fetch before allowing save.

## 6. Existing Architecture
FastAPI Router → `IdentityService` → `ChildRepository` → PostgreSQL, per `FAST-API-INSTRUCTIONS.md`. Step-up enforcement reuses C.19's `require_elevated_session` dependency — do not reimplement.

## 7. Existing Code to Reuse
- `require_elevated_session(parent, redis)` (`core/deps.py`) — C.19's step-up middleware.
- `ChildRepository.get_child_by_id_and_family()` — existing lookup, reuse for ownership verification.
- `ChildProfileUpdateRequest` schema — extend with the field set below rather than forking.
- `ValidationError`, `ConflictError`, `NotFoundError` from `core/exceptions.py`.

## 8. Files to Create
- `alembic/versions/xxxx_add_dob_immutability_trigger.py` — DB trigger migration (see Task 01).

## 9. Files to Modify
- `modules/identity/api.py` — extend `PATCH /v1/family/children/{id}` route to require `require_elevated_session`.
- `modules/identity/service.py` — add `update_child_profile()` business logic (DOB-lock check, duplicate-nickname check).
- `modules/identity/repository.py` — add `update()` respecting optimistic concurrency (`version` column via `BaseRepository.update_with_optimistic_lock`).
- `modules/identity/schemas.py` — finalize `ChildProfileUpdateRequest` (all fields optional/partial-update).
- `tests/modules/identity/test_children_edit.py` — new test module.

## 10. Backend Requirements
- Partial update semantics: only supplied fields change.
- DOB field, if present in the payload and differs from stored value while `dob_locked_at IS NOT NULL`, is rejected at the **application layer** (fast-fail, `422 DOB_IMMUTABLE`) *and* the **database layer** (defense-in-depth trigger — see Task 01) rejects any raw UPDATE that changes `dob` post-lock.
- Nickname uniqueness enforced by `UNIQUE(family_id, nickname)` constraint (DB-layer) with a friendly `409 DUPLICATE_NICKNAME` translation at the service layer.
- On first successful save that includes a DOB value and `dob_locked_at IS NULL`, set `dob_locked_at = now()`.

## 11. KMP Requirements
- `ChildManagementViewModel` (K-03) must call `ParentGateLauncher.requireParentAuth()` before invoking the repository's edit method.
- DOB field rendered read-only client-side whenever `dobLockedAt` is non-null — this is a UX affordance, not the source of truth; the server is authoritative.

## 12. NextJS Requirements
Not applicable — parent-facing endpoint only.

## 13. API Contract

**`PATCH /v1/family/children/{id}`**
- **Auth:** Bearer + step-up (`Depends(get_current_parent)` + `Depends(require_elevated_session)`).
- **Request:**
```json
{
  "nickname": "string?",
  "dob": "date?",
  "avatarId": "string?",
  "languageLevel": "string?",
  "interests": ["string"]?,
  "dailyGoalMinutes": "int?",
  "aiPermission": "bool?"
}
```
- **Response 200:** updated `ChildProfileResponse` (per B-01 §13 shape).
- **Error Responses:**
  - `401` — missing/invalid session or missing step-up marker.
  - `404` — child not found / not owned by family.
  - `409 DUPLICATE_NICKNAME` — nickname already used within family.
  - `422 DOB_IMMUTABLE` — attempted DOB change after `dob_locked_at` is set.
  - `409 OPTIMISTIC_LOCK_CONFLICT` — stale `version` supplied (concurrent-edit case).

## 14. Database Requirements
- `child.dob_locked_at` trigger: reject `UPDATE ... SET dob = X` where `dob_locked_at IS NOT NULL` and `X != OLD.dob`.
- `UNIQUE(family_id, nickname)` constraint (verify present from B-03's migration; if not yet applied, include here).
- `child.version` column (via `TimestampMixin`) for optimistic locking.

## 15. Validation
- Pydantic-level: field types, `dailyGoalMinutes` within platform bounds, `interests` against the known interest-chip enum.
- Business-level: DOB immutability, nickname uniqueness — both re-verified server-side regardless of client-side UI locking.

## 16. Authentication
Bearer parent session, required.

## 17. Authorization
Step-up (`require_elevated_session`) required on every call — no mutating shortcut with only a standard session token, per FR-11 and the NFR "Step-Up Auth Coverage."

## 18. Error Handling
| Scenario | Response |
|---|---|
| DOB change attempted post-lock | `422 DOB_IMMUTABLE` |
| Duplicate nickname | `409 DUPLICATE_NICKNAME` |
| Child not found/not owned | `404` |
| Step-up marker missing/expired | `401`, client re-triggers step-up flow |
| Concurrent stale write | `409 OPTIMISTIC_LOCK_CONFLICT` |

## 19. Offline First
N/A server-side; K-03 blocks the save action entirely while offline (mutating actions require connectivity per §1.14).

## 20. Local Data
N/A — see K-03/K-09.

## 21. Localization
`interests` and `languageLevel` are enum codes, not localized strings — translation happens client-side against the localization dictionary.

## 22. RTL
N/A backend.

## 23. Analytics
None server-side; `child_edit_started`/`child_edit_saved`/`child_duplicate_nickname_rejected`/`child_dob_edit_attempted_blocked` fire client-side.

## 24. Performance
Single-row update with two cheap pre-checks (DOB-lock, nickname-uniqueness) resolved via existing indexes; target consistent with p95 < 800ms save target (§1.8).

## 25. Security
- DOB-immutability trigger is the primary control — the only sanctioned bypass is B-10's audited Support tool.
- Step-up requirement prevents a stolen/leaked standard session token from mutating profile data.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: DOB-lock rejection at service layer.
- Unit: DB-layer trigger rejection — write a test attempting a raw UPDATE bypassing the service layer and assert it still fails.
- Unit: duplicate-nickname rejection.
- Integration: full edit flow happy path.
- Integration: step-up-missing rejection.
- Integration: concurrent edit — two updates racing, second gets `409 OPTIMISTIC_LOCK_CONFLICT`.

## 28. Documentation
Update OpenAPI description to document `422 DOB_IMMUTABLE` and `409 DUPLICATE_NICKNAME` explicitly as documented error responses (not just generic 4xx).

## 29. AI Coding Agent Implementation Steps

**Task 01 — DOB Immutability Database Trigger**
- **Objective:** Guarantee DOB cannot be altered post-lock even via a direct SQL path.
- **Why Required:** This is the PRD's single highest-priority guarantee (§5 backend AI prompt, item 1) — "Irreversibility Integrity" depends on a control beneath the application layer.
- **Files to Create:** new Alembic migration adding a PostgreSQL trigger function `enforce_dob_immutability()` fired `BEFORE UPDATE ON child`.
- **Implementation Details:** `IF OLD.dob_locked_at IS NOT NULL AND NEW.dob IS DISTINCT FROM OLD.dob THEN RAISE EXCEPTION 'DOB_IMMUTABLE';`.
- **Tests:** raw-SQL test bypassing the ORM service layer, asserting the exception is raised.
- **Do Not Change:** Do not alter unrelated triggers or the `TimestampMixin` behavior.
- **Definition of Done:** Trigger fires reliably under both ORM and raw-SQL update paths.

**Task 02 — Service-Layer Update Logic**
- **Objective:** Implement `update_child_profile()` with DOB-lock pre-check, nickname-uniqueness pre-check, and `dob_locked_at` first-save assignment.
- **Files to Modify:** `modules/identity/service.py`.
- **Business Rules:** Set `dob_locked_at = Clock.now()` the first time a DOB is persisted (whether at creation via B-03 or first edit here, whichever occurs first).
- **Error Handling:** Translate DB `UNIQUE` violation into `ConflictError("DUPLICATE_NICKNAME")`; translate DB trigger exception into `ValidationError("DOB_IMMUTABLE")`.
- **Tests:** Service-layer unit tests for both pre-check paths.
- **Definition of Done:** Both application-layer and database-layer guards independently verified.

**Task 03 — Optimistic Locking Wiring**
- **Objective:** Prevent silent last-write-wins data corruption beyond what §1.10 Edge Case #8 explicitly allows (last-write-wins is acceptable *product* behavior, but must not corrupt partial fields).
- **Files to Modify:** `modules/identity/repository.py` — use `BaseRepository.update_with_optimistic_lock`.
- **Tests:** Concurrent-update integration test.
- **Definition of Done:** Second concurrent writer receives a clear conflict response rather than a silently merged/corrupted row.

**Task 04 — Router Wiring & Step-Up Enforcement**
- **Objective:** Attach `require_elevated_session` to the route.
- **Files to Modify:** `modules/identity/api.py`.
- **Security:** Confirm via test that calling this endpoint with only a standard parent token (no step-up marker) is rejected.
- **Definition of Done:** No mutating code path reachable without step-up.

## 30. Definition of Done
DOB immutability enforced at both layers; duplicate-nickname rejected; step-up required; optimistic locking prevents silent corruption; full test suite green.

## 31. Final Verification Checklist
- [ ] Database trigger verified via raw-SQL bypass test
- [ ] Service-layer DOB-lock and duplicate-nickname checks tested
- [ ] Step-up enforcement tested (rejection without it)
- [ ] Optimistic-lock conflict tested under concurrency
- [ ] OpenAPI documents all named error codes
- [ ] No PostgreSQL/Redis credential changes
