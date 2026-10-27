# B-11 — Admin Cross-Domain Spaced Repetition Configuration & Graph Validation API

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). Two closely related governance surfaces bundled in one sub-feature: (1) the global daily-review-prompt-cap setting B-07 reads, and (2) the cross-domain prerequisite-graph cycle-detection validation that gates B-01's cross-domain prerequisite support.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
B-11 — Admin Cross-Domain Spaced Repetition Configuration & Graph Validation API (Admin API)

## 4. Objective
Implement (1) an update-only settings endpoint for the global `daily_review_prompt_cap`, and (2) a cross-domain extension of A.5's existing cycle-detection validator so it evaluates the combined prerequisite graph across ALL domains, not per-domain in isolation.

## 5. Business Requirements
- Admin Requirements (A.9 PRD §8): "Cross-Domain Spaced Repetition Configuration: the global daily-prompt-cap setting lives here, distinct from any domain-specific configuration"; "Cross-Domain Skill Graph Validation: Extends A.5's curriculum-graph cycle-detection to validate across domains."
- CRUD permissions: Spaced Repetition Cross-Domain Config = Update-only behind `product_admin`; Graph Validation = part of existing `curriculum_editor` role's tooling.
- Error Handling table: cross-domain prerequisite graph cycle rejected at admin-save time with the cycle path shown.
- Edge Case 6/11: prerequisite cycles and cross-domain prerequisite references must both be handled uniformly across any domain's graph.

## 6. Existing Architecture
FastAPI async Python 3.12, SQLAlchemy 2.0, PostgreSQL. A.5's existing Curriculum Builder (`09-admin-quran-skill-tree-curriculum-management-api.md`) already implements per-domain cycle-detection validation on `skill_node.prerequisite_node_ids`. This sub-feature extends that existing validator's scope rather than writing a new one.

## 7. Existing Code to Reuse
- A.5's existing cycle-detection validation function (wherever it lives in the `learning`/`admin` context's curriculum-save flow) — extend its graph-traversal scope to span all domains, do not fork a second validator.
- B-01's `SkillDomainService` (to confirm the graph traversal genuinely spans all registered domains).
- B-07's `spaced_repetition_scheduler.py` (consumer of the config this sub-feature manages).

## 8. Files to Create
- `src/noorheroes/modules/admin/schemas/spaced_repetition_config_admin.py` — `SpacedRepetitionConfigRequest/Response`.
- `tests/modules/admin/test_cross_domain_spaced_repetition_config_api.py`
- `tests/modules/learning/test_cross_domain_graph_validation.py`

## 9. Files to Modify
- `src/noorheroes/modules/admin/api.py` — add `GET/PUT /admin/v1/mastery/spaced-repetition-config`.
- A.5's existing curriculum-save cycle-detection validator function — extend its query/traversal to consider `skill_node` rows across all domains when checking for cycles, since prerequisites may now be cross-domain (Edge Case 11).

## 10. Backend Requirements
- **`GET/PUT /admin/v1/mastery/spaced-repetition-config`** — single global setting, `daily_review_prompt_cap` (default 2), no per-domain variant exposed here (explanatory copy in the response/UI clarifies this scope, per A.9 PRD §9 Admin AI Prompt item 4).
- **Update-only:** no create/delete semantics — this is a singleton configuration row (or a well-known config key in an existing admin-settings table, whichever pattern the platform already uses for global settings).
- **Cross-domain cycle detection (extends A.5's existing validator, no new page):** when Admin saves any `skill_node`'s `prerequisite_node_ids` via the existing Curriculum Builder save flow, the validator now traverses the FULL combined graph across all domains (not scoped to the node's own domain), correctly detecting a cycle that spans e.g. a Quran node depending on an Arabic node which depends back on the original Quran node.
- **Cycle rejection:** on detection, the save is rejected with the specific cycle path shown in the error response (existing A.5 behavior, generalized in scope).

## 11. KMP Requirements
N/A directly (admin-only).

## 12. NextJS Requirements
Directly backs N-03 (Cross-Domain Spaced Repetition Configuration settings form) and N-04 (Cross-Domain Skill Graph Validation, surfaced through the existing Curriculum Builder save flow, no new page per the top-level PRD's explicit instruction).

## 13. API Contract

**`GET /admin/v1/mastery/spaced-repetition-config`**
- **Auth:** Bearer (admin), `product_admin`
- **Response 200:** `{ "daily_review_prompt_cap": 2 }`

**`PUT /admin/v1/mastery/spaced-repetition-config`**
- **Auth:** `product_admin`
- **Request:** `{ "daily_review_prompt_cap": 3 }`
- **Response 200:** updated config.
- **Validation:** `daily_review_prompt_cap >= 1`.
- **Error Responses:** `422` (invalid value), `401`/`403`.

**Cycle validation** is not a standalone endpoint — it's enforced inside A.5's existing curriculum-save endpoint (e.g. `PUT /admin/v1/curriculum/skill-nodes/{id}`), whose error response now includes the cycle path when a cross-domain cycle is detected:
```json
{ "error": "prerequisite_cycle_detected", "cycle_path": ["quran:node_1", "arabic:node_7", "quran:node_1"] }
```

## 14. Database Requirements
- `spaced_repetition_config` (or equivalent existing global-settings table/pattern) — single row or well-known key holding `daily_review_prompt_cap`.
- No new tables for graph validation (operates over existing `skill_node.prerequisite_node_ids`).

## 15. Validation
- `daily_review_prompt_cap` must be a positive integer, sane upper bound (e.g., ≤ 10, to prevent a misconfiguration from overwhelming children).
- Cycle detection must correctly identify cycles that span multiple domains, not just single-domain cycles (this is the new behavior this sub-feature adds).

## 16. Authentication
Bearer JWT, admin-session scope.

## 17. Authorization
Config update: `product_admin` only. Graph validation: enforced as part of the existing `curriculum_editor` role's save flow (no separate role needed, since it's a validation extension, not a new mutating action).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `daily_review_prompt_cap` set to 0 or negative | `422` |
| Cross-domain prerequisite graph contains a cycle | Rejected at admin-save time with the cycle path shown (shared validation mechanism with A.5, now cross-domain-aware) |
| Large combined graph causes validation timeout | Validation runs with a reasonable time budget; on timeout, save is rejected with a "graph too large to validate, contact engineering" message rather than silently skipping validation |
| Wrong role attempts config update | `403` |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Explanatory copy about the "applies across all domains" scope should be localizable if the Admin Portal supports multiple admin-facing languages; otherwise English-only is acceptable for internal tooling (confirm against existing Admin Portal localization scope).

## 22. RTL
N/A (backend; Admin UI RTL owned by N-03/N-04 if applicable).

## 23. Analytics
Audit-log entry on every config update (who changed the cap, from what value to what value, when).

## 24. Performance
Cycle-detection traversal over the combined multi-domain graph must remain performant as the total `skill_node` count grows across all domains — reuse/extend A.5's existing algorithm's complexity characteristics rather than introducing a naive full-graph re-scan on every single node edit if the existing implementation was already optimized for incremental checking.

## 25. Security
Config-update gated behind `product_admin`; cycle-detection is a data-integrity control, not a security boundary per se, but prevents admin error from corrupting the skill graph platform-wide.

## 26. Library Requirements
No new libraries (reuses A.5's existing graph-traversal implementation/library choice).

## 27. Testing
- Unit: config validation boundary cases (0, negative, very large values).
- Cross-domain cycle test: construct a cycle spanning two domains (e.g., Quran node → Arabic node → back to the original Quran node), assert rejection with the correct cycle path.
- Regression: existing A.5 single-domain cycle-detection tests still pass unchanged.
- RBAC test: config update requires `product_admin`.

## 28. Documentation
OpenAPI schema for the config endpoint; update A.5's existing cycle-detection documentation to note it is now cross-domain-scoped, cross-referenced from B-01's Edge Case 11 handling.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Spaced Repetition Config Admin Endpoint**
- Task ID: B-11-T01
- Objective: Update-only global config surface.
- Why This Is Required: B-07's cap logic and N-03's settings form both need this.
- Existing Architecture to Follow: Existing admin-settings pattern (singleton row or config-key convention).
- Existing Files to Reuse: `require_role`, audit-log helper.
- Files to Create: `schemas/spaced_repetition_config_admin.py`.
- Files to Modify: `admin/api.py`.
- Implementation Details: `GET`/`PUT` over a single config value; `PUT` invalidates any cache B-07 reads this config through.
- Business Rules: Update-only, no create/delete.
- Validation: Per §15. Error Handling: Per §18.
- Security: `product_admin` role, audit log.
- Performance: N/A. Localization: Per §21. RTL: N/A.
- Analytics: Audit-log entry with before/after values.
- Tests: `test_cross_domain_spaced_repetition_config_api.py`.
- Documentation: OpenAPI schema.
- Dependencies: B-07.
- Do Not Change: B-07's decay-function logic itself.
- Expected Result: Working config endpoint.
- Definition of Done: RBAC + validation tests green; B-07 confirmed to read the updated value correctly.

**Task 02 — Extend Cycle-Detection Validator to Cross-Domain Scope**
- Task ID: B-11-T02
- Objective: Make A.5's existing single-domain cycle detector traverse the full combined graph.
- Why This Is Required: B-01's cross-domain prerequisite support (Edge Case 11) is unsafe without this — a cross-domain cycle would otherwise go undetected.
- Existing Architecture to Follow: A.5's existing validator implementation, extended in scope.
- Existing Files to Reuse: The existing cycle-detection function itself — locate and extend it, do not duplicate.
- Files to Create: `tests/modules/learning/test_cross_domain_graph_validation.py`.
- Files to Modify: The existing cycle-detection validator (exact file path depends on where A.5 implemented it — locate via the `learning`/`admin` context's curriculum-save flow before modifying).
- Implementation Details: Remove any domain-scoping filter from the graph-traversal query so it considers all `skill_node` rows regardless of `domain` when building the prerequisite graph for cycle detection.
- Business Rules: Cycle path in the error response must show the actual cross-domain path (e.g., `domain:node_id` pairs) so admins can understand and fix it.
- Validation: N/A. Error Handling: Per §18 (timeout handling for large graphs).
- Security: N/A. Performance: Per §24 — verify no regression on existing single-domain validation speed.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: Cross-domain cycle construction test; regression test confirming existing A.5 single-domain cycle tests still pass.
- Documentation: Update existing validator's docstring/comments.
- Dependencies: B-01 (cross-domain `skill_node.domain` field), B-09.
- Do Not Change: The validator's core cycle-detection algorithm (e.g., if it's DFS-based, keep it DFS-based) — only its graph-traversal scope changes.
- Expected Result: Cross-domain cycles now correctly detected and rejected.
- Definition of Done: Cross-domain cycle test passes; existing A.5 regression tests unaffected.

## 30. Definition of Done
Global spaced-repetition daily-cap config live and update-gated behind `product_admin`; A.5's existing cycle-detection validator correctly extended to detect cross-domain prerequisite cycles at admin-save time, with the cycle path surfaced in the rejection error, and zero regression to existing single-domain validation behavior.

## 31. Final Verification Checklist
- [x] Config GET/PUT working, `product_admin`-gated
- [x] B-07 confirmed reading the live config value (no stale cache after update)
- [x] Cross-domain cycle correctly detected and rejected with cycle path shown
- [x] Existing A.5 single-domain cycle-detection tests unaffected (regression-checked)
- [x] Large-graph validation timeout handled gracefully, not silently skipped
- [x] Audit log entries for config changes

## 32. Verification Evidence & Test Results
- **Dedicated B-11 Test Suites (63 passed in 2.46s, 100% green)**:
  - *Spaced Repetition Config Admin API (`tests/modules/admin/test_cross_domain_spaced_repetition_config_api.py`)*: 24 passed in 0.85s.
    - Dual route mount parity: `GET /admin/v1/mastery/spaced-repetition-config` and canonical `/v1/admin/mastery/spaced-repetition-config`.
    - RBAC authorization: `product_admin` and `super_admin` permitted; unauthorized roles (`curriculum_editor`, `learning_science`, `support_agent`, etc.) receive HTTP 403 Forbidden; unauthenticated requests receive HTTP 401.
    - Update validation: $1 \le \text{daily\_review\_prompt\_cap} \le 10$ enforced; values $\le 0$ or $> 10$ rejected with HTTP 422.
    - Explanatory copy: `scope_explanation` returned in response clarifying global/cross-domain scope per PRD §9 Item 4.
    - Cache invalidation: `PUT` evicts Redis key `noorheroes:learning:config:spaced_repetition`.
    - Audit logging: writes immutable `AdminAuditRecord` (`action="spaced_repetition_config_updated"`) with complete before/after diffs, admin ID, and timestamps in identical transaction.
    - Direct curriculum save cycle rejection: verifies save-time rejection with HTTP 409 and cycle path on `/admin/v1/curriculum/skill-nodes/{id}` and `/admin/v1/learning/skill-nodes/{id}`.
  - *Cross-Domain Graph Validation (`tests/modules/learning/test_cross_domain_graph_validation.py`)*: 11 passed in 0.42s.
    - Multi-domain cycle detection: 3-color DFS correctly detects cycles spanning multiple domains (e.g. `quran:node_1 -> arabic:node_7 -> quran:node_1`).
    - Domain tagging: cycle path returns domain-prefixed node identifiers for cross-domain cycles.
    - Single-domain non-regression: cycles within a single domain preserve raw node IDs (`["n1", "n2", "n1"]`).
    - Save-time rejection: raises `CurriculumCycleDetectedError` (HTTP 409).
    - Timeout protection: raises `CurriculumGraphTimeoutError` (HTTP 504 `GRAPH_VALIDATION_TIMEOUT`) when traversal budget is exceeded.
  - *Cross-Domain Daily Cap Consumption (`tests/modules/learning/test_cross_domain_daily_cap.py`)*: 28 passed in 1.19s.
    - Dynamic config consumption: B-07 `spaced_repetition_scheduler` immediately reads updated cap without stale cache.
    - Cross-domain enforcement: daily review prompts capped across all domains combined.
- **Full Admin Bounded Context Suite (`tests/modules/admin/`)**: 443 passed in 11.67s across all 25 test files (100% green).
- **Full Learning Bounded Context Suite (`tests/modules/learning/`)**: 1,083 passed in 19.31s across all test files (100% green).
- **Core Exceptions & I18n Suites (`tests/core/`)**: 263 passed in 35.37s (100% green, including zero-missing error catalog and script purity in `tests/core/test_i18n.py`).
- **Architectural Invariant Suites (`tests/architecture/` & `tests/api/v1/test_routing.py`)**: 255 passed, 4 skipped (Windows non-bash); thin-controller AST branching check proves 0 `ast.If` nodes in router endpoints.
- **OpenAPI Breaking Change Classifier (`src/noorheroes/scripts/classify_openapi_diff.py`)**: 0 breaking changes detected against `openapi.baseline.json`.

