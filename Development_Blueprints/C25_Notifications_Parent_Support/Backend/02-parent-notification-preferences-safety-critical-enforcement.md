# Blueprint: Parent Notification Preferences & Safety-Critical Category Enforcement

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI, Modular Monolith). Extends the existing `notifications` bounded context. This blueprint delivers the single most important guarantee of C.25: a safety-critical notification category (deletion grace period, billing failure) can **never** be fully disabled at the schema/validation layer — only its delivery channel may be adjusted.

## 2. Parent Feature
C.25 — Notifications (Parent) & Support.

## 3. Sub-feature
B-02 — Parent Notification Preferences & Safety-Critical Category Enforcement.

## 4. Objective
Implement `GET/PATCH /v1/parent/notification-preferences` writing to the **shared** `notification_preferences` table (B.17 §4.1) with `child_id = null` for parent-scoped rows, enforcing via an extensible category-registry `safety_critical` flag that `enabled: false` and empty-`channels` requests are structurally rejected for safety-critical categories.

## 5. Business Requirements
Source: PRD §1.7 FR-3, FR-4, FR-11; §1.8 Safety-Critical Delivery Guarantee; §1.9 Acceptance Criteria (no "turn off completely" option exists); §1.10 Edge Case 5; §3.4; §5 Backend AI Code-Generation Prompt items 1–2.
- **FR-3/FR-4 (zero-exception rule):** "Safety-critical notifications... cannot be fully disabled, only de-prioritized in delivery channel" — a parent may downgrade *how* it arrives (e.g., push de-prioritized in favor of email-only) but never opt out of receiving it through *some* channel entirely.
- This is enforced "at the preference-model layer... these categories simply have no 'fully off' state representable in the schema, not merely a UI restriction" (§1.8).
- Category registry's `safety_critical` flag must be **extensible** — "using a category registry's `safety_critical` flag, not a hardcoded category-name check" (§3.5) — so a future new safety-critical category requires no code change to be correctly enforced.
- `child_id = null` for parent-scoped rows is this feature's exact counterpart of B.17's shared schema (FR-11) — this endpoint writes rows the Policy Engine (B.17) reads; no divergent preference model.
- A de-prioritized channel must still actually deliver — "de-prioritized never means sometimes doesn't arrive at all" (Edge Case 5) — this is chiefly a Policy Engine (B.17) send-time concern, but this blueprint's validation must never accept a configuration that could produce a fully-undeliverable safety-critical category (i.e., the empty-channels rejection is the preventive half of that guarantee).

## 6. Existing Architecture
Per `FAST-API-INSTRUCTIONS.md` §5.8 `notifications` context: `NotificationPreference` model, `NotificationRepository.get_preferences_by_user_id()`. Per B.17 §4.2: `notification_preferences` — "FK `parent_id`, `child_id` (nullable for parent-only types); UNIQUE(`parent_id`, `child_id`, `channel`, `type`)". `core/exceptions.py` `ValidationError` (422). `common/schemas.py` `NoorHeroesBaseModel`.

## 7. Existing Code to Reuse
- `notification_preferences` table exactly as defined by B.17 (§4.2) — reuse the `UNIQUE(parent_id, child_id, channel, type)` constraint; do not add a competing table.
- `NotificationPreference` ORM model and `NotificationRepository.get_preferences_by_user_id()` — extend for parent-scoped (`child_id IS NULL`) queries rather than duplicating.
- `ValidationError` (`core/exceptions.py`) for the `422 SAFETY_CRITICAL_CANNOT_DISABLE` response.
- Parent-Session-Only Gate pattern (see B-01/C.20's B-01).

## 8. Files to Create
- `src/noorheroes/modules/notifications/category_registry.py` — the `safety_critical`-flagged category reference data/enum-with-metadata.
- `tests/modules/notifications/test_parent_preferences_safety_critical.py`

## 9. Files to Modify
- `src/noorheroes/core/exceptions.py` — add `SafetyCriticalCannotDisableError(ValidationError)` with `error_code="SAFETY_CRITICAL_CANNOT_DISABLE"`.
- `src/noorheroes/modules/notifications/schemas.py` — add `NotificationPreferenceResponse`, `NotificationPreferencePatchRequest` (`category`, `enabled`, `channels`, `quiet_hours`).
- `src/noorheroes/modules/notifications/repository.py` — add `get_parent_preferences(parent_id)`, `upsert_preference(parent_id, category, enabled, channels, quiet_hours)`.
- `src/noorheroes/modules/notifications/service.py` — add `NotificationService.get_parent_preferences()` / `update_parent_preference()`, calling into the category registry for validation.
- `src/noorheroes/modules/notifications/api.py` — add `GET/PATCH /v1/parent/notification-preferences`.

## 10. Backend Requirements
- Category registry: a small reference table or `enum`-with-metadata structure, e.g. `CategoryDefinition(code: str, safety_critical: bool, default_channels: list[str])`, covering at minimum `deletion_grace_period`, `billing_failure` (both `safety_critical=True`) and `new_content_updates` (or equivalent marketing category, `safety_critical=False`) — sourced from/consistent with whatever category set B.17's Policy Engine already recognizes (do not invent category codes divergent from B.17's trigger catalog; confirm against B.17's `notification_preferences.type` values before finalizing the registry's `code` set).
- `PATCH` validation order: (1) resolve `category` against the registry — unknown category → `422` generic validation error; (2) if `registry[category].safety_critical` and `enabled == False` → raise `SafetyCriticalCannotDisableError` (`422 SAFETY_CRITICAL_CANNOT_DISABLE`); (3) if `registry[category].safety_critical` and `channels == []` → raise the same error class (or a channels-specific variant sharing the `SAFETY_CRITICAL_CANNOT_DISABLE` code family) — a safety-critical category must always retain at least one enabled channel; (4) otherwise, persist.
- Non-safety-critical categories accept `enabled: false` freely, and may set `channels: []` (fully muted) without error.
- `quiet_hours` persisted only for non-safety-critical categories; a `quiet_hours` value submitted for a safety-critical category is either ignored (documented in the response) or rejected — pick one and apply consistently (recommend: reject with a clear validation message, since silently ignoring user input is a worse UX than an explicit rejection).
- All writes target `child_id = null` rows exclusively (FR-11) — this endpoint must never accept or write a `child_id`.

## 11. KMP Requirements
N/A for backend scope — consumed by K-02's `NotificationPreferencesViewModel`, which renders control type (toggle vs. channel-selector) purely from the `safety_critical` field returned by `GET`.

## 12. NextJS Requirements
N/A — this endpoint has no admin-facing counterpart in this blueprint (the category registry itself is developer/config-owned, not admin-editable, per PRD's silence on an admin category-management screen; do not invent one).

## 13. API Contract
### `GET /v1/parent/notification-preferences`
- **Auth:** Bearer (Parent session only)
- **Response 200:** `{ "categories": [ { "category": "billing_failure", "safety_critical": true, "enabled": true, "channels": ["push","email"], "quiet_hours": null }, ... ] }`

### `PATCH /v1/parent/notification-preferences`
- **Request:** `{ "category": "billing_alerts", "enabled": true, "channels": ["push","email"], "quiet_hours": null }` (PRD §3.4 exact shape)
- **Response 200:** Updated `NotificationPreferenceResponse` for the affected category.
- **Error 422 `SAFETY_CRITICAL_CANNOT_DISABLE`:** `{ "error_code": "SAFETY_CRITICAL_CANNOT_DISABLE", "message": "..." }` — returned for both the `enabled:false` and empty-`channels` rejection cases.

## 14. Database Requirements
None new — writes to the existing `notification_preferences` table (B.17 §4.2), scoped to `child_id IS NULL`. Category registry is application-level reference data (Python module or a small lookup table), not a new mutable schema unless the team decides categories should be DB-driven for admin editability in a future iteration — out of scope here.

## 15. Validation
- `category` must resolve against the registry.
- `enabled: false` rejected for `safety_critical=true` categories.
- `channels: []` rejected for `safety_critical=true` categories.
- `channels` values must be within the platform's known channel set (e.g., `push`, `email`, `sms` if applicable — confirm against B.17's actual channel enum rather than inventing new channel names).

## 16. Authentication
Reuses `get_current_parent()`. No new auth mechanism.

## 17. Authorization
Parent-Session-Only Gate; `child_id = null` scoping structurally prevents this endpoint from ever touching a child-scoped preference row (those remain B.17's exclusive concern).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `enabled:false` on safety-critical category | `422 SAFETY_CRITICAL_CANNOT_DISABLE` |
| `channels:[]` on safety-critical category | `422 SAFETY_CRITICAL_CANNOT_DISABLE` |
| `enabled:false` on non-safety-critical category | `200`, persisted |
| Unknown `category` value | `422` generic validation error |
| Child-mode token | `403 CHILD_MODE_TOKEN_REJECTED` |
| Concurrent PATCH race on same category | Last-write-wins is acceptable given single-parent-editing-own-preferences nature, but confirm no double-insert violates the `UNIQUE(parent_id, child_id, channel, type)` constraint — use upsert semantics |

## 19. Offline First
N/A server-side.

## 20. Local Data
N/A.

## 21. Localization
Category display names/descriptions are client-owned (K-02) via localization keys, not server-rendered strings — this endpoint returns machine-readable `category` codes only.

## 22. RTL
N/A (backend).

## 23. Analytics
No server-side event emission; `notification_category_toggled`, `notification_quiet_hours_set`, `safety_critical_category_disable_attempt_blocked` (PRD §1.19) are client-fired (K-02) — the client fires `safety_critical_category_disable_attempt_blocked` when its own local UX check intercepts an attempt, and equally when the server rejects one that slipped through, so ensure the `422` error code is distinguishable enough for the client to map it to this specific event.

## 24. Performance
Negligible — small per-category upserts against an indexed, already-existing table. No new indexes required beyond B.17's existing `UNIQUE(parent_id, child_id, channel, type)`.

## 25. Security
This is the schema-layer half of the feature's single highest-stakes guarantee (alongside B-04's ticket/cancellation separation). No sensitive PII beyond preference metadata; standard family-scoped access control.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: `PATCH` with `enabled:false` for `deletion_grace_period` → `422 SAFETY_CRITICAL_CANNOT_DISABLE`.
2. Unit test: `PATCH` with `enabled:false` for `billing_failure` → `422 SAFETY_CRITICAL_CANNOT_DISABLE`.
3. Unit test: `PATCH` with `enabled:false` for `new_content_updates` (non-safety-critical) → `200`, persisted successfully.
4. Unit test: `PATCH` with `channels: []` for a safety-critical category → `422 SAFETY_CRITICAL_CANNOT_DISABLE`.
5. Unit test: `PATCH` with `channels: []` for a non-safety-critical category → `200`, persisted successfully.
6. Unit test: category registry lookup is data-driven — adding a new category to the registry with `safety_critical=True` (in a test double) is immediately enforced without touching the validation function's code (proves no hardcoded name check exists).
7. Integration test: `GET` returns the `safety_critical` flag correctly per category for K-02's rendering logic to consume.
8. Integration test: child-mode token rejected on both routes.
9. Integration test: written rows have `child_id IS NULL` always.

## 28. Documentation
- OpenAPI: document the `422 SAFETY_CRITICAL_CANNOT_DISABLE` response schema explicitly on the `PATCH` operation.
- Docstring on the category registry module citing PRD FR-3/FR-4 as the source of the `safety_critical` semantics.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Build the Category Registry**
- Task ID: B02-T01
- Objective: Data-driven, extensible `safety_critical` metadata source.
- Why This Is Required: PRD explicitly forbids a hardcoded category-name check (§3.5, §5 item 1).
- Existing Architecture to Follow: Simple reference-data module pattern already used elsewhere in `common/utils/` (e.g., `AgeBand` enum) as a style reference — this is closer to a metadata dict than a Kotlin-style sealed enum, since each entry carries a boolean flag.
- Existing Files to Reuse: Confirm B.17's existing `notification_preferences.type`/category value set before finalizing codes.
- Files to Create: `modules/notifications/category_registry.py`.
- Files to Modify: none.
- Implementation Details: `CATEGORY_REGISTRY: dict[str, CategoryDefinition]` with at minimum `deletion_grace_period`, `billing_failure` (`safety_critical=True`) and one marketing category (`safety_critical=False`); a lookup function `get_category(code) -> CategoryDefinition | None`.
- Business Rules: FR-3, FR-4.
- Validation: N/A (this is the source of truth for validation, not itself validated).
- Error Handling: N/A.
- Security: This IS the core control.
- Performance: In-memory dict lookup, negligible.
- Localization: N/A (codes only, no display strings).
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: Docstring per §28.
- Dependencies: None.
- Do Not Change: N/A.
- Expected Result: Registry importable and lookup-able.
- Definition of Done: Matches B.17's category set exactly, no invented codes.

**Task 02 — Implement Repository Methods**
- Task ID: B02-T02
- Objective: `get_parent_preferences()` / `upsert_preference()` on `NotificationRepository`.
- Why This Is Required: Data-access layer, `child_id = null` scoped.
- Existing Architecture to Follow: `BaseRepository` upsert conventions (or explicit get-then-update/insert if no generic upsert helper exists).
- Existing Files to Reuse: `common/base_repository.py`.
- Files to Create: none.
- Files to Modify: `modules/notifications/repository.py`.
- Implementation Details: Upsert against `UNIQUE(parent_id, child_id, channel, type)`, always with `child_id = null`.
- Business Rules: FR-11.
- Validation: N/A (service layer's job).
- Error Handling: N/A.
- Security: `child_id = null` hardcoded at the query layer, never accepted as a parameter from the request.
- Performance: Indexed upsert.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: Docstrings.
- Dependencies: Task 01.
- Do Not Change: Do not touch B.17's child-scoped preference write paths.
- Expected Result: Correct upsert behavior.
- Definition of Done: Matches §10.

**Task 03 — Implement Service-Layer Validation**
- Task ID: B02-T03
- Objective: `update_parent_preference()` enforcing the safety-critical rules.
- Why This Is Required: This is the actual guarantee-enforcement point.
- Existing Architecture to Follow: `BaseService`, `ValidationError` hierarchy.
- Existing Files to Reuse: `category_registry.py` (Task 01), `core/exceptions.py`.
- Files to Create: none.
- Files to Modify: `modules/notifications/service.py`, `core/exceptions.py` (add `SafetyCriticalCannotDisableError`).
- Implementation Details: Validation order exactly as specified in §10.
- Business Rules: FR-3, FR-4 — the two highest-priority guarantees.
- Validation: Category lookup, `enabled`/`channels` rules.
- Error Handling: Raises `SafetyCriticalCannotDisableError` mapping to `422 SAFETY_CRITICAL_CANNOT_DISABLE`.
- Security: Core control of this blueprint.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: Docstrings citing FR-3/FR-4.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: All 5 validation scenarios from §27 behave correctly.
- Definition of Done: Zero path exists to persist a fully-disabled or zero-channel safety-critical category.

**Task 04 — Add Routes with Parent-Session-Only Gate**
- Task ID: B02-T04
- Objective: Expose `GET`/`PATCH` under the existing gate pattern.
- Why This Is Required: Consistency with B-01 and C.20's established pattern.
- Existing Architecture to Follow: Same gate dependency used in B-01 (reuse, do not re-implement).
- Existing Files to Reuse: `modules/notifications/api.py`.
- Files to Create: none.
- Files to Modify: `modules/notifications/api.py`, `modules/notifications/schemas.py`.
- Implementation Details: Both routes under `NotificationRouter`.
- Business Rules: N/A.
- Validation: Pydantic request schema.
- Error Handling: Per §18.
- Security: Router-level gate.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: OpenAPI.
- Dependencies: Task 03.
- Do Not Change: Do not alter B-01's routes.
- Expected Result: Both routes live.
- Definition of Done: Matches §13.

**Task 05 — Write Test Suite**
- Task ID: B02-T05
- Objective: Cover all 9 cases in §27.
- Why This Is Required: PRD §5 items 1–2 mandate exactly these tests.
- Existing Architecture to Follow: pytest conventions.
- Existing Files to Reuse: Existing auth fixtures.
- Files to Create: `tests/modules/notifications/test_parent_preferences_safety_critical.py`.
- Files to Modify: none.
- Implementation Details: All 9 cases from §27, treated as the highest-priority test suite in this sub-feature.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact `error_code` string.
- Security: This suite IS the security gate for FR-3/FR-4.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings citing FR-3/FR-4.
- Dependencies: Tasks 01–04.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green; CI treats this suite as mandatory per the same non-bypassable-gate principle B.17 applied to its own binding/policy tests.

## 30. Definition of Done
`GET/PATCH /v1/parent/notification-preferences` live, writing `child_id = null` rows to the shared `notification_preferences` table, with a data-driven category registry structurally preventing any safety-critical category from being fully disabled or reduced to zero channels, all tests green.

## 31. Final Verification Checklist
- [ ] `deletion_grace_period` and `billing_failure` cannot be set `enabled:false` (tested)
- [ ] Neither safety-critical category can be set to `channels: []` (tested)
- [ ] Non-safety-critical category CAN be fully disabled (tested)
- [ ] Category registry is data-driven, no hardcoded name checks in validation logic
- [ ] All writes have `child_id IS NULL`
- [ ] Child-mode token rejected
- [ ] No PostgreSQL/Redis credential files touched
- [ ] B.17's child-scoped preference logic untouched
