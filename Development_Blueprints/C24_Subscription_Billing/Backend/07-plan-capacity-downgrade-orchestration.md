# Blueprint: Plan-Capacity Downgrade Orchestration

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/subscriptions/`. Delivers the internal orchestration that detects a plan-capacity-reducing state transition and delegates child-disabling to C.21's existing mechanism — never reimplementing disable logic within the Billing Service.

## 2. Parent Feature
C.24 — Subscription & Billing.

## 3. Sub-feature
B-07 — Plan-Capacity Downgrade Orchestration.

## 4. Objective
When a subscription transitions to a state with lower `child_capacity` than the family's current `active_child_count`, trigger the child-selection requirement and, on selection (or 24-hour deterministic fallback), call C.21's existing `POST /v1/children/{id}/disable` endpoint/service internally for each excess child — with zero duplicate disable logic in this module.

## 5. Business Requirements
Source: PRD §1.7 FR-4, FR-10, §5 AI Code-Gen Prompt item 6, Edge Cases #3, #8.
- Applies to trial-cancellation (many→1) and any downgrade (Premium 8→Mobile 4, etc.) — the "select N of many to keep" generalized case (Edge Case #3).
- Parent is prompted to choose; deterministic most-recently-active fallback applies if no selection within 24 hours.
- Enforcement of "how many children may be active" is always against the *current* plan, never grandfathered from a historical tier (Edge Case #8).
- Downgrade never deletes data — disable only, per C.21's existing reversible-disable semantics.

## 6. Existing Architecture
Per C.21's PRD (§3.4): `POST /v1/children/{id}/disable` sets `status='disabled'`, revokes active sessions/device bindings immediately, retains all data. This blueprint's entire implementation constraint is: **call this existing endpoint/service internally, do not reimplement.** Per `FAST-API-INSTRUCTIONS.md`, cross-module internal calls follow the existing service-to-service invocation pattern (direct service method call within the same process, given NoorHeroes is a modular monolith — not a network call to its own API).

## 7. Existing Code to Reuse
- C.21's `ChildManagementService.disable_child(child_id)` (or equivalent internal method backing `POST /v1/children/{id}/disable` — confirm exact method name against the actual `modules/identity/` or `modules/children/` service before implementation; Do Not Guess if the exact class/method isn't present in the inventory).
- `SubscriptionStateMachine` (B-03) — this orchestration is triggered by the webhook-driven transition (B-03 step 6) and by direct-upgrade/downgrade paths (B-02).
- `ChildRepository.get_active_children_by_family()` (`modules/identity/`).

## 8. Files to Create
- `src/noorheroes/modules/subscriptions/downgrade_orchestrator.py` — `PlanCapacityDowngradeOrchestrator`
- `src/noorheroes/modules/subscriptions/tasks.py` (extend B-04's file) — add `apply_24h_deterministic_fallback` scheduled/delayed task
- `tests/modules/subscriptions/test_plan_capacity_downgrade_orchestration.py`

## 9. Files to Modify
- `src/noorheroes/modules/subscriptions/service.py` — wire orchestrator invocation into state transitions that reduce capacity
- `src/noorheroes/modules/subscriptions/schemas.py` — add `CapacityReductionEvent`, `ChildSelectionRequiredResponse`

## 10. Backend Requirements
- `PlanCapacityDowngradeOrchestrator.handle_capacity_reduction(family_id, new_capacity)`:
  1. Query `ChildRepository.get_active_children_by_family(family_id)`.
  2. If `active_child_count <= new_capacity`, no-op (Edge Case #4 — grace-period recovery scenario, no children disabled).
  3. Otherwise, compute `excess_count = active_child_count - new_capacity`; mark the family as pending child-selection, schedule a 24-hour deterministic-fallback delayed task.
  4. Emit a "child selection required" signal consumed by C.21's KMP-side selector flow (cross-ref K-09) — this may be a notification/flag on the family record or a dedicated event, per architecture team's cross-feature-signal convention.
  5. On parent selection (received via C.21's own selection-submission endpoint, which itself calls back into this orchestrator or directly calls C.21's disable service) OR on 24-hour fallback firing: for each child not selected to remain active, call C.21's `disable_child(child_id)` — this call is the only child-mutating action this module performs.
  6. Never write to the `child` table directly from this module.
- 24-hour fallback logic: deterministic = most-recently-active child(ren) remain active up to `new_capacity`; all others disabled.

## 11. KMP Requirements
Triggers K-09 (Downgrade Child-Selector Trigger), which itself delegates to C.21's `ChildManagementRepository` — this backend orchestration and K-09 mirror each other's "delegate, don't duplicate" constraint on both platforms.

## 12. NextJS Requirements
N/A direct — visible indirectly via N-02's subscription history (capacity-reduction events may appear in state-transition history for support investigation).

## 13. API Contract
No new public HTTP endpoint — this is an internal orchestration invoked by B-02 (direct downgrade) and B-03 (webhook-driven transition). If a status-check endpoint is needed for the KMP selector flow to know "is my family in a pending-selection state," it is `GET /v1/parent/subscription` (B-05)'s `active_child_count` vs `child_capacity` fields, not a new endpoint here.
- **Internal contract:** `PlanCapacityDowngradeOrchestrator.handle_capacity_reduction(family_id: UUID, new_capacity: int) -> None`

## 14. Database Requirements
No new tables owned by this sub-feature. Reads `subscription`/`child` tables; writes only a pending-selection flag/timestamp (likely on the `subscription` record, e.g. `capacity_reduction_pending_since`) to drive the 24-hour fallback timer — confirm exact field placement against the `subscription` table schema (PRD §4.2) before adding a column.

## 15. Validation
- `new_capacity` must be a valid plan's `child_capacity` value.
- Never disables more children than the exact excess count (`active_child_count - new_capacity`).

## 16. Authentication
N/A — internal orchestration, not a directly callable HTTP endpoint.

## 17. Authorization
N/A (internal); the eventual disable call inherits C.21's own step-up-authentication requirement for the *parent-initiated selection* path, but the 24-hour deterministic fallback is a system-initiated action requiring no additional auth (it's not a parent action).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `active_child_count <= new_capacity` | No-op, no children disabled (Edge Case #4) |
| C.21's disable service call fails for one child | Log, retry per standard retry policy, alert if failure persists past a bounded window (data-preservation guarantee must not be silently abandoned) |
| Parent selection arrives after the 24-hour fallback has already fired | Selection is honored if it differs from the fallback outcome and capacity still allows re-enabling (subject to C.21's own re-enable capacity check) |
| Payment recovers before any disable occurs | Pending-selection state cleared, no children disabled (Edge Case #4) |

## 19. Offline First
N/A (backend orchestration).

## 20. Local Data
N/A (backend).

## 21. Localization
N/A — no user-facing content generated by this module; the child-selector UI copy is owned by C.21/K-09.

## 22. RTL
N/A.

## 23. Analytics
`downgrade_initiated`, `downgrade_completed` per §1.19, fired at orchestration start/completion.

## 24. Performance
Low-volume, event-triggered path (only on actual capacity-reducing transitions, not per-request) — no special performance optimization required beyond standard async DB access.

## 25. Security
- **Defining constraint:** this module must never implement its own child-disable logic — a structural/test-enforced guarantee that all disabling flows through C.21's existing mechanism (single source of truth for the disable/data-retention guarantee).
- 24-hour fallback is system-initiated, not exploitable as a parent-bypass path around C.21's step-up auth (since it results in the same disable action C.21 itself would take).

## 26. Library Requirements
No new dependencies; uses Celery (existing) for the 24-hour delayed fallback task.

## 27. Testing
1. Unit test: capacity reduction with `active_child_count > new_capacity` triggers pending-selection state (PRD §5 item 6).
2. Unit test: this service delegates to C.21's `disable_child()` — mock/spy assertion confirming no local child-mutation logic exists (PRD §5 item 6 explicit test requirement).
3. Unit test: `active_child_count <= new_capacity` → no-op, no disable calls made.
4. Unit test: 24-hour fallback selects most-recently-active children deterministically up to `new_capacity`.
5. Unit test: parent selection before 24-hour window cancels the scheduled fallback task.
6. Unit test: payment-recovery-before-disable scenario (Edge Case #4) results in zero disables.
7. Integration test: full downgrade → pending-selection → fallback-or-selection → C.21 disable call, end to end.

## 28. Documentation
Module docstring explicitly stating the "delegate, never duplicate" constraint, cross-referencing C.21's disable contract; architecture note added to `docs/architecture/` cross-referenced from C.21's own blueprint.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Capacity-Reduction Detection & Pending-Selection State**
- Task ID: B07-T01
- Objective: Detect capacity-reducing transitions and mark pending-selection state.
- Why This Is Required: Entry point for the entire orchestration.
- Existing Architecture to Follow: `SubscriptionStateMachine` transition hook, `ChildRepository`.
- Existing Files to Reuse: `SubscriptionRepository`, `ChildRepository`.
- Files to Create: `modules/subscriptions/downgrade_orchestrator.py`.
- Files to Modify: `service.py` (wire into B-02/B-03 transition points).
- Implementation Details: Per §10 steps 1–3.
- Business Rules: FR-4, Edge Case #8 (current-plan-only enforcement).
- Validation: Per §15.
- Error Handling: N/A at this step.
- Security: N/A.
- Performance: N/A.
- Localization/RTL: N/A.
- Analytics: `downgrade_initiated`.
- Tests: Covered in Task 04.
- Documentation: Docstring.
- Dependencies: B-02, B-03.
- Do Not Change: Do not write to the `child` table here.
- Expected Result: Pending-selection state correctly set/cleared.
- Definition of Done: Edge Cases #3, #4, #8 all pass.

**Task 02 — Implement 24-Hour Deterministic Fallback Task**
- Task ID: B07-T02
- Objective: Scheduled Celery task selecting most-recently-active children if no parent selection arrives.
- Why This Is Required: PRD's deterministic-fallback guarantee (FR-4).
- Existing Architecture to Follow: Celery delayed-task pattern (extends B-04's task file).
- Existing Files to Reuse: `tasks.py` (B-04).
- Files to Create: none (extend existing file).
- Files to Modify: `tasks.py`.
- Implementation Details: Delayed task scheduled at pending-selection time, cancellable on early parent selection.
- Business Rules: FR-4 deterministic fallback.
- Validation: N/A.
- Error Handling: Per §18.
- Security: N/A.
- Performance: N/A.
- Localization/RTL: N/A.
- Analytics: N/A (covered by downstream disable calls' own events).
- Tests: Covered in Task 04.
- Documentation: Task docstring.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Deterministic fallback fires correctly at 24h if unselected.
- Definition of Done: Fallback selection logic test passes.

**Task 03 — Implement C.21 Delegation Call**
- Task ID: B07-T03
- Objective: Call C.21's existing `disable_child()` for each excess child.
- Why This Is Required: PRD §5 item 6's explicit non-duplication requirement.
- Existing Architecture to Follow: Direct in-process service call (modular monolith pattern), not a network call.
- Existing Files to Reuse: C.21's `ChildManagementService.disable_child()` (confirm exact name/location — Do Not Guess).
- Files to Create: none.
- Files to Modify: `downgrade_orchestrator.py`.
- Implementation Details: Loop over excess children, call C.21's service method, handle per-child failure per §18.
- Business Rules: FR-10 (never delete, disable only).
- Validation: N/A.
- Error Handling: Per §18.
- Security: This delegation IS the security/data-integrity guarantee.
- Performance: N/A.
- Localization/RTL: N/A.
- Analytics: `downgrade_completed` on full completion.
- Tests: Covered in Task 04 (mock/spy delegation assertion is the priority test).
- Documentation: Docstring citing C.21 dependency explicitly.
- Dependencies: Tasks 01–02, C.21's disable service (external dependency, confirm availability before this task can complete).
- Do Not Change: Do not implement any child-status-mutating logic locally — call C.21 only.
- Expected Result: Correct children disabled via C.21, data retained.
- Definition of Done: Delegation test (Task 04, test #2) passes.

**Task 04 — Write Test Suite**
- Task ID: B07-T04
- Objective: Cover all 7 scenarios in §27, with the delegation-not-duplication test as the priority case.
- Why This Is Required: PRD §5 item 6 explicit test requirement.
- Existing Architecture to Follow: pytest, mocked C.21 service.
- Existing Files to Reuse: Fixture factories for family/child/subscription state.
- Files to Create: `tests/modules/subscriptions/test_plan_capacity_downgrade_orchestration.py`.
- Files to Modify: none.
- Implementation Details: 7 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert per-child failure resilience.
- Security: Delegation-not-duplication test is priority/CI-relevant.
- Performance: N/A.
- Localization/RTL: N/A.
- Analytics: Assert `downgrade_initiated`/`downgrade_completed` emission.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 covered and green.

## 30. Definition of Done
Capacity-reducing transitions correctly detected, parent-selection/24-hour-fallback flow operational, all disabling delegated exclusively to C.21's existing service with zero local disable logic, data-preservation guarantee verified, all tests green.

## 31. Final Verification Checklist
- [ ] Delegation-to-C.21 verified (no local child-mutation code path exists)
- [ ] `active_child_count <= new_capacity` no-op case verified
- [ ] 24-hour deterministic fallback selects most-recently-active correctly
- [ ] Payment-recovery-before-disable results in zero disables (Edge Case #4)
- [ ] Current-plan-only enforcement, no historical-tier grandfathering (Edge Case #8)
- [ ] Per-child delegation failure handled without silent data loss
- [ ] Cross-referenced in C.21's own blueprint documentation
