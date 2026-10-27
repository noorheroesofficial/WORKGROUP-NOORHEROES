# K-01 — Shared Rewards Client Module (`:core:rewards-client`)

## 1. Feature Context
Part of Feature A.11 — Rewards System. The foundational KMP module every Rewards-surfacing screen (this feature's own K-02–K-08, plus any feature module displaying wallet/badge data inline) depends on for reading wallet/mission/catalog/family-board state and performing purchases.

## 2. Parent Feature
A.11 Rewards System — KMP App (Android/iOS)

## 3. Sub-feature
K-01 Shared Rewards Client Module (`:core:rewards-client`, Shared Core Module)

## 4. Objective
Stand up `:core:rewards-client` with `WalletRepository`, `MissionsRepository`, `AchievementStoreRepository`, `FamilyBoardRepository`, `AchievementSharingRepository`, mirroring the `:core:mastery-engine`/`:core:quiz-engine` shared-core-module pattern.

## 5. Business Requirements
- Optimistic wallet balance updates always reconciled against the next successful server response, never left permanently optimistic (FR-13).
- No feature module implements a parallel wallet-mutation or ledger-display path — this module is the single source of truth for reading reward state.
- Purchase idempotency key generated once at tap-time, reused on retry.

## 6. Existing Architecture
**Correction to PRD §7:** the PRD's Android AI Code-Generation Prompt describes a generic `RewardRepository.reportCompletion(activityType, reasonId, idempotencyKey)` called by every feature module to report completions client-side. Cross-checking the already-built A7 (Habits) and A10 (Games) KMP blueprints shows the **actual established pattern is backend-orchestrated**: each feature calls its own feature endpoint (e.g., `HabitRepository.checkIn()` → `POST /v1/habits/check-ins`), and that endpoint's backend service calls `RewardService.award_points()` **in-process** (per B-01 §6's Modular-Monolith correction) — the KMP layer never calls a shared "report completion" method directly (A10 K-03 explicitly resolves this exact discrepancy in favor of single-backend-call design, "avoiding duplicate writes," and flags it for architecture-owner confirmation). This module therefore does **not** implement a `reportCompletion()`-style write path. It is the **read-and-purchase client only**: Wallet, Missions/Challenges, Achievement Store (browse + purchase), Family Board, and Achievement Sharing. This is a structural correction to the PRD's illustrative wording, consistent with every other already-built consuming feature's actual integration point — flagged here per governance rule 30 for explicit architecture-owner confirmation before implementation.

Stack (confirmed against `core-*` instruction docs, not the PRD's Android-literal Hilt/Retrofit/Room-Android assumption): Kotlin, Compose Multiplatform, **Koin** DI (`core-common`'s `di` package, `CORE_NAVIGATION_INSTRUCTIONS.md`/`CORE_NETWORK_INSTRUCTIONS.md`/`CORE_DESIGNSYSTEM_INSTRUCTIONS.md` all confirm Koin), **Ktor** networking (`CORE_NETWORK_INSTRUCTIONS.md`), **Room + `BundledSQLiteDriver`** local caching (`CORE_DATABASE_INSTRUCTIONS.md`), `core-navigation`'s `Navigator`/`Route`/`NavigationAction` pattern, `core-analytics`'s `AnalyticsTracker` interface, `kotlinx-datetime`. **Note for governance:** A9/A10's own KMP blueprints assumed Hilt/Retrofit/Android-Room without citing a core-doc source, while A7 K-01 explicitly corrected this against cited `core-common`/`core-network` docs — this module follows the doc-cited (Koin/Ktor/Room-multiplatform) convention as the more verifiably authoritative one, and flags the A9/A10 drift for future harmonization rather than silently perpetuating it.

## 7. Existing Code to Reuse
- `core-common` `di`/`error`/`result`/`datetime` packages, `NoorResult<T>` return-type convention.
- `core-network` Ktor client setup, auth-header interceptor.
- `core-database` Room/`BundledSQLiteDriver` setup.
- `core-navigation` `Navigator`/`Route` pattern.
- `core-analytics` `AnalyticsTracker`.
- `HabitsRewardsRepository.checkInHabit()` — structural precedent for `NoorResult`-returning, sync-queueable repository methods (naming/shape precedent for `AchievementStoreRepository.purchase()`).

## 8. Files to Create
- `core/rewards-client/build.gradle.kts`
- `core/rewards-client/src/commonMain/kotlin/.../data/WalletRepository.kt` (interface + impl)
- `core/rewards-client/src/commonMain/kotlin/.../data/MissionsRepository.kt`
- `core/rewards-client/src/commonMain/kotlin/.../data/AchievementStoreRepository.kt`
- `core/rewards-client/src/commonMain/kotlin/.../data/FamilyBoardRepository.kt`
- `core/rewards-client/src/commonMain/kotlin/.../data/AchievementSharingRepository.kt`
- `core/rewards-client/src/commonMain/kotlin/.../data/dto/WalletDto.kt`, `MissionsDto.kt`, `CatalogItemDto.kt`, `FamilyBoardDto.kt`
- `core/rewards-client/src/commonMain/kotlin/.../data/db/WalletCacheEntity.kt`, `RewardsDao.kt`
- `core/rewards-client/src/commonMain/kotlin/.../di/RewardsClientModule.kt` (Koin module)
- `core/rewards-client/src/commonTest/kotlin/.../data/WalletRepositoryTest.kt`
- `core/rewards-client/src/commonTest/kotlin/.../data/PurchaseIdempotencyKeyTest.kt`
- `core/rewards-client/src/commonTest/kotlin/.../dto/FamilyBoardDtoReflectionTest.kt`

## 9. Files to Modify
- `settings.gradle.kts` — register `:core:rewards-client`.
- App-level Koin module registration — wire `RewardsClientModule`.

## 10. Backend Requirements
Consumes B-02 (`GET /v1/children/{id}/wallet`), B-04 (`GET /v1/children/{id}/achievements`), B-05 (`GET /v1/missions`, `POST /v1/missions/{id}/progress`), B-06 (`GET /v1/catalog-items`, `POST /v1/rewards/claims`), B-07 (`GET /v1/family/{family_id}/board`), B-08 (`POST /v1/achievements/{id}/share-card`).

## 11. KMP Requirements
- `WalletRepository.getWallet(childId): NoorResult<WalletDto>` — remote-first, Room-cached fallback for offline display.
- `AchievementStoreRepository.purchase(itemId, idempotencyKey): NoorResult<ClaimResultDto>` — idempotency key generated once at tap-time (K-07's responsibility to generate; this repository accepts and reuses it, never regenerates internally).
- `FamilyBoardDto` must contain no field capable of holding a per-child breakdown — enforced by a reflection test (mirrors A.7's pattern).
- All repository methods return `NoorResult<T>`, consistent with the project-wide convention.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Per §10; this module must not invent fields beyond those response contracts.

## 14. Database Requirements (Local)
Room: `wallet_cache` (last-synced wallet snapshot per child), `missions_cache`, `catalog_items_cache` — offline/instant-load fallback for read screens; purchases are never cached/queued offline (B-06 requires connectivity).

## 15. Validation
Reflection test enumerating all `FamilyBoardDto` fields, asserting none are collection types containing a nested `childId`/`child_id` field (mandatory, mirrors A.7's structural test pattern).

## 16. Authentication
Reuses `core-network`'s existing Bearer-token attachment interceptor.

## 17. Authorization
N/A at this layer (enforced server-side).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network failure on wallet/missions/catalog read | Serve last-synced Room cache with an offline indicator flag on the DTO |
| Purchase attempted while offline | Rejected client-side before the call is made (connectivity-required action, no outbox queuing) |
| `402 INSUFFICIENT_POINTS` | Mapped to a typed `NoorResult.Error` variant carrying the shortfall amount |

## 19. Offline First
Read paths (wallet/missions/catalog/family board) are offline-tolerant via Room cache; purchase and share-card actions require connectivity by design (B-06 §19, B-08 §19).

## 20. Local Data
```
Remote Data (B-02/B-04/B-05/B-06/B-07)
   ↓
WalletRepository / MissionsRepository / AchievementStoreRepository / FamilyBoardRepository
   ↓
Room wallet_cache / missions_cache / catalog_items_cache
   ↓
ViewModel UI State (K-02–K-08)
```

## 21. Localization
DTOs carry stable keys (`reason_type`, `locale_key`); this module does no localization itself — resolved in the presentation layer (K-03, K-04).

## 22. RTL
N/A at the data layer.

## 23. Analytics
N/A directly; `AnalyticsTracker` calls are fired from the presentation layer (K-02–K-08), tied to this module's confirmed server responses, not optimistic state.

## 24. Performance
Cache reads must not block the UI thread; Ktor calls use the project's existing coroutine-dispatcher conventions.

## 25. Security
No new sensitive data handling; purchase idempotency-key reuse-on-retry is this module's primary integrity property at the client layer.

## 26. Library Requirements
Compose Multiplatform, Koin, Ktor, Room (`BundledSQLiteDriver`), kotlinx-datetime, kotlinx-coroutines, kotlinx-serialization.

## 27. Testing
- Unit: `WalletRepository` cache-fallback logic, purchase idempotency-key reuse-on-retry (mandatory).
- Unit: `FamilyBoardDto` reflection test (mandatory).
- Integration: wallet read → cache write → offline read consistency.

## 28. Documentation
KDoc on `WalletRepository`/`AchievementStoreRepository` explicitly documenting the §6 architectural correction (no client-side `reportCompletion()`; reward issuance is backend-orchestrated per consuming feature), to prevent a future well-intentioned "fix" from reintroducing a duplicate-submission risk.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `:core:rewards-client` Module**
- Objective: establish the shared core module.
- Why Required: no dedicated Rewards read/purchase client exists yet.
- Existing Architecture to Follow: `:core:mastery-engine`/`:core:quiz-engine` module-pair convention.
- Files to Create: `build.gradle.kts`, package skeleton.
- Files to Modify: `settings.gradle.kts`, Koin app-module registration.
- Definition of Done: module compiles, wired into DI graph.

**Task 02 — Implement `WalletRepository`**
- Files to Create: `WalletRepository.kt`, `WalletDto.kt`, `WalletCacheEntity.kt`, `RewardsDao.kt` (wallet portion).
- Implementation Details: Ktor call to B-02, Room-cached fallback.
- Tests: repository unit tests (mocked Ktor client).
- Definition of Done: correct cache-fallback behavior verified.

**Task 03 — Implement `MissionsRepository` & `AchievementStoreRepository`**
- Files to Create: both repositories + DTOs.
- Business Rules: purchase idempotency-key reuse-on-retry (mandatory test).
- Implementation Details: purchase rejected client-side when offline (no outbox).
- Definition of Done: idempotency test passing.

**Task 04 — Implement `FamilyBoardRepository` with Structural DTO Test**
- Files to Create: `FamilyBoardRepository.kt`, `FamilyBoardDto.kt`, reflection test.
- Do Not Change: never add a per-child field to `FamilyBoardDto`.
- Definition of Done: reflection test passing (mandatory CI gate).

**Task 05 — Implement `AchievementSharingRepository`**
- Files to Create: `AchievementSharingRepository.kt`
- Implementation Details: calls B-08, requires elevated parent session token (attached by `core-network`'s existing interceptor based on session state, not reimplemented here).
- Definition of Done: correct call shape verified.

**Task 06 — Documentation & Final Review**
- Documentation: KDoc per §28.
- Do Not Change: do not introduce a generic `reportCompletion()` method into this module.
- Expected Result: PR merge-ready.

## 30. Definition of Done
`:core:rewards-client` live with correct read/cache/purchase behavior, structurally verified Family Board DTO, documented architectural boundary against client-side reward-reporting.

## 31. Final Verification Checklist
- [x] `:core:rewards-client` module compiles and is Koin-wired
- [x] `WalletRepository` cache-fallback verified
- [x] Purchase idempotency-key reuse-on-retry test passes
- [x] `FamilyBoardDto` reflection test passes (no per-child field)
- [x] No `reportCompletion()`-style generic write path exists in this module (documented boundary)
- [x] Purchase/share-card actions correctly blocked when offline
- [x] KDoc explains the §6 architectural correction
