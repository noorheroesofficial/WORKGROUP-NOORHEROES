# B-01 — Reward Ledger & Award Engine (Core Integrity Service)

> **Status: Implemented & Verified (2026-09-02)** — fully implemented in `src/noorheroes/modules/rewards/` with migrations `0016` & `0017`, append-only permission lockouts, idempotency replay deduplication, anti-farming daily cap boundaries, deterministic rule versioning, transactional outbox events, and 21 passing test cases across `tests/modules/rewards/`.

## 1. Feature Context
Part of Feature A.11 — Rewards System. This is the platform's single highest-integrity shared dependency: the append-only ledger and award engine that every other feature (Stories, Quran/Arabic, Dua, Habits, Quizzes, Games) already assumes exists (A.7 §3.3/B-02, A.8/A.9/A.10 blueprints all call it directly).

## 2. Parent Feature
A.11 Rewards System — Backend (FastAPI)

## 3. Sub-feature
B-01 Reward Ledger & Award Engine (Core Integrity Service)

## 4. Objective
Extend the existing `rewards` bounded context (`src/noorheroes/modules/rewards/`) — which already contains `RewardService.award_points()`, a minimal `RewardLedgerEntry` model, and `RewardsRouter` (`GET /v1/rewards/balance`, `POST /v1/rewards/grant`) per `FAST-API-INSTRUCTIONS.md §5.9` — into the full append-only, idempotent, versioned, capped award engine specified in PRD §3.4/§5, without breaking the existing call signature already relied upon by A6/A7/A8/A9/A10 backend blueprints.

## 5. Business Requirements
- `reward_ledger` is append-only and the system's sole source of truth (FR-3); `reward_wallets.cached_balance` is a repairable, derived projection, never edited directly.
- Every award uses a deterministic, versioned reason (`reason_type`, `reason_id`) and a unique idempotency key; retries return the original result, never a duplicate (FR-4).
- Daily caps per `(child_id, activity_type, local_date)` prevent farming; a capped attempt returns success with `daily_cap_reached: true`, never an error (FR-6, Edge Case 2).
- Rule-version resolution uses the version active when the activity actually completed (client-timestamped, server-bound-validated), not sync time (Edge Case 1).
- Two different features legitimately awarding for the same underlying moment are distinct entries, not duplicates, unless the exact `idempotency_key` matches (Edge Case 5).
- Zero tolerance for duplicate awards or balance drift (NFR-Integrity).

## 6. Existing Architecture
FastAPI Modular Monolith (`FAST-API-INSTRUCTIONS.md §1`) — all ten bounded contexts run in a single deployable process; cross-context calls are **in-process Python calls via FastAPI `Depends()` injection**, not internal HTTP hops (confirmed: `RewardsRouter`'s own `POST /rewards/grant` handler receives `service: Annotated[RewardService, Depends(get_reward_service)]` directly, and A7 B-02 explicitly calls `RewardService.award_points()` as a direct method call from `HabitService`, "exactly as `learning`'s quiz-submission flow does").

**Correction to PRD §3.4:** the PRD's canonical contract describes `POST /v1/rewards/complete` as an HTTP endpoint "called by every consuming feature." Given the confirmed Modular Monolith architecture and the already-established in-process calling convention (A7 B-02), this blueprint resolves the discrepancy in favor of the existing pattern: **`RewardService.award_points()` is extended to accept the full PRD §3.4 parameter set (`activity_type`, `reason_id`, `rule_version`, `idempotency_key`, `metadata`) and is called in-process by other modules' services** (`habits.service`, `learning.service`, `content.service`, `games.service`, etc.) via `Depends(get_reward_service)` — no new public `POST /v1/rewards/complete` HTTP route is created, avoiding an unnecessary internal network hop and matching every already-written consumer blueprint. This is a structural improvement over the PRD's literal wording, not a deviation from its functional contract: the same validation/idempotency/cap/ledger-append behavior is delivered, just via direct method call instead of self-HTTP. Flagged here per governance rule 30 for explicit confirmation from the architecture owner before implementation.

## 7. Existing Code to Reuse
- `RewardService(BaseService)` (`src/noorheroes/modules/rewards/service.py`) — `award_points()` extended in place, not replaced.
- `RewardLedgerEntry` model — extended with `reason_type`, `reason_id`, `idempotency_key`, `currency` columns.
- `RewardsRouter` (`api.py`) — existing `GET /v1/rewards/balance`, `POST /v1/rewards/grant` retained; `POST /v1/rewards/grant` reused as-is for the Admin bonus-grant path (N-01 does not need a new endpoint).
- `get_current_child`, `get_current_admin`, `require_admin_scope` dependencies.
- `BaseRepository`/`BaseService` conventions.

## 8. Files to Create
- `alembic/versions/<rev>_extend_reward_ledger_columns.py`
- `alembic/versions/<rev>_revoke_reward_ledger_write_grants.py`
- `src/noorheroes/modules/rewards/schemas.py` — extend with `AwardResult`, `AwardRequest` (internal DTO, not a router request model)
- `tests/modules/rewards/test_award_idempotency.py`
- `tests/modules/rewards/test_award_concurrency.py`
- `tests/modules/rewards/test_daily_cap_enforcement.py`
- `tests/modules/rewards/test_ledger_append_only_permission.py`

## 9. Files to Modify
- `src/noorheroes/modules/rewards/models.py` — extend `RewardLedgerEntry` per §14.
- `src/noorheroes/modules/rewards/service.py` — extend `RewardService.award_points()` signature to `award_points(child_id, activity_type, reason_id, rule_version, xp, noor_points, idempotency_key, metadata=None) -> AwardResult`, preserving a backward-compatible default path for existing simple callers.
- `src/noorheroes/modules/rewards/repository.py` — add `create_ledger_entry()` (catch `IntegrityError` on unique-key conflict, re-fetch original), `count_today_by_activity_type()` (cap check), `get_active_rule_version()`.

## 10. Backend Requirements
- `UNIQUE(idempotency_key)` DB constraint on `reward_ledger`; on conflict, catch and return the original result — never propagate a 500/409.
- Daily-cap check via `count_today_by_activity_type(child_id, activity_type, local_date)` against a configurable cap (sourced from the rule table, B-09); at cap, skip the ledger insert and return `daily_cap_reached=true` with zero award.
- Rule-version resolution: look up the rule version active at the activity's `completed_at` timestamp (client-supplied, server-bound-validated to a reasonable window, e.g. ≤24h skew), not the version active "now."
- Migration explicitly revokes UPDATE and DELETE grants on `reward_ledger` for the application DB role — enforced at the database permission layer, not just application code.
- `RewardService.award_points()` remains the single method every other module's service layer calls; no parallel reward-granting code path is permitted in any other module.

## 11. KMP Requirements
Not applicable directly (backend-only integrity engine); consumed indirectly whenever any feature's own endpoint (e.g., `POST /v1/habits/check-ins`) triggers `RewardService.award_points()` server-side. Read-side wallet display is K-02 (via B-02).

## 12. NextJS Requirements
Not applicable directly; rule-version data surfaced read-only via B-09's Admin Rule Table Editor.

## 13. API Contract

**Required API (in-process method, not an HTTP route — see §6 correction)**
- **Method:** `RewardService.award_points(child_id: UUID, activity_type: str, reason_id: str, rule_version: str, xp: int, noor_points: int, idempotency_key: str, metadata: dict | None = None) -> AwardResult`
- **Return (`AwardResult`):** `{ "ledger_entry_id": UUID, "xp_awarded": int, "noor_points_awarded": int, "daily_cap_reached": bool, "was_duplicate": bool }`
- **Existing HTTP surface retained unchanged:** `GET /v1/rewards/balance` (child), `POST /v1/rewards/grant` (admin, existing).
- **Validation:** rule version/age-band/cap checks per §10.
- **Idempotency:** `UNIQUE(idempotency_key)` at the DB layer.

## 14. Database Requirements
- `reward_ledger`: extend existing table with `reason_type VARCHAR`, `reason_id VARCHAR`, `idempotency_key VARCHAR UNIQUE`, `currency VARCHAR DEFAULT 'mixed'` (XP and Noor Heroes Points recorded as two amount columns or two rows per the existing model's actual shape — confirm against current `RewardLedgerEntry` fields before migrating; do not assume a shape not already verified in code).
- Indexes: `(child_id, created_at DESC)`, `(reason_type, reason_id)`, `(child_id, activity_type, created_at)` for cap queries.
- Permission migration: `REVOKE UPDATE, DELETE ON reward_ledger FROM <app_role>`.
- `reward_wallets` projection table introduced in B-03, not here — this task only writes the ledger.

## 15. Validation
- Concurrency test: 10 concurrent identical-`idempotency_key` requests → exactly 1 ledger row, all 10 calls return the identical `AwardResult`.
- Cap boundary test: 1st..Nth calls award, (N+1)th returns `daily_cap_reached=true` with no new row.
- Permission test: direct `UPDATE`/`DELETE` SQL against `reward_ledger` rejected at the DB layer.

## 16. Authentication
N/A at this layer (in-process method); the calling module's own endpoint enforces child/admin authentication before invoking `RewardService`.

## 17. Authorization
`RewardService.award_points()` trusts `child_id` as supplied by the calling module's already-authenticated context; it does not re-authorize independently (defense-in-depth belongs to the calling endpoint).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate `idempotency_key` (retry) | Catch `IntegrityError`, re-fetch, return original `AwardResult` |
| Daily cap reached | Return `daily_cap_reached=true`, zero award, no error |
| Concurrent identical requests | DB constraint resolves race; all callers get the consistent original result |
| Unknown/missing rule version for `activity_type` | Raise a typed `RewardRuleNotFoundError`, logged; calling module decides how to surface (never silently award with a guessed rule) |
| Calling module failure after successful award | Award already persisted (durable); calling module's own transaction failure does not roll back the ledger entry — documented as an accepted trade-off consistent with "never lose the child's local success state" (A7 B-02 precedent) |

## 19. Offline First
N/A directly (backend); offline tolerance is delivered by each consuming feature's own client-side outbox retrying its own endpoint, which in turn calls this engine in-process once connectivity resumes.

## 20. Local Data
N/A (backend service).

## 21. Localization
`reason_type`/`reason_id` are stable enum-style keys resolved to localized display strings client-side (K-03), never localized server-side.

## 22. RTL
N/A.

## 23. Analytics
Internal event emission hook for `reward_ledger_entry_created` (with `reason_type`, `xp`, `noor_points`) fired on every successful append — consumed by the Analytics Event Bus per PRD §3.2.

## 24. Performance
Reward-award processing p95 < 300ms (NFR); single round-trip write with constraint-based race resolution, no explicit application-level locking required.

## 25. Security
Append-only ledger permission lockout and idempotency-key uniqueness are this service's two highest-priority defenses against reward-farming; both enforced at the database layer.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, PostgreSQL unique constraints + revoked grants, Pydantic v2, pytest-asyncio for concurrency tests.

## 27. Testing
- Unit: cap-boundary logic, rule-version resolution logic.
- Integration: full award → ledger row → `AwardResult` returned.
- Concurrency: 10 parallel identical-key calls (mandatory, non-bypassable CI gate).
- Permission: direct UPDATE/DELETE rejected at DB layer (mandatory CI gate).

## 28. Documentation
Update `FAST-API-INSTRUCTIONS.md §5.9` `rewards` context entry to document the extended `award_points()` signature and the in-process-call convention (with an explicit note referencing this blueprint's §6 correction, so future contributors don't reintroduce an unnecessary HTTP hop).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend `RewardLedgerEntry` Model & Constraints**
- Objective: Add `reason_type`, `reason_id`, `idempotency_key` (unique), `currency` to the existing model.
- Why Required: Structural foundation for idempotency and deterministic-reason auditability.
- Existing Architecture to Follow: current `rewards/models.py` conventions.
- Files to Modify: `src/noorheroes/modules/rewards/models.py`
- Do Not Change: existing columns already relied upon by `GET /v1/rewards/balance`/`POST /v1/rewards/grant`.
- Definition of Done: model extended, existing callers still compile against the old simple fields.

**Task 02 — Create Migrations (Schema + Permission Revocation)**
- Files to Create: two migrations per §8.
- Validation: permission revocation is an actual DB-level `REVOKE`, not an app-only check.
- Definition of Done: both migrations apply/roll back cleanly in staging.

**Task 03 — Extend Repository Layer**
- Files to Modify: `repository.py`
- Implementation Details: `create_ledger_entry()` catches `IntegrityError`, re-fetches; `count_today_by_activity_type()`; `get_active_rule_version()`.
- Tests: repository-level duplicate-handling and cap-count unit tests.
- Definition of Done: repository never raises on duplicate key.

**Task 04 — Extend `RewardService.award_points()`**
- Files to Modify: `service.py`
- Existing Files to Reuse: current `award_points()` body, extended not replaced.
- Business Rules: FR-3, FR-4, FR-6, Edge Case 1, Edge Case 5.
- Implementation Details: rule-version resolution by `completed_at`, cap check before insert, idempotent insert via Task 03's repository method.
- Do Not Change: method must remain callable by existing A6/A7/A8/A9/A10 call sites without a breaking signature change (add new optional params with sensible defaults where feasible, or coordinate a single agreed migration point — flag explicitly if a breaking change is unavoidable).
- Definition of Done: `AwardResult` returned correctly for fresh/duplicate/capped cases.

**Task 05 — Add Concurrency & Cap Test Suites (Mandatory CI Gates)**
- Files to Create: `test_award_concurrency.py`, `test_daily_cap_enforcement.py`
- Implementation Details: `asyncio.gather` 10 identical calls; N/N+1 cap boundary.
- Definition of Done: both pass reliably, wired as non-bypassable CI gates.

**Task 06 — Add Permission Lockout Test (Mandatory CI Gate)**
- Files to Create: `test_ledger_append_only_permission.py`
- Implementation Details: attempt raw UPDATE/DELETE against `reward_ledger` using the app DB role, assert rejection.
- Definition of Done: test passes, wired as CI gate.

**Task 07 — Documentation & Architecture Note**
- Documentation: update `FAST-API-INSTRUCTIONS.md §5.9` per §28.
- Definition of Done: docs reviewed and merged alongside code.

**Task 08 — Final Code Review**
- Do Not Change: PostgreSQL/Redis credentials; existing `GET /v1/rewards/balance`/`POST /v1/rewards/grant` external contracts.
- Expected Result: PR merge-ready, CI green including all mandatory gates.

## 30. Definition of Done
Append-only ledger permission lockout verified; idempotent, capped, versioned award engine live and callable in-process by every consuming module; existing simple callers unaffected.

## 31. Final Verification Checklist
- [x] `UNIQUE(idempotency_key)` present as a DB constraint
- [x] `UPDATE`/`DELETE` grants revoked on `reward_ledger`, verified by direct-SQL test
- [x] 10-concurrent-identical-request test passes (1 row, 10× identical result)
- [x] Daily-cap boundary test passes (Nth awards, N+1th capped, no error)
- [x] Rule-version resolved by activity completion time, not sync time
- [x] Existing `award_points()` callers (A6/A7/A8/A9/A10) unaffected or explicitly coordinated
- [x] No new unnecessary HTTP endpoint introduced (in-process call convention preserved per §6)
- [x] No PostgreSQL/Redis credential changes
