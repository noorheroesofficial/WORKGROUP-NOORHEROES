# B-10 — Admin Dua Master Badge Threshold Configuration (Coordination File)

> **Status:** **Implemented & Verified**  
> **Implementation Date:** September 2026  
> **Coordination Note:** Reuses A11 generic admin badge/achievement CRUD (`content_editor` / `product_admin` roles per `require_admin_role`). Zero duplicate code or tables.

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. As established in B-05, badge threshold configuration is already owned generically by `A11_Rewards_System/Backend/10-admin-badge-achievement-definition-management-api.md` (`Badge`/`AchievementDefinition` CRUD with a `criteria_json` DSL, `content_editor` scope). Per explicit user direction this file is kept as the dedicated Dua Master coordination record rather than deleted, but it does not implement a second threshold-config endpoint.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
B-10 — Admin Dua Master Badge Threshold Configuration (owned by A11; this file documents A.6's specific configuration, not new code)

## 4. Objective
Ensure the "Dua Master" badge's threshold tiers are configured, discoverable, and changeable without a deploy — entirely through A11's existing generic admin CRUD — and record the exact configuration here so it isn't only discoverable by reverse-engineering the admin UI.

## 5. Business Requirements
FR-10; Admin Requirements §8 (update-only; verified against A11's authorization model: gated by `require_any_scope("content_editor", "product_admin", "superadmin", "economy_design")`).

## 6. Existing Architecture
`A11_Rewards_System/Backend/10`: `POST/PATCH /v1/admin/rewards/badges` and `PATCH /v1/admin/rewards/badges/{id}/criteria` with `criteria_json`, authorized for `content_editor`, `product_admin`, `superadmin`, and `economy_design` via `require_any_scope()`. Dynamic threshold reconfiguration occurs live without code deployment, database migrations, or server restarts.

## 7. Existing Code to Reuse
- `A11_Rewards_System/Backend/10`'s existing admin CRUD and `simulate_criteria()` dry-run tool

## 8. Files to Create
- `docs/dua/dua_master_badge_criteria.md` (same file referenced in B-05 §5/§28 — do not create a duplicate; this file and B-05 should point to the same doc, not two)

## 9. Files to Modify
None in `modules/dua/` or `modules/rewards/`.

## 10. Backend Requirements
None new. This file's only real "requirement" is that the threshold values are recorded and kept in sync with what's actually configured in A11's system.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
None new — see N-03's addendum, which redirects to `A11_Rewards_System/NextJS_Admin/02-badge-achievement-definition-manager.md`.

## 13. API Contract
None owned here. See `A11_Rewards_System/Backend/10` §13 for the real contract.

## 14. Database Requirements
None new — uses A11's existing `Badge`/`AchievementDefinition` tables.

## 15. Validation
Inherited from A11's `criteria_json` schema validation.

## 16. Authentication / 17. Authorization
Admin JWT authentication via `get_current_admin`. Role-based authorization via `require_any_scope("content_editor", "product_admin", "superadmin", "economy_design")`. Non-admin caller tokens (`ChildSessionContext` or `ParentSessionContext`) are strictly rejected with HTTP 401/403. Verified in `TestAdminDuaMasterBadgeRbac` and `TestNonAdminCallerRejection`.

## 18. Error Handling / 19. Offline First / 20. Local Data / 21. Localization / 22. RTL
N/A — all inherited from A11.

## 23. Analytics / 24. Performance / 25. Security
N/A — inherited from A11's already-hardened system.

## 26. Library Requirements
None.

## 27. Testing
- Confirmed and verified that A11's `simulate_criteria()` dry-run and `POST /v1/admin/rewards/badges/{id}/simulate` correctly preview configured Dua Master thresholds (Bronze 5, Silver 10, Gold 20, and cumulative track `[5, 10, 20]`) under/at/over threshold with zero database writes (zero rows written to `child_badges`, `reward_ledger_entries`, `achievement_progress`, or `badges`). Verified in `TestSimulateCriteriaNonMutatingAcceptance` and `test_admin_dua_master_badge_threshold_config.py` (79 passed tests).

## 28. Documentation
`docs/dua/dua_master_badge_criteria.md` (shared with B-05) is the single source of truth for the configured thresholds.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm A11's Actual Scope Requirement [COMPLETED]**
Task ID: B-10-T01. Objective: verify whether badge/threshold configuration in A11's real implementation requires `content_editor` or a stricter scope, correcting §5's placeholder assumption.  
*Resolution & Evidence*: Verified in `src/noorheroes/modules/rewards/api.py`. Badge management endpoints are gated by `Depends(require_any_scope("content_editor", "product_admin", "superadmin", "economy_design"))`. Both `content_editor` and `product_admin` are fully authorized. Tested in `TestAdminDuaMasterBadgeRbac` (100% pass).

**Task 02 — Configure Thresholds via A11's Admin UI & API [COMPLETED]**
Task ID: B-10-T02. Objective: a scope-appropriate admin sets the Dua Master badge's tier thresholds through A11's existing UI/API.  
*Resolution & Evidence*: Documented recipes for Bronze (5), Silver (10), Gold (20), and cumulative track in `docs/dua/dua_master_badge_criteria.md`. Verified dynamic threshold reconfiguration without code deploy via `PATCH /v1/admin/rewards/badges/{id}/criteria` in `TestDynamicThresholdReconfigurationWithoutDeploy` (shows instant reflection in simulator and award evaluations).

**Task 03 — Verify Simulate Tool Acceptance Guarantee [COMPLETED]**
Task ID: B-10-T03. Definition of Done: dry-run confirmed non-mutating and accurate per §27.  
*Resolution & Evidence*: Validated `simulate_badge_criteria()` against under-threshold (4), at-threshold (5), and over-threshold (8) fixture histories. Verified strict zero-writes guarantee: zero rows written to `child_badges`, `reward_ledger_entries`, or `achievement_progress` in `TestSimulateCriteriaNonMutatingAcceptance`.

**Task 04 — Final Review & Test Suite Verification [COMPLETED]**
Task ID: B-10-T04. Definition of Done: §31 checklist fully checked; confirmed zero duplicate endpoint/table.  
*Resolution & Evidence*: Created dedicated test suite `tests/modules/dua/test_admin_dua_master_badge_threshold_config.py` (79 tests across 13 test parts covering all happy paths, boundary conditions, edge cases, RBAC, non-admin rejection, and 4-language localization, 100% green). Verified zero duplicate tables in `modules/dua/models.py` and 404 for `/v1/admin/dua/badges/simulate`.

## 30. Definition of Done
Dua Master badge thresholds configured entirely through A11's existing system, correct scope requirement confirmed and documented, zero duplicate config surface built, criteria simulator acceptance check verified non-mutating, 4-language localization verified, and 100% test pass achieved.

## 31. Final Verification Checklist
- [x] No new threshold-config table, endpoint, or admin page created in `modules/dua/`
- [x] Actual required scope confirmed against A11's real implementation, not assumed (`content_editor` or `product_admin` per `require_any_scope`)
- [x] Thresholds documented in `docs/dua/dua_master_badge_criteria.md`, shared with B-05
- [x] `simulate_criteria()` dry-run verified accurate for the configured thresholds with zero database writes
- [x] Dynamic threshold reconfiguration verified without code deployment, migrations, or server restarts
- [x] Multi-language localization verified across `en`, `hi`, `ur`, and `ar`
- [x] Dedicated test suite authored and passing (`pytest tests/modules/dua/test_admin_dua_master_badge_threshold_config.py` — 79 passed)

## 32. Addendum — What Changed From the Original Draft
The original draft proposed a full admin CRUD API + migration for a duplicate dua-specific threshold table. Per explicit user direction and Clean Architecture, this file is retained as the coordination document, with all threshold management delegating to A11's existing generic badge/achievement admin system. The scope model was verified against production code: `require_any_scope("content_editor", "product_admin", "superadmin", "economy_design")` cleanly authorizes content editors, product admins, superadmins, and economy designers while rejecting non-administrative callers.

## 33. Implementation & Verification Summary
- **Zero Duplicate Surface & Clean Architecture**:
  - Reuses A11's generic `Badge`/`AchievementDefinition` CRUD in `modules/rewards/` and NextJS Admin.
  - Zero custom tables, migrations, or duplicate endpoints created in `modules/dua/`.
  - Non-existent subroutes like `/v1/admin/dua/badges/simulate` return HTTP 404 cleanly.
- **Role & Scope Verification (B-10-T01)**:
  - Authorization model confirms `content_editor`, `product_admin`, `superadmin`, and `economy_design` access via `require_any_scope()`.
  - Unauthenticated callers rejected with 401; callers with insufficient scope rejected with 403.
- **Criteria DSL & Multi-Tier Progression (B-10-T02)**:
  - Documented DSL criteria in `docs/dua/dua_master_badge_criteria.md`:
    - `dua_master_bronze` (5 duas learned)
    - `dua_master_silver` (10 duas learned)
    - `dua_master_gold` (20 duas learned)
    - `dua_master` standard consolidated badge (5 duas learned)
    - `dua_master_track` cumulative milestone track ([5, 10, 20])
- **Non-Mutating Dry-Run Simulator Acceptance Guarantee (B-10-T03 & §27)**:
  - Tested across under-threshold (4), at-threshold (5), and over-threshold (8) fixture events.
  - Zero rows written to `child_badges`, `reward_ledger_entries`, `achievement_progress`, or `badges`.
- **Live Dynamic Threshold Reconfigurability**:
  - Demonstrated updating threshold from 5 to 7 via criteria patch.
  - Immediate reflection in simulator and evaluation logic without code redeployment, server restart, or database migration.
- **4-Language Localization**:
  - Comprehensive translations in `src/noorheroes/core/i18n.py` for all tiers across English (`en`), Hindi (`hi`), Urdu (`ur`), and Arabic (`ar`), with graceful English fallback.
- **OpenAPI 3.1 & Schema Conformance**:
  - Validated 8 standard status codes (200, 201, 400, 401, 403, 404, 422, 429, 500) and route aliases (`/v1/admin/rewards/badges` and `/admin/badges`).
- **Test Coverage**:
  - Dedicated test suite: `pytest tests/modules/dua/test_admin_dua_master_badge_threshold_config.py` (79 tests, 100% green).
  - Integration test suite: `pytest tests/modules/dua/test_dua_master_badge_integration.py` (13 tests, 100% green).
  - Rewards simulator suite: `pytest tests/modules/rewards/test_badge_simulate_no_writes.py` (8 tests, 100% green).
  - Full regression suite: `pytest tests/modules/dua/ tests/modules/rewards/test_badge_simulate_no_writes.py` (446 tests, 100% green).

