# Blueprint: Subscription Purchase, Trial & Upgrade API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/subscriptions/`. This blueprint delivers the single most safety-critical write endpoint in the Billing Service: `POST /api/v1/billing/subscribe`, which activates trial or paid entitlement only after server-side receipt validation.

## 2. Parent Feature
C.24 — Subscription & Billing.

## 3. Sub-feature
B-02 — Subscription Purchase, Trial & Upgrade API.

## 4. Objective
Accept a store receipt from the client, validate it server-side against the Google Play/App Store verification API before writing any subscription state change, and activate trial or paid entitlement only on a confirmed-valid receipt — never on client-asserted purchase success.

## 5. Business Requirements
Source: PRD §1.7 FR-3, FR-9, FR-10, §3.4 (`POST /api/v1/billing/subscribe`), §5 AI Code-Gen Prompt item 1, Edge Case #10 (mid-trial direct upgrade).
- Parent has already seen trial length/price/renewal date/auto-renew disclosure (client-side, K-03) before this endpoint is called.
- Trial entitlement (Mobile Family level) activates immediately on a verified trial receipt.
- Direct upgrade (non-trial) activates entitlement immediately, keeping all child profiles intact.
- Mid-trial direct upgrade to a higher tier supersedes the scheduled day-7 auto-conversion.
- **Hard rule:** a syntactically-valid but store-unverifiable receipt must be rejected with zero entitlement activation.

## 6. Existing Architecture
Per `FAST-API-INSTRUCTIONS.md` §5.10: `SubscriptionService(BaseService)` (`activate_subscription()`), `SubscriptionRepository` (`get_active_family_subscription()`), `SubscriptionsRouter`. Extends the existing `subscriptions` module. Requires a new `ReceiptValidationClient` integration (Google Play Developer API / App Store Server API) — not yet present in the module inventory; build as a new `infrastructure/store_billing/` client rather than inline HTTP calls in the service (Do Not Guess exact SDK method names — confirm against the chosen store SDK's actual client library during implementation).

## 7. Existing Code to Reuse
- `SubscriptionService(BaseService)` — extend with `subscribe(parent_ctx, request)`.
- `SubscriptionRepository` — extend with `create_or_update_subscription()`.
- `get_current_parent` dependency (`core/deps.py`) → `ParentSessionContext`.
- `ChildRepository` (`modules/identity/`) — read family's current active child count for capacity checks on upgrade.

## 8. Files to Create
- `src/noorheroes/infrastructure/store_billing/receipt_validator.py` — `ReceiptValidationClient` (Play/App Store verification)
- `src/noorheroes/modules/subscriptions/exceptions.py` — `ReceiptValidationError`, `IllegalSubscriptionTransitionError`
- `tests/modules/subscriptions/test_subscription_purchase_trial_upgrade_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/subscriptions/schemas.py` — add `SubscribeRequest`, `SubscribeResponse`
- `src/noorheroes/modules/subscriptions/service.py` — add `subscribe()`
- `src/noorheroes/modules/subscriptions/repository.py` — add `create_or_update_subscription()`
- `src/noorheroes/modules/subscriptions/api.py` — add `POST /api/v1/billing/subscribe` route

## 10. Backend Requirements
- Route: `POST /api/v1/billing/subscribe`, requires `get_current_parent`, rejects child-mode tokens structurally.
- `SubscriptionService.subscribe(parent_ctx, request)`:
  1. Call `ReceiptValidationClient.verify(request.store_receipt)` — **must complete and return a positive result before any DB write**.
  2. On verification failure, raise `ReceiptValidationError` → `422`/`402`, no state change.
  3. On success, determine target state: `is_trial=true` → `state=trial`, `trial_ends_at = now + 7 days`, entitlement = Mobile Family level; `is_trial=false` → `state=active_paid` immediately at the requested `plan`.
  4. If an existing trial subscription is being upgraded mid-trial (Edge Case #10), supersede the scheduled conversion: write `plan=premium_family`, `state=active_paid` immediately, cancel the pending day-7 conversion intent.
  5. Persist via `SubscriptionRepository.create_or_update_subscription()` (idempotent upsert on `family_id`).
  6. Emit `trial_started`/`upgrade_completed` analytics event to the event bus.
- This endpoint never trusts `request.store_receipt` presence alone as proof of purchase — verification result is authoritative.

## 11. KMP Requirements
Consumed by `SubscriptionRepository.subscribe(receipt)` (K-04) — called only after the Play Billing Library's local purchase callback, with the backend response (not the SDK callback) driving UI entitlement state.

## 12. NextJS Requirements
N/A — no admin-initiated subscribe path exists (store-policy compliance, FR-7).

## 13. API Contract
- **HTTP Method:** POST
- **Endpoint:** `/api/v1/billing/subscribe`
- **Auth:** Bearer JWT (parent session only)
- **Request:**
```json
{ "plan": "mobile_family", "store_receipt": "opaque-store-receipt-token", "is_trial": true }
```
- **Response 200:**
```json
{ "subscription_id": "uuid", "state": "trial", "trial_ends_at": "2026-08-24T00:00:00Z" }
```
- **Authentication:** Bearer, parent session only
- **Authorization:** Family-scoped (subscription tied to `parent_ctx.family_id`)
- **Validation:** `plan` must be a valid active plan_code; `store_receipt` required, non-empty; `is_trial` boolean required
- **Error Responses:** `401` invalid session; `403` child-mode token rejected; `422`/`402` receipt validation failure (no entitlement granted); `409` illegal state transition (e.g., subscribing while already `active_paid` on the same plan); `503` store verification API unavailable

## 14. Database Requirements
Writes to `subscription` table (per PRD §4.2): PK/FK `family_id`, `plan`, `state` (CHECK constraint against canonical state enum), `trial_ends_at`, `renewal_date`, `store_receipt_ref`, `updated_at`. This endpoint is the primary writer for `Free→Trial` and `Free/Trial→ActivePaid` (direct upgrade) transitions.

## 15. Validation
- `plan` must exist in the active plan catalog (B-01).
- `store_receipt` non-empty, format-validated before even attempting store verification (fail fast on obviously malformed input).
- `is_trial=true` only permitted when no existing trial/paid subscription is already active for the family (except the mid-trial-upgrade exception, Edge Case #10).

## 16. Authentication
Bearer JWT, parent session only (`get_current_parent`).

## 17. Authorization
Family-scoped — subscription record keyed to `parent_ctx.family_id`; no cross-family write path exists.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Unverifiable/fabricated receipt | `422`/`402`, `ReceiptValidationError`, zero entitlement activation (highest-priority guarantee) |
| Store verification API timeout | `503`, retryable, no partial state write |
| Illegal transition (e.g., re-subscribing to an already-active plan) | `409`, `IllegalSubscriptionTransitionError` |
| Child-mode session token | `403`, structural rejection |
| Malformed request body | `400`, Pydantic validation error |

## 19. Offline First
N/A — this endpoint requires connectivity by definition (store receipt validation); KMP client must block this call offline and surface clear messaging (K-04's responsibility).

## 20. Local Data
N/A (backend).

## 21. Localization
No user-facing strings returned by this endpoint; error codes are machine-readable, localized client-side.

## 22. RTL
N/A (backend).

## 23. Analytics
`trial_started`, `upgrade_completed` fired server-side to the internal Analytics Event Bus on successful activation (mirrors client-side events but serves as the integrity-authoritative record).

## 24. Performance
- Store verification API call is the dominant latency factor (external dependency); apply a bounded timeout with clear `503` on exceed rather than hanging the request.
- Single DB write per call (upsert), no N+1 concerns.

## 25. Security
- **Defining security property of this endpoint:** never activate entitlement without a positive server-side verification result (PRD §12.1, §12.2).
- No raw receipt payload logged (log only verification outcome + receipt reference/hash).
- Structural child-mode-token rejection (mirrors C.20's middleware pattern).

## 26. Library Requirements
Google Play Developer API client / App Store Server API client (new dependency — confirm exact package with the team before adding to `pyproject.toml`, per Do Not Guess).

## 27. Testing
1. Unit test: valid trial receipt → `state=trial`, `trial_ends_at` set correctly, entitlement = Mobile Family.
2. Unit test: valid non-trial receipt → `state=active_paid` immediately, plan matches request.
3. Unit test: fabricated/unverifiable receipt → rejected, `422`/`402`, subscription table unchanged (assert no row written/updated).
4. Unit test: mid-trial direct upgrade to Premium Family supersedes scheduled conversion (Edge Case #10).
5. Unit test: child-mode session token rejected structurally.
6. Unit test: illegal transition (already active_paid, re-subscribe to same plan) → `409`.
7. Integration test: store verification API timeout → `503`, no partial write.
8. Integration test: full flow against store sandbox test-track receipt.

## 28. Documentation
OpenAPI docstring emphasizing the server-side-validation-before-activation contract; module README updated with a sequence note: "Client purchase callback → this endpoint → backend response is entitlement source of truth."

## 29. AI Coding Agent Implementation Steps

**Task 01 — Build Store Receipt Validation Client**
- Task ID: B02-T01
- Objective: Implement `ReceiptValidationClient.verify(receipt)` wrapping the store's own verification API.
- Why This Is Required: This is the platform's highest-priority monetization-integrity guarantee (PRD §5 item 1).
- Existing Architecture to Follow: New `infrastructure/store_billing/` client module, following existing `infrastructure/` client patterns (e.g., R2 client structure).
- Existing Files to Reuse: `infrastructure/` client base patterns if any exist.
- Files to Create: `src/noorheroes/infrastructure/store_billing/receipt_validator.py`.
- Files to Modify: none.
- Implementation Details: Async client calling Google Play Developer API `purchases.subscriptions.get` (or App Store Server API equivalent); returns a typed verification result (valid/invalid + expiry/state metadata).
- Business Rules: PRD §5 item 1 (highest priority).
- Validation: Malformed receipt fails fast without a network call.
- Error Handling: Timeout → typed exception distinct from invalid-receipt result.
- Security: No raw receipt logged; only outcome + reference hash.
- Performance: Bounded timeout (e.g., 5s) with clear failure mode.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05 (with mocked client).
- Documentation: Docstring on client explaining store-of-truth role.
- Dependencies: none.
- Do Not Change: Do not add store API credentials inline — use existing secrets/config management pattern.
- Expected Result: Client returns a reliable verify/reject signal.
- Definition of Done: Fabricated receipt reliably rejected in test with mocked store response.

**Task 02 — Define Subscribe Schemas & Exceptions**
- Task ID: B02-T02
- Objective: `SubscribeRequest`, `SubscribeResponse`, `ReceiptValidationError`, `IllegalSubscriptionTransitionError`.
- Why This Is Required: Type-safe contract and precise error signaling.
- Existing Architecture to Follow: `NoorHeroesBaseModel`, existing exception hierarchy (`core/exceptions.py`).
- Existing Files to Reuse: `common/schemas.py`, `core/exceptions.py` base classes.
- Files to Create: `modules/subscriptions/exceptions.py`.
- Files to Modify: `modules/subscriptions/schemas.py`.
- Implementation Details: Per §13 contract fields exactly.
- Business Rules: FR-3.
- Validation: `plan` enum-checked against active catalog at the schema or service layer.
- Error Handling: N/A (definitions only).
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: Docstrings.
- Dependencies: none.
- Do Not Change: Existing schemas elsewhere.
- Expected Result: Schemas/exceptions importable.
- Definition of Done: Matches §13 exactly.

**Task 03 — Implement SubscriptionService.subscribe()**
- Task ID: B02-T03
- Objective: Core activation logic per §10.
- Why This Is Required: Central business logic for the entire trial/purchase flow.
- Existing Architecture to Follow: `BaseService`, existing `SubscriptionService`.
- Existing Files to Reuse: `SubscriptionRepository`, `ReceiptValidationClient` (Task 01).
- Files to Create: none.
- Files to Modify: `modules/subscriptions/service.py`, `modules/subscriptions/repository.py`.
- Implementation Details: Per §10 steps 1–6 exactly, in order — verification MUST precede any write.
- Business Rules: FR-3, FR-9, FR-10, Edge Case #10.
- Validation: Per §15.
- Error Handling: Per §18.
- Security: Verification-before-write is non-negotiable; write a defensive assertion/test ensuring no code path writes state before a positive verification result.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: Emit `trial_started`/`upgrade_completed` on success.
- Tests: Covered in Task 05.
- Documentation: Docstring citing FR-3/FR-9/FR-10.
- Dependencies: Tasks 01–02.
- Do Not Change: Do not reorder verification after the DB write under any circumstance.
- Expected Result: Correct state transitions per §10.
- Definition of Done: All 8 test cases in Task 05 pass.

**Task 04 — Implement Route**
- Task ID: B02-T04
- Objective: Expose `POST /api/v1/billing/subscribe`.
- Why This Is Required: Public contract delivery.
- Existing Architecture to Follow: Existing router `Depends()` pattern, `get_current_parent`.
- Existing Files to Reuse: `modules/subscriptions/api.py`, `deps.py`.
- Files to Create: none.
- Files to Modify: `api.py`.
- Implementation Details: `@router.post("/api/v1/billing/subscribe", response_model=SubscribeResponse)` with `parent_ctx: Annotated[ParentSessionContext, Depends(get_current_parent)]`.
- Business Rules: FR-3.
- Validation: Pydantic request validation.
- Error Handling: Map service exceptions to HTTP status codes per §18.
- Security: Structural child-mode-token rejection (parent-only dependency).
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A (handled in service).
- Tests: Covered in Task 05.
- Documentation: OpenAPI summary emphasizing server-side validation guarantee.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: Endpoint live.
- Definition of Done: Matches §13 exactly.

**Task 05 — Write Test Suite (Receipt-Validated Activation Priority)**
- Task ID: B02-T05
- Objective: Cover all 8 scenarios in §27, with fabricated-receipt rejection treated as the single highest-priority test.
- Why This Is Required: Non-bypassable CI gate per PRD §10 DevOps.
- Existing Architecture to Follow: pytest, async test client, mocked `ReceiptValidationClient`.
- Existing Files to Reuse: Existing fixture factories for family/parent/subscription.
- Files to Create: `tests/modules/subscriptions/test_subscription_purchase_trial_upgrade_api.py`.
- Files to Modify: none.
- Implementation Details: 8 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact error codes.
- Security: Fabricated-receipt-rejection test is CI-blocking (per PRD §10 DevOps).
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: Assert event emission on success paths.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–04.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 covered and green; fabricated-receipt test marked CI-blocking.

## 30. Definition of Done
`POST /api/v1/billing/subscribe` live, gated by `get_current_parent`, activates entitlement only after positive server-side receipt verification, correctly handles trial/direct-upgrade/mid-trial-upgrade paths, all tests green with the fabricated-receipt-rejection test as a non-bypassable CI gate.

## 31. Final Verification Checklist
- [ ] Zero entitlement activation on unverifiable receipt (verified by test)
- [ ] Verification always precedes any DB write (code-path audited)
- [ ] Mid-trial upgrade supersession behaves per Edge Case #10
- [ ] Child-mode token structurally rejected
- [ ] No raw receipt payload appears in logs
- [ ] Response shape matches §13 exactly
- [ ] Fabricated-receipt test marked as CI-blocking gate
- [ ] OpenAPI docs reflect full contract and validation guarantee
