# B-03 — Child Profile Creation API (Plan-Capacity Gated)

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management. Powers "+ Add Child" from the ongoing Child Management surface (as distinct from A.1's first-time onboarding Add Child, though both share the same form and service method).

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**B-03 — Child Profile Creation API (Plan-Capacity Gated)** (`POST /v1/family/children`)

## 4. Objective
Create a new child profile subject to the family's current subscription-tier capacity, rejecting duplicate nicknames and requiring step-up authentication, so a parent can add children beyond the original onboarding flow without ever silently exceeding their plan.

## 5. Business Requirements
- FR-1/FR-8: "+ Add Child" entry point; visible child count gated by subscription tier, blocked inline with upsell path to C.24.
- FR-9: duplicate nicknames within a family rejected inline at save time.
- FR-11: step-up authentication required.
- Acceptance Criteria: "Given a parent attempts to add a child beyond plan capacity, then the action is blocked inline with a path to Subscription & Billing."

## 6. Existing Architecture
Reuses A.1's `IdentityService.create_child_profile()` — this sub-feature extends it with the capacity + step-up + idempotency requirements specific to the ongoing-management context, per `FAST-API-INSTRUCTIONS.md` §5.1 and §9 Scenario 2.

## 7. Existing Code to Reuse
- `IdentityService.create_child_profile(parent_ctx, payload)` — existing A.1 implementation already checks `active_child_count < max_child_limit` via `SubscriptionService.get_entitlement(family_id)` (per §9 Scenario 2 of `FAST-API-INSTRUCTIONS.md`) — **verify this exists before adding a second capacity check; do not duplicate.**
- `SubscriptionService.get_entitlement()` — reuse, do not reimplement capacity logic.
- `OutboxWriter.emit()` — reuse for `ChildProfileCreated` event.
- `EntitlementLimitExceededError` — existing exception class, map to `403 PLAN_CAPACITY_EXCEEDED`.

## 8. Files to Create
None — extends existing A.1 creation path.

## 9. Files to Modify
- `modules/identity/api.py` — attach `require_elevated_session` to `POST /v1/family/children` (the A.1 onboarding call site may be step-up-exempt since it happens during initial registration before a PIN exists; the C.21 management call site must require it — confirm via request context or a dedicated route flag, do not weaken the onboarding path).
- `modules/identity/service.py` — add idempotency-key handling and duplicate-nickname check if not already present.
- `modules/identity/schemas.py` — add `idempotencyKey` to `ChildProfileCreateRequest` if absent.
- `tests/modules/identity/test_children_creation.py` — extend for capacity/duplicate/step-up cases specific to the management context.

## 10. Backend Requirements
- Capacity check: `EntitlementLimitExceededError` → `403 PLAN_CAPACITY_EXCEEDED` with `{current, limit}` detail.
- Duplicate-nickname check: DB `UNIQUE(family_id, nickname)` → `409 DUPLICATE_NICKNAME`.
- Idempotency: client-supplied idempotency key prevents duplicate child creation on retry (e.g., flaky network double-tap).
- New child appended to end of `display_order` (`MAX(display_order) + 1` within the family, or `0` if first child).
- `dob_locked_at` set at creation time (first save always locks DOB per FR-7).

## 11. KMP Requirements
- K-03/K-07 call this through the shared Add/Edit Child form's create path, gated by `ParentGateLauncher.requireParentAuth()`.
- Client renders the Plan-Capacity-Blocked state (K-07) directly from the `403 PLAN_CAPACITY_EXCEEDED` response body's `{current, limit}` detail.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract

**`POST /v1/family/children`**
- **Auth:** Bearer + step-up.
- **Request:**
```json
{
  "nickname": "string",
  "dob": "date",
  "avatarId": "string",
  "languageLevel": "string",
  "interests": ["string"],
  "dailyGoalMinutes": "int",
  "aiPermission": "bool",
  "idempotencyKey": "string"
}
```
- **Response 201:** `ChildProfileResponse`.
- **Error Responses:**
  - `403 PLAN_CAPACITY_EXCEEDED` — `{ "current": 3, "limit": 3 }`.
  - `409 DUPLICATE_NICKNAME`.
  - `401` — missing session/step-up.
  - `422` — validation failure.

## 14. Database Requirements
- `UNIQUE(family_id, nickname)` constraint (introduce here if not already added by B-02).
- `display_order` assignment logic within the same transaction as the insert (row-level lock on the family's max `display_order` to avoid race duplication).

## 15. Validation
Full field validation per A.1's existing `ChildProfileCreateRequest` schema; `idempotencyKey` required and stored to dedupe retried requests.

## 16. Authentication
Bearer parent session.

## 17. Authorization
Step-up required for the C.21 management entry point (distinct from A.1's onboarding entry point, which occurs before a PIN may exist yet — confirm and document this distinction explicitly rather than assuming).

## 18. Error Handling
| Scenario | Response |
|---|---|
| At/over plan capacity | `403 PLAN_CAPACITY_EXCEEDED` with `{current, limit}` |
| Duplicate nickname | `409 DUPLICATE_NICKNAME` |
| Retried request with same idempotency key | `201` with the original created resource (idempotent replay), not a duplicate row |
| Step-up missing | `401` |

## 19. Offline First
Creation requires connectivity; not queued offline (mutating actions blocked offline per §1.14).

## 20. Local Data
N/A backend.

## 21. Localization
N/A — enum/free-text fields only.

## 22. RTL
N/A backend.

## 23. Analytics
None server-side; `child_add_initiated`/`_completed`/`_blocked_plan_capacity` fire client-side.

## 24. Performance
Capacity check and duplicate check both indexed/cheap; target consistent with p95 < 800ms save (§1.8).

## 25. Security
Capacity and duplicate checks are server-side only — never trust a client-side "capacity available" assumption; the server is the sole source of truth (§12.3).

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: capacity-exceeded rejection with correct `{current, limit}` payload.
- Unit: duplicate-nickname rejection.
- Unit: idempotency-key replay returns the same resource, not a duplicate.
- Integration: full creation happy path, including `display_order` correctness for the 2nd/3rd child.
- Integration: step-up-missing rejection at the C.21 management entry point specifically.

## 28. Documentation
Document `403 PLAN_CAPACITY_EXCEEDED` and `409 DUPLICATE_NICKNAME` as named, documented responses in OpenAPI, distinguishing the management-context step-up requirement from the onboarding-context exemption if applicable.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Verify & Extend Capacity-Check Reuse**
- **Objective:** Confirm A.1's existing capacity check is reused unmodified; add idempotency-key support alongside it.
- **Why Required:** Avoids duplicating C.24 entitlement logic — a documented architectural anti-pattern per rule "Use existing architecture."
- **Files to Modify:** `modules/identity/service.py`.
- **Do Not Change:** `SubscriptionService.get_entitlement()` internals — read-only consumer.
- **Definition of Done:** Single, shared capacity-check code path serves both A.1 onboarding and C.21 management creation.

**Task 02 — Idempotency Key Handling**
- **Objective:** Prevent duplicate child rows from retried creation requests.
- **Files to Modify:** `modules/identity/schemas.py`, `modules/identity/service.py`, `modules/identity/repository.py`.
- **Implementation Details:** Store idempotency key on the created row or a dedicated dedupe table scoped to `family_id`; on replay with the same key, return the existing resource instead of creating a new one.
- **Tests:** Duplicate-submission integration test.
- **Definition of Done:** Confirmed no duplicate rows created under simulated retry.

**Task 03 — Display Order Assignment & Step-Up Wiring**
- **Objective:** Correct append-to-end ordering; step-up enforced on the management entry point.
- **Files to Modify:** `modules/identity/api.py`, `modules/identity/repository.py`.
- **Implementation Details:** `SELECT COALESCE(MAX(display_order), -1) + 1 FROM child WHERE family_id = :fid FOR UPDATE` within the creation transaction.
- **Tests:** Race-condition test — two concurrent creations do not collide on `display_order`.
- **Definition of Done:** No `display_order` collisions under concurrent creation.

## 30. Definition of Done
Capacity enforcement reused (not duplicated) and verified; duplicate-nickname and idempotency both covered; step-up required at the management entry point; ordering correct under concurrency.

## 31. Final Verification Checklist
- [ ] Capacity check reuses `SubscriptionService.get_entitlement()` without duplication
- [ ] `403 PLAN_CAPACITY_EXCEEDED` payload includes `{current, limit}`
- [ ] Idempotency-key replay verified
- [ ] `display_order` race condition tested
- [ ] Step-up enforced on management entry point
- [ ] OpenAPI documents all named error codes
