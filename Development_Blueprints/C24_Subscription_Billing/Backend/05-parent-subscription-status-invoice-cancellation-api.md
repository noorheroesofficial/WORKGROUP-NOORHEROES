# Blueprint: Parent Subscription Status, Invoice History & Cancellation API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/subscriptions/`. Delivers the parent-facing read/action surface: `GET /v1/parent/subscription`, `POST /v1/parent/subscription/cancel`, plus invoice detail retrieval and restore-purchase, backing the Subscription landing, Invoice History, and Cancel Flow screens.

## 2. Parent Feature
C.24 — Subscription & Billing.

## 3. Sub-feature
B-05 — Parent Subscription Status, Invoice History & Cancellation API.

## 4. Objective
Give the parent app a single read model of current entitlement/billing state, a cancel action that preserves access until period end, invoice history/detail, and a restore-purchase path — all reading from and updating only the state established by B-02/B-03/B-04, never independently determining entitlement.

## 5. Business Requirements
Source: PRD §1.7 FR-4, §3.4 (`GET /v1/parent/subscription`, `POST /v1/parent/subscription/cancel`), §1.18 Screens 1, 7, 8, 10, 11, 18, Edge Cases #1, #5.
- Cancellation: access continues until `access_until` (period end), then reverts to Free — never immediate revocation.
- Trial cancellation within the first hour still honors the full 7-day trial entitlement (Edge Case #1) — canceling means "don't auto-convert," not "revoke now."
- Restore-purchase re-validates an existing store receipt server-side and re-establishes entitlement without a new purchase (Edge Case #5).
- Zero-invoice-history is a valid, expected empty state for new subscribers.

## 6. Existing Architecture
Per `FAST-API-INSTRUCTIONS.md` §5.10: extends `subscriptions` module, `SubscriptionService`, `SubscriptionRepository`. Reuses B-02's `ReceiptValidationClient` for the restore-purchase path (same verification mechanism, different trigger).

## 7. Existing Code to Reuse
- `SubscriptionRepository.get_active_family_subscription()`.
- `SubscriptionStateMachine` (B-03) — cancellation and restore both transition through this, not a bespoke write.
- `ReceiptValidationClient` (B-02) — reused for restore-purchase server-side re-validation.
- `get_current_parent` dependency.
- `InvoiceRepository` (new, or extend `SubscriptionRepository` — confirm whether `invoice` warrants its own repository per existing module conventions before deciding).

## 8. Files to Create
- `tests/modules/subscriptions/test_parent_subscription_status_invoice_cancellation_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/subscriptions/schemas.py` — add `ParentSubscriptionResponse`, `CancelResponse`, `InvoiceResponse`, `RestorePurchaseResponse`
- `src/noorheroes/modules/subscriptions/service.py` — add `get_parent_subscription()`, `cancel_subscription()`, `get_invoice_detail()`, `restore_purchase()`
- `src/noorheroes/modules/subscriptions/repository.py` — add `list_invoices()`, `get_invoice_by_id()`
- `src/noorheroes/modules/subscriptions/api.py` — add the four routes below

## 10. Backend Requirements
- `GET /v1/parent/subscription`: resolve family's active subscription, compose plan/state/renewal_date/child_capacity/active_child_count/invoices summary.
- `POST /v1/parent/subscription/cancel`: transition `ActivePaid→Canceled` (or `Trial→Free`-pending, i.e. "don't auto-convert" flag) via `SubscriptionStateMachine`; set `access_until` to the current period's end; never immediately revoke.
- `GET /v1/parent/subscription/invoices/{invoice_id}`: return invoice detail, family-ownership-scoped.
- `POST /v1/parent/subscription/restore`: re-validate the family's existing store receipt via `ReceiptValidationClient.verify()`; re-establish entitlement state from the verified result without creating a new purchase record.
- All routes require `get_current_parent`; structurally reject child-mode tokens.

## 11. KMP Requirements
Consumed by `SubscriptionRepository.cancel()/getInvoices()` (K-06), `SubscriptionViewModel` (K-01) for landing-screen state, and the Restore Purchase component (K-06).

## 12. NextJS Requirements
N/A direct — support tooling (N-02) reads subscription state via a separate admin-scoped lookup endpoint (see E.33), not this parent-facing API.

## 13. API Contract
**`GET /v1/parent/subscription`**
- Response 200: `{ "plan": "mobile_family", "state": "active_paid", "renewal_date": "...", "child_capacity": 4, "active_child_count": 3, "invoices": [{ "invoice_id": "...", "amount": 3.00, "currency": "USD", "issued_at": "..." }] }`

**`POST /v1/parent/subscription/cancel`**
- Response 200: `{ "canceled": true, "access_until": "2026-09-15T00:00:00Z" }`

**`GET /v1/parent/subscription/invoices/{invoice_id}`**
- Response 200: `{ "invoice_id": "...", "amount": 3.00, "currency": "USD", "status": "paid", "issued_at": "..." }`

**`POST /v1/parent/subscription/restore`**
- Request: `{ "store_receipt": "..." }`
- Response 200: `{ "restored": true, "state": "active_paid" }` or `{ "restored": false, "reason": "no_active_purchase_found" }`

- **Authentication:** Bearer, parent session only (all four routes)
- **Authorization:** Family-scoped
- **Validation:** `invoice_id` must belong to caller's family; restore `store_receipt` required
- **Error Responses:** `401`/`403` per standard auth gate; `404` invoice not found or not owned; `409` cancel attempted on a non-cancelable state (e.g., already `free`)

## 14. Database Requirements
Reads `subscription`, `invoice` tables (PRD §4.2). `invoice` is append-only, no writes from this sub-feature beyond what B-02/B-03 already produce. Cancellation writes only to `subscription.state`/`canceled_at`, never to `invoice`.

## 15. Validation
- `invoice_id` ownership check against `parent_ctx.family_id`.
- Cancel only legal from `active_paid`/`trial` states (state-machine-enforced).
- Restore `store_receipt` required and non-empty.

## 16. Authentication
Bearer JWT, parent session only, all four routes.

## 17. Authorization
Family-scoped on every read/write; invoice detail explicitly checked for family ownership (not just existence).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Cancel on non-cancelable state | `409`, `IllegalSubscriptionTransitionError` |
| Invoice not found / not owned | `404` (uniform response regardless of which, to avoid leaking existence) |
| Restore with no matching active purchase | `200 { "restored": false, "reason": "no_active_purchase_found" }` — not an error, a valid outcome |
| Restore receipt fails verification | `422`, no entitlement change |
| Child-mode session token | `403` structural rejection |

## 19. Offline First
N/A server-side; client renders last-cached response offline (K-01/K-06), these actions require connectivity.

## 20. Local Data
N/A (backend).

## 21. Localization
No hardcoded display strings; `reason` codes are machine-readable, localized client-side.

## 22. RTL
N/A (backend).

## 23. Analytics
`invoice_viewed`, `cancellation_initiated`→`_completed`, `restore_purchase_initiated`→`_completed` fired server-side on successful state changes (mirrors client events, integrity-authoritative record).

## 24. Performance
Single-row lookups (`family_id`-keyed), no N+1 concerns; invoice list paginated if it grows large (not expected to be large per family, but defensively bounded).

## 25. Security
- Cancellation never immediately revokes access (trust commitment, not just a UX nicety — PRD §1.9 Acceptance Criteria).
- Restore-purchase reuses the same server-side verification rigor as B-02 — never trusts a client-asserted "I own this" claim without receipt re-verification.
- Family-ownership check on every invoice lookup.

## 26. Library Requirements
No new dependencies beyond B-02's `ReceiptValidationClient`, reused here.

## 27. Testing
1. Unit test: `GET /v1/parent/subscription` returns correct composed state.
2. Unit test: cancel from `active_paid` → `Canceled`, `access_until` = current period end, entitlement NOT immediately revoked.
3. Unit test: cancel a trial within the first hour → trial entitlement remains active for the full 7 days (Edge Case #1).
4. Unit test: cancel on an already-`free`/non-cancelable state → `409`.
5. Unit test: invoice detail — cross-family access rejected with `404`.
6. Unit test: restore-purchase with a valid existing receipt → entitlement re-established, no new purchase record created.
7. Unit test: restore-purchase with no matching active purchase → `200 restored:false`, not an error.
8. Integration test: full cancel → access-until-expiry → automatic reversion to Free (cross-ref B-03's webhook-driven `Canceled→Free` transition).

## 28. Documentation
OpenAPI docstrings for all four routes; module docs note that cancellation and restore both route through `SubscriptionStateMachine`, consistent with B-03's integrity guarantee.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Schemas**
- Task ID: B05-T01
- Objective: `ParentSubscriptionResponse`, `CancelResponse`, `InvoiceResponse`, `RestorePurchaseRequest/Response`.
- Why This Is Required: Type-safe contracts for all four endpoints.
- Existing Architecture to Follow: `NoorHeroesBaseModel`.
- Existing Files to Reuse: `common/schemas.py`.
- Files to Create: none.
- Files to Modify: `modules/subscriptions/schemas.py`.
- Implementation Details: Per §13 exactly.
- Business Rules: FR-4.
- Validation: Field types match §13.
- Error Handling/Security/Performance/Localization/RTL/Analytics: N/A (definitions only).
- Tests: Covered in Task 04.
- Documentation: Docstrings.
- Dependencies: none.
- Do Not Change: N/A.
- Expected Result: Schemas importable.
- Definition of Done: Matches §13 exactly.

**Task 02 — Implement Service Methods**
- Task ID: B05-T02
- Objective: `get_parent_subscription()`, `cancel_subscription()`, `get_invoice_detail()`, `restore_purchase()`.
- Why This Is Required: Core business logic per §10.
- Existing Architecture to Follow: `BaseService`, `SubscriptionStateMachine` (B-03), `ReceiptValidationClient` (B-02).
- Existing Files to Reuse: `SubscriptionRepository`, B-02/B-03 components.
- Files to Create: none.
- Files to Modify: `service.py`, `repository.py`.
- Implementation Details: Per §10; cancel and restore both route through `SubscriptionStateMachine.transition()`.
- Business Rules: FR-4, Edge Cases #1, #5.
- Validation: Per §15.
- Error Handling: Per §18.
- Security: Family-ownership checks on every method.
- Performance: N/A.
- Localization/RTL: N/A.
- Analytics: Emit per §23 on success.
- Tests: Covered in Task 04.
- Documentation: Docstrings citing FR-4.
- Dependencies: Task 01, B-02, B-03.
- Do Not Change: Do not bypass `SubscriptionStateMachine` for cancel/restore transitions.
- Expected Result: Correct behavior for all 4 operations.
- Definition of Done: All Task 04 tests pass.

**Task 03 — Implement Routes**
- Task ID: B05-T03
- Objective: Expose the four routes.
- Why This Is Required: Public contract delivery.
- Existing Architecture to Follow: Existing router pattern, `get_current_parent`.
- Existing Files to Reuse: `api.py`.
- Files to Create: none.
- Files to Modify: `api.py`.
- Implementation Details: Per §13 exactly, all parent-session-gated.
- Business Rules: FR-4.
- Validation: Pydantic + service-layer checks.
- Error Handling: Per §18.
- Security: Structural child-mode-token rejection on all four.
- Performance: N/A.
- Localization/RTL/Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: OpenAPI summaries.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: All four endpoints live.
- Definition of Done: Matches §13 exactly.

**Task 04 — Write Test Suite**
- Task ID: B05-T04
- Objective: Cover all 8 scenarios in §27.
- Why This Is Required: QA coverage for parent-facing billing actions.
- Existing Architecture to Follow: pytest, async test client.
- Existing Files to Reuse: Fixture factories for subscription/invoice state.
- Files to Create: `tests/modules/subscriptions/test_parent_subscription_status_invoice_cancellation_api.py`.
- Files to Modify: none.
- Implementation Details: 8 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact status codes.
- Security: Cross-family invoice-access rejection test is security-critical.
- Performance: N/A.
- Localization/RTL: N/A.
- Analytics: Assert event emission.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 covered and green.

## 30. Definition of Done
All four parent-facing subscription endpoints live, gated by parent session, cancel/restore routed exclusively through `SubscriptionStateMachine`, cancellation never immediately revokes access, restore re-validates server-side, all tests green.

## 31. Final Verification Checklist
- [ ] Cancellation preserves access until period end (verified by test)
- [ ] Trial-cancel-within-first-hour honors full 7-day entitlement (Edge Case #1)
- [ ] Restore-purchase re-verifies server-side, no new purchase record created
- [ ] Cross-family invoice access rejected
- [ ] Cancel/restore both route through `SubscriptionStateMachine`, no bespoke writes
- [ ] Child-mode token structurally rejected on all four routes
- [ ] OpenAPI docs reflect full contract
