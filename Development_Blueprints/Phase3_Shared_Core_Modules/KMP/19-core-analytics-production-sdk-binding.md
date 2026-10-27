# Phase 3 — core-analytics: Real Analytics SDK Binding (Gap Closure)

## 0. Document Metadata

| Field | Value |
|---|---|
| Phase | Phase 3 — Shared Core Modules (KMP) |
| Blueprint ID | Phase3_Shared_Core_Modules.KMP.19 |
| Surface | KMP (`core-analytics` module + two new provider modules, Android + iOS actuals) |
| Status this closes | `core-analytics` is 🟡 **COMPLETED (partial)** — `AnalyticsTracker` abstraction, `LoggerAnalyticsTracker`, and `CompositeAnalyticsTracker` are built and in production use by every ViewModel; `CORE_ANALYTICS_INSTRUCTIONS.md` §5 Scenario 2 documents a real remote-provider binding as future work ("adding a new remote analytics provider") that was never executed. This document executes it. |
| Depends on | `core-common` (already built — `LogSeverity`, `AppError`, DI primitives); `core-security`'s `secureHash()` (already built, §9.4); C.26 `ConsentRepository` (already built per its own blueprint, K-02 — read/write veneer over A.1's consent ledger); a Firebase project + (optionally) a Mixpanel project — **prerequisite, not yet confirmed to exist, see §16.1.** |
| Vendor decision | **Firebase Analytics (via the GitLive Kotlin Firebase SDK) is the default, required transport.** Mixpanel is a fully-specified, **optional, deferred** second transport, added later without redesigning anything here (§3.5, §8.4-equivalent pattern). |
| Consumers of the outcome | Every feature ViewModel across the app that already injects `AnalyticsTracker` (per `CORE_ANALYTICS_INSTRUCTIONS.md` §4.1) — none of them change a single line as a result of this document. |
| Status of underlying code | `AnalyticsTracker` interface: complete, stable, **do not change its contract.** Concrete real-SDK implementation: **does not exist, this document specifies it in full.** |

---

## 1. Objective and Purpose

`core-analytics` already gives every ViewModel a single, stable way to say "this happened" — `AnalyticsTracker.logEvent(...)`, `.logScreenView(...)`, `.setUserProperty(...)`, `.setUserId(...)`, `.reset()` — without ever importing a vendor SDK class. Today, every one of those calls terminates at `LoggerAnalyticsTracker`, which prints a structured line to the console and goes nowhere else. `CORE_ANALYTICS_INSTRUCTIONS.md` §5 Scenario 2 already anticipates the next step by name — *"I'm adding a new remote analytics provider (e.g. Firebase) → implement the `AnalyticsTracker` interface in a platform-specific module (e.g., `core-analytics-firebase`)"* — but no such module exists yet. The product currently has zero visibility into what users actually do in the app: no funnel data, no retention data, no feature-adoption data. That is the gap.

This document's job is narrow and mechanical by design: **wire a real transport in behind the existing interface.** It does not invent new events, does not decide what any feature should track, and does not touch a single ViewModel. It answers exactly these questions, with zero ambiguity left for the implementing agent:

1. Which vendor SDK(s), and why (§3).
2. Exactly how the KMP binding is structured — module boundaries, `expect`/`actual` vs. GitLive's unified API, and where each piece of code lives (§4, §5).
3. **How real collection is gated behind parental consent, correctly, at two independent layers, before the SDK ever collects a single event** — this is the section that matters most for a children's product and is treated with the same non-negotiable weight §9 gives it (§9).
4. How failure (SDK init failure, consent read failure, network absence) degrades safely instead of crashing the app or silently over-collecting (§10).

### 1.1 Why this is a gap-closure, not a from-scratch build

The abstraction, the no-op implementation, and every call site already exist and are correct. Nothing about the *shape* of analytics in this codebase is being redesigned. The only thing missing is the concrete class that sits behind the interface in staging/production builds, plus the consent plumbing that must exist before that class is allowed to talk to a vendor. Every other section below is in service of that one addition.

---

## 2. Scope and Requirements

### 2.1 In scope
- A production-grade `FirebaseAnalyticsTracker` (in a new `core-analytics-firebase` module) implementing the existing `AnalyticsTracker` interface via the GitLive Kotlin Firebase SDK's unified `commonMain` API (§3.2–§3.4).
- A fully-specified, **optional/deferred** `MixpanelAnalyticsTracker` (in a new `core-analytics-mixpanel` module) using an `expect`/`actual` bridge, since no unified KMP Mixpanel SDK exists (§3.5).
- `AnalyticsConsentProvider` — a new, small, synchronous, reactive contract in `core-analytics` itself, plus its fail-closed default and the composition-root adapter that binds it to C.26's real consent state (§6.2, §9.2).
- `ConsentGatedAnalyticsTracker` — a decorator that sits between the composite of real trackers and everything upstream of it, enforcing the consent gate at the point of every call (§6.3, §9.3).
- `AnalyticsParamSanitizer` — a defense-in-depth PII filter applied to every event/param/user-property before it reaches a real vendor SDK (§9.5).
- Environment-aware DI wiring (`analyticsModule` + a composition-root module) that keeps `LoggerAnalyticsTracker` exactly as-is for local/debug builds and adds the consent-gated real transport for staging/production (§6.5, §13).
- Native-SDK platform configuration required specifically because this is a children's product: disabling ad-personalization signals, automatic screen reporting, and Advertising ID collection at the manifest/plist level (§9.6).
- Correction of `CORE_ANALYTICS_INSTRUCTIONS.md` to document the real binding and the consent gate (§13, Task 13).
- Full test plan, including the DebugView/Live-View manual verification acceptance criterion (§14).

### 2.2 Out of scope — explicitly do not touch
- **The `AnalyticsTracker` interface contract** (`logEvent`, `logScreenView`, `setUserProperty`, `setUserId`, `reset` — exact signatures per `CORE_ANALYTICS_INSTRUCTIONS.md` §4.1). Every existing ViewModel call site keeps compiling and calling it exactly as today. This is the single hardest constraint in this document, restated in §18.
- **What events any feature logs, with what names or parameters.** That is each feature's own blueprint's responsibility (per `AnalyticsConstants` in `core-common`, per `CORE_ANALYTICS_INSTRUCTIONS.md` §6 "Do"). This document only builds the pipe; it does not decide what flows through it.
- **`LoggerAnalyticsTracker` and `CompositeAnalyticsTracker`** — both already correct, both reused unmodified as building blocks (`LoggerAnalyticsTracker` stays the debug/dev binding verbatim; `CompositeAnalyticsTracker` is reused, not reimplemented, to fan out to multiple real trackers and to combine the logger with the gated real transport).
- **`core-security`'s `secureHash()`** — reused as-is (§9.4), never modified.
- **`core-crash`'s own Firebase/Crashlytics binding** — a separate, independently-scoped gap (its own module's status is unrelated to this document's Definition of Done). This document only calls out where the two should *share* Firebase project configuration so it isn't set up twice (§12.3, §15.4) — it does not implement or fix `core-crash`.
- **C.26's `ConsentRepository`, consent UI, or withdrawal flow** — already built (K-02). This document is a *consumer* of that repository's state, never a modifier of it. If `ConsentRepository` does not yet expose a reactive/observable accessor for a single consent type's current value, this document requires *adding* that one accessor (§6.2.1) — it does not touch anything else in that module.
- **`core-datastore-remote-config`'s** own bootstrap/endpoint work (a separate, already-specified gap closure, Phase3 KMP 16) — this document only *optionally* consumes a remote-config flag as an operational kill-switch (§15.3); it does not implement remote-config itself.

### 2.3 Non-functional requirements carried forward from the source corpus
- **Non-blocking, main-thread-safe:** every `AnalyticsTracker` method must remain non-blocking (`CORE_ANALYTICS_INSTRUCTIONS.md` §6 "Don't" — unchanged requirement, now binding on the real implementations too).
- **Never throws to the caller:** a ViewModel calling `tracker.logEvent(...)` must never see an exception, regardless of vendor SDK state, network state, or consent state (§10).
- **PII never leaves the device toward a vendor SDK** — restated and made structurally enforced, not just documented, by this work (§9.5).
- **Zero collection before affirmative parental consent, and immediate cessation on revocation** — the platform's binding, non-negotiable requirement for this document specifically (§9).

---

## 3. Technical Implementation Details

### 3.1 The vendor decision

**Firebase Analytics, via the GitLive Kotlin Firebase SDK (`dev.gitlive:firebase-analytics`), is the required default transport for this Definition of Done. Mixpanel is a fully-specified but optional, deferred second transport.**

| Consideration | Firebase Analytics (GitLive) | Mixpanel |
|---|---|---|
| KMP integration shape | **Unified `commonMain` API** — GitLive's SDK provides real, non-`expect`/`actual` Kotlin bindings that call the native Android and iOS Firebase SDKs underneath. One implementation file, not three. | No unified KMP SDK exists. Requires a hand-written `expect`/`actual` bridge over the native Android (`com.mixpanel.android:mixpanel-android`) and iOS (CocoaPods `Mixpanel-swift`) SDKs. |
| Shared infrastructure | **Already the project's chosen path for Firebase elsewhere** — this document's own metadata table and `CORE_CRASH_INSTRUCTIONS.md` §8 both name Firebase Crashlytics as `core-crash`'s intended (not-yet-bound) provider. Standing this module up on GitLive means a single Firebase project, a single `google-services.json`/`GoogleService-Info.plist`, and a single Firebase BoM version serve both `core-analytics` and, whenever it is closed, `core-crash`'s own gap (§12.3). | No existing project infrastructure to share. |
| Cost | Free at essentially any realistic scale for this product (Firebase Analytics has no event-volume billing). | Free tier is usage-capped; meaningful product-analytics depth (cohorts, funnels, session replay-adjacent features) is a paid tier. |
| Product-analytics depth | Solid funnel/retention/audience tooling via Firebase + BigQuery export, but weaker ad-hoc segmentation and event-property exploration than a purpose-built product-analytics tool. | Materially stronger ad-hoc exploration, cohort analysis, and event-property drill-down — the reason it is worth keeping as an option, not the reason to lead with it. |
| Decision | **Default, required.** Lower integration cost, shares infrastructure with `core-crash`, zero new vendor relationship needed beyond a Firebase project. | **Optional, additive, deferred.** Fully specified (§3.5, §5, §6.4) so adopting it later is a scoped module addition, not a redesign. Do not implement `core-analytics-mixpanel` as part of this Definition of Done unless explicitly directed — see §16.1 and §18.7. |

This mirrors the exact reasoning shape the project's own prior gap-closure documents use for a vendor/algorithm choice under multiple viable options (see Phase3 KMP 17 §8.2's PBKDF2-vs-Argon2id table for the precedent this table follows) — evaluate both fairly, pick the one that meets the bar with the least new risk, document the runner-up as a clean future addition rather than silently dropping it.

### 3.2 Why GitLive specifically, and not a hand-rolled `expect`/`actual` for Firebase too

A hand-rolled `expect`/`actual` Firebase binding was considered and rejected: Firebase's native Android and iOS SDKs have materially different call shapes (`FirebaseAnalytics.getInstance(context).logEvent(name, bundle)` on Android vs. `Analytics.logEvent(name, parameters:)` on iOS), and re-deriving that mapping by hand duplicates work GitLive's SDK — a real, maintained, widely-used KMP library — already does correctly, tested against both platforms' actual SDKs. Using it is the same "don't reinvent a KMP-native binding that already exists and is well-tested" reasoning `CORE_SECURITY_INSTRUCTIONS.md`'s own prior gap-closure work applies when it prefers a JDK/OS-builtin primitive over a hand-rolled one wherever possible (Phase3 KMP 17 §8.2). GitLive is not a data pass-through or a proxy service — it is a Kotlin binding layer with real platform actuals; using it does not violate the "never use concrete SDK classes in feature modules" rule, because feature modules still only ever see `AnalyticsTracker`, never GitLive's types (§4).

### 3.3 What "SDK binding" means concretely for this module

`FirebaseAnalyticsTracker` implements the existing `AnalyticsTracker` interface and, internally, calls a thin seam (`FirebaseAnalyticsNative`, §6.4) that wraps GitLive's `dev.gitlive.firebase.analytics.FirebaseAnalytics` object. The seam exists for exactly one reason: GitLive's real `Firebase.analytics` accessor cannot run inside a plain JVM unit test (it requires a live or emulated Firebase context on each platform), so `FirebaseAnalyticsTracker`'s actual logic — mapping calls, applying the sanitizer, applying the consent gate's second layer — is tested against a fake `FirebaseAnalyticsNative`, and only the one-line `GitLiveFirebaseAnalyticsNative` adapter is untested-by-unit-test (verified instead by the manual DebugView check in §14.5).

### 3.4 The consent-gating mechanism, at the architecture level (full detail in §9)

Two independent layers, not one, because they close two different collection paths:

1. **`ConsentGatedAnalyticsTracker`** — a decorator wrapping the composite of real trackers. Every explicit `AnalyticsTracker` call an app-level caller makes is checked against a synchronous, warm consent snapshot *before* it is ever forwarded. This closes the path of events this codebase explicitly emits.
2. **Each concrete real tracker (`FirebaseAnalyticsTracker`, `MixpanelAnalyticsTracker`) reactively toggles its vendor SDK's own native collection-enabled flag** (`setAnalyticsCollectionEnabled` / `optOutTracking`) whenever consent changes. This closes the path of events the *vendor SDK itself* emits automatically (Firebase's `session_start`/`app_open`/auto screen tracking) that never pass through our `AnalyticsTracker.logEvent()` call path at all, and therefore layer 1 alone cannot intercept.

Both layers default to **collection disabled** at construction, before either has ever read a real consent value — see §9.2's fail-closed design.

### 3.5 Mixpanel's binding shape (deferred, fully specified)

If/when `core-analytics-mixpanel` is built: an `expect class MixpanelBridge` in `commonMain` with `androidMain`/`iosMain` actuals wrapping the native SDKs, plus a `MixpanelAnalyticsTracker` implementing `AnalyticsTracker` over that bridge — same shape as `FirebaseAnalyticsTracker`, same sanitizer, same reactive consent toggle via Mixpanel's own `optOutTracking()`/`optInTracking()`. **Mixpanel's Session Replay / Autocapture features must be explicitly disabled if this module is ever built** — they capture UI content and interaction streams beyond anything this document's redaction layer can filter, and are unacceptable in a children's product regardless of consent state (§9.6.3).

---

## 4. Architecture and Component Responsibilities

```
Feature ViewModel (unchanged — injects AnalyticsTracker exactly as today)
    ↓ calls
AnalyticsTracker (interface, core-analytics — UNCHANGED)
    ↓ resolved by Koin to, per environment:
    ┌─────────────────────────────────────────────────────────────┐
    │ Debug/local:  LoggerAnalyticsTracker (UNCHANGED, untouched)  │
    │                                                               │
    │ Staging/Prod: CompositeAnalyticsTracker(                     │
    │   LoggerAnalyticsTracker,                    ← still runs,   │
    │                                                 console only │
    │   ConsentGatedAnalyticsTracker(               ← NEW, layer 1 │
    │     delegate = CompositeAnalyticsTracker(                    │
    │       FirebaseAnalyticsTracker,               ← NEW           │
    │       MixpanelAnalyticsTracker (optional)     ← NEW, deferred │
    │     ),                                                        │
    │     consentProvider = AnalyticsConsentProvider ← NEW          │
    │   )                                                           │
    │ )                                                             │
    └─────────────────────────────────────────────────────────────┘
        ↓ FirebaseAnalyticsTracker internally
    AnalyticsParamSanitizer (NEW) → FirebaseAnalyticsNative (NEW seam)
        ↓ reactively toggled by AnalyticsConsentProvider.consentState  ← layer 2
    GitLiveFirebaseAnalyticsNative → dev.gitlive Firebase.analytics → native Firebase SDK
        ↓
AnalyticsConsentProvider (interface, core-analytics — NEW)
    ↑ implemented at the composition root by
ConsentLedgerAnalyticsConsentProvider (NEW, app composition root)
    ↓ observes
C.26 ConsentRepository (already built) → C.26 consent ledger (`personalization` type, §9.2)
```

**Component responsibilities:**

| Component | Responsibility | New / Changed? | Lives in |
|---|---|---|---|
| `AnalyticsTracker` | Existing public contract. | **Unchanged.** | `core-analytics` |
| `LoggerAnalyticsTracker` | Console-only dev tracker. | **Unchanged, stays available.** | `core-analytics` |
| `CompositeAnalyticsTracker` | Fan-out to N trackers. | **Unchanged, reused.** | `core-analytics` |
| `AnalyticsConsentProvider` | Synchronous, reactive, fail-closed read of whether real analytics collection is currently permitted. | **New (interface).** | `core-analytics` |
| `AlwaysDeniedAnalyticsConsentProvider` | Fail-closed default binding so `core-analytics` never has an unbound dependency. | **New.** | `core-analytics` |
| `ConsentGatedAnalyticsTracker` | Layer-1 gate: drops every call at the source when consent is not currently granted; always forwards `reset()` regardless (§9.3.1). | **New.** | `core-analytics` |
| `AnalyticsParamSanitizer` | Deny-list + shape-based PII filter, param/name/value length and count caps matching vendor limits. | **New.** | `core-analytics` |
| `FirebaseAnalyticsTracker` | Concrete `AnalyticsTracker`; fail-closed init; layer-2 reactive native toggle; applies sanitizer; guards `setUserId` shape. | **New.** | `core-analytics-firebase` (new module) |
| `FirebaseAnalyticsNative` / `GitLiveFirebaseAnalyticsNative` | Testable seam over GitLive's real `Firebase.analytics`. | **New.** | `core-analytics-firebase` |
| `MixpanelAnalyticsTracker` / `MixpanelBridge` | Same shape as Firebase's, over Mixpanel's SDKs. | **New, deferred/optional.** | `core-analytics-mixpanel` (new module, not required for this DoD) |
| `ConsentLedgerAnalyticsConsentProvider` | Bridges the app's real, family-scoped `personalization` consent state into `AnalyticsConsentProvider`. | **New.** | App composition root (§5, exact module TBC on confirmation) |

---

## 5. Folder / File Structure

```
core-analytics/                                          (existing module)
  src/commonMain/kotlin/com/noorheroes/core/analytics/
    AnalyticsTracker.kt                                   # UNCHANGED
    LoggerAnalyticsTracker.kt                              # UNCHANGED
    CompositeAnalyticsTracker.kt                           # UNCHANGED
    ConsentGatedAnalyticsTracker.kt                        # NEW
    consent/
      AnalyticsConsentProvider.kt                          # NEW — interface
      AlwaysDeniedAnalyticsConsentProvider.kt               # NEW — fail-closed default
      AlwaysGrantedAnalyticsConsentProvider.kt              # NEW — test/QA-only double, see §14.6
    sanitizer/
      AnalyticsParamSanitizer.kt                            # NEW
    di/
      analyticsModule.kt                                    # MODIFIED — see §6.5
  src/commonTest/kotlin/com/noorheroes/core/analytics/
    ConsentGatedAnalyticsTrackerTest.kt                     # NEW
    sanitizer/AnalyticsParamSanitizerTest.kt                # NEW

core-analytics-firebase/                                  (NEW Gradle module)
  build.gradle.kts                                          # NEW — GitLive dep, applies google-services (Android)
  src/commonMain/kotlin/com/noorheroes/core/analytics/firebase/
    FirebaseAnalyticsNative.kt                              # NEW — interface seam
    FirebaseAnalyticsTracker.kt                             # NEW
    di/firebaseAnalyticsModule.kt                           # NEW
  src/androidMain/kotlin/com/noorheroes/core/analytics/firebase/
    GitLiveFirebaseAnalyticsNative.kt                       # NEW — thin adapter (GitLive is unified, so this
                                                              #        file is nearly identical on both platforms;
                                                              #        kept per-source-set only because GitLive's
                                                              #        Firebase.analytics accessor needs platform
                                                              #        init to have already run — confirm during
                                                              #        Task 02 whether it can instead live in
                                                              #        commonMain directly)
  src/iosMain/kotlin/com/noorheroes/core/analytics/firebase/
    GitLiveFirebaseAnalyticsNative.kt                       # NEW — see note above
  src/commonTest/kotlin/com/noorheroes/core/analytics/firebase/
    FirebaseAnalyticsTrackerTest.kt                         # NEW — against a fake FirebaseAnalyticsNative

core-analytics-mixpanel/                                  (NEW Gradle module — OPTIONAL, deferred, §3.5/§16.1)
  build.gradle.kts
  src/commonMain/kotlin/com/noorheroes/core/analytics/mixpanel/
    MixpanelBridge.kt                                       # expect
    MixpanelAnalyticsTracker.kt
    di/mixpanelAnalyticsModule.kt
  src/androidMain/.../mixpanel/MixpanelBridge.android.kt     # actual
  src/iosMain/.../mixpanel/MixpanelBridge.ios.kt              # actual

<app composition-root module — confirm exact name/path before assuming; likely `shared`/`composeApp`'s
 top-level DI assembly, alongside wherever `initKoin()` is called and other cross-cutting composition-root
 adapters for this project already live (e.g., alongside an equivalent `AuthStateProvider` binding)>
  .../analytics/ConsentLedgerAnalyticsConsentProvider.kt    # NEW
  .../di/AnalyticsCompositionModule.kt                       # NEW — assembles the environment-aware binding
                                                              #        from §4/§6.5; wired into initKoin()

NoorHeroes/core/
  CORE_ANALYTICS_INSTRUCTIONS.md                            # MODIFIED — §13 Task 13 specifies the exact addition

android app module / Manifest
  AndroidManifest.xml                                       # MODIFIED — §9.6.1 meta-data additions
  google-services.json                                      # NEW or REUSED — confirm before assuming (§12.3)

iOS app target
  Info.plist                                                # MODIFIED — §9.6.2 additions
  GoogleService-Info.plist                                  # NEW or REUSED — confirm before assuming (§12.3)
```

**Note on the composition-root location:** the corpus provided to this task does not name the exact module/file where cross-cutting adapters like an `AuthStateProvider` implementation are bound into Koin at app start. **Do not guess a path.** Task 01 of §13 requires locating that exact existing pattern (search for wherever `AuthStateProvider`'s concrete implementation, or an equivalent composition-root adapter, is currently bound) and placing `ConsentLedgerAnalyticsConsentProvider` alongside it, following the same convention — not inventing a new composition pattern for this one adapter.

---

## 6. APIs, Models, Interfaces, and Data Flow

### 6.1 `AnalyticsTracker` — unchanged interface (restated for reference only)
```kotlin
package com.noorheroes.core.analytics

interface AnalyticsTracker {
    fun logEvent(name: String, params: Map<String, Any?> = emptyMap())
    fun logScreenView(name: String, params: Map<String, Any?> = emptyMap())
    fun setUserProperty(name: String, value: String)
    fun setUserId(id: String?)
    fun reset()
}
```
No signature change of any kind. Confirm the exact current default-parameter shape against the real source file during Task 01 (§13) rather than assuming the above is letter-perfect — the behavior contract, not this restatement, is authoritative.

### 6.2 `AnalyticsConsentProvider` — new interface
```kotlin
package com.noorheroes.core.analytics.consent

import kotlinx.coroutines.flow.StateFlow

/**
 * A synchronous, non-blocking, reactive view of whether the current family has granted
 * the consent that gates real (non-logger) analytics SDK collection.
 *
 * Implementations MUST NOT perform blocking I/O, suspend work, or a network call inside
 * [isAnalyticsCollectionAllowed] — every AnalyticsTracker method calls this on the hot path,
 * potentially many times per screen. The correct pattern is: maintain a warm, reactively-updated
 * snapshot (a StateFlow collected in the background) and have both members simply read it.
 *
 * Fail-closed by contract: until a real consent value has been affirmatively read and found
 * `true`, every implementation MUST report `false`. See core-analytics's Phase3.KMP.19
 * gap-closure document §9.2 for why this is non-negotiable for this product.
 */
interface AnalyticsConsentProvider {
    /** Current snapshot; equivalent to consentState.value, provided for a non-Flow-aware call site. */
    fun isAnalyticsCollectionAllowed(): Boolean

    /** Reactive stream of the same value. Real trackers subscribe to this for layer-2 gating (§9.3.2). */
    val consentState: StateFlow<Boolean>
}
```

### 6.2.1 `AlwaysDeniedAnalyticsConsentProvider` — new, fail-closed default
```kotlin
package com.noorheroes.core.analytics.consent

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

/**
 * Default binding inside core-analytics itself, so the module never has an unbound
 * AnalyticsConsentProvider dependency. The composition root overrides this with
 * ConsentLedgerAnalyticsConsentProvider for any environment where real collection can occur.
 * If this default is ever what actually ends up bound in a staging/production build, that is
 * a wiring bug (real collection would be permanently, silently disabled) — see the Task 14.6
 * self-check that catches exactly this failure mode.
 */
class AlwaysDeniedAnalyticsConsentProvider : AnalyticsConsentProvider {
    override fun isAnalyticsCollectionAllowed(): Boolean = false
    override val consentState: StateFlow<Boolean> = MutableStateFlow(false)
}
```

### 6.2.2 `ConsentLedgerAnalyticsConsentProvider` — new, composition root
```kotlin
package com.noorheroes.<composition-root-package>.analytics   // exact package per §5's location note

import com.noorheroes.core.analytics.consent.AnalyticsConsentProvider
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.launch

/**
 * Bridges C.26's real, family-scoped consent state into the AnalyticsConsentProvider contract.
 * Gates on the `personalization` consent type — see this document's §9.2 for the full audit
 * trail behind that specific mapping decision.
 */
class ConsentLedgerAnalyticsConsentProvider(
    private val consentRepository: ConsentRepository,     // C.26, core-data — already built
    private val appScope: CoroutineScope,                 // process-lifetime scope — see §11.1
) : AnalyticsConsentProvider {

    private val _consentState = MutableStateFlow(false)   // fail-closed at cold start — see §9.2/§11.3
    override val consentState: StateFlow<Boolean> = _consentState.asStateFlow()
    override fun isAnalyticsCollectionAllowed(): Boolean = _consentState.value

    init {
        appScope.launch {
            consentRepository.observeConsentStatus(ConsentType.Personalization)  // §6.2.3
                .catch { emit(false) }   // any read/mapping error also fails closed, never fails open
                .collect { status -> _consentState.value = (status == ConsentStatus.Granted) }
        }
    }
}
```

### 6.2.3 Required extension to `ConsentRepository` if it does not already expose this
`CompositeAnalyticsTracker`'s real-transport branch needs a **reactive** single-consent-type accessor. C.26 K-02's own specification only names `getConsents()` (a full 6-item list) as the repository's read method. **Confirm the exact current signature before writing `ConsentLedgerAnalyticsConsentProvider`** (Task 01, §13). If no `Flow`-returning, single-type accessor exists:

```kotlin
// core-data, ConsentRepository interface — ADD this method if it is not already present.
// Do not add anything else to this interface; this is the one accessor this document needs.
interface ConsentRepository {
    // ... existing methods, unchanged ...
    fun observeConsentStatus(type: ConsentType): Flow<ConsentStatus>
}
```
A reasonable default implementation derives this from whatever cached/offline-first list source `getConsents()` already reads (per K-02 §19/§20, the list already renders from a local cache with a read-through), mapped down to the single type and re-emitted on every cache update — it should not require a new network call beyond what already keeps that cache fresh. This is an additive, backward-compatible interface change; it does not alter `getConsents()` or any existing call site.

### 6.3 `ConsentGatedAnalyticsTracker` — new decorator
```kotlin
package com.noorheroes.core.analytics

import com.noorheroes.core.analytics.consent.AnalyticsConsentProvider

/**
 * Layer 1 of the two-layer consent gate (§9.3). Wraps the composite of real (non-logger) trackers.
 * Every method except [reset] checks [AnalyticsConsentProvider.isAnalyticsCollectionAllowed] and
 * silently drops the call — never throws, never queues for later replay (§8) — when consent is
 * not currently granted.
 */
class ConsentGatedAnalyticsTracker(
    private val delegate: AnalyticsTracker,
    private val consentProvider: AnalyticsConsentProvider,
) : AnalyticsTracker {

    override fun logEvent(name: String, params: Map<String, Any?>) {
        if (!consentProvider.isAnalyticsCollectionAllowed()) return
        delegate.logEvent(name, params)
    }

    override fun logScreenView(name: String, params: Map<String, Any?>) {
        if (!consentProvider.isAnalyticsCollectionAllowed()) return
        delegate.logScreenView(name, params)
    }

    override fun setUserProperty(name: String, value: String) {
        if (!consentProvider.isAnalyticsCollectionAllowed()) return
        delegate.setUserProperty(name, value)
    }

    override fun setUserId(id: String?) {
        if (!consentProvider.isAnalyticsCollectionAllowed()) return
        delegate.setUserId(id)
    }

    /**
     * Deliberate exception: reset() is a clearing operation, not a collection operation, and
     * always runs — including when consent is currently withdrawn — so a real vendor SDK never
     * retains stale user-level state past logout regardless of the current consent value.
     */
    override fun reset() {
        delegate.reset()
    }
}
```

### 6.4 `FirebaseAnalyticsTracker` and its native seam — new
```kotlin
// core-analytics-firebase, commonMain
package com.noorheroes.core.analytics.firebase

/** Testable seam over GitLive's real Firebase.analytics — see §3.3 for why this seam exists. */
interface FirebaseAnalyticsNative {
    fun logEvent(name: String, params: Map<String, Any?>)
    fun setUserProperty(name: String, value: String)
    fun setUserId(id: String?)
    fun setAnalyticsCollectionEnabled(enabled: Boolean)
    fun resetAnalyticsData()
}
```

```kotlin
package com.noorheroes.core.analytics.firebase

import com.noorheroes.core.analytics.AnalyticsTracker
import com.noorheroes.core.analytics.consent.AnalyticsConsentProvider
import com.noorheroes.core.analytics.sanitizer.AnalyticsParamSanitizer
import com.noorheroes.core.logger.NoorHeroesLogger
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.launch

class FirebaseAnalyticsTracker(
    private val native: FirebaseAnalyticsNative,
    private val consentProvider: AnalyticsConsentProvider,
    private val appScope: CoroutineScope,
    private val logger: NoorHeroesLogger,
) : AnalyticsTracker {

    init {
        // Fail-closed BEFORE subscribing to anything — this is what "consent checked before the
        // SDK is even initialized" means concretely for a DI-constructed singleton (§9.2): the
        // very first thing this object does, synchronously, in its own constructor, is disable
        // native collection. There is no window, however narrow, where collection defaults on.
        runCatching { native.setAnalyticsCollectionEnabled(false) }
            .onFailure { logger.warn(TAG, "Initial fail-closed toggle failed: ${it.message}") }

        // Layer 2 (§9.3.2): reactively mirror consent into the native SDK's own collection flag,
        // closing the auto-collected-event gap layer 1 cannot reach.
        appScope.launch {
            consentProvider.consentState.collect { granted ->
                runCatching { native.setAnalyticsCollectionEnabled(granted) }
                    .onFailure { logger.warn(TAG, "Native collection toggle failed: ${it.message}") }
            }
        }
    }

    override fun logEvent(name: String, params: Map<String, Any?>) = safely {
        val sanitized = AnalyticsParamSanitizer.sanitize(name, params, logger)
        native.logEvent(name, sanitized)
    }

    override fun logScreenView(name: String, params: Map<String, Any?>) = safely {
        val sanitized = AnalyticsParamSanitizer.sanitize(name, params, logger)
        native.logEvent("screen_view", sanitized + ("screen_name" to name))
    }

    override fun setUserProperty(name: String, value: String) = safely {
        native.setUserProperty(name, value.take(36))   // Firebase's own user-property value limit
    }

    override fun setUserId(id: String?) = safely {
        if (id != null && !AnalyticsParamSanitizer.looksLikeOpaqueHashedId(id)) {
            logger.warn(TAG, "Refused to forward setUserId(): value does not look like a " +
                "secureHash()-produced opaque id. See §9.4 — never pass a raw account/child id.")
            return@safely
        }
        native.setUserId(id)
    }

    override fun reset() = safely { native.resetAnalyticsData() }

    /** Never let a native SDK failure propagate to a ViewModel (§10). */
    private inline fun safely(block: () -> Unit) {
        runCatching(block).onFailure { logger.warn(TAG, "Firebase Analytics call failed: ${it.message}") }
    }

    private companion object { const val TAG = "FirebaseAnalyticsTracker" }
}
```

### 6.5 DI composition — modified `analyticsModule` + new composition-root module
```kotlin
// core-analytics/di/analyticsModule.kt — MODIFIED (additive only)
val analyticsModule = module {
    single { LoggerAnalyticsTracker(get()) }                                  // UNCHANGED binding
    single<AnalyticsConsentProvider> { AlwaysDeniedAnalyticsConsentProvider() } // NEW default, overridable
}
```

```kotlin
// composition root — NEW module, loaded only for staging/production Koin graphs
fun analyticsCompositionModule(environment: AppEnvironment): Module = module {

    single<AnalyticsConsentProvider> {
        ConsentLedgerAnalyticsConsentProvider(get(), get(named("AppScope")))   // overrides the default
    }

    single<AnalyticsTracker> {
        val logger = get<LoggerAnalyticsTracker>()
        when (environment) {
            AppEnvironment.Debug -> logger   // UNCHANGED behavior — real transport never loaded
            AppEnvironment.Staging, AppEnvironment.Production -> {
                val realTransports = buildList {
                    add(get<FirebaseAnalyticsTracker>())
                    getOrNull<MixpanelAnalyticsTracker>()?.let { add(it) }  // present only if the
                                                                              // optional module is included
                }
                CompositeAnalyticsTracker(listOf(
                    logger,
                    ConsentGatedAnalyticsTracker(CompositeAnalyticsTracker(realTransports), get()),
                ))
            }
        }
    }
}
```
`AppEnvironment` is assumed to already exist somewhere in the project's build-variant/config plumbing (`core-common`'s `config` package per `CORE_COMMON_INSTRUCTIONS.md` §3 — *"App-wide constants, feature flag defaults, and environment config"*) — **confirm its exact name and values during Task 01 (§13) rather than inventing a second environment enum.**

### 6.6 Data flow — a single `logEvent` call, staging/production, consent granted
```
ViewModel.tracker.logEvent("story_tap", mapOf("story_id" to id))
    ↓
CompositeAnalyticsTracker.logEvent(...)
    ├─→ LoggerAnalyticsTracker.logEvent(...)              → console line (always, unconditional)
    └─→ ConsentGatedAnalyticsTracker.logEvent(...)
            ↓ consentProvider.isAnalyticsCollectionAllowed() == true → forward
        CompositeAnalyticsTracker(real transports).logEvent(...)
            └─→ FirebaseAnalyticsTracker.logEvent(...)
                    ↓ AnalyticsParamSanitizer.sanitize(...)   (deny-list, shape checks, length caps)
                    ↓ FirebaseAnalyticsNative.logEvent(...)
                GitLiveFirebaseAnalyticsNative → Firebase.analytics.logEvent(...) → native SDK → vendor
```

### 6.7 Data flow — consent revoked mid-session
```
Parent withdraws `personalization` consent via C.26 K-02's Consent Log screen
    ↓
ConsentRepository's withdrawal call succeeds → cache invalidated (K-02 §20)
    ↓
ConsentRepository.observeConsentStatus(Personalization) emits ConsentStatus.Withdrawn
    ↓
ConsentLedgerAnalyticsConsentProvider._consentState.value = false
    ├─→ [Layer 1] Every subsequent ConsentGatedAnalyticsTracker call reads false → dropped, immediately,
    │    on the very next call (no async delay — this is a synchronous StateFlow.value read)
    └─→ [Layer 2] FirebaseAnalyticsTracker's collector observes consentState → native.setAnalyticsCollectionEnabled(false)
         → native SDK's OWN auto-collected events also stop, not just app-emitted ones
```

---

## 7. Dependencies and Configuration Requirements

- **`core-analytics-firebase` (new module) Gradle dependency:** `dev.gitlive:firebase-analytics:<version>` (commonMain), pulled in alongside whatever GitLive Firebase BoM/version the project settles on — coordinate with `core-crash`'s eventual binding so both use the same GitLive version (§12.3). No platform-specific dependency declarations needed beyond what GitLive's own Gradle setup requires per-target.
- **Android:** the Google Services Gradle plugin (`com.google.gms:google-services`) applied to the app module, and a `google-services.json` present — **confirm whether this already exists in the project from any prior Firebase-adjacent work (`core-crash`, `core-datastore-remote-config`'s bootstrap endpoint) before creating a new Firebase project** (§12.3, §16.1).
- **iOS:** a `GoogleService-Info.plist` bundled into the iOS target, and the native Firebase iOS SDK linked (GitLive's iOS actuals call through to it) — via CocoaPods (`pod 'FirebaseAnalytics'`) or SPM, whichever this project's existing iOS dependency management already uses for any other native pod — **confirm before adding a second dependency-management mechanism.**
- **`core-analytics-mixpanel` (optional, deferred):** `com.mixpanel.android:mixpanel-android` (androidMain actual) and the `Mixpanel-swift` CocoaPod/SPM package (iosMain actual) — **not added as part of this Definition of Done** unless §16.1's prerequisite (a Mixpanel account/project) is confirmed to exist and the team explicitly opts in.
- **ProGuard/R8 (Android release builds):** confirm Firebase Analytics' own consumer ProGuard rules are picked up automatically (standard for `google-services`-integrated dependencies; no custom keep rules expected, but a one-line audit during Task 06, §13).
- **Firebase project console configuration (not code, but a hard prerequisite — §9.6.4, §15.1):** Google Signals disabled, ad personalization signals disabled, and a conservative data-retention window set, before this module ever ships to a production build with real users.

---

## 8. Database / Storage Requirements

**No new local database or persistent queue is introduced by this document — this is a deliberate, verified decision, not an oversight.**

- **Post-consent event transport:** both Firebase Analytics and Mixpanel's native SDKs already batch events in their own on-device store (Firebase: an internal SQLite-backed queue; Mixpanel: its own local queue) and flush opportunistically, surviving app backgrounding and brief network loss without any help from this module. Reimplementing that would duplicate infrastructure the vendor SDKs already provide and are responsible for.
- **Pre-consent events are never queued for later replay.** This was considered and explicitly rejected: buffering an event emitted before consent is confirmed granted, intending to flush it once consent resolves, would still mean the underlying user action was *recorded* (in memory, however briefly) before consent existed — which does not satisfy "collect only after consent," merely defers *transmission* of an already-captured data point. `ConsentGatedAnalyticsTracker` therefore drops any call made while `isAnalyticsCollectionAllowed()` is `false`, unconditionally and permanently for that call — there is no buffer to inspect, persist, or leak.
- **Practical consequence, stated plainly (§11.3):** a handful of the very first events in a cold session (e.g., a splash-screen `logScreenView`) may be dropped even for a family that has already granted `personalization` consent, if they fire before `ConsentLedgerAnalyticsConsentProvider`'s background collector has completed its first read of the (already-cached, so typically sub-100ms) consent value. This is an accepted, intentional trade-off — fail-closed over fail-open — not a defect to engineer around with a queue.

---

## 9. Authentication, Authorization, Validation, and Security Considerations

This is the section this document is judged on most strictly. NoorHeroes is a children's product; the child app surface is used directly by children, and analytics collection from that surface is squarely within COPPA's scope. Nothing below is a suggestion.

### 9.1 The governing rule
**No real analytics SDK collects, transmits, or persists any event, screen view, user property, or identifier unless the family's parent has affirmatively granted the specific consent this document gates on (§9.2), and collection must stop within one call cycle of that consent being withdrawn.** `LoggerAnalyticsTracker` (console-only, never leaves the device, never reaches a vendor) is exempt from this gate — it is not "real collection" in the sense this rule concerns itself with, and stays available unconditionally for local/debug builds exactly as it does today.

### 9.2 Which existing consent this binds to — verified, not assumed

C.26's consent ledger (per its own already-built blueprint, K-02, and the backend contract it wraps) defines exactly six consent types via a database `CHECK` constraint: `terms`, `privacy`, `child_data` (all three **required**, non-withdrawable without triggering account deletion) and `personalization`, `voice_ai`, `marketing` (all three **optional**, individually withdrawable). **No dedicated `analytics` consent type exists in the corpus provided to this task.**

Two candidate mappings were evaluated:

- **Option A — introduce a new, dedicated `analytics` consent type** via C.26's already-built admin Consent Type Registry (`Development_Blueprints/C26_Privacy_Consent_Account_Security_Data_Rights/Backend/05-admin-consent-type-registry-api.md`, `NextJS_Admin/01-consent-type-registry-management.md`). This is the structurally cleanest answer — a purpose-built type, not an overload of an existing one — but it requires a schema change (a new `CHECK` constraint value), a new consent-record field, new UI copy in the Consent Log screen, and product/legal sign-off on new user-facing language. That is real, cross-team work this document cannot unilaterally execute.
- **Option B — gate on the existing `personalization` consent type.** The Consent Log screen's own mockup copy (`PRD_Documents/Parent Area — In-App (19-26)/Feature_C26_Privacy_Consent_Account_Security_Data_Rights.md` §2.2) labels this row "Personalization & AI Recommendations" — behavioral/usage-pattern collection for the purpose of tailoring the experience is precisely what real analytics SDK collection *is*, and is a closer semantic match than `voice_ai` (a narrower, feature-specific permission) or `marketing` (a different purpose entirely — promotional communication, not in-app behavioral tracking). No schema change, no new UI, immediately usable.

**Decision: Option B — this document gates all real analytics SDK collection on the existing `personalization` consent type**, implemented exactly as specified in §6.2.2/§6.2.3. **This is flagged, not silently settled, as a decision requiring product/legal confirmation before this module ships to production with real users** (§16.1, §18.2) — precisely the same "implement the interim answer, document the flag, do not claim the ambiguity is resolved" discipline C.26's own `voice_ai` family-vs-per-child scope conflict (K-02 §13, §29) already establishes as this project's house style for exactly this kind of situation. If Option A is later executed, `ConsentLedgerAnalyticsConsentProvider`'s single line (`ConsentType.Personalization` → `ConsentType.Analytics`) is the only change required anywhere in this document's implementation — the interface, the gating layers, and every real tracker are unaffected, by design.

Consent is **family-scoped**, not per-child (`consent_record` carries `family_id`, never `child_id`) — switching the active child profile under an already-authenticated parent session does **not** re-evaluate or change the analytics consent gate; it is one value per family, exactly as C.26's own ledger models it (§11.4).

### 9.3 The two-layer gate, restated with intent

#### 9.3.1 Layer 1 — `ConsentGatedAnalyticsTracker`
Every explicit call this codebase makes into `AnalyticsTracker` (every ViewModel's `logEvent`/`logScreenView`/`setUserProperty`/`setUserId`) is checked, synchronously, against the current consent snapshot **before** it is forwarded to any real vendor tracker. `reset()` is the sole, deliberate exception (§6.3) — it always runs, because clearing stale vendor-side user state on logout is itself a privacy-protective action that must never be blocked by the very gate protecting privacy elsewhere.

#### 9.3.2 Layer 2 — reactive native SDK toggle
Firebase Analytics (and, if built, Mixpanel) collect a meaningful amount of data **automatically**, without any explicit `logEvent` call from this codebase — session start/end, app open, and (unless disabled, §9.6.1) automatic screen tracking derived from the native navigation stack. Layer 1 cannot intercept any of this, because it never passes through `AnalyticsTracker` at all. `FirebaseAnalyticsTracker` therefore independently subscribes to `AnalyticsConsentProvider.consentState` and calls the vendor SDK's own `setAnalyticsCollectionEnabled(false/true)` (Mixpanel's equivalent: `optOutTracking()`/`optInTracking()`) on every change — this is the only mechanism that stops the vendor SDK's *own* internal collection.

#### 9.3.3 Fail-closed at construction — "before the SDK is even initialized," concretely
A DI-constructed singleton cannot literally defer object construction until an async consent read completes without either blocking DI graph assembly or introducing nullable/lazy-everywhere plumbing throughout the codebase — both worse trade-offs than the one actually implemented: `FirebaseAnalyticsTracker.init` calls `native.setAnalyticsCollectionEnabled(false)` **synchronously, as the very first statement**, before it ever subscribes to the real consent Flow (§6.4). The practical guarantee is identical to "never initialized until consent is known" — the SDK's collection capability starts disabled and is only ever flipped on by an affirmative, already-resolved `true` consent read. There is no window, race, or code path where the native SDK defaults to enabled.

### 9.4 Identifiers — never a raw, persistent, or per-child identifier

COPPA classifies persistent identifiers used to recognize a user over time as personal information when collected from a child. Accordingly:
- **`setUserId` must never receive a raw account ID, family ID, email, phone number, or — under any circumstance — a per-child identifier.** `core-security`'s already-built `secureHash()` (Phase3 KMP 17 §3.1 confirms it stays SHA-256, purpose-built for exactly this: *"irreversible pseudonymization of identifiers for telemetry"*) is the mandatory transform for any identifier passed to `setUserId`; this document's job is only to enforce that at the transport boundary, not to decide who calls `setUserId` with what — that stays each feature's own concern per §2.2.
- **`FirebaseAnalyticsTracker.setUserId` defensively validates the shape of whatever it receives** (`AnalyticsParamSanitizer.looksLikeOpaqueHashedId`, §9.5) — a 64-character lowercase hex string matching `secureHash()`'s SHA-256 output shape is accepted; anything else (a UUID, an email-shaped string, a short numeric ID) is refused and logged as a warning, never forwarded. This is defense-in-depth against a future call site mistake, not the primary control (the primary control is: don't call `setUserId` with the wrong thing in the first place, which is each caller's responsibility).
- **No child-scoped identifier of any kind — hashed or not — is ever an acceptable `setUserId` value**, even under Option A of §9.2. Analytics identity, if used at all, is family/account-scoped only.

### 9.5 `AnalyticsParamSanitizer` — defense-in-depth PII filtering

`CORE_ANALYTICS_INSTRUCTIONS.md` §6 already tells every caller "DO NOT pass PII... in `params`." This document does not relax that expectation — it adds a second, structural layer that does not depend on every caller getting it right every time, consistent with `core-analytics`'s own stated responsibility (§1 of that document: *"Privacy Safety: Provide a centralized point for PII redaction and filtering before events are dispatched to external providers"*) — a responsibility that was documented but never actually implemented until this document.

```kotlin
package com.noorheroes.core.analytics.sanitizer

import com.noorheroes.core.logger.NoorHeroesLogger

object AnalyticsParamSanitizer {

    // Substring match, case-insensitive, against the param KEY — deliberately broad.
    // child_id/childid/profile_id/student_id are banned here specifically because no
    // per-child identifier is ever acceptable for real-SDK-bound analytics (§9.4), regardless
    // of what any individual feature's blueprint might otherwise intend to send.
    private val BANNED_KEY_TOKENS = listOf(
        "email", "e_mail", "phone", "msisdn", "name", "first_name", "last_name", "full_name",
        "address", "street", "dob", "date_of_birth", "birthdate", "ssn", "password", "pin",
        "token", "auth_token", "refresh_token", "access_token", "device_id", "advertising_id",
        "idfa", "gaid", "ip", "ip_address", "lat", "lng", "latitude", "longitude",
        "child_id", "childid", "profile_id", "student_id", "school",
    )

    private val EMAIL_SHAPE = Regex("""[^\s@]+@[^\s@]+\.[^\s@]+""")
    private val PHONE_SHAPE = Regex("""\+?\d[\d\s\-().]{7,}\d""")
    private val OPAQUE_SHA256_HEX = Regex("^[a-f0-9]{64}$")

    // Firebase Analytics' own published limits (confirm current values against Firebase's
    // official docs at implementation time — vendor limits can change) — enforced here so a
    // param that would otherwise cause Firebase to silently drop the *whole event* is instead
    // truncated/dropped at the param level, and so Mixpanel (if added) inherits the same
    // conservative caps rather than needing its own separate tuning pass.
    private const val MAX_PARAM_NAME_LENGTH = 40
    private const val MAX_PARAM_VALUE_LENGTH = 100
    private const val MAX_PARAMS_PER_EVENT = 25

    fun sanitize(eventName: String, params: Map<String, Any?>, logger: NoorHeroesLogger): Map<String, Any?> {
        val result = LinkedHashMap<String, Any?>()
        for ((key, value) in params) {
            if (result.size >= MAX_PARAMS_PER_EVENT) {
                logger.warn(TAG, "Event '$eventName' exceeded $MAX_PARAMS_PER_EVENT params; truncated.")
                break
            }
            val lowerKey = key.lowercase()
            if (key.length > MAX_PARAM_NAME_LENGTH || BANNED_KEY_TOKENS.any { lowerKey.contains(it) }) {
                logger.warn(TAG, "Dropped param '$key' on event '$eventName' (banned key or name too long).")
                continue
            }
            val stringValue = value?.toString()
            if (stringValue != null && (EMAIL_SHAPE.matches(stringValue) || PHONE_SHAPE.matches(stringValue))) {
                logger.warn(TAG, "Dropped param '$key' on event '$eventName': value shape looks like PII.")
                continue
            }
            result[key] = stringValue?.take(MAX_PARAM_VALUE_LENGTH) ?: value
        }
        return result
    }

    /** Used by FirebaseAnalyticsTracker.setUserId (§9.4) — accepts only a secureHash()-shaped value. */
    fun looksLikeOpaqueHashedId(id: String): Boolean = OPAQUE_SHA256_HEX.matches(id)

    private const val TAG = "AnalyticsParamSanitizer"
}
```

This runs for **every** real-SDK-bound call (`FirebaseAnalyticsTracker`, and `MixpanelAnalyticsTracker` if built) — it does not run inside `LoggerAnalyticsTracker`, which is dev-console-only and already excluded from the "real collection" concern this entire section addresses.

### 9.6 Platform and vendor-console configuration specific to a children's product

#### 9.6.1 Android manifest
```xml
<!-- AndroidManifest.xml, application-level meta-data -->
<meta-data android:name="google_analytics_default_allow_ad_personalization_signals" android:value="false" />
<meta-data android:name="google_analytics_automatic_screen_reporting_enabled" android:value="false" />
<meta-data android:name="google_analytics_adid_collection_enabled" android:value="false" />
```
- **Ad personalization signals off:** non-negotiable for a children's app — behavioral advertising is exactly the category COPPA and the FTC's COPPA enforcement guidance treat as prohibited without verifiable parental consent that goes well beyond ordinary analytics consent; this document does not attempt to support ad personalization at all, ever, regardless of consent state.
- **Automatic screen reporting off:** `logScreenView` already gives every screen transition explicitly and deliberately (§6.4); leaving Firebase's automatic Activity/Fragment-name capture on would both double-count and leak internal navigation-class names (an unreviewed, uncontrolled data surface) into the analytics stream.
- **Advertising ID collection off:** an IDFA/GAID-class identifier is exactly the kind of cross-app, persistent identifier COPPA's "personal information" definition was extended to cover; this must be off unconditionally, not merely consent-gated the way ordinary event params are.

#### 9.6.2 iOS Info.plist / GoogleService-Info.plist
- Set `FIREBASE_ANALYTICS_COLLECTION_ENABLED` to `false` as the plist default (mirrors the Android fail-closed default at the manifest level, redundant with but not a substitute for §6.4's runtime `init` block).
- Confirm the project does not link `AdSupport.framework`/request `ASIdentifierManager`'s advertising identifier anywhere in the app target — if it does for an unrelated reason, that is a pre-existing issue this document flags but does not fix (out of scope, §2.2), since it is unrelated to this module's own code.

#### 9.6.3 If Mixpanel is ever added
Mixpanel's Session Replay / Autocapture features **must be explicitly disabled** (`mixpanel.getPeople()`... session-replay and autocapture initialization flags left off / explicitly set to disabled at SDK init). These features record UI content and interaction streams that this document's `AnalyticsParamSanitizer` cannot filter, because they bypass the `AnalyticsTracker` interface entirely, the same class of gap layer 2 exists to close for *known* automatic events — an unreviewed screen-recording-adjacent feature is not an acceptable trade for "product-analytics depth" in a children's product, full stop.

#### 9.6.4 Firebase project console (prerequisite, not code — §15.1, §16.1)
Before any production traffic reaches this pipeline: Google Signals disabled at the Firebase/Google Analytics property level, ad personalization disabled at the property level (belt-and-suspenders with §9.6.1's manifest flag), and a conservative data-retention window configured (Google Analytics for Firebase supports a configurable retention period — set it to the shortest value that still serves the product's legitimate analytics needs, not the vendor default).

### 9.7 Validation
- `AnalyticsParamSanitizer.sanitize` never throws — a malformed or unexpected param value degrades to "dropped and logged," never an exception (§9.5, §10).
- `AnalyticsConsentProvider` implementations never throw from either member — `ConsentLedgerAnalyticsConsentProvider`'s `catch { emit(false) }` (§6.2.2) ensures a consent-read failure fails closed, never open, and never propagates.

---

## 10. Error Handling and Edge Cases

| Scenario | Required behavior |
|---|---|
| Firebase/GitLive SDK throws during `FirebaseAnalyticsTracker.init` (e.g., misconfigured `google-services.json`, missing `GoogleService-Info.plist`) | Caught inside `init`'s own `runCatching` (§6.4); app startup continues unaffected; a warning is logged via `NoorHeroesLogger` (never the crash reporter, to avoid recursive analytics-about-analytics noise); this tracker effectively becomes a safe no-op for the remainder of the process, and `LoggerAnalyticsTracker`'s console output continues unaffected since it does not depend on this object at all. |
| Any single `AnalyticsTracker` call throws inside a real tracker (native SDK edge case, malformed input despite validation) | Caught by that tracker's own `safely { }` wrapper (§6.4) — never propagates to `CompositeAnalyticsTracker`, never to the calling ViewModel. `CORE_ANALYTICS_INSTRUCTIONS.md`'s existing non-blocking/never-throws contract is upheld for the real implementation exactly as it already is for `LoggerAnalyticsTracker`. |
| `AnalyticsConsentProvider`'s underlying `ConsentRepository.observeConsentStatus` Flow throws or the network read fails | `.catch { emit(false) }` (§6.2.2) — fails closed, `isAnalyticsCollectionAllowed()` returns `false` until a subsequent successful read arrives. Never fails open. |
| Consent revoked while an event is mid-flight inside the native SDK's own internal queue (already accepted by `logEvent` before revocation) | Not retractable, and this document does not attempt to retract it — Firebase/Mixpanel's own local queue does not expose a "cancel a pending event" API. This is an accepted limitation: the gate stops *new* collection immediately (§6.7); it cannot un-send an event the native SDK already internally queued microseconds earlier. This is the same limitation any consent-gated analytics pipeline built on a vendor SDK's own opaque local queue has, and is not specific to a flaw in this design. |
| App launches fully offline | Real trackers still accept calls (subject to the consent gate) — Firebase/Mixpanel's native SDKs queue locally and flush on reconnect (§8); `ConsentLedgerAnalyticsConsentProvider` serves its last-cached consent value (per C.26's own offline-first cache, K-02 §19) rather than blocking or defaulting to denied purely because of connectivity (denial is reserved for "no consent value has ever been successfully read," not "currently offline with a previously-confirmed value in cache"). |
| A feature ViewModel passes a param that collides with a Firebase-reserved prefix (`google_`, `firebase_`, `ga_`) or an invalid event-name character | Not this document's concern to validate exhaustively — `AnalyticsParamSanitizer` handles PII-shaped and oversized values; full Firebase naming-convention validation is a per-feature-blueprint concern (§2.2) since it requires knowing the actual event/param names in use, which this document deliberately does not define. |
| `ConsentGatedAnalyticsTracker`'s `delegate` (the real-transport composite) is empty (e.g., `core-analytics-mixpanel` not included and, hypothetically, `FirebaseAnalyticsTracker`'s binding fails to resolve) | `CompositeAnalyticsTracker` with zero children is already a safe no-op per its existing, unmodified implementation — no special-casing needed here. |
| A QA/internal test build needs to exercise the real SDK path without a real parent consent flow (§14.6) | Use `AlwaysGrantedAnalyticsConsentProvider` (§5) bound only in that build variant's own Koin module, never in staging/production — this is a test double, not a bypass mechanism shipped to real users; its existence and binding scope must be covered by the Task 15 self-check (§13). |

---

## 11. State Management and Lifecycle Considerations

### 11.1 Scope of the background consent subscription
`ConsentLedgerAnalyticsConsentProvider`'s `init` block launches a coroutine that must live for the entire app process, not a single screen — it cannot use a `viewModelScope` (destroyed on navigation) or any screen-scoped lifecycle. **Confirm whether `core-common`'s DI graph already exposes a process-lifetime `CoroutineScope` singleton** (a natural candidate given `core-common`'s `di` package already hosts `GlobalKoinHolder`, per `CORE_COMMON_INSTRUCTIONS.md` §3/§4) **before adding a new one.** If none exists:
```kotlin
// core-common, di package — ADD only if no equivalent already exists (Task 01, §13)
val commonCoroutineModule = module {
    single<CoroutineScope>(qualifier = named("AppScope")) {
        CoroutineScope(SupervisorJob() + Dispatchers.Default)
    }
}
```
`FirebaseAnalyticsTracker`'s own `appScope` dependency (§6.4) uses the same scope, for the same reason.

### 11.2 Cold-start ordering and the accepted early-event gap
Restated from §8: `ConsentLedgerAnalyticsConsentProvider`'s `_consentState` starts at `false` and only flips once its background collector's first emission arrives. Because it reads from C.26's already-cached, offline-first consent list (K-02 §19), this is typically a low-single-digit-millisecond gap, not a network round trip — but it is not zero. A small number of the very first events in a session (most likely a splash-screen `logScreenView`) may be dropped even when the family's actual consent state is `granted`. This is intentional (§8) and must not be "fixed" with a pre-consent buffer (§8 explains why that would itself violate the gating requirement).

### 11.3 Backgrounding / foregrounding
No custom lifecycle handling is required from this module — Firebase's and Mixpanel's native SDKs already flush their own local queues on backgrounding per their standard lifecycle hooks. `ConsentGatedAnalyticsTracker` and `AnalyticsConsentProvider` hold no lifecycle-sensitive state beyond the `StateFlow` snapshot, which remains valid (and continues updating in the background scope) across backgrounding.

### 11.4 Child-profile switching vs. logout
- **Switching the active child profile under an already-authenticated parent** does not change the analytics consent gate (§9.2 — consent is family-scoped, not per-child) and requires no special handling in this module.
- **Logout** already triggers `tracker.reset()` per each feature's own existing convention (`CORE_ANALYTICS_INSTRUCTIONS.md` §6 "Do" — *"Call reset() during the logout flow"*, unchanged by this document). Because `ConsentGatedAnalyticsTracker.reset()` always forwards regardless of current consent state (§6.3), a real vendor SDK's user-level state is reliably cleared at logout even in the edge case where consent happened to be withdrawn at that exact moment.

---

## 12. Integration Points with Existing Modules

### 12.1 Every ViewModel (via `core-ui`'s constructor-injection convention)
Zero change. ViewModels continue to receive `AnalyticsTracker` via constructor injection exactly as `CORE_ANALYTICS_INSTRUCTIONS.md` §4.1 already documents, and `CORE_UI_INSTRUCTIONS.md`'s `BaseViewModel` pattern is unaffected — this document changes only which concrete implementation Koin resolves behind that interface per build environment (§6.5). No `BaseViewModel` file is touched.

### 12.2 C.26 `ConsentRepository` — new dependency, one direction only
`ConsentLedgerAnalyticsConsentProvider` (composition root) depends on C.26's `ConsentRepository`. **`core-analytics` itself gains zero new dependency** — the module-dependency rule stated in `CORE_ANALYTICS_INSTRUCTIONS.md` §2 (*"core-analytics depends only on core-common"*) remains literally true, because the adapter class that actually touches `ConsentRepository` lives outside `core-analytics`, at the composition root, which is the one layer in this architecture allowed to see every module. If `ConsentRepository` needs a new reactive accessor, §6.2.3 specifies exactly and only that addition.

### 12.3 `core-crash` — shared Firebase project infrastructure, not shared code
`core-crash`'s own gap-closure work (its Firebase Crashlytics binding — a separate, independently-scoped document, not this one) will need the same Firebase project, the same `google-services.json`/`GoogleService-Info.plist`, and ideally the same GitLive BoM version this document establishes. **Whichever of the two ships first should set up that shared project configuration once; the other should reuse it, not duplicate it.** This is a coordination note, not a code dependency — `core-analytics-firebase` and `core-crash`'s eventual implementation remain independent Gradle modules with no compile-time relationship to each other.

### 12.4 `core-datastore-remote-config` (Phase3 KMP 16) — optional operational kill-switch
Not required for this Definition of Done, but recommended for production readiness (§15.3): a remote-config boolean flag (e.g., `analytics_collection_killswitch`) that, when engaged, forces real collection off **regardless of consent state** — an emergency operational control (e.g., a cost spike, a vendor incident, a discovered PII leak requiring an immediate global stop) independent of and faster to flip than shipping a new app release. The composition must always be `finalEnabled = consentGranted && !killSwitchEngaged` — the kill switch can only ever turn collection *off*, never *on* in place of a missing consent grant.

### 12.5 `core-security`'s `secureHash()`
Referenced, not modified (§9.4) — the mandatory transform for any identifier a feature passes to `setUserId`.

---

## 13. Development Steps in the Correct Implementation Order

**Task 01 — Confirm the exact shape of everything this document assumes but does not have direct sight of.**
Locate: (a) `ConsentRepository`'s current exact interface and whether a reactive single-type accessor already exists (§6.2.3); (b) the project's existing `AppEnvironment`-equivalent config enum (§6.5); (c) whether a process-lifetime `CoroutineScope` singleton already exists in `core-common`'s DI graph (§11.1); (d) the existing composition-root pattern used for an equivalent adapter like `AuthStateProvider`'s implementation, to place `ConsentLedgerAnalyticsConsentProvider` consistently (§5's folder-structure note); (e) whether `google-services.json`/`GoogleService-Info.plist` already exist in the repo from prior Firebase-adjacent work. Do not proceed on an assumed answer to any of these five.

**Task 02 — Implement `AnalyticsParamSanitizer` and its unit tests (§9.5).**
Pure logic, zero platform/vendor dependency — build and test first, as the foundation the real trackers depend on.

**Task 03 — Implement `AnalyticsConsentProvider`, `AlwaysDeniedAnalyticsConsentProvider`, and `AlwaysGrantedAnalyticsConsentProvider` (§6.2, §5) in `core-analytics`.**

**Task 04 — Implement `ConsentGatedAnalyticsTracker` and its unit tests (§6.3, §14.2).**
Depends only on the interfaces from Tasks 02–03 — no real vendor SDK involved yet, fully testable in isolation.

**Task 05 — Create the `core-analytics-firebase` Gradle module; add the GitLive dependency; confirm/add Firebase project config files per Task 01(e).**

**Task 06 — Implement `FirebaseAnalyticsNative` and `GitLiveFirebaseAnalyticsNative` (§6.4).**
Confirm during this task whether the GitLive adapter can live in `commonMain` directly or must be per-platform-source-set (§5's file-structure note) — resolve empirically, do not assume.

**Task 07 — Implement `FirebaseAnalyticsTracker` (§6.4) and its unit tests against a fake `FirebaseAnalyticsNative` (§14.3).**
Confirm the fail-closed `init` behavior and the reactive layer-2 toggle both have direct test coverage — these are the two highest-value tests in this entire document (§14.3).

**Task 08 — Add the Android manifest meta-data and iOS Info.plist entries (§9.6.1, §9.6.2).**

**Task 09 — Implement `ConsentLedgerAnalyticsConsentProvider` and, if required by Task 01(a), the `ConsentRepository.observeConsentStatus` addition (§6.2.2, §6.2.3).**

**Task 10 — Wire the environment-aware composition (`analyticsModule` additions + the new composition-root module, §6.5) into `initKoin()`.**
Confirm `LoggerAnalyticsTracker` alone is still exactly what a Debug-environment Koin graph resolves — this is the single most important regression check in this task (§18.1).

**Task 11 — (Optional, only if §16.1's Mixpanel prerequisite is confirmed) implement `core-analytics-mixpanel` per §3.5/§5, mirroring Tasks 05–07's shape.**

**Task 12 — (Optional, recommended for production readiness) wire the remote-config kill-switch per §12.4, once Phase3 KMP 16's remote-config bootstrap is available.**

**Task 13 — Correct `CORE_ANALYTICS_INSTRUCTIONS.md`.**
Add a new subsection under §4 documenting: the real `FirebaseAnalyticsTracker` binding and which environments resolve it; the `personalization`-consent gate and the §9.2 flag that it awaits product/legal confirmation; that `setUserId` must only ever receive a `secureHash()`-produced value and never a per-child identifier. Update §5's Scenario 2 to state it is now implemented, pointing at this document, rather than describing it as a hypothetical future step.

**Task 14 — Full test suite (§14) and manual DebugView/Live-View verification (§14.5).**

**Task 15 — Final review self-check:** confirm zero direct vendor SDK import (`dev.gitlive.firebase.*`, `com.mixpanel.*`) exists anywhere outside `core-analytics-firebase`/`core-analytics-mixpanel` (a grep-level check enforcing `CORE_ANALYTICS_INSTRUCTIONS.md` §6's "Don't use concrete SDK classes in feature modules" rule, now actually true rather than merely stated); confirm a Debug-environment build resolves `LoggerAnalyticsTracker` and touches no vendor code at all; confirm no test or production code path can reach `FirebaseAnalyticsTracker.setUserId` with a value that is not `secureHash()`-shaped.

---

## 14. Testing Strategy and Acceptance Criteria

### 14.1 Unit — `AnalyticsParamSanitizer`
- Every entry in `BANNED_KEY_TOKENS` is dropped, case-insensitively, with a substring match (e.g., `"Customer_Email"` is caught by `"email"`).
- A value that matches the email or phone shape regex is dropped even under an innocuous key name.
- A param list over `MAX_PARAMS_PER_EVENT` is truncated, not silently accepted in full or thrown on.
- `looksLikeOpaqueHashedId` accepts a 64-char lowercase hex string and rejects a UUID, an email string, and a short numeric string.

### 14.2 Unit — `ConsentGatedAnalyticsTracker`
- With a fake `AnalyticsConsentProvider` reporting `false`: zero calls reach the delegate for `logEvent`/`logScreenView`/`setUserProperty`/`setUserId`.
- With the same fake reporting `true`: every call passes through unmodified.
- `reset()` reaches the delegate in **both** consent states — the one deliberate bypass (§6.3), and the single most important test in this file to get right, since it is the one place this document intentionally departs from "gate everything."
- Flipping the fake's underlying `StateFlow` from `true` to `false` mid-test causes the very next call, and every call after it, to be dropped — no call issued after the flip reaches the delegate.

### 14.3 Unit — `FirebaseAnalyticsTracker` (against a fake `FirebaseAnalyticsNative`)
- **The fail-closed init test:** immediately after construction, before any consent value has ever been emitted, assert `native.setAnalyticsCollectionEnabled(false)` was called — this is the test that proves §9.3.3's "before the SDK is even initialized" claim is actually true in code, not just in the design narrative.
- **The reactive toggle test:** emit `true` then `false` on a fake `AnalyticsConsentProvider.consentState`; assert `native.setAnalyticsCollectionEnabled` was called with `true` then `false`, in that order, closely following each emission.
- `logEvent`/`logScreenView` route params through `AnalyticsParamSanitizer` before reaching `native.logEvent` (verify a banned-key param never reaches the fake native seam).
- `setUserId` forwards a `secureHash()`-shaped value and refuses (never forwards) a UUID-shaped or email-shaped one, logging a warning in the refusal case (§9.4).
- Every public method swallows an exception thrown by the fake `native` and never propagates it to the caller (§10).

### 14.4 Integration — `ConsentLedgerAnalyticsConsentProvider`
- With a fake `ConsentRepository` whose `observeConsentStatus` Flow emits `Granted`: `isAnalyticsCollectionAllowed()` becomes `true`.
- With the same fake emitting `Withdrawn`: becomes `false`.
- With the same fake's Flow throwing: `isAnalyticsCollectionAllowed()` remains/becomes `false` (fail-closed on error, §10).
- Cold-start default (before any emission): `isAnalyticsCollectionAllowed()` is `false` (§9.2, §11.2).

### 14.5 Manual acceptance criterion — the test event actually appears in the vendor's debug view
This is the acceptance criterion the task brief calls out explicitly, and it must be performed honestly through the real consent gate, not by bypassing it:
1. On a build variant with `AlwaysGrantedAnalyticsConsentProvider` bound (§5, §10 — never a staging/production binding), enable Firebase DebugView: Android — `adb shell setprop debug.firebase.analytics.app <applicationId>`; iOS — add the `-FIRDebugEnabled` launch argument in the Xcode scheme.
2. Trigger any existing ViewModel call that already emits an event (any feature's existing `tracker.logEvent(...)` call — this document does not add a new one, §2.2).
3. Confirm the event appears in the Firebase console's DebugView within a few seconds, carrying no banned-key params and no raw identifier as `user_id`.
4. Repeat with `AlwaysDeniedAnalyticsConsentProvider` (or the real `ConsentLedgerAnalyticsConsentProvider` against a test family with `personalization` withdrawn) bound instead, and confirm **no** event appears — this negative case is just as important a pass/fail criterion as the positive one.
5. If `core-analytics-mixpanel` is built: repeat via Mixpanel's "Events → Live View."

### 14.6 Acceptance criteria (summary)
- [ ] `AnalyticsParamSanitizer` unit tests (§14.1) pass.
- [ ] `ConsentGatedAnalyticsTracker` unit tests (§14.2) pass, including the `reset()`-always-forwards case.
- [ ] `FirebaseAnalyticsTracker`'s fail-closed-init and reactive-toggle tests (§14.3) pass.
- [ ] `ConsentLedgerAnalyticsConsentProvider` integration tests (§14.4) pass, including the fail-closed-on-error case.
- [ ] A manually triggered test event is visible in Firebase DebugView when consent is granted (§14.5 step 3), and provably absent when consent is denied/withdrawn (§14.5 step 4).
- [ ] A Debug-environment Koin graph resolves `LoggerAnalyticsTracker` alone — zero vendor SDK code executes (§14, Task 15 self-check).
- [ ] Zero call site outside `core-analytics-firebase`/`core-analytics-mixpanel` imports a concrete vendor SDK class (grep-level check).
- [ ] Every existing ViewModel and its existing tests compile and pass unmodified (interface-stability proof, §18.1).

---

## 15. Production-Readiness Considerations

### 15.1 Firebase project console configuration (prerequisite, must be done before real users are exposed to a build with this binding active)
Google Signals disabled; ad personalization signals disabled at the property level; a conservative event-data retention window configured (§9.6.4). None of this is code — it is a one-time Firebase console configuration step, and this document's Definition of Done (§17) treats it as a required checklist item precisely because it is easy to forget when all the visible work is code.

### 15.2 App-store privacy declarations
Both the Play Console "Data safety" section and the App Store "App Privacy" (nutrition label) declarations need updating to reflect the new data collection this module introduces (App Interactions / Usage Data, declared as not linked to identity if the `setUserId` discipline in §9.4 holds, and never used for advertising per §9.6.1). This is a store-listing/compliance task, not code, but it is blocked on this module's exact final behavior and should be scheduled alongside it, not forgotten as a follow-up.

### 15.3 Operational kill-switch (recommended, not required — §12.4)
Wiring `core-datastore-remote-config`'s bootstrap once it is available gives an instant, release-independent way to halt real collection platform-wide if a problem is discovered post-launch (a cost spike, a vendor-side incident, a newly-discovered PII leak in some feature's event params that the sanitizer's deny-list didn't anticipate). Strongly recommended before this ships broadly; not blocking for an initial internal/staged rollout.

### 15.4 Staged rollout
Given the kill-switch in §15.3 (or, absent it, a build-level feature flag), consider enabling the real transport for a small internal/QA cohort first, confirming DebugView output and cost/volume are as expected, before flipping it on for all production traffic — standard practice for any new telemetry pipeline, doubly warranted here given the compliance stakes.

### 15.5 Coordination with `core-crash`
Per §12.3 — set up Firebase project infrastructure once, shared, not duplicated across the two modules' eventual gap-closures.

---

## 16. Dependencies / Prerequisites

### 16.1 Prerequisite decisions not yet made — must be resolved before or during implementation, not silently assumed
1. **A Firebase project must exist (or be created) for this app**, with `google-services.json`/`GoogleService-Info.plist` available to the build. Confirm during Task 01 whether one already exists from adjacent work (`core-crash`, `core-datastore-remote-config`) before creating a new one.
2. **Product/legal sign-off on the `personalization`-consent mapping decision (§9.2).** This document implements the mapping as its interim, technically-sound answer and flags it for confirmation — it does not claim the ambiguity is resolved. Do not treat §9.2's decision as unquestionable; escalate if asked.
3. **A Mixpanel account/project, if and only if the team opts into building `core-analytics-mixpanel` (§3.5, §16.1).** Not required for this Definition of Done.

### 16.2 Already-built dependencies this document relies on
- `core-common` — `LogSeverity`, `AppError`, DI primitives, `config` package's environment handling.
- `core-security`'s `secureHash()` (Phase3 KMP 17).
- C.26's `ConsentRepository` and its underlying consent ledger (K-02 and its backend).
- `core-analytics` itself — `AnalyticsTracker`, `LoggerAnalyticsTracker`, `CompositeAnalyticsTracker`.

---

## 17. Definition of Done

- [ ] `FirebaseAnalyticsTracker`, `FirebaseAnalyticsNative`/`GitLiveFirebaseAnalyticsNative`, `ConsentGatedAnalyticsTracker`, `AnalyticsConsentProvider` (+ its two provided implementations), and `AnalyticsParamSanitizer` are implemented exactly per §6–§9.
- [ ] `AnalyticsTracker`'s interface is byte-for-byte unchanged; every existing ViewModel and its existing test suite compiles and passes with zero modification.
- [ ] `LoggerAnalyticsTracker` remains the sole binding for Debug-environment Koin graphs, verified by a test (§14.6) — the no-op path this document must not break is provably still intact.
- [ ] Real analytics collection is gated at both layers (§9.3): explicit calls via `ConsentGatedAnalyticsTracker`, and the vendor SDK's own automatic collection via each real tracker's reactive native toggle.
- [ ] The native SDK defaults to collection-disabled at construction, before any consent value has ever been read (§9.3.3), verified by the Task 07 fail-closed-init test.
- [ ] `setUserId` never forwards a value that is not `secureHash()`-shaped, and never forwards a per-child identifier under any circumstance (§9.4).
- [ ] `AnalyticsParamSanitizer` is applied to every real-SDK-bound call and its deny-list/shape checks pass their full test suite (§14.1).
- [ ] Android manifest and iOS Info.plist changes from §9.6.1/§9.6.2 are in place (ad personalization off, automatic screen reporting off, ADID collection off).
- [ ] A test event is confirmed present in Firebase DebugView when consent is granted, and confirmed absent when consent is denied/withdrawn (§14.5).
- [ ] `CORE_ANALYTICS_INSTRUCTIONS.md` is corrected per §13 Task 13.
- [ ] The §9.2 consent-mapping decision is explicitly flagged for product/legal confirmation in both this document and the corrected instructions file — not silently presented as settled.
- [ ] Full test suite (§14) passing; the Task 15 grep-level self-check (§13) confirms zero direct vendor SDK usage outside the two new provider modules.

---

## 18. Assumptions or Decisions the Coding Agent Must Follow

1. **Firebase Analytics via GitLive is the required default transport; Mixpanel is optional and deferred (§3.1, §3.5).** Do not build `core-analytics-mixpanel` as part of this Definition of Done unless explicitly directed — it is fully specified so that doing so later is a scoped addition, not a design exercise, but building it unprompted expands this task's actual scope.
2. **The `AnalyticsTracker` interface does not change, under any circumstance, for any reason.** Every real implementation conforms to it exactly as it exists today; do not add an overload, a new method, or a changed default parameter, even if it would make the real implementation marginally cleaner.
3. **`LoggerAnalyticsTracker` stays exactly as it is and stays the sole binding for local/debug builds.** This is not merely "don't delete it" — it means the environment-aware composition in §6.5 must be additive, and a Debug-environment Koin graph must provably touch zero vendor SDK code (§14.6, Task 15).
4. **The consent gate binds to the existing `personalization` consent type (§9.2), not a new type, for this Definition of Done.** This is a documented, flagged interim decision — implement it as specified, do not silently substitute a different existing consent type, and do not silently invent a new consent-ledger type or database migration on your own initiative; that is Option A's territory and requires sign-off this document does not have.
5. **Fail-closed is the rule everywhere in this document, without exception:** default consent state, error handling on a consent-read failure, and the native SDK's collection-enabled flag at construction all default to "no collection" and only ever move to "collection allowed" on an affirmative, successful, positive read. Never invert this for convenience, testing ease, or perceived low risk.
6. **No pre-consent event buffering/replay (§8).** This was evaluated and deliberately rejected; do not add one to "avoid losing early events" — the loss of a handful of cold-start events is the accepted cost of the fail-closed guarantee, not a bug.
7. **`reset()` is the one method that always bypasses the consent gate (§6.3, §9.3.1).** Every other method is gated; this one is not. Do not gate it "for consistency," and do not extend the bypass to any other method.
8. **Never call a concrete vendor SDK class from any feature/ViewModel code.** All vendor-specific code lives inside `core-analytics-firebase` (and, if built, `core-analytics-mixpanel`) — this is an existing rule (`CORE_ANALYTICS_INSTRUCTIONS.md` §6), now made structurally checkable via the Task 15 grep self-check, not a new one.
9. **`setUserId` must reject anything that does not look like a `secureHash()` output (§9.4).** Do not weaken this to "trust the caller" even though the interface signature (`String?`) offers no compile-time way to enforce it — the runtime shape check in `FirebaseAnalyticsTracker` is the enforcement point, and it must not be removed for convenience.

---

## AI Agent Development Prompt

You are implementing the real analytics SDK binding for NoorHeroes' KMP `core-analytics` module. Read this entire document (`Phase3_Shared_Core_Modules.KMP.19-core-analytics-production-sdk-binding.md`) fully before writing any code. It contains a vendor decision, a two-layer consent-gating architecture, and a fully-specified implementation — do not re-litigate the decisions in §3 and §9, execute them.

**The gap:** `core-analytics` already has a stable `AnalyticsTracker` interface that every ViewModel injects and calls, currently backed only by `LoggerAnalyticsTracker` (console output, goes nowhere). No real analytics SDK is wired in. `CORE_ANALYTICS_INSTRUCTIONS.md` §5 Scenario 2 already names this exact next step ("adding a new remote analytics provider... in a platform-specific module e.g. `core-analytics-firebase`") without ever executing it.

**What you are building, in order (full detail in §13):**
1. Confirm five unknowns before writing any code: `ConsentRepository`'s exact current interface, the project's existing environment-config enum, whether a process-lifetime `CoroutineScope` singleton already exists, the project's existing composition-root pattern for an adapter like `AuthStateProvider`, and whether Firebase project config files already exist from adjacent work (§13 Task 01). Do not assume any of these.
2. Build `AnalyticsParamSanitizer` (§9.5) and `AnalyticsConsentProvider` + its fail-closed default (§6.2) — pure logic, no vendor dependency, build and test first.
3. Build `ConsentGatedAnalyticsTracker` (§6.3) — the layer-1 gate. Every method except `reset()` checks consent before forwarding; `reset()` always forwards.
4. Create the `core-analytics-firebase` module. Add the GitLive Kotlin Firebase SDK (`dev.gitlive:firebase-analytics`). Build `FirebaseAnalyticsNative` (a testable seam) and `GitLiveFirebaseAnalyticsNative` (the real GitLive adapter).
5. Build `FirebaseAnalyticsTracker` (§6.4): its `init` block must synchronously disable native collection *before* subscribing to anything (fail-closed, §9.3.3); it must reactively subscribe to `AnalyticsConsentProvider.consentState` and toggle the native SDK's own `setAnalyticsCollectionEnabled` on every change (layer-2 gate, §9.3.2); every method routes params through `AnalyticsParamSanitizer`; `setUserId` refuses anything that isn't `secureHash()`-shaped (§9.4); every method swallows exceptions internally and never throws to the caller.
6. Add the Android manifest meta-data and iOS Info.plist entries disabling ad personalization signals, automatic screen reporting, and Advertising ID collection (§9.6.1, §9.6.2) — non-negotiable for a children's product.
7. Build `ConsentLedgerAnalyticsConsentProvider` at the composition root (exact location per Task 01's finding), bridging C.26's `ConsentRepository` into `AnalyticsConsentProvider`, gated on the `personalization` consent type (§9.2, §6.2.2). If `ConsentRepository` lacks a reactive single-type accessor, add exactly the one method specified in §6.2.3 and nothing else.
8. Wire the environment-aware DI composition (§6.5): Debug environments resolve `LoggerAnalyticsTracker` alone, unchanged from today; Staging/Production resolve `CompositeAnalyticsTracker(LoggerAnalyticsTracker, ConsentGatedAnalyticsTracker(realTransports, consentProvider))`.
9. Correct `CORE_ANALYTICS_INSTRUCTIONS.md` per §13 Task 13 — document the real binding, the consent gate, and the `personalization`-mapping flag.
10. Implement the full test suite (§14), including the fail-closed-init test, the reactive-toggle test, the `reset()`-always-forwards test, and the manual Firebase DebugView verification (§14.5) — trigger it through the real consent gate (granted and denied cases both), never by bypassing the gate.
11. (Optional, only if directed) build `core-analytics-mixpanel` per §3.5, mirroring the Firebase module's shape exactly, including its own reactive native opt-out/opt-in toggle and the mandatory disabling of Mixpanel's Session Replay/Autocapture features (§9.6.3).

**What you must NOT change:**
- The `AnalyticsTracker` interface — signatures stay exactly as they are today. Zero ViewModel changes anywhere in the codebase.
- `LoggerAnalyticsTracker` and `CompositeAnalyticsTracker` — reused as-is; `LoggerAnalyticsTracker` must remain the sole, unmodified binding for local/debug builds.
- `core-security`'s `secureHash()` — used, never modified.
- C.26's `ConsentRepository`, consent UI, or withdrawal flow — only additive if a reactive accessor is genuinely missing (§6.2.3); nothing else in that module changes.
- `core-crash`'s own (separate, out-of-scope) Firebase Crashlytics binding work — coordinate on shared Firebase project config (§12.3), do not implement or modify it.
- What events any feature logs, or their param names — that is each feature's own concern, not this document's.

**What you must never build, under any framing:**
- Any code path where a real analytics SDK's collection defaults to enabled before an affirmative consent read.
- Any buffer that stores an event emitted before consent is confirmed, intending to replay it later.
- Any call site outside `core-analytics-firebase`/`core-analytics-mixpanel` that imports a concrete vendor SDK class.
- Any `setUserId` call that could carry a raw or per-child identifier — enforce the `secureHash()`-shape check, do not remove it "to trust the caller."

**How to verify you're done (full checklist in §17):**
- `AnalyticsParamSanitizer`, `ConsentGatedAnalyticsTracker`, and `FirebaseAnalyticsTracker` unit tests all pass, including the fail-closed-init test and the `reset()`-always-forwards test.
- A Debug-environment Koin graph resolves `LoggerAnalyticsTracker` alone — prove this with a test, not by inspection.
- A manually triggered event appears in Firebase DebugView when a test build's consent is granted, and is provably absent when it is denied — both cases exercised through the real gate.
- A grep across the codebase for `dev.gitlive.firebase` and `com.mixpanel` imports returns nothing outside the two new provider modules.
- `CORE_ANALYTICS_INSTRUCTIONS.md` reflects the real binding and the consent gate, including the explicit flag on the `personalization`-mapping decision.
- Every existing ViewModel and its existing test suite compiles and passes unmodified.

If, during implementation, you discover a fact that contradicts this document's design — for example, `ConsentRepository` turns out to have no viable path to a reactive per-type accessor without a larger change than §6.2.3 anticipates, or the project already has an established, differently-shaped composition-root pattern that this document's placement guidance doesn't fit — **stop and escalate rather than improvising a silent workaround.** The consent-gating guarantee in §9 is this document's entire reason for existing; a shortcut taken under implementation pressure that weakens it is not an acceptable trade for shipping faster.
