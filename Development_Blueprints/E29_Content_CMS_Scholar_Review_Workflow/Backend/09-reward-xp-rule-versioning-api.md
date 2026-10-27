# B-09 — Reward/XP-Rule Versioning API

## 1. Feature Context
The authoring-side origin point for A.11's non-retroactivity principle: a new XP rule or badge-criteria version is never an in-place edit of an existing live rule — it's always a new version, picked up by the Reward Engine for future events only, leaving historical ledger entries untouched forever.

## 2. Parent Feature
E.29 — Content CMS & Scholar Review Workflow

## 3. Sub-feature
1.9 Reward/XP-Rule Versioning API (ID: **B-09**)

## 4. Objective
Implement `POST /v1/admin/rewards` validating a reference to a valid event type and always inserting a new rule-version row, never updating an existing one — mirroring A.11's own reward-ledger append-only guarantee at its authoring source.

## 5. Business Requirements
- FR-11: reward/XP-rule content creation never disturbs historical ledger entries — new version validated, saved as new, old stays active until cutover, Reward Engine picks up the new rule for future events only.
- Edge Case 7: the rule version active at the moment an activity actually completes is the one applied, never retroactively recalculated based on which rule was live at request-processing time (mirrors A.9's "rule version active at time of completion" pattern) — this is enforced by A.11's Reward Engine at read/apply time, this module's job is only to never mutate history at the authoring layer.

## 6. Existing Architecture
`modules/content_cms/rewards/` sub-package, FK'd conceptually to A.11's event-type registry (read-only reference) but owning its own `reward_rule_version` table — this module is the authoring surface; A.11's Reward Engine (external, consumer-side) is what actually applies rule versions to events.

## 7. Existing Code to Reuse
- A.11's existing event-type registry/model (read-only reference — reuse, never fork a parallel event-type list)
- `common/base_service.py`, `common/base_repository.py`
- `modules/admin/audit/service.py::AuditLogService.log_action()` (E.28)

## 8. Files to Create
- `src/noorheroes/modules/content_cms/rewards/models.py` — `RewardRuleVersionOrm`
- `alembic/versions/xxxx_create_reward_rule_version.py`
- `src/noorheroes/modules/content_cms/rewards/schemas.py` — `RewardRuleCreateRequest`, `RewardRuleResponse`
- `src/noorheroes/modules/content_cms/rewards/repository.py` — `RewardRuleRepository` (no `update()` method — insert-only)
- `src/noorheroes/modules/content_cms/rewards/service.py` — `RewardRuleService(BaseService)`
- `src/noorheroes/modules/content_cms/rewards/api.py` — `RewardRuleRouter`
- `tests/modules/content_cms/rewards/test_reward_rule_service.py`
- `tests/modules/content_cms/rewards/test_no_update_statement.py`

## 9. Files to Modify
- `src/noorheroes/main.py` — register `RewardRuleRouter` under `/v1/admin/rewards`

## 10. Backend Requirements
- `RewardRuleService.create_version(payload, actor_id)`: validates `event_type` against A.11's existing registry; always calls `RewardRuleRepository.insert()` — the repository has no `update()` method defined at all, making an in-place mutation a compile-time-absent capability, not just a runtime-avoided one.
- The previous version remains `is_active=true` until an explicit, separate cutover action sets the new version active and the old inactive (both are inserts/flag-flips, never a destructive update of rule content itself).
- This service does not itself apply rules to events — that is A.11's Reward Engine's job, external to this module; this service only guarantees the authoring-side data never mutates in place.

## 11. API Contract

### `POST /v1/admin/rewards`
- Auth: `content_editor`+ role. Request: `{ event_type, xp_value, badge_criteria?, cutover_at? }`. Response 201: new rule version. Errors: `422 INVALID_EVENT_TYPE`.

## 12. Database Requirements
- `reward_rule_version`: FK to A.11's event-type reference; `is_active` boolean; append-only (no UPDATE grant on rows beyond the `is_active` flag-flip, ideally isolated to a narrow, explicitly-scoped cutover operation rather than a general-purpose update path).

## 13. Validation
`event_type` must reference a valid, existing event type in A.11's registry.

## 14. Authentication
Admin Bearer via `get_current_admin`.

## 15. Authorization
`require_admin_scope("content_editor")`.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Invalid/unknown `event_type` | `422 INVALID_EVENT_TYPE` |
| Attempted mutation of existing rule content | Structurally unavailable — no such method exists in the repository |
| Database failure | `503`, logged |

## 17. Security
Append-only-by-construction repository interface (no `update()` method) is the enforcement mechanism — not a runtime check that could be bypassed by a future careless call site, but an absent capability.

## 18. Analytics
`reward_rule_version_published` audited via `AuditLogService`.

## 19. Performance
Low-volume admin-write operation; no special performance requirements.

## 20. Library Requirements
No new libraries.

## 21. Testing
- Unit: `event_type` validation, insert-only creation.
- **Mandatory test**: static-analysis-style/reflection test confirming `RewardRuleRepository` contains no UPDATE statement against an existing rule-version row under any code path (per PRD backend AI-prompt requirement #8).
- Integration: create-new-version-while-old-remains-active flow.

## 22. Documentation
Update OpenAPI schema; document that this module intentionally has no rule-mutation capability, cross-referencing A.11's non-retroactivity guarantee as the reason.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `RewardRuleVersionOrm` Model & Migration**
Objective: Base table, append-only by design. Follow: existing SQLAlchemy/Alembic conventions. Tests: migration smoke test. Definition of Done: clean migration.

**Task 02 — Implement `RewardRuleRepository` with No `update()` Method**
Objective: Insert-only data access, explicit interface-level omission of any content-mutating method. Tests: **mandatory** — reflection/static test confirming absence of an UPDATE-issuing method. Definition of Done: test passes.

**Task 03 — Implement `RewardRuleService.create_version()`**
Objective: `event_type` validation against A.11's registry, insert-only creation. Dependencies: Task 02, A.11's event-type model (read-only import). Tests: invalid-event-type rejection. Definition of Done: test passes.

**Task 04 — Add Router Endpoint**
Objective: Wire `POST /v1/admin/rewards`. Tests: covered by Task 05. Definition of Done: endpoint live, documented.

**Task 05 — Add Unit & Integration Tests**
Objective: Full coverage per §21, including the mandatory static-analysis test. Definition of Done: all green in CI.

**Task 06 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify; document the intentional lack of mutation capability. Definition of Done: non-breaking diff confirmed.

**Task 07 — Final Code Review**
Objective: Confirm zero UPDATE statement against rule content exists anywhere in this module. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] `RewardRuleRepository` has no method capable of mutating existing rule-version content
- [ ] `event_type` validated against A.11's existing registry before every creation
- [ ] New versions are always inserted, old versions remain active until explicit cutover
- [ ] Mandatory static/reflection test confirming zero UPDATE statements passes
- [ ] `reward_rule_version_published` audited on every creation

## 25. Definition of Done
Reward/XP-rule authoring is structurally append-only, giving A.11's Reward Engine and its non-retroactivity guarantee a provably immutable historical foundation to read from.
