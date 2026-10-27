# B-10 — Admin DOB Correction Support API

> ✅ **UPDATE (resolved via cross-document search of `Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md`):** `support` is confirmed as a real, precedented bare role name (E.28 FR-4 lists "Support Agent" as one of nine defined portal roles); **no `resource:action` scope convention (e.g. `support:write`) exists anywhere in the project's docs** — the actual documented convention is bare role-name gating. This blueprint now uses `require_admin_scope("support")` directly. Path `/v1/admin/...` is confirmed via `FAST-API-INSTRUCTIONS.md`'s documented `AdminRouter`. **Still genuinely open:** whether a server-side identity-verification/elevation mechanism (mirroring the NextJS `useElevatedSession`/OTP pattern) already exists in the backend was not found in any searched document — this must be confirmed against the live codebase, not guessed, before Task 03.

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management's Admin Requirements (§8): the **only** legitimate, fully-audited bypass of the DOB-immutability guarantee enforced at the database layer in B-02.

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**B-10 — Admin DOB Correction Support API** (`PATCH /v1/admin/children/{id}/dob-correction`)

## 4. Objective
Allow Support staff to correct a genuinely wrong, locked DOB — the one scenario B-02 deliberately cannot handle — while requiring a documented reason, identity verification, and producing a high-sensitivity audit record for every use.

## 5. Business Requirements
- §8: "DOB Change Support Tool: The one legitimate path for post-lock DOB correction — requires documented reason and identity verification, fully audited."
- §12.5: "The DOB Change Support Tool is the only legitimate immutability bypass, heavily audited."
- §10 DevOps: "Alert on any DOB update post-lock via a non-Support-tool path (P0)."

## 6. Existing Architecture
`admin` bounded context; must call a dedicated `IdentityService` method that resets `dob_locked_at`, bypassing the DB trigger built in B-02 **only** through an explicitly privileged code path (e.g., a `SET LOCAL` session flag the trigger checks, or a dedicated admin-only stored procedure) — not by disabling the trigger globally.

## 7. Existing Code to Reuse
- `get_current_admin`, `require_admin_scope("support")` — bare role name, confirmed convention (see update note above).
- `AdminAuditRepository` / `audit_logs` writer — reuse the exact same audit-log mechanism as B-09 reads from and B-06 writes to.
- The DOB-immutability trigger from B-02, Task 01 — this task must extend it with the sanctioned bypass, not bypass it silently outside the DB layer.

## 8. Files to Create
- `modules/identity/dob_correction_service.py` — isolated service for this single, highly sensitive operation.

## 9. Files to Modify
- `modules/identity/models.py` / trigger migration (B-02, Task 01) — extend the trigger to permit the update only when a specific sanctioned marker is set within the same transaction (e.g., a Postgres session variable set exclusively by this service method, never by the general application code path).
- `modules/identity/api.py` — add the route (module placement follows B-09's resolved convention: `identity`, matching the table's own bounded context).
- `tests/modules/identity/test_dob_correction_support.py` — new test module.

## 10. Backend Requirements
- Request must include: `reason: str` (mandatory, non-empty), `newDob: date`, and an identity-verification confirmation flag/token per whatever identity-verification mechanism Support already uses for other high-risk actions (confirm against existing patterns, e.g. NextJS's `useElevatedSession`/OTP flow — the backend counterpart of that flow, not a new one).
- On success: reset `dob_locked_at` and set the new `dob` via the sanctioned bypass path, then immediately re-lock (`dob_locked_at = now()` again) — this is a one-time correction, not a re-opening of the field permanently.
- Write a high-sensitivity `audit_logs` entry containing: `reason`, `admin_id` (the agent), `old_dob`, `new_dob`, `timestamp`.
- Trigger a P0 monitoring alert path is explicitly for detecting *unsanctioned* DOB changes — this sanctioned path must be clearly distinguishable in logs/metrics from an alert-worthy event.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
N-02 (DOB Change Support Tool) is the sole consumer.

## 13. API Contract

**`PATCH /v1/admin/children/{id}/dob-correction`**
- **Auth:** Bearer (admin) + `support` role (via `require_admin_scope("support")`).
- **Request:**
```json
{
  "newDob": "date",
  "reason": "string",
  "identityVerificationConfirmed": true
}
```
- **Response 200:** updated `ChildProfileResponse` reflecting the new (re-locked) DOB.
- **Error Responses:**
  - `422` — `reason` empty, `identityVerificationConfirmed` false/missing.
  - `404` — child not found.
  - `403` — missing `support` role.
  - `401` — missing/invalid admin session.

## 14. Database Requirements
Extend the B-02 trigger with a sanctioned-bypass condition (e.g., a transaction-local session variable `noorheroes.dob_correction_authorized = true`, set only inside this service method's transaction and never elsewhere in the codebase).

## 15. Validation
`reason` non-empty and reasonably substantive (minimum length, not just whitespace); `identityVerificationConfirmed` must be a literal `true`.

## 16. Authentication
Bearer admin session.

## 17. Authorization
`support` bare role, confirmed as a real precedented role (E.28 FR-4) — narrower than a hypothetical general `admin:write`, matching §8's "narrow, audited Update-only behind `support`" description using the actual documented gating convention rather than an invented scope string.

## 18. Error Handling
| Scenario | Response |
|---|---|
| Missing/empty reason | `422` |
| Identity verification not confirmed | `422` |
| Child not found | `404` |
| Missing `support` role | `403` |
| Trigger rejects bypass (misconfigured sanction flag) | `500`, logged and alerted — this should never happen if Task 02 is implemented correctly |

## 19. Offline First
Not applicable — Admin Portal action.

## 20. Local Data
Not applicable.

## 21. Localization
Not applicable to this backend endpoint (Admin Portal localizes the surrounding UI, not this payload).

## 22. RTL
Not applicable backend.

## 23. Analytics
Not specified; the audit-log entry itself is the record of use, not a product-analytics event.

## 24. Performance
Single-row update, not latency-sensitive; correctness and auditability dominate.

## 25. Security
- This is the platform's single sanctioned bypass of a hard database-layer invariant — treat every implementation detail as security-critical.
- The sanction marker must be settable **only** from within `dob_correction_service.py`'s transaction — grep the codebase after implementation to confirm no other code path sets it.
- Every use is logged with enough detail (`reason`, `admin_id`, `old_dob`, `new_dob`, `timestamp`) to support a compliance audit without needing to correlate against other tables.

## 26. Library Requirements
No new libraries.

## 27. Testing
- **Highest-priority test:** attempt a DOB update through the normal `IdentityService.update_child_profile()` path (B-02) on a locked child and confirm it is still rejected — i.e., confirm this new sanctioned path did not accidentally weaken B-02's general guarantee.
- Unit: sanctioned-bypass path successfully updates DOB and re-locks it.
- Unit: `reason`/`identityVerificationConfirmed` validation.
- Integration: full correction flow produces exactly one `audit_logs` row with all required fields.
- Integration: `403` for an admin lacking the `support` role.
- Integration (monitoring): confirm the P0-alert path (built in B-02) does not fire for this sanctioned use, but would still fire for any other unsanctioned attempt.

## 28. Documentation
Document this endpoint prominently as "the only legitimate DOB-immutability bypass" in OpenAPI, cross-referencing B-02's trigger and the monitoring alert it's exempt from.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Server-Side Identity-Verification Mechanism (BLOCKING, narrowed scope)**
- **Objective:** Path and role name are now resolved (`/v1/admin/children/{id}/dob-correction`, `support` role — see the update note at the top of this file). The one remaining open item is whether an existing server-side elevation/OTP-verification mechanism (backend counterpart of the frontend's `useElevatedSession`) already exists for admin actions.
- **Action:** Search the live codebase for an existing admin-elevation dependency (something like `require_elevated_admin_session`, analogous to C.19's `require_elevated_session` for parents) before building a new one; if genuinely absent, this task's scope expands to include building that primitive, which should then be proposed for reuse by future high-risk admin actions rather than kept private to this one endpoint.
- **Definition of Done:** Verification mechanism confirmed-existing or explicitly built as a new, reusable primitive — documented here before Task 03.

**Task 02 — Extend DOB Trigger with Sanctioned Bypass**
- **Objective:** Allow this one code path, and only this one, to update a locked DOB.
- **Files to Modify:** the trigger migration from B-02, Task 01.
- **Implementation Details:** `IF current_setting('noorheroes.dob_correction_authorized', true) = 'true' THEN <allow> ELSE <existing rejection> END IF;` inside the trigger function; `dob_correction_service.py` sets this via `SET LOCAL` at the start of its transaction (scoped to that transaction only, auto-reset after commit/rollback).
- **Security:** Grep-verify no other code sets this session variable.
- **Tests:** The highest-priority regression test confirming B-02's general path still rejects.
- **Definition of Done:** Bypass works only through this one service method; verified via both positive and negative tests.

**Task 03 — Service, Audit Logging & Router**
- **Objective:** Implement `dob_correction_service.py`, wire the audit-log write, and expose the route behind the `support` role.
- **Files to Create/Modify:** per above.
- **Definition of Done:** Full end-to-end test producing exactly one correctly-populated audit-log row per correction.

## 30. Definition of Done
The sanctioned bypass is narrowly scoped to this one service method, fully audited, correctly re-locks after correction, and does not weaken B-02's general-path guarantee.

## 31. Final Verification Checklist
- [ ] Server-side identity-verification mechanism confirmed-existing or newly built as a reusable primitive
- [ ] Sanctioned bypass reachable only from `dob_correction_service.py` (grep-verified)
- [ ] B-02's normal-path rejection still holds (regression tested)
- [ ] DOB re-locked immediately after correction (not left permanently open)
- [ ] Exactly one audit-log row per correction, with all required fields
- [ ] `support` role enforced via `require_admin_scope("support")`
- [ ] Monitoring correctly distinguishes sanctioned use from unsanctioned alert-worthy attempts
