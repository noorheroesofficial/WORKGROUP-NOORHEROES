# Phase 3 — core-datastore: RemoteConfigRepository Bootstrap-Endpoint Integration (Gap Closure)

> **Type:** Gap-Closure Blueprint (not a from-scratch build spec)
> **Module:** `core-datastore` (KMP, Android/iOS) — with additive, coordinated changes to `core-common` and `core-network`
> **Closes:** `RemoteConfigRepository.refresh()` "Phase 0 Status" gap documented in `CORE_DATASTORE_INSTRUCTIONS.md` §4
> **Consumes:** `A1_Splash_Auth_Onboarding` → Backend → **B-01** (`GET /v1/identity/bootstrap`) — existing, already-specified blueprint. **This file does not re-spec B-01.** It specs only the client-side wiring that makes `RemoteConfigRepository.refresh()` actually call it.

---

## 1. Objective and Purpose

### 1.1 What this file is
`core-datastore` is **already fully built**. Per `CORE_DATASTORE_INSTRUCTIONS.md` §4:

> **Phase 0 Status**: `refresh()` currently triggers a local state refresh; future phases will integrate the network bootstrap endpoint.

This is the one remaining gap in an otherwise-complete module: `RemoteConfigRepository` has its full local-cache surface (interface, `Settings`/DataStore-backed implementation, `FeatureFlagDefaults` reconciliation, reactive `Flow` exposure) built and working, but `refresh()` does not talk to the network. It re-derives `FeatureFlagDefaults` from whatever is already sitting in local storage and returns — it never fetches anything new.

This file specs **exactly and only** the wiring needed to make `refresh()` (and the new stale-aware variant introduced here) perform a real network round-trip against B-01's bootstrap endpoint, parse the response, write the cacheable portion through to local storage, and expose the result reactively — while leaving every already-built piece of `core-datastore` untouched.

### 1.2 Why this is sequenced the way it is
This file physically lives in the `Phase3_Shared_Core_Modules` blueprint tree because `RemoteConfigRepository` is a Phase 3 (`core-datastore`) module concern. **However, its execution is gated on Phase 4.** The only backend endpoint this gap can wire against — B-01 (`A1_Splash_Auth_Onboarding` → Backend → `01-bootstrap-remote-configuration-api.md`) — is not built until **Phase 4 (Auth/Onboarding)** per the execution roadmap.

Do not attempt to implement this file until B-01 is live (or, at minimum, `GET /v1/identity/bootstrap` is deployed to a reachable environment with a stable contract — B-01's contract is already frozen and documented, so implementation *can* proceed against a mock/staging instance ahead of full B-01 rollout if the team chooses, but production wiring is not "done" until it talks to the real endpoint).

**Dependency chain for this file:**
```
Phase 3: core-network (built)  ─┐
Phase 3: core-datastore (built, minus this gap) ─┼─▶ THIS FILE ─▶ closes core-datastore to 🟢 COMPLETE
Phase 4: A1 Backend B-01 (not yet built) ────────┘
```
This file cannot reach "Definition of Done" (§17) until B-01 exists. The client-side code in §5–§13 below can be written and unit-tested against a mocked `BootstrapApiService` before B-01 ships; only the final integration/acceptance pass (§14) requires the live endpoint.

### 1.3 What "done" looks like
`RemoteConfigRepository.refresh()` (and its new stale-aware sibling) makes a real `GET /v1/identity/bootstrap` call through `core-network`'s established `safeCall`/Ktor pattern, correctly handles B-01's three-way response shape (200 / 426 / 503-maintenance — all three carry a valid `remote_config` body per B-01 §12), writes only the cacheable `remote_config` sub-object through to `core-datastore`'s existing `PreferenceManager`-backed storage, and leaves the non-cacheable session/routing fields (`session_valid`, `has_children`, `family_id`, version-gate fields, `maintenance_mode`) available in-memory only, per B-01's explicit "never cached" rule. On any network failure, the repository falls back to the last-known-good cached config and never throws away good data because of a bad network call.

---

## 2. Scope and Requirements

### 2.1 In Scope
- Adding a network dependency path from `core-datastore` → `core-network` (new Gradle dependency, new Koin wiring).
- A new, narrowly-scoped `BootstrapApiService` in `core-network` (or reuse, if it already exists — see §12.3) that calls `GET /v1/identity/bootstrap` and returns the full three-way response shape, not just the 200 path.
- `BootstrapResponseDto` / `RemoteConfigPayloadDto` models in `core-network/model/` matching B-01 §12 exactly.
- Making `RemoteConfigRepositoryImpl.refresh()` in `core-datastore` actually invoke `BootstrapApiService`, parse the result, and write-through the cacheable `remote_config` sub-object.
- A new stale-aware entry point (`refreshIfStale()`) implementing the 5-minute client-side TTL policy from B-01 §12 / K-01 §10.
- New, **additive-only** methods/models on the existing `RemoteConfigRepository` interface (in `core-common`) to expose the non-cacheable bootstrap metadata (`session_valid`, `has_children`, `family_id`, version-gate fields, `maintenance_mode`) reactively, without persisting them.
- New `PreferenceConstants` keys for the newly-cached fields and the last-fetch timestamp.
- Koin DI wiring so `composeApp` can inject the fully-wired `RemoteConfigRepository` and trigger `refresh()`/`refreshIfStale()` at the correct lifecycle points.
- Unit tests, including an explicit stale-cache-fallback-on-network-failure test.

### 2.2 Explicitly Out of Scope
- ❌ **Rebuilding `core-datastore`'s existing local-cache / `Settings`-backed storage.** `PreferenceManager`, `DataStoreFactory`, the Android/iOS platform bridges, `FamilyTimezoneStore`, `ClockSkewStore`, `LastObservedTimeZoneStore` are untouched. Do not modify `DataStoreFactory.kt`.
- ❌ **B-01 itself.** The backend endpoint, its schemas, its migration, its rate limiting, its analytics emission — all already fully specified in `Development_Blueprints/A1_Splash_Auth_Onboarding/Backend/01-bootstrap-remote-configuration-api.md`. This file is a pure consumer of that contract.
- ❌ **K-01's UI layer** (`SplashScreen`, `ForcedUpdateScreen`, `MaintenanceModeScreen`, `NoConnectivityScreen`, `SplashViewModel`, `OnboardingGraphInterceptor`, navigation routing matrix). Those belong to `Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/01-splash-bootstrap-update-gating-flow.md` (K-01), which is itself gated on Phase 4. This file stops at the `core-datastore` repository boundary and exposes what K-01 needs to consume — it does not build K-01's screens or view model.
- ❌ **Session/token management.** `RemoteConfigRepositoryImpl` does not read, store, or attach the `Authorization` bearer token itself. That remains `core-network`'s `HttpClient` Auth plugin's job (see §9.2).
- ❌ **Server-side feature-flag expansion.** B-01's `remote_config` payload today contains only `intro_slides_version` and `consent_version` — it does **not** contain `ramadanModeEnabled`/`aiTutorEnabled` (see §6.4 for why, and how this file still reconciles cleanly with the existing `FeatureFlagDefaults` model without inventing backend fields that don't exist yet).
- ❌ **Changing `RemoteConfigRepository`'s existing public method signatures.** See §18.

---

## 3. Technical Implementation Details

### 3.1 The core wiring, end to end
1. `RemoteConfigRepositoryImpl.refresh()` calls `BootstrapApiService.fetchBootstrap(appVersion, platform, locale)`.
2. `BootstrapApiService`'s implementation issues `GET /v1/identity/bootstrap` through the shared `HttpClient` (the same pinned, auth-aware, retry-configured client every other `core-network` call uses — see §9.2), using a **raw-response** call pattern (not the auto-throwing typed pattern) so that 426/503 response bodies remain readable (B-01 explicitly returns the same `BootstrapResponse` shape as `detail` on those two error paths — see §6.3).
3. The raw `HttpResponse` is classified into one of four outcomes:
   - `200` → `BootstrapOutcome.Available(dto)`
   - `426` → `BootstrapOutcome.ForcedUpdateRequired(dto)` (body still parses as `BootstrapResponseDto`)
   - `503` **with a parseable `BootstrapResponseDto` body where `maintenanceMode == true`** → `BootstrapOutcome.MaintenanceActive(dto)`
   - Anything else (network/timeout/connectivity failure, `422`, a `503` that does **not** carry a parseable maintenance body — i.e. B-01 §17's Postgres-hard-fail case) → falls through to `safeCall`'s standard `AppError` mapping, returned as `NoorResult.Failure`.
4. `RemoteConfigRepositoryImpl.refresh()` receives this classified result:
   - On `Available` / `ForcedUpdateRequired` / `MaintenanceActive` — **all three carry a valid `remote_config` object** — it writes `remote_config.intro_slides_version` and `remote_config.consent_version` through to `PreferenceManager`, along with `lastRemoteConfigFetchedAtEpochMillis = Clock.System.now().toEpochMilliseconds()`. It also updates the in-memory-only `bootstrapMetadata` `StateFlow` with the non-cacheable fields. It returns `NoorResult.Success(Unit)`.
   - On a true failure, it does **not** touch local storage at all (no partial writes, no clearing), leaves `bootstrapMetadata` at its previous value, and returns `NoorResult.Failure(error)`.
5. `observeFlags()` (existing, unchanged behavior) continues to reconcile `FeatureFlagDefaults` from whatever is in `PreferenceManager` at read time — it is unaffected by this change because B-01's payload doesn't currently touch the flag keys it reads.
6. A new `observeConfigSnapshot(): Flow<RemoteConfigSnapshot>` exposes the newly-cached `intro_slides_version`/`consent_version` fields plus a computed `isStale: Boolean` (based on the 5-minute TTL, computed at read time against the stored fetch timestamp — not a background timer).
7. A new `observeBootstrapMetadata(): StateFlow<BootstrapMetadata?>` exposes the non-cacheable, in-memory-only session/routing fields for K-01's future `SplashViewModel` to consume for its routing decision matrix — `null` until the first successful `refresh()` of the process lifetime.

### 3.2 Why the raw-response pattern instead of a typed auto-deserializing call
`core-network`'s general `safeCall<T>` wrapper (per `CORE_NETWORK_INSTRUCTIONS.md` §5) maps **non-2xx status codes to `AppError` using the backend `ErrorEnvelopeDto`** — i.e., it assumes error responses are generic error envelopes and discards the body's domain shape. B-01 is a deliberate exception to that generic pattern: its `426` and `503`(maintenance) responses carry the **same `BootstrapResponse` JSON shape** as a `200`, specifically so the client can still render the correct forced-update/maintenance screen with real version numbers (B-01 §12, §17). `BootstrapApiService` must therefore read the raw `HttpResponse`, inspect the status code itself, and attempt to parse the body as `BootstrapResponseDto` regardless of status — falling back to the generic `AppError` mapping only when that parse fails or the status is genuinely a hard failure. This is the one deliberate divergence from the "always use `safeCall`" rule, and it must stay contained inside `BootstrapApiServiceImpl` — everything downstream of it (`RemoteConfigRepositoryImpl`) still deals only in `NoorResult<T>` / `BootstrapOutcome`, never raw `HttpResponse`.

---

## 4. Architecture and Component Responsibilities

```text
composeApp (DI root, lifecycle hooks)
    │  injects RemoteConfigRepository (interface, core-common)
    ▼
core-datastore :: RemoteConfigRepositoryImpl        (MODIFIED — this file)
    │  - orchestrates: call network → classify outcome → write-through cache → update Flows
    │  - owns: FeatureFlagDefaults reconciliation (UNCHANGED), RemoteConfigSnapshot, BootstrapMetadata
    │  - depends on: PreferenceManager (existing), BootstrapApiService (NEW dependency, core-network)
    ▼
core-network :: BootstrapApiService / BootstrapApiServiceImpl   (NEW — this file)
    │  - single responsibility: GET /v1/identity/bootstrap, classify 200/426/503 into BootstrapOutcome
    │  - uses: shared HttpClient (existing), NetworkJson (existing), NetworkErrorMapper (existing)
    ▼
core-network :: HttpClient (existing, UNCHANGED)
    │  - cert pinning, auth-header attachment, retry/backoff — all already built
    ▼
Backend :: GET /v1/identity/bootstrap  (B-01 — Phase 4, not yet built, contract frozen)
```

| Component | Responsibility | Owns Network I/O? | Owns Persistence? | New or Modified |
|---|---|---|---|---|
| `RemoteConfigRepository` (interface, `core-common`) | Public contract feature modules depend on | No | No (abstraction only) | Modified — additive only |
| `RemoteConfigRepositoryImpl` (`core-datastore`) | Orchestration: call → classify → cache → expose | No (delegates) | Yes (via `PreferenceManager`) | Modified |
| `BootstrapApiService` (`core-network`) | HTTP call + response classification for this one endpoint | Yes | No | New |
| `PreferenceManager` (`core-datastore`) | Raw KV storage | No | Yes | Unchanged |
| `HttpClient` (`core-network`) | Transport, auth headers, pinning, retry | Yes | No | Unchanged |
| `composeApp` DI/lifecycle root | Wires Koin graph; triggers `refresh()`/`refreshIfStale()` at launch/foreground | No | No | Modified |

---

## 5. Folder / File Structure

All paths below are relative to each module's `src/commonMain/kotlin/com/noorheroes/...` unless noted. `internal` classes stay `internal`; only interfaces and DTOs meant for cross-module consumption are `public`.

```text
core-common/
└── src/commonMain/kotlin/com/noorheroes/core/common/
    ├── datastore/
    │   └── RemoteConfigRepository.kt              # MODIFY — add new methods (additive)
    ├── model/
    │   ├── FeatureFlagDefaults.kt                  # UNCHANGED
    │   ├── RemoteConfigSnapshot.kt                 # NEW
    │   └── BootstrapMetadata.kt                    # NEW
    └── preferences/
        └── PreferenceConstants.kt                  # MODIFY — add 3 new keys

core-network/
└── src/commonMain/kotlin/com/noorheroes/core/network/
    ├── api/
    │   └── BootstrapApiService.kt                  # NEW — interface + internal Impl
    ├── model/
    │   └── BootstrapDto.kt                         # NEW — BootstrapResponseDto, RemoteConfigPayloadDto
    └── di/
        └── NetworkModule.kt                        # MODIFY — register BootstrapApiService

core-datastore/
└── src/commonMain/kotlin/com/noorheroes/core/datastore/
    ├── store/
    │   ├── RemoteConfigRepositoryImpl.kt           # MODIFY — this is the primary change
    │   └── BootstrapConfigMapper.kt                # NEW, internal — DTO → cache-write / snapshot mapping
    └── di/
        └── DatastoreModule.kt                      # MODIFY — inject BootstrapApiService

core-datastore/build.gradle.kts                     # MODIFY — add core-network dependency

composeApp/
└── src/commonMain/kotlin/com/noorheroes/composeApp/
    └── startup/AppLifecycleObserver.kt              # MODIFY (or CREATE if no existing lifecycle hook) —
                                                       # calls refresh() at cold start, refreshIfStale() on foreground resume

core-datastore/src/commonTest/kotlin/com/noorheroes/core/datastore/store/
└── RemoteConfigRepositoryImplTest.kt                # MODIFY — add network-integration + stale-fallback tests

core-network/src/commonTest/kotlin/com/noorheroes/core/network/api/
└── BootstrapApiServiceTest.kt                       # NEW — DTO round-trip + 200/426/503 classification tests
```

> **Before creating any "NEW" file above, the implementing agent must first search the existing codebase** (`BootstrapDto.kt`, `AuthApiService.bootstrap()`, `BootstrapApiService`) — K-01 (`Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/01-splash-bootstrap-update-gating-flow.md`) independently lists a near-identical `BootstrapDto.kt` and a `bootstrap()` method on `AuthApiService` as *its own* Task 01. **Whichever of these two files lands first in implementation order owns the DTOs and the network call; the second must reuse them, not duplicate them.** See §12.4 for the exact reconciliation rule.

---

## 6. APIs, Models, Interfaces, and Data Flow

### 6.1 Request contract (consumed from B-01 §12, verbatim — do not deviate)
`GET /v1/identity/bootstrap`

| Header | Required | Value |
|---|---|---|
| `Authorization` | No | `Bearer <token>` — attached automatically by `HttpClient`'s existing Auth plugin when a session exists; `BootstrapApiService` never reads/attaches this itself (see §9.2) |
| `X-App-Version` | **Yes** | Semver string, e.g. `4.2.0` — sourced from the platform's app-version provider (see §7.3) |
| `X-Platform` | **Yes** | `android` \| `ios` — sourced from the platform's `expect`/`actual` platform-name provider |
| `X-Locale` | No | BCP-47 tag, e.g. `en-US` — sourced from the currently-persisted locale preference if set, else the OS default locale |

### 6.2 `BootstrapResponseDto` (`core-network/model/BootstrapDto.kt`)

```kotlin
@Serializable
data class BootstrapResponseDto(
    @SerialName("session_valid") val sessionValid: Boolean,
    @SerialName("family_id") val familyId: String? = null,
    @SerialName("has_children") val hasChildren: Boolean,
    @SerialName("min_supported_version") val minSupportedVersion: String,
    @SerialName("recommended_version") val recommendedVersion: String,
    @SerialName("maintenance_mode") val maintenanceMode: Boolean,
    @SerialName("maintenance_estimated_end_at") val maintenanceEstimatedEndAt: String? = null,
    @SerialName("remote_config") val remoteConfig: RemoteConfigPayloadDto,
)

@Serializable
data class RemoteConfigPayloadDto(
    @SerialName("intro_slides_version") val introSlidesVersion: String,
    @SerialName("consent_version") val consentVersion: String,
)
```
Field names and nullability mirror B-01 §12's two documented JSON examples (authenticated and unauthenticated) exactly. `maintenanceEstimatedEndAt` is nullable per B-01 §13's `nullable` column note. Use `core-network`'s shared `NetworkJson` instance (`ignoreUnknownKeys = true`) for parsing — **never** a locally-constructed `Json {}` instance, per `CORE_NETWORK_INSTRUCTIONS.md` §9.

### 6.3 `BootstrapOutcome` (`core-network/api/BootstrapApiService.kt`, internal to the classification step, surfaced to `core-datastore`)

```kotlin
sealed interface BootstrapOutcome {
    data class Available(val response: BootstrapResponseDto) : BootstrapOutcome         // HTTP 200
    data class ForcedUpdateRequired(val response: BootstrapResponseDto) : BootstrapOutcome // HTTP 426
    data class MaintenanceActive(val response: BootstrapResponseDto) : BootstrapOutcome    // HTTP 503 + parseable maintenance body
}
```

### 6.4 `BootstrapApiService` (public interface, `core-network/api/`)

```kotlin
interface BootstrapApiService {
    suspend fun fetchBootstrap(
        appVersion: String,
        platform: String,
        locale: String?,
    ): NoorResult<BootstrapOutcome>
}
```
`NoorResult<BootstrapOutcome>` is `Success(BootstrapOutcome)` for all three body-carrying cases (§6.3) and `Failure(AppError)` only for the genuinely-unrecoverable cases (no connectivity, timeout, `422`, unparseable `503`). This is the exact same `NoorResult<T>` typealias already used everywhere in `core-network` and `core-datastore` — no new result type is introduced.

**Implementation notes for `BootstrapApiServiceImpl` (`internal`):**
- Build the request with `HttpEndpoints`'s existing base-URL resolution (per `CORE_NETWORK_INSTRUCTIONS.md` §13 Do/Don't — never hardcode the path string outside `HttpEndpoints`).
- Issue the call via the shared `HttpClient`, but using `client.get(...) { ... }` directly (returning `HttpResponse`) rather than a typed `body<T>()` call that throws on non-2xx — this is what allows reading the `426`/`503` bodies.
- Classify:
  ```kotlin
  when (response.status.value) {
      200 -> BootstrapOutcome.Available(parseBody(response))
      426 -> BootstrapOutcome.ForcedUpdateRequired(parseBody(response))
      503 -> {
          val parsed = runCatching { parseBody(response) }.getOrNull()
          if (parsed?.maintenanceMode == true) {
              BootstrapOutcome.MaintenanceActive(parsed)
          } else {
              // Postgres-hard-fail case per B-01 §17 — no usable body, treat as a real failure
              return NoorResult.Failure(response.toAppError())
          }
      }
      else -> return NoorResult.Failure(response.toAppError()) // 422, 429, 5xx, etc. — generic ErrorEnvelopeDto path
  }
  ```
- Wrap the whole call in the same `try`/`catch` shape `safeCall` uses internally (catch `IOException`/`TimeoutException`/connectivity exceptions → `Throwable.toTransportAppError()`), since this method deliberately bypasses `safeCall` itself for the reason in §3.2. **Do not swallow `CancellationException`** (per `CORE_NETWORK_INSTRUCTIONS.md` §13).
- `parseBody(response)`: `NetworkJson.decodeFromString<BootstrapResponseDto>(response.bodyAsText())`.

### 6.5 `RemoteConfigSnapshot` (`core-common/model/RemoteConfigSnapshot.kt`, NEW)

```kotlin
data class RemoteConfigSnapshot(
    val introSlidesVersion: String?,
    val consentVersion: String?,
    val fetchedAtEpochMillis: Long?,
    val isStale: Boolean,
)
```
`null` fields mean "no successful bootstrap fetch has ever completed on this device" (first-launch, no-cache case — see §10.3). `isStale` is computed at read time (§8.2), never stored.

### 6.6 `BootstrapMetadata` (`core-common/model/BootstrapMetadata.kt`, NEW)

```kotlin
data class BootstrapMetadata(
    val sessionValid: Boolean,
    val familyId: String?,
    val hasChildren: Boolean,
    val minSupportedVersion: String,
    val recommendedVersion: String,
    val forcedUpdateRequired: Boolean,   // true only when the outcome was ForcedUpdateRequired (426)
    val maintenanceModeActive: Boolean,  // true only when the outcome was MaintenanceActive (503)
    val maintenanceEstimatedEndAt: String?,
    val fetchedAtEpochMillis: Long,
)
```
This is **in-memory only** — see §8.1 and §9.3. It is the shape K-01's future `SplashViewModel` will read for its four-branch routing matrix; this file defines and exposes it but does not build that consumer.

### 6.7 `RemoteConfigRepository` interface changes (`core-common`, additive only)

```kotlin
interface RemoteConfigRepository {
    // ── EXISTING — signatures UNCHANGED, do not touch ──
    fun observeFlags(): Flow<FeatureFlagDefaults>
    suspend fun refresh(): NoorResult<Unit>
    suspend fun saveRemoteValues(values: Map<String, String>): NoorResult<Unit>

    // ── NEW — additive only ──
    fun observeConfigSnapshot(): Flow<RemoteConfigSnapshot>
    fun observeBootstrapMetadata(): StateFlow<BootstrapMetadata?>
    suspend fun refreshIfStale(): NoorResult<Unit>
}
```
> The exact current signatures of the three "EXISTING" members above are asserted from `CORE_DATASTORE_INSTRUCTIONS.md` §4/§11 (Quick Reference Table: `RemoteConfigRepository | Feature Flags | Yes (Flow) | Yes (refresh)`) and are the most likely shape given `NoorResult<T>` is documented as "used for suspending operations like `refresh()`." **Before editing, the implementing agent must open the actual current `RemoteConfigRepository.kt` and `RemoteConfigRepositoryImpl.kt` and confirm the live signatures.** If they differ from the above, keep them exactly as found and add the three new members alongside — never rename or change the parameter/return shape of anything already there. See §18.

### 6.8 Data flow diagram

```text
composeApp launch
    │
    ▼
RemoteConfigRepository.refresh()  ──────────────────────────────────┐
    │                                                                │
    ▼                                                                │ (existing, unchanged)
BootstrapApiService.fetchBootstrap(appVersion, platform, locale)     │
    │                                                                │
    ├─ Success(Available/ForcedUpdateRequired/MaintenanceActive) ────┤
    │       │                                                        │
    │       ├─▶ PreferenceManager.setString(KEY_INTRO_SLIDES_VERSION, dto.remoteConfig.introSlidesVersion)
    │       ├─▶ PreferenceManager.setString(KEY_CONSENT_VERSION, dto.remoteConfig.consentVersion)
    │       ├─▶ PreferenceManager.setLong(KEY_REMOTE_CONFIG_LAST_FETCHED_AT, nowEpochMillis)
    │       ├─▶ bootstrapMetadataStateFlow.value = BootstrapMetadata(...)   [in-memory only]
    │       └─▶ return NoorResult.Success(Unit)
    │
    └─ Failure(AppError) ─▶ leave PreferenceManager & bootstrapMetadataStateFlow untouched
                             └─▶ return NoorResult.Failure(error)

observeFlags()          ◀── reads PreferenceManager (existing keys) ── UNCHANGED
observeConfigSnapshot() ◀── reads KEY_INTRO_SLIDES_VERSION / KEY_CONSENT_VERSION / KEY_REMOTE_CONFIG_LAST_FETCHED_AT, computes isStale
observeBootstrapMetadata() ◀── reads bootstrapMetadataStateFlow (in-memory)
```

---

## 7. Dependencies and Configuration Requirements

### 7.1 New Gradle dependency
`core-datastore/build.gradle.kts` — add to `commonMain.dependencies`:
```kotlin
implementation(project(":core-network"))
```
This is a **new, deliberate cross-module edge**: previously `core-datastore` had no dependency on `core-network`. Confirm this does not create a circular dependency (`core-network` must not depend on `core-datastore` anywhere in its `build.gradle.kts` — per `CORE_NETWORK_INSTRUCTIONS.md` §2's layering diagram, `core-network` sits below `core-data`/features and has no reason to depend on `core-datastore`, so this should be safe, but verify before proceeding).

### 7.2 Koin wiring
`core-datastore/di/DatastoreModule.kt` — `RemoteConfigRepositoryImpl`'s constructor gains a `Lazy<BootstrapApiService>` parameter (per the module's existing "Lazy DI" rule, `CORE_DATASTORE_INSTRUCTIONS.md` §9), resolved from `core-network`'s Koin module:
```kotlin
single<RemoteConfigRepository> {
    RemoteConfigRepositoryImpl(
        preferenceManager = get(),
        bootstrapApiService = get(), // resolved from core-network's module
    )
}
```
`composeApp`'s `startKoin { modules(...) }` call must include both `networkModule` and `datastoreModule` in its module list (Koin resolves lazily across modules regardless of list order, but both must be present — confirm `networkModule` is already registered there today; if not, add it as part of this change).

### 7.3 App-version / platform / locale providers
`BootstrapApiService.fetchBootstrap()` needs three values the caller (`RemoteConfigRepositoryImpl`) must supply:
- **App version**: reuse whatever existing `expect`/`actual` app-version provider already exists in `core-common` (commonly named `AppVersionProvider` or similar in KMP projects of this shape). **Search for it before creating one.** If genuinely absent, create a minimal `expect fun currentAppVersion(): String` / `actual` pair in `core-common` (Android: `BuildConfig.VERSION_NAME`; iOS: `NSBundle.mainBundle.infoDictionary["CFBundleShortVersionString"]`) — this is the one small platform primitive this file is allowed to introduce if it's missing, since without it the required `X-App-Version` header cannot be built at all.
- **Platform**: same pattern — reuse an existing `expect fun currentPlatformName(): String` returning `"android"`/`"ios"` if one exists; create the minimal `expect`/`actual` pair if not.
- **Locale**: read the currently-persisted locale preference via `PreferenceManager` if a locale key already exists in `PreferenceConstants` (pre-onboarding, this will usually be unset); fall back to the platform's OS-default locale tag if unset. Do not block `refresh()` waiting on a user-set locale — `X-Locale` is optional per B-01 §12.

### 7.4 No new third-party libraries
This file introduces zero new external dependencies. It exclusively composes existing `core-network` infrastructure (`HttpClient`, `NetworkJson`, `HttpEndpoints`, `AppError`/`NoorResult`) with existing `core-datastore` infrastructure (`PreferenceManager`). `kotlinx.datetime.Clock` (already a transitive dependency via existing `ClockSkewStore` usage) is reused for the fetch timestamp — do not add `java.time`/`NSDate` platform-specific timestamp code.

---

## 8. Database / Storage Requirements

`core-datastore` has no SQL database — this section covers the DataStore/`PreferenceManager` storage contract for the newly-cached fields.

### 8.1 What gets persisted vs. what stays in-memory
| Field | Persisted? | Storage | TTL |
|---|---|---|---|
| `remote_config.intro_slides_version` | **Yes** | `PreferenceManager` (String) | 5 min soft TTL (§8.2) |
| `remote_config.consent_version` | **Yes** | `PreferenceManager` (String) | 5 min soft TTL (§8.2) |
| Fetch timestamp | **Yes** | `PreferenceManager` (Long, epoch millis) | N/A (used to compute staleness) |
| `session_valid` | **No — never** | In-memory `StateFlow` only | Cleared on process death |
| `family_id` | **No — never** | In-memory `StateFlow` only | Cleared on process death |
| `has_children` | **No — never** | In-memory `StateFlow` only | Cleared on process death |
| `min_supported_version` / `recommended_version` / `maintenance_mode` / `maintenance_estimated_end_at` | **No — never** | In-memory `StateFlow` only | Cleared on process death |

This split is a direct, literal implementation of B-01 §12's caching rule ("`remote_config` object is safe for the client to cache 5 minutes client-side. `session_valid`/`has_children` must never be cached by the client") extended consistently to the sibling top-level fields (`family_id`, version-gate fields, `maintenance_mode`) that carry the same per-launch, must-be-fresh character — see §19 for this as an explicit stated assumption.

### 8.2 Staleness / TTL policy
- **TTL constant**: `REMOTE_CONFIG_TTL_MILLIS = 5 * 60 * 1000L` (5 minutes, matching B-01 §12 and K-01 §10 exactly). Define this as a `private const val` inside `RemoteConfigRepositoryImpl` — it is an implementation detail, not something callers configure.
- **Computation**: `isStale = (Clock.System.now().toEpochMilliseconds() - fetchedAtEpochMillis) > REMOTE_CONFIG_TTL_MILLIS`, computed fresh on every collection of `observeConfigSnapshot()` — **not** a background timer/alarm. No cache-eviction job is needed; stale data simply stays in storage until the next successful `refresh()` overwrites it.
- **`refresh()`**: always performs the network call, unconditionally, regardless of staleness. This is the "force" entry point — K-01's cold-launch Splash call and any manual "Retry" action must use this.
- **`refreshIfStale()`**: checks `isStale` first (reading the stored timestamp via `PreferenceManager`, no network call needed for the check itself); if not stale, returns `NoorResult.Success(Unit)` immediately without any network I/O; if stale (or no timestamp exists yet — first launch), delegates to `refresh()`. This is the entry point for foreground-resume (§11).

### 8.3 New `PreferenceConstants` keys
```kotlin
// core-common/preferences/PreferenceConstants.kt — ADD, do not renumber/reorder existing keys
const val KEY_REMOTE_CONFIG_INTRO_SLIDES_VERSION = "remote_config_intro_slides_version"
const val KEY_REMOTE_CONFIG_CONSENT_VERSION = "remote_config_consent_version"
const val KEY_REMOTE_CONFIG_LAST_FETCHED_AT = "remote_config_last_fetched_at_epoch_millis"
```
Per `CORE_DATASTORE_INSTRUCTIONS.md` §9, every DataStore key **must** go through `PreferenceConstants` — never a raw string literal in `RemoteConfigRepositoryImpl`.

### 8.4 Atomicity
Both new string writes plus the timestamp write happen inside a single `PreferenceManager` atomic write path if the existing implementation exposes a multi-key transactional `edit` helper (check `PreferenceManagerImpl` for an existing `editMultiple`/batch method before adding a new one). If no batch-write helper exists today, three sequential `suspend` writes are acceptable **but must all complete before `refresh()` returns success** — a failure partway through (e.g., process death) should leave the previous complete triple in place rather than a mixed old/new state; do not update the timestamp key until after both value keys have written successfully, so a partial failure is detected as "still using the old, complete config" rather than "stale timestamp lies about freshness."

---

## 9. Authentication, Authorization, Validation, and Security Considerations

### 9.1 Endpoint is intentionally public/optional-auth
B-01 §15: "No RBAC scope required — this is a public, pre-auth-safe endpoint by design." `BootstrapApiService` calls it exactly as documented — no auth requirement is enforced client-side, and a missing/expired token must not prevent the call from succeeding (B-01 §17: expired/invalid token → `session_valid: false`, HTTP 200, never 401).

### 9.2 Token attachment stays out of `core-datastore`
`RemoteConfigRepositoryImpl` and `BootstrapApiService` never read or attach the bearer token themselves. The shared `HttpClient` already auto-attaches `Authorization: Bearer <token>` when a valid session exists (`CORE_NETWORK_INSTRUCTIONS.md` §5: "Auth: Automatic token refresh on 401"), via whatever `core-security`-backed Ktor `Auth` plugin configuration already exists on the client. This keeps `core-datastore` free of any dependency on `core-security`, consistent with its own "What NOT to Add Here: Sensitive Data" rule. If `HttpClient`'s current Auth plugin only attaches tokens for calls that require auth (as opposed to optional-auth calls like this one), confirm during implementation that an unauthenticated call to this endpoint still succeeds (it must — B-01 explicitly supports a zero-session call) and that a present token is still attached when available. **Do not build a second, parallel token-attachment path inside `BootstrapApiServiceImpl` to work around this** — fix it at the `HttpClient` config level if needed, since that is a shared concern, not specific to this endpoint.

### 9.3 In-memory-only session fields are a security-relevant decision, not just a caching one
Per §8.1, `session_valid`/`family_id`/`has_children` are never written to `PreferenceManager`. This is intentional and must not be "optimized away" by an implementer who notices the pattern and decides to persist them for offline convenience — persisting `family_id` client-side unencrypted in a general-purpose KV store would create a data-exposure surface B-01's own design explicitly avoids (§21: "Bootstrap must not leak whether a `family_id` exists for a given token beyond what the token's own claims already authorize"). Keeping it in-memory-only, cleared on process death, is the correct and required behavior.

### 9.4 Response validation
`BootstrapResponseDto` parsing uses `NetworkJson` with `ignoreUnknownKeys = true` (forward compatibility, per `CORE_NETWORK_INSTRUCTIONS.md` §9) but does **not** relax required-field enforcement — if `remoteConfig`, `sessionValid`, `hasChildren`, `minSupportedVersion`, `recommendedVersion`, or `maintenanceMode` are absent or the wrong type, `kotlinx.serialization` throws a `SerializationException` on decode, which must be caught and mapped to `NoorResult.Failure(AppError.Validation(...))` inside `BootstrapApiServiceImpl` (do not let this propagate as an unhandled crash — see §10.2).

### 9.5 No secrets, no PII logging
Do not log the raw response body, the `family_id`, or any header value beyond what `core-network`'s existing header-redaction logging already permits (`CORE_NETWORK_INSTRUCTIONS.md` §5: "Redaction: Sensitive headers are automatically removed from logs"). Log at most: outcome type (`Available`/`ForcedUpdateRequired`/`MaintenanceActive`/failure), HTTP status, and latency — via `NoorHeroesLogger`, never `println` (per `CORE_NETWORK_INSTRUCTIONS.md` §13).

---

## 10. Error Handling and Edge Cases

| Scenario | Behavior |
|---|---|
| **Network failure** (no connectivity, timeout, DNS failure) | `BootstrapApiService` returns `NoorResult.Failure(AppError.Network.*)`. `RemoteConfigRepositoryImpl.refresh()` propagates the same `Failure`, touches **zero** local storage, leaves `bootstrapMetadata` StateFlow at its previous value. `observeFlags()`/`observeConfigSnapshot()` keep emitting the last-known-good cached values already on disk. |
| **Malformed / unparseable response body** (unexpected shape, missing required field on a `200`) | Caught inside `BootstrapApiServiceImpl` as a `SerializationException`, mapped to `NoorResult.Failure(AppError.Validation(...))`. Treated identically to a network failure by `RemoteConfigRepositoryImpl` — no partial cache write, stale-cache fallback applies. |
| **First launch, no cache exists yet, network call also fails** | `observeConfigSnapshot()` emits `RemoteConfigSnapshot(introSlidesVersion = null, consentVersion = null, fetchedAtEpochMillis = null, isStale = true)`. `observeFlags()` emits `FeatureFlagDefaults` with `source = BUILD_DEFAULT_FALLBACK` (existing, unchanged behavior — this already works today because it doesn't depend on network data). `observeBootstrapMetadata()` emits `null`. Callers (future K-01 `SplashViewModel`) must treat a `null` snapshot/metadata as "no data yet," not as an error state requiring a full-screen error — that UI decision belongs to K-01, not this file. |
| **First launch, no cache exists yet, network call succeeds** | Full write-through happens exactly per §3.1/§8; `isStale` is `false` immediately after. |
| **HTTP `426` (forced update required)** | Classified as `BootstrapOutcome.ForcedUpdateRequired` — **not** treated as a failure. `remote_config` from the body is still cached (B-01 guarantees it's present). `refresh()` returns `Success(Unit)`. The "this requires blocking the user" decision is surfaced via `observeBootstrapMetadata().forcedUpdateRequired = true`, for K-01 to act on — this file does not render any UI. |
| **HTTP `503` with `maintenance_mode: true` in a parseable body** | Classified as `BootstrapOutcome.MaintenanceActive` — **not** treated as a failure, same write-through as above. `observeBootstrapMetadata().maintenanceModeActive = true`. |
| **HTTP `503` with no parseable body / not a maintenance response** (B-01 §17's Postgres-hard-fail case) | Treated as a genuine `NoorResult.Failure` — this is the "client shows No-Connectivity/retry" case B-01 itself designates as the one true hard-fail. Stale-cache fallback applies exactly as the network-failure row above. |
| **HTTP `422`** (malformed `X-App-Version`/`X-Platform` sent by the client) | This indicates a **client bug** (missing/malformed header construction), not a transient condition — `NoorResult.Failure(AppError.Validation(...))`. Should not occur in correctly-implemented code (§7.3 ensures both required headers are always populated), but must not crash if it does. |
| **HTTP `429`** (rate limited — 60/min/IP per B-01 §12) | Falls through to the generic `else` branch in §6.4's classification, mapped to `AppError` by the existing `HttpResponse.toAppError()` extension. `refresh()` returns `Failure`; stale-cache fallback applies. This should be exceedingly rare for a single device's own launch cadence. |
| **`refresh()` called concurrently from two call sites** (e.g., cold-launch call and a foreground-resume race) | `RemoteConfigRepositoryImpl` must not issue two overlapping network calls. Use an internal `Mutex` (or a shared in-flight `Deferred<NoorResult<Unit>>` that concurrent callers await rather than re-triggering) so a second caller during an in-flight `refresh()` awaits the same result rather than firing a duplicate request. |
| **App killed mid-write** (process death between the two value writes and the timestamp write) | Per §8.4's write ordering, the timestamp is written last — so a mid-write kill leaves the timestamp reflecting the *previous* successful fetch (or absent, on first-ever fetch), which correctly reads as "still need to refresh," never as a false freshness signal. |

---

## 11. State Management and Lifecycle Considerations

`refresh()`/`refreshIfStale()` are triggered from exactly three call sites, none of which are built by this file (they live in `composeApp`'s startup wiring and, eventually, K-01) — this file's job is to make sure both entry points are correct and safe to call from any of them:

1. **App launch (cold start)** — the future K-01 `SplashViewModel` calls `refresh()` (forced, not `refreshIfStale()`) unconditionally, because `session_valid`/`has_children`/version-gate data must always be current at launch regardless of the `remote_config` TTL. This file's contract must support that call working correctly with zero prior state (§10, first-launch rows).
2. **Foreground resume** — `composeApp`'s lifecycle observer (`AppLifecycleObserver.kt`, §5) calls `refreshIfStale()` on `ON_START`/`onResume` (platform lifecycle hook — Android `ProcessLifecycleOwner`, iOS `applicationDidBecomeActive`), so a backgrounded-then-resumed app picks up new config without a full re-launch, but without hammering the network on every quick app-switch (the 5-minute TTL guard in `refreshIfStale()` handles this).
3. **Manual pull** — any future "Retry" control (e.g., on a No-Connectivity screen) calls `refresh()` (forced), never `refreshIfStale()`, since a user-initiated retry should always attempt a real network call regardless of TTL.

`RemoteConfigRepositoryImpl` itself holds no lifecycle awareness — it exposes `refresh()`/`refreshIfStale()` as plain `suspend` functions and lets callers decide when to invoke them, consistent with `core-datastore`'s existing architectural boundary ("Keep this module strictly about the *how* of data access," §1 of `CORE_DATASTORE_INSTRUCTIONS.md`). The `bootstrapMetadata` `StateFlow` is scoped to the repository singleton's lifetime (i.e., the process lifetime, since it's a Koin `single`) — it is deliberately **not** persisted across process death (§9.3), so a fresh cold start always starts with `observeBootstrapMetadata()` emitting `null` until the launch-time `refresh()` completes.

---

## 12. Integration Points with Existing Modules

### 12.1 `core-network`
- Reuses the shared `HttpClient` singleton (cert pinning, retry/backoff, `RequestIdPlugin`/`IdempotencyKeyPlugin`/`ServerTimePlugin`) — `BootstrapApiService` must be constructed with the same injected `HttpClient` every other `core-network` API service uses, never a second client instance.
- Reuses `NetworkJson`, `HttpEndpoints`, `NetworkErrorMapper`/`HttpResponse.toAppError()`, `Throwable.toTransportAppError()` — all existing, unmodified.
- New DI registration in `core-network/di/NetworkModule.kt`:
  ```kotlin
  single<BootstrapApiService> { BootstrapApiServiceImpl(client = get()) }
  ```

### 12.2 `composeApp`
- New/modified `startup/AppLifecycleObserver.kt` wires the two trigger points from §11. If `composeApp` already has an equivalent app-lifecycle observer for other purposes (likely, given `ConnectivityObserver` and other reactive singletons already exist per `core-network`'s doc), **extend it** rather than adding a second, competing lifecycle listener.
- `composeApp`'s Koin `startKoin { modules(...) }` call must include both `networkModule` and `datastoreModule` (§7.2).

### 12.3 `core-common`
- `RemoteConfigRepository` interface, `RemoteConfigSnapshot`, `BootstrapMetadata`, `PreferenceConstants` all live here and are the only `core-common` files this change touches.

### 12.4 Reconciling with K-01 (Phase 4, not yet built)
K-01's own blueprint (`Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/01-splash-bootstrap-update-gating-flow.md`) independently lists, as its own Task 01/Task 03: adding `bootstrap()` to `AuthApiService` plus DTOs, and a feature-level `BootstrapRepository` that calls it and writes to `RemoteConfigRepository`'s cache. **This file supersedes that specific piece of K-01's plan** to avoid two independent client-side implementations of the same network call:
- This file's `BootstrapApiService` + `BootstrapDto.kt` **are** the DTOs/network method K-01's Task 01 would otherwise create. When K-01 is implemented, its Task 01 is satisfied by confirming these already exist (skip re-creating them).
- This file's `RemoteConfigRepository.refresh()` **is** the cache-write step K-01's Task 03 (`BootstrapRepository`) would otherwise perform. When K-01 is implemented, its `BootstrapRepository`/`SplashViewModel` should call `RemoteConfigRepository.refresh()` directly (for the routing-critical, always-fresh cold-launch call) and read `observeBootstrapMetadata()` for the four-branch routing matrix (session_valid/has_children) — it should **not** independently call `AuthApiService.bootstrap()` a second time. If K-01's implementer still wants a thin `BootstrapRepository` façade purely for feature-module ergonomics, that façade should delegate to `RemoteConfigRepository`, not duplicate the HTTP call.
- If, at the time K-01 is implemented, this file has not yet been implemented (unlikely given the stated phase ordering, but possible if execution order slips), K-01's implementer should implement this file's contract first (or inline-equivalent) rather than building a parallel, disconnected `BootstrapRepository` — the whole point of this gap-closure is that `RemoteConfigRepository` is the **one** place bootstrap data enters the client.

---

## 13. Development Steps in Correct Implementation Order

1. **Confirm B-01 is reachable** (deployed to at least a staging environment with the frozen contract from `01-bootstrap-remote-configuration-api.md`) or set up a local mock server matching the exact contract for early development.
2. **Read the actual current source** of `RemoteConfigRepository.kt` (`core-common`) and `RemoteConfigRepositoryImpl.kt` (`core-datastore`) to confirm existing method signatures before writing any code (§6.7, §18).
3. **`core-network`**: create `model/BootstrapDto.kt` (§6.2) — or confirm it already exists from a prior K-01 partial implementation (§12.4) and reuse it.
4. **`core-network`**: create `api/BootstrapApiService.kt` (interface + `internal` `BootstrapApiServiceImpl`) (§6.3, §6.4) with the 200/426/503 classification logic (§3.2).
5. **`core-network`**: write `BootstrapApiServiceTest.kt` — DTO round-trip against B-01's two documented JSON examples, plus classification tests for 200/426/503-maintenance/503-hard-fail/422/network-failure.
6. **`core-network`**: register `BootstrapApiService` in `NetworkModule.kt` (§12.1).
7. **`core-common`**: add `RemoteConfigSnapshot.kt`, `BootstrapMetadata.kt` (§6.5, §6.6); add the three new `PreferenceConstants` keys (§8.3); add the three new methods to the `RemoteConfigRepository` interface, **appended after the existing members, unchanged** (§6.7).
8. **`core-datastore`**: add `implementation(project(":core-network"))` to `build.gradle.kts` (§7.1); verify no circular dependency results.
9. **`core-datastore`**: create `store/BootstrapConfigMapper.kt` (`internal`) — pure functions mapping `BootstrapOutcome`/`BootstrapResponseDto` → the cache-write triple and → `BootstrapMetadata`, kept separate from `RemoteConfigRepositoryImpl` for testability.
10. **`core-datastore`**: modify `RemoteConfigRepositoryImpl.kt` — inject `Lazy<BootstrapApiService>`; implement the new `refresh()` body (§3.1); add `refreshIfStale()`, `observeConfigSnapshot()`, `observeBootstrapMetadata()`; add the in-flight-call `Mutex` guard (§10, concurrent-call row).
11. **`core-datastore`**: wire the app-version/platform/locale providers (§7.3), creating the minimal `expect`/`actual` pair only if genuinely not already present elsewhere.
12. **`core-datastore`**: update `di/DatastoreModule.kt` to inject `BootstrapApiService` into `RemoteConfigRepositoryImpl` (§7.2).
13. **`core-datastore`**: write/extend `RemoteConfigRepositoryImplTest.kt` — full success path, all three `BootstrapOutcome` variants write-through correctly, network-failure stale-cache-fallback test (§14.2), first-launch-no-cache test, concurrent-refresh-dedup test.
14. **`composeApp`**: wire `AppLifecycleObserver.kt` for the foreground-resume `refreshIfStale()` trigger (§11, §12.2); confirm Koin module registration includes both `networkModule` and `datastoreModule`.
15. **Manual verification**: run the app against the staging B-01 endpoint; confirm a cold launch populates `observeConfigSnapshot()`/`observeBootstrapMetadata()` correctly for both an authenticated and unauthenticated session; confirm airplane-mode launch falls back to whatever was last cached (or `BUILD_DEFAULT_FALLBACK`/null on a truly fresh install).
16. **Final review against §18's "do not break" constraint** and the checklist in §17.

---

## 14. Testing Strategy and Acceptance Criteria

### 14.1 Unit tests — `BootstrapApiServiceTest.kt` (`core-network`)
- DTO deserializes correctly against B-01 §12's exact authenticated JSON example.
- DTO deserializes correctly against B-01 §12's exact unauthenticated JSON example.
- HTTP `200` → `BootstrapOutcome.Available`.
- HTTP `426` with a valid body → `BootstrapOutcome.ForcedUpdateRequired`, body fields intact.
- HTTP `503` with `maintenance_mode: true` and a valid body → `BootstrapOutcome.MaintenanceActive`.
- HTTP `503` with an unparseable/non-matching body → `NoorResult.Failure`, not a crash.
- HTTP `422` → `NoorResult.Failure(AppError.Validation)`.
- Simulated `IOException`/timeout → `NoorResult.Failure(AppError.Network.*)`.
- Malformed JSON on a `200` → `NoorResult.Failure`, not an unhandled `SerializationException`.

### 14.2 Unit tests — `RemoteConfigRepositoryImplTest.kt` (`core-datastore`) — **required, including the explicit stale-cache-fallback proof**
- **`refresh()` success path**: mock `BootstrapApiService` returns `Success(Available(dto))`; assert `PreferenceManager` now holds both new string values and an updated timestamp; assert `observeConfigSnapshot()` emits the new values with `isStale = false`; assert `observeBootstrapMetadata()` emits the correct `BootstrapMetadata`.
- **`refresh()` write-through on 426/503-maintenance**: same as above but via `ForcedUpdateRequired`/`MaintenanceActive` outcomes — confirm cache still updates (§10 table) and `forcedUpdateRequired`/`maintenanceModeActive` flags are set correctly on the metadata.
- **★ Stale-cache fallback on network failure (required acceptance test)**:
  1. Seed `PreferenceManager` directly (bypassing the network path) with a known-good `intro_slides_version`/`consent_version`/timestamp — simulating a prior successful fetch.
  2. Configure the mock `BootstrapApiService` to return `NoorResult.Failure(AppError.Network.NoConnectivity)`.
  3. Call `refresh()`.
  4. Assert the return value is `NoorResult.Failure`.
  5. Assert `observeConfigSnapshot()` **still emits the seeded values from step 1, unchanged** — the network failure must not have cleared or corrupted the cache.
  6. Assert `observeBootstrapMetadata()` remains at whatever it was before the failed call (its pre-test value, e.g. `null` if no prior successful `refresh()` in this test run).
  This test is the concrete proof that "network failure falls back to last-known-good cached config" (§10) actually holds, not just that it's documented.
- **First-launch, no cache, network failure**: empty `PreferenceManager`, mock returns `Failure`; assert `observeConfigSnapshot()` emits `RemoteConfigSnapshot(null, null, null, isStale = true)`; assert `observeFlags()` still emits `FeatureFlagDefaults(source = BUILD_DEFAULT_FALLBACK)` (proving the pre-existing flag-reconciliation path is unaffected by this change).
- **`refreshIfStale()` short-circuits within TTL**: seed a fetch timestamp 1 minute old; call `refreshIfStale()`; assert `BootstrapApiService.fetchBootstrap()` was **never invoked** (mock verify zero interactions); assert the call returns `NoorResult.Success(Unit)`.
- **`refreshIfStale()` delegates when stale**: seed a fetch timestamp 6 minutes old; call `refreshIfStale()`; assert `fetchBootstrap()` **was** invoked exactly once.
- **`refreshIfStale()` on first launch (no timestamp at all)**: treated as stale; assert it delegates to a real fetch attempt.
- **Concurrent `refresh()` calls are deduplicated**: launch two concurrent `refresh()` calls; assert `fetchBootstrap()` was invoked exactly once (Mutex/in-flight-`Deferred` guard from §10 works).
- **`observeFlags()` regression test**: with this change fully applied, confirm `observeFlags()`'s existing reconciliation behavior (remote override vs. `BUILD_DEFAULT_FALLBACK`) is byte-for-byte unchanged from before this file's implementation — run whatever test suite already exists for it and confirm it still passes untouched.

### 14.3 Acceptance criteria (summary)
- [ ] `refresh()` performs a real network call against B-01's contract (verified against a live/staging endpoint, not just mocks, at least once before sign-off).
- [ ] All three body-carrying outcomes (200/426/503-maintenance) correctly write-through `remote_config` to cache.
- [ ] `session_valid`/`family_id`/`has_children`/version-gate/`maintenance_mode` fields are never found in `PreferenceManager` storage after any test run (grep the test DataStore file/in-memory test double for these key names — must be absent).
- [ ] Network failure leaves previously-cached values fully intact (§14.2's required test, green).
- [ ] First-launch-no-cache-no-network path degrades gracefully with no crash and `BUILD_DEFAULT_FALLBACK`/null semantics.
- [ ] `refreshIfStale()` correctly respects the 5-minute TTL.
- [ ] No duplicate concurrent network calls.
- [ ] All pre-existing `core-datastore` tests (unrelated to this change) remain green, unmodified.

---

## 15. Production-Readiness Considerations

- **Timeout alignment**: `BootstrapApiService` uses the shared `HttpClient`'s existing configured timeout — do not set a bespoke, shorter timeout for this one endpoint just because K-01's Splash screen has a 2.5s display cap; that display-cap race belongs entirely in K-01's `SplashViewModel` (per K-01 §10: "the actual bootstrap call continues in the background regardless, never cancelled by the timeout"), not in this repository/service layer. `RemoteConfigRepositoryImpl.refresh()` must not itself impose a 2.5s cutoff.
- **Backoff/retry**: rely on `HttpClient`'s existing exponential-backoff retry plugin (`CORE_NETWORK_INSTRUCTIONS.md` §4) rather than adding a second, bespoke retry loop inside `BootstrapApiServiceImpl`.
- **Cold-start performance**: `RemoteConfigRepositoryImpl`'s constructor must not perform any network or DataStore I/O eagerly — all dependencies stay `Lazy<T>` (existing rule, §9 of `CORE_DATASTORE_INSTRUCTIONS.md`), and `refresh()` is only ever invoked explicitly by a caller, never from an `init` block.
- **Telemetry**: emit a lightweight internal log/metric (via `NoorHeroesLogger`, not analytics — analytics for this event is B-01's own server-side `bootstrap_completed`/`bootstrap_failed`, K-01 §16 explicitly forbids double-emitting client-side) for `refresh()` latency and outcome type, useful for debugging cache-staleness issues in production without duplicating the backend's analytics.
- **Backward compatibility of the cache format**: if a future app version changes what's stored under `KEY_REMOTE_CONFIG_INTRO_SLIDES_VERSION`, ensure `PreferenceManager`'s existing `getStringOrNull` + `runCatching` deserialization pattern (§9 of `CORE_DATASTORE_INSTRUCTIONS.md`, Scenario 2) is followed so an old cached value never crashes a newer app build — string fields here have no complex parsing, so this is low-risk, but keep the pattern consistent with the rest of the module.
- **Kill-switch safety**: because `remote_config` write-through happens even on 426/503, a prolonged backend maintenance window does not cause the client's cached `intro_slides_version`/`consent_version` to go stale in a way that matters — those values are still delivered and cached even while maintenance mode is active, which is correct (they're config values, not the maintenance status itself).

---

## 16. Dependencies / Prerequisites

- **Hard blocker**: Phase 4 A1 Backend **B-01** (`GET /v1/identity/bootstrap`) must be deployed and contract-stable before this file's acceptance testing (§14.3) can complete. Development against a mock matching B-01's frozen contract can start earlier.
- **Soft dependency**: `core-network` module (already built — no changes needed to its foundational pieces, only additive files within it).
- **Soft dependency**: `core-datastore` module (already built — this file's entire purpose is closing its one remaining gap).
- **Coordination dependency**: K-01 (`Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/01-splash-bootstrap-update-gating-flow.md`) — not a blocker for *this* file, but §12.4 must be followed when K-01 is implemented to avoid duplicate network wiring.
- No new third-party libraries, no new backend work, no new database work (this file's storage changes are three `PreferenceManager` keys only).

---

## 17. Definition of Done

- [ ] `RemoteConfigRepository.refresh()` performs a real `GET /v1/identity/bootstrap` call and no longer only re-derives state from existing local storage.
- [ ] All 19 sections of this file's requirements are implemented as specified (or, where the actual current source differed from this file's inferred signatures per §6.7, reconciled correctly without breaking existing callers).
- [ ] `refreshIfStale()`, `observeConfigSnapshot()`, `observeBootstrapMetadata()` exist, are additive, and function per §6.7/§8.
- [ ] The stale-cache-fallback test (§14.2 ★) is present and green.
- [ ] `observeFlags()`'s pre-existing behavior is provably unchanged (regression test green, §14.2).
- [ ] `session_valid`/`family_id`/`has_children`/version-gate/`maintenance_mode` are never persisted (verified by test, §14.3).
- [ ] `core-datastore` → `core-network` dependency added cleanly with no circular dependency.
- [ ] Koin wiring complete; `composeApp` can inject a fully-wired `RemoteConfigRepository` at startup.
- [ ] Verified against a live/staging B-01 deployment at least once (not mocks alone) before this is marked complete — this is the one criterion this file's implementer cannot satisfy purely through unit tests, because it requires Phase 4's backend to actually exist.
- [ ] `core-datastore`'s status updates from 🟡 **COMPLETED (partial)** to 🟢 **COMPLETE**.

---

## 18. Assumptions and Decisions the Coding Agent Must Follow

1. **Do not change `RemoteConfigRepository`'s existing public method signatures.** `observeFlags(): Flow<FeatureFlagDefaults>`, `suspend fun refresh(): NoorResult<Unit>`, and `suspend fun saveRemoteValues(...)` (or whatever their exact current shape proves to be once the real source is read, per §6.7) must remain source- and binary-compatible. All new capability is added via new, additional interface members. If any existing feature module already calls `refresh()` expecting its current (Phase 0, local-only) behavior, that caller will now transparently get real network data instead — this is the intended, desired change in *behavior*, not a change in *contract*.
2. **B-01's payload does not currently contain `ramadanModeEnabled`/`aiTutorEnabled`.** This is confirmed directly from B-01 §12's JSON examples and §13's table — `remote_config` contains only `intro_slides_version`/`consent_version`. This is not a bug to "fix" by inventing fields the backend doesn't send; `FeatureFlagDefaults`'s existing reconciliation logic continues to correctly fall back to `BUILD_DEFAULT_FALLBACK` for those two flags until a future backend iteration adds them to the bootstrap payload (B-09 §5 itself flags `onboarding_v1_enabled` as an open scope question for a *future* iteration — do not preempt that by guessing a field name/shape here).
3. **The three non-cacheable top-level fields beyond `session_valid`/`has_children`** (`family_id`, `min_supported_version`/`recommended_version`, `maintenance_mode`/`maintenance_estimated_end_at`) are treated as never-cached by extension of B-01's explicit rule for `session_valid`/`has_children`, since they share the same "must be fresh every launch" character and are not documented as safe to cache. If a future revision of B-01 explicitly designates any of these as client-cacheable, that would require updating this file, not silently deciding to cache them now.
4. **Raw-response handling for 426/503 is confined to `BootstrapApiServiceImpl`.** Do not generalize this pattern into `safeCall` itself or apply it to any other endpoint — this is a deliberate, narrow exception justified specifically by B-01's documented "same body on error" contract (§12, §17), not a new house style for error handling across `core-network`.
5. **If `BootstrapDto.kt`/`AuthApiService.bootstrap()`/a `BootstrapApiService` already exists** in the codebase by the time this file is implemented (most likely because K-01 was implemented first, out of the documented phase order), **reuse it — do not create a duplicate.** Adapt this file's `RemoteConfigRepositoryImpl` wiring to whatever the existing service's exact method signature is, keeping the classification/caching/staleness logic specified here.
6. **`refresh()` write-through on 426/503-maintenance is deliberate**, not an oversight — B-01 guarantees a valid `remote_config` body on all three response shapes, so discarding it on the two error paths would be strictly worse (stale config lingering longer than necessary) with no corresponding benefit.
7. **Do not add a background polling timer.** `refreshIfStale()` is check-then-fetch, invoked by external triggers (§11) — this module does not spin up its own scheduled/periodic refresh job.
8. **Do not touch `DataStoreFactory.kt` or any specialized domain store** (`FamilyTimezoneStore`, `ClockSkewStore`, `LastObservedTimeZoneStore`) — none of them are related to this gap.

---

## AI Agent Development Prompt

You are implementing a **gap-closure** change to the already-built `core-datastore` module in the NoorHeroes KMP project (Android/iOS, Kotlin Multiplatform, Compose Multiplatform, Ktor, Koin). Do not rebuild or restructure anything already working — you are wiring one specific missing piece into an existing, functioning module.

**The gap:** `RemoteConfigRepository.refresh()` in `core-datastore` is currently local-only ("Phase 0 Status" per `CORE_DATASTORE_INSTRUCTIONS.md`). It must be wired to call the already-specified backend bootstrap endpoint, `GET /v1/identity/bootstrap` (blueprint: `Development_Blueprints/A1_Splash_Auth_Onboarding/Backend/01-bootstrap-remote-configuration-api.md`, ID **B-01**).

**Before writing any code:**
1. Read `NoorHeroes/core/core-datastore/CORE_DATASTORE_INSTRUCTIONS.md` in full.
2. Read `NoorHeroes/core/core-network/CORE_NETWORK_INSTRUCTIONS.md` in full.
3. Read `Development_Blueprints/A1_Splash_Auth_Onboarding/Backend/01-bootstrap-remote-configuration-api.md` §12 (API Contract) and §17 (Error Handling) closely — the client wiring must match that contract exactly, field-for-field.
4. Open the **actual current source** of `RemoteConfigRepository.kt` (interface, `core-common`) and `RemoteConfigRepositoryImpl.kt` (implementation, `core-datastore`) and confirm their real method signatures before touching them.
5. Search the codebase for any pre-existing `BootstrapDto.kt`, `AuthApiService.bootstrap()`, or `BootstrapApiService` — if K-01 (`Development_Blueprints/A1_Splash_Auth_Onboarding/KMP/01-splash-bootstrap-update-gating-flow.md`) was implemented ahead of this file, these may already exist. Reuse them; do not create duplicates.

**What to build, in order** (full detail in §5–§13 of this spec):
1. `core-network/model/BootstrapDto.kt` — `BootstrapResponseDto`, `RemoteConfigPayloadDto`, matching B-01 §12's JSON exactly (snake_case `@SerialName`, camelCase Kotlin fields).
2. `core-network/api/BootstrapApiService.kt` — interface `fun fetchBootstrap(appVersion, platform, locale): NoorResult<BootstrapOutcome>` plus `internal` `BootstrapApiServiceImpl`. This implementation must read the **raw** `HttpResponse` (not an auto-throwing typed call) so it can parse the response body on HTTP 426 and 503 too — B-01 guarantees the same `BootstrapResponse` JSON shape on those two error codes. Classify: 200 → `Available`, 426 → `ForcedUpdateRequired`, 503-with-parseable-`maintenance_mode:true`-body → `MaintenanceActive`, everything else → `NoorResult.Failure` via the existing `HttpResponse.toAppError()`/`Throwable.toTransportAppError()` mappers.
3. Register `BootstrapApiService` in `core-network`'s Koin module.
4. `core-common`: add `RemoteConfigSnapshot` and `BootstrapMetadata` data classes; add three `PreferenceConstants` keys (`KEY_REMOTE_CONFIG_INTRO_SLIDES_VERSION`, `KEY_REMOTE_CONFIG_CONSENT_VERSION`, `KEY_REMOTE_CONFIG_LAST_FETCHED_AT`); add exactly three new methods to `RemoteConfigRepository` — `observeConfigSnapshot(): Flow<RemoteConfigSnapshot>`, `observeBootstrapMetadata(): StateFlow<BootstrapMetadata?>`, `suspend fun refreshIfStale(): NoorResult<Unit>` — **appended, not replacing anything**.
5. `core-datastore/build.gradle.kts`: add `implementation(project(":core-network"))`.
6. `core-datastore/store/RemoteConfigRepositoryImpl.kt`: inject `Lazy<BootstrapApiService>`; rewrite `refresh()`'s body to call it, classify the result, and — on any of the three success outcomes (200/426/503-maintenance) — write `intro_slides_version`/`consent_version`/fetch-timestamp through to `PreferenceManager` via `PreferenceConstants` keys, and update an in-memory `MutableStateFlow<BootstrapMetadata?>` with the non-cacheable fields. On any failure, touch nothing and return `NoorResult.Failure`. Keep `refresh()`'s **existing return type and signature** unchanged. Implement `refreshIfStale()` as a 5-minute-TTL check-then-`refresh()` gate. Guard against overlapping concurrent calls with a `Mutex`/shared in-flight result.
7. `core-datastore/store/BootstrapConfigMapper.kt` (internal): pure mapping functions, kept separate for unit-testability.
8. Wire Koin (`core-datastore/di/DatastoreModule.kt`) and `composeApp`'s lifecycle hook (call `refresh()` at cold launch, `refreshIfStale()` on foreground resume — the actual UI/ViewModel that decides *what* to render based on the result belongs to K-01, out of scope here; this file only needs the lifecycle *trigger*, e.g. an `AppLifecycleObserver`).
9. App-version/platform/locale header providers — reuse existing `core-common` primitives if present; create the minimal `expect`/`actual` pair only if genuinely absent.

**What NOT to change:**
- Do not modify `DataStoreFactory.kt`, `PreferenceManagerImpl`, or any specialized domain store (`FamilyTimezoneStore`, `ClockSkewStore`, `LastObservedTimeZoneStore`).
- Do not change the signature of any existing `RemoteConfigRepository` method — only add new ones.
- Do not persist `session_valid`, `family_id`, `has_children`, `min_supported_version`, `recommended_version`, `maintenance_mode`, or `maintenance_estimated_end_at` anywhere in `PreferenceManager` — these stay in-memory only, per B-01's own "never cache" rule.
- Do not build B-01 itself (backend) — it is a separate, already-specified blueprint, gated on Phase 4.
- Do not build K-01's screens/`SplashViewModel`/navigation interceptor — this file stops at the repository boundary K-01 will consume.
- Do not generalize the raw-response 426/503-body-parsing pattern into the shared `safeCall` wrapper or apply it to other endpoints.
- Do not invent feature-flag fields (`ramadanModeEnabled`/`aiTutorEnabled`) inside the bootstrap `remote_config` payload — B-01 does not send them today.
- Do not add a background polling timer — refresh is triggered externally only.

**How to verify you're done:**
1. Run the full test suite in `core-network` and `core-datastore`, including the **required** stale-cache-fallback test: seed `PreferenceManager` with known-good cached values, make the mocked `BootstrapApiService` return a network failure, call `refresh()`, and assert (a) it returns `Failure`, and (b) `observeConfigSnapshot()` still emits the untouched, previously-seeded values.
2. Confirm the pre-existing `observeFlags()` test suite (unrelated to this change) still passes unmodified — proving `FeatureFlagDefaults` reconciliation is unaffected.
3. Confirm via test or inspection that no test-double/in-memory DataStore ever contains a key for `session_valid`, `family_id`, `has_children`, or any version-gate/maintenance field.
4. If a staging deployment of B-01 is available, run the app and confirm a cold launch populates `observeConfigSnapshot()` and `observeBootstrapMetadata()` correctly for both an authenticated session and a fresh, unauthenticated install; confirm airplane-mode launch on a device with prior cached data falls back to that cached data instead of erroring.
5. Confirm `core-datastore`'s status can be updated from 🟡 COMPLETED (partial) to 🟢 COMPLETE.
