# B-08 — Plan-Downgrade Forced-Selection Workflow

> ✅ **UPDATE (resolved via cross-document search of `Feature_C24_Subscription_Billing.md`):** C.24 confirms **no domain event/webhook payload exists or is planned** for this handoff — C.24's Backend AI prompt (§5, item 6) explicitly instructs: *"trigger the same disable mechanism already built in C.21 (call C.21's existing disable endpoint/service internally, do NOT reimplement child-disabling logic here)."* C.24's own Screen Inventory lists *"Trial-Cancellation/Downgrade Child Selector (shared trigger, owned by C.21)"* and *"Deterministic-Fallback Notice (24h, cross-ref C.21)"* — confirming **C.21 owns this endpoint outright**, C.24 only triggers entry into it, and the safe-default fallback has a **concrete 24-hour grace window**, not an immediate/undefined-timing rule as originally read from C.21's own PRD alone. The exact request/response field names are still not published anywhere and remain a proposal below — everything else is now confirmed, not guessed.

## 0. Resolved Open Questions (see full research trail)
1. **Trigger mechanism:** C.24 surfaces a downgrade/cancellation UI moment and hands off into C.21's selector screen (K-08) as a "shared trigger" — C.21 owns the screen and the backend endpoint; C.24 does not call a webhook into C.21.
2. **Safe-default timing:** 24 hours from the downgrade event, per C.24's "Deterministic-Fallback Notice (24h, cross-ref C.21)" screen — the parent has a 24-hour window to make an explicit selection before the safe default (most-recently-active child) is applied automatically. This refines Edge Case #5's looser "before the parent completes the step" language with a concrete duration.
3. **Endpoint path precedent:** C.24 itself uses a `/v1/parent/...` prefix for parent-scoped state/action endpoints (e.g. `GET /v1/parent/subscription`, `POST /v1/parent/subscription/cancel`, `GET /v1/entitlements/check`) as distinct from `/api/v1/billing/...` for billing-transaction endpoints. `POST /v1/parent/children/downgrade-selection` follows this established precedent and is now the working proposal (upgraded from a blind guess).
4. **Still open:** exact request/response field names, and whether the 24h countdown is tracked by C.21 or by C.24 (and merely read by C.21). Confirm this one remaining point with C.24's implementer before Task 03.

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management, triggered by a C.24 (Subscription & Billing) plan-downgrade event rather than a direct parent action on the Child Management screen itself.

## 2. Parent Feature
C.21 Multi-Child Management (cross-cutting with C.24 Subscription & Billing)

## 3. Sub-feature
**B-08 — Plan-Downgrade Forced-Selection Workflow**

## 4. Objective
When a family's plan capacity decreases below their current active-child count, ensure exactly one child remains active per the parent's explicit choice (or a safe, well-defined default), while every other child is disabled — never deleted — with zero undefined intermediate states.

## 5. Business Requirements
- FR-10: trial-cancellation downgrade — parent selects the one child who remains active; all others disabled (not deleted), retaining data, until plan capacity returns.
- Edge Case #5: "A family's plan capacity decreases while more children are active than the new limit allows, before the parent completes the forced-selection step → a defined safe default applies (most-recently-active child remains enabled) rather than an undefined/inconsistent state."
- Acceptance Criteria: "Given a plan downgrade occurs, then the parent selects which one child remains active, and all others are disabled (never deleted)."

## 6. Existing Architecture
**Not** event-driven from C.24 (confirmed absence of any Outbox/webhook contract for this handoff, per C.24 §3.2's architecture diagram, which routes `BILLINGSVC` only to `EVENTBUS[Analytics Event Bus]` — no entitlement/domain event bus exists). Instead, C.24's own Backend AI prompt directs it to call **into** C.21's disable mechanism directly at downgrade time. This workflow is therefore owned and driven entirely within the `identity` context: C.24 (or a shared orchestration point) invokes this service synchronously/directly rather than this service subscribing to an event.

## 7. Existing Code to Reuse
- `IdentityService`/`ChildRepository` — for reading active children and applying disables.
- B-04's `disable_child()` service method — the "disable all but one" action is a batch application of the exact same logic already built and tested there; reuse, do not reimplement session revocation.
- `require_elevated_session` — the selection action itself is a mutating parent action and must be step-up gated per FR-11's blanket rule.

## 8. Files to Create
- `modules/identity/downgrade_selection_service.py` — service handling the 24h-window safe-default computation and the parent-driven selection.
- `modules/identity/models.py` addition: `family.downgrade_selection_deadline: timestamptz | None` — set when C.24 signals a downgrade, cleared once resolved (by parent selection or safe-default application). This is now a confirmed requirement (a 24h deadline must be tracked somewhere), though whether C.21 or C.24 is the system of record for the deadline itself is the one remaining open point (see §0.4).

## 9. Files to Modify
- `modules/subscriptions/service.py` (C.24) — at the point of downgrade/cancellation, call `downgrade_selection_service` directly (synchronous in-process call within the same request/transaction, per C.24's explicit "call C.21's existing disable endpoint/service internally" instruction) rather than emitting an event.
- `modules/identity/api.py` — add `POST /v1/parent/children/downgrade-selection` (see §13).

## 10. Backend Requirements
- **Safe default computation:** identify the most-recently-active child (by whatever "last active" signal already exists — e.g., last `LearningProgress` timestamp or last child-session timestamp; confirm which signal is authoritative before implementing) and keep that one `active`; disable all others.
- **Safe default timing:** applies automatically once the 24-hour window (`family.downgrade_selection_deadline`) elapses without a parent selection — confirmed via C.24's "Deterministic-Fallback Notice (24h, cross-ref C.21)" screen, refining Edge Case #5's original looser language.
- **Parent override:** if the parent completes the forced-selection screen (K-08) within the 24h window, apply their choice instead: chosen child → `active`, all others → `disabled`. After the window elapses, the safe default is final for that downgrade event (no further silent re-computation).
- **Reuse, don't duplicate:** the actual disable mechanics (status flip + session revocation + binding deactivation) must call B-04's existing `disable_child()`/`session_revocation` code, not a parallel implementation.
- **Scheduled enforcement:** a Celery periodic task (following the same pattern as B-06's purge job) sweeps for families whose `downgrade_selection_deadline` has passed without resolution and applies the safe default.

## 11. KMP Requirements
K-08's Trial-Cancellation Forced-Selection Screen reads `downgrade_selection_deadline` (surfaced via an extension to B-01's directory response or a small dedicated field on the family/session context) to render the 24h countdown and know whether it's still within the selection window.

## 12. NextJS Requirements
Not applicable directly, though C.24's admin subscription tooling may need visibility into pending downgrade-selection state — out of scope for this blueprint, flag to C.24's owner.

## 13. API Contract
**Working proposal, upgraded from precedent (not yet a signed-off spec — field names specifically still need sign-off):**
```
POST /v1/parent/children/downgrade-selection
Auth: Bearer + step-up
Request: { "keepActiveChildId": "uuid" }
Response 200: {
  "keptActiveChildId": "uuid",
  "disabledChildIds": ["uuid"],
  "children": [ /* refreshed list, B-01 shape */ ]
}
```
```
GET /v1/parent/children/downgrade-selection
Auth: Bearer
Response 200: {
  "pending": true,
  "selectionDeadline": "timestamp",
  "eligibleChildIds": ["uuid"]
} | { "pending": false }
```
The `GET` variant is new in this revision — K-08 needs a way to know whether a selection is currently pending and the deadline, which the original proposal didn't account for. Path prefix (`/v1/parent/...`) now follows confirmed C.24 precedent rather than an arbitrary guess. Field names remain a proposal pending sign-off.

## 14. Database Requirements
`family.downgrade_selection_deadline: timestamptz | None` (see §8) — migration can proceed now that the 24h-window requirement is confirmed; only the question of whether C.21 or C.24 owns writing this column remains open (see §0.4).

## 15. Validation
Once confirmed: the parent-submitted `keepActiveChildId` must belong to the family and must currently be one of the over-capacity active children.

## 16. Authentication
Bearer parent session, once the endpoint exists.

## 17. Authorization
Step-up required for the parent-driven selection action, per FR-11.

## 18. Error Handling
| Scenario | Response |
|---|---|
| `keepActiveChildId` not found / not owned by family | `404` |
| Step-up missing | `401` |
| Selection submitted after the 24h deadline has already passed and the safe default has applied | `409 SELECTION_WINDOW_EXPIRED` — the safe default stands; parent must use standard Enable (B-05) subject to capacity if they want a different child active |
| Capacity has changed again mid-flow (e.g., another downgrade/upgrade) | `409 CAPACITY_CHANGED`, client should re-fetch via `GET` before retrying |

## 19. Offline First
N/A — mutating/state-critical action, requires connectivity.

## 20. Local Data
N/A backend; K-08 surfaces this as a blocking/informational screen client-side.

## 21. Localization
N/A backend.

## 22. RTL
N/A backend.

## 23. Analytics
None server-side; `trial_cancellation_forced_selection_shown`/`_completed` fire client-side (K-08).

## 24. Performance
Not latency-critical; correctness of the safe-default logic matters far more.

## 25. Security
Step-up required on the parent-selection endpoint once defined; the safe-default auto-application must not be reachable via any parent-supplied input (system-triggered only, off the C.24 event).

## 26. Library Requirements
No new libraries anticipated; reuses existing event/outbox infrastructure.

## 27. Testing
- Unit: safe-default computation picks the correct "most-recently-active" child under a fixture with staggered activity timestamps.
- Unit: safe default disables all *other* children via the reused `disable_child()` path (assert session revocation also fires for each).
- Integration: downgrade event → safe default applied automatically, no undefined state at any point.
- Integration (once endpoint confirmed): parent override after safe default correctly flips the active child.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Deadline Ownership & Sign Off on Field Names (BLOCKING, narrowed scope)**
- **Objective:** Resolve the one remaining open question — whether C.21 or C.24 owns writing `downgrade_selection_deadline` — and get explicit sign-off on §13's field names before coding the endpoints.
- **Why Required:** Everything else about this workflow (trigger mechanism, 24h timing, path prefix, no-event-bus architecture) is now confirmed via C.24's own PRD (§0 above); only this ownership question and exact field naming remain genuinely unresolved, so the blocking scope is much narrower than the original draft of this blueprint.
- **Action:** Confirm with C.24's implementer whether `modules/subscriptions/service.py`'s downgrade/cancellation code path writes the deadline directly (simplest, given C.24 already calls into C.21 synchronously) or whether `downgrade_selection_service.py` computes and writes it upon being invoked.
- **Definition of Done:** Ownership decided and documented here before Task 02.

**Task 02 — Safe-Default Computation Service**
- **Objective:** Implement the automatic most-recently-active-child selection, applied when the 24h deadline elapses.
- **Files to Create:** `modules/identity/downgrade_selection_service.py`.
- **Implementation Details:** Reuse B-04's `disable_child()` for every non-selected child; do not reimplement session revocation. A Celery periodic task (mirroring B-06's purge-job pattern) sweeps `family.downgrade_selection_deadline <= now()` rows lacking a resolution and applies the default.
- **Tests:** Fixture-driven unit test with staggered activity timestamps; time-mocked test (`TestClock`) confirming the sweep only fires post-deadline, not before.
- **Definition of Done:** Safe default is deterministic, correctly time-gated at 24h, and covered by tests before the parent-override endpoint is built on top of it.

**Task 03 — Parent-Selection Endpoints**
- **Objective:** Implement both the `GET` (pending-state check) and `POST` (selection submission) endpoints per §13.
- **Files to Modify:** `modules/identity/api.py`.
- **Definition of Done:** Full endpoint pair per §13's contract, step-up gated on `POST`, fully tested including the post-deadline `409 SELECTION_WINDOW_EXPIRED` case.

## 30. Definition of Done
Safe-default logic is implemented, deterministic, correctly time-gated at 24 hours, and reuses B-04's disable mechanics; both endpoints exist and are tested against the confirmed contract in §13.

## 31. Final Verification Checklist
- [ ] Deadline-ownership question (C.21 vs. C.24) resolved and documented
- [ ] Safe-default logic reuses B-04's `disable_child()` (no duplicated session-revocation logic)
- [ ] 24-hour window correctly enforced (time-mocked test)
- [ ] `GET` pending-state endpoint lets K-08 render the countdown correctly
- [ ] Parent override via `POST`, step-up gated, tested
- [ ] Post-deadline submission correctly rejected with `409 SELECTION_WINDOW_EXPIRED`
