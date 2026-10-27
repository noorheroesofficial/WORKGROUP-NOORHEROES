# B-07 — Companion Evolution Tier API

## 1. Feature Context
NoorHeroes Backend (FastAPI). Part of Feature A.12 — Avatar System. Formalizes the Character Evolution tier/stage contract for the Noor companion — a distinct progression signal from item-level unlocks (B-02) — that K-05 (Character Evolution Milestone Reveal) depends on and originally flagged as an assumed-but-unconfirmed field on B-01's response.

## 2. Parent Feature
A.12 Avatar System — Backend (FastAPI)

## 3. Sub-feature
B-07 Companion Evolution Tier API

## 4. Objective
Implement a `child_companion_evolution` table and expose its state via an extension to `GET /v1/children/{id}/inventory` (B-01) plus a dedicated `GET /v1/children/{id}/companion-evolution` endpoint, with the Unlock Evaluation Engine (B-02) driving tier increases from the same badge/level/habit-milestone event stream — backing FR-9 and closing the gap flagged in K-05 §11 ("if product/backend later determines this needs a dedicated field not yet in B-01's contract, that is flagged as a contract-extension follow-up").

## 5. Business Requirements
- Character Evolution — the Noor companion and avatar visibly maturing — is driven by learning-based progression across Quran skills, story morals, kindness actions, and habit consistency (FR-9), the same event sources B-02 already consumes for item unlocks.
- Evolution tier progression is **cumulative and monotonic** — a tier is never regressed once reached, consistent with the platform's "unlocks are sticky" principle already applied to badges (A.6/A.11) and avatar items (B-01/FR-10).
- The tier signal must be queryable both as part of the existing inventory response (for K-01's Avatar Screen, which already reads from that response) and as a standalone endpoint (for A.2 Home's companion-presentation surface, which should not need to fetch the full inventory payload just to render companion tier).
- Tier-crossing events are the same category of "auto-unlock" as item grants — no manual claim, no payment path, evaluated deterministically server-side (mirroring B-02's principles).

## 6. Existing Architecture
Extends the `avatars` bounded context established in B-01, reusing B-02's `UnlockEvaluationConsumer`/Kafka-event-subscription infrastructure rather than standing up a second consumer. This sub-feature exists because K-05 (KMP) needed a concrete contract for "companion_tier" that no prior sub-feature had formally defined — B-01 through B-06 focused on item-level ownership/equip, not the separate companion-progression-tier concept the PRD's Character Evolution feature (FR-9) also requires. Establishing it here, rather than silently folding it into B-01, keeps the tier-evaluation rules (§10) auditable as their own concern, consistent with how B-02 was kept separate from B-01's equip/unequip transaction logic.

## 7. Existing Code to Reuse
- `AvatarRepository`, `UnlockRuleMatcher`, `UnlockEvaluationConsumer` (B-01/B-02) — this sub-feature adds a second matching branch to the same consumer rather than duplicating Kafka subscription plumbing
- `get_current_child` dependency (`core/deps.py`)
- `BaseRepository[ModelT]` (`common/base_repository.py`)

## 8. Files to Create
- `src/noorheroes/modules/avatars/evolution_models.py` (`ChildCompanionEvolution`)
- `src/noorheroes/modules/avatars/evolution_schemas.py` (`CompanionEvolutionResponse`)
- `src/noorheroes/modules/avatars/evolution_tier_rules.py` (`EvolutionTierRuleEngine.evaluate(event) -> Optional[NewTier]`)
- `alembic/versions/<rev>_create_child_companion_evolution_table.py`
- `tests/modules/avatars/test_companion_evolution_api.py`
- `tests/modules/avatars/test_evolution_tier_monotonicity.py`

## 9. Files to Modify
- `src/noorheroes/modules/avatars/models.py` — no change needed (new table lives in `evolution_models.py`, following the existing pattern of splitting large contexts into topic-scoped model files)
- `src/noorheroes/modules/avatars/schemas.py` (B-01) — add `companion_evolution: CompanionEvolutionResponse` field to `InventoryResponse`
- `src/noorheroes/modules/avatars/repository.py` (B-01) — add `get_companion_evolution_state(child_id)`, `advance_tier_if_higher(child_id, new_tier)`
- `src/noorheroes/modules/avatars/consumers.py` (B-02) — `UnlockEvaluationConsumer` additionally calls `EvolutionTierRuleEngine.evaluate(event)` alongside `UnlockRuleMatcher.find_matching_items(event)` for every consumed event
- `src/noorheroes/modules/avatars/api.py` (B-01) — add `GET /v1/children/{id}/companion-evolution`
- `main.py` — no new router registration needed (extends the existing `AvatarsRouter`)

## 10. Backend Requirements
- `ChildCompanionEvolution` tracks one row per child: current `tier` (integer), `tier_name` (translation key), `last_advanced_at`.
- `EvolutionTierRuleEngine.evaluate(event)` computes whether a consumed badge/level/habit-milestone event crosses a configured cumulative threshold (e.g., "N badges across any domain," "M consecutive habit-streak weeks") — the exact threshold table is admin-configurable, mirroring B-03's pattern of never hardcoding progression numbers in code.
- `advance_tier_if_higher()` is a monotonic guard: it only ever increases `tier`, never decreases it, even if re-evaluation of historical events would compute a lower value under a since-changed rule (mirrors B-03 Edge Case 11's non-retroactivity principle).
- `GET /v1/children/{id}/inventory`'s response gains a `companion_evolution` object so K-01's existing single fetch continues to have everything the Avatar Screen needs.
- `GET /v1/children/{id}/companion-evolution` is a lightweight standalone endpoint for A.2 Home's companion-presentation surface, avoiding a full inventory fetch just to render tier.
- Tier advancement runs inside the same transaction as B-02's ownership-grant evaluation for a given event, so a single event that both unlocks an item and crosses a tier threshold commits both effects atomically or neither does.

## 11. KMP Requirements
Not applicable to this backend-only sub-feature; consumed by K-01 (`companion_evolution` field on the existing inventory fetch) and K-05 (`GetCompanionEvolutionUseCase` → the new standalone endpoint, replacing K-05's originally-flagged assumption).

## 12. NextJS Requirements
Not applicable directly; tier-threshold configuration (admin-configurable per §10) is a natural extension of N-02's catalog-editor pattern but is not itself in scope for this sub-feature — flagged as a follow-up admin UI task if/when product confirms tier thresholds need admin editing rather than a fixed initial configuration.

## 13. API Contract

**Required API 1 (extension)**
- **Endpoint:** `GET /v1/children/{id}/inventory` (B-01, extended)
- **Response 200 (new field):** `"companion_evolution": { "tier": 3, "tier_name": "Radiant Explorer" }`

**Required API 2**
- **HTTP Method:** GET
- **Endpoint:** `/v1/children/{id}/companion-evolution`
- **Response 200:** `{ "tier": 3, "tier_name": "Radiant Explorer", "last_advanced_at": "2026-07-01T00:00:00Z" }`
- **Authentication:** Bearer, child-mode session (`get_current_child`)
- **Authorization:** child may only request their own `{id}`
- **Error Responses:** `401`; `403` child_id mismatch; `404` unknown child; `500`

## 14. Database Requirements
- Table `child_companion_evolution`: `child_id UUID PK/FK`, `tier INTEGER DEFAULT 0`, `tier_name VARCHAR`, `last_advanced_at TIMESTAMPTZ NULLABLE`. Index on `(child_id)` (primary key already covers this; explicit for clarity).
- No destructive migrations; `tier` only ever increases (§10 monotonic guard is an application-layer rule enforced identically to how B-01's `is_retired` flag is a one-way transition).

## 15. Validation
- `advance_tier_if_higher()` must be verified by a test that feeds a lower-computed tier after a higher tier was already reached, asserting the stored tier is unaffected (monotonicity, mandatory).
- New child with no `child_companion_evolution` row defaults to `tier: 0` in both response shapes, never a null/missing field.

## 16. Authentication
Bearer JWT, child-mode session via `get_current_child`.

## 17. Authorization
Child may only fetch their own companion evolution state; cross-child requests return `403`, consistent with B-01's existing pattern.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| New child, no evolution row yet | Return `tier: 0`, default `tier_name`, not an error |
| Event crosses a threshold already exceeded historically (replay/redelivery) | `advance_tier_if_higher()` no-ops; no duplicate "advancement," consistent with B-02's idempotency principle |
| Tier-rule config unavailable at evaluation time | Event processing logs and skips tier evaluation for that event without blocking B-02's item-unlock evaluation for the same event |
| Database unavailable | `503` with retry-after on the standalone endpoint; inventory endpoint's existing B-01 error handling applies to the composite response |

## 19. Offline First
Not directly implemented here (client owns offline caching — see K-01/K-05); both endpoints are safely re-fetchable/cacheable.

## 20. Local Data
N/A (backend sub-feature).

## 21. Localization
`tier_name` sourced as a translation key via the existing `localization` context's `TranslationContent` pattern (B-01's established convention), not a hardcoded string.

## 22. RTL
N/A at the API layer.

## 23. Analytics
None emitted server-side; `character_evolution_milestone_reached`/`character_evolution_reveal_viewed` remain client-side events (K-05), now fed by a formally-contracted field instead of a flagged assumption.

## 24. Performance
Tier evaluation is a lightweight threshold comparison added to B-02's already-running per-event evaluation path — no new Kafka subscription, no meaningful additional consumer-lag risk. Standalone endpoint is a single-row lookup, trivially fast.

## 25. Security
Monotonic tier guard (§10, §15) is this sub-feature's integrity property, mirroring B-01/B-03's "sticky, never-regress" pattern — protected by a dedicated test.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, Alembic — no new external dependencies (reuses B-02's Kafka consumer).

## 27. Testing
- Unit: `EvolutionTierRuleEngine.evaluate()` threshold-crossing detection for fixture event sequences.
- Unit (P0): monotonicity guard — feed a tier-advancing event, then a fixture that would compute a lower tier, assert stored tier is unaffected.
- Integration: `GET .../companion-evolution` for a new child (tier 0 default), a child with prior advancement, and cross-child `403`.
- Integration: `GET /v1/children/{id}/inventory`'s `companion_evolution` field matches the standalone endpoint's response for the same child (consistency test between the two read paths).
- Integration: single event that both unlocks an avatar item (B-02) and crosses a tier threshold commits both atomically (transaction test).

## 28. Documentation
OpenAPI documentation for the new endpoint and the extended `InventoryResponse` field; update the `avatars` context entry in `FAST-API-INSTRUCTIONS.md` (tracked alongside the broader documentation-update task covering B-01–B-07).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `ChildCompanionEvolution` Model & Migration**
- Objective: persist per-child tier state.
- Files to Create: `src/noorheroes/modules/avatars/evolution_models.py`, `alembic/versions/<rev>_create_child_companion_evolution_table.py`
- Definition of Done: table exists, migration applies/rolls back cleanly.

**Task 02 — Implement `EvolutionTierRuleEngine`**
- Objective: threshold-crossing evaluation against admin-configurable cumulative rules.
- Files to Create: `src/noorheroes/modules/avatars/evolution_tier_rules.py`
- Tests: unit tests for threshold-crossing logic across fixture event sequences.
- Definition of Done: engine correctly identifies tier crossings without hardcoded magic numbers.

**Task 03 — Add Repository Methods**
- Objective: `get_companion_evolution_state()`, `advance_tier_if_higher()` (monotonic guard).
- Files to Modify: `src/noorheroes/modules/avatars/repository.py`
- Tests (P0): monotonicity guard test.
- Definition of Done: P0 test passes.

**Task 04 — Integrate into `UnlockEvaluationConsumer`**
- Objective: evaluate tier-crossing alongside item-unlock matching for every consumed event, in the same transaction.
- Files to Modify: `src/noorheroes/modules/avatars/consumers.py` (B-02)
- Tests: atomic-commit test (item unlock + tier advance from one event).
- Do Not Change: do not introduce a second Kafka subscription; reuse B-02's existing consumer loop.
- Definition of Done: single event correctly drives both effects atomically.

**Task 05 — Extend `InventoryResponse` and Add Standalone Endpoint**
- Objective: `companion_evolution` field on B-01's response; new `GET .../companion-evolution` route.
- Files to Modify: `src/noorheroes/modules/avatars/schemas.py`, `api.py` (B-01)
- Tests: integration tests per §27, including the two-read-path consistency test.
- Definition of Done: both response shapes correct and consistent.

**Task 06 — Add Full Test Suite & Documentation**
- Files to Create: `tests/modules/avatars/test_companion_evolution_api.py`, `tests/modules/avatars/test_evolution_tier_monotonicity.py`
- Documentation: OpenAPI + `FAST-API-INSTRUCTIONS.md` update.
- Definition of Done: suite green, docs complete.

**Task 07 — Final Code Review**
- Do Not Change: B-02's core matching logic beyond the additive tier-evaluation call; PostgreSQL credentials.
- Expected Result: PR merge-ready, CI green including the monotonicity P0 gate.

## 30. Definition of Done
Companion evolution tier is persisted, monotonically advanced from the same event stream B-02 already consumes, and exposed both as an `InventoryResponse` field and a standalone endpoint — closing the contract gap K-05 originally flagged as an assumption.

## 31. Final Verification Checklist
- [ ] `ChildCompanionEvolution` model + migration created and reviewed
- [ ] `EvolutionTierRuleEngine` correctly detects threshold crossings from fixture event sequences
- [ ] Monotonic tier guard verified (CI-blocking test passing)
- [ ] Tier evaluation integrated into B-02's existing consumer without a second Kafka subscription
- [ ] Single event correctly advances both item ownership and tier atomically where applicable
- [ ] `GET /v1/children/{id}/inventory` and `GET /v1/children/{id}/companion-evolution` return consistent tier data
- [ ] New child defaults to tier 0, never a null/missing field
- [ ] Unit + integration tests passing
- [ ] OpenAPI documentation complete
- [ ] No PostgreSQL credential changes
- [ ] No unrelated existing-context code modified
