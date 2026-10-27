# B-06 — Weekly Challenge & Milestone Achievement API

## 1. Feature Context
NoorHeroes Child App, Feature A.2. Powers the "Weekly Challenge & Progress Map" and "Milestones & Reward Summary" Home sections.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
1.6 Weekly Challenge & Milestone Achievement API (ID: B-06)

## 4. Objective
Implement `GET /v1/challenges/weekly`, `GET /v1/children/{id}/achievements`, and challenge-join mutation, with graceful `null`/teaser fallbacks when no active challenge or achievements exist.

## 5. Business Requirements
Per PRD §2.2, §3.4, §4.2:
- Weekly challenge: `null` challenge object if none active for the locale/age band, never an empty/broken widget.
- Zero weekly-challenge participation → "Join Challenge" CTA state, not a progress bar.
- Zero achievements → milestone summary shows the next achievable milestone as a preview/teaser, not a blank module.
- No duplicate achievement unlocks.

## 6. Existing Architecture
FastAPI service-layer pattern; fan-out dependency of B-01, conforming to the `ChallengeClient`/`AchievementClient` contracts from B-01 Task 02.

## 7. Existing Code to Reuse
B-01's cache-invalidation helper (challenge-join should invalidate the `weekly_challenge` fragment); A.1 auth dependency.

## 8. Files to Create
- `app/routers/challenges.py`
- `app/services/challenge_service.py`, `app/services/achievement_service.py`
- `app/repositories/challenge_repository.py`, `app/repositories/achievement_repository.py`
- `app/models/challenge_definition.py`, `app/models/challenge_participation.py`, `app/models/achievement_definition.py`, `app/models/achievement_unlock.py`
- `alembic/versions/xxxx_create_challenge_achievement_tables.py`
- `tests/integration/test_challenge_join_flow.py`

## 9. Files to Modify
- `app/main.py`

## 10. Backend Requirements
- `GET /v1/challenges/weekly` resolves the currently-active challenge (by date range + age band/locale eligibility) and the child's `challenge_participation` percent, or `null` if none active.
- `POST /v1/challenges/{challenge_id}/join` (join action referenced in PRD §2.3's Click Target table) creates a `challenge_participation` row, `UNIQUE(challenge_id, child_id)` preventing duplicate joins.
- `GET /v1/children/{id}/achievements` returns unlocks from the last 7 days plus a computed "next achievable" teaser (nearest unmet `unlock_criteria`).

## 11. KMP Requirements
Not implemented here. Consumed by K-05 (Weekly Challenge & Milestones widgets).

## 12. NextJS Requirements
Not applicable directly in this sub-feature (challenge/achievement *definitions* are assumed managed by an existing admin surface elsewhere in the platform, e.g., Content CMS/Rewards admin from other features — confirm before assuming N-02-style curation is needed here; this PRD's Admin Requirements (§8) do not list a dedicated Challenge/Achievement admin tool for A.2, so none is created in this breakdown).

## 13. API Contract

**`GET /v1/challenges/weekly`** — Auth: Bearer (child-mode) — Response: current challenge definition + child's progress; `null` challenge object if none active.

**`POST /v1/challenges/{challenge_id}/join`** — Auth: Bearer (child-mode) — Response: `{ joined: true, percent_complete: 0 }` — Idempotent on `UNIQUE(challenge_id, child_id)`.

**`GET /v1/children/{id}/achievements`** — Auth: Bearer (child-mode, `id` must equal token's `child_id`) — Response: recent unlocks (7 days) + `next_teaser`.

## 14. Database Requirements
Per PRD §4.2:
- `challenge_definition(challenge_id PK, title, start_date, end_date, target_criteria jsonb)`.
- `challenge_participation(participation_id PK, challenge_id FK, child_id FK, percent_complete, joined_at)`; `UNIQUE(challenge_id, child_id)`; index on `(child_id)`.
- `achievement_definition(achievement_id PK, title, unlock_criteria jsonb)`.
- `achievement_unlock(unlock_id PK, achievement_id FK, child_id FK, unlocked_at)`; `UNIQUE(achievement_id, child_id)`; index on `(child_id, unlocked_at DESC)`. Append-only/immutable.

## 15. Validation
`{id}` path param on the achievements endpoint must equal the authenticated token's `child_id` (reject mismatch with `403`, not silently substitute).

## 16. Authentication
Bearer JWT (child-mode session).

## 17. Authorization
Strict `child_id` scoping on all three endpoints; achievements endpoint additionally validates path `{id}` against token claim.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Challenge Service failure | B-01 shows static fallback challenge description, hides progress map |
| Achievement Service failure | B-01 hides milestones section |
| No active challenge | `null` challenge object (not an error) |
| Duplicate join attempt | Idempotent success (existing participation returned) |

## 19. Offline First
Not applicable server-side.

## 20. Local Data
Not applicable (backend).

## 21. Localization
Challenge/achievement `title` resolved via existing content-localization pattern.

## 22. RTL
N/A (backend).

## 23. Analytics
Backend does not fire `weekly_challenge_widget_viewed`/`_joined`/`milestones_widget_viewed` (client-fired).

## 24. Performance
Achievement "next teaser" computation should avoid scanning all achievement definitions per request if the catalog grows large — consider a precomputed/cached eligibility check if the definition set is large; for initial launch scale, a straightforward filtered query is acceptable.

## 25. Security
`UNIQUE(challenge_id, child_id)` and `UNIQUE(achievement_id, child_id)` prevent duplicate-join/duplicate-unlock abuse at the DB layer.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0, Alembic, pytest-asyncio.

## 27. Testing
- Integration: no active challenge → `null` object returned, not an error.
- Integration: duplicate join → idempotent, no duplicate row.
- Integration: achievements endpoint rejects path `{id}` mismatched against token `child_id`.
- Unit: "next achievable" teaser computation.

## 28. Documentation
OpenAPI docs for all three endpoints.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create Challenge & Achievement Tables + Migration**
- Objective: Four tables per PRD ER diagram.
- Why Required: Foundational data layer.
- Existing Architecture to Follow: Alembic/SQLAlchemy conventions.
- Existing Files to Reuse: Base model class.
- Files to Create: Model files + migration listed in §8.
- Files to Modify: none
- Implementation Details: Exact fields/constraints per PRD §4.2.
- Business Rules: `achievement_unlock` append-only.
- Validation: N/A at model level.
- Error Handling: N/A.
- Security: Unique constraints are the anti-duplicate control.
- Performance: Indexes per spec.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Migration test.
- Documentation: Docstrings.
- Dependencies: None.
- Do Not Change: Do not modify PostgreSQL credentials.
- Expected Result: Tables created.
- Definition of Done: Migration passes.

**Task 02 — Implement Challenge Service (Resolve Active + Join)**
- Objective: `GET /v1/challenges/weekly` and join mutation.
- Why Required: Core feature logic.
- Existing Architecture to Follow: Service/repository pattern.
- Existing Files to Reuse: Task 01 models.
- Files to Create: `app/repositories/challenge_repository.py`, `app/services/challenge_service.py`, `app/routers/challenges.py`
- Files to Modify: `app/main.py`
- Implementation Details: `get_active_challenge(child_id, age_band, locale)` resolves by date-range + eligibility, returns `None` if none; `join_challenge(child_id, challenge_id)` upserts participation idempotently.
- Business Rules: `null` on no active challenge, never an error.
- Validation: Eligibility filter (age band/locale) before returning.
- Error Handling: Idempotent join.
- Security: Child-scoped.
- Performance: Indexed query on `(child_id)`.
- Localization: Pass-through.
- RTL: N/A.
- Analytics: N/A.
- Tests: Integration tests per §27.
- Documentation: OpenAPI docs.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working challenge endpoints.
- Definition of Done: Tests pass.

**Task 03 — Implement Achievement Service (Recent Unlocks + Next Teaser)**
- Objective: `GET /v1/children/{id}/achievements`.
- Why Required: Core feature logic.
- Existing Architecture to Follow: Service/repository pattern.
- Existing Files to Reuse: Task 01 models.
- Files to Create: `app/repositories/achievement_repository.py`, `app/services/achievement_service.py`
- Files to Modify: `app/routers/challenges.py` (or a dedicated `achievements.py` router — group logically per existing router-file conventions)
- Implementation Details: Query unlocks `WHERE unlocked_at > now() - 7 days`; compute nearest unmet `unlock_criteria` as `next_teaser` (simple threshold-distance comparison for launch scope).
- Business Rules: Path `{id}` must equal token `child_id`.
- Validation: Path/token match check.
- Error Handling: Achievement Service internal errors bubble as 5xx only for true failures; B-01 handles the graceful hide at its layer.
- Security: Path/token match enforcement (§15).
- Performance: Indexed query on `(child_id, unlocked_at DESC)`.
- Localization: Pass-through titles.
- RTL: N/A.
- Analytics: N/A.
- Tests: Integration test for path/token mismatch rejection; unit test for teaser computation.
- Documentation: OpenAPI docs.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working achievements endpoint.
- Definition of Done: Tests pass.

## 30. Definition of Done
All three endpoints implemented with correct null/teaser fallbacks, idempotent join, and strict child-scoped authorization; all tests green.

## 31. Final Verification Checklist
- [x] No active challenge returns `null` object, not an error
- [x] Duplicate join is idempotent (`UNIQUE(challenge_id, child_id)` enforced)
- [x] Achievement `{id}` path validated against token `child_id`
- [x] `UNIQUE(achievement_id, child_id)` prevents duplicate unlocks
- [x] Next-achievable teaser computed correctly when zero unlocks exist
- [x] All tests pass

## 32. Implementation & Verification Summary

- **Completed Components**:
  1. **Database Migration (`alembic/versions/0084_create_challenge_achievement_tables.py`)**:
     - Created four tables per PRD §4.2:
       - `challenge_definition`: `challenge_id` (PK, VARCHAR(36)), `title`, `description`, `start_date`, `end_date`, `target_criteria` (JSONB/JSON), `icon_url`, `banner_url`, `created_at`, `updated_at`.
       - `challenge_participation`: `participation_id` (PK, VARCHAR(36)), `challenge_id` (FK), `child_id` (FK), `percent_complete` (FLOAT, default 0.0), `joined_at`, timestamps. Check constraint `ck_challenge_participation_percent` (`0.0 <= percent_complete <= 100.0`), unique constraint `uq_challenge_participation_child` on `(challenge_id, child_id)`, and index on `child_id`.
       - `achievement_definition`: `achievement_id` (PK, VARCHAR(36)), `title`, `description`, `badge_icon_url`, `category`, `unlock_criteria` (JSONB/JSON), `sequence_order` (INT, default 0), timestamps.
       - `achievement_unlock`: `unlock_id` (PK, VARCHAR(36)), `achievement_id` (FK), `child_id` (FK), `unlocked_at` (TIMESTAMP). Unique constraint `uq_achievement_unlock_child` on `(achievement_id, child_id)` and compound index `ix_achievement_unlock_child_date` on `(child_id, unlocked_at DESC)`.
     - Down revision chained to `0083_create_progress_record_table`.
  2. **Core Domain Models (`src/noorheroes/modules/challenges/models.py`)**:
     - `ChallengeDefinition`, `ChallengeParticipation`, `MilestoneAchievementDefinition` (aliased as `AchievementDefinition`), and `AchievementUnlock`.
  3. **Data Transfer Objects (`src/noorheroes/modules/challenges/schemas.py`)**:
     - `WeeklyChallengeResponse` (challenge details, `joined`, `percent_complete`, `days_remaining`).
     - `ChallengeJoinResponse` (`joined`, `percent_complete`, `challenge_id`, `child_id`).
     - `AchievementRecentItem`, `NextTeaserItem`, and `AchievementResponse`.
  4. **Data Access Layer (`src/noorheroes/modules/challenges/repository.py`)**:
     - `ChallengeRepository`: `get_active_challenge` (active date range `start_date <= today <= end_date` and `target_criteria` age band/locale filtering), `get_challenge_by_id`, `get_participation`, and `join_challenge_idempotent` (database unique constraint handling).
     - `AchievementRepository`: `get_recent_unlocks` (`unlocked_at >= now() - 7 days` with eager loading), `get_unlocked_achievement_ids`, `get_next_achievable` (computes lowest sequence_order unmet definition), and `record_unlock_idempotent`.
  5. **Domain Services (`src/noorheroes/modules/challenges/service.py`)**:
     - `ChallengeService`: Active weekly challenge resolution with child participation enrichment, returning `None` (HTTP 200 `null`) when none active. Idempotent join mutation with immediate `HomeCache().invalidate_section(child_id, 'weekly_challenge')` invalidation.
     - `AchievementService`: Child-scoped 7-day recency window unlock aggregation, next-achievable teaser calculation, and zero-unlock preview fallback.
  6. **Unified Router & Endpoints (`src/noorheroes/modules/challenges/api.py` & `src/noorheroes/modules/rewards/api.py`)**:
     - `GET /v1/challenges/weekly`: Child-scoped, returns active weekly challenge with participation progress or `null`.
     - `POST /v1/challenges/{challenge_id}/join`: Child-scoped, idempotent join with cache invalidation.
     - `GET /v1/children/{id}/achievements`: Unified milestone achievements endpoint in `rewards/api.py` enriching discrete badges and cumulative achievement levels with recent unlocks (7 days) and next milestone teaser without route collisions or breaking existing contract assertions. Enforces strict tenancy: path `{id}` must match token `child_id` (403 on mismatch).
  7. **Backwards-Compatibility Facade (`app/`)**:
     - 100% re-exported facades under `app/models/challenge_definition.py`, `app/models/challenge_participation.py`, `app/models/achievement_definition.py`, `app/models/achievement_unlock.py`, `app/repositories/challenge_repository.py`, `app/repositories/achievement_repository.py`, `app/services/challenge_service.py`, `app/services/achievement_service.py`, `app/schemas/challenges.py`, and `app/routers/challenges.py`.
- **Verification Results**:
  - `tests/integration/test_challenge_join_flow.py`: 5/5 passed (100% green) covering active date range resolution, age band/locale filtering, graceful null fallback, join mutation idempotency, edge-cache invalidation, 7-day recency filtering, lowest sequence_order unmet teaser computation, sibling tenancy 403 enforcement, and full HTTP cycle.
  - `tests/modules/rewards/test_achievements_api.py`: 6/6 passed (100% green) verifying unified route compatibility, i18n headers, and complete status code coverage (200, 400, 401, 403, 404, 422, 429, 500).
  - `tests/modules/rewards/test_rewards_openapi.py`: 1/1 passed (100% green) verifying OpenAPI schema tags and operation IDs.
  - Combined Integration Regression Suite: 72/72 tests passed (100% green).
