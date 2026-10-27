# B-13 — Admin Preview & Support Override API

## 1. Feature Context
Lets Support/Content Review staff preview locked episodes for troubleshooting without ever granting the real child any reward or unlock progress. This is a zero-tolerance security boundary — reward leakage via this tool is explicitly called out as a threat in the PRD (§12.1) and requires dedicated integration-test proof of isolation.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
1.13 Admin Preview & Support Override API (ID: **B-13**)

## 4. Objective
Implement `POST /v1/admin/preview-session` inside the existing `admin` module, issuing a token carrying an `is_preview=true` claim that B-04 (reward/unlock skip) and B-07 (media access) already honor by contract, with full audit logging and role gating.

## 5. Business Requirements
- FR-17: admin/support preview access must be fully audited and must never grant the child any reward as a side effect.
- Acceptance Criteria: preview-session playback-complete call results in zero reward and zero unlock-state change for the real child_id.
- §5, backend AI-prompt requirement #5: every downstream service processing a request carrying `is_preview=true` must explicitly skip any state mutation affecting the real child's progress/rewards.

## 6. Existing Architecture
Extends the existing `admin` module's token/session issuance pattern alongside `AdminAuditRepository`. The `is_preview` claim is a JWT claim minted here and verified downstream by B-04 and B-07 — this sub-feature owns issuance and audit; B-04/B-07 own claim-respecting behavior (already specified in their own blueprints).

## 7. Existing Code to Reuse
- `core/security.py::create_access_token`, `JwtClaims` (extend with an `is_preview` claim field)
- `modules/admin/service.py::AdminService.log_action()`
- `core/deps.py::get_current_admin`, `require_admin_scope()`

## 8. Files to Create
- `src/noorheroes/modules/admin/preview_schemas.py` — `PreviewSessionRequest`, `PreviewSessionResponse`
- `src/noorheroes/modules/admin/preview_service.py` — `PreviewSessionService(BaseService)`
- `tests/modules/admin/test_preview_session_service.py`
- `tests/modules/admin/test_preview_session_api.py`
- `tests/integration/test_preview_reward_isolation.py` — dedicated cross-module isolation test

## 9. Files to Modify
- `src/noorheroes/modules/admin/api.py::AdminRouter` — add `POST /v1/admin/preview-session`
- `src/noorheroes/core/security.py::JwtClaims` — add optional `is_preview: bool = False` field

## 10. Backend Requirements
- `PreviewSessionService.issue_preview_session(admin_id, content_id)`: mints a short-lived (e.g., 15-minute, matching B-07's playback TTL) token with `is_preview=true` and `sub` set to a sentinel/admin-scoped identity distinct from any real child ID — the token must never be usable to impersonate or write against a real `child_id`'s records.
- Requires `support` or `content_review` admin scope.
- Every issuance writes an immutable audit log row (`admin_id`, `content_id`, `timestamp`).
- Downstream contract (enforced in B-04/B-07, referenced here for completeness): any request bearing `is_preview=true` skips `RewardService.award_points()` and `UnlockEngine.persist_unlock()` entirely; media manifest issuance (B-07) still applies unlock/entitlement bypass logic specific to preview (since the whole point is previewing locked content) but flags the resulting manifest request as preview end-to-end.

## 11. API Contract

### `POST /v1/admin/preview-session`
- Auth: Admin Bearer with `support` or `content_review` role. Response 200: time-limited preview token flagged `is_preview: true` end-to-end. Audit: every call writes an immutable audit log row.

## 12. Database Requirements
- No new tables beyond the existing `AdminAuditLog` (reused, not extended).

## 13. Validation
- `content_id` must reference an existing episode (withdrawn content may still be previewable for troubleshooting purposes — confirm against product intent; default to allowing preview of withdrawn content since Support needs to investigate exactly such cases).

## 14. Authentication
Admin Bearer via `get_current_admin`.

## 15. Authorization
`require_admin_scope("support")` OR `require_admin_scope("content_review")` — either role may issue a preview session.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Non-support/content_review role attempts issuance | `403 FORBIDDEN` |
| Unknown `content_id` | `404 CONTENT_NOT_FOUND` |
| Preview token expired mid-use | Standard token-expiry `401`, no special handling needed |
| Database failure during audit-log write | `503` — issuance itself should not succeed if the audit write fails (audit-first-or-fail semantics, since an unaudited preview session is a compliance gap) |

## 17. Security
- `is_preview` claim lives in the verified JWT, never in a client-supplied request body field anywhere downstream — this is the load-bearing security property the entire isolation guarantee rests on.
- Preview token subject is never a real `child_id` — architecturally prevents any accidental write against a real child's record even if a downstream check were ever missed.
- Full audit trail is mandatory and blocking (issuance fails if audit-write fails).

## 18. Analytics
Emit via `OutboxWriter`: `admin_preview_mode_used` (internal audit event, distinct from child-facing analytics).

## 19. Performance
Low-volume, low-latency admin operation — no special performance requirements.

## 20. Library Requirements
No new libraries — extends existing JWT infrastructure.

## 21. Testing
- Unit: role-gating rejection, audit-write-blocks-issuance-on-failure semantics.
- **Mandatory cross-module integration test** (`test_preview_reward_isolation.py`): issue a preview session, drive it through B-04's completion endpoint for a real episode, assert zero reward granted and zero `episode_unlock_state` change for the real `child_id` used as a control in the same test (per PRD backend AI-prompt requirement #5 and §13.4 Negative Cases).

## 22. Documentation
Update OpenAPI schema; document the `is_preview` claim contract prominently since B-04 and B-07 both depend on it being present and correctly verified.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Extend `JwtClaims` with `is_preview` Field**
Objective: Add the claim to the existing JWT structure. Follow: existing `core/security.py` conventions. Do Not Change: existing claim fields/verification logic for non-preview tokens. Tests: token round-trip with and without the claim. Definition of Done: existing auth flows unaffected (regression-tested).

**Task 02 — Implement `PreviewSessionService.issue_preview_session()`**
Objective: Mint the preview token with a non-real-child subject, audit-first-or-fail semantics. Dependencies: Task 01, `AdminService.log_action()`. Business Rules: audit write failure blocks issuance. Tests: role-gating, audit-blocks-issuance. Definition of Done: tests pass.

**Task 03 — Add Router Endpoint**
Objective: Wire `POST /v1/admin/preview-session` with `support`/`content_review` scope. Tests: covered by Task 05. Definition of Done: endpoint live, documented.

**Task 04 — Implement Mandatory Cross-Module Isolation Test**
Objective: Full preview-session → completion-call → assert-zero-reward-and-zero-unlock-change test, using a real `child_id` as a control to prove non-interference. Dependencies: B-04, B-07. Definition of Done: test passes and is registered as a required CI check (per PRD DevOps §10, mandatory gate on any PR touching Playback/Reward services).

**Task 05 — Add Remaining Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all green in CI.

**Task 06 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify; document the `is_preview` contract for B-04/B-07 maintainers. Definition of Done: non-breaking diff confirmed.

**Task 07 — Final Code Review**
Objective: Confirm the preview token's subject can never resolve to a real child's writable records under any circumstance; confirm audit-first-or-fail is truly blocking. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] Only `support`/`content_review` roles can issue a preview session
- [ ] Preview token subject is never a real `child_id`
- [ ] Audit log write is blocking — issuance fails if the audit write fails
- [ ] Mandatory cross-module isolation test passes: zero reward, zero unlock-state change for a real child during a preview session
- [ ] `is_preview` claim verified from the JWT only, never trusted from a request body field
- [ ] This test is registered as a required CI gate on any PR touching Playback/Reward services
- [ ] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
Support and content-review staff can preview locked content for troubleshooting through a fully audited, role-gated, provably reward-isolated session — satisfying the PRD's explicit zero-reward-leakage acceptance criteria.
