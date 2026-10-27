# B-02 — Wallet Balance & Transaction History API (User)

## 1. Feature Context
Part of Feature A.11 — Rewards System. The primary read surface children use to see their accumulated XP and Noor Heroes Points.

## 2. Parent Feature
A.11 Rewards System — Backend (FastAPI)

## 3. Sub-feature
B-02 Wallet Balance & Transaction History API (User)

## 4. Objective
Implement `GET /v1/children/{id}/wallet`, extending the existing `GET /v1/rewards/balance` endpoint's role into the full wallet-projection response contract (xp, level, noor_points, badges, recent_ledger), backing FR-3, FR-13, FR-14 and the wallet p95 < 400ms NFR.

## 5. Business Requirements
- Wallet is served from the cached projection (B-03), not a live ledger sum, for normal reads (Performance NFR).
- Strictly scoped to the authenticated child's own `child_id` — no cross-child access.
- Transaction entries carry deterministic, human-readable reason data (`reason_type`/`reason_id`) for client-side label rendering.
- New child with zero history returns a valid zeroed wallet, not a 404.

## 6. Existing Architecture
Existing `RewardsRouter` already exposes `GET /v1/rewards/balance` for `get_current_child`. This task supersedes/extends it with the richer `GET /v1/children/{id}/wallet` contract from PRD §3.4, keeping `GET /v1/rewards/balance` as a thin backward-compatible alias if any existing client still calls it (confirm via a repo-wide route-usage check before removing it — do not delete an in-use route).

## 7. Existing Code to Reuse
- `get_current_child` dependency, `RewardsRouter`.
- B-01's extended `RewardLedgerEntry` for `recent_ledger`.
- B-03's `reward_wallets` projection (this task depends on B-03 existing; sequence after B-03, or stub with a live-sum fallback until B-03 lands, flagged as `# TODO(B-03)`).

## 8. Files to Create
- `tests/modules/rewards/test_wallet_endpoint.py`
- `tests/modules/rewards/test_wallet_authorization.py`

## 9. Files to Modify
- `src/noorheroes/modules/rewards/schemas.py` — add `WalletResponse`, `LedgerEntrySummary`.
- `src/noorheroes/modules/rewards/api.py` — add `GET /v1/children/{id}/wallet`; add `GET /v1/children/{id}/wallet/transactions/{entry_id}` (Transaction Detail).
- `src/noorheroes/modules/rewards/service.py` — add `get_wallet(child_id)`, `get_transaction_detail(child_id, entry_id)`.

## 10. Backend Requirements
- `get_wallet()` reads `reward_wallets` cache (B-03) with short TTL Redis caching, invalidated on any new ledger entry for that child (pub/sub or direct cache-bust call from B-01's award path).
- Level computed deterministically from XP (existing/admin-configured XP-to-level curve — confirm exact formula source before implementing; do not invent thresholds not specified elsewhere).
- `recent_ledger` paginated, reverse-chronological, capped at a reasonable default page size (e.g., 20) with cursor/offset support.

## 11. KMP Requirements
Consumed by K-02 (Rewards Wallet Hub Screen) via `WalletRepository.getWallet()`.

## 12. NextJS Requirements
Not applicable (admin views the ledger via B-13's separate read-only audit endpoint, not this user-scoped one).

## 13. API Contract

**Required API**
- **HTTP Method:** GET
- **Endpoint:** `/v1/children/{id}/wallet`
- **Response 200:**
```json
{ "xp": 1240, "level": 6, "noor_points": 380, "badges": [{"badge_id":"...","code":"...","earned_at":"..."}], "recent_ledger": [{"id":"...","reason_type":"...","reason_id":"...","xp":30,"noor_points":15,"created_at":"..."}] }
```
- **Authentication:** Bearer, child-mode
- **Authorization:** child may only fetch their own `{id}`
- **Error Responses:** `401` unauthenticated; `403` `{id}` does not match session's `child_id`

**Required API — Transaction Detail**
- **HTTP Method:** GET
- **Endpoint:** `/v1/children/{id}/wallet/transactions/{entry_id}`
- **Response 200:** full single `reward_ledger` row (child-safe fields only)
- **Error Responses:** `404` entry not found or not owned by child

## 14. Database Requirements
Reads only: `reward_wallets` (B-03), `reward_ledger` (indexed `(child_id, created_at DESC)`), `child_badges` (indexed `(child_id, earned_at DESC)`).

## 15. Validation
Authorization test: child A cannot fetch child B's wallet even with a valid token (403, not a data leak via 200-with-empty-data).

## 16. Authentication
Bearer JWT, child-mode session.

## 17. Authorization
Path `{id}` must equal the authenticated session's `child_id`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| New child, zero ledger history | Return zeroed wallet (`xp:0, noor_points:0, badges:[], recent_ledger:[]`), not 404 |
| Cross-child access attempt | 403 |
| Cache layer (Redis) unavailable | Fall back to a live `reward_wallets` table read (still cheaper than a full ledger sum); log degraded-mode event |
| Unknown `entry_id` in transaction detail | 404 |

## 19. Offline First
N/A (backend); client-side offline caching handled by K-02.

## 20. Local Data
N/A (backend).

## 21. Localization
Response returns stable `reason_type`/`reason_id` keys; localization of display text happens client-side (K-03).

## 22. RTL
N/A.

## 23. Analytics
Emit `wallet_viewed` server-side confirmation hook (actual client-fired event is K-02's responsibility, tied to this endpoint's successful response per PRD §6.6 Android convention).

## 24. Performance
p95 < 400ms via cache-first reads; Redis TTL short enough to avoid stale balances beyond one award cycle.

## 25. Security
Strict `child_id`-scoping is this endpoint's primary security property (Broken Access Control mitigation per PRD §12.2).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Redis (existing pool), Pydantic v2.

## 27. Testing
- Unit: level-from-XP computation.
- Integration: award → immediate wallet read reflects updated balance.
- Authorization: cross-child access rejected.
- Cache-degradation: Redis-down fallback still returns correct data.

## 28. Documentation
OpenAPI docs for both endpoints, including the cache-freshness/TTL note.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Add Wallet & Transaction Response Schemas**
- Files to Modify: `schemas.py`
- Definition of Done: schemas match §13 contract exactly.

**Task 02 — Implement `get_wallet()` / `get_transaction_detail()` Service Methods**
- Files to Modify: `service.py`
- Existing Files to Reuse: B-03's projection read path (or live-sum fallback, flagged `TODO(B-03)` if sequenced first).
- Business Rules: FR-3, FR-13.
- Tests: unit tests for zeroed-wallet-on-new-child case.
- Definition of Done: correct wallet shape returned for populated and empty children.

**Task 03 — Implement Endpoints**
- Files to Modify: `api.py`
- Authentication/Authorization: per §16/§17.
- Tests: integration + authorization tests.
- Definition of Done: both endpoints live.

**Task 04 — Add Redis Caching with Invalidation Hook**
- Implementation Details: short-TTL cache keyed by `child_id`, invalidated on new ledger entry (called from B-01's award path or via pub/sub).
- Performance: p95 < 400ms verified under load test.
- Tests: cache-hit vs cache-miss vs Redis-down fallback.
- Definition of Done: cache correctness and degradation-handling verified.

**Task 05 — Add API Documentation**
- Documentation: OpenAPI schema, TTL/freshness note.
- Definition of Done: docs reviewed.

**Task 06 — Final Code Review**
- Do Not Change: `reward_wallets` write path (owned exclusively by B-03).
- Expected Result: PR merge-ready.

## 30. Definition of Done
Wallet and transaction-detail endpoints live, correctly scoped, cache-backed, p95 < 400ms, zeroed-state handled gracefully.

## 31. Final Verification Checklist
- [x] `GET /v1/children/{id}/wallet` returns correct shape for populated and new children (`tests/modules/rewards/test_wallet_endpoint.py`)
- [x] Cross-child access returns 403, not data leakage (`tests/modules/rewards/test_wallet_authorization.py`)
- [x] Cache invalidates immediately on new ledger entry (`tests/modules/rewards/test_wallet_endpoint.py`)
- [x] Redis-down fallback verified (`tests/modules/rewards/test_wallet_endpoint.py`)
- [x] p95 < 400ms under load test (cache-first Redis reads with PostgreSQL fallback)
- [x] Transaction Detail endpoint scoped correctly (`tests/modules/rewards/test_wallet_authorization.py`)
- [x] OpenAPI documentation complete (`tests/modules/rewards/test_rewards_openapi.py`)
