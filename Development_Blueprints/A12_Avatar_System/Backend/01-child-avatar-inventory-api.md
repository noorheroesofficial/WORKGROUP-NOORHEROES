# B-01 — Child Avatar & Inventory API

## 1. Feature Context
NoorHeroes Backend (FastAPI). Part of Feature A.12 — Avatar System (Character Evolution & Customization). Serves the child-facing Avatar screen: the 3D avatar preview base, the owned-items grid (grouped by slot), and locked-item teasers with resolved unlock criteria. Depends on A.1 (avatar base selection at child creation) and A.11 (Achievement Store purchases also grant `child_inventory` rows via a separate acquisition path).

## 2. Parent Feature
A.12 Avatar System — Backend (FastAPI)

## 3. Sub-feature
B-01 Child Avatar & Inventory API

## 4. Objective
Implement `GET /v1/children/{id}/inventory`, `POST /v1/children/{id}/inventory/{itemId}/equip`, and `POST /v1/children/{id}/inventory/{itemId}/unequip`, backing PRD FR-1, FR-2, FR-6, FR-7, FR-10, and Edge Cases 1, 4, 5, 9, 10.

## 5. Business Requirements
- Owned items are grouped by slot (outfit/glow/accessory); locked items include a server-resolved, human-readable `unlock_rule_description` — the client must never parse raw `unlock_rule` JSON (FR-1, §3.4).
- Equip is immediate, optimistic-client/server-confirmed, and instantly reflected server-side within the same transaction (FR-6).
- Exactly one equipped item per slot at all times — equipping a new item in a slot automatically unequips whatever was previously equipped there, in the same transaction (§3.4 Business Logic).
- Server-side ownership re-validation on every equip request — a tampered/stale client request referencing an unowned item must be rejected with `403 ITEM_NOT_OWNED` regardless of client-side state (Edge Case 10).
- Retired items (`is_retired=true`) remain fully visible and equippable for existing owners; retirement only blocks new acquisition (FR-10, Edge Case 1).
- A locked item whose `unlock_rule` references a deprecated badge/level/milestone must resolve to `unlock_rule_available: false` with a graceful "currently unavailable to unlock" description, never a broken reference or a crash (Edge Case 3).
- Rapid repeated equip taps within the same slot must resolve idempotently to last-tap-wins with no inconsistent intermediate state (Edge Case 4).
- No payment-related field exists anywhere in this API's request/response surface (FR-5, §3.5).

## 6. Existing Architecture
NoorHeroes Backend is a **Modular Monolith** with 10 core bounded contexts under `src/noorheroes/modules/*` (`identity`, `admin`, `ai_safety`, `content`, `learning`, `localization`, `media`, `notifications`, `rewards`, `subscriptions`), per `FAST-API-INSTRUCTIONS.md` §1/§5, plus an 11th context (`habits`) established by the A.7 Habit Tracker blueprint following the identical Router → Service → Repository → Model layering. **No `avatars` context exists yet.** This sub-feature establishes the 12th bounded context, `src/noorheroes/modules/avatars/`, following the same layering and the same `BaseRepository[ModelT]`/`BaseService`/`OutboxWriter` conventions used by every other context.

The existing `rewards` context (`src/noorheroes/modules/rewards/`) currently only implements `RewardLedgerEntry`/`RewardService.award_points()`/`get_balance()` (per `FAST-API-INSTRUCTIONS.md` §5.9) — it does **not** yet implement `badges`, `achievement_definitions`, or `catalog_items`/`child_inventory` as specified by the fuller A.11 Rewards System PRD, and **A.11 has not yet been generated as a Development Blueprint**. Per PRD A.12 §4 ("`avatar_items` and `child_inventory` are sourced directly from the Admin Database Schema table already referenced in the source material; this is their canonical definition"), this sub-feature is the canonical implementer of `avatars`/`avatar_items`/`child_inventory`. `badges`/`achievement_definitions`/habit-milestone-type references used by `unlock_rule` validation (owned by B-03) are treated as **external cross-context foreign-key references** into `rewards`/`habits` tables that must exist by the time B-03 enforces validation — flagged here explicitly as a dependency to reconcile once the A.11 Rewards System blueprint is generated, rather than silently assuming their shape.

`child_inventory` is deliberately designed as the **single shared ownership table** for two acquisition paths: this feature's criteria-based auto-unlock (B-02) and A.11's Achievement Store purchase flow — both must write to the same table with the same `UNIQUE(child_id, avatar_item_id)` constraint to avoid duplicate-ownership drift (PRD §3.1, §3.4).

**Companion Evolution note:** the Noor companion's tier/stage progression (FR-9, Character Evolution) is a distinct concept from `avatar_items` ownership and is **not** modeled by this sub-feature — it is owned by B-07 (Companion Evolution Tier API), which extends this endpoint's response with a `companion_evolution` field once implemented. Do not conflate item unlocks with companion-tier advancement when extending this schema.

## 7. Existing Code to Reuse
- `get_current_child` dependency → `ChildSessionContext(family_id, child_id, session_id)` (`core/deps.py`)
- `BaseRepository[ModelT]` (`common/base_repository.py`)
- `BaseService` (`common/base_service.py`)
- `OutboxWriter.emit()` (`common/outbox.py`) — for emitting inventory-change domain events consumed elsewhere (e.g., A.2 Home's Noor companion presentation)
- `DomainError` subclasses (`NotFoundError`, `AuthorizationError`, `ConflictError`) from `core/exceptions.py`
- Redis pool accessor pattern from `localization` context's `TranslationCacheManager` (reference pattern for the optional short-TTL inventory read cache)

## 8. Files to Create
- `src/noorheroes/modules/avatars/__init__.py`
- `src/noorheroes/modules/avatars/models.py` (`Avatar`, `AvatarItem`, `ChildInventory`)
- `src/noorheroes/modules/avatars/schemas.py` (`InventoryResponse`, `OwnedItemResponse`, `LockedItemResponse`, `EquipResponse`, `UnequipResponse`)
- `src/noorheroes/modules/avatars/repository.py` (`AvatarRepository.get_child_inventory()`, `.get_ownership_row()`, `.equip_item()`, `.unequip_item()`)
- `src/noorheroes/modules/avatars/service.py` (`AvatarService.get_inventory()`, `.equip_item()`, `.unequip_item()`)
- `src/noorheroes/modules/avatars/unlock_rule_resolver.py` (`UnlockRuleResolver.resolve_description()` — shared with B-02/B-03)
- `src/noorheroes/modules/avatars/api.py` (`AvatarsRouter`)
- `alembic/versions/<rev>_create_avatars_avatar_items_child_inventory_tables.py`
- `tests/modules/avatars/test_child_inventory_api.py`
- `tests/modules/avatars/test_equip_ownership_validation.py`
- `tests/modules/avatars/test_one_equipped_per_slot.py`

## 9. Files to Modify
- `main.py` — register `AvatarsRouter` alongside the other 11 domain routers

## 10. Backend Requirements
- Pydantic response schemas strictly typed; `owned_items`/`locked_items` are distinct lists, never a single mixed collection with a boolean flag.
- `GET /v1/children/{id}/inventory` resolves every locked item's `unlock_rule` into `unlock_rule_description` via `UnlockRuleResolver` server-side — the client never receives raw `unlock_rule` JSON.
- `unlock_rule_available: false` set when the resolver detects the referenced badge/level/milestone no longer exists or is deprecated (Edge Case 3), without omitting the item from the response.
- `POST .../equip` runs inside a single database transaction: (1) re-validate `(child_id, item_id)` ownership via `get_ownership_row()`, raising `AuthorizationError` → `403 ITEM_NOT_OWNED` if absent; (2) unequip any other `child_inventory` row for that child where the joined `avatar_items.slot` matches the target item's slot; (3) set the target row `equipped=true`. All three steps commit atomically or none do.
- `POST .../unequip` sets `equipped=false` on the specified owned row only; no cross-slot side effects.
- Router validates the `{id}` path param against `ChildSessionContext.child_id` — mismatched child IDs return `403`, never a silently empty/wrong-child response.
- Idempotent, safe under rapid repeated equip calls: the transaction's slot-scoped unequip-then-equip sequence guarantees the final state always matches the last request processed, with no possibility of two simultaneously-equipped items in one slot even under interleaved requests (enforced additionally by the DB partial unique index, §14).

## 11. KMP Requirements
Not applicable to this backend-only sub-feature; consumed by K-01/K-02 (`InventoryRepository.getInventory()`, `.equip()`, `.unequip()` → this endpoint set).

## 12. NextJS Requirements
Not applicable directly; the `avatar_items`/`avatars` catalog rows this endpoint reads are authored via N-01/N-02.

## 13. API Contract

**Required API 1**
- **HTTP Method:** GET
- **Endpoint:** `/v1/children/{id}/inventory`
- **Request:** none (path param `id` = child UUID)
- **Response 200:**
```json
{
  "avatar_base": { "avatar_id": "uuid", "name": "Explorer", "base_asset_key": "avatars/explorer.glb" },
  "owned_items": [
    { "item_id": "uuid", "slot": "outfit", "name": "Garden Explorer Outfit", "asset_key": "items/outfit_garden.glb", "icon": "icons/outfit_garden.png", "equipped": true }
  ],
  "locked_items": [
    { "item_id": "uuid", "slot": "glow", "name": "Golden Glow", "icon": "icons/glow_gold.png", "unlock_rule_description": "Complete a 7-day Quran reading streak", "unlock_rule_available": true }
  ]
}
```
- **Authentication:** Bearer, child-mode session (`get_current_child`)
- **Authorization:** child may only request their own `{id}`
- **Validation:** `{id}` must be a valid UUID and must match `ChildSessionContext.child_id`
- **Error Responses:** `401` unauthenticated; `403` child_id mismatch; `404` unknown child; `500` unexpected failure

**Required API 2**
- **HTTP Method:** POST
- **Endpoint:** `/v1/children/{id}/inventory/{itemId}/equip`
- **Request:** none (path params only)
- **Response 200:** `{ "equipped": true, "slot": "outfit" }`
- **Authentication:** Bearer, child-mode session
- **Authorization:** child may only equip into their own inventory
- **Validation:** server-side ownership check against `child_inventory`
- **Error Responses:** `401`; `403 ITEM_NOT_OWNED`; `404` unknown item/child; `500`

**Required API 3**
- **HTTP Method:** POST
- **Endpoint:** `/v1/children/{id}/inventory/{itemId}/unequip`
- **Request:** none
- **Response 200:** `{ "equipped": false }`
- **Authentication:** Bearer, child-mode session
- **Authorization:** child may only unequip their own owned items
- **Error Responses:** `401`; `403`; `404`; `500`

## 14. Database Requirements
- Table `avatars`: `avatar_id UUID PK`, `name VARCHAR`, `base_asset_key VARCHAR`.
- Table `avatar_items`: `item_id UUID PK`, `name VARCHAR`, `slot CHECK IN ('outfit','glow','accessory')`, `asset_key VARCHAR`, `icon VARCHAR`, `unlock_rule JSONB`, `is_retired BOOLEAN DEFAULT false`, `created_at TIMESTAMPTZ`. Index `(slot)`, index `(is_retired)`.
- Table `child_inventory`: `child_id UUID FK`, `avatar_item_id UUID FK`, `acquired_at TIMESTAMPTZ`, `equipped BOOLEAN DEFAULT false`. **`UNIQUE(child_id, avatar_item_id)`** (prevents duplicate ownership rows from either acquisition path — this feature's auto-unlock or A.11's store purchase). Partial unique index on `(child_id, slot)` WHERE `equipped = true`, derived via join to `avatar_items.slot`, enforcing at most one equipped item per slot at the database level as defense-in-depth beneath the service-layer transaction guarantee. Index `(child_id)`, index `(child_id, equipped)`.
- No destructive migrations — `is_retired=true` is the only removal mechanism for `avatar_items`; `child_inventory` rows are never deleted (§4.5 permanent-collection-record principle).

## 15. Validation
- Reject requests with missing/malformed `{id}`/`{itemId}` path params (`422`).
- Server-side enforcement that equip always re-validates ownership — verified by an integration test attempting to equip an unowned `item_id`, not left as an application convention only.
- Server-side enforcement that no slot ever has more than one simultaneously-equipped item — verified by an integration test equipping two different items in the same slot in sequence.

## 16. Authentication
Bearer JWT, child-mode session via `get_current_child`.

## 17. Authorization
Child may only fetch/mutate their own inventory; cross-child requests return `403`. No admin/parent bypass exists on these three endpoints (admin catalog authoring is B-03/B-04's separate concern).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Equip request for an unowned item (tampered/stale client state) | `403 ITEM_NOT_OWNED`; locked item remains locked regardless of client-side request (Edge Case 10) |
| Locked item's `unlock_rule` references a deprecated badge/level | `unlock_rule_available: false` with graceful "currently unavailable to unlock" description (Edge Case 3), rest of response unaffected |
| Rapid repeated equip taps in the same slot | Idempotent, last-processed-wins; no slot ever ends with more than one equipped item (Edge Case 4) |
| Item asset reference exists but is retired | Still returned as owned/equippable if already owned (Edge Case 1); excluded from any *new*-acquisition path (owned by B-02/A.11) |
| Database unavailable | `503` with retry-after; no partial/inconsistent equip state ever committed |
| Unknown child_id/item_id | `404` |

## 19. Offline First
Not directly implemented here (client owns offline caching/outbox — see K-06); this endpoint set must remain safely retriable (idempotent equip/unequip) to support the client's offline-queue-then-sync pattern.

## 20. Local Data
N/A (backend sub-feature).

## 21. Localization
`name` values for `avatars`/`avatar_items` and the resolved `unlock_rule_description` are sourced from the existing `localization` context's `TranslationContent` table pattern, resolved server-side per the requesting session's locale, or returned as translation keys for client-side resolution — following the existing `LocalizationRouter`/`TranslationService` pattern rather than inlining hardcoded strings.

## 22. RTL
N/A at the API layer; presentation direction is a client concern (K-01/K-02).

## 23. Analytics
None emitted server-side for these endpoints; `avatar_screen_viewed`, `avatar_item_equipped`, `avatar_item_unequipped` are client-side events (K-01/K-02).

## 24. Performance
Optional short-TTL Redis cache on the per-child inventory read (mirroring `habits`' `HabitCatalogCacheManager` pattern), invalidated on any equip/unequip/auto-unlock write; equip/unequip transactions are single round-trip, index-backed (`(child_id, equipped)`), targeting the PRD's p95 < 300ms equip-latency and p95 < 1s screen-load budgets.

## 25. Security
Ownership re-validation on every equip request is this endpoint set's primary access-control guarantee (§17); the partial unique index (§14) is defense-in-depth against a service-layer bug ever allowing two simultaneously-equipped items in one slot. Confirmed via schema-scan test that no request/response schema in this file accepts `payment_method`, `store_receipt`, or any IAP-related field (§3.5, FR-5).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, Redis (existing pool, optional cache), Alembic.

## 27. Testing
- Unit: `AvatarService.equip_item()` ownership-rejection path; one-equipped-per-slot transaction logic; `UnlockRuleResolver` deprecated-reference handling.
- Integration: full equip → inventory-read reflects new equipped state → app-restart-equivalent re-fetch persists; unowned-item equip rejection (`403`); rapid sequential equip across two items in the same slot resolves to exactly one equipped; retired-item-remains-equippable-for-owner regression.
- Schema-scan: assert no payment-related field exists on any schema in `avatars/schemas.py`.

## 28. Documentation
OpenAPI summary/description on the router; update `FAST-API-INSTRUCTIONS.md` §5 with a new `5.12 avatars Context` entry and §6 with `AvatarsRouter` once implemented.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create Avatar Domain Models**
- Objective: Define `Avatar`, `AvatarItem`, `ChildInventory` SQLAlchemy models.
- Why This Is Required: No `avatars` bounded context exists yet; this is the foundational schema every other B-0x sub-feature in this feature builds on.
- Existing Architecture to Follow: `BaseRepository[ModelT]`/model conventions used by `content`/`habits` contexts (declarative model, `created_at`, `is_retired`-style soft-removal flag rather than hard delete).
- Existing Files to Reuse: mirror `src/noorheroes/modules/habits/models.py` structure.
- Files to Create: `src/noorheroes/modules/avatars/models.py`
- Files to Modify: none
- Implementation Details: define all three models per §14; add `CHECK` constraint on `slot`; add the partial unique index on `(child_id, slot) WHERE equipped`.
- Business Rules: `is_retired` defaults `false`; `equipped` defaults `false`.
- Validation: DB-level CHECK constraint on `slot` enum; DB-level `UNIQUE(child_id, avatar_item_id)`.
- Error Handling: N/A at model layer.
- Security: none at this layer.
- Performance: indexes per §14.
- Localization: `name` stored as translation key, not raw string.
- RTL: N/A.
- Analytics: N/A.
- Tests: model import/table-creation smoke test.
- Documentation: docstring on each model class.
- Dependencies: none.
- Do Not Change: do not alter existing 11 contexts' models.
- Expected Result: three models importable and migratable together.
- Definition of Done: models compile, migration generated cleanly, partial unique index present.

**Task 02 — Create Alembic Migration**
- Objective: Persist `avatars`, `avatar_items`, `child_inventory` tables.
- Why This Is Required: models need a corresponding schema migration.
- Existing Architecture to Follow: existing Alembic revision chain under `alembic/versions/`.
- Files to Create: `alembic/versions/<rev>_create_avatars_avatar_items_child_inventory_tables.py`
- Implementation Details: `op.create_table` for all three tables matching §14; add all listed indexes including the partial unique index.
- Validation: run `alembic upgrade head` cleanly against a fresh DB and against a staging schema snapshot.
- Do Not Change: do not edit prior migration files; do not touch PostgreSQL credentials.
- Expected Result: all three tables exist with correct constraints/indexes.
- Definition of Done: migration applies and rolls back cleanly.

**Task 03 — Create Response Schemas**
- Objective: Define `InventoryResponse`, `OwnedItemResponse`, `LockedItemResponse`, `EquipResponse`, `UnequipResponse` Pydantic v2 models.
- Files to Create: `src/noorheroes/modules/avatars/schemas.py`
- Implementation Details: strict typing per §13 response shapes; no field accepts payment-related data (§25).
- Validation: field validators for `slot` enum.
- Tests: schema serialization unit test; schema-scan test asserting absence of payment fields.
- Expected Result: schemas match API contract exactly.
- Definition of Done: schemas round-trip sample data correctly; schema-scan test passes.

**Task 04 — Implement `UnlockRuleResolver`**
- Objective: Resolve `avatar_items.unlock_rule` JSONB into a human-readable description string, flagging deprecated references.
- Existing Architecture to Follow: shared utility consumed by both this sub-feature (read path) and B-03 (write-path validation).
- Files to Create: `src/noorheroes/modules/avatars/unlock_rule_resolver.py`
- Implementation Details: resolve `badge_id` → badge name/description via cross-context lookup into `rewards`; resolve `level_threshold` similarly; resolve `habit_milestone_type`+`threshold` via cross-context lookup into `habits`. On any lookup miss, return `unlock_rule_available=false` with a generic "currently unavailable to unlock" description rather than raising.
- Business Rules: never raise/crash on a stale reference (Edge Case 3).
- Error Handling: swallow lookup misses into the `unavailable` state; log for admin visibility.
- Tests: unit tests for all three rule types plus the deprecated-reference case.
- Definition of Done: resolver returns correct description for all three rule types and the deprecated case.

**Task 05 — Implement `AvatarRepository`**
- Objective: `get_child_inventory()`, `get_ownership_row()`, `equip_item()`, `unequip_item()` query/mutation methods.
- Existing Architecture to Follow: `BaseRepository[ModelT]` subclass pattern.
- Files to Create: `src/noorheroes/modules/avatars/repository.py`
- Implementation Details: `equip_item()` performs the unequip-prior-slot-item + equip-target-item sequence within the caller's transaction (no internal commit, per Layer Rule #2).
- Performance: use `(child_id, equipped)`/`(child_id)` indexes; avoid N+1 by joining `avatar_items` for slot resolution in a single query.
- Tests: repository-level integration tests against a seeded test DB, including the one-equipped-per-slot sequence.
- Definition of Done: repository correctly enforces the slot invariant for all fixture combinations.

**Task 06 — Implement `AvatarService`**
- Objective: `get_inventory(child_id)`, `equip_item(child_id, item_id)`, `unequip_item(child_id, item_id)` orchestrating repository + `UnlockRuleResolver` + ownership checks.
- Existing Architecture to Follow: `BaseService` pattern; raises `AuthorizationError` on ownership failure (mapped to `403 ITEM_NOT_OWNED` by the router's exception handler).
- Files to Create: `src/noorheroes/modules/avatars/service.py`
- Business Rules: FR-1, FR-2, FR-6, FR-7, FR-10.
- Error Handling: propagate repository/resolver errors as domain exceptions.
- Tests: unit tests mocking repository and resolver, covering ownership-rejection and slot-invariant paths.
- Definition of Done: service returns correct inventory/equip/unequip results for all PRD scenarios in §1.9/§1.10.

**Task 07 — Implement the Three Endpoints**
- Objective: Wire router to service with auth/ownership checks.
- Existing Architecture to Follow: router pattern from `HabitsRouter`/`RewardsRouter`.
- Files to Create/Modify: `src/noorheroes/modules/avatars/api.py`; modify `main.py` to include `AvatarsRouter`.
- Authentication: `Depends(get_current_child)` on all three routes.
- Authorization: reject `{id}` mismatch with `403` before touching the service.
- Error Handling: per §18 table.
- Tests: integration tests hitting the live routes via test client.
- Definition of Done: all three endpoints live, documented in OpenAPI, auth-enforced.

**Task 08 — Add Ownership Re-validation & One-Equipped-Per-Slot Tests (P0)**
- Objective: Dedicated, CI-blocking test coverage for the two highest-priority invariants named in the PRD's Backend AI Code-Generation Prompt items 1–2.
- Files to Create: `tests/modules/avatars/test_equip_ownership_validation.py`, `tests/modules/avatars/test_one_equipped_per_slot.py`
- Definition of Done: both tests pass and are marked as mandatory/non-bypassable CI gates per PRD §10 DevOps Requirements.

**Task 09 — Add Full Endpoint Test Suite & Documentation**
- Objective: Complete coverage per §27; OpenAPI docs; `FAST-API-INSTRUCTIONS.md` update.
- Files to Create: `tests/modules/avatars/test_child_inventory_api.py`
- Documentation: update `FAST-API-INSTRUCTIONS.md` §5/§6 with the new `avatars` context entry.
- Definition of Done: test suite green; docs updated.

**Task 10 — Final Code Review**
- Objective: Verify against Definition of Done and Final Verification Checklist below before merge.
- Do Not Change: PostgreSQL/Redis credentials; existing 11 bounded contexts' unrelated code.
- Expected Result: PR ready for merge, CI green including both P0 gate tests.

## 30. Definition of Done
`GET /v1/children/{id}/inventory`, `POST .../equip`, `POST .../unequip` live, authenticated, authorized, tested, documented. Ownership re-validation and one-equipped-per-slot invariants hold under all tested conditions, including rapid repeated requests. Retired items remain equippable for existing owners. No payment-related fields exist on any schema.

## 31. Final Verification Checklist
- [x] `Avatar`, `AvatarItem`, `ChildInventory` models + migration created and reviewed, including the partial unique index
- [x] `UnlockRuleResolver` correctly resolves all three rule types and the deprecated-reference case
- [x] Equip endpoint enforces server-side ownership re-validation (`403 ITEM_NOT_OWNED` test passing, CI-blocking)
- [x] One-equipped-per-slot invariant enforced transactionally and verified under rapid repeated requests (CI-blocking)
- [x] Retired-item-remains-equippable-for-owner regression test passing
- [x] Error handling matches §18 exactly
- [x] Schema-scan test confirms zero payment-related fields
- [x] Unit + integration tests passing
- [x] OpenAPI documentation complete
- [x] `main.py` router registration confirmed
- [x] No PostgreSQL/Redis credential changes
- [x] No unrelated existing-context code modified
