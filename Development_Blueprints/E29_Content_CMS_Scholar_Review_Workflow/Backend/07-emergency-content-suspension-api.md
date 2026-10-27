# B-07 — Emergency Content Suspension API

## 1. Feature Context
The safety-role-only kill switch: immediately pulls live content from serving eligibility and purges CDN caches, with zero exception on audit logging. Distinct from B-01's routine archive path — this is the emergency path for content already live and flagged as a problem.

## 2. Parent Feature
E.29 — Content CMS & Scholar Review Workflow

## 3. Sub-feature
1.7 Emergency Content Suspension API (ID: **B-07**)

## 4. Objective
Implement `POST /v1/admin/content/{id}/suspend`, restricted to safety roles, immediately excluding the content from catalog/search/recommendation eligibility and purging CDN caches, with a mandatory audit write.

## 5. Business Requirements
- FR-9: emergency suspension available to safety roles only, always audited.
- Edge Case 6: an active in-progress child session may complete its current natural unit; the content is excluded from all future search/browse/recommendation surfacing immediately, with CDN caches purged.

## 6. Existing Architecture
`modules/content_cms/suspend/` sub-package, reusing B-01's `content_item.status` transition and B-02's CDN-purge mechanism.

## 7. Existing Code to Reuse
- `modules/content_cms/repository.py::ContentItemRepository` (B-01)
- `modules/content_cms/media/service.py::MediaProcessingService` (B-02, CDN purge)
- `modules/admin/audit/service.py::AuditLogService.log_action()` (E.28)

## 8. Files to Create
- `src/noorheroes/modules/content_cms/suspend/schemas.py` — `SuspendRequest`
- `src/noorheroes/modules/content_cms/suspend/service.py` — `SuspensionService(BaseService)`
- `src/noorheroes/modules/content_cms/suspend/api.py` — suspend route addition
- `tests/modules/content_cms/suspend/test_suspension_service.py`

## 9. Files to Modify
- `src/noorheroes/modules/content_cms/api.py` (B-01) — add `POST /v1/admin/content/{id}/suspend`
- Consumer-feature catalog queries (e.g., A.3's B-01 Story Catalog, A.5, A.6, B.18) must already exclude `status != 'published'` items — this sub-feature confirms/documents that contract rather than re-implementing it per feature.

## 10. Backend Requirements
- `SuspensionService.suspend(content_id, actor_id, reason)`: requires non-empty `reason`; sets `content_item.status='suspended'`; calls `MediaProcessingService`'s CDN-purge helper for every media asset referenced by the item's current published version; writes an audit entry unconditionally — the write is not best-effort, the suspend transaction itself fails if the audit write fails (mirroring A.3's B-13 preview-session audit-first-or-fail pattern).
- Suspension does not retroactively affect an already-in-progress child session (per Edge Case 6) — this is a property of the consumer-facing catalog/manifest APIs' own live re-validation (already established per-feature, e.g., A.3's B-07), not something this endpoint needs to enforce directly.

## 11. API Contract

### `POST /v1/admin/content/{id}/suspend`
- Auth: `child_safety_reviewer` or `super_admin` role only. Request: `{ "reason": "..." }`. Response 200: `{ status: "suspended" }`. Errors: `422 REASON_REQUIRED`, `403 FORBIDDEN`.

## 12. Database Requirements
No new tables — writes `content_item.status`.

## 13. Validation
`reason` required, non-empty.

## 14. Authentication
Admin Bearer via `get_current_admin`.

## 15. Authorization
`require_admin_scope("child_safety_reviewer")` OR `require_admin_scope("super_admin")` — strictly safety roles, not `content_editor`/`publisher`/`scholar_reviewer`.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Missing/empty reason | `422 REASON_REQUIRED` |
| Non-safety-role attempts suspension | `403 FORBIDDEN` |
| Audit write fails | Suspend transaction itself fails and rolls back — never a suspended-but-unaudited state |
| Database/CDN-purge failure | `503`, logged; content status change and CDN purge should be attempted transactionally where feasible, with a retry-safe purge step |

## 17. Security
Audit-first-or-fail semantics make an unaudited emergency suspension structurally impossible — this is the platform's safety-critical kill switch and must never have a silent/untracked exercise.

## 18. Analytics
`content_suspended` (with `actor`, `reason`) audited via `AuditLogService`, always.

## 19. Performance
Suspension is a rare, low-volume, safety-critical action — no special performance requirements beyond correctness.

## 20. Library Requirements
No new libraries.

## 21. Testing
- Unit: reason-required validation, safety-role-only rejection.
- Integration: suspend → confirm content excluded from a mocked consumer-catalog query → confirm CDN purge called → confirm audit entry present; audit-write-failure-blocks-suspend test.

## 22. Documentation
Update OpenAPI schema; document the audit-first-or-fail invariant.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Implement `SuspensionService.suspend()`**
Objective: Reason-required, safety-role-scoped suspension with audit-first-or-fail semantics. Dependencies: B-01, B-02, E.28 B-05. Tests: audit-write-failure-blocks-suspend test. Definition of Done: test passes.

**Task 02 — Wire CDN Purge on Suspend**
Objective: Call B-02's purge helper for every media asset on the suspended item's published version. Dependencies: B-02. Tests: purge-called-for-all-assets test. Definition of Done: test passes.

**Task 03 — Add Router Endpoint with Safety-Role-Only Scope**
Objective: Wire the suspend route. Tests: role-rejection test. Definition of Done: test passes, endpoint documented.

**Task 04 — Add Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all green in CI.

**Task 05 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify. Definition of Done: non-breaking diff confirmed.

**Task 06 — Final Code Review**
Objective: Confirm zero code path can suspend content without a successful audit write. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] Only `child_safety_reviewer`/`super_admin` roles can suspend
- [ ] Reason required, non-empty
- [ ] Suspend transaction fails entirely if the audit write fails — never a silent/unaudited suspension
- [ ] CDN caches purged for all affected media on suspend
- [ ] `content_suspended` event includes actor and reason

## 25. Definition of Done
Safety roles can immediately and always-audibly pull live content from circulation — the platform's emergency kill switch, structurally incapable of an unaudited exercise.
