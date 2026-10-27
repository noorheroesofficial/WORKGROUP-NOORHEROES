# B-02 — Child Display Locale Preference API

## 1. Feature Context
Powers the Profile screen's language toggle. The child's **display language** is a distinct concept from content locale-eligibility (governed elsewhere by the platform's age/locale content-filtering system) — this endpoint only stores which language the app UI itself renders in for that child.

## 2. Parent Feature
Feature B.16 — Child Profile (Bottom Tab)

## 3. Sub-feature
1.2 Child Display Locale Preference API (ID: **B-02**)

## 4. Objective
Implement `PATCH /v1/children/{id}/preferences`, backed by a new one-row-per-child `child_preferences` table, with the same strict `id`-matches-session enforcement as B-01, validated against the existing supported-language registry.

## 5. Business Requirements
- FR-6: The language toggle changes the display language only, takes effect immediately, no app restart required, does not affect content-locale eligibility.
- Data Isolation: same strict per-child scoping guarantee as every other Profile endpoint.
- Non-mutating-risk: this is the only mutating action introduced by B.16, and it is low-stakes/idempotent by nature — setting the same value twice has no adverse effect.

## 6. Existing Architecture
New table, but reuses `modules/localization/repository.py::LanguageRepository` (existing, per `FAST-API-INSTRUCTIONS.md` §5.6) to validate the submitted `display_locale` against the platform's actual supported-language list rather than a hardcoded/duplicated enum.

## 7. Existing Code to Reuse
- `modules/localization/repository.py::LanguageRepository` (existing — validation lookup only)
- `core/deps.py::get_current_child` → `ChildSessionContext`
- `core/exceptions.py::ChildScopeViolationError`, `ValidationError`
- `common/base_repository.py::BaseRepository[ModelT]` (for `ChildPreferencesRepository`)
- `infrastructure/db/base.py::Base`, `TimestampMixin`

## 8. Files to Create
- `src/noorheroes/modules/identity/preferences_models.py` — `ChildPreferencesOrm`
- `src/noorheroes/modules/identity/preferences_repository.py` — `ChildPreferencesRepository`
- `src/noorheroes/modules/identity/preferences_service.py` — `ChildPreferencesService`
- `src/noorheroes/modules/identity/preferences_schemas.py` — `ChildPreferencesUpdateRequest`, `ChildPreferencesUpdateResponse`
- `alembic/versions/xxxx_create_child_preferences.py`
- `tests/modules/identity/test_child_preferences.py`

## 9. Files to Modify
- `src/noorheroes/modules/identity/api.py` — add `PATCH /v1/children/{id}/preferences` route
- `src/noorheroes/modules/identity/deps.py` — add `get_child_preferences_service` factory

## 10. Backend Requirements
- `ChildPreferencesService.update_locale(child_ctx, path_child_id, display_locale)` performs the same strict `id == child_ctx.child_id` check as B-01, first, before touching the database.
- Validate `display_locale` against `LanguageRepository`'s active supported-language list; reject codes not present there with `422 UNSUPPORTED_LOCALE`.
- Upsert semantics: `ChildPreferencesRepository.upsert(child_id, display_locale)` — `INSERT ... ON CONFLICT (child_id) DO UPDATE`, so repeated identical calls are true no-ops at the data level, not just functionally idempotent.
- No outbox event required — this is a simple, non-reward-affecting, non-mastery-affecting preference; do not wire `OutboxWriter` for this action (avoid inventing unnecessary event traffic for a low-stakes setting).

## 11. API Contract

### `PATCH /v1/children/{id}/preferences`
- **Auth:** Bearer, child-mode session (`get_current_child`)
- **Authorization:** path `id` must equal `child_ctx.child_id`
- **Request:** `{ "display_locale": "ar" }`
- **Response 200:** `{ "updated": true }`
- **Errors:** `401` unauthenticated · `403 CHILD_MISMATCH` · `422 UNSUPPORTED_LOCALE` (not in `LanguageRepository`'s active list) · `422` malformed body
- **Rate limit:** standard authenticated-write tier

## 12. Database Requirements
New table `child_preferences`:
| Column | Type | Constraint |
|---|---|---|
| `child_id` | uuid | PK, FK → `child.id` |
| `display_locale` | varchar | NOT NULL |
| `updated_at` | timestamptz | via `TimestampMixin` |

No independent soft-delete lifecycle — cascades with the parent `ChildProfile`'s own deletion/anonymization workflow (FK `ON DELETE CASCADE`).

## 13. Validation
`display_locale` required, non-empty string, must exist in `LanguageRepository`'s active supported-language set at request time.

## 14. Authentication
Bearer token via existing `get_current_child`.

## 15. Authorization
Strict `id == child_ctx.child_id`, identical rule and ordering to B-01.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Path `id` is a sibling's valid child_id | `403 CHILD_MISMATCH`, zero data leakage |
| `display_locale` not in supported-language registry | `422 UNSUPPORTED_LOCALE` |
| Missing/malformed request body | `422` |
| Database failure during upsert | `503`, retryable, client-side "last write wins" retry acceptable given low-stakes nature |

## 17. Analytics
No server-side event required beyond structured request logging; client-side `child_profile_language_changed` is emitted by K-03 on successful local apply.

## 18. Performance
Single indexed upsert on PK `child_id` — no additional query pattern needed given one row per child.

## 19. Security
Same IDOR-class mismatch protection as B-01. `display_locale` is a non-sensitive preference value — no encryption-at-rest consideration beyond the platform baseline.

## 20. Library Requirements
No new dependencies.

## 21. Testing
- Unit: `ChildPreferencesRepository.upsert()` — second call with the same value produces no row-count change, only `updated_at` refresh (or no-op, if implemented as a true conditional upsert).
- Integration: sibling-mismatch rejection on `PATCH` (mirrors B-01's signature test, reused fixture pair).
- Integration: unsupported locale code → `422 UNSUPPORTED_LOCALE`.
- Integration: repeated identical `PATCH` calls → idempotent, `200 { "updated": true }` both times, no duplicate rows (enforced by PK).
- Migration smoke test: table creates cleanly, FK cascade verified against a test child deletion.

## 22. Documentation
OpenAPI description explicitly notes this endpoint affects **display language only**, not content-locale eligibility, to prevent future confusion with the platform's separate age/locale content-filtering system.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `ChildPreferencesOrm` Model & Migration**
Objective: One-row-per-child preferences table. Why: FR-6 requires a persisted display-locale setting. Follow: `infrastructure/db/base.py::Base`/`TimestampMixin` conventions. Files to Create: `preferences_models.py`, migration. Business Rules: PK = FK `child_id`, `ON DELETE CASCADE`. Tests: migration smoke test. Definition of Done: table creates cleanly against the existing `child` table.

**Task 02 — Implement `ChildPreferencesRepository`**
Objective: Upsert-based data access. Follow: `common/base_repository.py::BaseRepository[ModelT]`, extended with a custom `upsert()` method (not part of the generic base, since upsert-by-PK is specific to this one-row-per-child pattern). Files to Create: `preferences_repository.py`. Tests: idempotent upsert test. Definition of Done: `INSERT ... ON CONFLICT DO UPDATE` used, not read-then-write.

**Task 03 — Implement `ChildPreferencesService`**
Objective: Mismatch-check-first orchestration, locale validation via `LanguageRepository`. Follow: `BaseService` pattern, raises typed `DomainError` subclasses only. Files to Create: `preferences_service.py`. Reuse: `modules/localization/repository.py::LanguageRepository` — do not duplicate the supported-language list. Do Not Change: do not modify `LanguageRepository`'s existing methods. Tests: mismatch-check-first unit test; unsupported-locale rejection test. Dependencies: Task 02. Definition of Done: zero database writes occur on a mismatched `id`.

**Task 04 — Add Route & Schemas**
Objective: Wire `PATCH /v1/children/{id}/preferences`. Follow: existing router conventions. Files to Create: `preferences_schemas.py`. Files to Modify: `api.py`, `deps.py`. Dependencies: Task 03. Definition of Done: route registered with `403`/`422` documented responses.

**Task 05 — Add Full Test Suite**
Objective: Coverage per §21, sibling-mismatch test reusing B-01's fixture pattern. Files to Create: `test_child_preferences.py`. Definition of Done: all green in CI, sibling-mismatch test CI-blocking alongside B-01's.

**Task 06 — Update OpenAPI Documentation**
Objective: Clarify display-language-only scope. Definition of Done: `/docs` entry unambiguous about the display-vs-content-locale distinction.

**Task 07 — Final Code Review**
Objective: Confirm mismatch-check ordering, upsert idempotency, cascade-on-delete behavior. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [x] `id`-matches-session check executes before any database write
- [x] Sibling-mismatch rejection verified, zero data leakage
- [x] `display_locale` validated against `LanguageRepository`'s live active list, not a hardcoded duplicate
- [x] Upsert is a true `ON CONFLICT` operation, not read-then-write
- [x] Repeated identical requests are idempotent at the row level
- [x] `child_preferences` FK cascades correctly on child-profile deletion
- [x] No `OutboxWriter` event wired for this low-stakes preference (confirmed intentional, not an oversight)
- [x] No PostgreSQL or Redis credentials modified

## 25. Definition of Done
`PATCH /v1/children/{id}/preferences` is live, strictly per-child-scoped, upsert-idempotent, validated against the existing language registry, and ready for K-03 (Display Language Toggle) to consume.

**Status:** ✅ **Implemented & Verified** (15 unit & API integration tests passing in `tests/modules/identity/test_child_preferences.py`).
