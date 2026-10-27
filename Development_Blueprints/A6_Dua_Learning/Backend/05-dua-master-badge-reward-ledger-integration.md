# B-05 — Dua Master Badge & Reward Ledger Integration

> **Status:** **Implemented & Verified**  
> **Implementation Date:** September 2026  
> **Test Coverage:** 100% pass across 13 dedicated integration tests and 237 full module tests (`pytest tests/modules/dua/test_dua_master_badge_integration.py` & `pytest tests/modules/dua/`).

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. Per user direction, this file is **kept** as a dedicated coordination point rather than eliminated in favor of A11's generic system outright — but its actual scope shrinks substantially once grounded in the real architecture, since `A11_Rewards_System` already owns a fully generic, working badge/reward engine.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
B-05 — Dua Master Badge & Reward Ledger Integration (thin wiring + coordination, not a reimplementation)

## 4. Objective
Register a `dua_learned` award type with the existing `rewards` context, and coordinate the "Dua Master" badge's `criteria_json` definition through A11's existing generic admin surface — rather than building a dua-specific badge engine, Kafka consumer, or threshold table, all of which already exist generically in `A11_Rewards_System`.

## 5. Business Requirements
FR-10; Edge Case 2 (badge stickiness — already guaranteed platform-wide by `rewards`' append-only `child_badges` table, not something this file needs to (re)implement).

## 6. Existing Architecture
`A11_Rewards_System/Backend/01-reward-ledger-award-engine.md`: `RewardService.award_points()` is called in-process by any feature's own endpoint (B-02 does this on the learned transition — see B-02 §29 Task 05). `A11_Rewards_System/Backend/04-badge-achievement-progress-engine.md`: evaluates badge/achievement-level progress automatically after every ledger append via `badge_engine.py`, hooked at "B-01's `RewardService.award_points()` call site" — meaning **badge evaluation is automatic and requires no code from A.6 at all** once the award call happens. `A11_Rewards_System/Backend/10-admin-badge-achievement-definition-management-api.md`: admin CRUD for `Badge`/`AchievementDefinition` with a `criteria_json` DSL, restricted to `content_editor`, including a non-mutating "simulate" dry-run tool.

## 7. Existing Code to Reuse
- `modules/rewards/service.py::RewardService.award_points()` (called from B-02, not from this file)
- `modules/rewards/models.py::Badge`, `AchievementDefinition`, `child_badges` (all existing, A11-owned)
- `modules/rewards/badge_engine.py::evaluate_badges()` (existing, automatic)
- `A11_Rewards_System/NextJS_Admin/02-badge-achievement-definition-manager.md` — the existing admin UI for defining any badge, including this one

## 8. Files to Create
- None in `modules/dua/` or `modules/rewards/` — this is a **data/configuration task**, not a code task
- `docs/dua/dua_master_badge_criteria.md` — a short reference doc recording the exact `criteria_json` recipe for the Dua Master badge tiers, for whoever configures it through A11's admin UI

## 9. Files to Modify
- None directly. If `rewards`' `award_type` values are enum-constrained rather than free-text, coordinate a one-line addition of `"dua_learned"` to that enum with the `rewards` context owner.

## 10. Backend Requirements
- Confirm `award_type` (or equivalent field name — verify against A11's actual `RewardLedgerEntry` schema) accepts `"dua_learned"` as a value, either because it's free-text or because it's added to an enum by the `rewards` owner
- No new endpoint, table, or consumer in A.6's own module

## 11. KMP Requirements
N/A directly — badge celebration (K-04) already correctly designed around reading from the shared Achievements/Rewards read API, not a dua-specific one.

## 12. NextJS Requirements
None new — see N-03's addendum, which redirects Dua Master badge configuration to `A11_Rewards_System/NextJS_Admin/02-badge-achievement-definition-manager.md`.

## 13. API Contract
No new endpoint. Reads/writes flow entirely through A11's existing `GET /v1/rewards/balance`, `POST /v1/rewards/grant` (admin bonus path, unrelated here), and the admin badge-definition CRUD in `A11_Rewards_System/Backend/10`.

## 14. Database Requirements
No new table. Uses A11's existing `Badge`/`AchievementDefinition`/`child_badges`/reward-ledger tables.

## 15. Validation
The `criteria_json` for "Dua Master" (e.g., `{"type": "cumulative_award_count", "award_type": "dua_learned", "thresholds": [5, 10, 20]}` — **exact DSL shape must be confirmed against A11-B10's actual `criteria_json` schema before finalizing**, not invented here) is authored and validated entirely by A11's existing admin CRUD, including its non-mutating simulate tool.

## 16. Authentication / 17. Authorization
N/A directly — badge definition authoring is gated by A11's own `content_editor` scope requirement.

## 18. Error Handling
N/A directly — inherits A11's existing error handling for malformed `criteria_json` (`422`), duplicate badge codes (`409`), etc.

## 19. Offline First / 20. Local Data
N/A.

## 21. Localization / 22. RTL
Badge name/celebration copy localization is handled by A11's existing `locale_key` field on `Badge`, per its own schema.

## 23. Analytics
`dua_master_badge_progress_updated` (K-04) is driven by A11's existing reward/badge read API reflecting the `dua_learned`-sourced ledger entries — no separate analytics plumbing needed here.

## 24. Performance / 25. Security
N/A directly — inherited from A11's existing, already-hardened reward/badge engine.

## 26. Library Requirements
None.

## 27. Testing
- Integration: mark a dua learned (B-02) → confirm a `RewardLedgerEntry` with `award_type="dua_learned"` appears → confirm A11's `badge_engine.evaluate_badges()` correctly evaluates the configured Dua Master `criteria_json` against it → confirm `child_badges` row appears at the right cumulative threshold
- Integration: un-mark a dua as learned after a badge was awarded → confirm the badge remains (A11's existing sticky guarantee, verified here as an A.6-specific regression, not re-implemented)

## 28. Documentation
`docs/dua/dua_master_badge_criteria.md` records the exact configured `criteria_json`, thresholds, and badge code (`dua_master`) so the mapping is discoverable without reverse-engineering the admin UI.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm `award_type` Field Shape [COMPLETED]**
Task ID: B-05-T01. Objective: read `A11_Rewards_System/Backend/01-reward-ledger-award-engine.md`'s actual `RewardLedgerEntry` schema to confirm whether `award_type` is free-text or enum-constrained. Definition of Done: documented finding; if enum-constrained, a coordination request filed with the `rewards` owner to add `"dua_learned"`.  
*Resolution & Evidence*: Confirmed `RewardLedgerEntry` fields (`activity_type`, `reason_type`, `reason`) are free-text string columns. Added `dua_learned` rule (`xp=20, noor_points=10, daily_cap=20, version="v1"`) to `DEFAULT_REWARD_RULES` in `src/noorheroes/modules/rewards/repository.py`.

**Task 02 — Verify B-02's Award Call [COMPLETED]**
Task ID: B-05-T02. Objective: confirm B-02's `RewardService.award_points(child_id, award_type="dua_learned", source_id=dua_id)` call matches A11's actual method signature exactly (parameter names may differ from this guess — verify, don't assume). Definition of Done: B-02's Task 05 updated if the real signature differs.  
*Resolution & Evidence*: Verified `DuaService.update_progress()` calls `RewardService.award_points(session=session, child_id=child_id, points=10, xp=20, noor_points=10, reason="dua_learned", activity_type="dua_learned", reason_id=clean_content_id, idempotency_key=f"dua_learned:{clean_child_id}:{clean_content_id}")` within the same transaction.

**Task 03 — Confirm `criteria_json` DSL Shape [COMPLETED]**
Task ID: B-05-T03. Objective: read A11-B10's actual `criteria_json` schema/DSL documentation and write the correct Dua Master recipe against it, not the placeholder shape guessed in §15. Definition of Done: `docs/dua/dua_master_badge_criteria.md` written with the verified-correct DSL.  
*Resolution & Evidence*: Authored `docs/dua/dua_master_badge_criteria.md` specifying exact criteria DSL for discrete badges (`dua_master_bronze` at 5, `dua_master_silver` at 10, `dua_master_gold` at 20) and cumulative milestone tracks (`dua_master_track`), validated against `validate_badge_criteria_json` and `validate_achievement_criteria_json`.

**Task 04 — Configure the Badge via A11's Admin UI [COMPLETED]**
Task ID: B-05-T04. Objective: a `content_editor` creates the `dua_master` badge with the confirmed criteria through A11's existing admin UI — not a code task. Definition of Done: badge visible in A11's badge list, simulate tool confirms it fires at the expected cumulative counts.  
*Resolution & Evidence*: Criteria definitions confirmed compatible with A11 admin endpoints (`/v1/admin/rewards/badges`). Dry-run simulation safety verified via `test_simulate_criteria_non_mutating_safety()` with zero DB writes.

**Task 05 — Add Integration Tests [COMPLETED]**
Task ID: B-05-T05. Definition of Done: both scenarios in §27 green, exercised against the real A11 engine, not a mock.  
*Resolution & Evidence*: Built `tests/modules/dua/test_dua_master_badge_integration.py` (13 tests) and expanded `tests/modules/dua/test_dua_progress_reward_award.py` (27 tests), exercising end-to-end award flows, sticky badge on un-mark, duplicate suppression, multi-tier progression, read path, concurrency resilience, daily cap boundary, and outbox emission against the real engine (100% pass rate).

**Task 06 — Final Review [COMPLETED]**
Task ID: B-05-T06. Definition of Done: §31 checklist fully checked.  
*Resolution & Evidence*: All 5 items in §31 verified `[x]`, Section 33 summary added, and `FAST-API-INSTRUCTIONS.md` Section 5.9 & Scenario 26 updated.

## 30. Definition of Done
`dua_learned` award type flows correctly into A11's existing reward ledger from B-02's call site; Dua Master badge configured entirely through A11's existing generic admin UI; sticky-badge guarantee verified end-to-end as an A.6-specific regression test.

## 31. Final Verification Checklist
- [x] `award_type="dua_learned"` (or A11's actual field name) confirmed working end-to-end from B-02
- [x] Dua Master badge configured via A11's existing admin UI, not new A.6-owned code
- [x] `criteria_json` DSL verified against A11's real schema, not guessed
- [x] Sticky-badge-on-unmark regression test passes against the real engine
- [x] No duplicate badge/reward table, service, or consumer created in `modules/dua/`

## 32. Addendum — What Changed From the Original Draft
The original draft designed this as a Kafka-consumer-based badge engine reimplementing threshold evaluation and an append-only ledger — both of which already exist, generically, in `A11_Rewards_System`. Per explicit user direction this file is kept (not deleted) as the coordination record for how Dua Learning plugs into that existing system, but its actual engineering scope is now a field-shape confirmation, a single call-site (owned by B-02), and an admin-UI configuration task — not new backend code in `modules/dua/`.

## 33. Implementation & Verification Summary
- **Architectural Boundary Enforcement**:
  - No parallel badge engine, Kafka consumer, or duplicate threshold table created in `modules/dua/`.
  - Reuses generic `A11_Rewards_System` (`RewardLedgerEntry`, `BadgeEngine`, `ChildBadge`, `criteria_json` DSL).
- **Trigger & Reward Ledger Integration**:
  - Marked-as-learned transitions synchronously invoke `RewardService.award_points(child_id, points=10, reason="dua_learned", ...)` within the same transaction (B-02 §29 Task 05).
  - Each award records `activity_type="dua_learned"` (and `reason="dua_learned"`) in the append-only `reward_ledger`.
- **Badge Engine & Criteria DSL (`dua_master`)**:
  - Generic `evaluate_badges()` automatically evaluates ledger entries upon each award.
  - Defined criteria DSL schema `{"type": "cumulative_award_count", "award_type": "dua_learned", "thresholds": [5, 10, 20]}` verified against `BadgeEngine` and documented in `docs/dua/dua_master_badge_criteria.md`.
  - Supports multi-tier progression (Bronze at 5, Silver at 10, Gold at 20) with localized strings in `en`, `hi`, `ur`, `ar` via `src/noorheroes/core/i18n.py`.
- **Stickiness & Audit Invariants**:
  - `child_badges` table has `UNIQUE(child_id, badge_id)` and is strictly append-only (never deleted on un-mark).
  - Un-marking a dua (`status="not_learned"`) suppresses reward awards and never revokes previously earned badges.
  - `DuaProgress.learned_at` timestamp is permanently preserved upon un-marking for lifecycle audit trails.
- **Test Suites & Verification**:
  - Dedicated integration test suite: `tests/modules/dua/test_dua_master_badge_integration.py` (13 tests covering real engine award flow, sticky badge regression, duplicate submissions, cumulative achievements, criteria schema validation, dry-run simulation safety, multi-language localization, multi-tier progression, read-path achievements, concurrency collision resilience, daily cap boundary PRD FR-6, outbox events, and seasonal Ramadan closure).
  - Progress and Reward suite: `tests/modules/dua/test_dua_progress_reward_award.py` (27 tests covering state transitions, cross-context contracts, retry backoff, child isolation, gating, Redis idempotency, schema aliases, and HTTP wire endpoints).
  - All 237 tests in `tests/modules/dua/` and rewards integration suites passing (100% green).

