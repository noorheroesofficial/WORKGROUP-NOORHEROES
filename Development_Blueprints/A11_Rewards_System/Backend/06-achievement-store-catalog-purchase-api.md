# B-06 — Achievement Store Catalog & Purchase API (User)

## 1. Feature Context
Part of Feature A.11 — Rewards System. The only spend-side surface in the reward economy: browsing the admin-managed cosmetic catalog and purchasing with Noor Heroes Points, atomically.

## 2. Parent Feature
A.11 Rewards System — Backend (FastAPI)

## 3. Sub-feature
B-06 Achievement Store Catalog & Purchase API (User)

## 4. Objective
Implement `GET /v1/catalog-items` and `POST /v1/rewards/claims` as an atomic, idempotent purchase transaction, backing FR-1, FR-8, FR-11 and Edge Cases 7, 8.

## 5. Business Requirements
- Noor Heroes Points are never purchasable with real money — structurally absent from this service, not merely unused (FR-1, FR-8, a hard zero-exception rule).
- Purchase debits the ledger and grants `child_inventory` atomically — together or not at all.
- Duplicate claim (double-tap) resolves via idempotency, shown as "already claimed," never a double-debit or error (Edge Case 8).
- A purchase-succeeds-but-equip-fails scenario is fine: ownership is committed independently of the (A.12-owned) equip action (Edge Case 7).

## 6. Existing Architecture
Extends the `rewards` bounded context. Purchase debit routes through the same append-only `reward_ledger` (B-01) as a negative-amount entry (`reason_type='store_purchase'`), inside one atomic DB transaction with the `child_inventory` insert.

## 7. Existing Code to Reuse
- B-01's ledger insert primitives (reused inside this transaction, not duplicated).
- `get_current_child` dependency.

## 8. Files to Create
- `src/noorheroes/modules/rewards/models.py` — extend with `CatalogItem`, `ChildInventory`.
- `alembic/versions/<rev>_create_catalog_inventory_tables.py`
- `tests/modules/rewards/test_purchase_atomicity.py`
- `tests/modules/rewards/test_purchase_idempotency.py`
- `tests/modules/rewards/test_no_real_money_purchase_path.py`

## 9. Files to Modify
- `src/noorheroes/modules/rewards/schemas.py` — `CatalogItemResponse`, `ClaimRequest`, `ClaimResponse`.
- `src/noorheroes/modules/rewards/service.py` — `list_catalog_items()`, `purchase_item()`.
- `src/noorheroes/modules/rewards/api.py` — add both routes.

## 10. Backend Requirements
- `catalog_items.price_points > 0` (CHECK constraint).
- `UNIQUE(child_id, item_id)` on `child_inventory`.
- `purchase_item()` wraps the negative-amount ledger insert and `child_inventory` insert in a single DB transaction; any failure rolls back both.
- `UNIQUE(idempotency_key)` on the claim operation (same pattern as B-01).
- Insufficient balance returns `402 INSUFFICIENT_POINTS` with the shortfall amount, no debit attempted.
- Structural audit: this module's OpenAPI schema must contain zero fields matching `/payment|receipt|price_usd|iap/i` on any endpoint capable of minting or spending currency.

## 11. KMP Requirements
Consumed by K-07 (Achievement Store Catalog & Purchase Flow).

## 12. NextJS Requirements
Catalog authored via B-12 (Admin Achievement Store Catalog Management API).

## 13. API Contract

**Required API**
- **HTTP Method:** GET
- **Endpoint:** `/v1/catalog-items?child_id=`
- **Response 200:** Array of `{ "id","type","price_points","eligibility_json","owned": bool }`

**Required API — Purchase**
- **HTTP Method:** POST
- **Endpoint:** `/v1/rewards/claims`
- **Request:** `{ "catalog_item_id":"...", "child_id":"...", "idempotency_key":"uuid..." }`
- **Response 200:** `{ "claimed": true, "item_id":"...", "new_balance": 130 }` or, on replay, the identical original result framed as "already claimed."
- **Error Codes:** `402 INSUFFICIENT_POINTS` (returns shortfall amount).
- **Validation:** atomic transaction per §10.

## 14. Database Requirements
- `catalog_items`: `id UUID PK`, `type VARCHAR`, `price_points INT CHECK > 0`, `eligibility_json JSONB`, `active BOOLEAN`. Index `(active, type)`.
- `child_inventory`: `child_id UUID FK`, `item_id UUID FK`, `acquired_at`, `equipped_at TIMESTAMPTZ NULL`. `UNIQUE(child_id, item_id)`. Index `(child_id)`.
- Soft delete: `catalog_items.active = false` retires an item without breaking existing `child_inventory` rows.

## 15. Validation
- Test: failure injected between debit and inventory insert → neither side-effect persists (full rollback).
- Test: duplicate claim returns original "already claimed" result without a second debit.
- Test: OpenAPI schema scan for `payment|receipt|price_usd|iap` fields → zero matches.

## 16. Authentication
Bearer JWT, child-mode, for both endpoints.

## 17. Authorization
Purchases scoped to own `child_id`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Insufficient balance | `402`, shortfall amount returned, no debit |
| Duplicate claim (double-tap) | Idempotent replay, "already claimed," no second debit |
| Mid-transaction failure | Full rollback, no partial state |
| Item deactivated after being viewed but before purchase | Purchase rejected with a clear "no longer available" error, distinct from insufficient-points |

## 19. Offline First
Purchases require connectivity (PRD §1.14) — no offline queueing for `POST /v1/rewards/claims`, unlike reward-completion events.

## 20. Local Data
N/A (backend).

## 21. Localization
Item type/category keys resolved client-side; no localized text stored here.

## 22. RTL
N/A.

## 23. Analytics
Emit `achievement_store_viewed/item_viewed/purchase_attempted/purchase_completed/purchase_insufficient_points` per PRD §1.19.

## 24. Performance
Catalog list cached briefly (active items change infrequently); purchase transaction kept minimal (two writes, one commit) to stay within the reward-award latency budget.

## 25. Security
Structural absence of any payment/IAP field is this endpoint's defining security/trust property (PRD §12.1, §12.7) — verified by an automated schema scan, not just code review.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async (transactional session), PostgreSQL, Pydantic v2.

## 27. Testing
- Unit: shortfall calculation, eligibility filtering.
- Integration: full purchase → debit + inventory grant → wallet reflects new balance.
- Atomicity, idempotency, and schema-scan tests per §15 (mandatory).

## 28. Documentation
OpenAPI docs explicitly stating the atomic-transaction guarantee and the structural no-real-money-purchase-path property.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `CatalogItem`/`ChildInventory` Models & Migration**
- Files to Create: models + migration per §8/§14.
- Definition of Done: tables created with correct constraints.

**Task 02 — Implement `list_catalog_items()`**
- Files to Modify: `service.py`
- Implementation Details: eligibility filtering, owned-state annotation per child.
- Definition of Done: correct response shape.

**Task 03 — Implement Atomic `purchase_item()`**
- Files to Modify: `service.py`
- Existing Files to Reuse: B-01's ledger-insert primitive (negative amount, `reason_type='store_purchase'`).
- Business Rules: FR-1, FR-11, Edge Case 7, Edge Case 8.
- Implementation Details: single DB transaction wrapping debit + inventory insert; idempotency via `UNIQUE(idempotency_key)`.
- Error Handling: `402` on insufficient balance, atomic rollback on any failure.
- Tests: atomicity + idempotency tests (mandatory).
- Definition of Done: both tests passing.

**Task 04 — Implement Endpoints**
- Files to Modify: `api.py`
- Authentication/Authorization: per §16/§17.
- Tests: integration tests.
- Definition of Done: both endpoints live.

**Task 05 — Implement No-Real-Money-Purchase-Path Schema Scan (Mandatory CI Gate)**
- Files to Create: `test_no_real_money_purchase_path.py`
- Implementation Details: scan this module's OpenAPI schema for `payment|receipt|price_usd|iap` fields.
- Definition of Done: zero matches, wired as a non-bypassable CI gate.

**Task 06 — Add API Documentation**
- Documentation: atomic-transaction + no-purchase-path notes.
- Definition of Done: docs reviewed.

**Task 07 — Final Code Review**
- Do Not Change: `reward_ledger` append-only guarantees; PostgreSQL/Redis credentials.
- Expected Result: PR merge-ready, CI green including the schema-scan gate.

## 30. Definition of Done
Catalog browse and atomic purchase endpoints live; zero real-money-purchase surface, verified by an automated, CI-blocking schema scan.

## 31. Final Verification Checklist
- [ ] Purchase debit + inventory grant atomic (rollback test passing)
- [ ] Duplicate claim idempotent, no double-debit
- [ ] `402 INSUFFICIENT_POINTS` returns shortfall, no debit
- [ ] Deactivated-item purchase attempt handled distinctly from insufficient-points
- [ ] OpenAPI schema scan for payment/IAP fields passes (zero matches), CI-blocking
- [ ] Soft-delete (`active=false`) preserves existing ownership records
- [ ] OpenAPI documentation complete
